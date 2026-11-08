"""
CHƯƠNG TRÌNH ĐIỀU KHIỂN ROBOT ORC K2 (4WD: 2 ENCODER + 2 DC THƯỜNG)
GIẢI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
"""

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
from maze_strategy import run_maze_left, run_maze_right

# ====================================================================
# 1. KHỞI TẠO NGOẠI VI & PHẦN CỨNG 4WD
# ====================================================================
md_v2 = MotorDriverV2()

# 4 Động cơ dẫn động:
# Cầu trước: 2 động cơ thường (M1, M2)
motor_fl = DCMotor(md_v2, config.MOTOR_FL_PORT, reversed=config.MOTOR_FL_REVERSED)
motor_fr = DCMotor(md_v2, config.MOTOR_FR_PORT, reversed=config.MOTOR_FR_REVERSED)

# Cầu sau: 2 động cơ có Encoder đo quãng đường (E1, E2)
motor_rl = DCMotor(md_v2, config.MOTOR_RL_PORT, reversed=config.MOTOR_RL_REVERSED)
motor_rr = DCMotor(md_v2, config.MOTOR_RR_PORT, reversed=config.MOTOR_RR_REVERSED)

# Khởi tạo DriveBase 4WD: m1=FL, m2=FR, m3=RL(Encoder), m4=RR(Encoder)
robot = DriveBase(config.DRIVE_MODE, m1=motor_fl, m2=motor_fr, m3=motor_rl, m4=motor_rr)

# Hệ thống Động cơ Servo tay gắp hoa Ø32mm
servo_lift = Servo(md_v2, config.SERVO_LIFT_PORT, 180) # S1: Nâng/Hạ
servo_grip = Servo(md_v2, config.SERVO_GRIP_PORT, 180) # S2: Kẹp/Thả

# Cảm biến góc MPU6050 (Tích hợp trên ORC Hub)
imu = MPU6050(transposition=(2, 1, 0), scaling=(-1, -1, -1))
angle_sensor = AngleSensor(imu)

# Tay cầm Gamepad
gamepad = Gamepad()

# Nút bấm vật lý trên mạch
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
# 2. CÁC HÀM SỰ KIỆN TAY CẦM (GAMEPAD CALLBACKS)
# ====================================================================
async def on_cmd_BTN_R1():
    """Kẹp hoa Ø32mm"""
    print("[GAMEPAD] -> KEP HOA")
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=120)

async def on_cmd_BTN_R2():
    """Nhả kẹp hoa"""
    print("[GAMEPAD] -> NHA HOA")
    await servo_grip.run_angle(angle=config.GRIP_OPEN, speed=120)

async def on_cmd_BTN_L1():
    """Nâng tay gắp lên cao để di chuyển nhanh"""
    print("[GAMEPAD] -> NANG TAY GAP")
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)

async def on_cmd_BTN_L2():
    """Hạ tay gắp sát sàn để đón/thả hoa"""
    print("[GAMEPAD] -> HA TAY GAP")
    await servo_lift.run_angle(angle=config.LIFT_DOWN, speed=100)

async def on_cmd_BTN_CIRCLE():
    """
    Nút TRÒN (CIRCLE) - COMBO ĐẶT HOA TỰ ĐỘNG CHUẨN ĐỨNG VỮNG:
    1. Hạ hoa sát sàn
    2. Nhả kẹp để đáy hoa tiếp đất 100%
    3. Lùi xe 8cm thẳng hàng không va đổ hoa
    4. Nhấc tay gắp lên để đi lấy hoa tiếp theo
    """
    print("[COMBO] -> DAT HOA CHUAN KHONG DO")
    robot.stop()
    await servo_lift.run_angle(angle=config.LIFT_DOWN, speed=90)
    await asleep_ms(200)
    await servo_grip.run_angle(angle=config.GRIP_OPEN, speed=120)
    await asleep_ms(250)
    await robot.backward_for(8, unit=CM, then=STOP)
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)

# ====================================================================
# 3. KÍCH HOẠT CHẾ ĐỘ TỰ ĐỘNG (GIAI ĐOẠN 1: MÊ CUNG)
# ====================================================================
async def on_btn_BOOT_pressed():
    global is_autonomous_running
    if not is_autonomous_running:
        is_autonomous_running = True
        robot.mode_auto = True
        neopix.show(0, hex_to_rgb('#ff0000')) # Đỏ: Đang chạy tự động
        await run_maze_left(robot, servo_lift, servo_grip)
        robot.mode_auto = False
        is_autonomous_running = False
        neopix.show(0, hex_to_rgb('#0000ff')) # Xanh dương: Đã vào Ô Xanh lá!
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
    print("=== KHỞI ĐỘNG HỆ THỐNG ORC K2 (4WD: 2 ENCODER + 2 DC THƯỜNG) ===")
    
    # Đèn Vàng: Đang hiệu chuẩn
    neopix.show(0, hex_to_rgb('#ffff00'))
    
    # Cấu hình Encoder cho 2 động cơ cầu sau (E1, E2)
    motor_rl.set_encoder(rpm=config.ENCODER_RPM, ppr=config.ENCODER_PPR, gears=config.ENCODER_GEARS)
    motor_rr.set_encoder(rpm=config.ENCODER_RPM, ppr=config.ENCODER_PPR, gears=config.ENCODER_GEARS)
    
    # Cấu hình kích thước xe 4WD (mm)
    robot.size(wheel=config.WHEEL_DIAMETER, width=config.CHASSIS_WIDTH)
    robot.speed(config.SPEED_AUTO_MAZE, min_speed=35)
    
    # Cấu hình Servo tay gắp
    servo_lift.limit(min=0, max=180)
    servo_grip.limit(min=0, max=180)
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=100)
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=100)
    
    # Hiệu chuẩn cảm biến góc IMU MPU6050
    print("Đang Calibrate MPU6050... Giữ yên xe!")
    angle_sensor.calibrate(400)
    create_task(angle_sensor.run())
    robot.angle_sensor(angle_sensor)
    robot.use_gyro(True)
    print("Calibrate IMU thành công!")
    
    # Gán các nút điều khiển Gamepad
    robot.on_teleop_command(BTN_R1, on_cmd_BTN_R1)
    robot.on_teleop_command(BTN_R2, on_cmd_BTN_R2)
    robot.on_teleop_command(BTN_L1, on_cmd_BTN_L1)
    robot.on_teleop_command(BTN_L2, on_cmd_BTN_L2)
    robot.on_teleop_command(BTN_CIRCLE, on_cmd_BTN_CIRCLE)
    
    # Kích hoạt Bluetooth & Gamepad Receiver
    create_task(ble.wait_for_msg())
    create_task(gamepad.run())
    create_task(robot.run_teleop(gamepad, accel_steps=3))
    
    # Đăng ký nút bấm vật lý
    btn_BOOT.pressed(on_btn_BOOT_pressed)
    btn_D3.pressed(on_btn_D3_pressed)
    btn_D4.pressed(on_btn_D4_pressed)
    
    create_task(task_telemetry())
    
    # Đèn Xanh Lá: Sẵn sàng tại Ô Đỏ xuất phát!
    neopix.show(0, hex_to_rgb('#00ff00'))
    print("Điện áp Pin Li-ion:", md_v2.battery(), "V")
    print(">>> 4WD SẴN SÀNG! ĐẶT XE VÀO Ô ĐỎ VÀ BẤM NÚT ĐỂ CHẠY <<<")

async def main():
    await setup()
    while True:
        await asleep_ms(100)

run_loop(main())
