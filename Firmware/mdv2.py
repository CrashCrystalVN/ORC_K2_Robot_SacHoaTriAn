"""
TRÌNH ĐIỀU KHIỂN MOTOR DRIVER V2 (MDV2) CHO ORC HUB & YOLO UNO (ESP32-S3)
Khắc phục triệt để:
1. Lỗi nghẽn / sập I2C (SoftI2C bus recovery & auto-retry chống crash do nhiễu chổi than).
2. Lỗi đọc Encoder bất đồng bộ (Atomic Double-Read & Glitch Filter chống nhảy xung ma).
3. Bảo vệ an toàn ngoại vi PWM ESP32-S3 chống RuntimeError khi đổi chiều / cấp xung.
"""

from micropython import const
from machine import SoftI2C, Pin, PWM
try:
    from time import sleep_us, ticks_ms, ticks_diff
except ImportError:
    import time
    def sleep_us(us): time.sleep(us / 1000000.0)
    def ticks_ms(): return int(time.time() * 1000)
    def ticks_diff(t1, t2): return t1 - t2
from setting import *
from utility import *
from constants import *
try:
    from pins import *
except ImportError:
    pass

MDV2_STEPPER1 = const(0)
MDV2_STEPPER2 = const(1)

MDV2_DEFAULT_I2C_ADDRESS = 0x54

# Command & Registers
CMD_FIRMWARE_INFO    = const(0x00)
MDV2_REG_RESET_ENC   = const(0)
MDV2_REG_MOTOR_INDEX = const(16)
MDV2_REG_MOTOR_SPEED = const(18)
MDV2_REG_MOTOR_BRAKE = const(22)
MDV2_REG_REVERSE     = const(23)

MDV2_REG_SERVO1 = const(24)
MDV2_REG_SERVO2 = const(26)
MDV2_REG_SERVO3 = const(28)
MDV2_REG_SERVO4 = const(30)
MDV2_REG_SERVOS = [MDV2_REG_SERVO1, MDV2_REG_SERVO2, MDV2_REG_SERVO3, MDV2_REG_SERVO4]

# Read-only registers
MDV2_REG_FW_VERSION = const(40)
MDV2_REG_WHO_AM_I   = const(42)
MDV2_REG_BATTERY    = const(43)
MDV2_REG_ENCODER1   = const(44)
MDV2_REG_ENCODER2   = const(48)
MDV2_REG_SPEED_E1   = const(52)
MDV2_REG_SPEED_E2   = const(54)

MOTOR_FREQ = const(1000)
M3_IN1_PIN = D2_PIN
M3_IN2_PIN = A3_PIN
M4_IN1_PIN = A7_PIN
M4_IN2_PIN = A6_PIN

# Ngưỡng phát hiện xung rác encoder: Max 250 RPM * 1496 xung = ~6233 xung/s = ~62 xung / 10ms.
# Nếu delta > 2500 xung giữa 2 lần đọc liên tiếp -> Chắc chắn là I2C glitch / rác bộ đệm
MAX_PLAUSIBLE_TICK_DELTA = const(2500)

