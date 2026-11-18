"""
=============================================================================
ORC K2 ROBOT - HYBRID OBSTACLE DETECTION & MAZE SENSING SYSTEM
=============================================================================
Cấu hình cảm biến chuẩn thi đấu "Sắc Hoa Tri Ân" (ESP32-S3 K2 Hub):
1. Cảm biến TRƯỚC (Front): Siêu âm HY-SRF05 / HC-SR04
   - Cổng D3 - D4: Trig = GPIO 6, Echo = GPIO 7 (hỗ trợ Auto-Swap)
   - Đo cự ly siêu âm dải 2cm - 400cm, trả về 999.0 cm khi timeout / kẹt quá sát.
2. Cảm biến TRÁI (Left): Laser ToF VL53L0X
   - Cổng D5 - D6: SCL = Pin(9), SDA = Pin(8) trên SoftI2C riêng.
   - Bám tường trái cực nhạy, độ phân giải 1mm.
3. Cảm biến PHẢI (Right): Laser ToF VL53L0X
   - Cổng D7 - D8: SCL = Pin(17), SDA = Pin(10) trên SoftI2C riêng.
   - Đo khoảng trống bên phải để rẽ ngã ba / quay đầu.

Tính năng:
- Bộ lọc trung vị (Median Filter) + EMA khử xung nhiễu
- Cung cấp giao diện đọc cả 2 đơn vị: milimet (mm) và centimet (cm)
- `read_all_cm()` -> (front_cm, left_cm, right_cm) phục vụ trực tiếp thuật toán Left Wall Follower PID
- Quy đổi an toàn giá trị ngoài tầm (>1.5m / 8190mm) sang 999.0 cm để nhận diện mở ngã rẽ mà không gây báo kẹt nhầm
=============================================================================
"""

import time
from machine import Pin, SoftI2C
import vl53l0x
from hcsr04 import HCSR04


