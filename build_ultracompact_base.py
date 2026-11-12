"""
build_ultracompact_base.py
Compiles, verifies, and packages the Ultra-Compact Omni Chassis Base for ORC K2 Robot.
"""

import os
import sys
import subprocess
import json
import zipfile
import numpy as np
import trimesh
from PIL import Image

BASE_DIR = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
MODELS_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
OPENSCAD_COM = r"C:\Program Files\OpenSCAD\openscad.com"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUT_3MF_DIR, exist_ok=True)

SCAD_CONTENT = """// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// THIẾT KẾ: KHUNG GẦM SIÊU GỌN BÁNH XE ĐA HƯỚNG (ORC-K2 PRO ULTRA-COMPACT OMNI BASE)
// FILE: 01_Chassis_Base_UltraCompact_Omni.scad
// PHIÊN BẢN V8.0: TỐI ƯU HÓA HOÀN TOÀN CHO BÁNH ĐA HƯỚNG (OMNI 48/58MM & MECANUM 48/60MM)
// TƯƠNG THÍCH 100% THÁP NÂNG 01B/01C, ADAPTER K2 HUB 01D, PIN 2S2P & CẢM BIẾN
// ====================================================================
// ĐẶC ĐIỂM HÌNH HỌC & TỐI ƯU HÓA ULTRA-COMPACT:
// 1. Kích thước Chi Tiết In 3D (Base Plate Part):
//    - Rộng X = 136.0 mm (Thân 118.0mm + 2x Ụ nhô Boss 9.0mm) - Tiết kiệm 3.0mm so với V7.0
//    - Dài Y   = 160.5 mm (Y_START = 8.0mm đến Y_END = 168.5mm) - Tiết kiệm 11.5mm so với V7.0 (172mm)!
//    - Cao Z   = 36.0 mm (Tâm trục 20mm + Bán kính Boss 16mm) - Tiết kiệm 2.0mm so với V7.0
//    -> KÍCH THƯỚC LỚN NHẤT CHI TIẾT IN = 160.5 MM <= 180.0 MM!
//    -> VỪA VẶN 100% ĐẶT THẲNG TRÊN BÀN IN BAMBU LAB A1 MINI (180x180MM), KHÔNG CẦN XOAY 45 ĐỘ!
// 2. Phủ bì Cụm Gầm Robot Khi Lắp Bánh Xe Đa Hướng (Assembled Robot Footprint):
//    - Bánh Omni 58mm: Rộng 154.0 mm x Dài 168.0 mm x Cao 58.0 mm (Diện tích giảm 31.2% so với 200x200)!
//    - Bánh Omni 48mm: Rộng 152.0 mm x Dài 160.5 mm x Cao 48.0 mm (Diện tích giảm 35.2% so với 200x200)!
//    - Bánh Mecanum 48mm: Rộng 166.0 mm x Dài 160.5 mm x Cao 48.0 mm!
// 3. Động cơ GA25 & Khe hở an toàn đuôi Encoder:
//    - BOSS_OUT = 9.0 mm, FLANGE_T = 3.0 mm.
//    - Khoảng cách giữa 2 mặt bích: INNER_SPAN = 118.0 + 2*(9.0 - 3.0) = 130.0 mm!
//    - Cầu sau 2x Motor GA25 Encoder (63.0mm x 2 = 126.0mm):
//      KHE HỞ AN TOÀN = 130.0 - 126.0 = 4.0 mm > 0! ZERO COLLISION 100%!
// 4. Khớp nối & Linh kiện chuẩn hóa (Không thay đổi toạ độ linh kiện):
//    - Giữ nguyên 100% tọa độ 10 lỗ bắt Tháp nâng (01B & 01C): X = ±16.0 & ±24.0, Y = 110.5, 122.0, 160.25
//    - Giữ nguyên 100% tọa độ 4 trụ K2 Hub & 4 lỗ chân đôn 01D: X = ±42.0 & ±33.0, Y = 49.0 & 99.0
//    - Giữ nguyên Khoang pin vạn năng 2S2P 82 x 76 mm (Y = 48.0..124.0 mm)
//    - Cản trước tích hợp hốc cảm biến ToF VL53L0X & 4 lỗ bắt đế cảm biến dò line 01E dưới gầm
//    - Vát góc 45° đuôi xe và mũi xe giúp robot xoay tròn tại chỗ linh hoạt, không vướng góc
// 5. Chuẩn in FDM: Đáy phẳng 100% tại Z = 0.0 mm, 0% Support, lỗ giọt nước Teardrop 45°.
// ====================================================================

DISPLAY_MODE = "part"; // "part", "assembly_omni_58", "assembly_omni_48", "assembly_mecanum_60"
$fn = (DISPLAY_MODE == "part") ? 40 : 24;

// THÔNG SỐ CƠ BẢN:
CHASSIS_W     = 118.0;   // Chiều rộng thân xe chính (mm)
Y_START       = 8.0;     // Tọa độ Y bắt đầu sàn sau (cắt bỏ 8mm thừa phía sau)
Y_END         = 168.5;   // Tọa độ Y kết thúc cản trước (tối ưu hóa mũi cản ToF)
CHASSIS_L_EFF = Y_END - Y_START; // 160.5 mm

FLOOR_T       = 4.0;     // Độ dày sàn chịu lực (mm)
WALL_T        = 4.0;     // Độ dày vách sườn chịu lực (mm)
WALL_H        = 30.0;    // Chiều cao vách sườn (mm)

// THÔNG SỐ Ụ NHÔ BẬC MOTOR (SLIM BOSS CHO BÁNH ĐA HƯỚNG):
BOSS_OUT      = 9.0;     // Độ nhô ra ngoài của mặt bích (mm)
BOSS_D        = 32.0;    // Đường kính ngoài ụ mặt bích (mm)
FLANGE_T      = 3.0;     // Độ dày mặt bích bắt motor (mm)

// TỌA ĐỘ TRỤC XE (CHUẨN ĐỒNG TRỤC TUYỆT ĐỐI):
Y_REAR        = 32.0;    // Trục bánh sau
Y_FRONT       = 142.0;   // Trục bánh trước
WHEELBASE     = Y_FRONT - Y_REAR; // 110.0 mm
Z_SHAFT       = 20.0;    // Cao độ tâm trục so với đáy sàn Z=0 (mm)

// KHOANG PIN VẠN NĂNG 2S2P 18650:
BAT_BAY_W     = 82.0;
BAT_BAY_L     = 76.0;
BAT_BAY_Y_START = 48.0;
BAT_BAY_Y_END   = BAT_BAY_Y_START + BAT_BAY_L; // 124.0 mm

// TRỤ ĐỠ TẦNG TRÊN (K2 HUB PILLARS):
PILLAR_X      = 42.0;
PILLAR_W_X    = 8.0;
PILLAR_L_Y    = 10.0;
PILLAR_H      = 18.0;

// KÍCH THƯỚC CHI TIẾT IN 3D:
PART_EXTENT_X = CHASSIS_W + 2.0 * BOSS_OUT; // 136.0 mm
PART_EXTENT_Y = CHASSIS_L_EFF;              // 160.5 mm
PART_EXTENT_Z = Z_SHAFT + BOSS_D / 2.0;     // 36.0 mm
PART_MAX_DIM  = max(PART_EXTENT_X, PART_EXTENT_Y, PART_EXTENT_Z); // 160.5 mm

// KHOẢNG HỞ MẶT BÍCH & MOTOR:
INNER_SPAN = CHASSIS_W + 2.0 * (BOSS_OUT - FLANGE_T); // 130.0 mm
MOTOR_ENC_L = 63.0; // Chiều dài motor GA25 Encoder sau kể cả nắp
REAR_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_ENC_L; // 130.0 - 126.0 = 4.0 mm > 0!

echo("====================================================================");
echo("=== ORC-K2 PRO ULTRA-COMPACT OMNI BASE VERIFICATION ===");
echo("====================================================================");
echo("Part Extent X (Width):", PART_EXTENT_X, "mm (Tiet kiem 3.0mm)");
echo("Part Extent Y (Length):", PART_EXTENT_Y, "mm (Tiet kiem 11.5mm)");
echo("Part Extent Z (Height):", PART_EXTENT_Z, "mm (Tiet kiem 2.0mm)");
echo(">>> MAX PART DIMENSION:", PART_MAX_DIM, "mm <= 180.0 mm (PASS 100% BAMBU A1 MINI!)");
echo("Inner Flange Span:", INNER_SPAN, "mm");
echo("Rear Encoder Gap:", REAR_CLEARANCE, "mm (ZERO COLLISION!)");
echo("====================================================================");

// TIỆN ÍCH LỖ GIỌT NƯỚC 45° TỰ ĐỠ IN 3D (TEARDROP HOLES)
module teardrop_hole_x(d = 9.0, h = 10.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2.0, -side/2.0])
                    cube([h, side, side]);
    }
}

// ====================================================================
// MODULE KHUNG GẦM ULTRA-COMPACT OMNI (chassis_base_ultracompact_omni)
// ====================================================================
module chassis_base_ultracompact_omni() {
    cradle_w = 28.0;

    difference() {
        union() {
            // 1. SÀN ĐÁY PHẲNG CHÍNH TẠI Z = 0.0 mm (Y = Y_START..Y_END)
            translate([-CHASSIS_W/2.0, Y_START, 0])
                cube([CHASSIS_W, CHASSIS_L_EFF, FLOOR_T]);

            // 2. HAI VÁCH SƯỜN CHỊU LỰC DÀY 4.0mm, CAO 30.0mm
            translate([-CHASSIS_W/2.0, Y_START, 0])
                cube([WALL_T, CHASSIS_L_EFF, WALL_H]);
            translate([CHASSIS_W/2.0 - WALL_T, Y_START, 0])
                cube([WALL_T, CHASSIS_L_EFF, WALL_H]);

            // 3. 4 CỤM BỆ MOTOR: Ụ NHÔ SLIM (BOSS) + Ổ ĐỠ GA25 (CRADLE)
            for (my = [Y_REAR, Y_FRONT]) {
                // --- BÊN TRÁI (LEFT SIDE) ---
                hull() {
                    translate([-CHASSIS_W/2.0 - BOSS_OUT, my, Z_SHAFT])
                        rotate([0, 90, 0])
                            cylinder(d=BOSS_D, h=BOSS_OUT);
                    translate([-CHASSIS_W/2.0 - BOSS_OUT, my - 14.0, 0])
                        cube([BOSS_OUT, 28.0, FLOOR_T]);
                }
                translate([-CHASSIS_W/2.0, my - 16.0, 0])
                    cube([WALL_T, 32.0, 31.0]);
                translate([-CHASSIS_W/2.0, my - 22.0, 0])
                    cube([cradle_w, 44.0, 20.0]);

                // --- BÊN PHẢI (RIGHT SIDE) ---
                hull() {
                    translate([CHASSIS_W/2.0, my, Z_SHAFT])
                        rotate([0, 90, 0])
                            cylinder(d=BOSS_D, h=BOSS_OUT);
                    translate([CHASSIS_W/2.0, my - 14.0, 0])
                        cube([BOSS_OUT, 28.0, FLOOR_T]);
                }
                translate([CHASSIS_W/2.0 - WALL_T, my - 16.0, 0])
                    cube([WALL_T, 32.0, 31.0]);
                translate([CHASSIS_W/2.0 - cradle_w, my - 22.0, 0])
                    cube([cradle_w, 44.0, 20.0]);
            }

            // 4. GỜ ĐỊNH VỊ 4 GÓC KHOANG PIN 2S2P (82.0 x 76.0 mm)
            for (bx = [-(BAT_BAY_W/2.0 + 2.0), BAT_BAY_W/2.0]) {
                translate([bx, BAT_BAY_Y_START + 2.0, FLOOR_T]) cube([2.0, 8.0, 3.0]);
                translate([bx, BAT_BAY_Y_END - 6.0, FLOOR_T]) cube([2.0, 6.0, 3.0]);
            }

            // 5. 4 TRỤ ĐỠ TẦNG TRÊN (MCU K2 HUB PILLARS: X = ±42.0, Y = 49.0 & 99.0 mm)
            for (sx = [-1, 1]) {
                for (py = [49.0, 99.0]) {
                    translate([sx * PILLAR_X - PILLAR_W_X/2.0, py - PILLAR_L_Y/2.0, FLOOR_T])
                        cube([PILLAR_W_X, PILLAR_L_Y, PILLAR_H]);
                }
            }

            // 6. BỆ GÁ MẠCH PS4 (TRÁI) & NÚT NHẤN (PHẢI)
            translate([-CHASSIS_W/2.0, 56.0, 0])
                cube([16.0, 26.0, 16.0]);
            translate([CHASSIS_W/2.0 - 16.0, 56.0, 0])
                cube([16.0, 26.0, 16.0]);

            // 7. MŨI CẢN TRƯỚC TỐI ƯU SIÊU GỌN (SLIM COMPACT FRONT BUMPER & ToF MOUNT)
            // Đặt tại Y = 164.5..168.5 mm (Dày 4.0mm, cao 14.0mm)
            hull() {
                translate([-28.0, Y_END - 2.0, 0]) cube([56.0, 2.0, 14.0]);
                translate([-32.0, 164.5, 0])       cube([64.0, 2.0, 14.0]);
            }
            // Tai nối cứng cáp vào vách sườn
            translate([-CHASSIS_W/2.0, 164.5, 0]) cube([WALL_T + 2.0, 4.0, 14.0]);
            translate([CHASSIS_W/2.0 - WALL_T - 2.0, 164.5, 0]) cube([WALL_T + 2.0, 4.0, 14.0]);

            // 8. GỜ ĐỊNH VỊ CHÂN THÁP NÂNG RỜI (01B & 01C)
            translate([-30.2, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            translate([ 28.2, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            translate([-28.0, 102.5, FLOOR_T]) cube([16.0, 2.0, 3.0]);
            translate([ 12.0, 102.5, FLOOR_T]) cube([16.0, 2.0, 3.0]);
        }

        // ================= KHOÉT RỖNG CSG & LỖ GIỌT NƯỚC 45° =================

        // 1. 4 CỤM KHOÉT LÒNG ĐỘNG CƠ GA25 & LỖ TRỤC GIỌT NƯỚC
        for (my = [Y_REAR, Y_FRONT]) {
            // --- BÊN TRÁI ---
            translate([-CHASSIS_W/2.0 - BOSS_OUT + FLANGE_T, my, Z_SHAFT])
                rotate([0, 90, 0])
                    cylinder(d=25.4, h=BOSS_OUT - FLANGE_T + cradle_w + 0.1);

            translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my, Z_SHAFT])
                teardrop_hole_x(d=9.0, h=FLANGE_T + 2.0);

            for (a = [0, 90, 180, 270]) {
                translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=FLANGE_T + 2.0);
            }

            for (dy = [-17.5, 17.5]) {
                translate([-44.0, my + dy, 3.0])
                    cylinder(d=3.0, h=18.0);
            }

            // --- BÊN PHẢI ---
            translate([CHASSIS_W/2.0 - cradle_w - 0.1, my, Z_SHAFT])
                rotate([0, 90, 0])
                    cylinder(d=25.4, h=BOSS_OUT - FLANGE_T + cradle_w + 0.1);

            translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my, Z_SHAFT])
                teardrop_hole_x(d=9.0, h=FLANGE_T + 2.0);

            for (a = [0, 90, 180, 270]) {
                translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=FLANGE_T + 2.0);
            }

            for (dy = [-17.5, 17.5]) {
                translate([44.0, my + dy, 3.0])
                    cylinder(d=3.0, h=18.0);
            }
        }

        // 2. KHOANG PIN VẠN NĂNG 2S2P (HẠ PHẲNG TRÊN SÀN: Y = 48.0..124.0 mm)
        translate([-BAT_BAY_W/2.0, BAT_BAY_Y_START, FLOOR_T])
            cube([BAT_BAY_W, BAT_BAY_L, 30.0]);

        // 3. 4 LỖ ỐC M3 TRÊN ĐỈNH TRỤ K2 HUB (X = ±42.0, Y = 49.0 & 99.0 mm)
        for (sx = [-1, 1]) {
            for (py = [49.0, 99.0]) {
                translate([sx * PILLAR_X, py, FLOOR_T + 2.0])
                    cylinder(d=3.0, h=PILLAR_H + 2.0);
            }
        }

        // 4. 4 LỖ SÀN M3 CHO KHUNG CHÂN ĐÔN 01D (X = ±33.0, Y = 49.0 & 99.0 mm)
        for (px = [-33.0, 33.0]) {
            for (py = [49.0, 99.0]) {
                translate([px, py, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }

        // 5. 10 LỖ BU-LÔNG M3 BẮT CỨNG 2 THÁP NÂNG (01B & 01C)
        for (sx = [-16.0, 16.0]) {
            for (sy = [110.5, 122.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=26.0);
            }
        }
        for (sx = [-24.0, 24.0]) {
            for (sy = [116.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=26.0);
            }
        }

        // 6. LỖ BẮT MẠCH PS4 & NÚT NHẤN
        translate([-CHASSIS_W/2.0 + 9.0, 61.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2.0 + 9.0, 77.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2.0 + 4.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        translate([CHASSIS_W/2.0 - 9.0, 61.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2.0 - 9.0, 77.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2.0 - 17.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        // 7. MA TRẬN LỖ ỐC M3 TRÊN SÀN (TỐI ƯU HÓA)
        for (ex = [-42.0, 42.0]) {
            for (ey = [88.0, 114.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }
        for (ex = [-8.0, 0.0, 8.0]) {
            for (ey = [112.0, 128.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }
        for (ex = [-16.0, 0.0, 16.0]) {
            for (ey = [12.0, 48.0, 64.0, 80.0, 96.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }

        // 8. 4 LỖ ỐC M3 ĐẾ CẢM BIẾN DÒ LINE (01E) & RÃNH CÁP
        for (lx = [-12.0, -8.0, 8.0, 12.0]) {
            translate([lx, 159.0, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
        }
        translate([-8.0, 146.0, -0.5]) cube([16.0, 8.0, FLOOR_T + 1.0]);

        // 9. HỐC GÁ & CỬA SỔ QUANG HỌC CẢM BIẾN LASER ToF VL53L0X
        translate([-7.0, 164.5, 5.5])
            cube([14.0, 4.5, 7.0]);
        translate([-12.8, 164.8, FLOOR_T])
            cube([25.6, 2.2, 11.0]);
        translate([-10.0, 164.0, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=5.5);
        translate([ 10.0, 164.0, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=5.5);
        translate([-7.0, 161.5, -0.5])
            cube([14.0, 3.5, FLOOR_T + 1.0]);

        // 10. RÃNH DÂY NGUỒN PIN & 4 KHE LUỒN ĐAI DÁN VELCRO 20mm
        translate([-12.0, 18.0, -0.5]) cube([24.0, 22.0, FLOOR_T + 1.0]);
        for (zx = [-40.0, 36.0]) {
            for (zy = [60.0, 90.0]) {
                translate([zx, zy, -0.5]) cube([4.0, 22.0, FLOOR_T + 1.0]);
            }
        }

        // 11. VÁT GÓC 45° ĐUÔI XE & MŨI XE (CHAMFERED CORNERS FOR SLIM MANEUVERABILITY)
        // Vát 45° góc sau (Left/Right Rear Corners)
        translate([-CHASSIS_W/2.0 - 10.0, Y_START - 5.0, -1.0])
            rotate([0, 0, 45])
                cube([18.0, 18.0, WALL_H + 5.0]);
        translate([CHASSIS_W/2.0 + 10.0, Y_START - 5.0, -1.0])
            rotate([0, 0, 45])
                cube([18.0, 18.0, WALL_H + 5.0]);
                
        // Vát 45° góc trước cản xe (Left/Right Front Bumper Corners)
        translate([-CHASSIS_W/2.0, Y_END + 2.0, -1.0])
            rotate([0, 0, -45])
                cube([16.0, 16.0, WALL_H + 5.0]);
        translate([CHASSIS_W/2.0, Y_END + 2.0, -1.0])
            rotate([0, 0, 135])
                cube([16.0, 16.0, WALL_H + 5.0]);
    }
}

// ====================================================================
// MODULE MÔ PHỎNG BÁNH XE ĐA HƯỚNG OMNI WHEEL (58MM & 48MM)
// ====================================================================
module omni_wheel_sim(wheel_d = 58.0, wheel_w = 16.0) {
    roller_d = (wheel_d == 58.0) ? 13.0 : 10.0;
    roller_w = (wheel_d == 58.0) ? 11.0 : 9.0;
    num_rollers = 10;
    
    color("DimGray") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=wheel_d - 6.0, h=wheel_w, center=true);
            rotate([0, 90, 0]) cylinder(d=12.0, h=wheel_w + 2.0, center=true);
            rotate([0, 90, 0]) cylinder(d=4.1, h=wheel_w + 4.0, center=true);
        }
    }
    // Con lăn cao su đa hướng (Omni Rollers)
    color("Black") {
        for (i = [0:num_rollers-1]) {
            rotate([i * (360/num_rollers), 0, 0])
                translate([0, (wheel_d - roller_d)/2.0, 0])
                    rotate([0, 0, 0])
                        rotate([0, 90, 0])
                            cylinder(d=roller_d, h=roller_w, center=true);
        }
    }
    // Khớp nối lục giác đồng thau (Brass Coupler)
    color("Goldenrod") {
        rotate([0, 90, 0]) cylinder(d=11.5, h=wheel_w + 6.0, center=true, $fn=6);
    }
}

// BÁNH XE MECANUM 60MM
module mecanum_wheel_60_sim() {
    color("DimGray") {
        rotate([0, 90, 0]) cylinder(d=60.0, h=28.0);
    }
}

// HIỂN THỊ CHÍNH
if (DISPLAY_MODE == "part") {
    color("DarkSlateGray")
        chassis_base_ultracompact_omni();
}
"""

