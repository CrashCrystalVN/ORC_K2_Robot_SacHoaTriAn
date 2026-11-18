// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE: TRU THAP PHAI TICH HOP GA DONG CO SERVO MG996R (DIRECT-DRIVE)
// File: 02_Tower_Right_Stanchion_v2.scad
// Phien ban: V2.0 Final Revision (Zero-Collision Y <= 160.25mm above Z=12mm)
// Tac gia: jaws_cad (Antigravity Swarm Architecture)
// ====================================================================

$fn = 48;

CHASSIS_Z_FLOOR     = 4.0;     // Cao do mat san chassis
PIVOT_X             = 27.0;    // Mat ngoai chot xoay
PIVOT_Y             = 160.25;  // Toa do Y truc xoay (Front Foot Centerline)
PIVOT_Z             = 58.0;    // Cao do Z truc xoay (tinh tu mat dat)

FOOT_THICKNESS      = 6.0;     // Do day de chan thap
WALL_THICKNESS      = 8.0;     // Be rong vach thap (X in [19.0, 27.0])

// TOA DO SERVO MG996R (VERTICAL ORIENTATION)
SERVO_SPLINE_Y      = PIVOT_Y; // 160.25mm
SERVO_SPLINE_Z      = PIVOT_Z; // 58.00mm

SERVO_EAR_PITCH_Z   = 48.5;    // Khoang cach 2 lo tai servo theo Z
SERVO_EAR_PITCH_Y   = 10.0;    // Khoang cach 2 lo tai servo theo Y
SERVO_Z_TOP         = SERVO_SPLINE_Z + 13.9;  // 71.9mm
SERVO_Z_BOT         = SERVO_SPLINE_Z - 34.6;  // 23.4mm

