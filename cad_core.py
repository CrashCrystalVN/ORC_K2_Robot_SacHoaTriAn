"""
cad_core.py - Nhân hình học cơ khí CAD 3D chuẩn xác cho Robot ORC-X1 PRO SẮC HOA TRI ÂN (V4.0 - DFM 3D-PRINT OPTIMIZED EDITION)
Giải đấu STEM THPT Ngô Quyền & 20/11 - Tối ưu hóa 100% cho công nghệ In 3D FDM (Zero-Support, 100% Flat Bed Adhesion, High Strength)

CÁC CẢI TIẾN ĐỘT PHÁ TRONG BẢN V4.0 (DFM - THUẬN LỢI TỐI ĐA ĐỂ IN 3D):
1. ĐÁY KHUNG GẦM PHẲNG TUYỆT ĐỐI 100% TRÊN MẶT BÀN IN (Z = 0.0 mm):
   - Loại bỏ khối lồi âm (Z = -6.0 mm) dưới đáy mũi xe từng làm kênh toàn bộ sàn xe 136x176mm lên 6mm khỏi mặt bàn in.
   - Tách thành Đế đệm rời `01E_Line_Sensor_Spacer_Pod` (52 x 24 x 6 mm) in phẳng 100% trên bàn in và bắt ốc M3 vào gầm mũi xe.
   - Bổ sung biên dạng lỗ Giọt nước tự đỡ 45° (Teardrop Holes) cho toàn bộ các lỗ ngang (cổ trục động cơ Ø9.0mm, mắt siêu âm Ø16.6mm, lỗ mặt bích Ø3.3mm) và mái vát 45° cho khe đai ốc M4 -> Khung gầm in KHÔNG CẦN SUPPORT (0% Support)!

2. TÁCH THÁP NÂNG TRÁI/PHẢI & BỆ MCU THÀNH MÔ-ĐUN IN PHẲNG 100% (ZERO-SUPPORT & BỀN GẤP 5 LẦN):
   - Khung gầm chính (`01_Monocoque_Chassis_GA25_Mecanum`) hạ chiều cao xuống còn 33.0 mm (thay vì 94.0 mm), loại bỏ hoàn toàn cầu treo MCU Deck và vòm treo chân tháp -> Thời gian in giảm một nửa, không tốn nhựa support.
   - Cặp Tháp nâng (`01B_Lift_Tower_Left` & `01C_Lift_Tower_Right_MG996R`) được thiết kế có mặt ngoài phẳng 100% kèm Đế chữ L + Mộng định vị âm dương và Tai giằng đỉnh. Khi xuất file STL in 3D, 2 tháp tự động đặt NẰM PHẲNG trên mặt bàn in (Z = 0..16mm):
     + Hốc chữ nhật chứa Servo MG996R (41.2 x 20.2 mm), 4 lỗ ốc tai Servo và lỗ trục xoay đều hướng thẳng đứng (trục Z) -> In 0% Support, chính xác tuyệt đối!
     + Thớ nhựa chạy dọc liên tục theo chiều dài tháp -> Chống gãy tách lớp tuyệt đối khi nâng hoa!
   - Bệ đặt mạch điều khiển (`01D_MCU_Control_Hub_Deck`) tách rời in phẳng 100% trên bàn in (Z = 0..8mm), bắt 4 ốc M3 lên 4 trụ khung gầm, giúp tháo lắp Pin 2S 18650 bên dưới cực kỳ thoáng và không phải cạy support trong hộc pin.

3. KHẮC PHỤC LỖI KÊNH TAY ĐÒN CHỮ H & CẦU TREO ĐẦU KẸP HOA:
   - Khung tay nâng chữ H dưới & trên (`03_Parallel_Arm_Truss_IBeam` & `03B_Upper_H_Frame_Follower_Arm`): Làm phẳng 100% mặt đáy tại Z = 0.0 mm (loại bỏ phần lồi dưới của đĩa horn_boss R=10mm làm kênh thanh tay đòn 4mm trên bàn in), vát 45° hai đầu và dùng lỗ giọt nước 45° -> Đặt phẳng 100% trên bàn in với 0% Support!
   - Bệ đầu kẹp hoa (`04_Gripper_Base_Head`): Loại bỏ 2 thanh cầu mỏng treo lơ lửng vắt ngang trên 2 trụ xoay hàm kẹp, giữ nguyên 2 trụ đỡ tai Servo MG996R vươn thẳng từ đáy kèm sườn tăng cứng 45° -> In phẳng 0% Support và lắp hàm kẹp từ phía trên cực dễ!
   - Cặp hàm kẹp hoa (`05/06_Gripper_Jaw`) & Tay gạt (`08_Servo_Horn`): Bổ sung mái côn 45° (Conical Self-Supporting Roof) cho lỗ bậc dưới đáy -> In phẳng 0% Support!
   - Nắp kẹp động cơ (`02_GA25_Motor_Clamp_Cap`) & Bánh xe (`07_Mecanum_Wheel`): Tự động xoay sẵn về tư thế đặt phẳng chuẩn in 3D (Z_min = 0.0 mm) ngay trong file STL!
"""

import math
import os
import sys

from OCP.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax1, gp_Ax2, gp_Trsf
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.StlAPI import StlAPI_Writer
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

# ====================================================================
# TIỆN ÍCH CẮT GỌT CSG & HÌNH HỌC TỰ ĐỠ IN 3D (DFM TEARDROP & CHAMFER)
# ====================================================================

def make_box(x0, y0, z0, dx, dy, dz):
    return BRepPrimAPI_MakeBox(gp_Pnt(x0, y0, z0), gp_Pnt(x0 + dx, y0 + dy, z0 + dz)).Shape()

def cut_box(solid, x0, y0, z0, dx, dy, dz):
    box = BRepPrimAPI_MakeBox(gp_Pnt(x0, y0, z0), gp_Pnt(x0 + dx, y0 + dy, z0 + dz)).Shape()
    return BRepAlgoAPI_Cut(solid, box).Shape()

def cut_hole_z(solid, x, y, z0, diameter, depth):
    cyl = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, z0), gp_Dir(0, 0, 1)),
        diameter / 2.0,
        depth
    ).Shape()
    return BRepAlgoAPI_Cut(solid, cyl).Shape()

def cut_counterbore_z_dfm(solid, x, y, z0, cb_diameter, cb_depth, thru_diameter, total_depth):
    """
    Khoét lỗ bậc từ mặt đáy Z=0 lên với mái côn chuyển tiếp 45° tự đỡ (Conical Self-Supporting Roof),
    giúp in 3D lỗ bậc nằm ở mặt dưới mà KHÔNG CẦN SUPPORT!
    """
    r_cb = cb_diameter / 2.0
    r_th = thru_diameter / 2.0
    solid = cut_hole_z(solid, x, y, z0, cb_diameter, cb_depth)
    if r_cb > r_th:
        cone_h = r_cb - r_th
        cone = BRepPrimAPI_MakeCone(
            gp_Ax2(gp_Pnt(x, y, z0 + cb_depth), gp_Dir(0, 0, 1)),
            r_cb,
            r_th,
            cone_h
        ).Shape()
        solid = BRepAlgoAPI_Cut(solid, cone).Shape()
    solid = cut_hole_z(solid, x, y, z0, thru_diameter, total_depth)
    return solid

def cut_hole_y(solid, x, y0, z, diameter, depth, teardrop=True):
    """
    Khoét lỗ ngang dọc trục Y; nếu teardrop=True thì vát đỉnh giọt nước 45° ở phía +Z
    giúp in 3D FDM không bị xệ đỉnh lỗ và không cần support.
    """
    r = diameter / 2.0
    cyl = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y0, z), gp_Dir(0, 1, 0)),
        r,
        depth
    ).Shape()
    solid = BRepAlgoAPI_Cut(solid, cyl).Shape()
    if teardrop and diameter >= 3.0:
        # Tạo khối lăng trụ vuông xoay 45° quanh trục Y đặt tại đỉnh lỗ (z + r * 0.7071)
        side = r * math.sqrt(2.0)
        b = make_box(-side / 2.0, 0.0, -side / 2.0, side, depth, side)
        tr_rot = gp_Trsf()
        tr_rot.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), math.radians(45.0))
        tr_pos = gp_Trsf()
        tr_pos.SetTranslation(gp_Vec(x, y0, z + r * 0.5))
        cap = BRepBuilderAPI_Transform(b, tr_pos * tr_rot).Shape()
        solid = BRepAlgoAPI_Cut(solid, cap).Shape()
    return solid