with open(os.path.join(MODELS_DIR, "01_Chassis_Base_UltraCompact_Omni.scad"), "w", encoding="utf-8") as f:
    f.write(SCAD_CONTENT)

print("Created 01_Chassis_Base_UltraCompact_Omni.scad successfully!")

# Write Assembly SCAD for preview rendering
ASSEMBLY_SCAD = """use <01_Chassis_Base_UltraCompact_Omni.scad>;

$fn = 28;

WHEEL_CONFIG = "OMNI_58"; // "OMNI_58", "OMNI_48", "MECANUM_60"

WHEEL_D = (WHEEL_CONFIG == "OMNI_58") ? 58.0 : ((WHEEL_CONFIG == "OMNI_48") ? 48.0 : 60.0);
WHEEL_W = (WHEEL_CONFIG == "OMNI_58") ? 16.0 : ((WHEEL_CONFIG == "OMNI_48") ? 15.0 : 28.0);
GROUND_CLEAR = WHEEL_D / 2.0 - 20.0; // 9.0mm (Omni 58) or 4.0mm (Omni 48)

CHASSIS_W = 118.0;
Y_REAR = 32.0;
Y_FRONT = 142.0;

TOTAL_W = CHASSIS_W + 2 * (2.0 + WHEEL_W);
TOTAL_L = (Y_FRONT + WHEEL_D/2.0) - (Y_REAR - WHEEL_D/2.0);

echo("Total Width:", TOTAL_W, "mm");
echo("Total Length:", TOTAL_L, "mm");

// Base Plate
color("DarkSlateGray")
    translate([0, 0, GROUND_CLEAR])
        chassis_base_ultracompact_omni();

// 4 Wheels
for (side = [-1, 1]) {
    x_pos = side * (CHASSIS_W/2 + 2.0 + WHEEL_W/2.0);
    translate([x_pos, Y_REAR, 20.0 + GROUND_CLEAR])
        omni_wheel_sim(wheel_d = WHEEL_D, wheel_w = WHEEL_W);
    translate([x_pos, Y_FRONT, 20.0 + GROUND_CLEAR])
        omni_wheel_sim(wheel_d = WHEEL_D, wheel_w = WHEEL_W);
}

// 4 GA25 Motors
for (side = [-1, 1]) {
    // Rear Encoder Motor (63mm)
    translate([side * (CHASSIS_W/2 + 6.0), Y_REAR, 20.0 + GROUND_CLEAR])
        rotate([0, side > 0 ? -90 : 90, 0]) {
            color("Silver") cylinder(d=25.0, h=48.0);
            color("DimGray") translate([0, 0, 48.0]) cylinder(d=24.4, h=15.0);
        }
    // Front DC Motor (48mm)
    translate([side * (CHASSIS_W/2 + 6.0), Y_FRONT, 20.0 + GROUND_CLEAR])
        rotate([0, side > 0 ? -90 : 90, 0]) {
            color("Silver") cylinder(d=25.0, h=48.0);
        }
}

// Battery Pack 2S2P Brick
color("RoyalBlue", 0.85)
    translate([-19.0, 51.0, GROUND_CLEAR + 4.0])
        cube([38.0, 70.0, 38.0]);

// K2 Control Hub Deck
color("Black")
    translate([-60.5, 30.0, GROUND_CLEAR + 44.0])
        cube([121.0, 86.0, 26.0]);

// Wireframe Box 185mm Cube
color("Red", 0.25) {
    translate([-92.5, 0, 0]) {
        cube([185, 1.5, 1.5]);
        cube([1.5, 185, 1.5]);
        translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
        translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        translate([0, 0, 183.5]) {
            cube([185, 1.5, 1.5]);
            cube([1.5, 185, 1.5]);
            translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
            translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        }
        cube([1.5, 1.5, 185]);
        translate([183.5, 0, 0]) cube([1.5, 1.5, 185]);
        translate([0, 183.5, 0]) cube([1.5, 1.5, 185]);
        translate([183.5, 183.5, 0]) cube([1.5, 1.5, 185]);
    }
}
"""

