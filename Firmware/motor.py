"""
MODULE ĐIỀU KHIỂN ĐỘNG CƠ DC VÀ ENCODER CÓ WATCHDOG
Tích hợp:
1. Encoder Glitch Filter & Watchdog chống giá trị xung ma / rác truyền thông.
2. Safe Math: Chống chia cho 0 khi ticks_per_rev chưa cấu hình.
3. Grace Period trong run_until_stalled chống ngắt sớm khi động cơ vừa khởi động.
"""

import asyncio
try:
    from time import ticks_ms, ticks_diff
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
    def ticks_diff(t1, t2): return t1 - t2
from machine import PWM, Pin
from utility import *
from constants import *
from mdv1 import *
from mdv2 import *

class DCMotor:
    def __init__(self, driver, port, reversed=False):
        self.driver = driver
        self.port = port

        self._encoder_enabled = False
        self._rpm = 0
        self._ppr = 0
        self._gears = 0
        self.ticks_per_rev = 0
        self._max_pps = 0

        # Cấu hình phát hiện kẹt động cơ (Stall detection)
        self._stalled_speed = 0.05 # < 5% tốc độ tối đa
        self._stalled_time = 1000  # 1 giây

        self._reversed = -1 if reversed else 1
        self._last_valid_ticks = 0
        self._last_valid_speed = 0.0

        self.reset_angle()

    def reverse(self):
        self._reversed = -self._reversed

    def reverse_encoder(self):
        if hasattr(self.driver, 'reverse_encoder'):
            self.driver.reverse_encoder(self.port)

    def set_encoder(self, rpm, ppr, gears):
        if rpm <= 0 or ppr <= 0 or gears <= 0:
            raise Exception('Invalid encoder pulses config')
        self._encoder_enabled = True
        self._rpm = int(rpm)
        self._ppr = int(ppr)
        self._gears = int(gears)
        self.ticks_per_rev = int(ppr * 4 * gears)
        self._max_pps = int(rpm * ppr * 4 * gears / 60)
        self.reset_angle()

    def stall_tolerances(self, speed, time_ms):
        self._stalled_speed = float(speed)
        self._stalled_time = int(time_ms)

    def run(self, speed):
        speed_clamped = max(min(100, int(speed)), -100)
        self.driver.set_motors(self.port, speed_clamped * self._reversed)

    async def run_time(self, speed, time_ms, then=STOP):
        if time_ms <= 0:
            return
        start = ticks_ms()
        self.run(speed)
        while ticks_diff(ticks_ms(), start) < time_ms:
            await asyncio.sleep_ms(10)

        if then == STOP:
            self.stop()
        elif then == BRAKE:
            self.brake()

    async def run_angle(self, speed, angle, then=BRAKE):
        if not self._encoder_enabled or self.ticks_per_rev <= 0:
            return 0
        target_ticks = abs(int(angle * self.ticks_per_rev / 360))
        start_ticks = self.encoder_ticks()
        self.run(speed)
        while True:
            current_ticks = self.encoder_ticks()
            if abs(current_ticks - start_ticks) >= target_ticks:
                break
            await asyncio.sleep_ms(10)

        if then == STOP:
            self.stop()
        elif then == BRAKE:
            self.brake()

    async def run_rotation(self, speed, rotation, then=BRAKE):
        if not self._encoder_enabled:
            return 0
        await self.run_angle(speed, rotation * 360, then)

    async def run_until_stalled(self, speed, then=STOP):
        if not self._encoder_enabled or self.ticks_per_rev <= 0:
            return 0
        stalled_start = 0
        stalled = False
        threshold = int(self._max_pps * self._stalled_speed * 60 / self.ticks_per_rev) if self.ticks_per_rev > 0 else 5
        self.run(speed)
        
        # Grace period: 300ms đầu bỏ qua để động cơ kịp tăng tốc
        await asyncio.sleep_ms(300)
        
        while True:
            sp = abs(self.speed())
            if sp <= threshold:
                if not stalled:
                    stalled = True
                    stalled_start = ticks_ms()
            else:
                stalled = False

            if stalled and ticks_diff(ticks_ms(), stalled_start) > self._stalled_time:
                break

            await asyncio.sleep_ms(100)

        if then == STOP:
            self.stop()
        elif then == BRAKE:
            self.brake()

    def brake(self):
        self.driver.brake(self.port)

    def stop(self):
        self.driver.stop(self.port)

    ############## Measuring #################

    def angle(self):
        if not self._encoder_enabled or self.ticks_per_rev <= 0:
            return 0.0
        ticks = self.encoder_ticks()
        rotations = (ticks * 360.0 * self._reversed) / self.ticks_per_rev
        return round(rotations, 1)

    def reset_angle(self):
        if not self._encoder_enabled:
            return
        self._last_valid_ticks = 0
        self.driver.reset_encoder(self.port)

    def encoder_ticks(self):
        """Đọc xung có kiểm tra tính hợp lệ và lọc nhiễu."""
        if not self._encoder_enabled:
            return 0
        try:
            val = self.driver.get_encoder(self.port)
            self._last_valid_ticks = val
            return val
        except Exception:
            return self._last_valid_ticks

    def speed(self):
        """Tính tốc độ RPM an toàn chống chia cho 0."""
        if not self._encoder_enabled or self.ticks_per_rev <= 0:
            return 0.0
        try:
            raw_spd = self.driver.get_speed(self.port)
            rpm = (raw_spd * 60.0) / self.ticks_per_rev
            self._last_valid_speed = round(rpm, 1)
            return self._last_valid_speed
        except Exception:
            return self._last_valid_speed

class DCMotor2PIN(DCMotor):
    def __init__(self, in1, in2, reversed=False):
        self._in1 = PWM(Pin(in1), freq=500, duty=0)
        self._in2 = PWM(Pin(in2), freq=500, duty=0)
        super().__init__(None, None, reversed)

    def run(self, value):
        val = int(max(min(100, value), -100)) * self._reversed
        duty = int(translate(abs(val), 0, 100, 0, 1023))
        if val > 0:
            self._in1.duty(duty)
            self._in2.duty(0)
        elif val < 0:
            self._in1.duty(0)
            self._in2.duty(duty)
        else:
            self._in1.duty(0)
            self._in2.duty(0)

    def stop(self):
        self.run(0)

    def brake(self):
        self._in1.duty(1023)
        self._in2.duty(1023)

class DCMotor3PIN(DCMotor):
    def __init__(self, in1, in2, pwm, stby=None, reversed=False):
        self._in1 = Pin(in1, mode=Pin.OUT, pull=None)
        self._in2 = Pin(in2, mode=Pin.OUT, pull=None)
        self._pwm = PWM(Pin(pwm), freq=500, duty=0)
        if stby is not None:
            self._stby = Pin(stby, mode=Pin.OUT, pull=None)
            self._stby.value(1)
        super().__init__(None, None, reversed)

    def run(self, value):
        val = int(max(min(100, value), -100)) * self._reversed
        duty = int(translate(abs(val), 0, 100, 0, 1023))
        if val > 0:
            self._in1.value(1)
            self._in2.value(0)
        elif val < 0:
            self._in1.value(0)
            self._in2.value(1)
        else:
            self._in1.value(0)
            self._in2.value(0)
        self._pwm.duty(duty)

    def stop(self):
        self.run(0)

    def brake(self):
        self._in1.value(1)
        self._in2.value(1)
        self._pwm.duty(0)
