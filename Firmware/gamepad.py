"""
MODULE ĐỌC TAY CẦM GAMEPAD (PS4 I2C RECEIVER & OHSTEM APP BLE)
Đã chuẩn hóa đọc tín hiệu trục Joystick, các nút bấm, rung Haptic Rumble và đổi màu LED.
"""

import math
import asyncio
from micropython import const
try:
    from time import ticks_ms
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
from utility import *
from ble import *
from constants import *
from ps4_receiver import PS4GamepadReceiver

def _parse_signed_byte(val):
    val = val & 0xFF
    return val - 256 if val > 127 else val

class Gamepad:
    def __init__(self):
        self._verbose = False
        self._last_print = 0

        self.data = {
            BTN_UP: 0,
            BTN_DOWN: 0,
            BTN_LEFT: 0,
            BTN_RIGHT: 0,
            BTN_SQUARE: 0,
            BTN_TRIANGLE: 0,
            BTN_CROSS: 0,
            BTN_CIRCLE: 0,
            BTN_L1: 0,
            BTN_R1: 0,
            BTN_L2: 0,
            BTN_R2: 0,
            BTN_THUMBL: 0,
            BTN_THUMBR: 0,
            BTN_M1: 0,
            BTN_M2: 0,
            'OPTIONS': 0,
            'START': 0,
            'SHARE': 0,
            'SELECT': 0,
            AL: 0,
            ALX: 0,
            ALY: 0,
            AL_DIR: -1,
            AL_DISTANCE: 0,
            AR: 0,
            ARX: 0,
            ARY: 0,
            AR_DIR: -1,
            AR_DISTANCE: 0,
        }

        self._cmd = None
        self._last_cmd = None
        self._run_speed = 0
        self._cmd_handlers = {}
        self._last_btn_states = {}

        # Mạch nhận tín hiệu Gamepad PS4 qua SoftI2C
        try:
            self._ps4_gamepad = PS4GamepadReceiver()
        except Exception as e:
            print('[GAMEPAD] PS4 receiver not detected via I2C:', e)
            self._ps4_gamepad = None

        # Kết nối BLE Gamepad trên ứng dụng OhStem
        try:
            ble.on_receive_msg('name_value', self.on_ble_cmd)
        except Exception:
            pass

    @property
    def is_connected(self):
        """Kiểm tra tay cầm PS4 có đang kết nối không."""
        if self._ps4_gamepad:
            return getattr(self._ps4_gamepad, 'is_connected', False)
        return False

    def set_rumble(self, force=255, duration=255):
        """
        Gửi lệnh rung trực tiếp tới tay cầm PS4.
        force: 0-255
        duration: 0-255
        """
        if self._ps4_gamepad:
            try:
                self._ps4_gamepad.set_rumble(force, duration)
            except Exception:
                pass

    async def rumble_pulse(self, duration_ms=200, force=220):
        """
        Rung tay cầm trong khoảng thời gian duration_ms (ms), sau đó tự động ngắt.
        """
        if self._ps4_gamepad:
            try:
                dur_param = min(255, max(1, duration_ms // 10))
                self._ps4_gamepad.set_rumble(force, dur_param)
            except Exception:
                pass
        await asyncio.sleep_ms(duration_ms)
        if self._ps4_gamepad:
            try:
                self._ps4_gamepad.set_rumble(0, 0)
            except Exception:
                pass

    async def rumble_feedback(self, mode):
        """
        Phản hồi rung haptic theo chế độ yêu cầu:
        - "MANUAL": Tay cầm rung 1 cái ngắn (200ms)
        - "AUTO": Tay cầm rung 2 cái dài (500ms -> ngắt 200ms -> 500ms)
        """
        if mode == "MANUAL":
            await self.rumble_pulse(duration_ms=200, force=220)
        elif mode == "AUTO":
            await self.rumble_pulse(duration_ms=500, force=255)
            await asyncio.sleep_ms(200)
            await self.rumble_pulse(duration_ms=500, force=255)

    def set_led_color(self, r, g, b):
        """Đặt màu LED thanh sáng (Lightbar) trên tay cầm PS4."""
        if self._ps4_gamepad:
            try:
                self._ps4_gamepad.set_led_color([int(r), int(g), int(b)])
            except Exception:
                pass

    async def on_ble_cmd(self, name, value):
        if name in (BTN_M2, 'M2', 'OPTIONS', 'START'):
            self.data[BTN_M2] = value
            self.data['OPTIONS'] = value
            self.data['START'] = value
            return
        if name in (BTN_M1, 'M1', 'SHARE', 'SELECT'):
            self.data[BTN_M1] = value
            self.data['SHARE'] = value
            self.data['SELECT'] = value
            return

        if name not in self.data:
            return
        self.data[name] = value

        if name == AL or name == AR:
            try:
                val_int = int(value)
                # Dữ liệu từ App OhStem: 16-bit integer (High byte = X, Low byte = Y)
                ax = _parse_signed_byte(val_int >> 8)
                ay = _parse_signed_byte(val_int & 0xFF)

                if name == AL:
                    self.data[ALX] = ax
                    self.data[ALY] = ay
                    dir, distance = self._calculate_joystick(self.data[ALX], self.data[ALY])
                    self.data[AL_DIR] = dir
                    self.data[AL_DISTANCE] = distance
                elif name == AR:
                    self.data[ARX] = ax
                    self.data[ARY] = ay
                    dir, distance = self._calculate_joystick(self.data[ARX], self.data[ARY])
                    self.data[AR_DIR] = dir
                    self.data[AR_DISTANCE] = distance
            except Exception:
                pass

    def on_button_pressed(self, button, callback):
        """Đăng ký callback khi một nút được nhấn (sườn lên 0 -> 1)."""
        self._cmd_handlers[button] = callback

    async def run(self):
        while True:
            if self._ps4_gamepad:
                try:
                    self._ps4_gamepad.update()
                    if self._ps4_gamepad.is_connected:
                        p_data = self._ps4_gamepad.data
                        self.data[BTN_UP]       = p_data.get('dpad_up', 0)
                        self.data[BTN_DOWN]     = p_data.get('dpad_down', 0)
                        self.data[BTN_LEFT]     = p_data.get('dpad_left', 0)
                        self.data[BTN_RIGHT]    = p_data.get('dpad_right', 0)
                        self.data[BTN_CROSS]    = p_data.get('a', 0)
                        self.data[BTN_CIRCLE]   = p_data.get('b', 0)
                        self.data[BTN_SQUARE]   = p_data.get('x', 0)
                        self.data[BTN_TRIANGLE] = p_data.get('y', 0)
                        self.data[BTN_L1]       = p_data.get('l1', 0)
                        self.data[BTN_R1]       = p_data.get('r1', 0)
                        self.data[BTN_L2]       = p_data.get('l2', 0)
                        self.data[BTN_R2]       = p_data.get('r2', 0)
                        self.data[BTN_M1]       = p_data.get('m1', 0)
                        self.data[BTN_M2]       = p_data.get('m2', 0)
                        self.data['OPTIONS']    = self.data[BTN_M2]
                        self.data['START']      = self.data[BTN_M2]
                        self.data['SHARE']      = self.data[BTN_M1]
                        self.data['SELECT']     = self.data[BTN_M1]
                        self.data[BTN_THUMBL]   = p_data.get('thumbl', 0)
                        self.data[BTN_THUMBR]   = p_data.get('thumbr', 0)

                        # Ánh xạ chuẩn phần cứng tay cầm PS4 receiver I2C:
                        # - Cần Trái (J1 - AL):
                        #   + alx: Trục Ngang (-508 Trái .. +512 Phải) -> ALX (-100 .. +100)
                        #   + aly: Trục Dọc (-508 Tiến .. +512 Lùi) -> ALY (+100 .. -100)
                        alx = p_data.get('alx', 0)
                        self.data[ALX] = translate(alx, -508, 512, -100, 100)

                        aly = p_data.get('aly', 0)
                        self.data[ALY] = translate(aly, 512, -508, -100, 100)

                        dir, distance = self._calculate_joystick(self.data[ALX], self.data[ALY])
                        self.data[AL_DIR] = dir
                        self.data[AL_DISTANCE] = distance

                        # - Cần Phải (J2 - AR):
                        #   + arx: Trục Ngang (-508 Trái .. +512 Phải) -> ARX (-100 .. +100)
                        #   + ary: Trục Dọc (-508 Tiến .. +512 Lùi) -> ARY (+100 .. -100)
                        arx = p_data.get('arx', 0)
                        self.data[ARX] = translate(arx, -508, 512, -100, 100)

                        ary = p_data.get('ary', 0)
                        self.data[ARY] = translate(ary, 512, -508, -100, 100)

                        dir, distance = self._calculate_joystick(self.data[ARX], self.data[ARY])
                        self.data[AR_DIR] = dir
                        self.data[AR_DISTANCE] = distance
                except Exception:
                    pass

            # Kiểm tra sườn lên (vừa nhấn 0 -> 1) cho các nút có callback đã đăng ký
            for btn, callback in self._cmd_handlers.items():
                curr = self.data.get(btn, 0)
                last = self._last_btn_states.get(btn, 0)
                if curr == 1 and last == 0:
                    if callback:
                        try:
                            res = callback()
                            if hasattr(res, '__await__') or hasattr(res, 'send'):
                                asyncio.create_task(res)
                        except Exception as e:
                            print(f'[GAMEPAD] Loi callback nut {btn}:', e)
                self._last_btn_states[btn] = curr

            if self._verbose:
                if ticks_ms() - self._last_print > 200:
                    print(self.data)
                    self._last_print = ticks_ms()

            await asyncio.sleep_ms(10)

    def _calculate_joystick(self, x, y):
        dir = -1
        distance = int(math.sqrt(x*x + y*y))

        if distance < 15:
            return (-1, 0)
        elif distance > 100:
            distance = 100

        angle = int(math.atan2(y, x) * 180 / math.pi)
        if angle < 0:
            angle += 360

        if angle < 23 or angle >= 338:
            dir = DIR_R
        elif angle < 68:
            dir = DIR_RF
        elif angle < 113:
            dir = DIR_FW
        elif angle < 158:
            dir = DIR_LF
        elif angle < 203:
            dir = DIR_L
        elif angle < 248:
            dir = DIR_LB
        elif angle < 293:
            dir = DIR_BW
        else:
            dir = DIR_RB

        return (dir, distance)