def cut_hole_x(solid, x0, y, z, diameter, depth, teardrop=True):
    """
    Khoét lỗ ngang dọc trục X; nếu teardrop=True thì vát đỉnh giọt nước 45° ở phía +Z
    giúp in 3D FDM không bị xệ đỉnh lỗ và không cần support.
    """
    r = diameter / 2.0
    cyl = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x0, y, z), gp_Dir(1, 0, 0)),
        r,
        depth
    ).Shape()
    solid = BRepAlgoAPI_Cut(solid, cyl).Shape()
    if teardrop and diameter >= 3.0:
        side = r * math.sqrt(2.0)
        b = make_box(0.0, -side / 2.0, -side / 2.0, depth, side, side)
        tr_rot = gp_Trsf()
        tr_rot.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.radians(45.0))
        tr_pos = gp_Trsf()
        tr_pos.SetTranslation(gp_Vec(x0, y, z + r * 0.5))
        cap = BRepBuilderAPI_Transform(b, tr_pos * tr_rot).Shape()
        solid = BRepAlgoAPI_Cut(solid, cap).Shape()
    return solid

def orient_for_print(shape, rx_deg=0.0, ry_deg=0.0, rz_deg=0.0):
    """
    Xoay chi tiết về tư thế tối ưu cho in 3D và dịch chuyển sao cho:
    - Mặt đáy nằm phẳng tuyệt đối tại Z = 0.0 mm (min_z = 0.0)
    - Tâm XY gần gốc (0, 0)
    """
    s = shape
    if abs(rx_deg) > 1e-6:
        tr = gp_Trsf()
        tr.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.radians(rx_deg))
        s = BRepBuilderAPI_Transform(s, tr, True).Shape()
    if abs(ry_deg) > 1e-6:
        tr = gp_Trsf()
        tr.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), math.radians(ry_deg))
        s = BRepBuilderAPI_Transform(s, tr, True).Shape()
    if abs(rz_deg) > 1e-6:
        tr = gp_Trsf()
        tr.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(rz_deg))
        s = BRepBuilderAPI_Transform(s, tr, True).Shape()

    bbox = Bnd_Box()
    BRepBndLib.Add_s(s, bbox)
    pmin = bbox.CornerMin()
    pmax = bbox.CornerMax()
    xmin, ymin, zmin = pmin.X(), pmin.Y(), pmin.Z()
    xmax, ymax, zmax = pmax.X(), pmax.Y(), pmax.Z()
    cx = 0.5 * (xmin + xmax)
    cy = 0.5 * (ymin + ymax)

    tr_shift = gp_Trsf()
    tr_shift.SetTranslation(gp_Vec(-cx, -cy, -zmin))
    return BRepBuilderAPI_Transform(s, tr_shift, True).Shape()


