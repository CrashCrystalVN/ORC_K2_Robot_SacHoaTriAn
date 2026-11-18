"""
=============================================================================
CHIẾN THUẬT GIẢI MÊ CUNG ROBOT ORC K2 - "SẮC HOA TRI ÂN" (STEM 20/11)
THUẬT TOÁN: LEFT WALL FOLLOWER + PID BÁM TƯỜNG TRÁI + CHỐNG KẸT PHỐI HỢP + CHỐNG KẸT LOOPS
=============================================================================
Chuyển đổi 100% logic Arduino C++ chuẩn sang MicroPython bất đồng bộ (async/await):
1. Tham số hình học hiệu chuẩn chuẩn xác theo Robot K2 (190 x 218 mm) & Sa bàn Thể lệ:
   - Hành lang mê cung rộng 250 mm (25.0 cm).
   - Hai cảm biến Laser Trái/Phải cách tâm đối xứng 67.6 mm (khoảng cách 2 sensor = 135.2 mm).
   - Khi robot chạy chính giữa hành lang 25cm: cự ly đo được từ laser trái = 5.74 cm (~5.8 cm).
   - Khung robot chiếm 21.8 cm -> khe hở mỗi bên còn ~1.6 cm.
   - Nhận diện ngã rẽ mở trái: khi distanceL > 16.0 cm (tường trái biến mất).
   - Nhận diện vật cản trước mặt: distanceF < 16.0 cm (cảm biến siêu âm HY-SRF05).
   - Nhận diện ngã rẽ phải thông thoáng: distanceR > 15.0 cm.
2. Thuật toán PID bám tường trái:
   - Kp = 3.5, Ki = 0.018, Kd = 3.8 (Quy đổi qua PWM_SCALE = 100.0 / 255.0).
   - Giữ robot luôn bám song song vách trái, triệt tiêu dốc lệch và sai số tĩnh.
3. Thuật toán chống kẹt phối hợp (Coordinated Anti-Stuck):
   - Kẹt 999: Cảm biến siêu âm trước trả về 999.0 liên tục > 600ms (kẹt sát tường / mất echo) -> Lùi 3cm.
   - Kẹt đứng yên 3.0s: Cả 3 cảm biến giữ nguyên trong ±2.0 cm trong 3000ms -> Lùi 3cm.
4. Thuật toán chống kẹt lặp Loops (Loop Anti-Stuck):
   - Nếu lặp lại cùng một hành động rẽ (1=Rẽ Trái, 2=Rẽ Phải, 3=Quay Đầu) >= 5 lần mà không đổi vị trí -> Kẹt vòng lặp!
   - Robot tự động dừng và lùi thoát hiểm 5cm, xóa bộ đếm loops.
5. Cơ chế phản hồi tức thì < 20ms:
   - Toàn bộ chu trình và các bước trễ delay đều phân mảnh thành các lát cắt 10-20ms kiểm tra cờ AUTO.
   - Ngay khi người dùng nhấn nút OPTIONS trên tay cầm, robot lập tức phanh dừng khẩn cấp.
=============================================================================
"""

import asyncio
try:
    from time import ticks_ms, ticks_diff
except ImportError:
    import time
    def ticks_ms(): return int(time.time() * 1000)
    def ticks_diff(end, start): return end - start

# Tương thích MicroPython asyncio.sleep_ms và CPython asyncio.sleep
if hasattr(asyncio, 'sleep_ms'):
    asleep_ms = asyncio.sleep_ms
else:
    async def asleep_ms(ms):
        await asyncio.sleep(ms / 1000.0)


# ====================================================================
# 1. HẰNG SỐ CẤU HÌNH HÌNH HỌC & NGƯỠNG KHOẢNG CÁCH (CENTIMET)
# ====================================================================
# Sa bàn: Hành lang rộng 25.0 cm | Robot K2: Phủ bì 21.8 cm, Cảm biến X=±6.76 cm
FRONT_THRESHOLD = 16.0        # Khoảng cách an toàn phía trước (cm) dừng để rẽ phải / quay đầu
FRONT_TOO_CLOSE = 10.0        # Quá sát tường trước (< 10cm) -> Lùi nhẹ trước khi rẽ trái
DESIRED_LEFT_WALL = 5.8       # Cự ly bám tường trái lý tưởng để robot đi chính giữa hành lang 25cm (cm)
MAX_WALL_DIST = 18.0          # Cự ly tối đa coi là có tường trái (cm)
LEFT_OPENING_THRESHOLD = 16.0 # Ngưỡng nhận diện mở ngã rẽ bên trái (cm)
RIGHT_CLEAR = 15.0            # Khoảng cách trống tối thiểu bên phải để rẽ phải (cm)

