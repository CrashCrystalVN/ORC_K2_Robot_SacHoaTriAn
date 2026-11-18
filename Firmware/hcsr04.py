"""
=============================================================================
ORC K2 ROBOT - HC-SR04 / HY-SRF05 ULTRASONIC SENSOR DRIVER
=============================================================================
Driver cảm biến siêu âm HY-SRF05 / HC-SR04 trên MicroPython ESP32-S3.
- Cổng kết nối mặc định: D3 - D4 (GPIO 6 & GPIO 7)
- Chân Trig: D3 (GPIO 6, OUTPUT)
- Chân Echo: D4 (GPIO 7, INPUT)
- Hỗ trợ cơ chế tự động dò/đảo chân (Auto-Swap Detection) nếu cắm ngược (Trig=7, Echo=6)
- Trả về 999.0 cm khi timeout / quá cự ly / kẹt quá sát theo chuẩn Arduino getDistance()
=============================================================================
"""

import time
from machine import Pin, time_pulse_us


class HCSR04:
    """
    Driver cảm biến siêu âm HY-SRF05 / HC-SR04 đo khoảng cách chính xác cao:
    - time_pulse_us đo xung Echo với timeout 25,000 us (~4.25 mét).
    - Khi timeout trả về 999.0 cm chuẩn hóa cho thuật toán chống kẹt.
    - Tích hợp bộ lọc trung vị (Median Filter 3 mẫu) nhẹ khử nhiễu tia phản xạ dội.
    """

    def __init__(self, trig_pin=6, echo_pin=7, echo_timeout_us=25000, auto_detect=True):
        self.trig_num = trig_pin
        self.echo_num = echo_pin
        self.echo_timeout_us = echo_timeout_us
        self.auto_detect = auto_detect
        self.pins_swapped = False

        self._init_pins(self.trig_num, self.echo_num)

        # Lịch sử 3 mẫu gần nhất cho bộ lọc Median nhẹ
        self._history = []

        if self.auto_detect:
            self._probe_pin_orientation()

    def _init_pins(self, trig_num, echo_num):
        """Khởi tạo cấu hình phần cứng chân GPIO"""
        try:
            self.trig = Pin(trig_num, Pin.OUT)
            self.echo = Pin(echo_num, Pin.IN)
            self.trig.value(0)
        except Exception as e:
            print("[HCSR04] Loi khoi tao Pin:", e)

    def _probe_pin_orientation(self):
        """
        Tự động kiểm tra hướng cắm Trig/Echo trên cổng D3-D4.
        Nếu cắm ngược (Trig=7, Echo=6), tự động hoán đổi chân để cảm biến hoạt động ngay!
        """
        # Thử đọc 2 lần ở cấu hình hiện tại
        d1 = self._measure_single_pulse()
        if d1 < 900.0:
            # Hoạt động chuẩn xác ở cấu hình hiện tại
            return

        # Nếu trả về 999, thử đảo chân (trig <-> echo)
        try:
            temp_trig = Pin(self.echo_num, Pin.OUT)
            temp_echo = Pin(self.trig_num, Pin.IN)
            temp_trig.value(0)

            # Bắn xung thử nghiệm
            temp_trig.value(0)
            time.sleep_us(2)
            temp_trig.value(1)
            time.sleep_us(10)
            temp_trig.value(0)

            pulse = time_pulse_us(temp_echo, 1, self.echo_timeout_us)
            if pulse > 0:
                dist = pulse * 0.0343 / 2.0
                if 2.0 <= dist <= 400.0:
                    # Hoán đổi thành công!
                    self.trig_num, self.echo_num = self.echo_num, self.trig_num
                    self.trig = temp_trig
                    self.echo = temp_echo
                    self.pins_swapped = True
                    print(f"[HCSR04] Tu dong nhan dien cam bien nguoc: Hoan doi sang Trig={self.trig_num}, Echo={self.echo_num}")
                    return
        except Exception:
            pass

        # Giữ nguyên cấu hình ban đầu
        self._init_pins(self.trig_num, self.echo_num)

    def _measure_single_pulse(self):
        """Đo xung phản hồi đơn lẻ (trả về cm hoặc 999.0 nếu timeout)"""
        try:
            # Phát xung Trigger tối thiểu 10us
            self.trig.value(0)
            time.sleep_us(2)
            self.trig.value(1)
            time.sleep_us(10)
            self.trig.value(0)

            # Đo độ rộng xung mức HIGH trên chân Echo
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            if pulse_time <= 0:
                return 999.0  # Timeout hoặc không có vật cản phản hồi

            # Tốc độ âm thanh trong không khí ~343 m/s = 0.0343 cm/us
            dist_cm = (pulse_time * 0.0343) / 2.0

            # Giới hạn vật lý của cảm biến SRF05 (2cm - 400cm)
            if dist_cm < 1.5 or dist_cm > 450.0:
                return 999.0

            return round(dist_cm, 1)

        except OSError:
            return 999.0
        except Exception:
            return 999.0

    def distance_cm(self, filtered=True):
        """
        Đọc khoảng cách theo đơn vị centimet (cm).
        - filtered=True: Dùng Median Filter 3 mẫu để triệt tiêu nhiễu tia dội góc tường.
        - Trả về 999.0 nếu timeout hoặc mất phản hồi.
        """
        val = self._measure_single_pulse()

        if not filtered:
            return val

        # Fast attack: nếu có vật cản gần (< 15cm) xuất hiện đột ngột, phản hồi tức thì
        if val < 15.0 and len(self._history) > 0 and self._history[-1] > 25.0:
            self._history = [val]
            return val

        self._history.append(val)
        if len(self._history) > 3:
            self._history.pop(0)

        # Median Filter 3 mẫu
        sorted_h = sorted(self._history)
        med = sorted_h[len(sorted_h) // 2]
        return med

    def distance_mm(self, filtered=True):
        """Đọc khoảng cách theo đơn vị milimet (mm) để tương thích LaserSystem"""
        d_cm = self.distance_cm(filtered=filtered)
        if d_cm >= 900.0:
            return 9990
        return int(round(d_cm * 10.0))