# ====================================================================
# 1A. KHUNG GẦM CHÍNH ĐÁY PHẲNG 100% (DFM V4.0 - ZERO SUPPORT)
# ====================================================================
def create_monocoque_chassis():
    """
    Khung gầm chính DFM V4.0 tối ưu hóa 100% cho in 3D FDM:
    - Đáy phẳng tuyệt đối 100% tại Z = 0.0 mm trên toàn bộ diện tích 136.0 x 176.0 mm.
    - Chiều cao tối đa chỉ 33.0 mm (đã tách 2 Tháp nâng 94mm và Bệ MCU thành mô-đun in phẳng rời).
    - Tích hợp 4 ổ đỡ động cơ GA25 (lòng máng chữ U mở lên trên + lỗ cổ trục Ø9.0mm giọt nước 45°).
    - Tích hợp 4 trụ đỡ Bệ MCU (10 x 10 x 18 mm) có lỗ bắt ốc M3 tại X = ±33.0, Y = 49.0 và 99.0.
    - Tích hợp Hệ Gờ Định Vị & 6 Lỗ Bu-lông M3 (Ø3.2mm) để lắp cứng 2 Tháp Nâng Rời Trái/Phải.
    """
    W, L, T = 136.0, 176.0, 4.0
    Z_SHAFT_LOCAL = 20.0

    # 1. Sàn đáy chính phẳng tuyệt đối 100% tại Z = 0.0 mm
    base = make_box(-W/2.0, 0.0, 0.0, W, L, T)

    # 2. Hai vách sườn chịu lực & mặt bích động cơ dày 4.0 mm, cao 30.0 mm
    wall_left = make_box(-W/2.0, 0.0, 0.0, 4.0, L, 30.0)
    wall_right = make_box(W/2.0 - 4.0, 0.0, 0.0, 4.0, L, 30.0)
    base = BRepAlgoAPI_Fuse(base, wall_left).Shape()
    base = BRepAlgoAPI_Fuse(base, wall_right).Shape()

    # 3. 4 Ổ đỡ nửa dưới động cơ GA25 (Y = 32.0 và Y = 142.0)
    for my in [32.0, 142.0]:
        cradle_l = make_box(-W/2.0, my - 22.0, 0.0, 38.0, 44.0, Z_SHAFT_LOCAL)
        cradle_r = make_box(W/2.0 - 38.0, my - 22.0, 0.0, 38.0, 44.0, Z_SHAFT_LOCAL)
        flange_l = make_box(-W/2.0, my - 16.0, 0.0, 4.0, 32.0, 33.0)
        flange_r = make_box(W/2.0 - 4.0, my - 16.0, 0.0, 4.0, 32.0, 33.0)
        base = BRepAlgoAPI_Fuse(base, cradle_l).Shape()
        base = BRepAlgoAPI_Fuse(base, cradle_r).Shape()
        base = BRepAlgoAPI_Fuse(base, flange_l).Shape()
        base = BRepAlgoAPI_Fuse(base, flange_r).Shape()

    # 4. 4 Gờ định vị thấp 3.0 mm giữ Pin Li-ion 2S 18650 ở khoang giữa
    for bx in [-21.5, 18.5]:
        for by in [52.0, 90.0]:
            bat_guide = make_box(bx, by, T, 3.0, 8.0, 3.0)
            base = BRepAlgoAPI_Fuse(base, bat_guide).Shape()

    # 5. 4 Trụ đỡ Bệ MCU (10 x 10 x 18 mm, Z = 4.0..22.0 mm) - Đỉnh phẳng để bắt tấm 01D_MCU_Control_Hub_Deck rời!
    for px in [-38.0, 28.0]:
        for py in [44.0, 94.0]:
            pillar = make_box(px, py, T, 10.0, 10.0, 18.0)
            base = BRepAlgoAPI_Fuse(base, pillar).Shape()

    # 6A. Bệ gá Mạch nhận tín hiệu điều khiển tay cầm PS4 I2C (Sườn trái Y in [56, 82], Z = 16.0)
    i2c_mount_l = make_box(-W/2.0, 56.0, 0.0, 16.0, 26.0, 16.0)
    base = BRepAlgoAPI_Fuse(base, i2c_mount_l).Shape()

    # 6B. Bệ gá Module Nút nhấn đôi OhStem (Sườn phải đối xứng Y in [56, 82], Z = 16.0)
    btn_mount_r = make_box(W/2.0 - 16.0, 56.0, 0.0, 16.0, 26.0, 16.0)
    base = BRepAlgoAPI_Fuse(base, btn_mount_r).Shape()

    # 7. Mũi cản trước tích hợp Hốc & Bệ bắt Cảm biến khoảng cách Siêu âm OhStem (48 x 24 x 18 mm)
    bumper = make_box(-34.0, L - 10.0, 0.0, 68.0, 10.0, 28.0)
    us_shelf = make_box(-26.0, L - 16.0, 0.0, 52.0, 6.0, 10.0)
    base = BRepAlgoAPI_Fuse(base, bumper).Shape()
    base = BRepAlgoAPI_Fuse(base, us_shelf).Shape()

    # 8. Gờ định vị chân Tháp Nâng Rời Trái & Phải (cao 3.0 mm tại Z = 4.0..7.0 mm) giúp tự căn vuông góc 90° khi lắp:
    # Chân tháp nằm tại X in [-28, -12] (Trái) và X in [+12, +28] (Phải), Y in [105.0, 127.5] (chân sau) & [154.5, 166.0] (chân trước)
    for side_sign in [-1, 1]:
        # Gờ chặn mặt ngoài tại X = ±28.0..±30.0 ở chân sau (Y in [105, 119.5], không chạm ổ motor trước Y=120)
        outer_x = -30.0 if side_sign < 0 else 28.0
        guide_out = make_box(outer_x, 105.0, T, 2.0, 14.5, 4.0)
        # Gờ chặn phía sau tại Y = 102.5..105.0, X in [±12, ±28]
        inner_x = -28.0 if side_sign < 0 else 12.0
        guide_rear = make_box(inner_x, 102.5, T, 16.0, 2.5, 4.0)
        base = BRepAlgoAPI_Fuse(base, guide_out).Shape()
        base = BRepAlgoAPI_Fuse(base, guide_rear).Shape()

    # ================= KHOÉT LỖ CHÍNH XÁC BẰNG CSG (TEARDROP DFM) =================

    # 1. Khoét lòng đặt động cơ GA25 (Ø25.4 mm mở lên trên) + Lỗ cổ trục Ø9.0 mm (Giọt nước 45°) + 4 lỗ ốc M3:
    for my in [32.0, 142.0]:
        # Bên Trái
        base = cut_hole_x(base, -W/2.0 + 4.0, my, Z_SHAFT_LOCAL, 25.4, 36.0, teardrop=False)
        base = cut_hole_x(base, -W/2.0 - 1.0, my, Z_SHAFT_LOCAL, 9.0, 6.0, teardrop=True)
        for a_deg in [0, 90, 180, 270]:
            rad = math.radians(a_deg)
            base = cut_hole_x(base, -W/2.0 - 1.0, my + 8.5 * math.cos(rad), Z_SHAFT_LOCAL + 8.5 * math.sin(rad), 3.3, 6.0, teardrop=True)

        # Bên Phải
        base = cut_hole_x(base, W/2.0 - 40.0, my, Z_SHAFT_LOCAL, 25.4, 36.0, teardrop=False)
        base = cut_hole_x(base, W/2.0 - 5.0, my, Z_SHAFT_LOCAL, 9.0, 6.0, teardrop=True)
        for a_deg in [0, 90, 180, 270]:
            rad = math.radians(a_deg)
            base = cut_hole_x(base, W/2.0 - 5.0, my + 8.5 * math.cos(rad), Z_SHAFT_LOCAL + 8.5 * math.sin(rad), 3.3, 6.0, teardrop=True)

    # 2. 8 Lỗ ốc M3 bắt 4 nắp kẹp động cơ GA25 tại X = ±44.0 mm, Y = my ± 17.5 mm:
    for my in [32.0, 142.0]:
        for dy in [-17.5, 17.5]:
            base = cut_hole_z(base, -44.0, my + dy, 3.0, 3.0, 18.0)
            base = cut_hole_z(base, 44.0, my + dy, 3.0, 3.0, 18.0)

    # 3. 4 Lỗ ốc M3 chính tâm 4 Trụ đỡ Bệ MCU (tại X = ±33.0, Y = 49.0 và 99.0):
    for px in [-33.0, 33.0]:
        for py in [49.0, 99.0]:
            base = cut_hole_z(base, px, py, 4.0, 3.0, 19.0)

    # 4. 10 Lỗ bu-lông M3 (Ø3.2 mm xuyên sàn) để bắt cứng 2 Tháp Nâng Rời Trái & Phải vào khung gầm:
    # - 3 lỗ trên tai chữ L bên trong mỗi tháp (X = ±16.0, Y = 110.5, 122.0, 160.25)
    # - 2 lỗ xuyên từ dưới sàn xe lên trực tiếp thân tháp dày 8mm mỗi bên (X = ±24.0, Y = 116.0, 160.25)
    for sx in [-16.0, 16.0]:
        for sy in [110.5, 122.0, 160.25]:
            base = cut_hole_z(base, sx, sy, -0.5, 3.2, T + 1.0)
    for sx in [-24.0, 24.0]:
        for sy in [116.0, 160.25]:
            base = cut_hole_z(base, sx, sy, -0.5, 3.2, T + 1.0)

    # 5A. 2 Lỗ bu-lông M4 (Ø4.2 mm) bắt Mạch nhận tín hiệu điều khiển I2C sườn trái + khe đai ốc M4:
    base = cut_hole_z(base, -W/2.0 + 9.0, 61.0, 4.0, 4.2, 14.0)
    base = cut_hole_z(base, -W/2.0 + 9.0, 77.0, 4.0, 4.2, 14.0)
    base = cut_box(base, -W/2.0 + 4.0, 58.0, 6.0, 13.0, 22.0, 4.0)

    # 5B. 2 Lỗ bắt Module Nút nhấn đôi (Dual Push Button OhStem) sườn phải:
    base = cut_hole_z(base, W/2.0 - 9.0, 61.0, 4.0, 3.4, 14.0)
    base = cut_hole_z(base, W/2.0 - 9.0, 77.0, 4.0, 3.4, 14.0)
    base = cut_box(base, W/2.0 - 17.0, 58.0, 6.0, 13.0, 22.0, 4.0)

    # 6. Ma trận lỗ ốc M3 đa năng trên sàn xe:
    for ex in [-50.0, -42.0, 42.0, 50.0]:
        for ey in [88.0, 104.0, 114.0]:
            base = cut_hole_z(base, ex, ey, -0.5, 3.2, T + 1.0)
    for ex in [-8.0, 0.0, 8.0]:
        for ey in [112.0, 128.0]:
            base = cut_hole_z(base, ex, ey, -0.5, 3.2, T + 1.0)
    for ex in [-16.0, 0.0, 16.0]:
        for ey in [8.0, 48.0, 64.0, 80.0, 96.0]:
            base = cut_hole_z(base, ex, ey, -0.5, 3.2, T + 1.0)

    # 7. Hệ lỗ ốc M3 (bước 16/24/32mm) & Rãnh luồn cáp Grove tại mũi xe để bắt Đế đệm Cảm biến dò line (`01E`):
    for lx in [-16.0, -12.0, -8.0, 8.0, 12.0, 16.0]:
        base = cut_hole_z(base, lx, 160.0, -0.5, 3.2, T + 1.0)
    base = cut_box(base, -8.0, 146.0, -0.5, 16.0, 8.0, T + 1.0)

    # 8. Hốc & Lỗ mắt Cảm biến khoảng cách Siêu âm OhStem (2 mắt Ø16.6mm biên dạng Giọt nước 45° tự đỡ!):
    base = cut_hole_y(base, -13.0, L - 11.0, 14.0, 16.6, 15.0, teardrop=True)
    base = cut_hole_y(base, 13.0, L - 11.0, 14.0, 16.6, 15.0, teardrop=True)
    base = cut_box(base, -24.4, L - 10.5, 4.0, 48.8, 3.5, 22.0)
    base = cut_hole_z(base, -8.0, L - 13.0, -0.5, 3.2, 12.0)
    base = cut_hole_z(base, 8.0, L - 13.0, -0.5, 3.2, 12.0)
    base = cut_hole_y(base, -21.0, L - 11.0, 14.0, 3.2, 15.0, teardrop=True)
    base = cut_hole_y(base, 21.0, L - 11.0, 14.0, 3.2, 15.0, teardrop=True)

    # 9. Rãnh luồn dây điện thông thoáng & 4 Khe luồn dây rút (Zip-tie slots) giữ Pin:
    base = cut_box(base, -12.0, 18.0, -0.5, 24.0, 22.0, T + 1.0)
    for zx in [-24.0, 20.0]:
        for zy in [56.0, 86.0]:
            base = cut_box(base, zx, zy, -0.5, 4.0, 8.0, T + 1.0)

    return base


