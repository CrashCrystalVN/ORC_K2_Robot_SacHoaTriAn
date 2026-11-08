"""
CẤU HÌNH HỆ THỐNG ROBOT ORC K2 BASIC GA25 MECANUM
Giải đấu "Sắc Hoa Tri Ân" - STEM THPT Ngô Quyền & 20/11
Chuẩn 100% theo tài liệu hướng dẫn Canva K2 GA25 OhStem & Linh kiện thực tế
"""

from constants import *

# 1. Chế độ dẫn động 4 bánh Mecanum đa hướng (Mecanum Holonomic Drive)
DRIVE_MODE = "MECANUM"
CHASSIS_WIDTH = 218      # Chiều rộng phủ bì qua 4 bánh Mecanum K3 (mm) - chuẩn khung 136mm, lọt 248mm mê cung
WHEEL_DIAMETER = 80      # Đường kính bánh xe Mecanum K3 OhStem (80mm)
WHEEL_CIRCUMFERENCE = 251.3  # Chu vi bánh xe pi * D (mm)

# 2. Phân bổ 4 cổng Động cơ OH-GA25-370 trên ORC Control Hub (Chuẩn Slide 30 Canva):
# - Cầu trước: 2 Động cơ GA25 DC 6V 250RPM thường (Cổng M1, M2)
# - Cầu sau: 2 Động cơ GA25 DC 6V 250RPM tích hợp Hall Encoder (Cổng E1, E2)
MOTOR_FL_PORT = M1       # Trước - Trái (GA25 DC thường)
MOTOR_FR_PORT = M2       # Trước - Phải (GA25 DC thường)
MOTOR_RL_PORT = E1       # Sau - Trái (GA25 Hall Encoder 6P)
MOTOR_RR_PORT = E2       # Sau - Phải (GA25 Hall Encoder 6P)

MOTOR_FL_REVERSED = False
MOTOR_FR_REVERSED = True
MOTOR_RL_REVERSED = False
MOTOR_RR_REVERSED = True

# Thông số chuẩn động cơ OH-GA25-370 6V 250RPM OhStem:
ENCODER_RPM = 250
ENCODER_PPR = 11
ENCODER_GEARS = 34
TICKS_PER_REV = ENCODER_PPR * ENCODER_GEARS * 4  # Quadrature decoding = 1496 xung/vòng

# 3. Động cơ Servo điều khiển cơ cấu cánh tay, cổ tay gập dọc và đầu kẹp 3 trụ hoa:
SERVO_LIFT_PORT  = S1    # Servo 1 (S1): Nâng/hạ cánh tay chữ H
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
SPEED_TELEOP_NORMAL = 75  # Tốc độ di chuyển bằng tay cầm Gamepad
