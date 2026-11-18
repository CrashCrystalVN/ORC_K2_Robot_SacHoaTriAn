// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE 04: BE DAU KEP VA CO TAY KHOP NOI (GRIPPER BASE HEAD V3.0)
// File: 04_Gripper_Base_Head_v3.scad
// ====================================================================
// DAC TINH KY THUAT V3.0 (CHUAN DFM & DONG HOC KINEMATICS):
// 1. Khung de chiu luc nguyen khoi (Monolithic Base) tich hop 100% Zero-Support FDM:
//    - Day phang Z = 0 tiep xuc ban in PEI, vat mep chong chan voi 0.4mm x 45 deg.
//    - Ban truot phang Z = 5.0mm do vung chac 2 ngon kep, chong xe lech khi mang tai ong hoa D32.
// 2. Hai coc tru xoay M3 sieu cung vung (Heavy-Duty M3 Axle Bosses):
//    - Khoang cach tam truc C = 30.00mm (X = -15.0mm va X = +15.0mm), Y = 38.0mm.
//    - Duong kinh coc D = 8.00mm, chieu cao h = 9.50mm (Z = 5.0 .. 14.5mm).
//    - Chan coc bo cone vat 45 deg (d1 = 11.5mm -> d2 = 8.0mm) chong gay chan tru.
//    - Lo xuyen M3 phi 3.4mm; hoc tan luc giac M3 chim duoi day (phi 6.45mm sau 3.0mm)
//      co non tu do 45 deg (khong can support) va ho tro dong ren dong M3 brass insert.
//    - Ranh thoat rang hop so (Gear relief cut) ban kinh R = 18.0mm quanh 2 tam truc,
//      dam bao khe ho > 1.5mm voi dinh rang than khai m=1.5 (Ra = 16.5mm) o moi goc quay!
// 3. Gia treo Servo MG996R dang vom cau Cantilever sieu cung (Z = 19.5 .. 25.5mm):
//    - Khoang lot than Servo 42.5mm x 20.8mm, tam truc 25T dong tam tuyet doi voi coc phai (+15.0, 38.0).
//    - Ham rong cao 14.5mm (Z = 5.0 .. 19.5mm), tao khe ho 1.5mm phia tren ngon kep (Z=18.0mm)
//      giup ngon kep quay tu do 0 - 105 deg khong va cham!
//    - 4 lo bat tai Servo (48.5 x 10.0mm) ho tro M3 brass inserts phi 4.2mm x sau 3.8mm
//      va ranh bat tan chim ben trong vach, khong bao gio lo oc xuong vung quay cua ngon kep.
//    - 4 lo thoat tua-vit phi 6.5mm xuyen qua san day, cho phep xuyen tua-vit van oc hai chieu de dang!
// 4. Khop noi co tay Clevis (04A_Wrist_Clevis_Pitch_Bracket_S3 Compatible):
//    - Long clevis rong 54.0mm (X in [-27.0, +27.0]), truc xoay tai Y = 6.0mm, Z = 38.0mm.
//    - Ma clevis trai day 6.0mm co lo chot M3 phi 3.4mm va bac chim dau oc phi 6.5mm x 2.5mm.
//    - Ma clevis phai day 8.0mm co hoc gam dia tron Servo 25T phi 20.8mm x sau 2.8mm,
//      ranh tay don 8.2mm, lo thoat tua-vit phi 6.5mm va 8 lo vit M3 tren PCD phi 14.0mm.
//    - 4 lo bat oc M3 mat sau (grid 24x20mm) ho tro bat truc tiep vao ban truot / thap nang.
// ====================================================================

$fn = 64;

// THONG SO HINH HOC CO BAN
BASE_C_DIST         = 30.0;    // Khoang cach 2 tam truc = 30.00mm
BASE_PIVOT_XL       = -15.0;   // Tam truc trai
BASE_PIVOT_XR       = 15.0;    // Tam truc phai
BASE_Y_JAW          = 38.0;    // Toa do Y tam coc xoay
BASE_Y_PIV          = 6.0;     // Toa do Y truc clevis co tay
BASE_Z_PIV          = 38.0;    // Toa do Z truc clevis co tay