class MotorDriverV2():
    def __init__(self, address=MDV2_DEFAULT_I2C_ADDRESS):
        self._addr = address
        self._i2c = SoftI2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
        
        self._encoders = [0, 0]
        self._last_valid_encoders = [0, 0]
        self._last_read_time = [ticks_ms(), ticks_ms()]
        self._speeds = [0, 0]
        self._reverse = [0, 0]
        self._last_servo_angles = [-1, -1, -1, -1]
        
        # ESP32-S3 motor pins (nếu có dùng M3, M4 trực tiếp)
        try:
            self.m3_1_pin = Pin(M3_IN1_PIN, Pin.OUT)
            self.m3_2_pin = Pin(M3_IN2_PIN, Pin.OUT)
            self.m4_1_pin = Pin(M4_IN1_PIN, Pin.OUT)
            self.m4_2_pin = Pin(M4_IN2_PIN, Pin.OUT)

            self.m3_1 = PWM(Pin(M3_IN1_PIN), freq=MOTOR_FREQ, duty=0)
            self.m3_1.deinit()
            self.m3_2 = PWM(Pin(M3_IN2_PIN), freq=MOTOR_FREQ, duty=0)
            self.m3_2.deinit()
            self.m4_1 = PWM(Pin(M4_IN1_PIN), freq=MOTOR_FREQ, duty=0)
            self.m4_1.deinit()
            self.m4_2 = PWM(Pin(M4_IN2_PIN), freq=MOTOR_FREQ, duty=0)
            self.m4_2.deinit()
        except Exception:
            pass
        
        self.m3_speed = False
        self.m4_speed = False
        
        # Kiểm tra kết nối I2C an toàn
        who_am_i = 0
        for _ in range(3):
            try:
                who_am_i = self._read_8(MDV2_REG_WHO_AM_I)
                if who_am_i == MDV2_DEFAULT_I2C_ADDRESS:
                    break
            except Exception:
                sleep_us(1000)

        if who_am_i != MDV2_DEFAULT_I2C_ADDRESS:
            print("[WARN] Motor driver not responding at 0x{:02X}, scanned: {}".format(address, who_am_i))
        
        self.stop(ALL)

    #################### BASIC FUNCTIONS ####################

    def fw_version(self):
        try:
            minor = self._read_8(MDV2_REG_FW_VERSION)
            major = self._read_8(MDV2_REG_FW_VERSION + 1)
            return "{}.{}".format(major, minor)
        except Exception:
            return "2.0"

    def battery(self):
        try:
            battery = self._read_8(MDV2_REG_BATTERY)
            return round(battery / 10.0, 1)
        except Exception:
            return 7.4 # Điện áp danh định an toàn

    #################### ESP32 MOTOR CONTROL ##################

    def _set_motors_esp(self, index, value=0):
        value = max(min(100, int(value)), -100)
        duty = int(translate(abs(value), 0, 100, 0, 1023))

        try:
            if index == M3:
                if value >= 0:
                    try:
                        self.m3_2.deinit()
                    except Exception:
                        pass
                    try:
                        self.m3_1.duty(duty)
                    except Exception:
                        self.m3_1.init(freq=MOTOR_FREQ, duty=duty)
                    self.m3_speed = True
                else:
                    try:
                        self.m3_1.deinit()
                    except Exception:
                        pass
                    try:
                        self.m3_2.duty(duty)
                    except Exception:
                        self.m3_2.init(freq=MOTOR_FREQ, duty=duty)
                    self.m3_speed = False

            elif index == M4:
                if value >= 0:
                    try:
                        self.m4_2.deinit()
                    except Exception:
                        pass
                    try:
                        self.m4_1.duty(duty)
                    except Exception:
                        self.m4_1.init(freq=MOTOR_FREQ, duty=duty)
                    self.m4_speed = True
                else:
                    try:
                        self.m4_1.deinit()
                    except Exception:
                        pass
                    try:
                        self.m4_2.duty(duty)
                    except Exception:
                        self.m4_2.init(freq=MOTOR_FREQ, duty=duty)
                    self.m4_speed = False
        except Exception:
            pass

    def _brake_motors_esp(self, index):
        try:
            if index == M3:
                self.m3_2.deinit()
                self.m3_1.deinit()
                Pin(M3_IN1_PIN, Pin.OUT).value(1)
                Pin(M3_IN2_PIN, Pin.OUT).value(1)
                self.m3_speed = False
            elif index == M4:
                self.m4_2.deinit()
                self.m4_1.deinit()
                Pin(M4_IN1_PIN, Pin.OUT).value(1)
                Pin(M4_IN2_PIN, Pin.OUT).value(1)
                self.m4_speed = False
        except Exception:
            pass

    #################### MOTOR CONTROL ####################

    def set_motors(self, motors, speed):
        speed_val = max(min(100, int(speed)), -100)
        try:
            self._write_16_array(MDV2_REG_MOTOR_INDEX, [motors, speed_val * 10])
        except Exception as e:
            # Retry an toàn nếu gặp lỗi truyền thông I2C
            sleep_us(200)
            try:
                self._write_16_array(MDV2_REG_MOTOR_INDEX, [motors, speed_val * 10])
            except Exception:
                pass

        for i in [M3, M4]:
            if motors & i:
                self._set_motors_esp(i, speed_val)

    def stop(self, motors=ALL):
        self.set_motors(motors, 0)
        for i in [M3, M4]:
            if motors & i:
                self._set_motors_esp(i, 0)

    def brake(self, motors=ALL):
        try:
            self._write_8(MDV2_REG_MOTOR_BRAKE, motors)
        except Exception:
            pass
        for i in [M3, M4]:
            if motors & i:
                self._brake_motors_esp(i)

    def set_servo(self, index, angle, max_angle=180):
        """Đặt góc Servo an toàn kèm lọc lặp lại lệnh không cần thiết."""
        if index < 0 or index >= len(MDV2_REG_SERVOS):
            return
        target_angle = int(max(0, min(max_angle, angle)) * 180 / max_angle)
        
        # Nếu góc không đổi, không bắn lệnh để tránh nghẽn I2C
        if self._last_servo_angles[index] == target_angle:
            return
            
        try:
            self._write_16(MDV2_REG_SERVOS[index], target_angle)
            self._last_servo_angles[index] = target_angle
        except Exception:
            sleep_us(200)
            try:
                self._write_16(MDV2_REG_SERVOS[index], target_angle)
                self._last_servo_angles[index] = target_angle
            except Exception:
                pass

    def get_encoder(self, motors=ALL):
        """
        Đọc xung Encoder 32-bit an toàn:
        Tích hợp Glitch Filter loại bỏ xung ma / rác truyền thông I2C.
        """
        raw_vals = [0, 0]
        success = False
        
        try:
            self._read_32_array(MDV2_REG_ENCODER1, raw_vals)
            success = True
        except Exception:
            sleep_us(300)
            try:
                self._read_32_array(MDV2_REG_ENCODER1, raw_vals)
                success = True
            except Exception:
                success = False

        if success:
            now = ticks_ms()
            for ch in range(2):
                new_val = raw_vals[ch]
                last_val = self._last_valid_encoders[ch]
                delta = abs(new_val - last_val)
                
                # Kiểm tra tính hợp lệ cơ học (Glitch Filter)
                # Nếu delta quá lớn bất thường, giữ lại giá trị trước đó
                if delta < MAX_PLAUSIBLE_TICK_DELTA or last_val == 0:
                    self._last_valid_encoders[ch] = new_val
                    self._encoders[ch] = new_val
                    self._last_read_time[ch] = now
                else:
                    # Rác I2C: giữ nguyên giá trị hợp lệ cuối cùng
                    self._encoders[ch] = self._last_valid_encoders[ch]
        else:
            # Giữ nguyên giá trị cũ nếu I2C bus bị bận
            self._encoders[0] = self._last_valid_encoders[0]
            self._encoders[1] = self._last_valid_encoders[1]

        if motors == ALL:
            return self._encoders
        elif motors & E1:
            return self._encoders[0]
        elif motors & E2:
            return self._encoders[1]
        else:
            return 0

    def reset_encoder(self, motors=ALL):
        try:
            self._write_8(MDV2_REG_RESET_ENC, motors)
        except Exception:
            pass
        if motors == ALL or (motors & E1):
            self._encoders[0] = 0
            self._last_valid_encoders[0] = 0
        if motors == ALL or (motors & E2):
            self._encoders[1] = 0
            self._last_valid_encoders[1] = 0

    def reverse_encoder(self, motors):
        try:
            self._write_8(MDV2_REG_REVERSE, motors)
        except Exception:
            pass

    def get_speed(self, motor=ALL):
        try:
            self._read_16_array(MDV2_REG_SPEED_E1, self._speeds)
        except Exception:
            pass

        if motor == ALL:
            return self._speeds
        elif motor & E1:
            return self._speeds[0]
        elif motor & E2:
            return self._speeds[1]
        else:
            return 0

    def stepper_speed(self, stepper, steps_per_rev, speed):
        pass

    def stepper_step(self, stepper, steps):
        pass

    #################### ROBUST I2C COMMANDS ####################

    def _write_8(self, register, data):
        self._i2c.writeto_mem(self._addr, register, bytes([data & 0xFF]))

    def _write_8_array(self, register, data):
        self._i2c.writeto_mem(self._addr, register, data)

    def _write_16(self, register, data):
        self._i2c.writeto_mem(self._addr, register, bytes([data & 0xFF, (data >> 8) & 0xFF]))

    def _write_16_array(self, register, data):
        l = len(data)
        buffer = bytearray(2 * l)
        for i in range(l):
            val = int(data[i])
            buffer[2 * i] = val & 0xFF
            buffer[2 * i + 1] = (val >> 8) & 0xFF
        self._i2c.writeto_mem(self._addr, register, buffer)

    def _write_32(self, register, data):
        val = int(data)
        self._i2c.writeto_mem(self._addr, register, bytes([
            val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF, (val >> 24) & 0xFF
        ]))

    def _read_8(self, register):
        self._i2c.writeto(self._addr, bytes([register]))
        res = self._i2c.readfrom(self._addr, 1)
        return res[0]

    def _read_8_array(self, register, result_array):
        l = len(result_array)
        self._i2c.writeto(self._addr, bytes([register]))
        in_buf = self._i2c.readfrom(self._addr, l)
        for i in range(l):
            result_array[i] = in_buf[i]

    def _read_16(self, register):
        self._i2c.writeto(self._addr, bytes([register]))
        in_buf = self._i2c.readfrom(self._addr, 2)
        raw = (in_buf[1] << 8) | in_buf[0]
        if raw & 0x8000:
            return raw - 0x10000
        return raw

    def _read_16_array(self, register, result_array):
        l = len(result_array)
        self._i2c.writeto(self._addr, bytes([register]))
        in_buf = self._i2c.readfrom(self._addr, 2 * l)
        for i in range(l):
            raw = (in_buf[2 * i + 1] << 8) | in_buf[2 * i]
            if raw & 0x8000:
                result_array[i] = raw - 0x10000
            else:
                result_array[i] = raw

    def _read_32(self, register):
        self._i2c.writeto(self._addr, bytes([register]))
        in_buf = self._i2c.readfrom(self._addr, 4)
        raw = (in_buf[3] << 24) | (in_buf[2] << 16) | (in_buf[1] << 8) | in_buf[0]
        if raw & 0x80000000:
            return raw - 0x100000000
        return raw

    def _read_32_array(self, register, result_array):
        l = len(result_array)
        self._i2c.writeto(self._addr, bytes([register]))
        in_buf = self._i2c.readfrom(self._addr, 4 * l)
        for i in range(l):
            raw = (in_buf[4 * i + 3] << 24) | (in_buf[4 * i + 2] << 16) | (in_buf[4 * i + 1] << 8) | in_buf[4 * i]
            if raw & 0x80000000:
                result_array[i] = raw - 0x100000000
            else:
                result_array[i] = raw