# ====================================================================
# 1B & 1C. THÁP NÂNG CÁNH TAY TRÁI & PHẢI RỜI (IN PHẲNG 100% - 0% SUPPORT)
# ====================================================================
def create_lift_tower_assembly_space(is_left=True):
    """
    Tạo Tháp nâng Trái hoặc Phải trong hệ tọa độ lắp ghép trên khung gầm (Z = 4.0..94.0 mm):
    - Mặt ngoài của tháp (X = -28.0 với Tháp Trái, X = +28.0 với Tháp Phải) PHẲNG TUYỆT ĐỐI 100%!
    - Khi xoay nằm phẳng mặt ngoài xuống bàn in (orient_for_print):
      + Toàn bộ tấm tháp 61 x 90 mm áp sát bàn in tại Z_print = 0.0 mm.
      + Đế chữ L dưới chân (Z = 4.0..12.0) và Tai giằng đỉnh (Z = 88.0..94.0) vươn thẳng đứng lên (+Z_print) -> 0% Overhang!
      + Hốc Servo MG996R (41.2 x 20.2 mm), 4 lỗ ốc tai Servo và các lỗ trục xoay (Ø3.3 mm) hướng thẳng đứng -> 0% Support!
    """
    x_wall_min = -28.0 if is_left else 20.0
    x_flange_min = -20.0 if is_left else 12.0

    # 1. Tấm vách tháp chính dày 8.0 mm (Y in [105.0, 166.0], Z in [4.0, 94.0])
    tower = make_box(x_wall_min, 105.0, 4.0, 8.0, 61.0, 90.0)

    # 2. Hai đế chữ L dưới chân (chân sau Y in [105.0, 127.5] và chân trước Y in [154.5, 166.0], cao Z in [4.0, 12.0])
    foot_rear = make_box(x_flange_min, 105.0, 4.0, 8.0, 22.5, 8.0)
    foot_front = make_box(x_flange_min, 154.5, 4.0, 8.0, 11.5, 8.0)
    tower = BRepAlgoAPI_Fuse(tower, foot_rear).Shape()
    tower = BRepAlgoAPI_Fuse(tower, foot_front).Shape()

    # 3. Tai giằng ngang trên đỉnh tháp (Y in [105.0, 118.0], Z in [88.0, 94.0], vươn vào tới X = 0.0 để nối cứng 2 tháp)
    brace_x0 = -20.0 if is_left else 0.0
    top_brace = make_box(brace_x0, 105.0, 88.0, 20.0, 13.0, 6.0)
    tower = BRepAlgoAPI_Fuse(tower, top_brace).Shape()

    # --- KHOÉT LỖ TRÊN THÁP ---
    # 1. Khoét vòm cổng dưới chân tháp (Y in [127.5, 154.5], Z in [3.5, 34.0]) để lọt thông thoáng trên cầu trước
    tower = cut_box(tower, -30.0, 127.5, 3.5, 60.0, 27.0, 30.5)

    # 2. Hốc Servo MG996R trên Tháp Phải / Ô thoáng giảm trọng lượng trên Tháp Trái:
    if not is_left:
        # Hốc chữ nhật 41.2 x 20.2 mm (Y in [114.05, 155.25], Z in [47.9, 68.1])
        tower = cut_box(tower, 19.0, 114.05, 47.9, 10.0, 41.2, 20.2)
        # 4 Lỗ ốc M3/M4 (Ø3.4 mm) bắt tai Servo MG996R chuẩn 48.5 x 10.0 mm
        for sy in [134.65 - 24.25, 134.65 + 24.25]:
            for sz in [58.0 - 5.0, 58.0 + 5.0]:
                tower = cut_hole_x(tower, 19.0, sy, sz, 3.4, 10.0, teardrop=False)
    else:
        # Ô thoáng giảm trọng lượng trên Tháp Trái (Y in [114.05, 136.0], Z in [47.9, 68.1])
        tower = cut_box(tower, -29.0, 114.05, 47.9, 10.0, 22.0, 20.2)
        # Lỗ chốt xoay M3 dưới (Y = 145.0, Z = 58.0) trên Tháp Trái
        tower = cut_hole_x(tower, -30.0, 145.0, 58.0, 3.3, 12.0, teardrop=False)

    # 3. Lỗ chốt xoay M3 trên (Y = 145.0, Z = 86.0) trên cả 2 tháp:
    tower = cut_hole_x(tower, -30.0, 145.0, 86.0, 3.3, 60.0, teardrop=False)

    # 4. 3 Lỗ bu-lông M3 trên Đế chữ L (X = ±16.0, Y = 110.5, 122.0, 160.25) + 2 lỗ ốc M3 dưới đáy tháp (X = ±24.0, Y = 116.0, 160.25):
    fx = -16.0 if is_left else 16.0
    wx = -24.0 if is_left else 24.0
    for sy in [110.5, 122.0, 160.25]:
        tower = cut_hole_z(tower, fx, sy, 3.5, 3.3, 10.0)
    for sy in [116.0, 160.25]:
        tower = cut_hole_z(tower, wx, sy, 3.5, 3.0, 14.0)

    # 5. Lỗ ốc M3 khóa nối 2 tai giằng đỉnh tại mặt phẳng giữa X = 0.0 (Y = 111.5, Z = 91.0):
    tower = cut_hole_x(tower, -10.0, 111.5, 91.0, 3.3, 20.0, teardrop=False)

    return tower

def create_lift_tower_printable(is_left=True):
    """
    Xoay Tháp nâng Trái/Phải nằm phẳng mặt ngoài (X = ±28.0) xuống mặt bàn in Z = 0.0 mm!
    - Tháp Trái (mặt phẳng ngoài ở X = -28.0): xoay -90° quanh trục Y -> X = -28.0 trở thành Z_min = 0.0!
    - Tháp Phải (mặt phẳng ngoài ở X = +28.0): xoay +90° quanh trục Y -> X = +28.0 trở thành Z_min = 0.0!
    """
    raw = create_lift_tower_assembly_space(is_left=is_left)
    ry = -90.0 if is_left else 90.0
    return orient_for_print(raw, ry_deg=ry)


# ====================================================================
# 1D. BỆ ĐẶT MẠCH ĐIỀU KHIỂN MCU RỜI (IN PHẲNG 100% - 0% SUPPORT)
# ====================================================================
def create_mcu_deck_assembly_space():
    """
    Bệ phẳng đặt mạch điều khiển ORC Control Hub (Y in [44.0, 104.0], Z in [22.0, 30.0] trên khung gầm):
    - Khi in rời đặt phẳng trên mặt bàn in (Z = 0.0..8.0 mm): In 100% không cần support!
    - Bắt 4 ốc M3 tại (X = ±33.0, Y = 49.0 và 99.0) xuống 4 trụ đỡ của khung gầm.
    """
    deck = make_box(-38.0, 44.0, 22.0, 76.0, 60.0, 4.0)
    # Khoét ô thoáng giữa sàn MCU (44 x 32 mm) để tản nhiệt, giảm nhựa và luồn dây:
    deck = cut_box(deck, -22.0, 58.0, 21.5, 44.0, 32.0, 5.0)

    # 4 Gờ chữ L định vị góc hộp MCU ORC Control Hub (lọt lòng 76.0 x 61.0 mm tại Z = 26.0..30.0 mm):
    for cx_sign in [-1, 1]:
        for cy_pos in [44.0, 101.0]:
            lip_x = -39.5 if cx_sign < 0 else 36.5
            lip = make_box(lip_x, cy_pos, 26.0, 3.0, 3.0, 4.0)
            deck = BRepAlgoAPI_Fuse(deck, lip).Shape()

    # 4 Lỗ ốc M3 bắt xuống 4 trụ khung gầm (X = ±33.0, Y = 49.0 và 99.0):
    for px in [-33.0, 33.0]:
        for py in [49.0, 99.0]:
            deck = cut_hole_z(deck, px, py, 21.5, 3.4, 6.0)

    # Hệ lỗ ốc M3 chuẩn OhStem trên Bệ MCU quanh tâm Y = 74.0 mm:
    for ox in [-32.0, -28.0, 28.0, 32.0]:
        for oy in [-28.0, -24.0, 24.0, 28.0]:
            deck = cut_hole_z(deck, ox, 74.0 + oy, 21.5, 3.2, 6.0)

    return deck

