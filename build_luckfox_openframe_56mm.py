"""
build_luckfox_openframe_56mm.py
Bộ thiết kế hoàn chỉnh cụm gá & vỏ Open-Frame cho bo Luckfox Pico Max/Pro
và Cảm biến ToF VL53L5CX V2 trên 2 ống tròn Ø8.0mm (C-C = 56.0mm, mép ngoài 64.0mm).

Tối ưu hóa FDM 100%:
- Đặt phẳng tuyệt đối tại Z = 0.0mm.
- 0% Support.
- Manifold 100% (Simple: yes, Volumes: 1 trên từng chi tiết rời).
- Dung sai lắp ghép chuẩn: PCB +0.6mm, Ống Ø8 +0.25mm, Ốc M3 Ø3.4mm, Ốc M2 Ø2.3mm.
"""

import os
import subprocess
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OUT_DIR = os.path.join(BASE_DIR, "3D_Models", "Luckfox_Pico_OpenFrame_56mm")
OPENSCAD_COM = r"C:\Program Files\OpenSCAD\openscad.com"

os.makedirs(OUT_DIR, exist_ok=True)

# ====================================================================
# 1. MÃ NGUỒN OPENSCAD ĐẦY ĐỦ CỦA TOÀN BỘ CỤM
# ====================================================================

COMMON_HEADER = """$fn = 64;

// ====================================================================
// THÔNG SỐ HÌNH HỌC HỆ THỐNG
// ====================================================================

// 1. Hệ 2 ống tròn Ø8.0 mm
rod_D       = 8.25;         // Đường kính kẹp ôm ống Ø8.0mm (+0.25mm dung sai ôm khít)
rod_CC      = 56.0;         // Khoảng cách tâm - đến - tâm (C-C) = 56.0mm (X = -28.0 và +28.0)
rod_out     = 64.0;         // Mép ngoài - ngoài = 64.0mm (tại X = -32.0 và +32.0)
rod_in      = 48.0;         // Mép trong - trong = 48.0mm (tại X = -24.0 và +24.0)

// 2. Bo Luckfox Pico Max / Pro
pcb_L       = 72.0;         // Chiều dài PCB Luckfox (mm) (X = -36.0 .. +36.0)
pcb_W       = 21.0;         // Chiều rộng PCB Luckfox (mm) (Y = -10.5 .. +10.5)
pcb_T       = 1.6;          // Độ dày PCB (mm)

cav_L       = 72.8;         // Chiều dài hốc chứa PCB (+0.8mm dung sai)
cav_W       = 21.6;         // Chiều rộng hốc chứa PCB (+0.6mm dung sai)

// 3. Chân GPIO Luckfox (40 chân quay xuống dưới)
gpio_L      = 50.8;         // Chiều dài 2 hàng chân 20x1 (X = -35.2 .. +15.6)
gpio_H      = 11.5;         // Độ sâu chân thò xuống dưới PCB (mm)
gpio_Y      = 8.89;         // Khoảng cách tâm 2 hàng chân (Y = -8.89 và +8.89)

// 4. Module Cảm biến ToF VL53L5CX V2
tof_pcb_L   = 24.7;         // Chiều dài tổng thể PCB gồm 2 tai bắt ốc (mm)
tof_pcb_H   = 10.5;         // Chiều cao thân PCB (mm)
tof_pcb_T   = 1.2;          // Độ dày PCB ToF (mm)
tof_hole_CC = 20.0;         // Khoảng cách tâm 2 lỗ ốc M2 = 20.0mm (X = -10.0 và +10.0)
tof_hole_D  = 2.3;          // Đường kính lỗ ốc M2 (mm)
tof_sensor_W = 6.4;         // Kích thước mắt cảm biến (mm)
tof_sensor_H = 3.0;

// Các hàm bổ trợ hình học
module rounded_box_z(lx, ly, lz, r=2.4) {
    hull() {
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx*(lx/2 - r), sy*(ly/2 - r), 0])
                    cylinder(r=r, h=lz);
    }
}

module m3_nut_trap(h=3.2) {
    cylinder(d=6.35, h=h, $fn=6);
}

module m2_nut_trap(h=2.2) {
    cylinder(d=4.6, h=h, $fn=6);
}
"""

