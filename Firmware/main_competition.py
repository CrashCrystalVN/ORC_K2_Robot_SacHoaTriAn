"""
=============================================================================
CHƯƠNG TRÌNH ĐIỀU KHIỂN ROBOT ORC K2 (4WD GA25 MECANUM: 2 ENCODER + 2 DC THƯỜNG)
GIẢI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & KỶ NIỆM 20/11
BẢN THI ĐẤU CHÍNH THỨC (COMPETITION RELEASE)
=============================================================================
Hệ thống điều khiển chuẩn hóa:
- Động học 4 bánh Mecanum tích hợp Bộ trộn Desaturation chống méo vector.
- 2 Joystick FPS / Arcade Drive:
    * J1 (Cần Trái): Lên/Xuống = Tiến/Lùi (Vy); Trái/Phải = Trượt Ngang (Vx)
    * J2 (Cần Phải): Trái/Phải = Xoay tròn tại chỗ (Omega)
- Bộ lọc Deadband 7% triệt tiêu trôi xe khi nhả tay cầm.
- Đường cong độ nhạy phi tuyến Expo (0.4) + Slew-Rate Limiter êm ái chống giật.
=============================================================================
"""

import asyncio
try:
    from time import ticks_ms
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
from motor import *
from mdv2 import *
from drivebase import *
from servo import *
from ble import *
from gamepad import *
from mpu6050 import MPU6050
from angle_sensor import AngleSensor
from abutton import *
from pins import *
from utility import *
import config
from mecanum_kinematics import MecanumTeleopController
from maze_strategy import run_maze_left, run_maze_right

# ====================================================================
# 1. KHỞI TẠO NGOẠI VI & PHẦN CỨNG 4WD MECANUM
# ====================================================================
md_v2 = MotorDriverV2()

# 4 Động cơ dẫn động (Sơ đồ phần cứng thực tế):
# Cầu trước: 2 động cơ thường (M2: Trái Trước -> m1, M1: Phải Trước -> m2)
motor_fl = DCMotor(md_v2, config.MOTOR_FL_PORT, reversed=config.MOTOR_FL_REVERSED)  # Trái Trước (M2)
motor_fr = DCMotor(md_v2, config.MOTOR_FR_PORT, reversed=config.MOTOR_FR_REVERSED)  # Phải Trước (M1)

# Cầu sau: 2 động cơ có Encoder (E1: Trái Sau -> m3, E2: Phải Sau -> m4)
motor_rl = DCMotor(md_v2, config.MOTOR_RL_PORT, reversed=config.MOTOR_RL_REVERSED)  # Trái Sau (E1)
motor_rr = DCMotor(md_v2, config.MOTOR_RR_PORT, reversed=config.MOTOR_RR_REVERSED)  # Phải Sau (E2)

# Khởi tạo DriveBase 4WD Mecanum
robot = DriveBase(MODE_MECANUM, m1=motor_fl, m2=motor_fr, m3=motor_rl, m4=motor_rr)

# Hệ thống Động cơ Servo tay gắp hoa Ø32mm (MG996R)
servo_lift  = Servo(md_v2, config.SERVO_LIFT_PORT, 180)  # S1: Nâng/Hạ tay chữ H
servo_grip  = Servo(md_v2, config.SERVO_GRIP_PORT, 180)  # S2: Kẹp/Thả 3 trụ hoa
servo_wrist = Servo(md_v2, config.SERVO_WRIST_PORT, 180) # S3: Cổ tay gập dọc (tùy chọn)

# Cảm biến góc MPU6050 (Tích hợp trên ORC Control Hub)
try:
    imu = MPU6050(transposition=(2, 1, 0), scaling=(-1, -1, -1))
    angle_sensor = AngleSensor(imu)
except Exception as e:
    print("[WARN] Khong khoi tao duoc IMU:", e)
    angle_sensor = None

# Tay cầm Gamepad (Hỗ trợ mạch thu PS4 I2C & App OhStem BLE)
gamepad = Gamepad()

# Bộ điều khiển Teleop 2 Joystick chuyên nghiệp (FPS / Arcade Drive)
teleop = MecanumTeleopController(robot, gamepad, max_speed=config.SPEED_TELEOP_NORMAL)

# Nút bấm vật lý & LED chỉ báo trên mạch
btn_BOOT = aButton(BOOT_PIN)
btn_D3 = aButton(D3_PIN)
btn_D4 = aButton(D4_PIN)
led_D13 = Pins(D13_PIN)

is_autonomous_running = False

def deinit():
    robot.stop()
    btn_BOOT.deinit()
    btn_D3.deinit()
    btn_D4.deinit()

import yolo_uno
yolo_uno.deinit = deinit