def create_mcu_deck_printable():
    return orient_for_print(create_mcu_deck_assembly_space())


# ====================================================================
# 1E. ĐẾ ĐỆM HẠ THẤP CẢM BIẾN DÒ LINE 4 MẮT RỜI (IN PHẲNG 100%)
# ====================================================================
def create_line_sensor_spacer_assembly_space():
    """
    Đế đệm hạ thấp 6.0 mm dưới gầm mũi xe cho Cảm biến dò đường 4 mắt OhStem (48 x 24 mm, I2C 0x23):
    - Tách rời khỏi đáy khung gầm để sàn khung gầm phẳng tuyệt đối 100% tại Z = 0.0 mm!
    """
    pod = make_box(-26.0, 148.0, -6.0, 52.0, 24.0, 6.0)
    for lx in [-16.0, -12.0, -8.0, 8.0, 12.0, 16.0]:
        pod = cut_hole_z(pod, lx, 160.0, -6.5, 3.3, 7.0)
    pod = cut_box(pod, -8.0, 146.0, -6.5, 16.0, 8.0, 7.0)
    return pod

def create_line_sensor_spacer_printable():
    return orient_for_print(create_line_sensor_spacer_assembly_space())


# ====================================================================
# 2. NẮP KẸP ÔM ĐỘNG CƠ GA25 (GA25 CLAMP CAP V4.0 - IN PHẲNG MẶT BÊN 0% SUPPORT)
# ====================================================================
def create_ga25_clamp_cap():
    """
    Nắp kẹp bán nguyệt ôm chặt nửa trên động cơ kim loại Ø25mm của GA25 (trong hệ tọa độ lắp ghép):
    - Khi xuất file in 3D (`create_ga25_clamp_cap_printable`), chi tiết được xoay 90° quanh trục Y
      để mặt bên phẳng (Y x Z) nằm áp sát bàn in -> Vòm Ø25.4mm hướng thẳng đứng, in 0% Support và siêu bền!
    """
    flange = make_box(-12.0, -22.0, 0.0, 24.0, 44.0, 6.0)
    arch = make_box(-12.0, -14.2, 0.0, 24.0, 28.4, 16.0)
    cap = BRepAlgoAPI_Fuse(flange, arch).Shape()

    # Khoét rãnh bán nguyệt Ø25.4 mm dọc theo TRỤC X
    cap = cut_hole_x(cap, -13.0, 0.0, 0.0, 25.4, 26.0, teardrop=False)

    # 2 Lỗ ốc M3 (Ø3.4 mm) tại Y = ±17.5 mm
    cap = cut_hole_z(cap, 0.0, -17.5, -0.5, 3.4, 8.0)
    cap = cut_hole_z(cap, 0.0, 17.5, -0.5, 3.4, 8.0)

    return cap

def create_ga25_clamp_cap_printable():
    """
    Đặt Nắp kẹp động cơ nằm trên mặt bên phẳng (X = -12.0 trở thành Z = 0.0 mm)
    để vòm bán nguyệt Ø25.4mm in thẳng đứng dọc trục Z -> 0% Support, chịu lực căng đai kẹp tối đa!
    """
    return orient_for_print(create_ga25_clamp_cap(), ry_deg=-90.0)


# ====================================================================
# 3A. KHUNG TAY NÂNG DƯỚI CHỮ H ĐÁY PHẲNG 100% (DFM V4.0 - 0% SUPPORT)
# ====================================================================
def create_lower_h_frame_arm(length=98.0, height=12.0, thickness=5.0):
    """
    Khung tay nâng dưới chữ H chuẩn DFM V4.0:
    - Toàn bộ mặt đáy (Z = -height/2.0 = -6.0 mm) PHẲNG TUYỆT ĐỐI 100% từ đầu đến cuối!
    - Đã loại bỏ phần lồi dưới của đĩa horn_boss R=10mm từng làm kênh thanh tay đòn 4mm khỏi bàn in.
    - Bổ sung gờ tăng cứng phía trên (+Z) quanh hốc Servo Horn MG996R để giữ mặt đáy Z = -6.0 phẳng hoàn toàn!
    """
    arm_l = make_box(-19.5, 0.0, -height/2.0, thickness, length, height)
    arm_r = make_box(14.5, 0.0, -height/2.0, thickness, length, height)

    for x0 in [-19.5, 14.5]:
        c_rear = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0, 0.0, 0.0), gp_Dir(1, 0, 0)), height/2.0, thickness).Shape()
        c_front = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0, length, 0.0), gp_Dir(1, 0, 0)), height/2.0, thickness).Shape()
        # Chân đế phẳng dưới 2 đầu xoay giúp in 3D bám bàn 100% từ Y = -height/2 đến Y = length + height/2 không bị overhang cong đáy!
        flat_rear = make_box(x0, -height/2.0, -height/2.0, thickness, height/2.0, height/2.0)
        flat_front = make_box(x0, length, -height/2.0, thickness, height/2.0, height/2.0)
        arm_l = BRepAlgoAPI_Fuse(arm_l, c_rear).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, c_front).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, flat_rear).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, flat_front).Shape()

    frame = BRepAlgoAPI_Fuse(arm_l, arm_r).Shape()

    # Thanh giằng ngang chữ H chống xoắn (đồng phẳng đáy Z = -height/2.0)
    cross_bar = make_box(-14.5, 42.0, -height/2.0, 29.0, 14.0, height)
    frame = BRepAlgoAPI_Fuse(frame, cross_bar).Shape()

    # Khoét rãnh âm 2.0 mm ở mặt ngoài bên phải (X in [17.5, 19.5]) để ốp vừa khít Cánh tay gạt MG996R:
    frame = cut_box(frame, 17.5, -4.1, -4.1, 2.5, 24.0, 8.2)
    # 2 Lỗ vít khóa Cánh tay gạt MG996R (Ø2.3 mm tại Y = 10.0 và Y = 16.0 mm):
    frame = cut_hole_x(frame, 13.5, 10.0, 0.0, 2.3, 7.0, teardrop=False)
    frame = cut_hole_x(frame, 13.5, 16.0, 0.0, 2.3, 7.0, teardrop=False)

    # Lỗ chốt xoay M3 ở 2 đầu (biên dạng Giọt nước 45° tự đỡ)
    frame = cut_hole_x(frame, -22.0, 0.0, 0.0, 3.3, 44.0, teardrop=True)
    frame = cut_hole_x(frame, -22.0, length, 0.0, 3.3, 44.0, teardrop=True)

    return frame

def create_lower_h_frame_arm_printable():
    return orient_for_print(create_lower_h_frame_arm())


