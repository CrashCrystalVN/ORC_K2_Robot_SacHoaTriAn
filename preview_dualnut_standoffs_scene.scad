$fn = 60;

// Mô phỏng bu-lông M3 DIN 912 (Socket Head Cap Screw)
module m3_bolt(len = 12.0, thread_len = 12.0) {
    color([0.2, 0.75, 1.0, 0.95]) { // Màu xanh Cyan phản quang cực kỳ nổi bật
        cylinder(d = 5.5, h = 3.0); // Mũ bu-lông M3
        translate([0, 0, 1.2]) cylinder(d = 2.8, h = 2.0, $fn = 6); // Lục giác chìm
        translate([0, 0, -len]) cylinder(d = 3.0, h = len); // Thân ren
    }
}

// Mô phỏng tán lục giác M3 DIN 934
module m3_hex_nut() {
    color([0.88, 0.88, 0.92, 0.95]) { // Thép mạ Niken sáng bóng
        difference() {
            cylinder(d = 6.35, h = 2.40, $fn = 6);
            translate([0, 0, -0.5]) cylinder(d = 2.95, h = 3.4);
        }
    }
}

// 1. CỌC 26MM NGUYÊN BẢN ĐỨNG (NGOÀI CÙNG BÊN TRÁI)
translate([-38.0, 0, 0]) {
    color([0.98, 0.52, 0.05, 0.95]) { // Bambu Orange
        import("3D_Models/01D_Riser_Standoff_26mm_2S2P.stl");
    }
}

// 2. MẶT CẮT BỔ DỌC CỌC 26MM + 2 TÁN M3 + 2 BU-LÔNG M3 BẮT 2 ĐẦU
translate([-14.0, 0, 0]) {
    difference() {
        color([0.98, 0.52, 0.05, 0.92]) {
            import("3D_Models/01D_Riser_Standoff_26mm_2S2P.stl");
        }
        // Cắt bỏ nửa Y < 0 để nhìn thấy mặt cắt bên trong:
        translate([-20.0, -25.0, -1.0]) cube([40.0, 25.0, 30.0]);
    }
    
    // Tán M3 dưới tại Z = 3.50mm:
    translate([0, 0, 3.50]) m3_hex_nut();
    // Bu-lông M3 bắt từ dưới lên (xuyên qua sàn xe Z=0..4mm, bệ cọc Z=4..7.5mm vào tán):
    translate([0, 0, 0.0]) rotate([180, 0, 0]) m3_bolt(len = 10.0);

    // Tán M3 trên tại Z = 19.75mm:
    translate([0, 0, 19.75]) m3_hex_nut();
    // Bu-lông M3 bắt từ trên xuống (xuyên qua K2 Adapter plate vào tán):
    translate([0, 0, 26.0]) m3_bolt(len = 10.0);
}

// 3. CỌC 44MM NGUYÊN BẢN ĐỨNG
translate([12.0, 0, 0]) {
    color([0.95, 0.42, 0.08, 0.95]) {
        import("3D_Models/01D_Riser_Standoff_44mm_2S2P.stl");
    }
}

// 4. MẶT CẮT BỔ DỌC CỌC 44MM + 2 TÁN M3 + 2 BU-LÔNG M3 BẮT 2 ĐẦU
translate([36.0, 0, 0]) {
    difference() {
        color([0.95, 0.42, 0.08, 0.92]) {
            import("3D_Models/01D_Riser_Standoff_44mm_2S2P.stl");
        }
        translate([-20.0, -25.0, -1.0]) cube([40.0, 25.0, 50.0]);
    }
    
    // Tán M3 dưới tại Z = 3.50mm:
    translate([0, 0, 3.50]) m3_hex_nut();
    translate([0, 0, 0.0]) rotate([180, 0, 0]) m3_bolt(len = 12.0);

    // Tán M3 trên tại Z = 37.75mm:
    translate([0, 0, 37.75]) m3_hex_nut();
    translate([0, 0, 44.0]) m3_bolt(len = 12.0);
}