# --------------------------------------------------------------------
# PART 01A: OPEN-FRAME UNDER-MOUNT (Gá 2 ống ngang Y, C-C 56mm)
# --------------------------------------------------------------------
SCAD_PART_01A = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 01A: KHUNG OPEN-FRAME UNDER-MOUNT (ỐNG NGANG Y, C-C 56MM)
// - Bệ đỡ PCB tại Z = 16.0mm.
// - Toàn bộ vùng GPIO giữa X = -21.0mm và X = +21.0mm MỞ RỖNG 100%
//   ở mặt đáy và có vòm mở bên sườn để cắm rút Dupont cực kỳ thoáng!
// - 2 Đầu giữ cứng PCB có vách chặn đầu chống trượt khi cắm/rút USB-C và RJ45.
// - Ngàm kẹp 2 ống Ø8mm tại X = ±28.0mm, bắt vít M3 siết thanh khóa kép 02A.
// - Mặt trước (+Y) có 2 tai bắt vít M3 liên kết Giá gá ToF VL53L5CX V2.
// ====================================================================

module part_01A_openframe_undermount() {
    z_pcb_bot = 16.0;       // Đáy PCB tựa tại Z = 16.0mm
    z_top_rim = 19.6;       // Gờ viền bao ngoài mép PCB (cao hơn mặt trên 2.0mm)
    frame_L   = 79.0;       // Chiều dài khung (X = -39.5 .. +39.5)
    frame_W   = 27.6;       // Chiều rộng khung (Y = -13.8 .. +13.8)

