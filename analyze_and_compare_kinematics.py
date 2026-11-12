"""
Analyze Support Polygon, Center of Gravity (CoG), and Kinematic Symmetry
Comparison between Zigzag V9.1 Base vs Balanced Omni Base V10.0
"""

import numpy as np

# ====================================================================
# 1. WHEEL AND CHASSIS COORDINATES
# ====================================================================

# Wheel contact points (X, Y) on the ground (Z = 0):
# Note: X is half of total track width to wheel contact center
# For Omni 58mm wheel with hex coupler:
# Zigzag Base V9.1 (CHASSIS_W = 76mm, BOSS_OUT = 4mm, COUPLER_LEN = 15mm, WHEEL_W = 16mm):
# Track half-width = 38 + 4 + 15 + 8 = 65.0 mm
WHEELS_ZIGZAG = {
    "RL": np.array([-65.0, 24.0]),
    "RR": np.array([ 65.0, 54.0]),
    "FL": np.array([-65.0, 86.0]),
    "FR": np.array([ 65.0, 142.0])
}

# Balanced Omni Base V10.0 (CHASSIS_W = 136mm, WALL_T = 4mm, motor flange at ±64mm, outer boss ±68mm):
# Wheel contact center: X = ± (68 + 3 + 8) = ± 79.0 mm (Omni 58mm track half-width)
WHEELS_BALANCED = {
    "RL": np.array([-79.0, 24.0]),
    "RR": np.array([ 79.0, 24.0]),
    "FL": np.array([-79.0, 142.0]),
    "FR": np.array([ 79.0, 142.0])
}

# Key component positions:
# Lift tower: Y = 110.5 .. 160.25 mm (Mass ~ 180g)
# Gripper arm + MG996R servo + flower payload: Y = 150 .. 220 mm (Mass ~ 250g)
# Battery 2S2P 18650 on Deck 1: Y = 38 .. 100 mm (Mass ~ 200g)
# Base chassis + 4x GA25 motors: (Chassis ~ 130g, Motors ~ 4x 85g = 340g)

# Estimated Center of Gravity (CoG) in various operational states:
# 1. Neutral / Idle state (Arm retracted)
COG_NEUTRAL = np.array([0.0, 92.0])

# 2. Extending gripper forward to pick flower (Arm reaching out at Y=200mm)
COG_EXTENDED = np.array([0.0, 128.0])

# 3. Dynamic braking / Deceleration while carrying flower
# Inertial forward force tilts effective CoG vector forward
COG_BRAKING = np.array([-15.0, 138.0]) # If steering slightly or asymmetrical braking

def point_in_poly(pt, poly):
    """Ray casting algorithm to test if point is inside polygon"""
    x, y = pt
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def dist_point_to_line(pt, p1, p2):
    """Perpendicular signed distance from point to line segment p1-p2"""
    # Vector p1 -> p2
    v = p2 - p1
    # Normal vector pointing outwards (right hand rule)
    norm = np.array([v[1], -v[0]])
    norm = norm / np.linalg.norm(norm)
    # Vector p1 -> pt
    w = pt - p1
    return np.dot(w, norm)

def min_stability_margin(pt, poly):
    """
    Minimum distance from CoG to any boundary of the support polygon.
    Positive = inside polygon (stable).
    Negative = outside polygon (TIPPING / COLLAPSE!).
    """
    n = len(poly)
    margins = []
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        # Line from p1 to p2
        d = dist_point_to_line(pt, p1, p2)
        margins.append(d)
    return min(margins), margins

# ====================================================================
# 2. CALCULATE AND PRINT COMPARISON METRICS
# ====================================================================
poly_zigzag = [WHEELS_ZIGZAG["RL"], WHEELS_ZIGZAG["RR"], WHEELS_ZIGZAG["FR"], WHEELS_ZIGZAG["FL"]]
poly_balanced = [WHEELS_BALANCED["RL"], WHEELS_BALANCED["RR"], WHEELS_BALANCED["FR"], WHEELS_BALANCED["FL"]]

print("="*75)
print("PHÂN TÍCH ĐỘNG HỌC & CƠ HỌC ĐA GIÁC ĐỠ (SUPPORT POLYGON STABILITY)")
print("SO SÁNH: BẢN ZIGZAG V9.1 vs BẢN CÂN BẰNG ĐỐI XỨNG BALANCED OMNI V10.0")
print("="*75)

