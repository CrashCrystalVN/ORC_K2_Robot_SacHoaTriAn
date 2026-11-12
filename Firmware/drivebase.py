try:
    from time import ticks_ms
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
import asyncio, math
from ble import *
from utility import *
from yolo_uno import *
from setting import *
from constants import *
from motor import *
from line_sensor import *
from gamepad import *
from pid import PIDController
try:
    import config
except ImportError:
    config = None

def apply_deadband(val, threshold=12.0):
    if abs(val) <= threshold:
        return 0.0
    sign = 1.0 if val > 0 else -1.0
    return sign * (abs(val) - threshold) / (100.0 - threshold) * 100.0

def holonomic_mix(vy_raw, vx_raw, rot_raw, max_speed=95, trim=(1.0, 1.0, 1.0, 1.0), min_pwm=28, deadband=12.0):
    """
    Trộn động học Holonomic 4 bánh Mecanum:
    vy_raw: Joy 1 Dọc (-100..+100, Tiến > 0, Lùi < 0)
    vx_raw: Joy 2 Ngang (-100..+100, Ngang phải > 0, Ngang trái < 0)
    rot_raw: Joy 1 Ngang (-100..+100, Xoay phải > 0, Xoay trái < 0)
    """
    vy = apply_deadband(vy_raw, deadband)
    vx = apply_deadband(vx_raw, deadband)
    rot = apply_deadband(rot_raw, deadband)

    if abs(vy) < 0.01 and abs(vx) < 0.01 and abs(rot) < 0.01:
        return (0, 0, 0, 0)

    # 1. Ma trận động học Mecanum X-Pattern chuẩn:
    # FL = vy + vx + rot
    # FR = vy - vx - rot
    # RL = vy - vx + rot
    # RR = vy + vx - rot
    fl = vy + vx + rot
    fr = vy - vx - rot
    rl = vy - vx + rot
    rr = vy + vx - rot

    # 2. Desaturation: Chuẩn hóa tỉ lệ vector nếu max > 100
    max_mag = max(abs(fl), abs(fr), abs(rl), abs(rr))
    if max_mag > 100.0:
        scale = 100.0 / max_mag
        fl *= scale
        fr *= scale
        rl *= scale
        rr *= scale

    # 3. Scale theo max_speed teleop (mặc định 95%)
    speed_scale = max_speed / 100.0
    fl *= speed_scale
    fr *= speed_scale
    rl *= speed_scale
    rr *= speed_scale

    # 4. Áp dụng trim từng bánh (FL, FR, RL, RR)
    if trim is not None and len(trim) >= 4:
        fl *= trim[0]
        fr *= trim[1]
        rl *= trim[2]
        rr *= trim[3]

    # 5. Ngưỡng PWM tối thiểu thắng ma sát hộp số GA25 và con lăn Mecanum
    wheels = [fl, fr, rl, rr]
    res = []
    for w in wheels:
        if abs(w) > 0.5:
            sign = 1.0 if w > 0 else -1.0
            mag = abs(w)
            if mag < min_pwm:
                mag = float(min_pwm)
            mag = min(100.0, mag)
            res.append(int(round(sign * mag)))
        else:
            res.append(0)

    return tuple(res)


