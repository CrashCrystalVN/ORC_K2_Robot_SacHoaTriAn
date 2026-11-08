"""
CHIẾN THUẬT & LỘ TRÌNH GIẢI MÊ CUNG TỰ ĐỘNG (GIAI ĐOẠN 1)
Áp dụng Dead-Reckoning kết hợp IMU MPU6050 (Closed-Loop Gyro Heading)
"""

from constants import *
from utility import *
import config

async def run_maze_left(robot, servo_lift, servo_grip):
    """
    Lộ trình cho đội sân bên TRÁI:
    Từ Ô Đỏ (giáp vách giữa, đáy sân) -> Vượt mê cung -> Ô Xanh Lá (Góc ngoài bên trái)
    """
    print(">>> [AUTO] Bắt đầu giải mê cung: SÂN TRÁI <<<")
    
    # 0. Thu gọn tay gắp lọt khung 20x20x50cm theo thể lệ
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=120)
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=120)
    await asleep_ms(300)
    
    robot.speed(config.SPEED_AUTO_MAZE, min_speed=35)
    
    # Đoạn 1: Rời Ô Đỏ, tiến thẳng vào hành lang ngang đầu tiên (25cm)
    await robot.forward_for(25, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 2: Rẽ trái 90 độ đi về phía mép ngoài sân
    await robot.turn_left_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(62, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 3: Rẽ phải 90 độ (hướng Bắc lên trên)
    await robot.turn_right_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(50, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 4: Uốn qua vách ziczac
    await robot.turn_left_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(38, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 5: Rẽ phải hướng thẳng vào hành lang ra Ô Xanh lá
    await robot.turn_right_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(75, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 6: Tiến trọn vẹn vào Ô XANH LÁ (Vùng Chuyển Tiếp)
    await robot.turn_left_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(30, unit=CM, then=STOP)
    
    robot.stop()
    print(">>> [AUTO] ĐÃ VÀO Ô XANH LÁ! HOÀN THÀNH GIAI ĐOẠN 1 (+40 ĐIỂM) <<<")


async def run_maze_right(robot, servo_lift, servo_grip):
    """
    Lộ trình cho đội sân bên PHẢI (Đối xứng trục với sân trái)
    """
    print(">>> [AUTO] Bắt đầu giải mê cung: SÂN PHẢI <<<")
    
    await servo_lift.run_angle(angle=config.LIFT_UP, speed=120)
    await servo_grip.run_angle(angle=config.GRIP_CLOSE, speed=120)
    await asleep_ms(300)
    
    robot.speed(config.SPEED_AUTO_MAZE, min_speed=35)
    
    # Đoạn 1: Rời Ô Đỏ
    await robot.forward_for(25, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 2: Rẽ phải 90 độ
    await robot.turn_right_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(62, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 3: Rẽ trái 90 độ (hướng Bắc)
    await robot.turn_left_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(50, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 4: Ziczac
    await robot.turn_right_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(38, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 5: Hướng vào hành lang ra
    await robot.turn_left_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(75, unit=CM, then=STOP)
    await asleep_ms(150)
    
    # Đoạn 6: Vào Ô Xanh lá bên phải
    await robot.turn_right_for(90, unit=DEGREE, then=STOP)
    await asleep_ms(150)
    await robot.forward_for(30, unit=CM, then=STOP)
    
    robot.stop()
    print(">>> [AUTO] ĐÃ VÀO Ô XANH LÁ BÊN PHẢI! HOÀN THÀNH GIAI ĐOẠN 1 (+40 ĐIỂM) <<<")