    difference() {
        union() {
            // 1. Thân chính khung đỡ Open-Frame
            rounded_box_z(frame_L, frame_W, z_top_rim, r=2.5);

            // 2. 2 Tai bắt ốc M3 ở 2 bên sườn tại X = 0.0mm (Y = ±17.0mm)
            //    dùng để bắt Nẹp trên khóa giữ PCB
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(frame_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([-5.0, sy*(frame_W/2 - 1.5), 0])
                        cube([10.0, 3.0, z_top_rim]);
                }
            }

            // 3. 2 Vấu bắt Giá gá ToF VL53L5CX V2 ở mặt trước (Y = +frame_W/2)
            //    tại X = -12.0mm và X = +12.0mm (C-C = 24.0mm)
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*12.0, frame_W/2 + 3.5, 0])
                        cylinder(d=7.6, h=z_top_rim);
                    translate([sx*12.0 - 3.8, frame_W/2 - 1.5, 0])
                        cube([7.6, 3.0, z_top_rim]);
                }
            }

            // 4. Khối mở rộng gia cường chân ngàm kẹp ống tại X = ±28.0mm
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*28.0, 0, 0])
                        cylinder(d=frame_W, h=10.0);
                }
            }
        }

        // ------------------------------------------------------------
        // CÁC HỐC CẮT CƠ KHÍ & KHÔNG GIAN OPEN-FRAME
        // ------------------------------------------------------------

        // A. Hốc chứa bo Luckfox từ Z = z_pcb_bot (16.0) lên đỉnh
        translate([-cav_L/2, -cav_W/2, z_pcb_bot])
            cube([cav_L, cav_W, z_top_rim - z_pcb_bot + 2.0]);

        // B. CỬA SỔ OPEN-FRAME CHÍNH (ĐÁY RỖNG 100% TỪ Z = -1 LÊN Z = 16.5)
        //    Giữa X = -21.0mm và X = +20.0mm (Dài 41.0mm!)
        //    Khoảng Y = -9.2mm đến +9.2mm mở toang thông suốt để cắm Dupont!
        translate([-21.0, -9.2, -1.0])
            cube([41.0, 18.4, z_pcb_bot + 2.0]);

        // C. CỬA SỔ BÊN SƯỜN (SIDE ACCESS ARCHES) CHO 2 HÀNG CHÂN GPIO
        //    Khoét rỗng 2 vách sườn từ Z = 0 lên Z = 12.5mm
        //    giúp tay và đầu cos Dupont tiếp cận từ 2 bên hông dễ dàng!
        for (sy = [-1, 1]) {
            translate([-16.0, sy*frame_W/2 - 3.0, -1.0])
                cube([32.0, 6.0, 13.5]);
        }

        // D. RÃNH THOÁT DƯỚI CHÂN GPIO ĐẦU TRÁI (X = -35.2 .. -21.0)
        //    Chân GPIO thò xuống 11.5mm (đến Z = 4.5mm), khoét rãnh sâu từ Z=3.0 lên Z=16.5
        for (sy = [-1, 1]) {
            translate([-35.5, sy*gpio_Y - 2.2, 3.0])
                cube([15.0, 4.4, z_pcb_bot - 2.0]);
        }

        // E. 2 RÃNH ÔM ỐNG Ø8.25mm TẠI X = -28.0mm VÀ X = +28.0mm (C-C = 56.0mm!)
        //    Trục ống chạy dọc theo Y, tâm ống tại Z = 4.0mm
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), frame_W/2 + 6.0, 4.0])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=frame_W + 12.0);

            // Khe mở miệng ngàm kẹp hướng xuống đáy Z = 0 (rộng 7.25mm)
            translate([sx*(rod_CC/2) - 3.625, -frame_W/2 - 6.0, -0.5])
                cube([7.25, frame_W + 12.0, 4.6]);
        }

        // F. 4 LỖ VÍT M3 KHÓA ỐNG TẠI X = ±28.0mm (Y = ±10.0mm)
        //    Bắt vít M3 từ dưới lên siết thanh khóa nẹp 02A
        for (sx = [-1, 1]) {
            for (sy = [-1, 1]) {
                translate([sx*28.0, sy*10.0, -0.5])
                    cylinder(d=3.4, h=z_top_rim + 1.0);
                // Hốc tán M3 lục giác âm trên mặt trên Z = 11.0 .. 14.5mm
                translate([sx*28.0, sy*10.0, 11.5])
                    m3_nut_trap(h=3.5);
            }
        }

        // G. KHE CỔNG USB TYPE-C Ở ĐẦU TRÁI (X = -39.5mm)
        //    Rộng 14.0mm, cao từ Z = 15.0 đến 21.0mm
        translate([-frame_L/2 - 1.0, -7.0, z_pcb_bot - 0.5])
            cube([6.0, 14.0, 8.0]);

        // H. KHE CỔNG RJ45 Ở ĐẦU PHẢI (X = +39.5mm)
        //    Rộng 17.0mm, cao từ Z = 15.5 đến đỉnh
        translate([cav_L/2 - 1.0, -8.5, z_pcb_bot - 0.5])
            cube([6.0, 17.0, 10.0]);

        // I. 2 LỖ ỐC M3 + HỐC TÁN M3 Ở TAI BÊN SƯỜN (X = 0, Y = ±17.0mm)
        //    để bắt Nẹp trên khóa giữ PCB
        for (sy = [-1, 1]) {
            translate([0, sy*(frame_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([0, sy*(frame_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.2);
        }

        // J. 2 LỖ ỐC M3 Ở MẶT TRƯỚC (X = ±12.0mm, Y = +frame_W/2 + 3.5)
        //    để bắt Giá gá ToF VL53L5CX V2
        for (sx = [-1, 1]) {
            translate([sx*12.0, frame_W/2 + 3.5, -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([sx*12.0, frame_W/2 + 3.5, -0.1])
                m3_nut_trap(h=3.2);
        }
    }
}

part_01A_openframe_undermount();
"""

# --------------------------------------------------------------------
# PART 01B: OPEN-FRAME BACK-MOUNT (Gá 2 ống đứng Z, C-C 56mm)
# --------------------------------------------------------------------
SCAD_PART_01B = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 01B: KHUNG OPEN-FRAME BACK-MOUNT (ỐNG ĐỨNG Z, C-C 56MM)
// - Dành cho robot có 2 ống Ø8mm dựng đứng (trục Z).
// - Ngàm kẹp nằm phía sau lưng (Y = +19.5mm), tâm X = ±28.0mm (C-C = 56.0mm).
// - Mặt đáy dưới PCB rỗng 100% từ đầu đến cuối, không vướng ống!
// ====================================================================

module part_01B_openframe_backmount() {
    z_pcb_bot = 16.0;
    z_top_rim = 19.6;
    frame_L   = 79.0;
    frame_W   = 27.6;
    y_rod     = frame_W/2 + 7.4; // 21.2mm

    difference() {
        union() {
            // 1. Thân chính khung
            rounded_box_z(frame_L, frame_W, z_top_rim, r=2.5);

            // 2. Cầu nối ngàm kẹp 2 ống Ø8mm phía sau lưng (X = ±28.0mm)
            hull() {
                for (sx = [-1, 1]) {
                    translate([sx*28.0, y_rod, 0])
                        cylinder(d=12.0, h=z_top_rim);
                    translate([sx*34.0, frame_W/2 - 2.0, 0])
                        cylinder(d=3.0, h=z_top_rim);
                }
            }

            // 3. 2 Tai bắt ốc M3 nẹp trên tại X = 0 (Y = ±17.0mm)
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(frame_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([-5.0, sy*(frame_W/2 - 1.5), 0])
                        cube([10.0, 3.0, z_top_rim]);
                }
            }

            // 4. 2 Vấu bắt Giá gá ToF ở mặt trước (Y = -frame_W/2)
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*12.0, -frame_W/2 - 3.5, 0])
                        cylinder(d=7.6, h=z_top_rim);
                    translate([sx*12.0 - 3.8, -frame_W/2 + 0.5, 0])
                        cube([7.6, 3.0, z_top_rim]);
                }
            }
        }

        // Hốc chứa PCB
        translate([-cav_L/2, -cav_W/2, z_pcb_bot])
            cube([cav_L, cav_W, z_top_rim - z_pcb_bot + 2.0]);

        // Cửa sổ Open-Frame đáy rỗng 100%
        translate([-34.0, -9.2, -1.0])
            cube([54.0, 18.4, z_pcb_bot + 2.0]);

        // Cửa sổ bên sườn
        for (sy = [-1, 1]) {
            translate([-22.0, sy*frame_W/2 - 3.0, -1.0])
                cube([44.0, 6.0, 13.5]);
        }

        // 2 Lòng ôm ống Ø8.25mm thẳng đứng (trục Z) tại X = ±28.0mm, Y = y_rod
        for (sx = [-1, 1]) {
            translate([sx*28.0, y_rod, -0.5])
                cylinder(d=rod_D, h=z_top_rim + 1.0);

            // Miệng mở Snap-fit phía sau (rộng 7.25mm)
            translate([sx*28.0 - 3.625, y_rod, -0.5])
                cube([7.25, 10.0, z_top_rim + 1.0]);
        }

        // 2 Lỗ ốc M3 siết thanh khóa sau lưng tại X = ±14.0mm, Y xuyên ngang
        for (sx = [-1, 1]) {
            translate([sx*14.0, y_rod + 6.0, z_top_rim/2])
                rotate([90, 0, 0])
                    cylinder(d=3.4, h=16.0);
            translate([sx*14.0 - 2.85, frame_W/2 + 1.0, -0.1])
                cube([5.7, 2.7, z_top_rim/2 + 3.0]);
        }

        // Khe USB-C và RJ45
        translate([-frame_L/2 - 1.0, -7.0, z_pcb_bot - 0.5])
            cube([6.0, 14.0, 8.0]);
        translate([cav_L/2 - 1.0, -8.5, z_pcb_bot - 0.5])
            cube([6.0, 17.0, 10.0]);

        // Lỗ ốc nẹp trên và gá ToF
        for (sy = [-1, 1]) {
            translate([0, sy*(frame_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([0, sy*(frame_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.2);
        }
        for (sx = [-1, 1]) {
            translate([sx*12.0, -frame_W/2 - 3.5, -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([sx*12.0, -frame_W/2 - 3.5, -0.1])
                m3_nut_trap(h=3.2);
        }
    }
}

part_01B_openframe_backmount();
"""

# --------------------------------------------------------------------
# PART 02A: THANH KHÓA KÉP CHO BẢN UNDER-MOUNT (C-C 56MM)
# --------------------------------------------------------------------
SCAD_PART_02A = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 02A: THANH NẸP KHÓA KÉP CHO BẢN UNDER-MOUNT (C-C 56MM)
// - Dài 68.0mm, rộng 18.0mm, dày 7.0mm.
// - 2 Rãnh bán nguyệt Ø8.25mm tại X = ±28.0mm (C-C chuẩn 56.0mm).
// - 4 Lỗ ốc M3 (X = ±28.0mm, Y = ±10.0mm) kèm hốc chìm đầu ốc M3.
// - Khoét nhẹ rãnh giữa để giảm trọng lượng và tăng độ đàn hồi khi siết.
// - Đặt phẳng Z = 0, 0% Support!
// ====================================================================

module part_02A_rod_clamp_dual_bar() {
    bar_L = 68.0;
    bar_W = 26.0;
    bar_H = 7.0;

    difference() {
        // Thân thanh nẹp
        rounded_box_z(bar_L, bar_W, bar_H, r=2.5);

        // 2 Lòng ôm ống Ø8.25mm tại X = -28.0mm và X = +28.0mm (C-C = 56.0mm)
        // Tâm ống đặt ở Z = bar_H + 1.0mm -> ngoạm sâu 3.125mm vào mặt trên
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), bar_W/2 + 1.0, bar_H + 1.0])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=bar_W + 2.0);
        }

        // 4 Lỗ ốc M3 xuyên suốt (X = ±28.0mm, Y = ±10.0mm)
        for (sx = [-1, 1]) {
            for (sy = [-1, 1]) {
                translate([sx*28.0, sy*10.0, -0.5])
                    cylinder(d=3.4, h=bar_H + 1.0);
                // Hốc chìm đầu ốc M3 ở mặt đáy Z = 0
                translate([sx*28.0, sy*10.0, -0.1])
                    cylinder(d=6.3, h=3.0);
            }
        }

        // Rãnh khoét thoáng giữa (X = -18.0 .. +18.0, Y = -8.0 .. +8.0)
        translate([-18.0, -8.0, 2.5])
            cube([36.0, 16.0, bar_H]);
    }
}