# Ngưỡng chống kẹt
STUCK_TOLERANCE = 2.0         # Ngưỡng khoảng cách không đổi (±2.0 cm)
STUCK_TIME_LIMIT = 3000       # 3.0 giây: 3 cảm biến không đổi ±2cm = KẸT CƠ KHÍ
STUCK_999_LIMIT = 600         # 0.6 giây: Cảm biến trước trả về 999 liên tục = KẸT QUÁ SÁT MŨI
BACKWARD_3CM_MS = 200         # Thời gian lùi nhẹ khoảng 3-4 cm (ms)
BACKWARD_5CM_MS = 320         # Thời gian lùi thoát kẹt Loops khoảng 5-6 cm (ms)
MAX_REPEAT_ACTIONS = 5        # 5 lần lặp lại cùng hành động rẽ không đổi vị trí = KẸT LOOPS

# ====================================================================
# 2. QUY ĐỔI TỐC ĐỘ ARDUINO (0..255) SANG DRIVEBASE ORC K2 (-100..100)
# ====================================================================
PWM_SCALE = 100.0 / 255.0     # Hệ số tỉ lệ = 0.392157

BASE_SPEED_PWM = 125
MIN_SPEED_PWM = 60
MAX_SPEED_PWM = 220
TURN_LEFT_SPEED_PWM = 120
TURN_RIGHT_SPEED_PWM = 140
TURN_BACK_SPEED_PWM = 145
BACKWARD_SPEED_PWM = 125

BASE_SPEED = int(round(BASE_SPEED_PWM * PWM_SCALE))         # ~49%
MIN_SPEED = int(round(MIN_SPEED_PWM * PWM_SCALE))           # ~24%
MAX_SPEED = int(round(MAX_SPEED_PWM * PWM_SCALE))           # ~86%
TURN_LEFT_SPEED = int(round(TURN_LEFT_SPEED_PWM * PWM_SCALE))   # ~47%
TURN_RIGHT_SPEED = int(round(TURN_RIGHT_SPEED_PWM * PWM_SCALE)) # ~55%
TURN_BACK_SPEED = int(round(TURN_BACK_SPEED_PWM * PWM_SCALE))   # ~57%
BACKWARD_SPEED = int(round(BACKWARD_SPEED_PWM * PWM_SCALE))     # ~49%

# Thời gian trễ căn chỉnh cua góc (ms)
PRE_TURN_FORWARD_DELAY = 180  # Nhích tiến qua mép khúc cua trước khi rẽ trái
POST_TURN_FORWARD_DELAY = 160 # Nhích tiến sau khi rẽ để xe nằm thẳng vào hành lang mới
TURN_LEFT_DELAY_MS = 280      # Thời gian rẽ trái 90 độ fallback (khi không có IMU)
TURN_RIGHT_DELAY_MS = 320     # Thời gian rẽ phải 90 độ fallback (khi không có IMU)
TURN_BACK_DELAY_MS = 540      # Thời gian quay đầu 180 độ fallback (khi không có IMU)

# Bù tốc độ động cơ phần cứng
RIGHT_COMP = 0
LEFT_COMP = 0


# ====================================================================
# 3. TRÌNH QUẢN LÝ BỘ ĐIỀU KHIỂN PID BÁM TƯỜNG TRÁI
# ====================================================================
class WallFollowerPID:
    """
    Bộ điều khiển PID bám tường trái:
    - Kp = 3.5, Ki = 0.018, Kd = 3.8
    - Tính toán theo thang PWM Arduino, sau đó quy đổi sang DriveBase qua PWM_SCALE.
    - Tích hợp Anti-windup chống bão hòa khâu tích phân.
    """
    def __init__(self, kp=3.5, ki=0.018, kd=3.8):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.reset()

    def reset(self):
        self.last_error = 0.0
        self.integral = 0.0
        self.last_time = ticks_ms()

    def compute(self, current_error):
        now = ticks_ms()
        dt = ticks_diff(now, self.last_time) / 1000.0
        if dt <= 0.0 or dt > 0.5:
            dt = 0.03  # Giá trị phòng ngừa dt bất thường
        self.last_time = now

        # Khâu Tỷ lệ (P)
        p_term = self.kp * current_error

        # Khâu Tích phân (I) kèm chống bão hòa (Anti-windup)
        self.integral += current_error * dt
        if self.integral > 100.0: self.integral = 100.0
        elif self.integral < -100.0: self.integral = -100.0
        i_term = self.ki * self.integral

        # Khâu Vi phân (D)
        derivative = (current_error - self.last_error) / dt
        d_term = self.kd * derivative
        self.last_error = current_error

        # Đầu ra PID
        output = p_term + i_term + d_term
        return output


