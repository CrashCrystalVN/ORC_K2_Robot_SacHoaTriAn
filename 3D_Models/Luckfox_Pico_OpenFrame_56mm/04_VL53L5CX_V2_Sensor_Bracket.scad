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

// Hốc tán M3 chuẩn FDM: d=6.6mm ($fn=6 -> s=5.72mm) tránh kẹt tán do co ngót
module m3_nut_trap(h=3.5) {
    cylinder(d=6.6, h=h, $fn=6);
}

// Hốc tán M2 chuẩn FDM: d=4.9mm ($fn=6 -> s=4.25mm) lọt êm tán M2 (s=4.0mm)
module m2_nut_trap(h=2.5) {
    cylinder(d=4.9, h=h, $fn=6);
}

// ====================================================================
// CHI TIẾT 04: GIÁ GÁ CẢM BIẾN TOF VL53L5CX V2 (CHĨA THẲNG TRƯỚC)
// - Bắt chắc vào 2 vấu mặt trước khung Open-Frame bằng 2 vít M3 (C-C = 24.0mm).
// - Mặt dựng gắn module ToF VL53L5CX V2 (dài 24.7mm, 2 lỗ M2 cách nhau đúng 20.0mm).
// - Cửa sổ thông quang 12.0 x 7.5mm vát mép 45° không che chắn FoV 63°.
// - Có hốc lùi 1.2mm cho linh kiện SMD mặt sau bo ToF.
// - KHE THOÁT CÁP DUPONT 16x6mm Ở ĐÁY: cho phép cắm đầu cos Dupont cái thẳng
//   vào hàng chân 6-pin của cảm biến ToF mà không bị cấn chân đế.
// - Gân gia cường tam giác dày 2.5mm (đạt chuẩn >= 2.4mm).
// - Hốc tán M2 d=4.9mm (s=4.25mm) lắp vừa khít không cần ép nhiệt.
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

            // 3. Ke gia cường tam giác 2 bên sườn (dày 2.5mm >= 2.4mm)
            for (sx = [-1, 1]) {
                hull() {
                    translate([sx*(base_L/2 - 2.5), -base_W/2 + 1.0, 0])
                        cube([2.5, 1.0, base_H]);
                    translate([sx*(base_L/2 - 2.5), base_W/2 - 1.0, 0])
                        cube([2.5, 1.0, base_H + 10.0]);
                }
            }
        }

        // A. 2 Lỗ ốc M3 bắt vào khung (X = ±12.0mm, Y = 0)
        for (sx = [-1, 1]) {
            translate([sx*12.0, 0, -0.5])
                cylinder(d=3.4, h=base_H + 1.0);
            // Hốc chìm đầu ốc M3 (d=6.6mm)
            translate([sx*12.0, 0, base_H - 1.8])
                cylinder(d=6.6, h=2.5);
        }

        // B. CỬA SỔ QUANG HỌC TOF (X = 0, Z = base_H + 9.5mm)
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

        // C. 2 LỖ BẮT VÍT M2 CHO TAI MODULE VL53L5CX V2 (C-C = 20.0mm chuẩn)
        //    Tại X = -10.0mm và X = +10.0mm, Z = base_H + 9.5mm
        for (sx = [-1, 1]) {
            translate([sx*(tof_hole_CC/2), y_face, base_H + 9.5]) {
                rotate([-90, 0, 0])
                    cylinder(d=tof_hole_D, h=face_T + 4.0, center=true);
                // Hốc tán M2 lục giác (d=4.9mm, s=4.25mm) ở mặt sau
                translate([0, -face_T/2 - 0.1, 0])
                    rotate([90, 0, 0])
                        m2_nut_trap(h=2.5);
            }
        }

        // D. HỐC LÙI SÂU 1.2mm CHO MỐI HÀN VÀ LINH KIỆN SMD MẶT SAU BO TOF
        //    (Kích thước 17.0 x 11.2mm)
        translate([0, y_face - face_T/2 + 0.6, base_H + 9.5])
            cube([17.0, 1.4, 11.2], center=true);

        // E. KHE THOÁT CHÂN HEADER 6-PIN TRÊN VÁCH DỰNG (Z = base_H .. base_H + 3.0)
        translate([0, y_face, base_H + 2.0])
            cube([16.5, face_T + 4.0, 4.0], center=true);

        // F. KHE THOÁT CÁP DUPONT 16x6mm XUYÊN QUA ĐẾ (Z = -0.5 .. base_H + 1.0)
        //    Giúp đầu cắm Dupont cái thẳng cắm từ dưới lên cực kỳ thuận tiện
        translate([-8.0, y_face - 3.0, -0.5])
            cube([16.0, 6.0, base_H + 1.0]);
    }
}

part_04_vl53l5cx_v2_sensor_bracket();
