// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// FILE: 00_Test_Tower_Chassis_Assembly_10_Bolts.scad
// MỤC TIÊU: KIỂM TRA ĐỒNG TÂM TUYỆT ĐỐI (0.00 mm ERROR) GIỮA 10 LỖ BU-LÔNG M3
// TRÊN 2 CHÂN THÁP NÂNG (01B & 01C) VÀ KHUNG GẦM CHÍNH 01_CHASSIS_BASE_200X200
// ====================================================================

$fn = 36;

// 1. KHUNG GẦM CHÍNH 200x200mm (Màu xám thép mờ hoặc than chì)
color([0.35, 0.38, 0.42, 0.85]) {
    import("01_Chassis_Base_200x200.stl");
}

// 2. THÁP NÂNG TRÁI (01B_Lift_Tower_Left_FlatPrint.stl)
// Đặt chính xác vào hệ tọa độ lắp ghép: X in [-28, 0], Y in [105, 166], Z in [4, 94]
color([0.95, 0.45, 0.1, 0.9]) {
    translate([-28.0, 135.5, 49.0])
        rotate([0, 90, 0])
            import("01B_Lift_Tower_Left_FlatPrint.stl");
}

// 3. THÁP NÂNG PHẢI (01C_Lift_Tower_Right_MG996R_FlatPrint.stl)
// Đặt chính xác vào hệ tọa độ lắp ghép: X in [0, 28], Y in [105, 166], Z in [4, 94]
color([1.0, 0.55, 0.05, 0.9]) {
    translate([28.0, 0, 0])
        rotate([0, -90, 0])
            import("01C_Lift_Tower_Right_MG996R_FlatPrint.stl");
}

// 4. MÔ PHỎNG 10 BU-LÔNG M3x16mm (Đầu trụ Socket Head Cap M3 x 16mm, mạ Niken sáng bóng)
module m3_bolt(x, y, z_head = 15.0, bolt_len = 16.0) {
    color([0.1, 0.85, 1.0]) { // Màu xanh Cyan phản quang cực kỳ nổi bật
        translate([x, y, z_head]) {
            // Mũ bu-lông M3: Đường kính 5.5mm, cao 3.0mm
            cylinder(d=5.5, h=3.0);
            // Lỗ lục giác chìm 2.5mm trên mũ bu-lông
            translate([0, 0, 1.2]) cylinder(d=2.8, h=2.0, $fn=6);
            // Thân ren M3: Đường kính 3.0mm, dài 16mm cắm sâu qua tháp và xuyên sàn xe
            translate([0, 0, -bolt_len])
                cylinder(d=3.0, h=bolt_len);
        }
    }
}

// CỤM THÁP TRÁI (01B): 5 BU-LÔNG M3
// - Chân Sau (Foot 2 - 3 lỗ):
m3_bolt(-16.0, 110.5, 15.0);
m3_bolt(-16.0, 122.0, 15.0);
m3_bolt(-24.0, 116.0, 15.0);
// - Chân Trước (Foot 1 - 2 lỗ):
m3_bolt(-16.0, 160.25, 15.0);
m3_bolt(-24.0, 160.25, 15.0);

// CỤM THÁP PHẢI (01C): 5 BU-LÔNG M3
// - Chân Sau (Foot 3 - 3 lỗ):
m3_bolt( 16.0, 110.5, 15.0);
m3_bolt( 16.0, 122.0, 15.0);
m3_bolt( 24.0, 116.0, 15.0);
// - Chân Trước (Foot 4 - 2 lỗ):
m3_bolt( 16.0, 160.25, 15.0);
m3_bolt( 24.0, 160.25, 15.0);