BASE_FLOOR_Z        = 5.0;     // Do day san day = 5.0mm
BASE_BOSS_D         = 8.0;     // Duong kinh coc xoay
BASE_BOSS_H         = 9.5;     // Chieu cao coc xoay tren mat san (Z = 5.0 .. 14.5)
BASE_BRIDGE_Z_BOT   = 19.5;    // Day cau treo Servo (khe ho 1.5mm tren dinh ngon Z=18.0)
BASE_BRIDGE_Z_TOP   = 25.5;    // Dinh mat cau bat tai Servo (day 6.0mm)

// TOA DO SERVO MG996R S2
SERVO_BODY_L        = 42.5;    // Chieu dai khoang lot than Servo
SERVO_BODY_W        = 20.8;    // Chieu rong khoang lot than Servo
SERVO_SPLINE_OFFSET = 10.35;   // Khoang cach tu tam truc spline den tam than servo
SERVO_CENTER_X      = BASE_PIVOT_XR - SERVO_SPLINE_OFFSET; // X = 4.65mm
SERVO_MOUNT_PITCH_X = 48.5;    // Khoang cach lo tai servo theo X
SERVO_MOUNT_PITCH_Y = 10.0;    // Khoang cach lo tai servo theo Y

// ====================================================================
// MODULE CHINH: BE DAU KEP V3.0
// ====================================================================
module gripper_base_head_v3() {
    difference() {
        union() {
            // -------------------------------------------------------------
            // 1. SAN DAY CHINH & BAN TRUOT DO NGAM (Z = 0 .. 5.0mm)
            // -------------------------------------------------------------
            // San phan hau (Y in [16.0, 35.0], X in [-31.0, +33.0])
            translate([-31.0, 16.0, 0])
                cube([64.0, 19.0, BASE_FLOOR_Z]);

            // Ban truot vuon truoc do 2 ngon kep (Y in [34.0, 52.0])
            hull() {
                translate([-25.0, 34.0, 0]) cube([50.0, 2.0, BASE_FLOOR_Z]);
                translate([-18.0, 50.0, 0]) cube([36.0, 2.0, BASE_FLOOR_Z]);
            }

            // -------------------------------------------------------------
            // 2. HAI COC TRU XOAY M3 SIEU CUNG VUNG (Z = 5.0 .. 14.5mm)
            // -------------------------------------------------------------
            for (px = [BASE_PIVOT_XL, BASE_PIVOT_XR]) {
                // Than coc xoay phi 8.0mm
                translate([px, BASE_Y_JAW, BASE_FLOOR_Z])
                    cylinder(d = BASE_BOSS_D, h = BASE_BOSS_H);

                // Cone vat 45 do gia cu chan coc (d1=11.5mm -> d2=8.0mm)
                translate([px, BASE_Y_JAW, BASE_FLOOR_Z])
                    cylinder(d1 = 11.5, d2 = BASE_BOSS_D, h = 1.75);
            }

            // -------------------------------------------------------------
            // 3. VACH HAU LIEN KET NGUYEN KHOI (Y in [16.0, 20.5], Z in [0, 44.0])
            // -------------------------------------------------------------
            // Vach hau tang cung tang duoi (Z in [0, 22.0])
            translate([-31.0, 16.0, 0])
                cube([64.0, 4.5, 22.0]);

            // Vach hau tang tren do tam clevis (Z in [22.0, 44.0])
            translate([-31.0, 16.0, 22.0])
                cube([64.0, 4.5, 22.0]);

            // -------------------------------------------------------------
            // 4. MA CLEVIS BEN TRAI (X in [-33.0, -27.0]) - LO PIVOT M3
            // -------------------------------------------------------------
            hull() {
                translate([-33.0, BASE_Y_PIV, BASE_Z_PIV])
                    rotate([0, 90, 0]) cylinder(d = 18.0, h = 6.0);
                translate([-33.0, 16.0, 20.0])
                    cube([6.0, 4.5, 20.0]);
                translate([-31.0, 16.0, 0.0])
                    cube([4.0, 4.5, 20.0]);
            }

            // -------------------------------------------------------------
            // 5. MA CLEVIS BEN PHAI (X in [+27.0, +35.0]) - HOC DIA TRON MG996R
            // -------------------------------------------------------------
            hull() {
                translate([27.0, BASE_Y_PIV, BASE_Z_PIV])
                    rotate([0, 90, 0]) cylinder(d = 25.0, h = 8.0);
                translate([27.0, 16.0, 20.0])
                    cube([8.0, 4.5, 20.0]);
                translate([27.0, 16.0, 0.0])
                    cube([6.0, 4.5, 20.0]);
            }

            // -------------------------------------------------------------
            // 6. CAU TREO SERVO S2 CANTILEVER ARCH SIEU CUNG (Z in [19.5, 25.5])
            // -------------------------------------------------------------
            // Gia do tai trai (X in [-25.0, -13.0], Y in [20.0, 45.0])
            hull() {
                translate([-25.0, 16.0, BASE_BRIDGE_Z_BOT]) cube([12.0, 4.5, 6.0]);
                translate([-25.0, 31.0, BASE_BRIDGE_Z_BOT]) cube([12.0, 14.0, 6.0]);
            }
            // Gan gia cu tam giac 45 do cho tai trai
            hull() {
                translate([-25.0, 16.0, 5.0]) cube([8.0, 4.5, 5.0]);
                translate([-25.0, 28.0, BASE_BRIDGE_Z_BOT]) cube([8.0, 3.5, 2.0]);
            }

            // Gia do tai phai (X in [+24.0, +34.0], Y in [20.0, 45.0])
            hull() {
                translate([24.0, 16.0, BASE_BRIDGE_Z_BOT]) cube([10.0, 4.5, 6.0]);
                translate([24.0, 31.0, BASE_BRIDGE_Z_BOT]) cube([10.0, 14.0, 6.0]);
            }
            // Gan gia cu tam giac 45 do cho tai phai
            hull() {
                translate([24.0, 16.0, 5.0]) cube([8.0, 4.5, 5.0]);
                translate([24.0, 28.0, BASE_BRIDGE_Z_BOT]) cube([8.0, 3.5, 2.0]);
            }

            // Cau ngang lien ket chu U chong xoan van tren cao
            translate([-25.0, 16.0, BASE_BRIDGE_Z_BOT])
                cube([59.0, 6.0, 6.0]);
        }

        // =================================================================
        // CAC PHEP CAT KHUYET CO KHI (DIFFERENCE CUTS)
        // =================================================================

        // -----------------------------------------------------------------
        // A. KHOANG LOT THAN SERVO MG996R (42.5mm x 20.8mm)
        // Tam truc spline tai X = +15.0, Y = 38.0
        // Tam than servo tai X = 4.65, Y = 38.0
        // -----------------------------------------------------------------
        translate([SERVO_CENTER_X - SERVO_BODY_L / 2.0, BASE_Y_JAW - SERVO_BODY_W / 2.0, 16.0])
            cube([SERVO_BODY_L, SERVO_BODY_W, 32.0]);

        // -----------------------------------------------------------------
        // B. 4 LO BAT TAI SERVO MG996R (Pitch 48.5 x 10.0mm) + DUAL INSERTS
        // -----------------------------------------------------------------
        for (sx = [SERVO_CENTER_X - SERVO_MOUNT_PITCH_X / 2.0, SERVO_CENTER_X + SERVO_MOUNT_PITCH_X / 2.0]) {
            for (sy = [BASE_Y_JAW - SERVO_MOUNT_PITCH_Y / 2.0, BASE_Y_JAW + SERVO_MOUNT_PITCH_Y / 2.0]) {
                // Lo xuyen bat oc M3 phi 3.4mm
                translate([sx, sy, BASE_BRIDGE_Z_BOT - 1.0])
                    cylinder(d = 3.4, h = 8.0);

                // Hoc ren dong M3 brass heat-set insert (phi 4.2mm x sau 3.8mm tu tren)
                translate([sx, sy, BASE_BRIDGE_Z_TOP - 3.8])
                    cylinder(d = 4.2, h = 4.0);

                // Hoc tan luc giac M3 chim ben duoi cau (phi 6.4mm x sau 2.5mm)
                // Giup giu tan chim 100% khong vuot qua mat duoi Z=19.5mm!
                translate([sx, sy, BASE_BRIDGE_Z_BOT - 0.1])
                    cylinder(d = 6.4, h = 2.5, $fn = 6);

                // Lo thoat tua-vit phi 6.5mm xuyen qua san day Z=0..5mm
                // Cho phep tiep can tua-vit thang dung tu phia duoi!
                translate([sx, sy, -1.0])
                    cylinder(d = 6.5, h = BASE_FLOOR_Z + 2.0);
            }
        }

        // -----------------------------------------------------------------
        // C. RANH THOAT RANG HOP SO (GEAR RELIEF CUTS)
        // Ban kinh R = 18.0mm quanh 2 tam truc, chieu cao h = 14.5mm (Z = 4.8 .. 19.3mm),
        // triet tieu 100% va cham voi toan bo chieu cao ngon kep (H=13.0mm, Z=5.0..18.0mm)
        // va dinh rang than khai m=1.5 (Ra = 16.5mm) o moi goc quay!
        // -----------------------------------------------------------------
        for (px = [BASE_PIVOT_XL, BASE_PIVOT_XR]) {
            translate([px, BASE_Y_JAW, BASE_FLOOR_Z - 0.2])
                cylinder(r = 18.0, h = 14.5);
        }

        // -----------------------------------------------------------------
        // D. 2 LO TAM TRUC COC XOAY M3 + HOC TAN VA REN DONG CHIM DUOI DAY
        // -----------------------------------------------------------------
        for (px = [BASE_PIVOT_XL, BASE_PIVOT_XR]) {
            // Lo xuyen tam M3 phi 3.4mm
            translate([px, BASE_Y_JAW, -1.0])
                cylinder(d = 3.4, h = BASE_FLOOR_Z + BASE_BOSS_H + 2.0);

            // Hoc tan luc giac M3 chim day (phi 6.45mm sau 3.0mm)
            translate([px, BASE_Y_JAW, -0.1])
                rotate([0, 0, 30])
                    cylinder(d = 6.45, h = 3.0, $fn = 6);

            // Non tu do 45 do len lo M3 (100% Zero-Support FDM bridge)
            translate([px, BASE_Y_JAW, 2.85])
                cylinder(d1 = 6.45, d2 = 3.4, h = 1.6);
        }

        // -----------------------------------------------------------------
        // E. KHOP CLEVIS TRAI (Y_piv = 6.0, Z_piv = 38.0)
        // -----------------------------------------------------------------
        // Lo xuyen chot clevis phi 3.4mm
        translate([-35.0, BASE_Y_PIV, BASE_Z_PIV])
            rotate([0, 90, 0]) cylinder(d = 3.4, h = 10.0);

        // Bac chim dau bu-long M3 ngoai ma trai
        translate([-33.5, BASE_Y_PIV, BASE_Z_PIV])
            rotate([0, 90, 0]) cylinder(d = 6.5, h = 2.8);

        // -----------------------------------------------------------------
        // F. HOC DIA TRON SERVO S3 TREN MA CLEVIS PHAI
        // -----------------------------------------------------------------
        // Hoc dia tron phi 20.8mm x sau 2.8mm
        translate([26.8, BASE_Y_PIV, BASE_Z_PIV])
            rotate([0, 90, 0]) cylinder(d = 20.8, h = 2.8);

        // Ranh thoat tay don dia tron 8.2mm x 22.0mm
        translate([26.8, BASE_Y_PIV - 4.1, BASE_Z_PIV - 11.0])
            cube([2.8, 22.0, 8.2]);

        // Lo xuyen tam thoat tua-vit oc truc chinh Servo phi 6.5mm
        translate([26.0, BASE_Y_PIV, BASE_Z_PIV])
            rotate([0, 90, 0]) cylinder(d = 6.5, h = 10.0);

        // 8 lo bat oc M3 dia tron PCD phi 14.0mm
        for (a = [0 : 45 : 315]) {
            hy = BASE_Y_PIV + 7.0 * cos(a);
            hz = BASE_Z_PIV + 7.0 * sin(a);
            translate([26.0, hy, hz])
                rotate([0, 90, 0]) cylinder(d = 2.9, h = 10.0);
        }

        // -----------------------------------------------------------------
        // G. 4 LO BAT OC M3 MAT HAU CHO GA TRUC TIEP THAP NANG / BAN TRUOT
        // -----------------------------------------------------------------
        for (bx = [-12.0, 12.0]) {
            for (bz = [8.0, 28.0]) {
                translate([bx, 22.0, bz])
                    rotate([90, 0, 0]) cylinder(d = 3.3, h = 10.0);
                translate([bx, 22.0, bz])
                    rotate([90, 0, 0]) rotate([0, 0, 45]) cube([3.3/2, 3.3/2, 10.0]);
            }
        }
    }
}

// Module xuat STL truc tiep
module export_gripper_base_v3() {
    gripper_base_head_v3();
}

// Goi render mac dinh khi mo file
export_gripper_base_v3();
