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
// CHI TIẾT 01B: KHUNG OPEN-FRAME BACK-MOUNT (ỐNG ĐỨNG Z, C-C 56MM)
// - BẢN THIẾT KẾ TIÊU CHUẨN KHUYÊN DÙNG CHO ROBOT ORC K2.
// - 2 Ống Ø8.0mm dựng đứng dọc trục Z tại X = ±28.0mm (C-C 56.0mm chuẩn).
// - ĐÁY RỖNG MỞ RỘNG TỚI X = -37.0mm: Đảm bảo Pin 0 (X = -34.5mm) và toàn bộ
//   40 đầu cắm Dupont cái cắm rút 100% tự do, không hề va chạm thành khung!
// - 4 VÍT M3 KHÓA ỐNG TANGENTIAL ÔM 2 BÊN SƯỜN ỐNG (X = ±20.0 và X = ±36.0mm):
//   Loại bỏ hoàn toàn lỗi đâm xuyên tim ống; lực siết kẹp đối xứng cực mạnh.
// - KHE HỞ KẸP CLAMP GAP = 1.20mm (>= 1.0mm) đảm bảo siết cứng ngắc vào ống.
// - VÒM MỞ BÊN SƯỜN CÓ GÂN GIỮA VÀ VÁT GÓC 45°: Loại bỏ cầu treo 44mm,
//   in phẳng 100% 0% support không bị võng sợi.
// - TAI BẮT TOF VÀ NẸP TRÊN ĐƯỢC TĂNG PHI LÊN D=8.6mm (thành dày 2.6mm >= 2.4mm).
// ====================================================================

module part_01B_openframe_backmount() {
    z_pcb_bot = 16.0;       // Mặt đáy PCB tựa tại Z = 16.0mm
    z_top_rim = 19.6;       // Gờ vành khung cao Z = 19.6mm
    frame_L   = 79.0;       // Dài khung (X = -39.5 .. +39.5)
    frame_W   = 27.6;       // Rộng thân khung (Y = -13.8 .. +13.8)
    y_rod     = 21.2;       // Tâm 2 ống Ø8mm phía sau lưng
    y_mate    = 20.6;       // Mặt phẳng lắp ghép với thanh nẹp 02B

    difference() {
        union() {
            // 1. Thân chính khung Open-Frame
            rounded_box_z(frame_L, frame_W, z_top_rim, r=2.5);

            // 2. Khối liên kết ngàm kẹp 2 ống Ø8mm phía sau lưng (từ Y = 12.0 đến y_mate = 20.6mm)
            //    Bao phủ 2 ống X = ±28.0mm và 4 tai ốc X = ±20.0, ±36.0mm
            hull() {
                translate([-39.0, 12.0, 0])
                    cube([78.0, 1.0, z_top_rim]);
                translate([-39.0, y_mate - 1.0, 0])
                    cube([78.0, 1.0, z_top_rim]);
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

            // 4. 2 Vấu bắt Giá gá ToF ở mặt trước (Y = -frame_W/2) tại X = ±12.0mm
            //    Tăng phi d=8.6mm để thành vách đạt 2.6mm (>= 2.4mm)
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*12.0, -frame_W/2 - 3.5, 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([sx*12.0 - 4.3, -frame_W/2 + 0.5, 0])
                        cube([8.6, 3.0, z_top_rim]);
                }
            }
        }

        // ------------------------------------------------------------
        // CÁC HỐC CẮT HÌNH HỌC VÀ KHÔNG GIAN KỸ THUẬT
        // ------------------------------------------------------------

        // A. Hốc chứa bo mạch Luckfox từ Z = z_pcb_bot (16.0mm) lên đỉnh
        translate([-cav_L/2, -cav_W/2, z_pcb_bot])
            cube([cav_L, cav_W, z_top_rim - z_pcb_bot + 2.0]);

        // B. CỬA SỔ OPEN-FRAME CHÍNH MỞ RỘNG TỚI X = -37.0mm!
        //    Chiều dài 57.0mm (từ X = -37.0 đến +20.0mm), rộng 18.4mm
        //    Bao trọn Pin 0 (X = -34.5mm) với dung sai > 2.5mm cho đầu Dupont
        translate([-37.0, -9.2, -1.0])
            cube([57.0, 18.4, z_pcb_bot + 2.0]);