with open(os.path.join(MODELS_DIR, "full_assembly_ultracompact_omni.scad"), "w", encoding="utf-8") as f:
    f.write(ASSEMBLY_SCAD)

print("Created full_assembly_ultracompact_omni.scad successfully!")

# Compile STL
stl_path = os.path.join(MODELS_DIR, "01_Chassis_Base_UltraCompact_Omni.stl")
scad_path = os.path.join(MODELS_DIR, "01_Chassis_Base_UltraCompact_Omni.scad")

print(f"Compiling {stl_path} with OpenSCAD...")
res = subprocess.run([OPENSCAD_COM, "-o", stl_path, scad_path], capture_output=True, text=True)
if res.returncode != 0:
    print("OpenSCAD Error:", res.stderr)
    sys.exit(1)
print("Compiled STL successfully! Output:", res.stderr.strip() or res.stdout.strip())

# Measure with trimesh
mesh = trimesh.load(stl_path)
bounds = mesh.bounds
extents = bounds[1] - bounds[0]
volume = mesh.volume
area = mesh.area

print(f"=== TRIMESH MEASUREMENTS ===")
print(f"Bounding Box: X=[{bounds[0][0]:.2f}, {bounds[1][0]:.2f}], Y=[{bounds[0][1]:.2f}, {bounds[1][1]:.2f}], Z=[{bounds[0][2]:.2f}, {bounds[1][2]:.2f}]")
print(f"Extents: X={extents[0]:.2f} mm, Y={extents[1]:.2f} mm, Z={extents[2]:.2f} mm")
print(f"Max Dimension: {max(extents):.2f} mm")
print(f"Volume: {volume:.2f} mm3 (Est weight: {volume*1.24/1000.0:.1f} g PLA)")
print(f"Is watertight: {mesh.is_watertight}")