class DriveBase:
    def __init__(self, drive_mode, m1, m2, m3=None, m4=None):
        if drive_mode not in (MODE_2WD, MODE_4WD, MODE_MECANUM):
            raise ValueError("Invalid drive mode, should be MODE_2WD, MODE_4WD or MODE_MECANUM")
        else:
            self._drive_mode = drive_mode
        
        self.left = []
        self.right = []
        self.left_motor_ports = 0
        self.right_motor_ports = 0
        self.m1 = None # front left motor
        self.m2 = None # front right motor
        self.m3 = None # back left motor
        self.m4 = None # back right motor
        self.left_encoder = None
        self.right_encoder = None

        if m1 != None:
            self.m1 = m1 # front left motor
            self.m1.reverse()
            self.left.append(m1)
            if m1.port in (E1, E2):
                self.left_encoder = m1
        
        if m3 != None:
            self.m3 = m3 # back left motor
            self.m3.reverse()
            self.left.append(m3)
            if m3.port in (E1, E2):
                self.left_encoder = m3
        
        if m2 != None:
            self.m2 = m2 # front right motor
            self.right.append(m2)
            if m2.port in (E1, E2):
                self.right_encoder = m2
        
        if m4 != None:
            self.m4 = m4 # back right motor
            self.right.append(m4)
            if m4.port in (E1, E2):
                self.right_encoder = m4

        for m in self.left:
            self.left_motor_ports += m.port

        for m in self.right:
            self.right_motor_ports += m.port

        self._speed = 75
        self._min_speed = 40

        self._wheel_diameter = 80 # mm
        self._width = 300 # mm
        self._wheel_circ = math.pi * self._wheel_diameter # mm
        self._ticks_per_rev = 0
        self._ticks_to_m = 0

        self._line_sensor = None
        self._angle_sensor = None
        self._use_gyro = False
        self._turn_offset_left = 0
        self._turn_offset_right = 0

        # remote control
        self.mode_auto = True
        self._teleop_cmd = None
        self._last_teleop_cmd = None
        self._teleop_cmd_handlers = {}
        self.side_move_mode = JOYSTICK

        # line following sensor state detected
        self._last_line_state = LINE_CENTER

        # mecanum mode speed setting

        # Motor connection
        # \\ m1 | m2 //
        # ------| -----
        # // m3 | m4 \\

        self._mecanum_speed_factor = (
            (1, 1, 1, 1),      # forward DIR_FW 
            (1, 0, 0, 1),      # right forward DIR_RF
            (1, -1, 1, -1),    # turn right DIR_R
            (0, -1, -1, 0),    # right backward DIR_RB
            (-1, -1, -1, -1),  # backward DIR_BW
            (-1, 0, 0, -1),    # left backward DIR_LB
            (-1, 1, -1, 1),    # turn left DIR_L
            (0, 1, 1, 0),      # left forward DIR_LF
            (-1.3, 1.3, 1.3, -1.3),    # move side left DIR_SL
            (1.3, -1.3, -1.3, 1.3)     # move side right DIR_SR
        )

        # PID related settings
        self._pid = PIDController(5, 0.15, 0.1, setpoint=0, sample_time=None, output_limits=(-10, 10))

        self._speed_ratio = (1, 1)

    ######################## Configuration #####################

    '''
        Config moving speed.

        Parameters:
             speed (Number) - Default speed used to move, 0 to 100.
    '''
    def speed(self, speed=None, min_speed=None):
        if speed == None and min_speed == None:
            return self._speed
        else:
            self._speed = speed
            if min_speed != None:
                self._min_speed = min_speed
            else:
                self._min_speed = int(speed/2)
    
    def line_sensor(self, sensor):
        self._line_sensor = sensor
    
    def angle_sensor(self, sensor):
        self._angle_sensor = sensor
    
    '''
        Config robot size and moving mode.

        Parameters:
             width (Number, mm) - Width between two wheels.
             wheel (Number, mm) - Wheel diameter
    '''
    def size(self, wheel, width):
        if width < 0 or wheel < 0:
            raise Exception("Invalid robot config value")

        self._wheel_diameter = wheel
        self._width = width
        self._wheel_circ = math.pi * self._wheel_diameter

        if self.left_encoder and self.right_encoder:
            self._ticks_per_rev = int((self.left_encoder.ticks_per_rev + self.right_encoder.ticks_per_rev)/2)
            self._ticks_to_m = (self._wheel_circ / self._ticks_per_rev) / 1000
    
    '''
        Config sensor used to drive and turn precisely.

        Parameters:
             enabled (Boolean) - If True, will use gyroscope, else will use encoder
    '''
    def use_gyro(self, enabled):
        self._use_gyro = enabled

    '''
        Config turn offset to compensate for inertia.
        Parameters:
             offset (Number, degree) - Angle to compensate (or left offset).
             right_offset (Number, degree) - Angle to compensate for right turn.
    '''
    def turn_offset(self, offset=None, right_offset=None):
        if offset is None:
            return (self._turn_offset_left, self._turn_offset_right)
        self._turn_offset_left = offset
        if right_offset is not None:
            self._turn_offset_right = right_offset
        else:
            self._turn_offset_right = offset

    '''
        Config robot PID.

        Parameters:

    '''
    def pid(self, Kp, Ki, Kd):
        self._pid.tunings = (Kp, Ki, Kd)
    
    '''
        Config robot speed ration to keep it moving straight.

        Parameters:

    '''
    def speed_ratio(self, left, right):
        self._speed_ratio = (left, right)

    ######################## Driving functions #####################

    def forward(self):
        self.run(DIR_FW)

    async def forward_for(self, amount, unit=SECOND, then=STOP):
        await self.straight(self._speed, amount, unit, then)
    
    def backward(self):
        self.run(DIR_BW)

    async def backward_for(self, amount, unit=SECOND, then=STOP):
        await self.straight(-self._speed, amount, unit, then)
    
    def turn_left(self):
        self.run(DIR_L)
    
    async def turn_left_for(self, amount, unit=SECOND, then=STOP):
        await self.turn(-100, amount, unit, then)

    def turn_right(self):
        self.run(DIR_R)

    async def turn_right_for(self, amount, unit=SECOND, then=STOP):
        await self.turn(100, amount, unit, then)

    def move_left(self):
        if self._drive_mode != MODE_MECANUM:
            self.turn_left()
            return
        else:
            self.run(DIR_SL)

    async def move_left_for(self, amount, unit=SECOND, then=STOP):
        if self._drive_mode != MODE_MECANUM:
            await self.turn_left_for(amount, unit, then)
            return

        else:
            if unit != SECOND:
                return
            # only support SECOND unit
            distance = abs(abs(amount*1000)) # to ms
            driven = 0
            last_driven = 0
            time_start = ticks_ms()

            while True:
                driven = ticks_ms() - time_start                

                if driven > distance:
                    break

                # speed smoothing and go straight
                adjusted_speed = self._calc_speed(abs(self._speed), distance, driven, last_driven)
                self.run(DIR_SL, adjusted_speed)

                last_driven = driven
                await asyncio.sleep_ms(10)

            await self.stop_then(then)

    def move_right(self):
        if self._drive_mode != MODE_MECANUM:
            self.turn_right()
            return
        else:
            self.run(DIR_SR)
    
    async def move_right_for(self, amount, unit=SECOND, then=STOP):
        if self._drive_mode != MODE_MECANUM:
            await self.turn_right_for(amount, unit, then)
            return

        if unit != SECOND:
            return
        # only support SECOND unit
        distance = abs(abs(amount*1000)) # to ms
        driven = 0
        last_driven = 0
        time_start = ticks_ms()

        while True:
            driven = ticks_ms() - time_start                

            if driven > distance:
                break

            # speed smoothing and go straight
            adjusted_speed = self._calc_speed(abs(self._speed), distance, driven, last_driven)
            self.run(DIR_SR, adjusted_speed)

            last_driven = driven
            await asyncio.sleep_ms(10)

        await self.stop_then(then)

    '''
        Drives straight for a given distance and then stops.

        Parameters:
            speed (Number, %) - Speed to travel

            amount (Number, cm or inch or seconds) - Amount to travel

            then (STOP | BRAKE) - What to do after coming to a standstill.

            unit - can be CM, INCH, or SECOND
    '''
    async def straight(self, speed, amount, unit=SECOND, then=STOP):
        await self.reset_angle()
        # calculate target 
        distance = 0
        driven = 0
        last_driven = 0
        expected_speed = 0

        # apply pid
        self._pid.reset()

        if unit == CM:
            distance = abs(int(amount*10)) # to mm
        elif unit == INCH:
            distance = abs(int(amount*25.4)) # to mm
        elif unit == SECOND:
            distance = abs(abs(amount*1000)) # to ms
            time_start = ticks_ms()

        speed_dir = (1 if speed >= 0 else -1) # safe direction without zero division

        while True:
            if unit == SECOND:
                driven = ticks_ms() - time_start                
            else:
                driven = abs(self.distance())

            #print(driven, distance)
            
            if driven >= distance:
                break
            
            if (unit == SECOND and amount < 2) or (unit == CM and amount < 10) or (unit == INCH and amount < 4):
                expected_speed = speed
            else:
                # speed smoothing using accel and deccel technique when distance is long enough
                expected_speed = speed_dir*self._calc_speed(abs(speed), distance, driven, last_driven)

            # adjust left and right speed to go straight
            left_speed, right_speed = self._calib_speed(expected_speed)

            self.run_speed(left_speed, right_speed)

            last_driven = driven
            
            await asyncio.sleep_ms(5)

        await self.stop_then(then)

    '''
        Turns in place by a given angle and then stops.

        Drives an arc along a circle of a given radius, by a given angle if radius > 0.

        Parameters:
            amount (Number, deg or second) - Amount of degree or time of the turn.

            radius (Number, mm) - Radius of the arc turn.

            then - What to do after coming to a standstill.

            unit - UNIT_DEGREE or UNIT_SECOND
    '''
    async def turn(self, steering, amount=None, unit=SECOND, then=STOP):
        speed = self._speed

        if not amount:
            left_speed, right_speed = self._calc_steering(speed, steering)
            self.run_speed(left_speed, right_speed)
            return

        # calculate distance
        distance = 0
        driven_distance = 0
        last_driven = 0

        if unit == DEGREE:
            if self._use_gyro: # use angle sensor
                if self._angle_sensor == None: # no angle sensor
                    return

                distance = amount

                if abs(distance) > 359:
                    distance = 359
            else: # use encoders
                # Arc length is computed accordingly.
                # arc_length = (10 * abs(angle) * radius) / 573
                radius = 0 # Fix me
                distance = abs(( math.pi * (radius+self._width/2)*2 ) * (amount / 360 ))
                #print('arc length: ', distance)
                # reference link: https://subscription.packtpub.com/book/iot-and-hardware/9781789340747/12/ch12lvl1sec11/making-a-specific-turn
            await self.reset_angle()

        elif unit == SECOND:
            distance = abs(amount*1000) # to ms
            time_start = ticks_ms()

        #print(left_speed, right_speed)

        wheel_circ_degree = self._wheel_circ/360

        while True:
            driven_distance = 0
            if unit == SECOND:
                driven_distance = ticks_ms() - time_start
            elif unit == DEGREE:
                if self._use_gyro: # use angle sensor
                    if self._angle_sensor != None:
                        driven_distance = abs(self._angle_sensor.heading)
                    else:
                        driven_distance = 0
                else: # use encoder
                    if steering > 0:
                        driven_distance = abs(self.left_encoder.angle())*wheel_circ_degree
                    else:
                        driven_distance = abs(self.right_encoder.angle())*wheel_circ_degree

            #print(driven_distance)
            if (unit == SECOND and amount < 1) or (unit == DEGREE and amount < 45):
                expected_speed = speed
            else:
                # speed smoothing using accel and deccel technique when distance is long enough
                expected_speed = self._calc_speed(speed, distance, driven_distance, last_driven)

            left_speed, right_speed = self._calc_steering(expected_speed, steering)
            #print(expected_speed, left_speed, right_speed)

            self.run_speed(left_speed, right_speed)

            last_driven = driven_distance

            target_distance = distance
            if unit == DEGREE:
                offset = self._turn_offset_left if steering < 0 else self._turn_offset_right

                if self._use_gyro:
                    target_distance -= offset
                else:
                    # Convert offset degree to arc length mm for encoder mode
                    # Assuming radius=0 (turn in place)
                    target_distance -= (math.pi * self._width) * (offset / 360)

            if driven_distance >= target_distance:
                break

            await asyncio.sleep_ms(5)
        
        await self.stop_then(then)

    ######################## Drive forever #####################

    '''
        Starts driving to the specified direction at given speed. 

        Parameters:
            dir (Number) - One of 8 directions plus 2 sidingg for mecanum mode

            speed (Number, %) - Running speed, from 0 to 100.
            
    '''
    
    def run(self, dir, speed=None):

        # calculate direction based on angle
        #           90(DIR_FW)
        #   135(DIR_LF) |  45(DIR_RF)
        # 180(DIR_L) ---+----Angle=0(dir=DIR_R)
        #   225(DIR_LB) |  315(DIR_RB)
        #         270(DIR_BW)
        #
        # DIR_SL: move side left DIR_SR: move side right only for mecanum

        if speed == None:
            speed = self._speed
        else:
            speed = abs(max(min(100, speed), -100))

        if self._drive_mode == MODE_MECANUM:
            self.m1.run(speed*self._mecanum_speed_factor[dir][0]*self._speed_ratio[0])
            self.m2.run(speed*self._mecanum_speed_factor[dir][1]*self._speed_ratio[1])
            self.m3.run(speed*self._mecanum_speed_factor[dir][2]*self._speed_ratio[0])
            self.m4.run(speed*self._mecanum_speed_factor[dir][3]*self._speed_ratio[1])
            return
        else:
            if dir == DIR_FW:
                self.run_speed(speed, speed)

            elif dir == DIR_BW:
                self.run_speed(-speed, -speed)

            elif dir == DIR_L:
                self.run_speed(-speed, speed)

            elif dir == DIR_R:
                self.run_speed(speed, -speed)

            elif dir == DIR_RF:
                self.run_speed(speed, int(speed/2))

            elif dir == DIR_LF:
                self.run_speed(int(speed/2), speed)
            
            elif dir == DIR_RB:
                self.run_speed(-speed, int(-speed/2))

            elif dir == DIR_LB:
                self.run_speed(int(-speed/2), -speed)

            else:
                self.stop()
    
    '''
        Starts driving with the specified left and right speed. 

        Parameters:
            left_speed (Number, %) - Left motor speed, from 0 to 100.

            right_speed (Number, %) - Right motor speed, from 0 to 100.
            
    '''
    
    def run_speed(self, left_speed, right_speed=None):
        if right_speed == None:
            right_speed = left_speed

        for i in range(len(self.left)):
            self.left[i].run(int(left_speed*self._speed_ratio[0]))
            self.right[i].run(int(right_speed*self._speed_ratio[1]))

    def run_mecanum(self, v_fl, v_fr, v_rl, v_rr):
        if self.m1: self.m1.run(int(v_fl * self._speed_ratio[0]))
        if self.m2: self.m2.run(int(v_fr * self._speed_ratio[1]))
        if self.m3: self.m3.run(int(v_rl * self._speed_ratio[0]))
        if self.m4: self.m4.run(int(v_rr * self._speed_ratio[1]))


    ######################## Stop functions #####################
    
    '''
        Stops the robot by letting the motors spin freely.
    '''
    def stop(self):
        self.left[0].driver.set_motors(self.left_motor_ports+self.right_motor_ports, 0)
    
    '''
        Stops the robot by passively braking the motors.
    '''
    def brake(self):
        self.left[0].driver.brake(self.left_motor_ports+self.right_motor_ports)

    '''
        Stops the robot by given method.

        Parameters:
            then: STOP or BRAKE or None
    '''
    async def stop_then(self, then):
        if then == BRAKE:
            self.brake()
            await asyncio.sleep_ms(500)
            self.stop()
        elif then == STOP:
            self.stop()
        else:
            return

    ######################## Measuring #####################

    '''
        Gets the estimated driven distance.

        Returns:
            Driven distance since last reset (mm).
    '''
    def distance(self):
        if self.left_encoder and self.right_encoder:
            ang_l = abs(self.left_encoder.angle())
            ang_r = abs(self.right_encoder.angle())
            angle = (ang_l + ang_r) / 2.0
            dist = (angle * self._wheel_circ) / 360.0
            return dist
        elif self.left_encoder:
            return (abs(self.left_encoder.angle()) * self._wheel_circ) / 360.0
        elif self.right_encoder:
            return (abs(self.right_encoder.angle()) * self._wheel_circ) / 360.0
        else:
            return 0
    
    '''
        Gets the estimated driven angle.

        Returns:
            Driven angle since last reset (degree).
    '''
    def angle(self):
        if self._angle_sensor:
            return self._angle_sensor.heading
        else:
            return 0
    
    '''
        Resets the estimated driven distance and angle to 0.
    '''
    async def reset_angle(self):
        if self._angle_sensor:
            await self._angle_sensor.reset()

        for m in (self.left + self.right):
            m.reset_angle()

    ######################## Remote control #####################

    async def run_teleop(self, gamepad: Gamepad, accel_steps=8):
        self.mode_auto = False
        self._teleop_cmd = ''

        # Đọc cấu hình từ config.py (nếu có)
        trim = getattr(config, 'WHEEL_TRIM', (1.0, 1.0, 1.0, 1.0)) if config else (1.0, 1.0, 1.0, 1.0)
        min_pwm = getattr(config, 'MOTOR_MIN_PWM', 28) if config else 28
        deadband_val = getattr(config, 'JOYSTICK_DEADBAND', 12.0) if config else 12.0
        wheel_polarity = getattr(config, 'WHEEL_POLARITY', (1, 1, -1, -1)) if config else (1, 1, -1, -1)

        curr = [0, 0, 0, 0]  # Tốc độ PWM thực tế hiện tại [FL, FR, RL, RR]
        last_btn_states = {}
        check_buttons = [
            BTN_L1, BTN_R1, BTN_L2, BTN_R2,
            BTN_CIRCLE, BTN_CROSS, BTN_SQUARE, BTN_TRIANGLE,
            BTN_THUMBL, BTN_THUMBR, BTN_M1, BTN_M2
        ]

        while True:
            if self.mode_auto == True:  # Chế độ tự động đang chạy
                await asyncio.sleep_ms(100)
                continue

            # 1. Xử lý các nút bấm điều khiển ngoại vi (Servo / Cánh tay / Nút gắp)
            d = gamepad.data
            for btn in check_buttons:
                val = d.get(btn, 0)
                last_val = last_btn_states.get(btn, 0)
                if val == 1 and last_val == 0:  # Sườn lên (vừa nhấn)
                    if btn in self._teleop_cmd_handlers and self._teleop_cmd_handlers[btn]:
                        try:
                            await self._teleop_cmd_handlers[btn]()
                        except Exception as e:
                            print('[BTN ERROR]', btn, e)
                last_btn_states[btn] = val

            # 2. Đọc trục Joystick chuẩn hóa:
            # - J1 (Cần Trái): Dọc ALY (Tiến > 0 / Lùi < 0), Ngang ALX (Xoay Phải > 0 / Xoay Trái < 0)
            # - J2 (Cần Phải): Ngang ARX (Trượt ngang Phải > 0 / Trượt ngang Trái < 0)
            vy_in = float(d.get(ALY, 0))
            rot_in = float(d.get(ALX, 0))
            vx_in = float(d.get(ARX, 0)) if self._drive_mode == MODE_MECANUM else 0.0

            # Hỗ trợ D-Pad di chuyển nhích bước chính xác nếu không gạt Joystick
            if abs(vy_in) <= 12 and abs(rot_in) <= 12 and abs(vx_in) <= 12:
                if d.get(BTN_UP, 0):
                    vy_in = 65.0
                elif d.get(BTN_DOWN, 0):
                    vy_in = -65.0
                if d.get(BTN_RIGHT, 0):
                    if self._drive_mode == MODE_MECANUM:
                        vx_in = 65.0
                    else:
                        rot_in = 65.0
                elif d.get(BTN_LEFT, 0):
                    if self._drive_mode == MODE_MECANUM:
                        vx_in = -65.0
                    else:
                        rot_in = -65.0

            # 3. Trộn Holonomic liên tục với chuẩn hóa Desaturation, Trim và bù ma sát Min PWM
            target = holonomic_mix(
                vy_in, vx_in, rot_in,
                max_speed=self._speed,
                trim=trim,
                min_pwm=min_pwm,
                deadband=deadband_val
            )

            # 4. Khi thả hết cần: Dừng khẩn cấp cả 4 bánh ngay lập tức (Brake)
            if target == (0, 0, 0, 0):
                if curr != [0, 0, 0, 0]:
                    self.brake()
                    curr = [0, 0, 0, 0]
                await asyncio.sleep_ms(15)
                continue

            # 5. Xử lý đảo chiều đột ngột (Zero-crossing) chống quay vòng xe:
            # Nếu bất kỳ bánh nào đảo ngược chiều chạy đáng kể (curr * target < -100, ví dụ SL -> SR):
            # Lập tức phanh cả 4 bánh về 0 và dừng 70ms để triệt tiêu toàn bộ quán tính
            if any(c * t < -100 for c, t in zip(curr, target)):
                self.brake()
                curr = [0, 0, 0, 0]
                await asyncio.sleep_ms(70)

            # 6. Slew-rate đồng bộ: Cả 4 bánh tiến về target theo cùng một tỉ lệ (Preserve Vector)
            deltas = [target[i] - curr[i] for i in range(4)]
            max_delta = max(abs(d) for d in deltas)
            step = accel_steps if accel_steps > 0 else 10

            if max_delta <= step:
                curr = list(target)
            else:
                ratio = step / max_delta
                for i in range(4):
                    curr[i] = int(round(curr[i] + deltas[i] * ratio))

            # 7. Ghi lệnh PWM mở trực tiếp cho cả 4 bánh đồng thời (áp dụng WHEEL_POLARITY)
            if self._drive_mode == MODE_MECANUM:
                self.run_mecanum(
                    int(curr[0] * wheel_polarity[0]),
                    int(curr[1] * wheel_polarity[1]),
                    int(curr[2] * wheel_polarity[2]),
                    int(curr[3] * wheel_polarity[3])
                )
            else:
                self.run_speed(curr[0], curr[1])

            await asyncio.sleep_ms(15)
    
    def on_teleop_command(self, cmd, callback):
        self._teleop_cmd_handlers[cmd] = callback


    ######################## Utility functions #####################

    '''
        Used to calculate all the speeds in our programs. Brakes and accelerates

        Parameters:
            speed: The current speed the robot has
            start_speed: Speed the robot starts at. Type: Integer. Default: No default value.
            max_speed: The maximum speed the robot reaches. Type: Integer. Default: No default value.
            end_speed: Speed the robot aims for while braking, minimum speed at the end of the program. Type: Integer. Default: No default value.
            add_speed: Percentage of the distance after which the robot reaches the maximum speed. Type: Integer. Default: No default value.
            brakeStartValue: Percentage of the driven distance after which the robot starts braking. Type: Integer. Default: No default value.
            drivenDistance: Calculation of the driven distance in degrees. Type: Integer. Default: No default value.
    '''
    def _calc_speed(self, speed, distance, driven_distance, last_driven):
        start_speed = self._min_speed

        max_speed = speed
        end_speed = start_speed
        accel_distance = 0.3*distance
        decel_distance = 0.7*distance

        if driven_distance == 0:
            return start_speed
        elif abs(driven_distance) < abs(accel_distance):
            return int(start_speed + (max_speed - start_speed) * driven_distance / accel_distance)
        elif abs(driven_distance) > abs(decel_distance):
            return int(max_speed - (max_speed - end_speed) * (driven_distance-decel_distance) / (distance-decel_distance))
        else:
            return speed
    
    def _calib_speed(self, speed):
        if self._use_gyro:
            if self._angle_sensor is not None:
                if callable(getattr(self._angle_sensor, 'heading', None)):
                    angle_error = self._angle_sensor.heading()
                else:
                    angle_error = getattr(self._angle_sensor, 'heading', 0)
            else:
                return (speed, speed)
        else:
            left_ticks = 0
            right_ticks = 0
            if self.left_encoder:
                left_ticks = abs(self.left_encoder.encoder_ticks())
            if self.right_encoder:
                right_ticks = abs(self.right_encoder.encoder_ticks())

            if speed > 0:
                angle_error = abs(left_ticks) - abs(right_ticks)
            else:
                angle_error = abs(right_ticks) - abs(left_ticks)

        correction = self._pid(angle_error)
        # Bao ve khong bao gio triet tieu qua 35% cong suat motor khi chay thang
        max_c = max(4, abs(speed) * 0.35)
        correction = max(-max_c, min(max_c, correction))

        left = speed + correction
        right = speed - correction
        return (left, right)

    
    def _calc_steering(self, speed, steering):
        left_speed = 0
        right_speed = 0
        
        if steering > 0:
            left_speed = speed
            right_speed = int(-2*(speed/100)*steering + speed)
        elif steering < 0:
            right_speed = speed
            left_speed = int(-2*(speed/100)*abs(steering) + speed)
        else:
            left_speed = right_speed = speed
        
        return (left_speed, right_speed)
    
    ######################## Line following #####################

    async def follow_line(self, backward=True, line_state=None):
        if self._line_sensor == None:
            return
        
        self.speed_factors = [ 25, 50, 100 ] # 1: light turn, 2: normal turn, 3: heavy turn
        steering = 0

        if line_state == None:
            line_state = self._line_sensor.check()

        if line_state == LINE_END: #no line found
            if backward:
                self.run(DIR_BACKWARD, self._min_speed) # slow down
        else:
            if line_state == LINE_CENTER:
                if self._last_line_state == LINE_CENTER:
                    self.forward() #if it is running straight before then robot should speed up now
                else:
                    self.run(DIR_FORWARD, self._min_speed) #just turn before, shouldn't set high speed immediately, speed up slowly

            elif line_state == LINE_CROSS:
                self.run(DIR_FORWARD, self._min_speed) # cross line found, slow down

            else:
                if line_state == LINE_RIGHT:
                    self.run_speed(self._min_speed, int(self._min_speed*1.25)) # left light turn
                elif line_state == LINE_RIGHT2:
                    self.run_speed(0, self._min_speed) # left normal turn
                elif line_state == LINE_RIGHT3:
                    while line_state != LINE_CENTER and line_state != LINE_LEFT:
                        self.run_speed(-self._min_speed, self._min_speed) # left heavy turn
                        line_state = self._line_sensor.check()
                    self._last_line_state = line_state
                    
                    return
                
                elif line_state == LINE_LEFT:
                    self.run_speed(int(self._min_speed*1.25), self._min_speed) # right light turn
                elif line_state == LINE_LEFT2:
                    self.run_speed(self._min_speed, 0) #right normal turn
                elif line_state == LINE_LEFT3:
                    while line_state != LINE_CENTER and line_state != LINE_RIGHT:
                        self.run_speed(self._min_speed, -self._min_speed) # right heavy turn
                        line_state = self._line_sensor.check()

                    self._last_line_state = line_state
                    return
        
        self._last_line_state = line_state

    async def follow_line_until_end(self, then=STOP):
        count = 2

        while True:
            line_state = self._line_sensor.check()

            if line_state == LINE_END:
                count = count - 1
                if count == 0:
                    break

            await self.follow_line(False, line_state)

            await asleep_ms(10)

        await self.stop_then(then)

    async def follow_line_until_cross(self, then=STOP):
        status = 1
        count = 0

        while True:
            line_state = self._line_sensor.check()

            if status == 1:
                if line_state != LINE_CROSS:
                    status = 2
            elif status == 2:
                if line_state == LINE_CROSS:
                    count = count + 1
                    if count == 2:
                        break

            await self.follow_line(True, line_state)

            if status == 2 and count == 1:
                await asleep_ms(20)
            else:
                await asleep_ms(10)

        #await self.forward_for(0.1, unit=SECOND) # to pass cross line a bit
        await self.stop_then(then)

    async def follow_line_by_time(self, timerun, then=STOP):
        start_time = time.ticks_ms()
        duration = timerun * 1000 # convert to ms

        while time.ticks_ms() - start_time < duration:
            await self.follow_line(True)
            await asleep_ms(10)

        await self.stop_then(then)
    
    async def follow_line_until(self, condition, then=STOP):
        status = 1
        count = 0

        while True:
            line_state = self._line_sensor.check()

            if status == 1:
                if line_state != LINE_CROSS:
                    status = 2
            elif status == 2:
                if condition():
                    count = count + 1
                    if count == 2:
                        break

            await self.follow_line(True, line_state)

            await asleep_ms(10)

        await self.stop_then(then)

    async def turn_until_line_detected(self, steering, then=STOP):
        counter = 0
        status = 0

        await self.turn(steering)

        while True:
            line_state = self._line_sensor.check()

            if status == 0:
                if line_state == LINE_END: # no black line detected
                    # ignore case when robot is still on black line since started turning
                    status = 1
            
            elif status == 1:
                if line_state != LINE_END:
                    self.turn(int(steering*0.75))
                    counter = counter - 1
                    if counter <= 0:
                        break

            await asleep_ms(10)

        await self.stop_then(then)

    async def turn_until_condition(self, steering, condition, then=STOP):
        count = 0

        await self.turn(steering)

        while True:
            if condition():
                count = count + 1
                if count == 3:
                    break
            await asleep_ms(10)

        await self.stop_then(then)