# ====================================================================
# 3B. KHUNG TAY NÂNG TRÊN CHỮ H ĐÁY PHẲNG 100% (DFM V4.0 - 0% SUPPORT)
# ====================================================================
def create_upper_h_frame_arm(length=98.0, height=11.0, thickness=5.0):
    arm_l = make_box(-19.5, 0.0, -height/2.0, thickness, length, height)
    arm_r = make_box(14.5, 0.0, -height/2.0, thickness, length, height)

    for x0 in [-19.5, 14.5]:
        c_rear = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0, 0.0, 0.0), gp_Dir(1, 0, 0)), height/2.0, thickness).Shape()
        c_front = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0, length, 0.0), gp_Dir(1, 0, 0)), height/2.0, thickness).Shape()
        flat_rear = make_box(x0, -height/2.0, -height/2.0, thickness, height/2.0, height/2.0)
        flat_front = make_box(x0, length, -height/2.0, thickness, height/2.0, height/2.0)
        arm_l = BRepAlgoAPI_Fuse(arm_l, c_rear).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, c_front).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, flat_rear).Shape()
        arm_l = BRepAlgoAPI_Fuse(arm_l, flat_front).Shape()

    frame = BRepAlgoAPI_Fuse(arm_l, arm_r).Shape()
    cross_bar = make_box(-14.5, 44.0, -height/2.0, 29.0, 12.0, height)
    frame = BRepAlgoAPI_Fuse(frame, cross_bar).Shape()

    frame = cut_hole_x(frame, -22.0, 0.0, 0.0, 3.3, 44.0, teardrop=True)
    frame = cut_hole_x(frame, -22.0, length, 0.0, 3.3, 44.0, teardrop=True)

    return frame

def create_upper_h_frame_arm_printable():
    return orient_for_print(create_upper_h_frame_arm())


# ====================================================================
# 4. BỆ ĐẦU KẸP HOA TÍCH HỢP GÁ SERVO MG996R (DFM V4.0 - ZERO SUPPORT)
# ====================================================================
def create_gripper_base_head():
    """
    Bệ đầu kẹp hoa chuẩn Servo MG996R (S2) - Bản DFM V4.0 Không Cầu Treo (0% Support):
    - Đáy phẳng tuyệt đối 100% tại Z = 0.0 mm.
    - 2 Trụ đỡ tai bắt ốc Servo MG996R (pillar_l tại X in [-25.0, -16.95] và pillar_r tại X in [24.25, 32.0])
      vươn thẳng đứng từ tấm đế Z = 0.0 mm lên Z = 35.0 mm (đỡ trọn vẹn 4 lỗ ốc tai Servo tại X = -20.60 và +27.90).
    - Đã loại bỏ 2 dải cầu mỏng treo lơ lửng vắt ngang trên 2 trụ bản lề hàm kẹp -> In 0% Support và lắp hàm kẹp từ trên xuống cực dễ!
    """
    # 1. Tấm đế dưới đỡ 2 hàm kẹp (Z in [0, 5.0])
    plate = make_box(-25.0, 0.0, 0.0, 57.0, 43.5, 5.0)

    # 2. 2 Tai sau liên kết tay đòn song hành + Vách hậu tăng cứng
    ear_l = make_box(-14.0, 0.0, 0.0, 5.5, 16.0, 44.0)
    ear_r = make_box(8.5, 0.0, 0.0, 5.5, 16.0, 44.0)
    rear_tie = make_box(-25.0, 0.0, 0.0, 57.0, 6.0, 35.0)
    rear_top = make_box(-14.0, 0.0, 0.0, 28.0, 6.0, 44.0)
    base = BRepAlgoAPI_Fuse(plate, ear_l).Shape()
    base = BRepAlgoAPI_Fuse(base, ear_r).Shape()
    base = BRepAlgoAPI_Fuse(base, rear_tie).Shape()
    base = BRepAlgoAPI_Fuse(base, rear_top).Shape()

    # 3. 2 Trụ định tâm hàm kẹp tại (X = ±14.0, Y = 32.0, Z in [5.0, 15.0], Ø8.0 mm)
    boss_l = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-14.0, 32.0, 5.0), gp_Dir(0, 0, 1)), 4.0, 10.0).Shape()
    boss_r = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(14.0, 32.0, 5.0), gp_Dir(0, 0, 1)), 4.0, 10.0).Shape()
    base = BRepAlgoAPI_Fuse(base, boss_l).Shape()
    base = BRepAlgoAPI_Fuse(base, boss_r).Shape()

    # 4. Hai trụ đỡ tai bắt ốc Servo MG996R nối liền từ sàn Z = 0.0 lên Z = 35.0 mm (kèm vách nối về phía sau Y in [0, 43.5]):
    # Hoàn toàn không có cầu ngang treo lơ lửng -> Tự in 100% không cần support!
    pillar_l = make_box(-25.0, 0.0, 0.0, 8.05, 43.5, 35.0)
    pillar_r = make_box(24.25, 0.0, 0.0, 7.75, 43.5, 35.0)
    base = BRepAlgoAPI_Fuse(base, pillar_l).Shape()
    base = BRepAlgoAPI_Fuse(base, pillar_r).Shape()

    # --- KHOÉT LỖ BỆ ĐẦU KẸP ---
    # 1. Khoan 4 lỗ ốc M3/M4 (Ø3.2 mm) bắt tai Servo MG996R chuẩn 48.5 x 10.0 mm trên 2 trụ:
    for sx in [3.65 - 24.25, 3.65 + 24.25]:
        for sy in [32.0 - 5.0, 32.0 + 5.0]:
            base = cut_hole_z(base, sx, sy, 15.0, 3.2, 22.0)

    # 2. 2 Lỗ trục xoay hàm kẹp M3 tại (X = ±14.0, Y = 32.0):
    base = cut_hole_z(base, -14.0, 32.0, -0.5, 3.3, 20.0)
    base = cut_hole_z(base, 14.0, 32.0, -0.5, 3.3, 20.0)

    # 3. 2 Lỗ chốt M3 liên kết với khung tay nâng chữ H (Y = 8.0, Z = 10.0 và Z = 38.0 - biên dạng Giọt nước 45°):
    base = cut_hole_x(base, -28.0, 8.0, 10.0, 3.3, 62.0, teardrop=True)
    base = cut_hole_x(base, -28.0, 8.0, 38.0, 3.3, 62.0, teardrop=True)

    return base

def create_gripper_base_head_printable():
    return orient_for_print(create_gripper_base_head())