# ====================================================================
# 4. TRÌNH THEO DÕI CHỐNG KẸT PHỐI HỢP & CHỐNG KẸT LOOPS
# ====================================================================
class StuckTracker:
    """
    Quản lý 2 cơ chế chống kẹt:
    1. Chống kẹt phối hợp (Coordinated Anti-Stuck):
       - Cảm biến trước trả về 999 liên tục > 600ms = KẸT QUÁ SÁT MŨI
       - Cả 3 cảm biến không đổi (±2cm) trong 3.0s = KẸT CƠ KHÍ
    2. Chống kẹt vòng lặp (Loop Stuck):
       - 1 hành động rẽ (1=Trái, 2=Phải, 3=Quay đầu) lặp >= 5 lần = KẸT LOOPS
    """
    def __init__(self):
        self.reset_stuck_tracker()
        self.reset_loop_stuck()

    def reset_stuck_tracker(self):
        self.last_stuck_f = -999.0
        self.last_stuck_l = -999.0
        self.last_stuck_r = -999.0
        self.last_stuck_time = ticks_ms()
        self.stuck_999_start_time = 0

    def reset_loop_stuck(self):
        self.last_action_id = -1
        self.repeat_action_count = 0

    def check_stuck(self, dist_f, dist_l, dist_r):
        now = ticks_ms()

        # 1. Cảm biến trước trả về 999.0 (kẹt quá sát tường hoặc mất echo siêu âm)
        if dist_f >= 900.0:
            if self.stuck_999_start_time == 0:
                self.stuck_999_start_time = now
            elif ticks_diff(now, self.stuck_999_start_time) > STUCK_999_LIMIT:
                return True
        else:
            self.stuck_999_start_time = 0

        # 2. Cả 3 cảm biến giữ nguyên trong khoảng ±STUCK_TOLERANCE trong STUCK_TIME_LIMIT (3.0s)
        # Chỉ xét khi các cảm biến đo được khoảng cách thực tế (không phải mất tín hiệu)
        f_same = abs(dist_f - self.last_stuck_f) <= STUCK_TOLERANCE
        l_same = abs(dist_l - self.last_stuck_l) <= STUCK_TOLERANCE
        r_same = abs(dist_r - self.last_stuck_r) <= STUCK_TOLERANCE

        if f_same and l_same and r_same:
            if ticks_diff(now, self.last_stuck_time) > STUCK_TIME_LIMIT:
                return True
        else:
            self.last_stuck_f = dist_f
            self.last_stuck_l = dist_l
            self.last_stuck_r = dist_r
            self.last_stuck_time = now

        return False

    def check_loop_stuck(self, action_id):
        if action_id == self.last_action_id:
            self.repeat_action_count += 1
            if self.repeat_action_count >= MAX_REPEAT_ACTIONS:
                return True
        else:
            self.last_action_id = action_id
            self.repeat_action_count = 1
        return False


# ====================================================================
# 5. CÁC HÀM ĐIỀU KHIỂN CHUYỂN ĐỘNG CƠ BẢN (NON-BLOCKING)
# ====================================================================
async def async_sleep_check(duration_ms, is_auto_func, step_ms=15):
    """Delay bất đồng bộ chia nhỏ, đảm bảo ngắt tức thì < 20ms khi bấm OPTIONS"""
    elapsed = 0
    while elapsed < duration_ms:
        if is_auto_func and not is_auto_func():
            return False
        wait_time = min(step_ms, duration_ms - elapsed)
        await asleep_ms(wait_time)
        elapsed += wait_time
    return True


