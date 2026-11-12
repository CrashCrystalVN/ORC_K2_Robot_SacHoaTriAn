"""
=============================================================================
BẢNG TÍNH TOÁN VÀ MÔ PHỎNG ĐỘNG HỌC 4 BÁNH MECANUM ROBOT ORC K2
Giải đấu "Sắc Hoa Tri Ân" - STEM THPT Ngô Quyền & 20/11
Phân tích 16 tổ hợp dấu động cơ (m1, m2, m3, m4) theo ảnh thực tế slide 7 Canva
=============================================================================
Quy ước tọa độ SAE / Robot chuẩn:
- Trục X: Dọc thân xe (Tiến +Fx / Lùi -Fx)
- Trục Y: Ngang thân xe (Trượt Phải +Fy / Trượt Trái -Fy)
- Mô-men xoay (Torque / Yaw): Quay ngược chiều KĐH (Trái) +Tau / Cùng chiều (Phải) -Tau

Kích thước cơ khí thực tế ORC K2 (từ full_assembly.scad & config.py):
- Khoảng cách từ tâm đến bánh xe theo trục ngang (Half-width): w = 90.0 mm
- Khoảng cách từ tâm đến trục bánh xe theo trục dọc (Half-wheelbase): L = 55.0 mm

Vị trí 4 bánh xe:
- FL (Trước Trái - M1): x = +L = +55 mm, y = -w = -90 mm
- FR (Trước Phải - M2): x = +L = +55 mm, y = +w = +90 mm
- RL (Sau Trái   - E1): x = -L = -55 mm, y = -w = -90 mm
- RR (Sau Phải   - E2): x = -L = -55 mm, y = +w = +90 mm
=============================================================================
"""

import itertools
import numpy as np

# Thông số hình học xe ORC K2
L = 55.0  # mm (Nửa chiều dài cơ sở wheelbase / 2 = (142 - 32) / 2)
w = 90.0  # mm (Nửa khoảng cách tâm 2 bánh xe ngang track_width / 2)

# Vị trí tọa độ (x_i, y_i) của 4 bánh:
# x: trục dọc (Tiến +), y: trục ngang (Phải +)
pos = [
    np.array([+L, -w]),  # FL (M1)
    np.array([+L, +w]),  # FR (M2)
    np.array([-L, -w]),  # RL (E1)
    np.array([-L, +w]),  # RR (E2)
]

# Hướng lực sinh ra từ mặt sàn lên từng bánh khi động cơ quay TIẾN (+1):
# Dựa trên ảnh thực tế slide 7 Canva:
# Mặt trên con lăn xếp hình chữ X:
# - FL mặt trên xiên \, tiếp xúc đất xiên / -> lực F = (Fx=+1, Fy=-1) [Tiến & Đẩy Trái]
# - FR mặt trên xiên /, tiếp xúc đất xiên \ -> lực F = (Fx=+1, Fy=+1) [Tiến & Đẩy Phải]
# - RL mặt trên xiên /, tiếp xúc đất xiên \ -> lực F = (Fx=+1, Fy=+1) [Tiến & Đẩy Phải]
# - RR mặt trên xiên \, tiếp xúc đất xiên / -> lực F = (Fx=+1, Fy=-1) [Tiến & Đẩy Trái]
F_forward_P1 = [
    np.array([1.0, -1.0]),  # FL: Fx=+1 (Tiến), Fy=-1 (Trái)
    np.array([1.0,  1.0]),  # FR: Fx=+1 (Tiến), Fy=+1 (Phải)
    np.array([1.0,  1.0]),  # RL: Fx=+1 (Tiến), Fy=+1 (Phải)
    np.array([1.0, -1.0]),  # RR: Fx=+1 (Tiến), Fy=-1 (Trái)
]

def simulate_16_combinations(F_forward, config_name):
    print(f"\n{'='*75}")
    print(f"MÔ PHỎNG 16 TỔ HỢP DẤU - CẤU HÌNH: {config_name}")
    print(f"{'='*75}")
    print(f"{'STT':>3} | {'m1(FL)':>6} {'m2(FR)':>6} {'m3(RL)':>6} {'m4(RR)':>6} | {'Fx (Tiến)':>9} {'Fy (Ngang)':>10} {'Torque (Nmm)':>12} | {'Hành vi xe'}")
    print("-" * 75)
    
    stt = 1
    best_strafe = []
    
    for signs in itertools.product([1, -1], repeat=4):
        m1, m2, m3, m4 = signs
        m = [m1, m2, m3, m4]
        
        # Lực từng bánh
        f_wheels = [F_forward[i] * m[i] for i in range(4)]
        
        # Tổng hợp lực Fx, Fy
        total_Fx = sum(f[0] for f in f_wheels)
        total_Fy = sum(f[1] for f in f_wheels)
        
        # Tổng mô-men xoay quanh tâm: Tau = x * Fy - y * Fx
        total_Tau = sum(pos[i][0] * f_wheels[i][1] - pos[i][1] * f_wheels[i][0] for i in range(4))
        
        # Phân tích hành vi
        actions = []
        if abs(total_Fx) > 0.1:
            actions.append("TIẾN" if total_Fx > 0 else "LÙI")
        if abs(total_Fy) > 0.1:
            actions.append("TRƯỢT PHẢI" if total_Fy > 0 else "TRƯỢT TRÁI")
        if abs(total_Tau) > 0.1:
            actions.append("XOAY TRÁI (CCW)" if total_Tau > 0 else "XOAY PHẢI (CW)")
        if not actions:
            actions.append("ĐỨNG YÊN")
        action_str = " + ".join(actions)
        
        # Kiểm tra điều kiện đi ngang lý tưởng: Fx = 0, Torque = 0, |Fy| cực đại
        is_ideal_strafe = (abs(total_Fx) < 1e-4 and abs(total_Tau) < 1e-4 and abs(total_Fy) >= 3.9)
        marker = " <== [CHUẨN]" if is_ideal_strafe else ""
        
        print(f"{stt:3d} | {m1:6d} {m2:6d} {m3:6d} {m4:6d} | {total_Fx:9.1f} {total_Fy:10.1f} {total_Tau:12.1f} | {action_str}{marker}")
        
        if is_ideal_strafe:
            best_strafe.append((signs, total_Fx, total_Fy, total_Tau, action_str))
        stt += 1
        
    print("\nKẾT QUẢ ĐI NGANG THUẦN TÚY (Fx=0, Torque=0, |Fy|=Max=4.0):")
    for signs, fx, fy, tau, act in best_strafe:
        dir_name = "DIR_SR (Trượt Phải)" if fy > 0 else "DIR_SL (Trượt Trái)"
        print(f"-> {dir_name}: (m1={signs[0]:+d}, m2={signs[1]:+d}, m3={signs[2]:+d}, m4={signs[3]:+d})")
        print(f"   Fx = {fx:.1f}, Fy = {fy:+.1f}, Torque = {tau:.1f}")

if __name__ == '__main__':
    simulate_16_combinations(F_forward_P1, "CHUẨN SLIDE 7 CANVA OHSTEM (Mặt trên 'X' -> Tiếp xúc đất 'O')")
