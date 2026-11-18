try:
    from time import ticks_ms, ticks_us, ticks_diff
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
    def ticks_us(): return int(time.time() * 1000000)
    def ticks_diff(end, start): return end - start
import asyncio, math
try:
    asleep_ms = asyncio.sleep_ms
except AttributeError:
    async def asleep_ms(ms):
        await asyncio.sleep(ms / 1000.0)
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

        # Cấu hình & Trạng thái thuật toán dò line nâng cao (Yolo:UNO Robotics)
        self._line_cruise = None
        self._line_slow = None
        self._line_kp = 1.0
        self._line_ki = 0.0
        self._line_kd = 0.03
        self._line_d_alpha = 0.5            # Low-pass filter coefficient cho khâu vi sai D
        self._line_slowdown = 1.2           # Dynamic curve slowdown: giảm tốc khi |position| = 1/1.2
        self._line_sensor_offset = 0        # mm từ tâm sensor tới trục bánh
        self._line_turn_offset_ms = 0       # ms bù trễ quay line
        self._line_lost_timeout = 3000      # ms tối đa tìm line trước khi dừng hẳn
        self._line_gap_ms = 250             # ms duy trì chạy thẳng qua đứt đoạn
        self._line_end_ms = 100             # ms mất line ở mắt giữa để xác định kết thúc line
        self._line_confirm = 2              # Số khung hình liên tiếp để xác nhận vạch ngang
        self._line_invert = 1
        self._line_debug = False
        self._line_debug_interval = 100
        self._line_debug_ts = 0
        self._line_edge = 1.4               # Tọa độ khi chỉ mắt ngoài cùng nhìn thấy line
        self._line_corner_ms = 350          # Cửa sổ thời gian ghi nhận đỉnh cua (Corner Apex)
        self._line_outer_cap = None         # Giới hạn PWM bánh ngoài khi cua (None: 100%)
        self._line_search_speed = None
        self._line_min_wheel = 0            # Ngưỡng PWM tối thiểu tránh kéo lết bánh trong
        self._line_max_turn = 135           # Góc quay tối đa khi quét tìm line (tránh quay ngược 180)
        self._line_mark = None
        self._distance_tolerance = 5
        self._line_reset()

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
        # Desaturation Scaling: Chuẩn hóa tỉ lệ vector nếu max > 100 để bảo toàn hướng di chuyển
        max_mag = max(abs(v_fl), abs(v_fr), abs(v_rl), abs(v_rr))
        if max_mag > 100.0:
            scale = 100.0 / max_mag
            v_fl *= scale
            v_fr *= scale
            v_rl *= scale
            v_rr *= scale
        if self.m1: self.m1.run(int(v_fl * self._speed_ratio[0]))
        if self.m2: self.m2.run(int(v_fr * self._speed_ratio[1]))
        if self.m3: self.m3.run(int(v_rl * self._speed_ratio[0]))
        if self.m4: self.m4.run(int(v_rr * self._speed_ratio[1]))

    def _run_mecanum(self, forward, side, rotate):
        """
        Trộn động học và phát lệnh 4 bánh Mecanum tích hợp Desaturation Scaling:
        forward, side, rotate: từ -100 đến +100
        """
        m1 = forward + side + rotate
        m2 = forward - side - rotate
        m3 = forward - side + rotate
        m4 = forward + side - rotate

        biggest = max(abs(m1), abs(m2), abs(m3), abs(m4), 100.0)
        scale = 100.0 / biggest

        self.run_mecanum(m1 * scale, m2 * scale, m3 * scale, m4 * scale)

    def holonomic_drive(self, vy, vx, rot=0):
        """
        Dieu khien Mecanum 4 banh chu dong khong rung lac:
        - vy: Van toc tien/lui (-100..100)
        - vx: Van toc dat ngang (-100..100, phai > 0, trai < 0)
        - rot: Van toc quay goc (-100..100, phai > 0, trai < 0)
        Tu dong ngat dong co va reset PID khi dung yen de chong rung giat.
        """
        if abs(vy) < 2 and abs(vx) < 2 and abs(rot) < 2:
            self.brake()
            self.stop()
            self._pid.reset()
            return

        fl = vy + vx + rot
        fr = vy - vx - rot
        rl = vy - vx + rot
        rr = vy + vx - rot

        max_mag = max(abs(fl), abs(fr), abs(rl), abs(rr))
        if max_mag > 100.0:
            scale = 100.0 / max_mag
            fl *= scale
            fr *= scale
            rl *= scale
            rr *= scale

        min_pwm = getattr(config, 'MOTOR_MIN_PWM', 28) if config else 28
        polarity = getattr(config, 'WHEEL_POLARITY', (1, 1, -1, -1)) if config else (1, 1, -1, -1)

        wheels = [fl, fr, rl, rr]
        res = []
        for w in wheels:
            if abs(w) > 1.0:
                sign = 1.0 if w > 0 else -1.0
                mag = max(float(min_pwm), abs(w))
                res.append(int(round(sign * min(100.0, mag))))
            else:
                res.append(0)

        self.run_mecanum(
            res[0] * polarity[0],
            res[1] * polarity[1],
            res[2] * polarity[2],
            res[3] * polarity[3]
        )


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
            await asyncio.sleep_ms(150)
            self.stop()
        elif then == STOP:
            self.brake()
            await asyncio.sleep_ms(50)
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
        if 'BTN_OPTIONS' in globals() and BTN_OPTIONS not in check_buttons:
            check_buttons.append(BTN_OPTIONS)

        while True:
            # 1. Xử lý các nút bấm điều khiển (kể cả nút OPTIONS chuyển chế độ)
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

            if self.mode_auto == True:  # Chế độ tự động đang chạy, bỏ qua điều khiển Joystick
                await asyncio.sleep_ms(50)
                continue

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
        if abs(speed) < 2:
            self._pid.reset()
            return (0, 0)
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

    ######################## Configuration #####################

    '''
        Config line following speeds.

        Parameters:
             speed (Number, %) - cruise speed on straight line. Default: robot speed
             min_speed (Number, %) - speed in the tightest curves and when
                 searching for a lost line. Default: robot min_speed
    '''
    def line_speed(self, speed=None, min_speed=None, max_speed=None):
        if max_speed is not None: # develop-branch name for the cruise speed
            speed = max_speed
        if speed is not None:
            self._line_cruise = abs(speed)
        if min_speed is not None:
            self._line_slow = abs(min_speed)

    def _line_speeds(self):
        cruise = self._speed if self._line_cruise is None else self._line_cruise
        slow = self._min_speed if self._line_slow is None else self._line_slow
        return cruise, min(slow, cruise)

    '''
        Speed of the turn on the spot that looks for a lost line. Default:
        min_speed. A robot whose motors need more than min_speed to start
        turning from standstill searches far too slowly, or not at all, in
        the direction its weaker motor turns backwards: give it a speed
        above that.
    '''
    def line_search_speed(self, speed):
        self._line_search_speed = abs(speed) if speed else None

    '''
        For plain DC motors (no speed control) on fast gears.

        Parameters:
             min_duty (Number, %) - duty a wheel needs to start turning. A
                 smaller command is raised to it, and an inner wheel meant to
                 (nearly) stop turns gently backwards instead, so both wheels
                 pull and the robot turns about its middle. 0: off (default)
             max_outer (Number, %) - limit of the outer wheel in curves.
                 Default 100. At the cruise speed the robot then turns by
                 slowing its inner wheel rather than speeding up the outer
                 one, which on fast motors carries it off the line at sharp
                 corners
    '''
    def line_wheels(self, min_duty=None, max_outer=None):
        if min_duty is not None:
            self._line_min_wheel = max(0, min_duty)
        if max_outer is not None:
            self._line_outer_cap = max(1, max_outer)

    '''
        Config the line following controller. Position is -1..1, steer is
        -1..1 (1 = inner wheel stopped at cruise speed).

        Parameters:
             Kp (Number) - steer per unit of position. 1.0: line under the
                 outer eye gives full steering
             Ki (Number) - steer per unit of position*second. Usually 0
             Kd (Number) - steer per unit of position/second. Damps the
                 swing back onto the line; 0.02..0.06 is typical
    '''
    def line_pid(self, Kp=None, Ki=None, Kd=None):
        if Kp is not None:
            self._line_kp = Kp
        if Ki is not None:
            self._line_ki = Ki
        if Kd is not None:
            self._line_kd = Kd

    '''
        How much to slow down in curves: 0 = never slow down, 1 = curve
        speed when the line is under the outer eye, 2 = already at
        half way. Default 1.2.
    '''
    def line_slowdown(self, amount):
        self._line_slowdown = max(0, amount)

    '''
        'digital' or 'analog' (5-channel array only, see line_sensor.py).
    '''
    def line_mode(self, mode):
        s = self._line_sensor
        if mode in ('analog', 'raw'):
            if hasattr(s, 'mode'):
                s.mode('analog')
            else:
                print('line_mode: this sensor has no analog reading, using digital')
        elif hasattr(s, 'mode'):
            s.mode('digital')

    '''
        Distance from the sensor to the wheel axle (mm). When set,
        turn_until_line_detected() first drives forward so that the axle -
        the centre of the turn - ends up where the sensor saw the last
        crossing, and the robot turns on the junction itself.

        Needs encoder motors (ports E1/E2, or any port of Motor Driver V3): without them the library has no
        way to measure a distance, and this setting does nothing. Use
        line_turn_offset() with a time instead - it is what the robot falls
        back to here.
    '''
    def line_sensor_offset(self, mm):
        self._line_sensor_offset = max(0, mm)

    '''
        Same as line_sensor_offset() but as a time (seconds), for robots
        without encoders: at a crossing the robot keeps following the line
        for this long, held at the curve speed, before it turns. 0 disables
        it. With the sensor 10 cm ahead of the axle, 0.4 to 0.6 s is a
        sensible starting point at the usual curve speeds.

        Used whenever the encoder path above is not available, so a robot
        without encoders only needs this one.
    '''
    def line_turn_offset(self, seconds):
        self._line_turn_offset_ms = max(0, int(seconds * 1000))

    '''
        How long (ms) to search for a lost line before giving up, and how
        long (ms) to coast straight when the line vanishes from under the
        middle of the sensor before treating it as a corner and searching
        (dashed lines need a longer gap).
    '''
    def line_lost_timeout(self, ms, gap_ms=None):
        self._line_lost_timeout = max(100, int(ms))
        if gap_ms is not None:
            self._line_gap_ms = max(0, int(gap_ms))

    '''
        Prints one CSV line per interval while following:
        t_ms, pattern, position, steer, speed, left, right
    '''
    def line_debug(self, on, interval_ms=None):
        self._line_debug = bool(on)
        if interval_ms is not None:
            self._line_debug_interval = int(interval_ms)
        if self._line_debug:
            print('LINE,t_ms,pattern,pos,steer,speed,left,right')

    def line_invert(self, invert):
        # -1 if the robot steers away from the line: sensor mounted backwards
        self._line_invert = -1 if (invert is False or invert < 0) else 1

    '''
        Learns the analog calibration of the 5-channel array by spinning in
        place, half the time each way, so every eye sees the line and the
        background. Saved to flash. Start with the line under the sensor.
    '''
    async def line_calibrate(self, seconds=2):
        s = self._line_sensor
        if not hasattr(s, 'reset_calibration'):
            print('line_calibrate: only the 5-channel array has an analog calibration')
            return False
        s.mode('analog')
        s.reset_calibration()
        cruise, slow = self._line_speeds()
        duration = int(seconds * 1000)
        start = ticks_ms()
        flipped = False
        self.run_speed(slow, -slow)
        while ticks_diff(ticks_ms(), start) < duration:
            if not flipped and ticks_diff(ticks_ms(), start) > duration // 2:
                self.run_speed(-slow, slow)
                flipped = True
            s.update()
            await asyncio.sleep_ms(5)
        self.stop()
        if s.calibrated():
            s.save_calibration()
            print('line calibration ok: min=%s max=%s black_high=%s' % (s._cal_min, s._cal_max, s._line_high))
            return True
        print('line calibration poor: the sensor did not see enough black/white contrast')
        return False

    # develop-branch tuning names that no longer have an effect
    def line_curve_gain(self, gain):
        self.line_slowdown(gain * 2)

    def line_deadband(self, db):
        pass

    def line_turn_gain(self, gain, correction_limit=1.0):
        pass

    def line_d_alpha(self, alpha):
        self._line_d_alpha = max(0.01, min(1.0, float(alpha)))

    def line_lost_fwd(self, ratio):
        pass

    def line_lost_grace(self, ms):
        self._line_gap_ms = max(0, int(ms))

    def line_accel(self, accel_per_s):
        pass

    def line_end_detect(self, confirm_ms=None, escape_mag=None, escape_trend=None, coast_ratio=None,
                        recover_hold_ms=None):
        if confirm_ms is not None:
            self._line_end_ms = int(confirm_ms)

    def line_debug_interval(self, ms):
        self._line_debug_interval = int(ms)

    def reset_line_pid(self):
        self._line_reset()

    def line_error(self):
        s = self._line_sensor
        if s is None:
            return 0.0
        pos = s.position()
        return 0.0 if pos is None else pos

    def line_read(self, index=None):
        return self._line_sensor.read(index)

    ######################## Control step #####################

    def _line_reset(self):
        # _line_mark is kept: it belongs to the last crossing seen, and the
        # next turn uses it
        self._line_last_pos = None # seeded by the first reading, see below
        self._line_d = 0.0
        self._line_integral = 0.0
        self._line_abs = 0.0
        self._line_speed_state = None # set to the curve speed on the first step
        self._line_last_us = None
        self._line_lost_since = None
        self._line_lost_ms = 0
        self._line_ok_ts = None # last time the robot held the line for a while
        self._line_hold_since = None # start of the current unbroken stretch on it
        self._line_lost_corner = False
        self._line_lost_mid = False # the current loss began under the middle eyes
        self._line_pivoting = False
        # crossing detector, see line_crossed()
        self._line_cross_seen = [None] * (self._line_sensor.n_sensors if self._line_sensor else 5)
        self._line_cross_wide = None
        self._line_cross_off = 0
        self._line_cross_hits = 0
        self._line_cross_first = None
        self._line_cross_event = False
        self._line_stop_at_cross = False
        self._line_steer = 0.0
        self._line_seen = 0
        self._line_side = 0
        self._line_corner_ts = None # last wide one-sided pattern, see follow_line_step()
        self._line_corner_side = 0
        self._line_lost_heading = None # heading when the line was lost, see _line_heading()
        self._line_sweep_side = 0
        self._line_sweep_n = 0
        self._line_acute = False
        self._line_found_ts = None # the line was last found again by a search
        self._last_line_state = LINE_CENTER

    '''
        One line following step; call it every 5 ms or so. Never blocks.

        Returns:
            False once the line has been lost for longer than the lost
            timeout (motors stopped), True otherwise.
    '''
    def follow_line_step(self):
        s = self._line_sensor
        if s is None:
            return False

        pos = s.update()
        if pos is not None:
            pat = s.pattern()
            n = s.n_sensors
            outer = 1 << (n - 1)
            if self._line_edge and n >= 4:
                # only an outer eye sees the line: its centre is already past
                # the array, further out than the eye itself
                if pat == 1:
                    pos = -self._line_edge
                elif pat == outer:
                    pos = self._line_edge
            if s.count() >= 3 and bool(pat & 1) != bool(pat & outer) and (
                    self._line_found_ts is None or ticks_diff(ticks_ms(), self._line_found_ts) > 150):
                # three or more eyes, reaching one outer eye but not the other:
                # the apex of a corner turning towards that side. If the line
                # disappears shortly after, that is where it went. The first
                # such pattern of a corner tells the side: at an acute corner
                # the branch shows up on its own side first, and then, as the
                # robot runs over the apex, both lines sweep across the array
                # and end up lighting the other outer eye. A corner ends when
                # such patterns stop for a moment (the next one may follow
                # within a few cm, turning the other way). Not right after the
                # line was found again by a search: it then lies across the
                # array at an angle, which is no corner
                now_ms = ticks_ms()
                if self._line_corner_ts is None or ticks_diff(now_ms, self._line_corner_ts) > 80:
                    self._line_corner_side = 1 if pat & outer else -1
                self._line_corner_ts = now_ms
        now = ticks_us()
        if self._line_last_us is None:
            dt = 0.01
        else:
            dt = ticks_diff(now, self._line_last_us) / 1000000
            if dt < 0.001:
                dt = 0.001
            elif dt > 0.05:
                dt = 0.05
        self._line_last_us = now

        cruise, slow = self._line_speeds()
        if self._line_speed_state is None:
            self._line_speed_state = slow

        searching = self._line_lost_since is not None
        if pos is not None and searching and self._line_lost_heading is not None:
            # Turned this far from where the line was lost, the robot faces
            # back the way it came: what the sensor finds there is the line it
            # was following, not the branch it is looking for. Following it
            # would drive the robot back along the track
            turned = self._line_heading() - self._line_lost_heading
            if abs(turned) > self._line_max_turn:
                pos = None
        if pos is not None and searching:
            # while searching, a line at an outer eye is not caught yet: the
            # opposite eye only brushes the end of the line we came from
            # (ignore it), the expected eye means keep pivoting at search
            # speed until the line reaches the inner eyes
            e = pos * self._line_invert
            if abs(e) > 0.6 and self._line_lost_ms < 400:
                # just after losing it, an edge eye is still brushing the line we
                # came from: keep searching. Later on an edge reading is the line
                # itself arriving, so it counts
                if (e > 0) == (self._line_side > 0) or self._line_side == 0:
                    self._line_side = 1 if e > 0 else -1
                pos = None
                self._line_lost_corner = True
            else:
                # a single frame is a flicker (low contrast, a speck): steer on it
                # but only call the line found again on the second frame in a
                # row, so flickers cannot keep resetting the give-up timer
                self._line_seen += 1
                if self._line_seen < 2:
                    self._line_last_pos = e
                    self._line_d = 0.0
                    steer = max(-1.0, min(1.0, self._line_kp * e))
                    turn = steer * slow
                    self.run_speed(slow + turn, slow - turn)
                    self._line_last_us = now
                    return True
        if pos is None:
            self._line_seen = 0

        if pos is None:
            # ---- line lost ----
            now_ms = ticks_ms()
            if self._line_lost_since is None:
                self._line_lost_since = now_ms
                # a sharp corner: the line left under an outer eye. Otherwise it
                # vanished from under the middle: a gap or the end of the line
                last = self._line_last_pos or 0.0
                corner_seen = self._line_corner_ts is not None and \
                    ticks_diff(now_ms, self._line_corner_ts) <= self._line_corner_ms
                # Gone from under the middle right after a corner's apex: an
                # acute corner, whose branch leaves far back (see the sweep)
                self._line_acute = corner_seen and abs(last) < 0.5
                self._line_lost_corner = corner_seen or abs(last) >= 0.5
                # decided once, here, and not touched again until the line is
                # back: brushing the stub of the line we came from promotes
                # _line_lost_corner below, and the end of a line must not be
                # reclassified as a corner by it
                self._line_lost_mid = not self._line_lost_corner
                if corner_seen:
                    self._line_side = self._line_corner_side * self._line_invert
                elif self._line_lost_corner:
                    self._line_side = 1 if last > 0 else -1
                elif abs(self._line_steer) > 0.2:
                    # the robot was turning when the line went out of sight, so
                    # the sensor swung off it: the line is on the other side
                    self._line_side = -1 if self._line_steer > 0 else 1
                elif self._line_side == 0:
                    # nothing better known: search where it drifted last
                    self._line_side = 1 if last >= 0 else -1
                self._line_lost_heading = self._line_heading()
                self._line_sweep_side = self._line_side
                self._line_sweep_n = 0
            self._line_lost_ms = ticks_diff(now_ms, self._line_lost_since)
            self._line_hold_since = None
            if self._line_ok_ts is None:
                self._line_ok_ts = now_ms

            # give up on how long it has been since the robot last followed the
            # line, not since the last glimpse of it: while searching, single
            # frames catching the stub of the line we came from would otherwise
            # keep the search alive for ever
            if ticks_diff(now_ms, self._line_ok_ts) > self._line_lost_timeout:
                self.stop()
                if self._line_debug:
                    print('line lost')
                return False

            steer = 0
            if self._line_lost_corner or self._line_lost_ms >= 2 * self._line_gap_ms + 100:
                # sweep: pivot towards the side the line was last seen on, then
                # turn back a little further each time. A wrong guess costs one
                # short sweep instead of a full turn on the spot
                turned = None
                if self._line_lost_heading is not None:
                    turned = self._line_heading() - self._line_lost_heading
                if turned is not None:
                    # The robot knows how far it has turned, so the sweep goes
                    # by angle: first to the expected side - all the way for
                    # an acute corner, whose branch may be 150 degrees round,
                    # 90 degrees otherwise - then wide each way, never round
                    # to the line it came from
                    side = self._line_sweep_side or 1
                    if self._line_sweep_n == 0 and not self._line_acute:
                        limit = min(90, self._line_max_turn)
                    else:
                        limit = self._line_max_turn
                    if turned * side >= limit:
                        side = -side
                        self._line_sweep_side = side
                        self._line_sweep_n += 1
                else:
                    swept = self._line_lost_ms
                    if not self._line_lost_corner:
                        swept -= 2 * self._line_gap_ms + 100
                    side = self._line_side
                    period = 350
                    while swept >= period:
                        swept -= period
                        side = -side
                        period *= 2
                steer = side
                pivot = self._line_search_speed or slow
                left = pivot * steer
                right = -pivot * steer
                self._line_pivoting = True
            elif self._line_lost_ms < self._line_gap_ms:
                # coast straight over a gap
                left = right = slow
            else:
                # no line after the gap: back up to where it vanished, so the
                # pivot that follows sweeps the sensor over a branch that was
                # already behind it (short sensor arm, 4-eye missing a corner)
                left = right = -slow
            self._line_speed_state = slow
            self._line_d = 0.0
            self._line_integral = 0.0
            speed = slow
        else:
            # ---- on the line ----
            e = pos * self._line_invert
            if self._line_last_pos is None:
                # first reading of this move: no derivative from a made-up past
                self._line_last_pos = e
            if self._line_lost_since is not None:
                # just found it again: no derivative kick, start gently
                self._line_lost_since = None
                self._line_lost_mid = False
                self._line_lost_corner = False
                self._line_corner_ts = None
                self._line_lost_heading = None
                self._line_found_ts = ticks_ms()
                self._line_last_pos = e
                self._line_d = 0.0
                self._line_speed_state = slow
                if self._line_pivoting:
                    # the robot is still turning from the search and would swing
                    # straight past the line: stop that rotation first
                    self._line_pivoting = False
                    pivot = self._line_search_speed or slow
                    self.run_speed(-pivot * self._line_side, pivot * self._line_side)
                    self._line_last_us = now
                    return True
            if abs(e) >= 0.5:
                self._line_side = 1 if e > 0 else -1
            elif abs(e) < 0.2:
                self._line_side = 0

            d_raw = (e - self._line_last_pos) / dt
            self._line_d += getattr(self, "_line_d_alpha", 0.5) * (d_raw - self._line_d)
            self._line_last_pos = e
            if self._line_ki:
                # a new curve starts from zero instead of unwinding the last
                # one first, and the term fades once the robot is centred
                if e * self._line_integral < 0:
                    self._line_integral = 0.0
                self._line_integral += e * dt
                lim = 0.5 / self._line_ki
                self._line_integral = max(-lim, min(lim, self._line_integral))
                if abs(e) < 0.2:
                    self._line_integral *= 0.9
            else:
                self._line_integral = 0.0

            steer = self._line_kp * e + self._line_ki * self._line_integral + self._line_kd * self._line_d
            steer = max(-1.0, min(1.0, steer))
            self._line_steer = steer
            # "following" means holding the line for a stretch, not brushing it
            # for a frame: at the end of a line the robot keeps catching the
            # stub it came from, and that must not read as progress
            now_ms = ticks_ms()
            if self._line_hold_since is None:
                self._line_hold_since = now_ms
            elif ticks_diff(now_ms, self._line_hold_since) >= 300:
                self._line_ok_ts = now_ms

            # curve estimate: |pos| held for a moment, so the speed does not
            # jump back up between two eyes lighting up
            ae = abs(e)
            if ae > self._line_abs:
                self._line_abs = ae
            else:
                self._line_abs += (ae - self._line_abs) * min(1.0, dt / 0.15)
            target = cruise - (cruise - slow) * min(1.0, self._line_slowdown * self._line_abs)

            # slow down at once, speed up gradually
            if target <= self._line_speed_state:
                self._line_speed_state = target
            else:
                self._line_speed_state = min(target, self._line_speed_state + max(cruise - slow, 40) * dt / 0.25)
            speed = self._line_speed_state

            turn = steer * cruise
            left = speed + turn
            right = speed - turn
            # keep the difference between the wheels when one saturates
            cap = self._line_outer_cap or 100
            if left > cap:
                right -= left - cap
                left = cap
            elif right > cap:
                left -= right - cap
                right = cap
            if left < -100:
                left = -100
            if right < -100:
                right = -100

        if self._line_min_wheel:
            left, right = self._line_floor(left, right)
        self.run_speed(left, right)
        self._line_watch_crossing()

        if self._line_debug:
            now_ms = ticks_ms()
            if ticks_diff(now_ms, self._line_debug_ts) >= self._line_debug_interval:
                self._line_debug_ts = now_ms
                print('LINE,%d,%s,%s,%.2f,%d,%d,%d' % (now_ms, bin(s.pattern()), 'lost' if pos is None else ('%.2f' % pos),
                                                     steer, speed, left, right))
        return True

    def _line_heading(self):
        # Heading in degrees, clockwise positive (as the angle sensor counts),
        # from the angle sensor or else the wheel encoders. None without
        # either: the search then goes by time alone
        if self._angle_sensor is not None:
            return self._angle_sensor.angle
        if self.left_encoder and self.right_encoder and self._width:
            d = (self.left_encoder.angle() - self.right_encoder.angle()) * self._wheel_circ / 360
            return math.degrees(d / self._width)
        return None

    def _line_floor(self, left, right):
        # A wheel asked for less than it needs to turn at all stands still,
        # and the robot drags it round instead of turning. Small commands go
        # up to the minimum; an inner wheel meant to (nearly) stop while the
        # outer one drives turns gently backwards instead, so both wheels pull
        # and the robot turns about its middle.
        floor = self._line_min_wheel
        out = []
        for v, other in ((left, right), (right, left)):
            a = abs(v)
            if a >= floor:
                out.append(v)
            elif v < floor * 0.5 and other >= floor:
                out.append(-floor)
            elif a < floor * 0.5:
                out.append(0)
            else:
                out.append(floor if v > 0 else -floor)
        return out[0], out[1]

    '''
        Runs after every step. A bar reached at an angle - right after a
        curve - sweeps across the array instead of lighting it all at once:
        first one outer eye, a few frames later the other. So a crossing is
        judged over a short window: both outer eyes lit within 100 ms, and
        three eyes at once at some point in it, which a single line never
        does. Confirmed by a second sighting within 150 ms (the frames in
        between may miss it: weak eyes flicker over black), and only after a
        few frames without one, so the bar the robot starts on is left alone.
    '''
    def _line_watch_crossing(self):
        s = self._line_sensor
        n = s.n_sensors
        now_ms = ticks_ms()
        pat = s.pattern()
        seen = self._line_cross_seen
        for i in range(n):
            if pat & (1 << i):
                seen[i] = now_ms
        if s.count() >= 3:
            self._line_cross_wide = now_ms
        bar = s.cross() or (
            seen[0] is not None and seen[n - 1] is not None and self._line_cross_wide is not None
            and ticks_diff(now_ms, seen[0]) <= 100 and ticks_diff(now_ms, seen[n - 1]) <= 100
            and ticks_diff(now_ms, self._line_cross_wide) <= 100)
        if not bar:
            if self._line_cross_off < 100:
                self._line_cross_off += 1
            return
        if self._line_cross_off < 3:
            return
        if self._line_cross_first is None or ticks_diff(now_ms, self._line_cross_first) > 150:
            self._line_cross_first = now_ms
            self._line_cross_hits = 0
        self._line_cross_hits += 1
        if self._line_mark is None:
            self._line_mark = self.distance()
        if self._line_stop_at_cross:
            # slow down at once so the stop lands close to the bar
            self._line_speed_state = self._line_speeds()[1]
        if self._line_cross_hits >= self._line_confirm:
            self._line_cross_event = True
            self._line_cross_off = 0
            self._line_cross_hits = 0
            self._line_cross_first = None

    '''
        True once for every crossing line the robot has driven over since
        the last call, as seen by follow_line_step(). Lets a program count
        bars or react to them without stopping:

            while robot.follow_line_step():
                if robot.line_crossed():
                    count += 1
                await asyncio.sleep_ms(5)
    '''
    def line_crossed(self):
        if self._line_cross_event:
            self._line_cross_event = False
            return True
        return False

    async def follow_line(self, backward=True, line_state=None):
        if self._line_sensor is None:
            return False

        if hasattr(self._line_sensor, 'update'):
            return self.follow_line_step()

        if line_state is None and hasattr(self._line_sensor, 'check'):
            line_state = self._line_sensor.check()

        if line_state == LINE_END:
            if backward:
                self.run(DIR_BACKWARD, self._min_speed)
        elif line_state == LINE_CENTER:
            if self._last_line_state == LINE_CENTER:
                self.forward()
            else:
                self.run(DIR_FORWARD, self._min_speed)
        elif line_state == LINE_CROSS:
            self.run(DIR_FORWARD, self._min_speed)
        else:
            if line_state == LINE_RIGHT:
                self.run_speed(self._min_speed, int(self._min_speed * 1.25))
            elif line_state == LINE_RIGHT2:
                self.run_speed(0, self._min_speed)
            elif line_state == LINE_RIGHT3:
                while line_state != LINE_CENTER and line_state != LINE_LEFT:
                    self.run_speed(-self._min_speed, self._min_speed)
                    line_state = self._line_sensor.check()
                self._last_line_state = line_state
                return True
            elif line_state == LINE_LEFT:
                self.run_speed(int(self._min_speed * 1.25), self._min_speed)
            elif line_state == LINE_LEFT2:
                self.run_speed(self._min_speed, 0)
            elif line_state == LINE_LEFT3:
                while line_state != LINE_CENTER and line_state != LINE_RIGHT:
                    self.run_speed(self._min_speed, -self._min_speed)
                    line_state = self._line_sensor.check()
                self._last_line_state = line_state
                return True

        self._last_line_state = line_state
        return True

    def follow_line_pid(self, base=None):
        return self.follow_line_step()

    async def run_line_follow(self, base=None, on_event=None, lost_limit=60):
        self._line_reset()
        while self.mode_auto:
            if not self.follow_line_step():
                break
            await asyncio.sleep_ms(5)
        self.stop()

    '''
        After a crossing or before a turn: bring the wheel axle to where
        the sensor is, if line_sensor_offset()/line_turn_offset() was set.
        Then stops as asked.
    '''
    async def _line_advance(self, then):
        cruise, slow = self._line_speeds()
        if self._line_sensor_offset > 0 and self.left_encoder and self.right_encoder:
            # the offset counts from where the sensor saw the last crossing,
            # not from where the robot came to a halt after it
            remaining = self._line_sensor_offset
            mark = self._line_mark
            self._line_mark = None
            if mark is not None and self.distance() >= mark:
                remaining -= self.distance() - mark
            if remaining > self._distance_tolerance:
                await self.straight(slow, remaining / 10, CM, then)
            else:
                await self.stop_then(then)
            return
        if self._line_turn_offset_ms > 0:
            # Hold the curve speed for the whole advance. On a crossing every
            # eye is lit and the position is 0, so the controller would take
            # this as a straight and accelerate to the cruise speed - the time
            # the user tuned would then cover a different distance each run.
            start = ticks_ms()
            while ticks_diff(ticks_ms(), start) < self._line_turn_offset_ms:
                self._line_speed_state = slow
                # Past a junction the line very often simply stops - at a T, or
                # at a bar the robot meets head on. That is the normal case
                # here, not something to go looking for, so once the line is
                # gone drive straight for the rest of the time instead of
                # letting the controller coast, back up and sweep for it.
                if self._line_lost_since is None and self.follow_line_step():
                    pass
                else:
                    l, r = self._calib_speed(slow)
                    self.run_speed(l, r)
                await asyncio.sleep_ms(5)
        await self.stop_then(then)

    ######################## Follow until #####################

    '''
        Follows the line until a crossing line is under the sensor, then
        stops. A crossing is only accepted
        while the robot is centred on the line, so a sharp corner cutting
        across the eyes is not mistaken for one.

        Returns: True on a crossing, False if the line was lost
    '''
    async def follow_line_until_cross(self, then=STOP):
        s = self._line_sensor
        if s is None:
            return False
        self._line_reset()
        self._line_stop_at_cross = True
        ok = True
        while True:
            ok = self.follow_line_step()
            if not ok or self.line_crossed():
                break
            await asyncio.sleep_ms(5)
        self._line_stop_at_cross = False
        await self.stop_then(then)
        return ok

    '''
        Follows the line until it ends: no eye sees it for a moment while
        it was under the middle of the sensor just before. Losing it under
        an outer eye is a corner instead, and the robot turns to find it.

        Needs a sensor that can tell "no eye sees the line" from "on track":
        LineSensor2P never reports it (both eyes straddle the line), so it
        returns False at once there. 3P, 4P and 5P are fine.

        Returns: True at the end of the line, False if it was lost in a
        corner and not found again
    '''
    async def follow_line_until_end(self, then=STOP):
        s = self._line_sensor
        if s is None or s.n_sensors < 3:
            return False
        self._line_reset()
        self._line_ok_ts = ticks_ms()
        ok = True
        while True:
            if not self.follow_line_step():
                ok = False
                break # searched for the line long enough and never found it
            if s.lost() and self._line_lost_mid and self._line_lost_ms >= self._line_end_ms:
                break
            if ticks_diff(ticks_ms(), self._line_ok_ts) > max(self._line_end_ms, 1200):
                break # only brushing the line since a while: this is its end
            await asyncio.sleep_ms(5)
        await self.stop_then(then)
        return ok

    async def follow_line_by_time(self, timerun, then=STOP):
        if self._line_sensor is None:
            return False
        self._line_reset()
        start_time = ticks_ms()
        duration = timerun * 1000 # convert to ms
        ok = True
        while ticks_diff(ticks_ms(), start_time) < duration:
            ok = self.follow_line_step()
            if not ok:
                break
            await asyncio.sleep_ms(5)
        await self.stop_then(then)
        return ok

    '''
        Follows the line until condition() has been true for a few
        readings in a row.
    '''
    async def follow_line_until(self, condition, then=STOP):
        if self._line_sensor is None:
            return False
        self._line_reset()
        count = 0
        ok = True
        while True:
            ok = self.follow_line_step()
            if not ok:
                break
            if condition():
                count += 1
                if count >= self._line_confirm:
                    break
            else:
                count = 0
            await asyncio.sleep_ms(5)
        await self.stop_then(then)
        return ok

    ######################## Turning onto a line #####################

    '''
        Turns until the line is centred under the sensor, so the robot is
        ready to follow it. Turns fast with the angle sensor (if enabled)
        for the first part, then slowly while looking for the line, and
        trims until the line is centred.

        Parameters:
            steering (Number) - > 0 turn right, < 0 turn left; +-100 pivots
                in place, smaller values arc

        Returns: True when the line was found, False on timeout
    '''
    async def turn_until_line_detected(self, steering, then=STOP):
        s = self._line_sensor
        if s is None or steering == 0:
            return False
        self._line_reset()
        await self._line_advance(None)

        cruise, slow = self._line_speeds()
        sign = 1 if steering > 0 else -1
        use_gyro = self._use_gyro and self._angle_sensor is not None and abs(steering) >= 100
        if use_gyro:
            await self.reset_angle()

        def pivot(v):
            l, r = self._calc_steering(v, steering)
            self.run_speed(l, r)

        # the line sweeps in from the side the robot turns towards; brake as soon
        # as it reaches the inner eye on that side, the rest of the way is
        # covered by the braking itself. Following takes it from there
        centre = 0.3
        entry = sign
        def dbg(what, pos):
            if self._line_debug:
                print('TURN,%d,%s,%s,%s' % (ticks_diff(ticks_ms(), start), what, bin(s.pattern()),
                                           'lost' if pos is None else ('%.2f' % pos)))

        pivot(cruise if use_gyro else slow)
        start = ticks_ms()
        left_at = None
        # the line we started from stays within reach of the sensor for the
        # first few degrees (a crossing bar runs right past it) and can come
        # back into view after a short blank; the next line is the one that
        # shows up after the sensor has seen nothing for a while. With the
        # gyro the first 40 degrees are turned blind, which settles that
        blank_needed = 0 if use_gyro else 120
        blank_since = None
        found = False
        dbg('start', s.update())
        while ticks_diff(ticks_ms(), start) < self._line_lost_timeout * 3:
            if use_gyro:
                turned = abs(self._angle_sensor.angle)
                if turned < 40:
                    # still on or next to the line we started from: keep going
                    await asyncio.sleep_ms(5)
                    continue
                if turned >= 60:
                    pivot(slow)
                    use_gyro = False
            pos = s.update()
            now_ms = ticks_ms()
            if pos is None:
                if blank_since is None:
                    blank_since = now_ms
            if left_at is None:
                if pos is None or abs(pos) > 0.6 or ticks_diff(now_ms, start) > 600:
                    left_at = now_ms
                    dbg('left the line', pos)
            elif pos is not None:
                pivot(slow)
                blank = blank_since is not None and ticks_diff(now_ms, blank_since) >= blank_needed
                if pos * entry <= 0.5 and (blank or blank_needed == 0):
                    found = True
                    dbg('found', pos)
                    break
            if pos is not None and (blank_since is None or ticks_diff(now_ms, blank_since) < blank_needed):
                blank_since = None # too short a blank: still the starting line
            await asyncio.sleep_ms(5)

        self.brake()
        if found:
            # let it settle, then nudge back if the brake overshot: short pulses,
            # shorter every time, so they cannot overshoot again
            # pulses at the straight-line speed, longer each time the robot did
            # not budge: from standstill the shortest pulse often does nothing
            # against the static friction of the drive
            pulse = 40
            last = None
            for _ in range(4):
                await asyncio.sleep_ms(120)
                pos = s.update()
                dbg('settled', pos)
                if pos is None or abs(pos) <= centre:
                    break
                if last is not None and abs(pos - last) < 0.1:
                    pulse *= 2
                last = pos
                v = cruise if pos > 0 else -cruise # line on the right: turn right
                self.run_speed(v, -v)
                await asyncio.sleep_ms(pulse)
                self.brake()
        else:
            dbg('timeout', s.update())
        await self.stop_then(then)
        return found

    # develop-branch name: direction -1 left, +1 right
    async def turn_until_line(self, direction, speed=None, max_ms=2500, then=None):
        return await self.turn_until_line_detected(100 if direction > 0 else -100, then)

    async def turn_until_condition(self, steering, condition, then=STOP):
        count = 0
        await self.turn(steering)
        while True:
            if condition():
                count += 1
                if count >= self._line_confirm:
                    break
            else:
                count = 0
            await asyncio.sleep_ms(10)
        await self.stop_then(then)