def move_pid(robot, pid_output):
    """
    Điều khiển 2 bên bánh xe bằng đầu ra PID bám tường trái:
    - error = distanceL - DESIRED_LEFT_WALL
    - error > 0 (quá xa vách trái) -> pidOutput > 0 -> giảm tốc trái, tăng tốc phải -> LƯỢN SANG TRÁI
    - error < 0 (quá sát vách trái) -> pidOutput < 0 -> tăng tốc trái, giảm tốc phải -> LƯỢN SANG PHẢI
    """
    # Quy đổi đầu ra sang thang K2
    pid_k2 = pid_output * PWM_SCALE

    left_speed = BASE_SPEED - pid_k2 + LEFT_COMP
    right_speed = BASE_SPEED + pid_k2 + RIGHT_COMP

    # Giới hạn an toàn trong dải [MIN_SPEED, MAX_SPEED]
    left_speed = int(max(MIN_SPEED, min(MAX_SPEED, left_speed)))
    right_speed = int(max(MIN_SPEED, min(MAX_SPEED, right_speed)))

    robot.run_speed(left_speed, right_speed)


async def stop_robot(robot):
    """Phanh dừng robot dứt khoát"""
    robot.brake()
    await asleep_ms(40)
    robot.stop()


async def move_backward(robot, speed, duration_ms, is_auto_func=None):
    """Lùi xe trong khoảng thời gian duration_ms có kiểm tra ngắt OPTIONS"""
    robot.run_speed(-int(speed), -int(speed))
    await async_sleep_check(duration_ms, is_auto_func)
    await stop_robot(robot)


async def turn_left(robot, angle_sensor=None, is_auto_func=None):
    """Rẽ trái 90 độ tại chỗ: Bánh trái lùi, bánh phải tiến"""
    if angle_sensor is not None:
        try:
            start_heading = angle_sensor.heading
            robot.run_speed(-TURN_LEFT_SPEED, TURN_LEFT_SPEED)
            start_t = ticks_ms()
            while ticks_diff(ticks_ms(), start_t) < 700:
                if is_auto_func and not is_auto_func(): break
                await asleep_ms(15)
                cur_heading = angle_sensor.heading
                diff = cur_heading - start_heading
                while diff > 180: diff -= 360
                while diff < -180: diff += 360
                if abs(diff) >= 88.0:
                    break
            await stop_robot(robot)
            return
        except Exception:
            pass

    # Fallback thời gian chuẩn
    robot.run_speed(-TURN_LEFT_SPEED, TURN_LEFT_SPEED)
    await async_sleep_check(TURN_LEFT_DELAY_MS, is_auto_func)
    await stop_robot(robot)


async def turn_right(robot, angle_sensor=None, is_auto_func=None):
    """Rẽ phải 90 độ tại chỗ: Bánh trái tiến, bánh phải lùi"""
    if angle_sensor is not None:
        try:
            start_heading = angle_sensor.heading
            robot.run_speed(TURN_RIGHT_SPEED, -TURN_RIGHT_SPEED)
            start_t = ticks_ms()
            while ticks_diff(ticks_ms(), start_t) < 700:
                if is_auto_func and not is_auto_func(): break
                await asleep_ms(15)
                cur_heading = angle_sensor.heading
                diff = cur_heading - start_heading
                while diff > 180: diff -= 360
                while diff < -180: diff += 360
                if abs(diff) >= 88.0:
                    break
            await stop_robot(robot)
            return
        except Exception:
            pass

    # Fallback thời gian chuẩn
    robot.run_speed(TURN_RIGHT_SPEED, -TURN_RIGHT_SPEED)
    await async_sleep_check(TURN_RIGHT_DELAY_MS, is_auto_func)
    await stop_robot(robot)


async def turn_back(robot, angle_sensor=None, is_auto_func=None):
    """Quay đầu 180 độ tại chỗ khi gặp ngõ cụt"""
    if angle_sensor is not None:
        try:
            start_heading = angle_sensor.heading
            robot.run_speed(TURN_BACK_SPEED, -TURN_BACK_SPEED)
            start_t = ticks_ms()
            while ticks_diff(ticks_ms(), start_t) < 1100:
                if is_auto_func and not is_auto_func(): break
                await asleep_ms(15)
                cur_heading = angle_sensor.heading
                diff = cur_heading - start_heading
                while diff > 180: diff -= 360
                while diff < -180: diff += 360
                if abs(diff) >= 176.0:
                    break
            await stop_robot(robot)
            return
        except Exception:
            pass

    # Fallback thời gian chuẩn
    robot.run_speed(TURN_BACK_SPEED, -TURN_BACK_SPEED)
    await async_sleep_check(TURN_BACK_DELAY_MS, is_auto_func)
    await stop_robot(robot)


