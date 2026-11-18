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
// CHI TIẾT 02B: THANH NẸP KHÓA KÉP CHO BẢN BACK-MOUNT (C-C 56MM)
// - BẢN NẸP KHÓA SAU LƯNG ĐỒNG BỘ 100% VỚI KHUNG 01B.
// - Định hướng in FDM: Nằm phẳng trên bàn in Z = 0 (0% Support!).
// - 2 RÃNH ÔM ỐNG DỌC ĐỨNG TRỤC Z (khi lắp ráp):
//   Cắt vào mặt trên Z = 9.0mm, chạy dọc theo Y với C-C chuẩn 56.0mm.
// - ĐỒNG TRỤC 100% VỚI 01B: 4 Lỗ vít M3 xuyên ngang (Y khi lắp, Z khi in)
//   tại X = ±20.0mm và X = ±36.0mm, trùng khít hoàn toàn với 01B.
// - KHOẢNG HỞ KẸP CLAMP GAP = 1.20mm (>= 1.0mm): Độ sâu rãnh 3.525mm
//   kết hợp với rãnh 3.525mm trên 01B tạo lực siết tối đa lên ống Ø8.0mm.
// - Hốc chìm đầu ốc M3 d=6.6mm vát côn 45° in sạch không tì vết.
// ====================================================================

module part_02B_rod_clamp_backmount() {
    clamp_L = 82.0;         // Chiều dài thanh nẹp (X = -41.0 .. +41.0)
    clamp_H = 19.6;         // Chiều cao thanh nẹp (Y = -9.8 .. +9.8, khớp với 01B)
    clamp_T = 9.0;          // Độ dày thanh nẹp (Z = 0 .. 9.0)

    difference() {
        // 1. Thân chính thanh nẹp đặt phẳng Z = 0
        rounded_box_z(clamp_L, clamp_H, clamp_T, r=3.0);

        // 2. 2 Lòng ôm ống Ø8.25mm tại X = ±28.0mm (C-C chuẩn 56.0mm)
        //    Độ sâu ngàm = 3.525mm (tâm hình trụ đặt tại Z = 9.0 + 0.6 = 9.6mm)
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), 0, clamp_T + 0.6])
                rotate([-90, 0, 0])
                    cylinder(d=rod_D, h=clamp_H + 2.0, center=true);
        }

        // 3. 4 Lỗ ốc M3 xuyên suốt (X = ±20.0mm và X = ±36.0mm, Y = 0)
        //    Đồng trục tuyệt đối với 4 lỗ trên 01B!
        for (x_pos = [-36.0, -20.0, 20.0, 36.0]) {
            // Lỗ thông vít M3
            translate([x_pos, 0, -0.5])
                cylinder(d=3.4, h=clamp_T + 1.0);

            // Hốc chìm đầu ốc M3 (d=6.6mm) ở mặt ngoài Z = 0
            translate([x_pos, 0, -0.1])
                cylinder(d=6.6, h=3.2);

            // Vát chuyển tiếp 45° từ d=6.6 lên d=3.4mm để in 0% support
            translate([x_pos, 0, 3.1])
                cylinder(d1=6.6, d2=3.4, h=1.6);
        }

        // 4. Khe vát nhẹ ở giữa (X = -12.0 .. +12.0) để giảm khối lượng
        //    và tăng độ đàn hồi kẹp (giữ vách dày >= 4.0mm)
        translate([-12.0, -clamp_H/2 - 1.0, clamp_T - 1.5])
            cube([24.0, clamp_H + 2.0, 2.0]);
    }
}

part_02B_rod_clamp_backmount();