module tower_right_stanchion_v2() {
    difference() {
        union() {
            // 1. CHAN DE PHAI (FOOT PAD) - X in [12.0, 27.0], Z in [CHASSIS_Z_FLOOR, CHASSIS_Z_FLOOR + FOOT_THICKNESS]
            // Chan sau (Y in [105.0, 126.0])
            translate([12.0, 105.0, CHASSIS_Z_FLOOR])
                cube([15.0, 21.0, FOOT_THICKNESS]);
            // Chan truoc (Y in [154.0, 166.5])
            translate([12.0, 154.0, CHASSIS_Z_FLOOR])
                cube([15.0, 12.5, FOOT_THICKNESS]);
            // Day de doc theo suon ngoai (X in [19.0, 27.0])
            translate([19.0, 105.0, CHASSIS_Z_FLOOR])
                cube([8.0, 61.5, FOOT_THICKNESS]);

            // 2. COT TRU DUNG TAI Y = 160.25mm (X in [19.0, 27.0])
            hull() {
                translate([19.0, 154.0, CHASSIS_Z_FLOOR]) cube([8.0, 6.25, FOOT_THICKNESS]);
                translate([19.0, PIVOT_Y - 9.0, PIVOT_Z - 9.0]) cube([8.0, 9.0, 18.0]);
                translate([19.0, PIVOT_Y - 9.0, SERVO_Z_TOP - 2.0]) cube([8.0, 9.0, 8.0]);
            }

            // 3. THANH GIANG CHEO A-FRAME TRUSS DOC NGUOC VE PHIA SAU (X in [19.0, 27.0])
            hull() {
                translate([19.0, 105.0, CHASSIS_Z_FLOOR]) cube([8.0, 16.0, FOOT_THICKNESS]);
                translate([19.0, PIVOT_Y - 9.0, PIVOT_Z - 9.0]) cube([8.0, 9.0, 18.0]);
            }
            // Ban webbing tang cung giua cot dung va giang cheo
            hull() {
                translate([19.0, 115.0, 15.0]) cube([8.0, 40.0, 10.0]);
                translate([19.0, PIVOT_Y - 14.0, PIVOT_Z - 10.0]) cube([8.0, 14.0, 20.0]);
            }

            // 4. TAI GA TANG CUONG MAT TRONG CHO 4 LO VIT SERVO (X in [13.0, 19.0])
            // Tai tren (Z around 71.9, Y in [150.0, 160.25])
            hull() {
                translate([13.0, PIVOT_Y - 10.0, SERVO_Z_TOP - 5.0]) cube([6.5, 10.0, 10.0]);
                translate([19.0, PIVOT_Y - 10.0, SERVO_Z_TOP - 8.0]) cube([2.0, 10.0, 15.0]);
            }
            // Tai duoi (Z around 23.4, Y in [150.0, 160.25])
            hull() {
                translate([13.0, PIVOT_Y - 10.0, SERVO_Z_BOT - 5.0]) cube([6.5, 10.0, 10.0]);
                translate([19.0, PIVOT_Y - 10.0, SERVO_Z_BOT - 8.0]) cube([2.0, 10.0, 15.0]);
            }
            // Suon giang noi 2 tai o mat trong
            translate([13.0, PIVOT_Y - 10.0, SERVO_Z_BOT]) cube([6.5, 10.0, SERVO_EAR_PITCH_Z]);
        }

        // =============================================================
        // CAC PHEP CAT KHUYET (DIFFERENCE CUTS)
        // =============================================================

        // A. 5 LO BU-LONG M3 BAT XUONG SAN KHUNG GAM (CHASSIS INTERFACE)
        // - 3 Lo chan sau:
        for (pos = [[16.0, 110.5], [16.0, 122.0], [24.0, 116.0]]) {
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR - 1.0]) cylinder(d = 3.4, h = FOOT_THICKNESS + 2.0);
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR + FOOT_THICKNESS - 3.5]) cylinder(d = 6.5, h = 10.0);
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR + FOOT_THICKNESS - 4.5])
                cylinder(d1 = 3.4, d2 = 6.5, h = 1.0);
        }
        // - 2 Lo chan truoc:
        for (pos = [[16.0, 160.25], [24.0, 160.25]]) {
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR - 1.0]) cylinder(d = 3.4, h = FOOT_THICKNESS + 2.0);
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR + FOOT_THICKNESS - 3.5]) cylinder(d = 6.5, h = 10.0);
            translate([pos[0], pos[1], CHASSIS_Z_FLOOR + FOOT_THICKNESS - 4.5])
                cylinder(d1 = 3.4, d2 = 6.5, h = 1.0);
        }

        // B. VOM CONG THOAT SUON SAN & GIAM TRONG LUONG (Y in [126.0, 152.0])
        translate([10.0, 126.0, CHASSIS_Z_FLOOR - 1.0])
            cube([20.0, 26.0, 12.0]);
        // Vom cong vat nghieng 45 do
        hull() {
            translate([10.0, 128.0, CHASSIS_Z_FLOOR + 11.0]) cube([20.0, 22.0, 1.0]);
            translate([10.0, 134.0, CHASSIS_Z_FLOOR + 16.0]) cube([20.0, 10.0, 1.0]);
        }

        // C. HOC CHU NHAT CHO THAN DONG CO MG996R (20.5 x 41.5mm)
        // Than servo dat dung: Y in [140.0, 160.5mm], Z in [27.3, 68.7mm]
        translate([11.0, PIVOT_Y - 20.25, PIVOT_Z - 30.7])
            cube([9.0, 20.5, 41.5]);

        // D. 4 LO BAT VIT M3 CHO SERVO MG996R + HOC CHIM TAN M3 LUC GIAC
        for (sz = [SERVO_Z_BOT, SERVO_Z_TOP]) {
            for (sy = [PIVOT_Y - SERVO_EAR_PITCH_Y - 0.25, PIVOT_Y - 0.25]) {
                // Lo xuyen vit M3 phi 3.4mm
                translate([11.0, sy, sz]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 18.0);
                // Hoc chim tan luc giac M3 o mat trong (X = 13.0..16.2)
                translate([12.9, sy, sz]) rotate([0, 90, 0]) cylinder(d = 6.45, h = 3.2, $fn = 6);
                // Non tu do 45 do chong sap tan o mat trong (0% support)
                translate([15.9, sy, sz]) rotate([0, 90, 0]) cylinder(d1 = 6.45, d2 = 3.4, h = 1.5);
                // Lo thoat tua-vit phi 6.5mm o mat ngoai (X in [22.0, 28.0])
                translate([22.0, sy, sz]) rotate([0, 90, 0]) cylinder(d = 6.5, h = 6.0);
            }
        }

        // E. LO TRUC CHOT PITCH & KHOP NOI CO TAY CLEVIS
        // 1. Lo thong truc spline / bac chan servo phi 14.0mm
        translate([18.0, PIVOT_Y - 5.0, PIVOT_Z]) rotate([0, 90, 0]) cylinder(d = 14.0, h = 10.0);
        // 2. Lo thoat tua-vit van vit M3 truc chinh servo phi 7.0mm xuyen suot
        translate([10.0, PIVOT_Y, PIVOT_Z]) rotate([0, 90, 0]) cylinder(d = 7.0, h = 20.0);
        // 3. Hoc dia tron 25T phi 21.4mm x sau 1.5mm o mat ngoai
        translate([PIVOT_X - 1.5, PIVOT_Y, PIVOT_Z]) rotate([0, 90, 0]) cylinder(d = 21.4, h = 2.0);

        // F. RANH LUON DAY SERVO (CABLE ROUTING TUNNEL)
        translate([14.0, PIVOT_Y - 14.0, 15.0]) cube([7.0, 7.0, 14.0]);

        // G. TAM GIAC THOANG GIAM TRONG LUONG GIUA THANH GIANG (LIGHTENING POCKET)
        hull() {
            translate([18.0, 122.0, 16.0]) rotate([0, 90, 0]) cylinder(d = 8.0, h = 10.0);
            translate([18.0, 142.0, 16.0]) rotate([0, 90, 0]) cylinder(d = 8.0, h = 10.0);
            translate([18.0, 148.0, 42.0]) rotate([0, 90, 0]) cylinder(d = 8.0, h = 10.0);
        }

        // H. CAT BO HOAN TOAN KHOANG KHONG PHIA TRUOC Y > 160.25mm O CAO DO Z > 12.0mm
        // Triet tieu 100% va cham voi cum dau kep Gripper Base Head V3 tai moi goc quay!
        translate([10.0, PIVOT_Y - 0.05, 12.0])
            cube([20.0, 30.0, 80.0]);
    }
}

module export_tower_right_stanchion_v2() {
    translate([0, 0, PIVOT_X])
        rotate([0, 90, 0])
            tower_right_stanchion_v2();
}

mode = "print"; // ["print", "assembled"]

if (mode == "print") {
    export_tower_right_stanchion_v2();
} else if (mode == "assembled") {
    tower_right_stanchion_v2();
}