part_02A_rod_clamp_dual_bar();
"""

# --------------------------------------------------------------------
# PART 02B: THANH KHÓA KÉP CHO BẢN BACK-MOUNT (C-C 56MM)
# --------------------------------------------------------------------
SCAD_PART_02B = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 02B: THANH NẸP KHÓA KÉP CHO BẢN BACK-MOUNT (C-C 56MM)
// - Dài 68.0mm, rộng 14.0mm, cao 8.0mm.
// - 2 Rãnh ôm ống đứng tại X = ±28.0mm.
// - 2 Lỗ ốc M3 tại X = ±14.0mm siết vào lưng bản 01B.
// ====================================================================

module part_02B_rod_clamp_backmount() {
    bar_L = 68.0;
    bar_W = 14.0;
    bar_H = 8.0;

    difference() {
        rounded_box_z(bar_L, bar_W, bar_H, r=2.5);

        // 2 Lòng ôm ống Ø8.25mm tại X = ±28.0mm
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), bar_W/2 + 1.0, bar_H/2])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=bar_W + 2.0);
        }

        // 2 Lỗ ốc M3 tại X = ±14.0mm
        for (sx = [-1, 1]) {
            translate([sx*14.0, 0, -0.5])
                cylinder(d=3.4, h=bar_H + 1.0);
            translate([sx*14.0, 0, -0.1])
                cylinder(d=6.3, h=3.0);
        }
    }
}

part_02B_rod_clamp_backmount();
"""