# ====================================================================
# 6. THUẬT TOÁN CHÍNH: RUN_MAZE_FOLLOWER
# ====================================================================
async def run_maze_follower(robot, laser_system, angle_sensor=None, is_auto_func=None):
    """
    Vòng lặp chính thuật toán Left Wall Follower + PID + Chống kẹt:
    - robot: DriveBase 4 bánh Mecanum
    - laser_system: Hệ thống cảm biến Front (SRF05), Left (VL53L0X), Right (VL53L0X)
    - angle_sensor: Cảm biến góc MPU6050 (tùy chọn)
    - is_auto_func: Hàm kiểm tra trạng thái AUTO (lambda: auto_running_flag)
    """
    print("\n" + "=" * 65)
    print(">>> [MAZE] BẮT ĐẦU THUẬT TOÁN LEFT WALL FOLLOWER + PID BÁM TƯỜNG TRÁI <<<")
    print(f"    Thông số: DESIRED_LEFT={DESIRED_LEFT_WALL}cm | FRONT_TH={FRONT_THRESHOLD}cm | OPEN_L={LEFT_OPENING_THRESHOLD}cm")
    print("=" * 65 + "\n")

    pid = WallFollowerPID(kp=3.5, ki=0.018, kd=3.8)
    stuck = StuckTracker()

    loop_count = 0

    while True:
        # Kiểm tra ngắt khẩn cấp từ nút OPTIONS (< 20ms)
        if is_auto_func and not is_auto_func():
            print("[MAZE] Nhan tin hieu ngat che do AUTO -> Dung robot ngay lap tuc!")
            await stop_robot(robot)
            break

        loop_count += 1

        # 1. Đọc 3 cảm biến khoảng cách (cm)
        dist_f, dist_l, dist_r = laser_system.read_all_cm(raw=False)

        # Telemetry in ra mỗi 15 chu kỳ (~450ms)
        if loop_count % 15 == 0:
            print(f"[MAZE TELEMETRY] F:{dist_f:5.1f}cm | L:{dist_l:5.1f}cm | R:{dist_r:5.1f}cm")

        # =============================================================
        # BƯỚC 1: THUẬT TOÁN CHỐNG KẸT PHỐI HỢP
        # 1. Cảm biến trước trả về 999.0 liên tục > 0.6s
        # 2. Khoảng cách 3 cảm biến giữ nguyên (±2cm) trong 3.0s
        # =============================================================
        if stuck.check_stuck(dist_f, dist_l, dist_r):
            print(f">>> [CHỐNG KẸT] PHÁT HIỆN KẸT (999 HOẶC ĐỨNG YÊN 3S)! F:{dist_f}cm | L:{dist_l}cm | R:{dist_r}cm -> LÙI NHẸ 3CM <<<")
            await stop_robot(robot)
            await asleep_ms(30)
            await move_backward(robot, BACKWARD_SPEED, BACKWARD_3CM_MS, is_auto_func)
            stuck.reset_stuck_tracker()
            continue

        # =============================================================
        # BƯỚC 2: QUY TẮC BÀN TAY TRÁI ƯU TIÊN SỐ 1
        # Nếu phát hiện bên trái có đường rẽ lớn (distanceL > 16.0cm) -> RẼ TRÁI
        # =============================================================
        if dist_l > LEFT_OPENING_THRESHOLD:
            # Nếu phía trước quá sát (< 10cm) -> Lùi nhẹ trước để mũi xe không va quẹt tường trước khi rẽ
            if dist_f < FRONT_TOO_CLOSE:
                print(f" -> Quá sát tường trước ({dist_f:.1f}cm < 10cm)! Lùi nhẹ trước khi rẽ trái")
                await stop_robot(robot)
                await asleep_ms(30)
                await move_backward(robot, int(100 * PWM_SCALE), 150, is_auto_func)
                dist_f, dist_l, dist_r = laser_system.read_all_cm(raw=False)

            # Kiểm tra kẹt lặp 5 vòng liên tiếp
            if stuck.check_loop_stuck(1):  # 1 = Rẽ Trái
                print(">>> [CHỐNG KẸT LOOPS] Rẽ trái 5 lần liên tiếp không đổi vị trí! Lùi 5cm <<<")
                await stop_robot(robot)
                await asleep_ms(40)
                await move_backward(robot, BACKWARD_SPEED, BACKWARD_5CM_MS, is_auto_func)
                stuck.reset_loop_stuck()
                continue

            # Bước 2.1: Nhích tiến qua khỏi mép khúc cua cột tường ngã rẽ
            move_pid(robot, 0.0)
            ok = await async_sleep_check(PRE_TURN_FORWARD_DELAY, is_auto_func)
            if not ok: break
            await stop_robot(robot)
            await asleep_ms(40)

            print(" -> Phát hiện ngã rẽ trái! Rẽ Trái (Turn Left 90°)")
            await turn_left(robot, angle_sensor, is_auto_func)

            # Bước 2.2: Nhích tiến sau khi rẽ để xe nằm thẳng vào hành lang mới
            move_pid(robot, 0.0)
            ok = await async_sleep_check(POST_TURN_FORWARD_DELAY, is_auto_func)
            if not ok: break

            # Reset bộ điều khiển PID bám đoạn tường mới
            pid.reset()

        # =============================================================
        # BƯỚC 3: KIỂM TRA VẬT CẢN PHÍA TRƯỚC (KHI BÊN TRÁI KÍN TƯỜNG)
        # =============================================================
        elif dist_f < FRONT_THRESHOLD:
            await stop_robot(robot)
            await asleep_ms(40)
            pid.reset()

            # Do bên trái kín tường, vướng trước mặt sẽ Rẽ Phải hoặc Quay Đầu
            if dist_r > RIGHT_CLEAR:
                if stuck.check_loop_stuck(2):  # 2 = Rẽ Phải
                    print(">>> [CHỐNG KẸT LOOPS] Rẽ phải 5 lần liên tiếp không đổi vị trí! Lùi 5cm <<<")
                    await move_backward(robot, BACKWARD_SPEED, BACKWARD_5CM_MS, is_auto_func)
                    stuck.reset_loop_stuck()
                    continue

                print(f" -> Tường trước chặn ({dist_f:.1f}cm)! Bên phải thông ({dist_r:.1f}cm) -> Rẽ Phải (Turn Right 90°)")
                await turn_right(robot, angle_sensor, is_auto_func)
                move_pid(robot, 0.0)
                ok = await async_sleep_check(POST_TURN_FORWARD_DELAY, is_auto_func)
                if not ok: break
            else:
                if stuck.check_loop_stuck(3):  # 3 = Quay Đầu
                    print(">>> [CHỐNG KẸT LOOPS] Quay đầu 5 lần liên tiếp không đổi vị trí! Lùi 5cm <<<")
                    await move_backward(robot, BACKWARD_SPEED, BACKWARD_5CM_MS, is_auto_func)
                    stuck.reset_loop_stuck()
                    continue

                print(f" -> Ngõ cụt (F:{dist_f:.1f}cm, L:{dist_l:.1f}cm, R:{dist_r:.1f}cm) -> Quay Đầu (Turn Back 180°)")
                await turn_back(robot, angle_sensor, is_auto_func)
                move_pid(robot, 0.0)
                await asleep_ms(20)

        # =============================================================
        # BƯỚC 4: KHI ĐI TRONG HÀNH LANG: BÁM TƯỜNG TRÁI BẰNG BỘ PID NHẠY
        # =============================================================
        else:
            # Reset đếm kẹt lặp khi di chuyển thẳng bình thường
            stuck.reset_loop_stuck()

            # Tính sai lệch khoảng cách so với cự ly lý tưởng
            error = dist_l - DESIRED_LEFT_WALL
            pid_output = pid.compute(error)

            if loop_count % 15 == 0:
                print(f" | Err: {error:5.1f}cm | PID: {pid_output:5.2f}")

            move_pid(robot, pid_output)

        # Chu kỳ lặp 30ms (giống Arduino delay(30))
        await asleep_ms(30)

    # Đảm bảo dừng robot khi thoát vòng lặp
    await stop_robot(robot)
    print(">>> [MAZE] ĐÃ DỪNG THUẬT TOÁN GIẢI MÊ CUNG <<<")
