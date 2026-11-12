"""
MODULE ĐIỀU KHIỂN ĐỘNG CƠ SERVO TAY GẮP & KHỚP CỔ TAY (S1, S2, S3, S4)
Tối ưu hóa:
1. Chống tràn / nghẽn I2C (I2C Bus Flooding Protection) khi nhận speed > 100 hoặc speed cao.
2. Với speed >= 85: Gửi trực tiếp góc đích, loại bỏ vòng lặp 1 độ/bước làm nghẽn bus I2C.
3. Với speed < 85: Làm mịn bước xoay (2-3 độ/bước) kèm delay tối thiểu an toàn >= 10ms.
"""

import asyncio
from machine import PWM, Pin
from utility import *
from mdv2 import *

class Servo:
    def __init__(self, *args):
        if len(args) == 3:
            if isinstance(args[0], MotorDriverV2):
                self._driver = args[0]
                self._port = int(args[1])
                self._max_angle = int(args[2])
            else:
                raise ValueError('Invalid servo argument')

        elif len(args) == 2:
            if isinstance(args[0], int):
                self._port = PWM(Pin(int(args[0])))
                self._port.freq(50)
                self._driver = None
                self._max_angle = int(args[1])
            else:
                raise ValueError('Invalid servo argument')

        self._current_angle = None
        self._limit_min = 0
        if self._max_angle is None or self._max_angle <= 0:
            self._max_angle = 180

        self._limit_max = self._max_angle

    def limit(self, min=0, max=180, min_val=None, max_val=None):
        if min_val is not None:
            min = min_val
        if max_val is not None:
            max = max_val
        if min < 0 or min > max or max > self._max_angle:
            raise ValueError('Invalid servo limit value')

        self._limit_min = int(min)
        self._limit_max = int(max)

    def _angle_to_pulse(self, angle):
        pulse = 25 + int((angle / self._max_angle) * 100)
        return pulse

    def angle(self, angle):
        target = int(max(min(self._limit_max, angle), self._limit_min))

        if self._driver:
            self._driver.set_servo(self._port, target, self._max_angle)
        else:
            pulse = self._angle_to_pulse(target)
            self._port.duty(pulse)

        self._current_angle = target

    async def run_angle(self, angle, speed=100):
        """
        Quay Servo đến góc angle với tốc độ speed (1-100).
        Khắc phục triệt để lỗi nghẽn bus I2C khi speed >= 85 hoặc speed > 100.
        """
        target = int(max(min(self._limit_max, angle), self._limit_min))
        speed_safe = max(1, min(100, int(speed)))

        # Nếu tốc độ cao (>=85) hoặc chưa biết góc hiện tại:
        # Gửi trực tiếp góc đích, để mạch Servo tự điều khiển chiết áp mượt mà
        # Tránh gửi hàng chục gói tin I2C làm tê liệt giao tiếp động cơ và encoder!
        if speed_safe >= 85 or self._current_angle is None:
            self.angle(target)
            return

        # Với tốc độ chậm (<85): quét góc với bước 2-3 độ và delay an toàn
        delay_ms = max(10, int(translate(speed_safe, 1, 85, 30, 10)))
        step = 2

        if self._current_angle > target:
            for i in range(self._current_angle, target - 1, -step):
                self.angle(max(target, i))
                await asyncio.sleep_ms(delay_ms)
        else:
            for i in range(self._current_angle, target + 1, step):
                self.angle(min(target, i))
                await asyncio.sleep_ms(delay_ms)

        self.angle(target)

    async def run_steps(self, steps, speed=100):
        if self._current_angle is None:
            self._current_angle = 90
        new_pos = self._current_angle + int(steps)
        await self.run_angle(new_pos, speed)

    def spin(self, speed):
        spd = int(max(min(100, speed), -100))
        ang = 90 - (spd / 100.0) * 90
        self.angle(ang)