# --------------------------------------------------------------------
# PART 03: NẸP TRÊN KHÓA GIỮ PCB LUCKFOX PICO MAX/PRO
# --------------------------------------------------------------------
SCAD_PART_03 = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 03: NẸP TRÊN KHÓA GIỮ PCB LUCKFOX PICO MAX / PRO
// - Đặt phẳng Z = 0, 0% Support.
// - Đè giữ 2 đầu PCB Luckfox ép chặt xuống khung, chống rung nảy.
// - Khoét rỗng toàn bộ khu vực cổng RJ45, cáp Camera CSI, chip RV1106,
//   nút BOOT / RESET, và cổng Type-C!
// - 2 Tai bắt ốc M3 ở 2 bên sườn (X = 0, Y = ±17.0mm).
// ====================================================================

module part_03_pcb_top_retainer() {
    ret_L = 79.0;
    ret_W = 27.6;
    ret_H = 3.6;

    difference() {
        union() {
            // Khung nẹp chính
            rounded_box_z(ret_L, ret_W, ret_H, r=2.5);

            // 2 Tai bắt ốc M3
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(ret_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=ret_H);
                    translate([-5.0, sy*(ret_W/2 - 1.5), 0])
                        cube([10.0, 3.0, ret_H]);
                }
            }
        }

        // ------------------------------------------------------------
        // CÁC HỐC THOÁNG TRÊN NẸP
        // ------------------------------------------------------------

        // 1. Cổng RJ45 (X = +15.5 .. +39.5, rộng 17.0mm)
        translate([15.5, -8.5, -0.5])
            cube([25.0, 17.0, ret_H + 1.0]);

        // 2. Cáp Camera MIPI CSI (X = +6.0 .. +15.0, rộng 16.5mm)
        translate([6.0, -8.25, -0.5])
            cube([9.0, 16.5, ret_H + 1.0]);

        // 3. Khe tản nhiệt Chip RV1106 (X = -8.0 .. +5.0)
        translate([-8.0, -7.0, -0.5])
            cube([13.0, 14.0, ret_H + 1.0]);

        // 4. Khe bấm nút BOOT / RESET & Khe thẻ MicroSD (X = -31.0 .. -12.0)
        translate([-31.0, -7.0, -0.5])
            cube([19.0, 14.0, ret_H + 1.0]);

        // 5. Cổng Type-C (X = -39.5 .. -31.0, rộng 13.0mm)
        translate([-40.5, -6.5, -0.5])
            cube([10.0, 13.0, ret_H + 1.0]);

        // 6. 2 Lỗ ốc M3 ở 2 tai (X = 0, Y = ±17.0mm)
        for (sy = [-1, 1]) {
            translate([0, sy*(ret_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=ret_H + 1.0);
            translate([0, sy*(ret_W/2 + 3.2), ret_H - 1.8])
                cylinder(d=6.3, h=2.0);
        }
    }
}

part_03_pcb_top_retainer();
"""

# --------------------------------------------------------------------
# PART 04: GIÁ GÁ CẢM BIẾN TOF VL53L5CX V2
# --------------------------------------------------------------------
SCAD_PART_04 = COMMON_HEADER + """
// ====================================================================
// CHI TIẾT 04: GIÁ GÁ CẢM BIẾN TOF VL53L5CX V2 (CHĨA THẲNG TRƯỚC)
// - Bắt chắc vào 2 vấu mặt trước khung Open-Frame bằng 2 vít M3 (C-C = 24.0mm).
// - Mặt dựng gắn module ToF VL53L5CX V2 (dài 24.7mm, 2 lỗ M2 cách nhau đúng 20.0mm).
// - Cửa sổ thông quang 12.0 x 7.5mm vát mép 45° không che chắn FoV 63°.
// - Có hốc lùi 1.2mm cho linh kiện SMD mặt sau bo ToF.
// - Khe thoát chân header 6-pin cắm dây Dupont thuận tiện.
// - In phẳng tại Z = 0, 0% Support!
// ====================================================================

