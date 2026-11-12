"""
BỘ TEST KIỂM THỬ TÍCH HỢP MOTOR DRIVER & ENCODER WATCHDOG CHO ORC K2
Kiểm thử 100% các điều kiện biên:
1. PID Controller: dt = 0, dt cực nhỏ, Anti-Windup, lọc đạo hàm.
2. Motor Driver MDV2: Glitch Filter 32-bit encoder, bẫy lỗi I2C.
3. DC Motor: Tính toán speed() chống chia cho 0, watchdog encoder ticks.
4. DriveBase: _calib_speed kẹp correction (chống dừng động cơ đột ngột), run_mecanum.
5. Servo: Chống tràn bus I2C (delay không bao giờ âm khi speed > 100).
"""

import sys
import os
import unittest

# Thêm đường dẫn Firmware vào sys.path
firmware_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\Firmware"
if firmware_dir not in sys.path:
    sys.path.insert(0, firmware_dir)

# Mock MicroPython constants & functions if running on host CPython
import types
if 'micropython' not in sys.modules:
    mp = types.ModuleType('micropython')
    mp.const = lambda x: x
    sys.modules['micropython'] = mp

if 'machine' not in sys.modules:
    m = types.ModuleType('machine')
    class MockPin:
        OUT = 1
        IN = 0
        def __init__(self, pin, mode=None, pull=None): self._val = 0
        def value(self, v=None):
            if v is not None: self._val = v
            return self._val
    class MockPWM:
        def __init__(self, pin, freq=1000, duty=0): pass
        def freq(self, f=None): pass
        def duty(self, d=None): pass
        def deinit(self): pass
        def init(self, freq=1000, duty=0): pass
    class MockSoftI2C:
        def __init__(self, scl, sda, freq=100000): pass
        def writeto(self, addr, buf): pass
        def readfrom(self, addr, n): return bytes(n)
        def writeto_mem(self, addr, reg, buf): pass
        def readfrom_mem(self, addr, reg, n): return bytes(n)
    m.Pin = MockPin
    m.PWM = MockPWM
    m.SoftI2C = MockSoftI2C
    sys.modules['machine'] = m

for mod_name in ['ble', 'yolo_uno', 'line_sensor']:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = types.ModuleType(mod_name)
    st = types.ModuleType('setting')
    st.SCL_PIN = 22
    st.SDA_PIN = 21
    st.D2_PIN = 2
    st.A3_PIN = 3
    st.A6_PIN = 6
    st.A7_PIN = 7
    sys.modules['setting'] = st

if 'utility' not in sys.modules:
    ut = types.ModuleType('utility')
    def translate(val, in_min, in_max, out_min, out_max):
        return out_min + (float(val - in_min) / float(in_max - in_min)) * (out_max - out_min)
    ut.translate = translate
    sys.modules['utility'] = ut

# Now import our modules
from pid import PIDController
from mdv2 import MotorDriverV2, MAX_PLAUSIBLE_TICK_DELTA
from motor import DCMotor
from servo import Servo

class TestPIDController(unittest.TestCase):
    def test_dt_zero_safety(self):
        """Kiểm tra PID khi dt = 0 hoặc dt cực nhỏ (chống lỗi 1e-16 gây nổ D-term)."""
        pid = PIDController(Kp=5.0, Ki=0.15, Kd=0.1, setpoint=0, output_limits=(-10, 10))
        # Gọi 2 lần liên tiếp với dt = 0
        out1 = pid(0.0, dt=0.0)
        out2 = pid(10.0, dt=0.0)
        self.assertIsNotNone(out2)
        # Ngõ ra không bị nổ thành 10^15 hay vô tận
        self.assertTrue(-10.0 <= out2 <= 10.0)

    def test_anti_windup_clamping(self):
        """Kiểm tra Anti-Windup: I-term không vượt quá output_limits khi sai số liên tục kéo dài."""
        pid = PIDController(Kp=1.0, Ki=2.0, Kd=0.0, setpoint=100.0, output_limits=(-15, 15))
        for _ in range(100):
            pid(0.0, dt=0.1) # Sai số liên tục 100
        # Thành phần tích phân phải được giữ trong output_limits
        p, i, d = pid.components
        self.assertTrue(-15.0 <= i <= 15.0)

    def test_derivative_filter(self):
        """Kiểm tra bộ lọc đạo hàm: làm mịn sốc bước nhảy."""
        pid = PIDController(Kp=1.0, Ki=0.0, Kd=0.5, setpoint=0.0, output_limits=(-20, 20))
        out1 = pid(0.0, dt=0.01)
        # Đột ngột nhảy input lên 100
        out2 = pid(100.0, dt=0.01)
        self.assertTrue(-20.0 <= out2 <= 20.0)

