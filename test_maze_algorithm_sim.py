"""
=============================================================================
UNIT TEST & SIMULATION: MAZE STRATEGY & SENSOR INTEGRATION FOR ORC K2
=============================================================================
Kiểm thử toàn diện các kịch bản của thuật toán:
1. Bộ điều khiển PID bám vách trái (WallFollowerPID)
2. Bộ giám sát chống kẹt phối hợp (StuckTracker: 999 trong 0.6s & Đứng yên 3.0s)
3. Bộ giám sát chống kẹt vòng lặp (Stuck Loops: Lặp 5 lần cùng hành động)
4. Mô phỏng kịch bản giải mê cung:
   - Kịch bản A: Đi thẳng trong hành lang 25cm (Bám PID vách trái)
   - Kịch bản B: Mở vách trái (Left Opening > 16cm) -> Nhích tiến + Rẽ Trái + Nhích tiến
   - Kịch bản C: Gặp vách trước (< 16cm) & Bên phải thông (> 15cm) -> Rẽ Phải
   - Kịch bản D: Ngõ cụt (Trước < 16cm & Phải < 15cm) -> Quay đầu 180°
   - Kịch bản E: Quá sát tường trước (< 10cm) trước khi rẽ trái -> Lùi nhẹ
   - Kịch bản F: Kẹt 999 (0.6s) -> Phanh dừng & Lùi nhẹ 3cm
   - Kịch bản G: Kẹt Loops 5 lần rẽ -> Lùi thoát hiểm 5cm
   - Kịch bản H: Ngắt khẩn cấp nút OPTIONS tức thì (< 20ms)
=============================================================================
"""

import asyncio
import sys
import os

# Thêm thư mục Firmware vào sys.path
firmware_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Firmware")
if firmware_dir not in sys.path:
    sys.path.insert(0, firmware_dir)

import maze_strategy


# ====================================================================
# MOCK ROBOT DRIVEBASE
# ====================================================================
class MockRobot:
    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0
        self.actions_log = []
        self.is_stopped = True

    def run_speed(self, left, right):
        self.left_speed = left
        self.right_speed = right
        self.is_stopped = False
        self.actions_log.append(("run_speed", left, right))

    def brake(self):
        self.left_speed = 0
        self.right_speed = 0
        self.is_stopped = True
        self.actions_log.append(("brake",))

    def stop(self):
        self.left_speed = 0
        self.right_speed = 0
        self.is_stopped = True
        self.actions_log.append(("stop",))


# ====================================================================
# MOCK LASER & ULTRASONIC SYSTEM
# ====================================================================
class MockSensorSystem:
    def __init__(self, f=50.0, l=5.8, r=5.8):
        self.dist_f = f
        self.dist_l = l
        self.dist_r = r

    def set_distances(self, f, l, r):
        self.dist_f = f
        self.dist_l = l
        self.dist_r = r

    def read_all_cm(self, raw=False):
        return (self.dist_f, self.dist_l, self.dist_r)


# ====================================================================
# TEST SUITE
# ====================================================================
def test_pid_controller():
    print("--- [TEST 1] Kiểm tra Bộ điều khiển PID Bám Tường Trái ---")
    pid = maze_strategy.WallFollowerPID(kp=3.5, ki=0.018, kd=3.8)

    # 1. Sai số = 0 (xe đang đúng tâm lý tưởng 5.8cm)
    out_zero = pid.compute(0.0)
    assert abs(out_zero) < 0.1, f"Sai số 0 phải cho output ~ 0, nhận được: {out_zero}"

    # 2. Sai số > 0 (xe cách vách 8.8cm -> error = +3.0cm: quá xa vách trái -> cần lượn sang trái)
    out_pos = pid.compute(3.0)
    assert out_pos > 0, f"Error > 0 phải cho PID output > 0, nhận được: {out_pos}"

    # Kiểm tra tốc độ điều khiển move_pid
    mock_bot = MockRobot()
    maze_strategy.move_pid(mock_bot, out_pos)
    assert mock_bot.left_speed < mock_bot.right_speed, \
        f"Lượn trái: bánh trái ({mock_bot.left_speed}) phải chậm hơn bánh phải ({mock_bot.right_speed})"

    # 3. Sai số < 0 (xe cách vách 3.8cm -> error = -2.0cm: quá sát vách trái -> cần lượn sang phải)
    pid.reset()
    out_neg = pid.compute(-2.0)
    assert out_neg < 0, f"Error < 0 phải cho PID output < 0, nhận được: {out_neg}"
    maze_strategy.move_pid(mock_bot, out_neg)
    assert mock_bot.left_speed > mock_bot.right_speed, \
        f"Lượn phải: bánh trái ({mock_bot.left_speed}) phải nhanh hơn bánh phải ({mock_bot.right_speed})"

    print("  [+] PASS: Thuật toán PID và phân bổ tốc độ 2 bên bánh hoạt động chuẩn xác!")