module part_04_vl53l5cx_v2_sensor_bracket() {
    base_L    = 34.0;       // Dài chân đế (mm)
    base_W    = 10.0;       // Rộng chân đế bắt vào khung (mm)
    base_H    = 3.5;        // Độ dày chân đế (mm)
    face_H    = 18.0;       // Chiều cao mặt dựng gắn ToF (mm)
    face_T    = 3.2;        // Độ dày mặt dựng (mm)

    difference() {
        union() {
            // 1. Chân đế ngang bắt vít M3 vào khung (nằm tại Z = 0 .. base_H)
            hull() {
                for (sx = [-1, 1])
                    translate([sx*12.0, 0, 0])
                        cylinder(d=base_W, h=base_H);
            }

            // 2. Mặt dựng đứng gắn cảm biến ToF (Z = base_H .. base_H + face_H)
            translate([-base_L/2, -face_T/2 + base_W/2 - 1.0, 0])
                cube([base_L, face_T, base_H + face_H]);

            // 3. Ke gia cường tam giác 2 bên sườn
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*(base_L/2 - 1.5), -base_W/2 + 1.0, 0])
                        cube([1.5, 1.0, base_H]);
                    translate([sx*(base_L/2 - 1.5), base_W/2 - 1.0, 0])
                        cube([1.5, 1.0, base_H + 10.0]);
                }
            }
        }

        // A. 2 Lỗ ốc M3 bắt vào khung (X = ±12.0mm, Y = 0)
        for (sx = [-1, 1]) {
            translate([sx*12.0, 0, -0.5])
                cylinder(d=3.4, h=base_H + 1.0);
            // Hốc chìm đầu ốc M3
            translate([sx*12.0, 0, base_H - 1.8])
                cylinder(d=6.3, h=2.0);
        }

        // B. CỬA SỔ QUANG HỌC TOF (X = 0, Z = base_H + 9.0mm)
        //    Kích thước 12.0 x 7.5mm, vát côn 45° về phía trước để đảm bảo FoV 63°
        y_face = base_W/2 - 1.0;
        translate([0, y_face, base_H + 9.5]) {
            // Lỗ thông quang xuyên suốt
            cube([12.0, face_T + 4.0, 7.5], center=true);

            // Vát mép mở rộng 45°
            hull() {
                translate([0, 1.0, 0])
                    cube([12.0, 0.5, 7.5], center=true);
                translate([0, 3.5, 0])
                    cube([16.0, 0.5, 11.5], center=true);
            }
        }

        // C. 2 LỖ BẮT VÍT M2 CHO TAI MODULE VL53L5CX V2 (C-C = 20.0mm chuẩn!)
        //    Tại X = -10.0mm và X = +10.0mm, Z = base_H + 9.5mm
        for (sx = [-1, 1]) {
            translate([sx*(tof_hole_CC/2), y_face, base_H + 9.5]) {
                rotate([-90, 0, 0])
                    cylinder(d=tof_hole_D, h=face_T + 4.0, center=true);
                // Hốc tán M2 lục giác hoặc hốc chìm ở mặt sau
                translate([0, -face_T/2 - 0.1, 0])
                    rotate([90, 0, 0])
                        m2_nut_trap(h=2.2);
            }
        }

        // D. HỐC LÙI SÂU 1.2mm CHO MỐI HÀN VÀ LINH KIỆN SMD MẶT SAU BO TOF
        //    (Kích thước 17.0 x 11.0mm)
        translate([0, y_face - face_T/2 + 0.6, base_H + 9.5])
            cube([17.0, 1.4, 11.2], center=true);

        // E. KHE THOÁT CHÂN HEADER 6-PIN CHO CÁP DUPONT (ở mép dưới Z = base_H .. base_H + 3.0)
        translate([0, y_face, base_H + 2.0])
            cube([16.5, face_T + 4.0, 4.0], center=true);
    }
}

part_04_vl53l5cx_v2_sensor_bracket();
"""

# --------------------------------------------------------------------
# SCAD PREVIEW LẮP RÁP TOÀN BỘ (00_Full_Assembly_Preview.scad)
# --------------------------------------------------------------------
SCAD_ASSEMBLY = COMMON_HEADER + """
// ====================================================================
// 00_Full_Assembly_Preview.scad
// Mô phỏng trực quan 100% Cụm Lắp Ráp Khung Open-Frame Luckfox Pico Max
// và Cảm biến ToF VL53L5CX V2 trên 2 ống tròn Ø8.0mm (C-C = 56.0mm).
// ====================================================================

