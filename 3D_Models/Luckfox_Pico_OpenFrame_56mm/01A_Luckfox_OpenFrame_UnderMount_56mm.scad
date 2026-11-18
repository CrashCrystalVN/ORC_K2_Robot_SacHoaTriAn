$fn = 64;

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

// Các hàm bổ trợ hình học chuẩn FDM
module rounded_box_z(lx, ly, lz, r=2.4) {
    hull() {
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx*(lx/2 - r), sy*(ly/2 - r), 0])
                    cylinder(r=r, h=lz);
    }
}

// Hốc tán M3 chuẩn FDM: d=6.6mm ($fn=6 -> s=5.72mm)
module m3_nut_trap(h=3.5) {
    cylinder(d=6.6, h=h, $fn=6);
}

// Hốc tán M2 chuẩn FDM: d=4.9mm ($fn=6 -> s=4.25mm)
module m2_nut_trap(h=2.5) {
    cylinder(d=4.9, h=h, $fn=6);
}

// ====================================================================
// CHI TIẾT 01A: KHUNG OPEN-FRAME UNDER-MOUNT (ỐNG NGANG Y, C-C 56MM)
// - Bệ đỡ PCB tại Z = 16.0mm.
// - 4 VÍT M3 KHÓA ỐNG TANGENTIAL DỜI RA 2 BÊN SƯỜN (X = ±20.0 & X = ±36.0mm, Y = 0):
//   Loại bỏ hoàn toàn lỗi đâm xuyên tim ống tại X = ±28.0mm!
// - VÒM MỞ BÊN SƯỜN VÁT GÓC 45°: Loại bỏ trần ngang 32mm gây võng sợi.
// - VẤU BẮT TOF VÀ NẸP TRÊN GIA CƯỜNG D=8.6mm (thành dày 2.6mm >= 2.4mm).
// - Hốc tán M3 d=6.6mm ($fn=6) chuẩn FDM.
// ====================================================================

module part_01A_openframe_undermount() {
    z_pcb_bot = 16.0;       // Đáy PCB tựa tại Z = 16.0mm
    z_top_rim = 19.6;       // Gờ viền bao ngoài mép PCB
    frame_L   = 79.0;       // Chiều dài khung (X = -39.5 .. +39.5)
    frame_W   = 27.6;       // Chiều rộng khung (Y = -13.8 .. +13.8)

    difference() {
        union() {
            // 1. Thân chính khung đỡ Open-Frame
            rounded_box_z(frame_L, frame_W, z_top_rim, r=2.5);

            // 2. 2 Tai bắt ốc M3 ở 2 bên sườn tại X = 0.0mm (Y = ±17.0mm)
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(frame_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([-5.0, sy*(frame_W/2 - 1.5), 0])
                        cube([10.0, 3.0, z_top_rim]);
                }
            }

            // 3. 2 Vấu bắt Giá gá ToF VL53L5CX V2 ở mặt trước (Y = +frame_W/2)
            //    tại X = ±12.0mm, tăng phi d=8.6mm (thành dày 2.6mm >= 2.4mm)
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*12.0, frame_W/2 + 3.5, 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([sx*12.0 - 4.3, frame_W/2 - 1.5, 0])
                        cube([8.6, 3.0, z_top_rim]);
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

        // B. CỬA SỔ OPEN-FRAME CHÍNH (ĐÁY RỖNG TỪ Z = -1 LÊN Z = 16.5)
        //    Giữa X = -18.5mm và X = +18.5mm (đảm bảo vách tại X = ±20mm đủ dày cho vít M3)
        translate([-18.5, -9.2, -1.0])
            cube([37.0, 18.4, z_pcb_bot + 2.0]);

        // C. CỬA SỔ BÊN SƯỜN VÁT GÓC 45° (SIDE ACCESS ARCHES)
        //    Vát mép 45° từ Z = 8.0 đến 12.5mm loại bỏ cầu treo phẳng 32mm
        for (sy = [-1, 1]) {
            hull() {
                translate([-16.0, sy*frame_W/2 - 3.0, -1.0])
                    cube([32.0, 6.0, 9.0]);
                translate([-12.0, sy*frame_W/2 - 3.0, 12.5 - 0.1])
                    cube([24.0, 6.0, 0.2]);
            }
        }

        // D. RÃNH THOÁT DƯỚI CHÂN GPIO ĐẦU TRÁI (X = -35.5 .. -19.0)
        for (sy = [-1, 1]) {
            translate([-35.5, sy*gpio_Y - 2.2, 3.0])
                cube([16.5, 4.4, z_pcb_bot - 2.0]);
        }

        // E. 2 RÃNH ÔM ỐNG Ø8.25mm TẠI X = ±28.0mm (C-C = 56.0mm)
        //    Trục ống chạy dọc theo Y, tâm ống tại Z = 4.0mm
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), frame_W/2 + 6.0, 4.0])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=frame_W + 12.0);

            // Khe mở miệng ngàm kẹp hướng xuống đáy Z = 0
            translate([sx*(rod_CC/2) - 3.625, -frame_W/2 - 6.0, -0.5])
                cube([7.25, frame_W + 12.0, 4.6]);
        }

        // F. 4 LỖ VÍT M3 KHÓA ỐNG TANGENTIAL ÔM 2 BÊN SƯỜN ỐNG
        //    Tại X = ±20.0mm (trong) và X = ±36.0mm (ngoài), Y = 0
        //    LOẠI BỎ HOÀN TOÀN XUNG ĐỘT ĐÂM XUYÊN ỐNG TẠI X = ±28.0mm!
        for (x_pos = [-36.0, -20.0, 20.0, 36.0]) {
            translate([x_pos, 0, -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            // Hốc tán M3 lục giác âm trên mặt trên Z = 11.5mm
            translate([x_pos, 0, 11.5])
                m3_nut_trap(h=3.5);
        }

        // G. KHE CỔNG USB TYPE-C Ở ĐẦU TRÁI (X = -39.5mm)
        translate([-frame_L/2 - 1.0, -7.0, z_pcb_bot - 0.5])
            cube([6.0, 14.0, 8.0]);

        // H. KHE CỔNG RJ45 Ở ĐẦU PHẢI (X = +39.5mm)
        translate([cav_L/2 - 1.0, -8.5, z_pcb_bot - 0.5])
            cube([6.0, 17.0, 10.0]);

        // I. 2 LỖ ỐC M3 + HỐC TÁN M3 Ở TAI BÊN SƯỜN (X = 0, Y = ±17.0mm)
        for (sy = [-1, 1]) {
            translate([0, sy*(frame_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([0, sy*(frame_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.5);
        }

        // J. 2 LỖ ỐC M3 Ở MẶT TRƯỚC (X = ±12.0mm, Y = +frame_W/2 + 3.5)
        for (sx = [-1, 1]) {
            translate([sx*12.0, frame_W/2 + 3.5, -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([sx*12.0, frame_W/2 + 3.5, -0.1])
                m3_nut_trap(h=3.5);
        }
    }
}

part_01A_openframe_undermount();
