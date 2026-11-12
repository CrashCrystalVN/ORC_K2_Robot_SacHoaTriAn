"""
=============================================================================
BỘ TRỘN ĐỘNG HỌC MECANUM & ĐIỀU KHIỂN TAY CẦM 2 JOYSTICK (FPS / ARCADE DRIVE)
ROBOT ORC K2 - GIẢI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
=============================================================================
Thiết kế chuẩn hóa 100%:
1. Joystick 1 (J1 - Cần Trái / Arcade Steering):
   - Gạt LÊN / XUỐNG : Vy > 0 (Đi TIẾN) / Vy < 0 (Đi LÙI)
   - Gạt TRÁI / PHẢI : Omega < 0 (Xoay TRÁI tại chỗ) / Omega > 0 (Xoay PHẢI tại chỗ)
   - Gạt CHÉO        : Vừa tiến/lùi vừa bẻ lái cua xe mượt mà
2. Joystick 2 (J2 - Cần Phải / Mecanum Strafe):
   - Gạt TRÁI / PHẢI : Vx < 0 (Trượt ngang TRÁI DIR_SL) / Vx > 0 (Trượt ngang PHẢI DIR_SR)
3. Bộ lọc Deadband (Vùng chết 5% - 8% quanh tâm 0) chống trôi xe khi buông tay.
4. Đường cong gia tốc phi tuyến (Exponential Sensitivity Curve) + Slew-Rate Limiter:
   Xe chuyển động cực êm ái, căn chỉnh hoa mượt mà, không giật nảy, không trượt bánh.
5. Ma trận động học 4 bánh Mecanum + Chuẩn hóa Desaturation chống bão hòa PWM:
   - V_FL = Vy + Vx + Omega
   - V_FR = Vy - Vx - Omega
   - V_RL = Vy - Vx + Omega
   - V_RR = Vy + Vx - Omega
=============================================================================
"""

import math
import asyncio
try:
    from micropython import const
except ImportError:
    const = lambda x: x
from constants import *
import config

def apply_deadband(val, deadband=7.0):
    """
    Bộ lọc vùng chết (Deadband):
    - Triệt tiêu hoàn toàn nhiễu và sai số cơ khí quanh tâm khi buông tay cầm.
    - Tái phân bố tuyến tính từ 0..100% để loại bỏ hiện tượng giật bước (no jump).
    """
    if abs(val) <= deadband:
        return 0.0
    sign = 1.0 if val > 0 else -1.0
    return sign * (abs(val) - deadband) / (100.0 - deadband) * 100.0

def apply_expo(val, expo=0.4):
    """
    Đường cong độ nhạy phi tuyến (Exponential Response Curve):
    - Dải tay gạt nhỏ (0..40%): Đáp ứng siêu mịn để tài xế căn chỉnh hoa Ø32mm.
    - Dải tay gạt lớn (70..100%): Tăng tốc tối đa để bứt tốc qua các đoạn thẳng.
    """
    if val == 0.0:
        return 0.0
    sign = 1.0 if val > 0 else -1.0
    norm = abs(val) / 100.0
    curved = (1.0 - expo) * norm + expo * (norm * norm)
    return sign * curved * 100.0

def slew_rate(target, current, accel_step=10, decel_step=16):
    """
    Bộ giới hạn gia tốc (Slew-Rate Limiter):
    - Ngăn chặn biến thiên công suất đột ngột gây quăng quật kết cấu tay nâng.
    - Đảm bảo gia tốc êm và phanh dứt khoát không rê trượt bánh Mecanum trên thảm.
    """
    diff = target - current
    if diff > 0:
        step = accel_step if current >= 0 else decel_step
        return current + min(diff, step)
    elif diff < 0:
        step = decel_step if current > 0 else accel_step
        return current - min(-diff, step)
    return current