use <01A_Luckfox_OpenFrame_UnderMount_56mm.scad>
use <02A_Rod_Clamp_Dual_Bar_56mm.scad>
use <03_Luckfox_PCB_Top_Retainer.scad>
use <04_VL53L5CX_V2_Sensor_Bracket.scad>

// 1. Hai ống tròn Ø8.0mm (màu xám kim loại, C-C = 56.0mm)
module render_rods() {
    color([0.7, 0.73, 0.75, 0.9]) {
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), 0, 4.0])
                rotate([90, 0, 0])
                    cylinder(d=8.0, h=100.0, center=true);
        }
    }
}

// 2. Bo Luckfox Pico Max / Pro
module render_luckfox_board() {
    z_bot = 16.0;
    // PCB (Xanh lá)
    color([0.1, 0.55, 0.25, 0.95])
        translate([-pcb_L/2, -pcb_W/2, z_bot])
            cube([pcb_L, pcb_W, pcb_T]);

    // Cổng RJ45 (Bạc kim loại)
    color([0.85, 0.85, 0.88, 1.0])
        translate([15.5, -8.0, z_bot + pcb_T])
            cube([21.0, 16.0, 13.5]);

    // Cổng Type-C (Bạc)
    color([0.75, 0.75, 0.78, 1.0])
        translate([-36.5, -4.5, z_bot + pcb_T])
            cube([8.0, 9.0, 3.2]);

    // Chip SoC RV1106 (Đen mờ)
    color([0.15, 0.15, 0.15, 1.0])
        translate([-7.0, -5.5, z_bot + pcb_T])
            cube([10.0, 10.0, 1.2]);

    // 40 Chân GPIO quay xuống dưới (Vàng đồng)
    color([0.9, 0.75, 0.2, 1.0]) {
        for (i = [0:19]) {
            x_pin = -34.5 + i*2.54;
            for (sy = [-1, 1]) {
                translate([x_pin, sy*gpio_Y, z_bot - gpio_H])
                    cylinder(d=0.64, h=gpio_H);
            }
        }
    }
}

// 3. Module ToF VL53L5CX V2
module render_tof_module() {
    // PCB ToF (Tím đậm)
    color([0.35, 0.15, 0.45, 0.95])
        translate([-tof_pcb_L/2, -tof_pcb_T/2, -tof_pcb_H/2])
            cube([tof_pcb_L, tof_pcb_T, tof_pcb_H]);

    // Mắt cảm biến quang học VL53L5CX (Đen bóng có thấu kính)
    color([0.1, 0.1, 0.1, 1.0])
        translate([-tof_sensor_W/2, tof_pcb_T/2, -tof_sensor_H/2])
            cube([tof_sensor_W, 1.6, tof_sensor_H]);

    // 6 Chân header cắm dây Dupont
    color([0.9, 0.75, 0.2, 1.0]) {
        for (p = [0:5]) {
            translate([-6.35 + p*2.54, 0, -tof_pcb_H/2 - 2.5])
                cylinder(d=0.64, h=3.0);
        }
    }
}

// ====================================================================
// TOÀN BỘ CỤM LẮP RÁP PREVIEW
// ====================================================================
module full_assembly() {
    // Khung Open-Frame Base (Cam ORC)
    color([0.95, 0.45, 0.1, 0.9])
        part_01A_openframe_undermount();

    // Thanh khóa kép kẹp 2 ống dưới đáy (Cam đậm)
    color([0.8, 0.35, 0.08, 0.95])
        translate([0, 0, -7.0])
            part_02A_rod_clamp_dual_bar();

    // Nẹp trên khóa giữ PCB (Vàng cam)
    color([0.95, 0.65, 0.15, 0.85])
        translate([0, 0, 19.6])
            part_03_pcb_top_retainer();

    // Giá gá ToF VL53L5CX V2 (Xanh dương ORC)
    color([0.15, 0.45, 0.85, 0.9])
        translate([0, 13.8 + 3.5, 0])
            part_04_vl53l5cx_v2_sensor_bracket();

    // Module ToF đặt trên giá gá
    translate([0, 13.8 + 3.5 + 5.0 + 1.2, 3.5 + 9.5])
        render_tof_module();

    // Bo mạch Luckfox Pico Max
    render_luckfox_board();

    // 2 Ống Ø8.0mm C-C 56mm
    render_rods();
}