states = [
    ("1. Trạng thái Nghỉ / Cánh tay thu gọn (Retracted CoG)", COG_NEUTRAL),
    ("2. Trạng thái Vươn kẹp hoa về phía trước (Extended CoG)", COG_EXTENDED),
    ("3. Trạng thái Phanh gấp khi đang gắp hoa (Braking Dynamic CoG)", COG_BRAKING),
]

for name, cog in states:
    print(f"\n>>> {name} [CoG = ({cog[0]:.1f}, {cog[1]:.1f}) mm]:")
    
    # Zigzag evaluation
    inside_zz = point_in_poly(cog, poly_zigzag)
    margin_zz, all_m_zz = min_stability_margin(cog, poly_zigzag)
    
    # Check critical tipping line: from FL (-65, 86) to FR (65, 142)
    # Line FL -> FR
    v_front = WHEELS_ZIGZAG["FR"] - WHEELS_ZIGZAG["FL"] # (130, 56)
    # The front edge of support polygon is slanted at angle:
    slant_deg = np.degrees(np.arctan2(v_front[1], v_front[0]))
    
    print(f"   [ZIGZAG V9.1]:")
    print(f"     - Độ nghiêng đường đỡ trước (FL -> FR): {slant_deg:.1f}° (BỊ MÉO XUYÊN TÂM!)")
    print(f"     - Mép đỡ góc trước-trái: Chỉ có bánh ở Y=86mm, thiếu hụt tới {168.5 - 86:.1f}mm phía trước!")
    print(f"     - Trạng thái thăng bằng: {'AN TOÀN' if inside_zz else 'NGUY HIỂM / CHÚI LẬT (TIPPED)!'}")
    print(f"     - Biên độ ổn định (Margin): {margin_zz:.1f} mm")
    if margin_zz < 15.0:
        print(f"     -> CẢNH BÁO: Robot rất dễ bập bênh, chúi đầu về góc trước-trái khi phanh hoặc vươn gắp!")

    # Balanced evaluation
    inside_bal = point_in_poly(cog, poly_balanced)
    margin_bal, all_m_bal = min_stability_margin(cog, poly_balanced)
    print(f"   [BALANCED OMNI V10.0]:")
    print(f"     - Độ nghiêng đường đỡ trước (FL -> FR): 0.0° (HOÀN TOÀN SONG SONG TRỤC X!)")
    print(f"     - Mép đỡ 2 góc trước: Cả 2 bánh đều tại Y=142.0mm, chống đỡ trọn vẹn tháp nâng!")
    print(f"     - Trạng thái thăng bằng: {'VỮNG VÀNG TUYỆT ĐỐI' if inside_bal else 'LẬT'}")
    print(f"     - Biên độ ổn định (Margin): {margin_bal:.1f} mm (Tăng +{margin_bal - margin_zz:.1f} mm!)")

# Kinematics drift analysis
print("\n" + "="*75)
print("PHÂN TÍCH ĐỘNG HỌC OMNI / MECANUM 4 BÁNH:")
print("="*75)
print("1. BẢN ZIGZAG V9.1:")
print("   - Trục bánh không đồng hàng: Y_FL=86, Y_FR=142, Y_RL=24, Y_RR=54 mm.")
print("   - Khoảng cách đến trọng tâm Ly của mỗi bánh hoàn toàn khác nhau:")
y_mid_zz = (24 + 54 + 86 + 142) / 4.0 # 76.5mm
print(f"     Ly_FL = {86 - y_mid_zz:+.1f} mm | Ly_FR = {142 - y_mid_zz:+.1f} mm")
print(f"     Ly_RL = {24 - y_mid_zz:+.1f} mm | Ly_RR = {54 - y_mid_zz:+.1f} mm")
print("   - HỆ QUẢ: Khi xe chạy thẳng (Vy > 0), tổng mô-men quay Yaw = Sum(Wx * Ly) != 0.")
print("     -> Xe bị NHAO LÁI LỆCH TÂM (Kinematic Yaw Drift), chạy lệch vệt line!")

print("\n2. BẢN BALANCED OMNI V10.0:")
print("   - Trục bánh đối xứng tuyệt đối: Y_FL = Y_FR = 142.0 mm, Y_RL = Y_RR = 24.0 mm.")
y_mid_bal = (24 + 142) / 2.0 # 83.0 mm
print(f"     Ly_FL = Ly_FR = {142 - y_mid_bal:+.1f} mm")
print(f"     Ly_RL = Ly_RR = {24 - y_mid_bal:+.1f} mm")
print("   - HỆ QUẢ: Cánh tay đòn đối xứng hoàn hảo 100%.")
print("     -> Mô-men triệt tiêu nhau hoàn toàn, xe chạy thẳng tắp, bám line chuẩn xác!")