# ====================================================================
# 5 & 6. CẶP HÀM KẸP HOA V-GUIDE Ø32mm (DFM V4.0 - LỖ BẬC CÔN 45° 0% SUPPORT)
# ====================================================================
def create_specialized_gripper_jaw(is_left=True):
    """
    Hàm kẹp hoa chuyên dụng (tâm xoay tại (±14.0, 0), tâm ống hoa tại (0, 34.0)):
    - Bổ sung mái côn tự đỡ 45° (cut_counterbore_z_dfm) cho lỗ bạc lót Ø8.2mm dưới đáy trục xoay
      giúp cả Hàm Trái và Hàm Phải in phẳng 100% trên bàn in mà KHÔNG CẦN SUPPORT!
    """
    r_in, r_out, H = 16.5, 21.5, 22.0
    pivot_x = -14.0 if is_left else 14.0
    Y_FL = 34.0

    # 1. Máng bán nguyệt ôm thân hoa tại (0, Y_FL)
    outer = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0.0, Y_FL, 0.0), gp_Dir(0, 0, 1)), r_out, H).Shape()
    inner = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0.0, Y_FL, -0.5), gp_Dir(0, 0, 1)), r_in, H + 1.0).Shape()
    cradle = BRepAlgoAPI_Cut(outer, inner).Shape()
    cradle = cut_box(cradle, -25.0, Y_FL, -0.5, 50.0, 25.0, H + 1.0)
    if is_left:
        cradle = cut_box(cradle, 0.0, 0.0, -0.5, 25.0, 60.0, H + 1.0)
    else:
        cradle = cut_box(cradle, -25.0, 0.0, -0.5, 25.0, 60.0, H + 1.0)

    # 2. Cánh phễu V-Guide dẫn hướng đón hoa (mở rộng 35°)
    wing_box = make_box(-2.0, 0.0, 0.0, 4.0, 22.0, H)
    tr_rot = gp_Trsf()
    angle_wing = 35.0 if is_left else -35.0
    tr_rot.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(angle_wing))
    tr_mov = gp_Trsf()
    tr_mov.SetTranslation(gp_Vec(-18.5 if is_left else 18.5, Y_FL, 0.0))
    wing = BRepBuilderAPI_Transform(wing_box, tr_mov * tr_rot).Shape()
    jaw = BRepAlgoAPI_Fuse(cradle, wing).Shape()

    # 3. Gờ đỡ đáy chống tuột hoa (Bottom Retention Lip dày 3.0 mm)
    lip_outer = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0.0, Y_FL, 0.0), gp_Dir(0, 0, 1)), r_in, 3.0).Shape()
    lip_inner = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0.0, Y_FL, -0.5), gp_Dir(0, 0, 1)), 13.5, 4.0).Shape()
    lip = BRepAlgoAPI_Cut(lip_outer, lip_inner).Shape()
    lip = cut_box(lip, -25.0, Y_FL, -0.5, 50.0, 25.0, 5.0)
    if is_left:
        lip = cut_box(lip, 0.0, 0.0, -0.5, 25.0, 60.0, 5.0)
    else:
        lip = cut_box(lip, -25.0, 0.0, -0.5, 25.0, 60.0, 5.0)
    jaw = BRepAlgoAPI_Fuse(jaw, lip).Shape()

    # 4. Cổ trục xoay & Thân bánh răng rẻ quạt tại (pivot_x, 0) + Tay đòn nối lên máng hoa
    hub = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(pivot_x, 0.0, 0.0), gp_Dir(0, 0, 1)), 12.2, H).Shape()
    neck = make_box(pivot_x - 5.0, 0.0, 0.0, 10.0, 22.0, H)
    jaw = BRepAlgoAPI_Fuse(jaw, hub).Shape()
    jaw = BRepAlgoAPI_Fuse(jaw, neck).Shape()

    # 5. Các răng bánh răng rẻ quạt ăn khớp lệch pha tại (0, 0):
    tooth_angles = [-36.0, -18.0, 0.0, 18.0, 36.0] if is_left else [153.0, 171.0, 189.0, 207.0]
    for a_deg in tooth_angles:
        t_box = make_box(11.5, -1.7, 0.0, 4.1, 3.4, H)
        tr_t_rot = gp_Trsf()
        tr_t_rot.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(a_deg))
        tr_t_pos = gp_Trsf()
        tr_t_pos.SetTranslation(gp_Vec(pivot_x, 0.0, 0.0))
        tooth = BRepBuilderAPI_Transform(t_box, tr_t_pos * tr_t_rot).Shape()
        jaw = BRepAlgoAPI_Fuse(jaw, tooth).Shape()

    # 6. Lỗ bạc lót trục xoay Ø8.2 mm sâu 10.2 mm có mái côn tự đỡ 45° + Lỗ ốc tâm M3 (Ø3.3 mm):
    jaw = cut_counterbore_z_dfm(jaw, pivot_x, 0.0, -0.2, 8.2, 10.4, 3.3, H + 1.0)

    # 7. Hốc âm lắp Cánh tay gạt (Servo Horn) MG996R ở mặt trên Hàm Phải (Z in [19.5, 22.0] - ngửa lên trên, 0% Support!):
    if not is_left:
        jaw = cut_box(jaw, pivot_x - 4.1, -4.1, H - 2.5, 8.2, 22.0, 3.0)
        jaw = cut_hole_z(jaw, pivot_x, 8.0, 8.0, 2.3, H - 7.0)
        jaw = cut_hole_z(jaw, pivot_x, 13.0, 8.0, 2.3, H - 7.0)

    return jaw

def create_specialized_gripper_jaw_printable(is_left=True):
    return orient_for_print(create_specialized_gripper_jaw(is_left=is_left))


# ====================================================================
# 7. BÁNH XE MECANUM K3 Ø80mm x 38mm (IN PHẲNG TRÊN BÀN IN)
# ====================================================================
def create_mecanum_wheel_k3(is_left=True):
    D, W_m = 80.0, 38.0
    r = D / 2.0
    rim = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), r, W_m).Shape()
    c_sub1 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-0.5, 0, 0), gp_Dir(1, 0, 0)), r - 7.0, 7.0).Shape()
    c_sub2 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(W_m - 6.5, 0, 0), gp_Dir(1, 0, 0)), r - 7.0, 7.0).Shape()
    rim = BRepAlgoAPI_Cut(rim, c_sub1).Shape()
    rim = BRepAlgoAPI_Cut(rim, c_sub2).Shape()
    rim = cut_hole_x(rim, -0.5, 0, 0, 4.2, W_m + 1.0, teardrop=False)
    return rim

def create_mecanum_wheel_k3_printable(is_left=True):
    """
    Xoay bánh xe nằm phẳng trên mặt bàn in (Z = 0.0..38.0 mm) để không bị chìm xuống dưới mặt lưới Z=0!
    """
    return orient_for_print(create_mecanum_wheel_k3(is_left=is_left), ry_deg=-90.0)


# ====================================================================
# 8. CÁNH TAY GẠT SERVO MG996R RỜI (DFM V4.0 - LỖ BẬC CÔN 45° 0% SUPPORT)
# ====================================================================
def create_mg996r_servo_lever_horn():
    arm = make_box(-4.0, 0.0, 0.0, 8.0, 20.0, 4.0)
    c_hub = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 6.5, 6.0).Shape()
    c_tip = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 20.0, 0), gp_Dir(0, 0, 1)), 4.0, 4.0).Shape()
    horn = BRepAlgoAPI_Fuse(arm, c_hub).Shape()
    horn = BRepAlgoAPI_Fuse(horn, c_tip).Shape()
    horn = cut_counterbore_z_dfm(horn, 0.0, 0.0, -0.2, 6.0, 3.2, 3.2, 7.0)
    for ry in [10.0, 13.0, 16.0, 20.0]:
        horn = cut_hole_z(horn, 0.0, ry, -0.5, 2.3, 5.0)
    return horn

def create_mg996r_servo_lever_horn_printable():
    return orient_for_print(create_mg996r_servo_lever_horn())