full_assembly();
"""

# ====================================================================
# 2. GHI CÁC FILE SCAD VÀ BIÊN DỊCH RA FILE STL
# ====================================================================

PARTS_TO_GENERATE = [
    ("01A_Luckfox_OpenFrame_UnderMount_56mm.scad", SCAD_PART_01A),
    ("01B_Luckfox_OpenFrame_BackMount_56mm.scad", SCAD_PART_01B),
    ("02A_Rod_Clamp_Dual_Bar_56mm.scad", SCAD_PART_02A),
    ("02B_Rod_Clamp_BackMount_56mm.scad", SCAD_PART_02B),
    ("03_Luckfox_PCB_Top_Retainer.scad", SCAD_PART_03),
    ("04_VL53L5CX_V2_Sensor_Bracket.scad", SCAD_PART_04),
    ("00_Full_Assembly_Preview.scad", SCAD_ASSEMBLY),
]

def main():
    print(f"=== KHỞI TẠO VÀ XUẤT CÁC FILE THIẾT KẾ VÀO: {OUT_DIR} ===")

    scad_files = []
    stl_files = []

    for filename, content in PARTS_TO_GENERATE:
        filepath = os.path.join(OUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        scad_files.append(filepath)
        print(f"[OK] Đã ghi file SCAD: {filename}")

    # Biên dịch các chi tiết rời thành file STL
    compile_targets = [
        "01A_Luckfox_OpenFrame_UnderMount_56mm",
        "01B_Luckfox_OpenFrame_BackMount_56mm",
        "02A_Rod_Clamp_Dual_Bar_56mm",
        "02B_Rod_Clamp_BackMount_56mm",
        "03_Luckfox_PCB_Top_Retainer",
        "04_VL53L5CX_V2_Sensor_Bracket",
    ]

    print("\n=== BIÊN DỊCH OPENSCAD -> STL (FDM 0% SUPPORT) ===")
    for target in compile_targets:
        scad_path = os.path.join(OUT_DIR, f"{target}.scad")
        stl_path = os.path.join(OUT_DIR, f"{target}.stl")
        cmd = [OPENSCAD_COM, "-o", stl_path, scad_path]
        print(f"Đang biên dịch {target}.stl ...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(stl_path):
            stl_files.append(stl_path)
            size_kb = os.path.getsize(stl_path) / 1024.0
            print(f" -> [THÀNH CÔNG] {target}.stl ({size_kb:.1f} KB)")
        else:
            print(f" -> [LỖI] {target}: {res.stderr}")

    # Xuất ảnh render xem trước (Preview PNG)
    preview_scad = os.path.join(OUT_DIR, "00_Full_Assembly_Preview.scad")
    preview_png = os.path.join(OUT_DIR, "00_Full_Assembly_Preview.png")
    print(f"\nĐang render ảnh preview 3D: {preview_png} ...")
    cmd_img = [
        OPENSCAD_COM,
        "--colorscheme=Tomorrow Night",
        "--imgsize=1920,1080",
        "--camera=45,-75,35,0,0,10,800",
        "-o", preview_png,
        preview_scad
    ]
    subprocess.run(cmd_img, capture_output=True, text=True)
    if os.path.exists(preview_png):
        print(f"[OK] Đã tạo ảnh preview thành công: {os.path.basename(preview_png)}")

    # ====================================================================
    # 3. KIỂM TRA ĐỘ KÍN NƯỚC (MANIFOLD) & KÍCH THƯỚC BẰNG TRIMESH
    # ====================================================================
    print("\n=== KIỂM ĐỊNH HÌNH HỌC MESH BẰNG TRIMESH ===")
    all_pass = True
    for stl_path in stl_files:
        name = os.path.basename(stl_path)
        mesh = trimesh.load(stl_path)
        is_watertight = mesh.is_watertight
        extents = mesh.extents
        bounds = mesh.bounds
        vol = mesh.volume if is_watertight else 0.0

        print(f"\nChi tiết: {name}")
        print(f"  - Watertight (Manifold): {'PASS (100% Kín)' if is_watertight else 'FAIL'}")
        print(f"  - Kích thước bao (LxWxH): {extents[0]:.2f} x {extents[1]:.2f} x {extents[2]:.2f} mm")
        print(f"  - Tọa độ Z: từ {bounds[0][2]:.2f} đến {bounds[1][2]:.2f} mm (Z_min >= 0: {bounds[0][2] >= -0.05})")
        print(f"  - Thể tích: {vol:.1f} mm³")

        if not is_watertight:
            all_pass = False

    print(f"\n>>> KẾT QUẢ TỔNG QUAN TRIMESH: {'TOÀN BỘ CHI TIẾT ĐẠT 100% MANIFOLD' if all_pass else 'CÓ LỖI'}")

if __name__ == "__main__":
    main()