# ====================================================================
# 2. CÁC HÀM SỰ KIỆN TAY CẦM (GAMEPAD ACTIONS)
# ====================================================================
async def on_cmd_BTN_R1():
    """Kẹp chặt 3 thân ống hoa Ø32mm"""
    print("[GAMEPAD] -> KEP HOA")
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=100)

async def on_cmd_BTN_R2():
    """Nhả hàm kẹp hoa"""
    print("[GAMEPAD] -> NHA HOA")
    await servo_grip.run_angle(angle=config.GRIP_OPEN, speed=100)

async def on_cmd_BTN_L1():
    """Nâng tay gắp lên cao để di chuyển nhanh lướt qua mê cung"""
    print("[GAMEPAD] -> NANG TAY GAP")
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)

async def on_cmd_BTN_L2():
    """Hạ tay gắp sát sàn để đón/thả hoa tự đứng"""
    print("[GAMEPAD] -> HA TAY GAP")
    await servo_lift.run_angle(angle=config.LIFT_DOWN, speed=100)

async def on_cmd_BTN_CIRCLE():
    """
    Nút TRÒN (CIRCLE) - COMBO ĐẶT HOA TỰ ĐỘNG CHUẨN ĐỨNG VỮNG:
    1. Hạ hoa sát sàn
    2. Nhả kẹp để đáy hoa tiếp đất 100%
    3. Lùi xe 8cm thẳng hàng không va đổ hoa
    4. Nhấc tay gắp lên để chuẩn bị lấy hoa tiếp theo
    """
    print("[COMBO] -> DAT HOA CHUAN KHONG DO")
    robot.stop()
    await servo_lift.run_angle(angle=config.LIFT_DOWN, speed=90)
    await asleep_ms(200)
    await servo_grip.run_angle(angle=config.GRIP_OPEN, speed=100)
    await asleep_ms(250)
    await robot.backward_for(8, unit=CM, then=STOP)
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)

async def on_cmd_BTN_CROSS():
    """Nút X (CROSS) - Bật/Tắt chế độ di chuyển chậm chính xác (Precision Mode)"""
    is_slow = teleop.toggle_precision_mode()
    if is_slow:
        neopix.show(0, hex_to_rgb('#00ffff'))
    else:
        neopix.show(0, hex_to_rgb('#00ff00'))

_last_options_toggle_ms = 0

async def on_cmd_BTN_OPTIONS():
    """Chuyển đổi chế độ AUTO <-> MANUAL bằng nút OPTIONS kèm phản hồi rung Haptic Rumble & debounce 400ms"""
    global is_autonomous_running, _last_options_toggle_ms
    now = ticks_ms()
    if now - _last_options_toggle_ms < 400:
        return
    _last_options_toggle_ms = now

    if not is_autonomous_running:
        is_autonomous_running = True
        robot.mode_auto = True
        neopix.show(0, hex_to_rgb('#0000ff'))
        gamepad.set_led_color(0, 0, 255)
        print("\n>>> [MODE] CHUYỂN SANG AUTO (TỰ HÀNH) - Rung 2 cái dài <<<")
        create_task(gamepad.rumble_feedback("AUTO"))
        try:
            await run_maze_left(robot, servo_lift, servo_grip)
        except Exception as e:
            print("[AUTO ERROR]", e)
        robot.mode_auto = False
        is_autonomous_running = False
        neopix.show(0, hex_to_rgb('#00ff00'))
        gamepad.set_led_color(0, 255, 0)
        print("\n>>> [MODE] TỰ HÀNH HOÀN THÀNH -> TRẢ VỀ MANUAL - Rung 1 cái ngắn <<<")
        create_task(gamepad.rumble_feedback("MANUAL"))
    else:
        is_autonomous_running = False
        robot.mode_auto = False
        robot.stop()
        neopix.show(0, hex_to_rgb('#00ff00'))
        gamepad.set_led_color(0, 255, 0)
        print("\n>>> [MODE] NGẮT TỰ HÀNH KHẨN CẤP -> TRẢ VỀ MANUAL - Rung 1 cái ngắn <<<")
        create_task(gamepad.rumble_feedback("MANUAL"))

async def on_cmd_BTN_TRIANGLE():
    """Nút TAM GIÁC (TRIANGLE) - Gập dựng cụm kẹp (nếu có servo cổ tay) hoặc Turbo Mode"""
    try:
        await servo_wrist.run_angle(angle=config.WRIST_VERTICAL_UP, speed=100)
        print("[GAMEPAD] -> GAP CO TAY DUNG DUNG 90 DO")
    except Exception:
        if teleop.max_speed == config.SPEED_TELEOP_TURBO:
            teleop.set_max_speed(config.SPEED_TELEOP_NORMAL)
            print("[TELEOP] Speed: NORMAL (75%)")
        else:
            teleop.set_max_speed(config.SPEED_TELEOP_TURBO)
            print("[TELEOP] Speed: TURBO (100%)")