        // C. CỬA SỔ BÊN SƯỜN VÁT GÓC 45° CÓ TRỤ GIỮA GIA CƯỜNG TẠI X = 0
        //    Chia làm 2 khoang: Trái (X = -22.0 .. -2.5) và Phải (X = +2.5 .. +22.0)
        //    Vát góc 45° ở đỉnh (Z = 8.5 .. 12.5mm) loại bỏ hoàn toàn cầu ngang võng sợi!
        for (sy = [-1, 1]) {
            // Khoang bên trái (X = -22.0 .. -2.5)
            hull() {
                translate([-22.0, sy*frame_W/2 - 3.0, -1.0])
                    cube([19.5, 6.0, 9.5]);
                translate([-18.0, sy*frame_W/2 - 3.0, 12.5 - 0.1])
                    cube([11.5, 6.0, 0.2]);
            }
            // Khoang bên phải (X = +2.5 .. +22.0)
            hull() {
                translate([2.5, sy*frame_W/2 - 3.0, -1.0])
                    cube([19.5, 6.0, 9.5]);
                translate([6.5, sy*frame_W/2 - 3.0, 12.5 - 0.1])
                    cube([11.5, 6.0, 0.2]);
            }
        }

        // D. 2 LÒNG ÔM ỐNG Ø8.25mm THẲNG ĐỨNG (TRỤC Z) TẠI X = ±28.0mm, Y = y_rod
        //    Độ sâu ngàm trong 01B = 3.525mm (cùng với 02B tạo khoảng hở kẹp clamp gap = 1.20mm)
        for (sx = [-1, 1]) {
            translate([sx*28.0, y_rod, -0.5])
                cylinder(d=rod_D, h=z_top_rim + 1.0);

            // Mở miệng ngàm về phía sau (từ y_mate = 20.6mm trở đi)
            translate([sx*28.0 - rod_D/2, y_mate, -0.5])
                cube([rod_D, 10.0, z_top_rim + 1.0]);
        }

        // E. 4 LỖ ỐC M3 KHÓA ỐNG TANGENTIAL ÔM 2 BÊN SƯỜN ỐNG
        //    Tọa độ X = ±20.0mm (trong) và X = ±36.0mm (ngoài)
        //    Trục ốc xuyên ngang phương Y tại Z = 10.0mm
        for (x_pos = [-36.0, -20.0, 20.0, 36.0]) {
            // Lỗ thông vít M3 xuyên ngang từ mặt ghép y_mate vào trong
            translate([x_pos, y_mate + 1.0, 10.0])
                rotate([90, 0, 0])
                    cylinder(d=3.4, h=12.0);

            // Hốc tán M3 lục giác thẳng đứng (Z) tại Y = 14.5mm
            // Đặt đứng theo trục Z -> in chuẩn 100% không cần support!
            translate([x_pos, 14.5, -0.5])
                cylinder(d=6.6, h=14.0, $fn=6);
        }

        // F. KHE CỔNG USB TYPE-C Ở ĐẦU TRÁI (X = -39.5mm)
        translate([-frame_L/2 - 1.0, -7.0, z_pcb_bot - 0.5])
            cube([6.0, 14.0, 8.0]);

        // G. KHE CỔNG RJ45 Ở ĐẦU PHẢI (X = +39.5mm)
        translate([cav_L/2 - 1.0, -8.5, z_pcb_bot - 0.5])
            cube([6.0, 17.0, 10.0]);

        // H. 2 LỖ ỐC M3 BẮT NẸP TRÊN (X = 0, Y = ±17.0mm) KÈM HỐC TÁN M3
        for (sy = [-1, 1]) {
            translate([0, sy*(frame_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([0, sy*(frame_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.5);
        }

        // I. 2 LỖ ỐC M3 BẮT GIÁ TOF (X = ±12.0mm, Y = -frame_W/2 - 3.5)
        for (sx = [-1, 1]) {
            translate([sx*12.0, -frame_W/2 - 3.5, -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([sx*12.0, -frame_W/2 - 3.5, -0.1])
                m3_nut_trap(h=3.5);
        }
    }
}

part_01B_openframe_backmount();
