"""
=============================================================================
CHƯƠNG TRÌNH ĐIỀU KHIỂN CHÍNH ROBOT ORC K2 (ESP32-S3 / K2 HUB)
GIẢI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & KỶ NIỆM 20/11
=============================================================================
Tính năng tích hợp:
1. Chuyển đổi linh hoạt chế độ MANUAL <-> AUTO bằng nút OPTIONS trên tay cầm PS4.
2. Phản hồi rung xúc giác Haptic Rumble & Đổi màu đèn LED tay cầm:
   - MANUAL: Rung 1 cái ngắn (200ms) + LED Xanh Lá (#00ff00).
   - AUTO  : Rung 2 cái dài (500ms - 200ms - 500ms) + LED Xanh Dương (#0000ff).
3. Ở chế độ MANUAL:
   - Điều khiển 4 bánh Mecanum mượt mà (tiến/lùi/dạt ngang/xoay) bằng 2 Joystick.
   - Nâng/hạ tháp, gắp/thả hoa bằng các nút bấm trên tay cầm.
4. Ở chế độ AUTO:
   - Kích hoạt chiến thuật tự hành thông minh kết hợp Dò Line và 3 Cảm biến
     khoảng cách Laser ToF VL53L0X (Trước, Trái, Phải).
   - Tự động tránh vật cản, cân bằng tâm vách mê cung và tự động đón/kẹp hoa.
   - Nhấn nút OPTIONS bất cứ lúc nào để lập tức ngắt tự hành và trả quyền điều khiển về tay cầm.
=============================================================================
"""

import asyncio
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
from constants import *
from laser_system import LaserSystem

# ====================================================================
# 1. TRẠNG THÁI HỆ THỐNG & BIẾN TOÀN CỤC
# ====================================================================
SYSTEM_MODE = "MANUAL"       # "MANUAL" (Mặc định) hoặc "AUTO"
auto_running_flag = False    # Cờ điều khiển chu trình tự hành
current_auto_task = None     # Tham chiếu task tự hành asyncio

# ====================================================================
# 2. KHỞI TẠO PHẦN CỨNG & NGOẠI VI
# ====================================================================
md_v2 = MotorDriverV2()

# 4 Động cơ dẫn động Mecanum GA25
motor_fl = DCMotor(md_v2, M2, reversed=True)  # Trái Trước (M2)
motor_fr = DCMotor(md_v2, M1, reversed=True)  # Phải Trước (M1)
motor_rl = DCMotor(md_v2, E1, reversed=True)  # Trái Sau (E1)
motor_rr = DCMotor(md_v2, E2, reversed=True)  # Phải Sau (E2)

# Biến tương thích ngược
motor1 = motor_fl
motor2 = motor_fr
motor3 = motor_rl
motor4 = motor_rr

# DriveBase 4WD Mecanum
robot = DriveBase(MODE_MECANUM, m1=motor_fl, m2=motor_fr, m3=motor_rl, m4=motor_rr)

# Động cơ DC M3 (Roller / Tháp nâng)
motor5 = DCMotor(md_v2, M3, reversed=True)

# Động cơ Servo điều khiển cơ cấu cánh tay và kẹp hoa
servo1 = Servo(md_v2, S1, 180)  # Cánh tay nâng chữ H
servo2 = Servo(md_v2, S2, 180)  # Hàm kẹp hoa Ø32mm
servo3 = Servo(md_v2, S3, 180)  # Cổ tay gập dọc / Servo phụ
servo4 = Servo(md_v2, S4, 180)  # Khóa an toàn / Servo phụ

# Tay cầm Gamepad (PS4 I2C Receiver & OhStem App BLE)
gamepad = Gamepad()

# Hệ thống 3 Cảm biến khoảng cách Laser ToF VL53L0X (Trước, Trái, Phải)
laser_system = LaserSystem()

# Cảm biến dò line I2C PCF8574 (0x23)
try:
    from line_sensor import LineSensorI2C
    line_sensor = LineSensorI2C(address=0x23)
except Exception as e:
    print('[WARN] Khong khoi tao duoc Line Sensor:', e)
    line_sensor = None

# Cảm biến góc nghiêng MPU6050
try:
    imu = MPU6050(transposition=(2, 1, 0), scaling=(-1, -1, -1))
    angle_sensor = AngleSensor(imu)
except Exception as e:
    print('[WARN] Khong khoi tao duoc IMU MPU6050:', e)
    imu = None
    angle_sensor = None