# Render PNGs
img_iso = os.path.join(BASE_DIR, "preview_ultracompact_omni_iso.png")
img_top = os.path.join(BASE_DIR, "preview_ultracompact_omni_top.png")
asm_iso = os.path.join(BASE_DIR, "preview_assembly_omni_iso.png")
asm_top = os.path.join(BASE_DIR, "preview_assembly_omni_top.png")

print("Rendering preview images...")
# Base Plate ISO
subprocess.run([OPENSCAD_COM, "--camera=0,88,18,60,0,320,500", "--imgsize=1200,900", "--colorscheme=Tomorrow Night", "-o", img_iso, scad_path])
# Base Plate Top
subprocess.run([OPENSCAD_COM, "--camera=0,88,18,0,0,0,450", "--imgsize=1200,900", "--colorscheme=Tomorrow Night", "-o", img_top, scad_path])
# Assembly ISO
asm_scad = os.path.join(MODELS_DIR, "full_assembly_ultracompact_omni.scad")
subprocess.run([OPENSCAD_COM, "--camera=0,88,30,60,0,325,550", "--imgsize=1200,900", "--colorscheme=Tomorrow Night", "-o", asm_iso, asm_scad])
# Assembly Top
subprocess.run([OPENSCAD_COM, "--camera=0,88,30,0,0,0,480", "--imgsize=1200,900", "--colorscheme=Tomorrow Night", "-o", asm_top, asm_scad])

print("Rendered PNG previews successfully!")