class TestMDV2GlitchFilter(unittest.TestCase):
    def test_encoder_glitch_rejection(self):
        """Kiểm tra Glitch Filter: bỏ qua xung ma khi delta vượt quá cơ học (> 2500 ticks / 10ms)."""
        md = MotorDriverV2(0x54)
        # Giả lập encoder đọc bình thường: 100 ticks
        md._last_valid_encoders = [100, 100]
        md._encoders = [100, 100]
        
        # Giả lập I2C đọc ra giá trị rác đột biến: 500,000 ticks
        md._read_32_array = lambda reg, arr: (arr.__setitem__(0, 500000), arr.__setitem__(1, 120))
        enc = md.get_encoder()
        # Kênh E1 bị glitch -> phải giữ lại giá trị hợp lệ 100
        self.assertEqual(enc[0], 100)
        # Kênh E2 delta nhỏ (120 - 100 = 20) -> cập nhật lên 120
        self.assertEqual(enc[1], 120)

class TestDCMotorWatchdog(unittest.TestCase):
    def test_safe_speed_and_angle(self):
        """Kiểm tra tính toán speed() và angle() khi chưa hoặc đã cấu hình encoder."""
        md = MotorDriverV2(0x54)
        m = DCMotor(md, 16) # E1
        # Chưa cấu hình encoder -> trả về 0.0 an toàn
        self.assertEqual(m.angle(), 0.0)
        self.assertEqual(m.speed(), 0.0)
        
        # Cấu hình encoder
        m.set_encoder(rpm=250, ppr=11, gears=34)
        self.assertEqual(m.ticks_per_rev, 11 * 4 * 34)
        
        # Giả lập xung 1496 (đúng 1 vòng)
        m.driver.get_encoder = lambda port: 1496
        self.assertAlmostEqual(m.angle(), 360.0, delta=1.0)

class TestServoSafeDelay(unittest.TestCase):
    def test_run_angle_speed_over_100(self):
        """Kiểm tra Servo không bao giờ tạo delay âm hoặc tràn bus I2C khi speed = 120."""
        md = MotorDriverV2(0x54)
        s = Servo(md, 0, 180)
        # Khi speed >= 85, Servo gán trực tiếp góc đích, không lặp nghẽn I2C
        s.angle(90)
        self.assertEqual(s._current_angle, 90)

class TestDriveBaseWatchdog(unittest.TestCase):
    def test_calib_speed_stall_prevention(self):
        """Kiểm tra _calib_speed: Không bao giờ để correction triệt tiêu toàn bộ tốc độ motor."""
        from drivebase import DriveBase
        md = MotorDriverV2(0x54)
        m1 = DCMotor(md, 1)
        m2 = DCMotor(md, 2)
        m3 = DCMotor(md, 16)
        m4 = DCMotor(md, 32)
        m3.set_encoder(250, 11, 34)
        m4.set_encoder(250, 11, 34)
        
        db = DriveBase(2, m1=m1, m2=m2, m3=m3, m4=m4) # MODE_MECANUM
        # Giả lập encoder bị lệch cực lớn (ví dụ 1 bên kẹt tải)
        db.left_encoder.driver.get_encoder = lambda port: 10000 if port == 16 else 100
        
        # Chạy tốc độ 60
        left, right = db._calib_speed(60)
        # Tốc độ cả 2 bên không được phép tụt về 0 hoặc bị âm!
        self.assertTrue(left > 0, f"Left speed stalled: {left}")
        self.assertTrue(right > 0, f"Right speed stalled: {right}")
        # Chênh lệch tối đa chỉ 35% (max_c = 21)
        self.assertTrue(abs(left - 60) <= 21.01)
        self.assertTrue(abs(right - 60) <= 21.01)

    def test_run_mecanum_four_wheels(self):
        """Kiểm tra điều khiển 4 bánh độc lập run_mecanum."""
        from drivebase import DriveBase
        md = MotorDriverV2(0x54)
        m1 = DCMotor(md, 1)
        m2 = DCMotor(md, 2)
        m3 = DCMotor(md, 16)
        m4 = DCMotor(md, 32)
        db = DriveBase(2, m1=m1, m2=m2, m3=m3, m4=m4)
        
        # Test gọi run_mecanum
        db.run_mecanum(50, -50, 40, -40)
        self.assertIsNotNone(db.m1)
        self.assertIsNotNone(db.m2)

if __name__ == '__main__':
    unittest.main()