# Nút bấm vật lý & LED chỉ báo
btn_BOOT = aButton(BOOT_PIN)
# Lưu ý: Cổng D3-D4 (GPIO 6 & 7) được dùng riêng cho Cảm biến Laser ToF Phía Trước (Front)
btn_D3 = None
btn_D4 = None
led_D13 = Pins(D13_PIN)

def deinit():
    robot.stop()
    motor5.stop()
    btn_BOOT.deinit()
    if btn_D3:
        btn_D3.deinit()
    if btn_D4:
        btn_D4.deinit()

import yolo_uno
yolo_uno.deinit = deinit

# ====================================================================
# 3. CƠ CHẾ CHUYỂN ĐỔI CHẾ ĐỘ & PHẢN HỒI RUNG HAPTIC (OPTIONS BUTTON)
# ====================================================================
async def switch_to_manual():
    """Chuyển hệ thống sang chế độ MANUAL (Điều khiển tay cầm)"""
    global SYSTEM_MODE, auto_running_flag, current_auto_task

    SYSTEM_MODE = "MANUAL"
    auto_running_flag = False
    robot.mode_auto = False

    # Dừng ngay lập tức toàn bộ chuyển động tự hành
    robot.stop()
    motor5.stop()

    if current_auto_task:
        try:
            if hasattr(current_auto_task, 'cancel'):
                current_auto_task.cancel()
        except Exception:
            pass
        current_auto_task = None

    # Phản hồi thị giác: LED Onboard & LED Tay cầm màu XANH LÁ
    try:
        neopix.show(0, hex_to_rgb('#00ff00'))
    except Exception:
        pass
    gamepad.set_led_color(0, 255, 0)

    print("\n" + "=" * 65)
    print(">>> [CHẾ ĐỘ] ĐÃ CHUYỂN SANG: MANUAL (ĐIỀU KHIỂN TAY CẦM) <<<")
    print("    Phản hồi: Rung Haptic 1 cái ngắn (200ms) - LED Xanh Lá")
    print("=" * 65 + "\n")

    # Phản hồi rung haptic: 1 cái ngắn (200ms)
    await gamepad.rumble_feedback("MANUAL")


async def switch_to_auto():
    """Chuyển hệ thống sang chế độ AUTO (Tự hành thông minh)"""
    global SYSTEM_MODE, auto_running_flag, current_auto_task

    SYSTEM_MODE = "AUTO"
    auto_running_flag = True
    robot.mode_auto = True

    # Dừng di chuyển bằng tay cầm
    robot.stop()
    motor5.stop()

    # Phản hồi thị giác: LED Onboard & LED Tay cầm màu XANH DƯƠNG
    try:
        neopix.show(0, hex_to_rgb('#0000ff'))
    except Exception:
        pass
    gamepad.set_led_color(0, 0, 255)

    print("\n" + "=" * 65)
    print(">>> [CHẾ ĐỘ] ĐÃ CHUYỂN SANG: AUTO (TỰ HÀNH THÔNG MINH) <<<")
    print("    Phản hồi: Rung Haptic 2 cái dài (500ms - 200ms - 500ms) - LED Xanh Dương")
    print("=" * 65 + "\n")

    # Phản hồi rung haptic: 2 cái dài (500ms -> ngắt 200ms -> 500ms)
    await gamepad.rumble_feedback("AUTO")

    # Kích hoạt luồng chiến thuật tự hành thông minh
    current_auto_task = create_task(run_smart_autonomous())


async def toggle_robot_mode():
    """Hàm đảo trạng thái chuyển đổi giữa MANUAL và AUTO khi bấm nút OPTIONS"""
    if SYSTEM_MODE == "MANUAL":
        await switch_to_auto()
    else:
        await switch_to_manual()


try:
    from time import ticks_ms
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)

async def task_options_monitor():
    """
    Task giám sát liên tục nút OPTIONS (BTN_OPTIONS / BTN_M2 / START)
    Đảm bảo phản hồi tức thì < 20ms trong mọi tình huống (kể cả khi đang AUTO).
    Tích hợp bộ lọc chống dội phím (Debounce Cooldown 400ms) để ngăn kích hoạt lặp.
    """
    last_state = 0
    last_toggle_time = 0
    while True:
        await asleep_ms(20)
        curr_state = (
            gamepad.data.get(BTN_OPTIONS, 0)
            or gamepad.data.get(BTN_M2, 0)
            or gamepad.data.get('OPTIONS', 0)
        )
        now = ticks_ms()
        if curr_state == 1 and last_state == 0 and (now - last_toggle_time > 400):  # Sườn lên + debounce 400ms
            last_toggle_time = now
            print("[EVENT] Nhấn nút OPTIONS trên tay cầm!")
            await toggle_robot_mode()
        last_state = curr_state


