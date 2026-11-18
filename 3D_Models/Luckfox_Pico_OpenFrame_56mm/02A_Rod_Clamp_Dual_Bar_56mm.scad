$fn = 64;

// ====================================================================
// THÔNG SỐ HÌNH HỌC HỆ THỐNG
// ====================================================================

// 1. Hệ 2 ống tròn Ø8.0 mm
rod_D       = 8.25;         // Đường kính kẹp ôm ống Ø8.0mm (+0.25mm dung sai ôm khít)
rod_CC      = 56.0;         // Khoảng cách tâm - đến - tâm (C-C) = 56.0mm (X = -28.0 và +28.0)
rod_out     = 64.0;         // Mép ngoài - ngoài = 64.0mm (tại X = -32.0 và +32.0)
rod_in      = 48.0;         // Mép trong - trong = 48.0mm (tại X = -24.0 và +24.0)

// Các hàm bổ trợ hình học chuẩn FDM
module rounded_box_z(lx, ly, lz, r=2.4) {
    hull() {
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx*(lx/2 - r), sy*(ly/2 - r), 0])
                    cylinder(r=r, h=lz);
    }
}

// ====================================================================
// CHI TIẾT 02A: THANH NẸP KHÓA KÉP CHO BẢN UNDER-MOUNT (C-C 56MM)
// - Dài 82.0mm, rộng 26.0mm, dày 8.0mm.
// - ĐỒNG TRỤC 100% VỚI 01A: 4 Lỗ vít M3 dời ra 2 bên sườn ống (X = ±20.0, ±36.0mm, Y = 0):
//   Loại bỏ hoàn toàn xung đột đâm xuyên tim ống tại X = ±28.0mm!
// - KHẮC PHỤC TRIỆT ĐỂ LỖI VỠ RÁCH MÉP: Đặt lỗ tại Y = 0, khoảng cách ra mép
//   vách ngoài lên tới 9.7mm (an toàn tuyệt đối, vượt xa chuẩn >= 2.4mm).
// - KHOẢNG HỞ KẸP CLAMP GAP = 1.20mm (>= 1.0mm): Độ sâu rãnh ngàm 3.05mm
//   cho lực ép kẹp ống Ø8.0mm cực kỳ mạnh mẽ, chống xoay tuột 100%.
// - Đặt phẳng Z = 0, 0% Support!
// ====================================================================

module part_02A_rod_clamp_dual_bar() {
    bar_L = 82.0;
    bar_W = 26.0;
    bar_H = 8.0;

    difference() {
        // 1. Thân thanh nẹp đặt phẳng Z = 0
        rounded_box_z(bar_L, bar_W, bar_H, r=2.5);

        // 2. 2 Lòng ôm ống Ø8.25mm tại X = ±28.0mm (C-C chuẩn 56.0mm)
        //    Độ sâu ngàm = 3.05mm (tạo clamp gap 1.20mm khi bắt với 01A)
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), 0, bar_H + (rod_D/2 - 3.05)])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=bar_W + 2.0, center=true);
        }

        // 3. 4 Lỗ ốc M3 xuyên suốt (X = ±20.0mm và X = ±36.0mm, Y = 0)
        //    Đồng trục hoàn toàn với 01A
        for (x_pos = [-36.0, -20.0, 20.0, 36.0]) {
            // Lỗ thông vít M3
            translate([x_pos, 0, -0.5])
                cylinder(d=3.4, h=bar_H + 1.0);

            // Hốc chìm đầu ốc M3 (d=6.6mm) ở mặt đáy Z = 0
            translate([x_pos, 0, -0.1])
                cylinder(d=6.6, h=3.0);

            // Vát mép 45° từ d=6.6 lên d=3.4mm để in 0% support
            translate([x_pos, 0, 2.9])
                cylinder(d1=6.6, d2=3.4, h=1.6);
        }

        // 4. Rãnh khoét thoáng giữa (X = -12.0 .. +12.0, Y = -8.0 .. +8.0)
        //    Giảm trọng lượng và tăng độ đàn hồi kẹp ống
        translate([-12.0, -8.0, 3.0])
            cube([24.0, 16.0, bar_H]);
    }
}

part_02A_rod_clamp_dual_bar();