# ====================================================================
# 3. KÍCH HOẠT CHẾ ĐỘ TỰ ĐỘNG (GIAI ĐOẠN 1: MÊ CUNG)
# ====================================================================
async def on_btn_BOOT_pressed():
    global is_autonomous_running
    if not is_autonomous_running:
        is_autonomous_running = True
        robot.mode_auto = True
        neopix.show(0, hex_to_rgb('#ff0000'))
        await run_maze_left(robot, servo_lift, servo_grip)
        robot.mode_auto = False
        is_autonomous_running = False
        neopix.show(0, hex_to_rgb('#0000ff'))
        robot.speed(config.SPEED_TELEOP_NORMAL, min_speed=35)

async def on_btn_D3_pressed():
    await on_btn_BOOT_pressed()

async def on_btn_D4_pressed():
    global is_autonomous_running
    if not is_autonomous_running:
        is_autonomous_running = True
        robot.mode_auto = True
        neopix.show(0, hex_to_rgb('#ff0000'))
        await run_maze_right(robot, servo_lift, servo_grip)
        robot.mode_auto = False
        is_autonomous_running = False
        neopix.show(0, hex_to_rgb('#0000ff'))
        robot.speed(config.SPEED_TELEOP_NORMAL, min_speed=35)

async def task_telemetry():
    while True:
        await asleep_ms(1000)
        led_D13.toggle()

# ====================================================================
# 4. KHỞI ĐỘNG HỆ THỐNG (SETUP)
# ====================================================================
async def setup():
    print("=== KHỞI ĐỘNG HỆ THỐNG ORC K2 (4WD GA25 MECANUM) ===")
    
    neopix.show(0, hex_to_rgb('#ffff00'))
    
    motor_rl.set_encoder(rpm=config.ENCODER_RPM, ppr=config.ENCODER_PPR, gears=config.ENCODER_GEARS)
    motor_rr.set_encoder(rpm=config.ENCODER_RPM, ppr=config.ENCODER_PPR, gears=config.ENCODER_GEARS)
    
    robot.size(wheel=config.WHEEL_DIAMETER, width=config.CHASSIS_WIDTH)
    robot.speed(config.SPEED_AUTO_MAZE, min_speed=35)
    
    servo_lift.limit(min=0, max=180)
    servo_grip.limit(min=0, max=180)
    servo_wrist.limit(min=0, max=180)
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=100)
    
    if angle_sensor is not None:
        print("Đang Calibrate MPU6050... Giữ yên xe!")
        try:
            angle_sensor.calibrate(400)
            create_task(angle_sensor.run())
            robot.angle_sensor(angle_sensor)
            robot.use_gyro(True)
            print("Calibrate IMU thành công!")
        except Exception as e:
            print("[WARN] Calibrate IMU that bai:", e)
    
    teleop.on_button(BTN_R1, on_cmd_BTN_R1)
    teleop.on_button(BTN_R2, on_cmd_BTN_R2)
    teleop.on_button(BTN_L1, on_cmd_BTN_L1)
    teleop.on_button(BTN_L2, on_cmd_BTN_L2)
    teleop.on_button(BTN_CIRCLE, on_cmd_BTN_CIRCLE)
    teleop.on_button(BTN_CROSS, on_cmd_BTN_CROSS)
    teleop.on_button(BTN_TRIANGLE, on_cmd_BTN_TRIANGLE)
    # Nút OPTIONS được quản lý độc quyền qua teleop.on_button (có debounce 400ms)
    teleop.on_button(BTN_OPTIONS, on_cmd_BTN_OPTIONS)
    
    create_task(ble.wait_for_msg())
    create_task(gamepad.run())
    create_task(teleop.run())
    
    btn_BOOT.pressed(on_btn_BOOT_pressed)
    btn_D3.pressed(on_btn_D3_pressed)
    btn_D4.pressed(on_btn_D4_pressed)
    
    create_task(task_telemetry())
    
    neopix.show(0, hex_to_rgb('#00ff00'))
    try:
        mv = md_v2.battery()
        v = mv / 1000.0 if mv > 100 else mv
        print("Điện áp Pin Li-ion:", f"{v:.2f}V")
    except Exception:
        pass
    print(">>> ROBOT MECANUM K2 SẴN SÀNG CHIẾN ĐẤU! <<<")

async def main():
    await setup()
    while True:
        await asleep_ms(100)

run_loop(main())