# ====================================================================
# 4. CHIẾN THUẬT TỰ HÀNH THÔNG MINH (LEFT WALL FOLLOWER + PID + CHỐNG KẸT)
# ====================================================================
async def run_smart_autonomous():
    """
    Chuỗi tác vụ tự hành giải mê cung bằng thuật toán Left Wall Follower + PID
    bám tường trái kết hợp Chống kẹt phối hợp (999 / 3.0s đứng yên) & Chống kẹt Loops (5 lần lặp):
    - Front: Siêu âm HY-SRF05 đo cự ly vật cản và chống kẹt 999
    - Left: Laser ToF VL53L0X bám vách trái chính xác cao bằng PID
    - Right: Laser ToF VL53L0X kiểm tra khoảng trống rẽ phải
    - Phản hồi ngắt khẩn cấp tức thì < 20ms khi người dùng nhấn nút OPTIONS trên tay cầm
    """
    global SYSTEM_MODE, auto_running_flag
    print("\n" + "=" * 65)
    print(">>> [AUTO] KÍCH HOẠT THUẬT TOÁN LEFT WALL FOLLOWER PID GIẢI MÊ CUNG <<<")
    print("=" * 65)

    # 1. Thu gọn cánh tay nâng và hàm kẹp lọt khung 20x20x50cm theo thể lệ giải đấu
    try:
        await servo1.run_angle(angle=85, speed=100)
        await servo2.run_angle(angle=0, speed=90)   # Mở ngàm
        await asleep_ms(150)
    except Exception as e:
        print("[AUTO] Canh bao setup servo:", e)

    # 2. Khởi chạy thuật toán bám tường trái Left Wall Follower
    from maze_strategy import run_maze_follower
    try:
        await run_maze_follower(
            robot=robot,
            laser_system=laser_system,
            angle_sensor=angle_sensor,
            is_auto_func=lambda: (auto_running_flag and SYSTEM_MODE == "AUTO")
        )
    except Exception as e:
        print("[AUTO] Loi thuc thi giai me cung:", e)

    # Đảm bảo phanh êm và ngắt động cơ khi dừng chu trình tự hành
    robot.brake()
    await asleep_ms(80)
    robot.stop()
    motor5.stop()
    print(">>> [AUTO] ĐÃ KẾT THÚC CHU TRÌNH TỰ HÀNH (PHANH ÊM, AN TOÀN) <<<")
# ====================================================================
# 5. TÁC VỤ ĐIỀU KHIỂN TAY CẦM NGOẠI VI TRONG CHẾ ĐỘ MANUAL
# ====================================================================
async def on_cmd_BTN_L1():
    if SYSTEM_MODE == "MANUAL":
        await servo3.run_angle(angle=0, speed=150)

async def on_cmd_BTN_L2():
    if SYSTEM_MODE == "MANUAL":
        await servo3.run_angle(angle=90, speed=150)

async def on_cmd_BTN_THUMBR():
    if SYSTEM_MODE == "MANUAL":
        motor5.brake()

async def task_manual_tower_gripper():
    """Điều khiển tháp nâng và tay kẹp hoa khi ở chế độ MANUAL"""
    while True:
        await asleep_ms(60)
        if SYSTEM_MODE != "MANUAL":
            continue

        # Nút TAM GIÁC / VUÔNG: Nâng / Hạ mô-tơ M3
        if gamepad.data[BTN_TRIANGLE] == 1:
            motor5.run(100)
        elif gamepad.data[BTN_SQUARE] == 1:
            motor5.run(-100)

        # Nút R1 / R2: Kẹp hoa / Hạ ngàm thả hoa
        if gamepad.data[BTN_R1] == 1:
            await servo1.run_angle(angle=85, speed=100)
            await servo2.run_angle(angle=60, speed=100)
        elif gamepad.data[BTN_R2] == 1:
            await servo1.run_angle(angle=125, speed=100)
            await servo2.run_angle(angle=0, speed=90)


