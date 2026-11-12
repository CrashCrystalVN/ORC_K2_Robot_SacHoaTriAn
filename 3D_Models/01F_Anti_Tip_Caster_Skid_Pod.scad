// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// PHỤ KIỆN: VẤU TRƯỢT & GÁ BI MẮT TRÂU CHỐNG CHÚI / BẬP BÊNH (ANTI-TIP CASTER SKID POD)
// FILE: 01F_Anti_Tip_Caster_Skid_Pod.scad
// PHIÊN BẢN V11.0: DÀNH CHO KHUNG GẦM ULTRA-SLIM 120
// KHỚP 100% 2 LỖ M3 KHOẢNG CÁCH 16MM & HỐC ĐỊNH VỊ Ø14MM TRÊN SÀN XE
// ====================================================================

$fn = 36;

// CẤU HÌNH CHIỀU CAO TƯƠNG ỨNG BÁNH XE:
// Omni 48mm -> Ground clearance 4.0mm -> POD_HEIGHT = 4.0mm
// Omni 58mm -> Ground clearance 9.0mm -> POD_HEIGHT = 9.0mm
POD_HEIGHT  = 4.0;   // Chiều cao đệm dưới gầm (mm)
BOSS_D      = 13.8;  // Đường kính gờ lồi định vị khớp hốc sàn Ø14mm
BOSS_H      = 1.5;   // Chiều cao gờ định vị (mm)
POD_W       = 14.0;  // Bề rộng vấu trượt (mm)
POD_L       = 24.0;  // Chiều dài vấu trượt (mm)
HOLE_SP     = 16.0;  // Khoảng cách 2 lỗ ốc M3 (mm)
BALL_D      = 12.0;  // Đường kính bi trợ lực (mm)

module anti_tip_skid_pod() {
    difference() {
        union() {
            // 1. Thân chính hình bầu dục vát cạnh trượt êm
            hull() {
                translate([0, -HOLE_SP/2.0, 0])
                    cylinder(d=POD_W, h=POD_HEIGHT);
                translate([0,  HOLE_SP/2.0, 0])
                    cylinder(d=POD_W, h=POD_HEIGHT);
            }
            
            // 2. Gờ lồi định vị cắm vào hốc sàn chassis (Z = POD_HEIGHT..POD_HEIGHT + BOSS_H)
            translate([0, 0, POD_HEIGHT])
                cylinder(d=BOSS_D, h=BOSS_H);
                
            // 3. Mũi trượt vát cong bán cầu chống mắc kẹt góc sân
            hull() {
                translate([0, -HOLE_SP/2.0, 1.0])
                    sphere(d=POD_W * 0.9);
                translate([0,  HOLE_SP/2.0, 1.0])
                    sphere(d=POD_W * 0.9);
            }
        }
        
        // 2 Lỗ ốc M3 xuyên suốt kèm vát chìm đầu vít bắt ngược từ dưới lên
        for (sy = [-HOLE_SP/2.0, HOLE_SP/2.0]) {
            translate([0, sy, -1.0])
                cylinder(d=3.4, h=POD_HEIGHT + BOSS_H + 2.0);
            translate([0, sy, -0.5])
                cylinder(d=6.2, h=2.5);
        }
        
        // Hốc bi lăn Ø12mm (nếu người dùng muốn lắp bi mắt trâu rời)
        translate([0, 0, -0.5])
            cylinder(d=BALL_D, h=POD_HEIGHT * 0.6);
    }
}

anti_tip_skid_pod();
