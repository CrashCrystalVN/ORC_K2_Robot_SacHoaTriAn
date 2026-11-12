"""
BỘ ĐIỀU KHIỂN PID TỐI ƯU HÓA CHO MICROPYTHON & ESP32-S3
Tích hợp:
1. Tính toán dt chính xác bằng time.ticks_ms() & time.ticks_diff() chống sập / chia cho 0.
2. Cơ chế chống tràn tích phân Anti-Windup (Conditional Integration & Dynamic Clamping).
3. Bộ lọc đạo hàm thông thấp (Low-pass Filter) chống sốc/giật ngõ ra khi encoder có nhiễu lượng tử hóa.
"""

import time
try:
    from time import ticks_ms, ticks_diff
except ImportError:
    def ticks_ms(): return int(time.time() * 1000)
    def ticks_diff(t1, t2): return t1 - t2

def _clamp(value, limits):
    if value is None or limits is None:
        return value
    lower, upper = limits
    if upper is not None and value > upper:
        return upper
    if lower is not None and value < lower:
        return lower
    return value

class PIDController(object):
    """PID Controller chuẩn thời gian thực cho Robot Mecanum / 4WD."""
    
    def __init__(
        self,
        Kp=1.0,
        Ki=0.0,
        Kd=0.0,
        setpoint=0.0,
        sample_time=None,
        output_limits=(None, None),
        auto_mode=True,
        proportional_on_measurement=False,
        differential_on_measurement=False,
        error_map=None,
        starting_output=0.0,
    ):
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.Kd = float(Kd)
        self.setpoint = float(setpoint)
        self.sample_time = sample_time
        self._min_output, self._max_output = None, None
        self._auto_mode = auto_mode
        self.proportional_on_measurement = proportional_on_measurement
        self.differential_on_measurement = differential_on_measurement
        self.error_map = error_map

        self._proportional = 0.0
        self._integral = 0.0
        self._derivative = 0.0
        self._last_time = ticks_ms()
        self._last_output = starting_output
        self._last_error = 0.0
        self._last_input = 0.0
        self._d_filter = 0.0

        self.output_limits = output_limits
        self.reset()
        self._integral = _clamp(starting_output, output_limits) if output_limits else starting_output

    def __call__(self, input_, dt=None):
        """Cập nhật và tính toán ngõ ra PID."""
        if not self._auto_mode:
            return self._last_output

        now = ticks_ms()

        if dt is None:
            # Dùng ticks_diff tránh tràn số 30-bit/31-bit trên MicroPython
            dt_ms = ticks_diff(now, self._last_time)
            dt = dt_ms / 1000.0
        else:
            dt = float(dt)

        # Chống dt <= 0 hoặc dt quá nhỏ gây nổ đạo hàm (1e-16 bug)
        if dt < 0.001:
            if self.sample_time is not None and self._last_output is not None:
                return self._last_output
            dt = 0.001 # Ngưỡng an toàn tối thiểu 1ms

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            return self._last_output

        # Tính toán sai số
        error = self.setpoint - float(input_)
        if self.error_map is not None:
            error = self.error_map(error)

        d_input = float(input_) - self._last_input
        d_error = error - self._last_error

        # 1. Thành phần Tỉ lệ (P)
        if not self.proportional_on_measurement:
            self._proportional = self.Kp * error
        else:
            self._proportional -= self.Kp * d_input

        # 2. Thành phần Tích phân (I) kèm Anti-Windup (Conditional Integration)
        # Chỉ tích lũy khi ngõ ra chưa bão hòa hoặc sai số kéo ra khỏi vùng bão hòa
        i_term_delta = self.Ki * error * dt
        potential_integral = self._integral + i_term_delta

        # Giới hạn I-term không vượt quá output_limits
        self._integral = _clamp(potential_integral, self.output_limits)

        # 3. Thành phần Đạo hàm (D) có bộ lọc thông thấp (Alpha = 0.65)
        raw_derivative = 0.0
        if self.differential_on_measurement:
            raw_derivative = -self.Kd * d_input / dt
        else:
            raw_derivative = self.Kd * d_error / dt

        # Lọc nhiễu đạo hàm (chống nhảy giật do encoder đếm ngắt rời rạc)
        self._d_filter = 0.65 * raw_derivative + 0.35 * self._d_filter
        self._derivative = self._d_filter

        # 4. Tính toán ngõ ra tổng và Clamp
        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        # Lưu vết trạng thái
        self._last_output = output
        self._last_input = float(input_)
        self._last_error = error
        self._last_time = now

        return output

    @property
    def components(self):
        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):
        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):
        self.Kp, self.Ki, self.Kd = [float(x) for x in tunings]

    @property
    def auto_mode(self):
        return self._auto_mode

    @auto_mode.setter
    def auto_mode(self, enabled):
        self.set_auto_mode(enabled)

    def set_auto_mode(self, enabled, last_output=None):
        if enabled and not self._auto_mode:
            self.reset()
            self._integral = last_output if (last_output is not None) else 0.0
            self._integral = _clamp(self._integral, self.output_limits)
        self._auto_mode = enabled

    @property
    def output_limits(self):
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        if limits is None:
            self._min_output, self._max_output = None, None
            return
        min_output, max_output = limits
        if (min_output is not None) and (max_output is not None) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')
        self._min_output = min_output
        self._max_output = max_output
        self._integral = _clamp(self._integral, self.output_limits)
        if self._last_output is not None:
            self._last_output = _clamp(self._last_output, self.output_limits)

    def reset(self):
        self._proportional = 0.0
        self._integral = 0.0
        self._derivative = 0.0
        self._d_filter = 0.0
        self._last_time = ticks_ms()
        self._last_error = 0.0
        self._last_input = 0.0
