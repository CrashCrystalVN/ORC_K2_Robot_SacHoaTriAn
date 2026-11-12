"""
CẤU HÌNH HỆ THỐNG ROBOT ORC K2 BASIC GA25 MECANUM
Giải đấu "Sắc Hoa Tri Ân" - STEM THPT Ngô Quyền & 20/11
Chuẩn 100% theo tài liệu hướng dẫn Canva K2 GA25 OhStem & Linh kiện thực tế
"""

from constants import *

# 1. Chế độ dẫn động 4 bánh Mecanum đa hướng (Mecanum Holonomic Drive)
DRIVE_MODE = MODE_MECANUM
CHASSIS_WIDTH = 218      # Chiều rộng phủ bì qua 4 bánh Mecanum K3 (mm) - chuẩn khung 136mm, lọt 248mm mê cung
WHEEL_DIAMETER = 80      # Đường kính bánh xe Mecanum K3 OhStem (80mm)
WHEEL_CIRCUMFERENCE = 251.3  # Chu vi bánh xe pi * D (mm)

# 2. Phân bổ 4 cổng Động cơ OH-GA25-370 trên ORC Control Hub (Sơ đồ thực tế người dùng):
# - M2: Động cơ thường TRÁI TRƯỚC (Front-Left -> m1)
# - M1: Động cơ thường PHẢI TRƯỚC (Front-Right -> m2)
# - E1: Động cơ encoder TRÁI SAU (Rear-Left -> m3)
# - E2: Động cơ encoder PHẢI SAU (Rear-Right -> m4)
MOTOR_FL_PORT = M2       # Trước - Trái (M2, GA25 DC thường)
MOTOR_FR_PORT = M1       # Trước - Phải (M1, GA25 DC thường)
MOTOR_RL_PORT = E1       # Sau - Trái (E1, GA25 Hall Encoder 6P)
MOTOR_RR_PORT = E2       # Sau - Phải (E2, GA25 Hall Encoder 6P)

MOTOR_FL_REVERSED = True
MOTOR_FR_REVERSED = True
MOTOR_RL_REVERSED = True
MOTOR_RR_REVERSED = True

# Thông số chuẩn động cơ OH-GA25-370 6V 250RPM OhStem:
ENCODER_RPM = 250
ENCODER_PPR = 11
ENCODER_GEARS = 34
TICKS_PER_REV = ENCODER_PPR * ENCODER_GEARS * 4  # Quadrature decoding = 1496 xung/vòng

# 3. Động cơ Servo điều khiển cơ cấu cánh tay, cổ tay gập dọc và đầu kẹp 3 trụ hoa:
SERVO_LIFT_PORT  = S1    # Servo 1 (S1): Nâng/hạ cánh tay chữ H (MG996R)
SERVO_GRIP_PORT  = S2    # Servo 2 (S2): Đóng/mở hàm kẹp 3 trụ hoa Ø32mm
SERVO_WRIST_PORT = S3    # Servo 3 (S3): Gập dọc cụm kẹp 0°..90° (Pitch quanh trục ngang X)

LIFT_DOWN = 15           # Hạ sát sàn để đón/thả hoa tự đứng
LIFT_UP = 85             # Nâng cao di chuyển lướt qua mê cung
GRIP_OPEN = 30           # Mở ngàm đón 3 thân ống Ø32mm
GRIP_CLOSE = 105         # Kẹp chắc 3 thân ống hoa Ø32mm
WRIST_HORIZONTAL = 15    # Hạ ngang cụm kẹp (0°) để lùa và kẹp 3 trụ hoa
WRIST_TILT_CARRY = 30    # Hơi ngóc mũi kẹp lên 15° khi chở 3 hoa để chống quệt sàn
WRIST_VERTICAL_UP = 105  # Gập dựng đứng cụm kẹp lên 90° để tiết kiệm 105mm chiều dài trong mê cung!

# 4. Tốc độ di chuyển
SPEED_AUTO_MAZE = 60     # Tốc độ chạy tự động vượt mê cung
SPEED_STRAFE = 50        # Tốc độ trượt ngang (strafe) căn chỉnh hoa
SPEED_TELEOP_NORMAL = 95  # Tốc độ di chuyển bằng tay cầm Gamepad (Mặc định)
SPEED_TELEOP_SLOW = 60    # Tốc độ căn chỉnh chính xác (Precision Mode)
SPEED_TELEOP_TURBO = 100  # Tốc độ bứt tốc tối đa (Turbo Mode)

# 5. CẤU HÌNH TAY CẦM GAMEPAD 2 JOYSTICK (ARCADE DRIVE + MECANUM STRAFE):
# Chuẩn hóa điều khiển:
# - Joystick 1 (J1 - Cần Trái):
#     + Gạt LÊN / XUỐNG : Vy > 0 (Đi TIẾN) / Vy < 0 (Đi LÙI)
#     + Gạt TRÁI / PHẢI : Rot < 0 (Xoay TRÁI) / Rot > 0 (Xoay PHẢI) - Arcade Steering
#     + Gạt CHÉO        : Vừa tiến/lùi vừa bẻ lái cua xe mượt mà
# - Joystick 2 (J2 - Cần Phải):
#     + Gạt TRÁI / PHẢI : Vx < 0 (Trượt TRÁI DIR_SL) / Vx > 0 (Trượt PHẢI DIR_SR)
JOYSTICK_DEADBAND = 12.0     # Vùng chết 12% chống trôi cần khi buông tay

# Hệ số Trim từng bánh xe Mecanum (FL, FR, RL, RR):
# Thứ tự: FL (Trước-Trái, M2), FR (Trước-Phải, M1), RL (Sau-Trái, E1), RR (Sau-Phải, E2)
# Hướng dẫn hiệu chỉnh:
# - Nếu đi ngang bị xoay đầu lệch sang phải -> Giảm trim cặp bánh quay mạnh (ví dụ giảm FL hoặc RR xuống 0.92)
# - Nếu đi ngang bị xoay đầu lệch sang trái -> Giảm trim cặp bánh quay mạnh (ví dụ giảm FR hoặc RL xuống 0.92)
# - Nếu 2 bánh trước DC thường quay nhanh hơn 2 bánh sau Encoder -> Giảm trim FL, FR xuống (0.95, 0.95, 1.0, 1.0)
WHEEL_TRIM = (1.0, 1.0, 1.0, 1.0)

# Ngưỡng PWM tối thiểu thắng ma sát hộp số GA25 và con lăn Mecanum
MOTOR_MIN_PWM = 28

# Cực tính quay của 4 bánh Mecanum (FL, FR, RL, RR):
# Thứ tự: FL (Trước-Trái, M2), FR (Trước-Phải, M1), RL (Sau-Trái, E1), RR (Sau-Phải, E2)
# Đổi dấu phần tử nếu bánh đó quay ngược khi tiến.
# Hiện tại: 2 bánh trước (FL, FR) quay đúng chiều tiến (+1, +1),
#           2 bánh sau (RL, RR) quay ngược chiều khi tiến (-1, -1).
WHEEL_POLARITY = (1, 1, -1, -1)