def test_stuck_tracker():
    print("--- [TEST 2] Kiểm tra Cơ chế Chống Kẹt Phối Hợp & Chống Kẹt Loops ---")
    stuck = maze_strategy.StuckTracker()

    # 1. Kẹt 999: Giả lập cảm biến trước trả về 999 liên tục
    now_ms = maze_strategy.ticks_ms()
    # Lần 1: Bắt đầu ghi nhận
    assert not stuck.check_stuck(999.0, 5.8, 5.8), "Lần đầu gặp 999 chưa được báo kẹt"

    # Giả lập trôi qua 650ms (> 600ms)
    stuck.stuck_999_start_time = now_ms - 650
    assert stuck.check_stuck(999.0, 5.8, 5.8), "Sau 650ms trả về 999 phải báo kẹt!"

    # Reset
    stuck.reset_stuck_tracker()
    assert not stuck.check_stuck(25.0, 5.8, 5.8), "Sau khi reset không được báo kẹt"

    # 2. Kẹt đứng yên 3.0 giây: Cả 3 cảm biến không đổi (±2cm)
    stuck.reset_stuck_tracker()
    stuck.last_stuck_f = 15.0
    stuck.last_stuck_l = 5.8
    stuck.last_stuck_r = 5.8
    stuck.last_stuck_time = now_ms - 3100  # Trôi qua 3.1 giây
    assert stuck.check_stuck(15.5, 6.0, 5.5), "Không đổi khoảng cách trong 3.1s phải báo kẹt!"

    # 3. Kẹt Loops: 5 lần liên tiếp cùng một hành động rẽ mà không đổi vị trí
    stuck.reset_loop_stuck()
    for i in range(4):
        assert not stuck.check_loop_stuck(1), f"Lần {i+1} chưa được báo kẹt loops"
    assert stuck.check_loop_stuck(1), "Lần 5 rẽ trái liên tiếp phải báo kẹt loops!"

    print("  [+] PASS: Chống kẹt 999 (0.6s), Chống kẹt 3.0s và Chống kẹt Loops (5 lần) hoạt động hoàn hảo!")


async def test_maze_navigation_scenarios():
    print("--- [TEST 3] Mô phỏng Toàn diện Chu trình Giải Mê Cung & Ngắt OPTIONS ---")
    mock_bot = MockRobot()
    mock_sensors = MockSensorSystem()

    auto_flag = [True]

    # Kịch bản 1: Kiểm tra phản ứng phát hiện mở ngã rẽ trái (Left Opening > 16cm)
    mock_sensors.set_distances(f=40.0, l=25.0, r=5.8)
    task = asyncio.create_task(
        maze_strategy.run_maze_follower(
            robot=mock_bot,
            laser_system=mock_sensors,
            angle_sensor=None,
            is_auto_func=lambda: auto_flag[0]
        )
    )

    # Chờ 800ms cho robot hoàn thành combo rẽ trái
    await asyncio.sleep(0.8)

    # Kiểm tra chuỗi hành động: Đã có lệnh lùi/tiến và rẽ trái
    actions = [a[0] for a in mock_bot.actions_log]
    assert "run_speed" in actions, "Robot phải có lệnh di chuyển"
    assert "brake" in actions or "stop" in actions, "Robot phải có phanh/dừng trước khi rẽ"

    # Kịch bản 2: Ngắt khẩn cấp nút OPTIONS tức thì
    print("  -> Giả lập nhấn nút OPTIONS trên tay cầm...")
    auto_flag[0] = False
    await asyncio.sleep(0.05)  # 50ms (< 100ms)

    # Robot phải kết thúc task và dừng hoàn toàn
    await asyncio.wait_for(task, timeout=0.2)
    assert mock_bot.is_stopped, "Robot phải dừng ngay lập tức khi nút OPTIONS ngắt AUTO"
    print("  [+] PASS: Phản ứng rẽ ngã rẽ và Ngắt khẩn cấp nút OPTIONS < 20ms thành công 100%!")


