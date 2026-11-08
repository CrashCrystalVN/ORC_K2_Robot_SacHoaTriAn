"""
=============================================================================
CHƯƠNG TRÌNH KIỂM TRA TOÀN DIỆN MẠCH OHSTEM ORC K2 CONTROL HUB (ESP32-S3)
Tự động test phần cứng & Hỗ trợ chế độ tương tác qua nút bấm / Gamepad
=============================================================================
"""

import asyncio
from machine import Pin
from utility import *
from constants import *
from mdv2 import *
from motor import *
from servo import *
from drivebase import *
from mpu6050 import MPU6050
from angle_sensor import AngleSensor
from abutton import *
from pins import *
from ble import *
from gamepad import *

print("=====================================================")
print(" [*] KHOI DONG HE THONG TEST K2 CONTROL HUB OHSTEM")
print("=====================================================")

# 1. KHỞI TẠO DRIVER & NGOẠI VI
md_v2 = MotorDriverV2()
led_D13 = Pins(D13_PIN)
btn_BOOT = aButton(BOOT_PIN)
btn_D3   = aButton(D3_PIN)
btn_D4   = aButton(D4_PIN)

# 2. KHỞI TẠO 4 ĐỘNG CƠ (M1, M2, E1, E2)
m1 = DCMotor(md_v2, M1)
m2 = DCMotor(md_v2, M2)
m3 = DCMotor(md_v2, E1) # Hỗ trợ Encoder
m4 = DCMotor(md_v2, E2) # Hỗ trợ Encoder

# Cấu hình Encoder cho 2 động cơ E1, E2 (Chuẩn GA25 250RPM)
try:
    m3.set_encoder(rpm=250, ppr=11, gears=34)
    m4.set_encoder(rpm=250, ppr=11, gears=34)
    print(" [OK] Da cau hinh Encoder E1, E2 thanh cong.")
except Exception as e:
    print(" [!] Khong the cau hinh encoder:", e)

# 3. KHỞI TẠO 4 CỔNG SERVO (S1, S2, S3, S4)
servo1 = Servo(md_v2, S1, 180)
servo2 = Servo(md_v2, S2, 180)
servo3 = Servo(md_v2, S3, 180)
servo4 = Servo(md_v2, S4, 180)

# 4. KHỞI TẠO CẢM BIẾN GÓC IMU MPU6050
try:
    imu = MPU6050(transposition=(2, 1, 0), scaling=(-1, -1, -1))
    angle_sensor = AngleSensor(imu)
    angle_sensor.calibrate(300)
    create_task(angle_sensor.run())
    print(" [OK] IMU MPU6050 da duoc hieu chuan.")
except Exception as e:
    print(" [!] Khong the khoi tao IMU:", e)
    angle_sensor = None

# 5. KHỞI TẠO TAY CẦM GAMEPAD
gamepad = Gamepad()

# =====================================================================
# CÁC BÀI TEST CHỨC NĂNG
# =====================================================================

async def test_rgb_led():
    """Test đổi màu LED RGB NeoPixel"""
    colors = [
        ('#ff0000', 'DO (RED)'),
        ('#00ff00', 'XANH LA (GREEN)'),
        ('#0000ff', 'XANH DUONG (BLUE)'),
        ('#ffff00', 'VANG (YELLOW)'),
        ('#00ffff', 'XANH LAM (CYAN)'),
        ('#ff00ff', 'TIM (PURPLE)'),
        ('#ffffff', 'TRANG (WHITE)')
    ]
    for hex_c, name in colors:
        try:
            neopix.show(0, hex_to_rgb(hex_c))
        except Exception:
            pass
        await asleep_ms(300)
    # Tắt hoặc để xanh lá báo READY
    try:
        neopix.show(0, hex_to_rgb('#00ff00'))
    except Exception:
        pass

async def test_servos():
    """Test quét góc 4 cổng Servo S1, S2, S3, S4"""
    print("\n>>> DANG TEST 4 CONG SERVO (S1 -> S4) <<<")
    servos = [("S1", servo1), ("S2", servo2), ("S3", servo3), ("S4", servo4)]
    
    for name, s in servos:
        print(f" -> Quet {name}: 0 do -> 90 do -> 180 do -> 90 do")
        await s.run_angle(angle=0, speed=100)
        await asleep_ms(400)
        await s.run_angle(angle=90, speed=100)
        await asleep_ms(400)
        await s.run_angle(angle=180, speed=100)
        await asleep_ms(400)
        await s.run_angle(angle=90, speed=100)
        await asleep_ms(200)
    print(" [OK] Hoan tat test Servo.")