async def task_manual_aux_servos():
    """Điều khiển các servo phụ (S4) khi ở chế độ MANUAL"""
    while True:
        await asleep_ms(60)
        if SYSTEM_MODE != "MANUAL":
            continue

        if gamepad.data[BTN_CIRCLE] == 1:
            await servo4.run_angle(angle=70, speed=40)
        elif gamepad.data[BTN_CROSS] == 1:
            await servo4.run_angle(angle=58, speed=40)


async def task_heartbeat():
    """Nhấp nháy LED D13 báo trạng thái hệ thống hoạt động ổn định"""
    while True:
        await asleep_ms(500)
        led_D13.toggle()


# ====================================================================
# 6. SỰ KIỆN NÚT BẤM VẬT LÝ TRÊN MẠCH (BOOT, D3, D4)
# ====================================================================
async def on_abutton_BOOT_pressed():
    await toggle_robot_mode()

async def on_abutton_D3_double_pressed():
    await switch_to_manual()

async def on_abutton_D3_pressed():
    await toggle_robot_mode()

async def on_abutton_D4_pressed():
    await toggle_robot_mode()


# ====================================================================
# 7. KHỞI TẠO HỆ THỐNG (SETUP) & VÒNG LẶP CHÍNH (MAIN)
# ====================================================================
async def setup():
    print("\n" + "=" * 65)
    print("=== KHỞI ĐỘNG HỆ THỐNG ROBOT ORC K2 (MECANUM + 3 LASER ToF) ===")
    print("=" * 65)

    neopix.show(0, hex_to_rgb('#ffff00'))  # Vàng: Đang khởi tạo

    # Cài đặt thông số động cơ & encoder
    motor_rl.set_encoder(rpm=350, ppr=11, gears=35)
    motor_rr.set_encoder(rpm=350, ppr=11, gears=35)
    robot.size(wheel=60, width=320)
    robot.speed(95, min_speed=60)

    # Giới hạn góc và đưa servo về vị trí ban đầu
    servo1.limit(min=0, max=180)
    servo2.limit(min=0, max=180)
    servo3.limit(min=0, max=180)
    servo4.limit(min=0, max=180)

    await servo1.run_angle(angle=125, speed=90)
    await servo2.run_angle(angle=0, speed=90)
    await servo3.run_angle(angle=0, speed=150)
    await servo4.run_angle(angle=58, speed=90)

    # Đăng ký lệnh teleop
    robot.on_teleop_command(BTN_L1, on_cmd_BTN_L1)
    robot.on_teleop_command(BTN_L2, on_cmd_BTN_L2)
    robot.on_teleop_command(BTN_THUMBR, on_cmd_BTN_THUMBR)
    # Nút OPTIONS được quản lý độc quyền bởi task_options_monitor (kèm debounce 400ms)

    # Calibrate IMU MPU6050 nếu có
    if angle_sensor is not None:
        try:
            print("Đang Calibrate IMU MPU6050...")
            angle_sensor.calibrate(500)
            create_task(angle_sensor.run())
            robot.angle_sensor(angle_sensor)
            robot.use_gyro(True)
            print("Calibrate IMU thành công!")
        except Exception as e:
            print('[WARN] Lỗi calibrate cảm biến góc:', e)
            robot.use_gyro(False)
    else:
        robot.use_gyro(False)

    # Đăng ký sự kiện nút bấm phần cứng
    btn_BOOT.pressed(on_abutton_BOOT_pressed)
    if btn_D3:
        btn_D3.double_pressed(on_abutton_D3_double_pressed)
        btn_D3.pressed(on_abutton_D3_pressed)
    if btn_D4:
        btn_D4.pressed(on_abutton_D4_pressed)

    # Khởi động các tiến trình bất đồng bộ nền
    create_task(ble.wait_for_msg())
    create_task(gamepad.run())
    create_task(robot.run_teleop(gamepad, accel_steps=8))
    create_task(task_options_monitor())
    create_task(task_manual_tower_gripper())
    create_task(task_manual_aux_servos())
    create_task(task_heartbeat())

    # Trạng thái ban đầu: MANUAL sẵn sàng
    await switch_to_manual()

    try:
        mv = md_v2.battery()
        v = mv / 1000.0 if mv > 100 else mv
        print(f"Điện áp Pin Li-ion K2: {v:.2f}V")
    except Exception:
        pass

    print(">>> ROBOT ORC K2 SẴN SÀNG! BẤM OPTIONS ĐỂ BẬT/TẮT TỰ HÀNH <<<")


async def main():
    await setup()
    while True:
        await asleep_ms(100)


run_loop(main())