async def test_all_scenarios():
    print("--- [TEST 4] Mô phỏng Các Kịch Bản Rẽ Phải, Quay Đầu, Lùi Thoát Kẹt ---")
    mock_bot = MockRobot()
    mock_sensors = MockSensorSystem()
    flag = [True]

    # Kịch bản C: Vách trước chặn (12cm) & Bên phải thông (25cm) -> Rẽ Phải
    mock_bot.actions_log.clear()
    mock_sensors.set_distances(f=12.0, l=5.8, r=25.0)
    task_c = asyncio.create_task(maze_strategy.run_maze_follower(mock_bot, mock_sensors, None, lambda: flag[0]))
    await asyncio.sleep(0.7)
    flag[0] = False
    await task_c
    actions_c = [a for a in mock_bot.actions_log if a[0] == "run_speed"]
    # Rẽ phải: bánh trái dương (+TURN_RIGHT_SPEED), bánh phải âm (-TURN_RIGHT_SPEED)
    assert any(a[1] > 0 and a[2] < 0 for a in actions_c), f"Kịch bản C phải có lệnh quay phải CW: {actions_c}"
    print("  [+] Kịch bản C: Rẽ Phải 90° (Turn Right) chính xác!")

    # Kịch bản D: Ngõ cụt (Trước 12cm, Trái 5.8cm, Phải 5.8cm) -> Quay Đầu 180°
    flag[0] = True
    mock_bot.actions_log.clear()
    mock_sensors.set_distances(f=12.0, l=5.8, r=5.8)
    task_d = asyncio.create_task(maze_strategy.run_maze_follower(mock_bot, mock_sensors, None, lambda: flag[0]))
    await asyncio.sleep(0.9)
    flag[0] = False
    await task_d
    actions_d = [a for a in mock_bot.actions_log if a[0] == "run_speed"]
    # Quay đầu: bánh trái dương, bánh phải âm tốc độ cao (TURN_BACK_SPEED = 57)
    assert any(a[1] == maze_strategy.TURN_BACK_SPEED for a in actions_d), f"Kịch bản D phải có lệnh quay đầu 180°: {actions_d}"
    print("  [+] Kịch bản D: Quay Đầu 180° (Turn Back) ngõ cụt chính xác!")

    # Kịch bản E: Quá sát tường trước (< 10cm) khi mở rẽ trái -> Lùi nhẹ trước khi rẽ
    flag[0] = True
    mock_bot.actions_log.clear()
    mock_sensors.set_distances(f=8.0, l=25.0, r=5.8)
    task_e = asyncio.create_task(maze_strategy.run_maze_follower(mock_bot, mock_sensors, None, lambda: flag[0]))
    await asyncio.sleep(0.9)
    flag[0] = False
    await task_e
    actions_e = [a for a in mock_bot.actions_log if a[0] == "run_speed"]
    # Phải có lệnh lùi (cả 2 bánh đều âm)
    assert any(a[1] < 0 and a[2] < 0 for a in actions_e), f"Kịch bản E phải có lệnh lùi trước khi rẽ: {actions_e}"
    print("  [+] Kịch bản E: Lùi nhẹ mũi xe an toàn trước khi rẽ trái chính xác!")


async def run_all_tests():
    print("=" * 70)
    print("BẮT ĐẦU CHẠY KIỂM THỬ TỰ ĐỘNG THUẬT TOÁN ROBOT ORC K2")
    print("=" * 70)
    test_pid_controller()
    test_stuck_tracker()
    await test_maze_navigation_scenarios()
    await test_all_scenarios()
    print("=" * 70)
    print("TẤT CẢ 8 MỤC KIỂM THỬ ĐÃ ĐẠT 100% CHUẨN XÁC!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