class DistanceFilter:
    """
    Bộ lọc lai Median Filter (5 mẫu) + EMA để khử xung nhiễu 8190mm và làm mịn tín hiệu laser.
    """
    def __init__(self, window_size=5, alpha=0.40, max_range_mm=2000):
        self.window_size = window_size
        self.alpha = alpha
        self.max_range_mm = max_range_mm
        self.window = []
        self.ema = None
        self.last_valid = max_range_mm

    def update(self, raw_val):
        if raw_val is None or raw_val <= 0:
            raw_val = 8190

        # Fast Attack: Khi phát hiện vật cản gần (< 350mm) mà trước đó đang xa (> 600mm),
        # cập nhật tức thì để phanh kịp thời, không bị trễ bởi cửa sổ median
        if raw_val < 350 and (self.ema is None or self.ema > 600):
            self.window = [raw_val]
            self.ema = float(raw_val)
            self.last_valid = raw_val
            return raw_val

        self.window.append(raw_val)
        if len(self.window) > self.window_size:
            self.window.pop(0)

        # 1. Median Filter loại bỏ xung đột biến (8190mm)
        s = sorted(self.window)
        med = s[len(s) // 2]

        # 2. Bộ lọc Exponential Moving Average (EMA) cho dải đo thực
        if med < 8000:
            self.last_valid = med
            if self.ema is None or self.ema >= 8000:
                self.ema = float(med)
            else:
                self.ema = self.alpha * float(med) + (1.0 - self.alpha) * self.ema
        else:
            self.ema = 8190.0

        return int(round(self.ema))

    def reset(self):
        self.window.clear()
        self.ema = None


class LaserSystem:
    """
    Hệ thống cảm biến kết hợp cho Robot ORC K2:
    - TRƯỚC: Siêu âm HY-SRF05 / HC-SR04 (Cổng D3-D4: GPIO 6 & 7)
    - TRÁI : Laser VL53L0X (Cổng D5-D6: SCL=9, SDA=8)
    - PHẢI : Laser VL53L0X (Cổng D7-D8: SCL=17, SDA=10)
    """

    # Ánh xạ chân cứng cổng Grove trên mạch K2 Hub (ESP32-S3)
    PORT_FRONT_US = {"trig": 6, "echo": 7}  # Cổng D3 - D4 (GPIO 6 & 7)
    PORT_LEFT = {"scl": 9, "sda": 8}        # Cổng D5 - D6 (GPIO 8 & 9)
    PORT_RIGHT = {"scl": 17, "sda": 10}     # Cổng D7 - D8 (GPIO 10 & 17)

    def __init__(self, continuous=True, timing_budget_us=33000):
        self.continuous = continuous
        self.timing_budget_us = timing_budget_us

        # Đối tượng cảm biến phần cứng
        self.sensor_front = None
        self.front_sensor = None
        self.sensor_center = None

        self.sensor_left = None
        self.left_sensor = None

        self.sensor_right = None
        self.right_sensor = None

        # Bộ lọc số cho kênh laser trái & phải
        self.filter_left = DistanceFilter(window_size=5, alpha=0.40)
        self.filter_right = DistanceFilter(window_size=5, alpha=0.40)

        # Bộ nhớ lưu giá trị gần nhất
        self._last_raw = (9990, 8190, 8190)
        self._last_filtered = (9990, 8190, 8190)
        self._last_cm = (999.0, 999.0, 999.0)

        self._init_all_sensors()

    def _init_all_sensors(self):
        # 1. Cảm biến Siêu âm TRƯỚC (D3-D4: Trig=6, Echo=7, Auto-Swap)
        try:
            self.sensor_front = HCSR04(
                trig_pin=self.PORT_FRONT_US["trig"],
                echo_pin=self.PORT_FRONT_US["echo"],
                echo_timeout_us=25000,
                auto_detect=True
            )
            self.front_sensor = self.sensor_front
            self.sensor_center = self.sensor_front
            print("[SENSOR] Sieu am HY-SRF05 Truoc (D3-D4: GPIO 6 & 7) khoi tao thanh cong.")
        except Exception as e:
            print("[SENSOR] Canh bao: Loi khoi tao Sieu am Truoc:", e)
            self.sensor_front = None
            self.front_sensor = None
            self.sensor_center = None

        # 2. Cảm biến Laser TRÁI (D5-D6: SCL=9, SDA=8, 100kHz)
        try:
            self.i2c_left = SoftI2C(
                scl=Pin(self.PORT_LEFT["scl"], Pin.IN, Pin.PULL_UP),
                sda=Pin(self.PORT_LEFT["sda"], Pin.IN, Pin.PULL_UP),
                freq=100000,
                timeout=10000
            )
            try:
                self.i2c_left.writeto(0x29, bytes([0xFF, 0x00]))
            except Exception:
                pass
            devs = self.i2c_left.scan()
            if 0x29 in devs:
                self.sensor_left = vl53l0x.VL53L0X(self.i2c_left, address=0x29, io_timeout_ms=100)
                self.sensor_left.measurement_timing_budget = self.timing_budget_us
                if self.continuous:
                    self.sensor_left.start_continuous()
                self.left_sensor = self.sensor_left
                print("[SENSOR] Laser VL53L0X Trai (D5-D6: SCL=9, SDA=8) khoi tao thanh cong.")
            else:
                print("[SENSOR] Canh bao: Khong tim thay VL53L0X tai Cong D5-D6 Trai (Addr 0x29).")
        except Exception as e:
            print("[SENSOR] Loi khoi tao Laser Trai:", e)

        # 3. Cảm biến Laser PHẢI (D7-D8: SCL=17, SDA=10, 100kHz)
        try:
            self.i2c_right = SoftI2C(
                scl=Pin(self.PORT_RIGHT["scl"], Pin.IN, Pin.PULL_UP),
                sda=Pin(self.PORT_RIGHT["sda"], Pin.IN, Pin.PULL_UP),
                freq=100000,
                timeout=10000
            )
            try:
                self.i2c_right.writeto(0x29, bytes([0xFF, 0x00]))
            except Exception:
                pass
            devs = self.i2c_right.scan()
            if 0x29 in devs:
                self.sensor_right = vl53l0x.VL53L0X(self.i2c_right, address=0x29, io_timeout_ms=100)
                self.sensor_right.measurement_timing_budget = self.timing_budget_us
                if self.continuous:
                    self.sensor_right.start_continuous()
                self.right_sensor = self.sensor_right
                print("[SENSOR] Laser VL53L0X Phai (D7-D8: SCL=17, SDA=10) khoi tao thanh cong.")
            else:
                print("[SENSOR] Canh bao: Khong tim thay VL53L0X tai Cong D7-D8 Phai (Addr 0x29).")
        except Exception as e:
            print("[SENSOR] Loi khoi tao Laser Phai:", e)

    # -------------------------------------------------------------------------
    # HÀM ĐỌC ĐƠN VỊ CENTIMET (CM) - DÙNG CHO THUẬT TOÁN LEFT WALL FOLLOWER PID
    # -------------------------------------------------------------------------
    def read_front_cm(self, raw=False):
        """Đọc khoảng cách cảm biến siêu âm TRƯỚC theo cm (999.0 nếu timeout/kẹt)."""
        if self.sensor_front is None:
            return 999.0
        try:
            return self.sensor_front.distance_cm(filtered=not raw)
        except Exception:
            return 999.0

    def read_left_cm(self, raw=False):
        """
        Đọc khoảng cách Laser TRÁI theo cm:
        - Trong tầm đo bình thường: trả về mm / 10.0 (cm).
        - Khi ngoài tầm đo (> 1.5m / 8190mm): trả về 999.0 cm (mở hành lang / ngã rẽ).
        """
        mm = self.read_left(raw=raw)
        if mm >= 8000:
            return 999.0
        return round(mm / 10.0, 1)

    def read_right_cm(self, raw=False):
        """
        Đọc khoảng cách Laser PHẢI theo cm:
        - Trong tầm đo bình thường: trả về mm / 10.0 (cm).
        - Khi ngoài tầm đo (> 1.5m / 8190mm): trả về 999.0 cm (trống bên phải).
        """
        mm = self.read_right(raw=raw)
        if mm >= 8000:
            return 999.0
        return round(mm / 10.0, 1)

    def read_all_cm(self, raw=False):
        """
        Đọc đồng thời 3 cảm biến theo đơn vị Centimet (cm).
        Trả về tuple: (distanceF, distanceL, distanceR) chuẩn Arduino.
        """
        df = self.read_front_cm(raw=raw)
        dl = self.read_left_cm(raw=raw)
        dr = self.read_right_cm(raw=raw)
        self._last_cm = (df, dl, dr)
        return (df, dl, dr)

    # -------------------------------------------------------------------------
    # HÀM ĐỌC ĐƠN VỊ MILIMET (MM) - TƯƠNG THÍCH NGƯỢC HỆ THỐNG CŨ
    # -------------------------------------------------------------------------
    def read_front(self, raw=False):
        """Đọc cự ly cảm biến TRƯỚC theo mm (9990 nếu timeout)."""
        if self.sensor_front is None:
            return 9990
        try:
            return self.sensor_front.distance_mm(filtered=not raw)
        except Exception:
            return 9990

    def read_center(self, raw=False):
        """Alias tương thích ngược."""
        return self.read_front(raw=raw)

    def read_left(self, raw=False):
        """Đọc cự ly cảm biến Laser TRÁI theo mm (8190 nếu ngoài tầm)."""
        s = self.sensor_left
        if s is None:
            return 8190
        try:
            raw_val = s.read()
        except Exception:
            raw_val = 8190
        if raw:
            return raw_val
        return self.filter_left.update(raw_val)

    def read_right(self, raw=False):
        """Đọc cự ly cảm biến Laser PHẢI theo mm (8190 nếu ngoài tầm)."""
        s = self.sensor_right
        if s is None:
            return 8190
        try:
            raw_val = s.read()
        except Exception:
            raw_val = 8190
        if raw:
            return raw_val
        return self.filter_right.update(raw_val)

    def read_all(self, raw=False):
        """
        Đọc cả 3 cảm biến theo đơn vị milimet (mm).
        Trả về: tuple (front_mm, left_mm, right_mm).
        """
        df = self.read_front(raw=raw)
        dl = self.read_left(raw=raw)
        dr = self.read_right(raw=raw)
        if raw:
            self._last_raw = (df, dl, dr)
        else:
            self._last_filtered = (df, dl, dr)
        return (df, dl, dr)

    def has_obstacle(self, threshold_mm=200):
        """Kiểm tra có vật cản nào gần hơn ngưỡng threshold_mm không."""
        df, dl, dr = self.read_all(raw=False)
        return (df < 9000 and df < threshold_mm) or (dl < threshold_mm) or (dr < threshold_mm)

    def check_obstacles(self, threshold_mm=200):
        """Kiểm tra chi tiết từng hướng vật cản dạng tuple bool."""
        df, dl, dr = self.read_all(raw=False)
        return (df < 9000 and df < threshold_mm, dl < threshold_mm, dr < threshold_mm)

    def is_obstacle_ahead(self, threshold_mm=180, distance=None):
        """Kiểm tra vật cản phía trước mặt."""
        d = distance if distance is not None else self._last_filtered[0]
        return (d < 9000 and d < threshold_mm)

    def is_flower_in_capture_range(self, min_mm=35, max_mm=140, distance=None):
        """Kiểm tra ống hoa trong tầm gắp."""
        d = distance if distance is not None else self._last_filtered[0]
        return (min_mm <= d <= max_mm)

    def get_maze_centering_offset(self, max_wall_dist_mm=320, d_left=None, d_right=None, desired_dist_mm=160):
        """Tính sai lệch tâm xe giữa 2 vách mê cung cho di chuyển Mecanum Strafe."""
        if d_left is None:
            d_left = self._last_filtered[1]
        if d_right is None:
            d_right = self._last_filtered[2]

        has_left = (0 < d_left < max_wall_dist_mm)
        has_right = (0 < d_right < max_wall_dist_mm)

        if has_left and has_right:
            return float(d_right - d_left)
        elif has_left and not has_right:
            err = float(desired_dist_mm - d_left)
            return max(-50.0, min(50.0, err))
        elif has_right and not has_left:
            err = float(d_right - desired_dist_mm)
            return max(-50.0, min(50.0, err))
        return 0.0

    def soft_brake(self, drivebase, safe_distance=150, slow_distance=350):
        """Phanh mềm an toàn chủ động theo cự ly."""
        df, dl, dr = self.read_all(raw=False)
        min_front = df if df < 9000 else 9999
        min_dist = min(min_front, min(dl, dr))

        if min_dist <= safe_distance:
            drivebase.brake()
            return True

        if min_dist < slow_distance:
            scale = (min_dist - safe_distance) / (slow_distance - safe_distance)
            scale = max(0.35, min(1.0, scale))
            current_speed = drivebase.speed()
            reduced_speed = int(current_speed * scale)
            if hasattr(drivebase, 'run_speed'):
                drivebase.run_speed(reduced_speed, reduced_speed)
            return False

        return False

    def print_status(self):
        df, dl, dr = self.read_all_cm(raw=False)
        print(f"[SENSOR STATUS] Truoc (SRF05): {df:5.1f}cm | Trai (Laser): {dl:5.1f}cm | Phai (Laser): {dr:5.1f}cm")