def mecanum_kinematics_mix(vy, vx, omega, max_speed=100.0):
    """
    Ma trận động học 4 bánh Mecanum:
      V_FL = Vy + Vx + Omega
      V_FR = Vy - Vx - Omega
      V_RL = Vy - Vx + Omega
      V_RR = Vy + Vx - Omega

    Chuẩn hóa Desaturation:
    Nếu tổng thành phần vượt quá 100%, tự động co tỉ lệ toàn bộ 4 bánh
    để hướng vector chuyển động và góc xoay không bao giờ bị méo mó.
    """
    v_fl = vy + vx + omega
    v_fr = vy - vx - omega
    v_rl = vy - vx + omega
    v_rr = vy + vx - omega

    max_mag = max(abs(v_fl), abs(v_fr), abs(v_rl), abs(v_rr))
    if max_mag > 100.0:
        scale = 100.0 / max_mag
        v_fl *= scale
        v_fr *= scale
        v_rl *= scale
        v_rr *= scale

    speed_ratio = max_speed / 100.0
    return (
        int(v_fl * speed_ratio),
        int(v_fr * speed_ratio),
        int(v_rl * speed_ratio),
        int(v_rr * speed_ratio)
    )

class MecanumTeleopController:
    """
    Bộ điều khiển Teleop 2 Joystick chuyên nghiệp (FPS / Arcade Drive).
    Tương thích 100% với:
      1. Tay cầm không dây PS4 / Gamepad qua I2C (PS4GamepadReceiver).
      2. Ứng dụng điều khiển OhStem App qua Bluetooth BLE.
    """
    def __init__(self, robot, gamepad, max_speed=None):
        self.robot = robot
        self.gamepad = gamepad
        self.max_speed = max_speed if max_speed is not None else getattr(config, 'SPEED_TELEOP_NORMAL', 75)
        self.normal_speed = self.max_speed
        self.slow_speed = getattr(config, 'SPEED_TELEOP_SLOW', 40)
        self.turbo_speed = getattr(config, 'SPEED_TELEOP_TURBO', 100)
        self.is_precision_mode = False

        # Trạng thái vận tốc làm mịn hiện thời
        self.curr_vy = 0.0
        self.curr_vx = 0.0
        self.curr_omega = 0.0

        # Tham số cấu hình chuẩn từ config.py
        self.swap_xy = getattr(config, 'GAMEPAD_SWAP_XY', True)
        self.invert_vx = getattr(config, 'GAMEPAD_INVERT_VX', False)
        self.invert_vy = getattr(config, 'GAMEPAD_INVERT_VY', False)
        self.invert_omega = getattr(config, 'GAMEPAD_INVERT_OMEGA', False)
        self.deadband = getattr(config, 'JOYSTICK_DEADBAND', 7.0)
        self.expo = getattr(config, 'JOYSTICK_EXPO', 0.4)
        self.accel_rate = getattr(config, 'TELEOP_ACCEL_RATE', 10)
        self.decel_rate = getattr(config, 'TELEOP_DECEL_RATE', 16)

        # Bộ quản lý sự kiện nút bấm
        self._button_handlers = {}
        self._button_last_state = {}

    def on_button(self, button, callback):
        """Đăng ký hàm xử lý khi một nút trên Gamepad được nhấn."""
        self._button_handlers[button] = callback
        self._button_last_state[button] = 0

    def set_max_speed(self, speed):
        self.max_speed = max(min(100, int(speed)), 20)

    def toggle_precision_mode(self):
        """Bật/Tắt chế độ di chuyển chậm chính xác (Precision Mode)."""
        self.is_precision_mode = not self.is_precision_mode
        self.max_speed = self.slow_speed if self.is_precision_mode else self.normal_speed
        print(f"[TELEOP] Che do chinh xac (Precision Mode): {'BAT (40%)' if self.is_precision_mode else 'TAT (75%)'}")
        return self.is_precision_mode

    def get_raw_joystick(self):
        """
        Trích xuất và chuẩn hóa giá trị từ tay cầm:
        - J1 (Cần Trái - Arcade Steering):
            + Vy: Dọc J1 (Lên > 0 Tiến, Xuống < 0 Lùi)
            + Omega: Ngang J1 (Phải > 0 Xoay Phải, Trái < 0 Xoay Trái)
        - J2 (Cần Phải - Mecanum Strafe):
            + Vx: Ngang J2 (Phải > 0 Trượt Phải, Trái < 0 Trượt Trái)
        """
        d = self.gamepad.data
        raw_j1_vert = float(d.get(ALY, 0))   # Dọc J1 (Vy)
        raw_j1_horiz = float(d.get(ALX, 0))  # Ngang J1 (Omega - Xoay / Cua)
        raw_j2_horiz = float(d.get(ARX, 0))  # Ngang J2 (Vx - Trượt ngang Mecanum)

        # Đảo dấu trục nếu cấu hình yêu cầu
        if self.invert_vy:
            raw_j1_vert = -raw_j1_vert
        if self.invert_vx:
            raw_j2_horiz = -raw_j2_horiz
        if self.invert_omega:
            raw_j1_horiz = -raw_j1_horiz

        return raw_j1_vert, raw_j2_horiz, raw_j1_horiz

    async def run(self):
        """
        Vòng lặp điều khiển thời gian thực (50Hz - 20ms).
        """
        print("[MECANUM TELEOP] He thong dieu khien 2 Joystick (FPS/Arcade) DA KICH HOAT!")
        while True:
            # 1. Bỏ qua nếu đang chạy chiến thuật tự động giải mê cung
            if getattr(self.robot, 'mode_auto', False):
                await asyncio.sleep_ms(100)
                continue

            # 2. Xử lý sự kiện nhấn các nút tác vụ (Buttons)
            d = self.gamepad.data
            for btn, handler in self._button_handlers.items():
                state = d.get(btn, 0)
                if state and not self._button_last_state.get(btn, 0):
                    if handler is not None:
                        try:
                            await handler()
                        except Exception as e:
                            print(f"[BUTTON ERROR] {btn}: {e}")
                self._button_last_state[btn] = state

            # 3. Hỗ trợ phím D-Pad để di chuyển nhích từng milimet (Micro-Stepping)
            dpad_vy = 0.0
            dpad_vx = 0.0
            if d.get(BTN_UP, 0):
                dpad_vy += 35.0
            if d.get(BTN_DOWN, 0):
                dpad_vy -= 35.0
            if d.get(BTN_RIGHT, 0):
                dpad_vx += 40.0
            if d.get(BTN_LEFT, 0):
                dpad_vx -= 40.0

            if dpad_vy != 0.0 or dpad_vx != 0.0:
                target_vy = dpad_vy
                target_vx = dpad_vx
                target_omega = 0.0
            else:
                # 4. Đọc dữ liệu 2 Joystick
                raw_vy, raw_vx, raw_omega = self.get_raw_joystick()

                # Lọc vùng chết Deadband (5-8%)
                clean_vy = apply_deadband(raw_vy, self.deadband)
                clean_vx = apply_deadband(raw_vx, self.deadband)
                clean_omega = apply_deadband(raw_omega, self.deadband)

                # Làm mịn phi tuyến bằng đường cong Expo
                target_vy = apply_expo(clean_vy, self.expo)
                target_vx = apply_expo(clean_vx, self.expo)
                target_omega = apply_expo(clean_omega, self.expo)

            # 5. Bộ làm mịn gia tốc (Slew-Rate Limiter)
            self.curr_vy = slew_rate(target_vy, self.curr_vy, self.accel_rate, self.decel_rate)
            self.curr_vx = slew_rate(target_vx, self.curr_vx, self.accel_rate, self.decel_rate)
            self.curr_omega = slew_rate(target_omega, self.curr_omega, self.accel_rate, self.decel_rate)

            # 6. Dừng hoàn toàn nếu trong vùng trung hòa
            if abs(self.curr_vy) < 1.0 and abs(self.curr_vx) < 1.0 and abs(self.curr_omega) < 1.0:
                self.curr_vy = 0.0
                self.curr_vx = 0.0
                self.curr_omega = 0.0
                self.robot.stop()
            else:
                # 7. Tính toán vận tốc 4 bánh Mecanum bằng ma trận động học
                v_fl, v_fr, v_rl, v_rr = mecanum_kinematics_mix(
                    self.curr_vy, self.curr_vx, self.curr_omega, self.max_speed
                )
                if hasattr(self.robot, 'run_mecanum'):
                    self.robot.run_mecanum(v_fl, v_fr, v_rl, v_rr)
                else:
                    self.robot.m1.run(v_fl)
                    self.robot.m2.run(v_fr)
                    self.robot.m3.run(v_rl)
                    self.robot.m4.run(v_rr)

            await asyncio.sleep_ms(20)