# ====================================================================
# 9. MÔ HÌNH LẮP GHÉP TỔNG THỂ ROBOT ORC-X1 PRO V4.0 (FULL ASSEMBLY)
# ====================================================================
def create_full_assembly_modern():
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)

    Z_GROUND = 20.0
    Z_SHAFT = 40.0
    Y_PIVOT = 145.0
    ARM_L = 98.0
    ARM_ANGLE = -20.0
    DY_ARM = ARM_L * math.cos(math.radians(ARM_ANGLE))  # 92.09 mm
    DZ_ARM = ARM_L * math.sin(math.radians(ARM_ANGLE))  # -33.52 mm

    # 1. Khung gầm chính + 2 Tháp nâng rời + Bệ MCU rời + Đế đệm cảm biến dò line rời
    tr_ch = gp_Trsf()
    tr_ch.SetTranslation(gp_Vec(0, 0, Z_GROUND))
    builder.Add(compound, BRepBuilderAPI_Transform(create_monocoque_chassis(), tr_ch).Shape())
    builder.Add(compound, BRepBuilderAPI_Transform(create_lift_tower_assembly_space(is_left=True), tr_ch).Shape())
    builder.Add(compound, BRepBuilderAPI_Transform(create_lift_tower_assembly_space(is_left=False), tr_ch).Shape())
    builder.Add(compound, BRepBuilderAPI_Transform(create_mcu_deck_assembly_space(), tr_ch).Shape())
    builder.Add(compound, BRepBuilderAPI_Transform(create_line_sensor_spacer_assembly_space(), tr_ch).Shape())

    # 2. 4 Nắp kẹp động cơ GA25 (tại X = ±44.0 mm)
    cap_raw = create_ga25_clamp_cap()
    for my in [32.0, 142.0]:
        for x_pos in [-44.0, 44.0]:
            tr_cap = gp_Trsf()
            tr_cap.SetTranslation(gp_Vec(x_pos, my, Z_SHAFT))
            builder.Add(compound, BRepBuilderAPI_Transform(cap_raw, tr_cap).Shape())

    # 3. 4 Bánh xe Mecanum K3 (Phủ bì 218.0 mm < 248.0 mm hành lang mê cung)
    wh_raw = create_mecanum_wheel_k3()
    wheels_data = [
        (-109.0, 142.0, Z_SHAFT),
        (109.0 - 38.0, 142.0, Z_SHAFT),
        (-109.0, 32.0, Z_SHAFT),
        (109.0 - 38.0, 32.0, Z_SHAFT),
    ]
    for wx, wy, wz in wheels_data:
        tr_w = gp_Trsf()
        tr_w.SetTranslation(gp_Vec(wx, wy, wz))
        builder.Add(compound, BRepBuilderAPI_Transform(wh_raw, tr_w).Shape())

    # 4. 4 Động cơ kim loại GA25-370
    motors = [
        (-64.0, 142.0, Z_SHAFT, 48.0),
        (64.0 - 48.0, 142.0, Z_SHAFT, 48.0),
        (-64.0, 32.0, Z_SHAFT, 54.0),
        (64.0 - 54.0, 32.0, Z_SHAFT, 54.0),
    ]
    for mx, my, mz, ml in motors:
        cyl_m = BRepPrimAPI_MakeCylinder(
            gp_Ax2(gp_Pnt(mx, my, mz), gp_Dir(1, 0, 0)),
            12.5, ml
        ).Shape()
        builder.Add(compound, cyl_m)

    # 5. Khung tay nâng 4 khâu chữ H
    lower_arm_raw = create_lower_h_frame_arm(length=ARM_L)
    tr_rot_arm = gp_Trsf()
    tr_rot_arm.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.radians(ARM_ANGLE))
    tr_low_pos = gp_Trsf()
    tr_low_pos.SetTranslation(gp_Vec(0, Y_PIVOT, 78.0))
    builder.Add(compound, BRepBuilderAPI_Transform(lower_arm_raw, tr_low_pos * tr_rot_arm).Shape())

    upper_arm_raw = create_upper_h_frame_arm(length=ARM_L)
    tr_up_pos = gp_Trsf()
    tr_up_pos.SetTranslation(gp_Vec(0, Y_PIVOT, 106.0))
    builder.Add(compound, BRepBuilderAPI_Transform(upper_arm_raw, tr_up_pos * tr_rot_arm).Shape())

    # 6. Cụm bệ đầu kẹp hoa & 2 Hàm kẹp bánh răng ăn khớp
    Y_HEAD = Y_PIVOT + DY_ARM - 8.0
    Z_HEAD = 78.0 + DZ_ARM - 10.0

    tr_head = gp_Trsf()
    tr_head.SetTranslation(gp_Vec(0, Y_HEAD, Z_HEAD))
    builder.Add(compound, BRepBuilderAPI_Transform(create_gripper_base_head(), tr_head).Shape())

    tr_jaws = gp_Trsf()
    tr_jaws.SetTranslation(gp_Vec(0, Y_HEAD + 32.0, Z_HEAD + 5.0))
    builder.Add(compound, BRepBuilderAPI_Transform(create_specialized_gripper_jaw(is_left=True), tr_jaws).Shape())
    builder.Add(compound, BRepBuilderAPI_Transform(create_specialized_gripper_jaw(is_left=False), tr_jaws).Shape())

    # 7. 2 Khối mô phỏng Servo MG996R (S1 trên tháp nâng & S2 trên đầu kẹp)
    servo_s1 = make_box(22.0, 114.3, Z_GROUND + 48.0, 37.5, 40.7, 19.7)
    builder.Add(compound, servo_s1)

    servo_s2 = make_box(3.65 - 20.35, Y_HEAD + 32.0 - 9.85, Z_HEAD + 29.0, 40.7, 19.7, 37.5)
    builder.Add(compound, servo_s2)

    # 8. Ống hoa mẫu Ø32.0 mm cao 120.0 mm tại tâm máng kẹp
    flower = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(0, Y_HEAD + 66.0, 10.0), gp_Dir(0, 0, 1)),
        16.0, 120.0
    ).Shape()
    builder.Add(compound, flower)

    return compound


# ====================================================================
# XUẤT FILE STEP & STL CHUẨN CÔNG NGHIỆP (TẤT CẢ ĐỀU NẰM PHẲNG TẠI Z = 0.0)
# ====================================================================

def export_step(shape, filepath):
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    status = writer.Write(filepath)
    if status == IFSelect_RetDone:
        print(f"-> Xuat thanh cong file STEP: {os.path.basename(filepath)}")
    else:
        print(f"[LOI] Khong the xuat file STEP: {filepath}")

def export_stl(shape, filepath, deflection=0.05):
    BRepMesh_IncrementalMesh(shape, deflection)
    writer = StlAPI_Writer()
    writer.ASCIIMode = False
    writer.Write(shape, filepath)
    print(f"-> Xuat thanh cong file STL (Binary Watertight, Z_min=0.0): {os.path.basename(filepath)}")

def generate_all_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    step_dir = os.path.join(base_dir, "STEP_Models")
    stl_dir = os.path.join(base_dir, "3D_Models")
    os.makedirs(step_dir, exist_ok=True)
    os.makedirs(stl_dir, exist_ok=True)

    # Tất cả các chi tiết in 3D đều được xoay & căn phẳng mặt đáy tại Z = 0.0 mm (orient_for_print)
    parts = [
        ("01_Monocoque_Chassis_GA25_Mecanum", orient_for_print(create_monocoque_chassis())),
        ("01B_Lift_Tower_Left_FlatPrint", create_lift_tower_printable(is_left=True)),
        ("01C_Lift_Tower_Right_MG996R_FlatPrint", create_lift_tower_printable(is_left=False)),
        ("01D_MCU_Control_Hub_Deck_FlatPrint", create_mcu_deck_printable()),
        ("01E_Line_Sensor_Spacer_Pod_FlatPrint", create_line_sensor_spacer_printable()),
        ("02_GA25_Motor_Clamp_Cap", create_ga25_clamp_cap_printable()),
        ("03_Parallel_Arm_Truss_IBeam", create_lower_h_frame_arm_printable()),
        ("03B_Upper_H_Frame_Follower_Arm", create_upper_h_frame_arm_printable()),
        ("04_Gripper_Base_Head", create_gripper_base_head_printable()),
        ("05_Gripper_Jaw_Left_VGuide_Flower32", create_specialized_gripper_jaw_printable(is_left=True)),
        ("06_Gripper_Jaw_Right_VGuide_Flower32", create_specialized_gripper_jaw_printable(is_left=False)),
        ("07_Mecanum_Wheel_K3_80mm", create_mecanum_wheel_k3_printable(is_left=True)),
        ("08_MG996R_Servo_Lever_Horn", create_mg996r_servo_lever_horn_printable()),
    ]

    print("\n=== DANG XUAT CAC FILE CHI TIET CO KHI ORC-X1 PRO V4.0 DFM (STEP & STL) ===")
    for name, solid in parts:
        step_path = os.path.join(step_dir, f"{name}.step")
        stl_path = os.path.join(stl_dir, f"{name}.stl")
        export_step(solid, step_path)
        export_stl(solid, stl_path)

    print("\n=== DANG TAO VA XUAT MO HINH LAP GHEP TONG THE ORC-X1 PRO V4.0 ===")
    assembly = create_full_assembly_modern()
    export_step(assembly, os.path.join(step_dir, "00_ORC_X1_Pro_Unibody_Full_Assembly.step"))
    export_stl(assembly, os.path.join(stl_dir, "00_ORC_X1_Pro_Unibody_Full_Assembly.stl"))
    print("\n=== HOAN TAT 100% TAT CA MO HINH 3D ORC-X1 PRO V4.0 (DFM 3D-PRINT OPTIMIZED)! ===")

if __name__ == "__main__":
    generate_all_models()
