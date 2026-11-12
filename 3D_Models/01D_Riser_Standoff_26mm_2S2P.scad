// ====================================================================
// DỰ ÁN: ROBOT ORC K2 - SẮC HOA TRI ÂN (STEM THPT NGÔ QUYỀN & 20/11)
// CỌC ĐÔN KÉP M3 DUAL-NUT STANDOFF 26MM CHO PIN 2S2P
// FILE: 01D_Riser_Standoff_26mm_2S2P.scad
// CHIỀU CAO: H = 26.0 mm | ĐƯỜNG KÍNH NGOÀI: Ø11.6 mm
// D-FLAT CHỐNG VA CHẠM NẸP MOTOR SAU: Y = -5.3 mm (R_-Y = 5.30 mm <= 5.50 mm)
// ====================================================================

$fn = 60;

module dual_nut_standoff_m3(h = 26.0, od = 11.6, d_flat_y = -5.3) {
    r = od / 2.0;
    slot_w = 5.80;       // Rãnh nhét tán M3 rộng 5.80mm (DIN 934 s=5.50mm, chống xoay cực chắc)
    slot_h = 2.75;       // Chiều cao khe trượt 2.75mm (tán M3 dày 2.40mm, đút trơn tru)
    slot_depth = 3.25;   // Khoét vào quá tâm 3.25mm (đồng tâm 100% với trục Ø3.5mm)
    base_t = 3.50;       // Bệ chịu lực đáy dày 3.50mm (Z in [0.0, 3.50])
    top_t = 3.50;        // Bệ chịu lực đỉnh dày 3.50mm (Z in [h-3.50, h])
    bore_d = 3.50;       // Lỗ trục đứng xuyên suốt Ø3.50mm từ -1 đến h+1
    ch = 0.50;           // Chamfer vát mép 45° chống chân voi (elephant's foot)

    difference() {
        // 1. Thân trụ chính tròn Ø11.6mm kèm vát mép 45° hai đầu
        union() {
            cylinder(d1 = od - 2.0*ch, d2 = od, h = ch);
            translate([0, 0, ch]) cylinder(d = od, h = h - 2.0*ch);
            translate([0, 0, h - ch]) cylinder(d1 = od, d2 = od - 2.0*ch, h = ch);
        }

        // 2. Vát phẳng D-flat ở mặt -Y (cách tâm 5.30mm) chống va chạm nẹp motor sau GA25
        translate([-od, -od + d_flat_y, -1.0])
            cube([2.0*od, od, h + 2.0]);

        // 3. Lỗ trục đứng xuyên suốt 100% Ø3.50mm cho bu-lông / ty ren M3
        translate([0, 0, -1.0])
            cylinder(d = bore_d, h = h + 2.0);

        // 4. Vát côn dẫn hướng Ø4.5mm -> Ø3.5mm ở 2 miệng lỗ trục
        translate([0, 0, -0.01])
            cylinder(d1 = bore_d + 1.0, d2 = bore_d, h = ch + 0.02);
        translate([0, 0, h - ch - 0.01])
            cylinder(d1 = bore_d, d2 = bore_d + 1.0, h = ch + 0.02);

        // 5. HỐC CÀI TÁN M3 DƯỚI (Z in [base_t, base_t + slot_h] = [3.50, 6.25 mm])
        translate([-slot_depth, -slot_w/2.0, base_t])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        // Vát mép mở rộng miệng vào rãnh 0.5mm:
        translate([r - 0.5, -slot_w/2.0 - 0.5, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        // DFM 45° Roof Chamfer chống xệ sợi nhựa khi in FDM đứng:
        translate([0, 0, base_t + slot_h - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);

        // 6. HỐC CÀI TÁN M3 TRÊN (Z in [h - top_t - slot_h, h - top_t] = [19.75, 22.50 mm])
        translate([-slot_depth, -slot_w/2.0, h - top_t - slot_h])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        // Vát mép mở rộng miệng vào rãnh 0.5mm:
        translate([r - 0.5, -slot_w/2.0 - 0.5, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        // DFM 45° Roof Chamfer chống xệ sợi nhựa:
        translate([0, 0, h - top_t - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);
    }
}

// Xuất chi tiết đứng thẳng theo trục Z chuẩn in 3D FDM:
dual_nut_standoff_m3(h = 26.0, od = 11.6, d_flat_y = -5.3);