async def test_motors():
    """Test quay 4 động cơ M1, M2, E1, E2"""
    print("\n>>> DANG TEST 4 DONG CO DC (M1, M2, E1, E2) <<<")
    motors = [("M1", m1), ("M2", m2), ("E1", m3), ("E2", m4)]
    
    for name, m in motors:
        print(f" -> {name}: QUAY TIEN 50%...")
        m.run(50)
        await asleep_ms(1000)
        print(f" -> {name}: DUNG...")
        m.brake()
        await asleep_ms(300)
        
        print(f" -> {name}: QUAY LUI -50%...")
        m.run(-50)
        await asleep_ms(1000)
        print(f" -> {name}: PHANH (BRAKE)...")
        m.brake()
        await asleep_ms(400)
    print(" [OK] Hoan tat test Dong Co DC.")

async def test_encoders():
    """Test đọc xung Encoder trên cổng E1, E2"""
    print("\n>>> DANG TEST DOC ENCODER E1 & E2 (Quay dong co va doc xung) <<<")
    m3.reset_angle()
    m4.reset_angle()
    
    print(" -> Chay E1 & E2 voi toc do 40% trong 1.5 giay...")
    m3.run(40)
    m4.run(40)
    for _ in range(5):
        await asleep_ms(300)
        t3 = m3.encoder_ticks()
        t4 = m4.encoder_ticks()
        print(f"    Ticks E1: {t3:6d} | Ticks E2: {t4:6d} | Toc do E1: {m3.speed()} RPM")
    
    m3.brake()
    m4.brake()
    print(" [OK] Hoan tat test Encoder.")

# =====================================================================
# GÁN SỰ KIỆN CHO CÁC NÚT BẤM VẬT LÝ TRÊN MẠCH
# =====================================================================

async def on_btn_BOOT_pressed():
    print("\n[NUT BOOT] Duoc nhan -> Chay bai test DONG CO DC!")
    await test_motors()

async def on_btn_D3_pressed():
    print("\n[NUT D3] Duoc nhan -> Chay bai test DONG CO SERVO!")
    await test_servos()

async def on_btn_D4_pressed():
    print("\n[NUT D4] Duoc nhan -> Chay bai test ENCODER E1/E2 & IMU!")
    await test_encoders()
    if angle_sensor:
        print(f" -> IMU Goc Yaw hien tai: {angle_sensor.heading():.2f} do")

btn_BOOT.pressed(on_btn_BOOT_pressed)
btn_D3.pressed(on_btn_D3_pressed)
btn_D4.pressed(on_btn_D4_pressed)

# =====================================================================
# TASKS CHẠY NỀN (BACKGROUND TASKS)
# =====================================================================

async def task_heartbeat_led():
    """Nhay LED D13 va hien thi dien ap Pin dinh ky"""
    count = 0
    while True:
        await asleep_ms(500)
        led_D13.toggle()
        count += 1
        if count % 10 == 0: # Moi 5 giay in thong so 1 lan
            try:
                mv = md_v2.battery()
                v = mv / 1000.0 if mv > 100 else mv
                yaw = angle_sensor.heading() if angle_sensor else 0
                print(f"[STATUS] Pin: {v:.2f}V | IMU Yaw: {yaw:6.1f} do | D13: Nhap nhay OK")
            except Exception:
                pass

async def setup():
    # 1. Đọc và in thông số Pin
    try:
        v = md_v2.battery()
        print(f" [*] Dien ap Pin hien tai: {v/1000.0:.2f} V ({v} mV)")
    except Exception as e:
        print(" [!] Khong the doc dien ap Pin:", e)

    # 2. Test mau RGB
    print(" [*] Kiem tra hien thi LED RGB NeoPixel...")
    await test_rgb_led()

    # 3. Kích hoạt BLE Gamepad
    try:
        create_task(ble.wait_for_msg())
        create_task(gamepad.run())
        print(" [*] BLE Gamepad receiver da san sang ket noi.")
    except Exception as e:
        print(" [!] Khong the khoi tao BLE Gamepad:", e)

    # 4. Khoi dong Task Heartbeat
    create_task(task_heartbeat_led())

    print("\n" + "="*53)
    print(" [OK] K2 CONTROL HUB DA SAN SANG!")
    print(" HUONG DAN TEST NHANH:")
    print("  - Nhan nut BOOT: Test 4 Dong Co DC (M1, M2, E1, E2)")
    print("  - Nhan nut D3  : Test 4 Cong Servo (S1, S2, S3, S4)")
    print("  - Nhan nut D4  : Test Encoder E1, E2 va Cam bien IMU")
    print("  - LED D13 nhap nhay deu dan bao hieu he thong on dinh")
    print("="*53 + "\n")

async def main():
    await setup()
    # Chạy tự động chuỗi test kiểm tra ban đầu một lượt
    await asleep_ms(1000)
    await test_servos()
    await asleep_ms(500)
    await test_motors()
    await asleep_ms(500)
    await test_encoders()
    
    while True:
        await asleep_ms(100)

run_loop(main())

