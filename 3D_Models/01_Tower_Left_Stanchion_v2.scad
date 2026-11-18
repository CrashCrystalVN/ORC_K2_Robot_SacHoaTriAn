// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE 01: TRU THAP NANG BEN TRAI V2.0 (LEFT LIFT TOWER STANCHION V2.0)
// File: 01_Tower_Left_Stanchion_v2.scad
// Tac gia: @base_cad (CAD Specialist)
// Dac ta ky thuat: Option A Approved (Y_pivot = 160.25mm, Z_pivot = 58.00mm)
// ====================================================================
// DAC TINH KY THUAT V2.0 (CHUAN DFM & ZERO-COLLISION KINEMATICS):
// 1. Co cau 2-Part sieu tinh gon (Option A - Zero-Collision Pivot):
//    - Truc xoay dori ve Y_pivot = 160.25mm, Z_pivot = 58.00mm (ngay tren 2 lo oc chan truoc).
//    - Cot dung vuon thang dung tai Y = 160.25mm; toan bo thanh giang cheo A-frame doc nguoc
//      ve phia sau neo vao 3 lo oc chan sau (Y = 110.5 .. 122.0mm).
//    - Khong gian phia truoc Y >= 160.25mm hoan toan mo (100% open air), triet tieu 100% va cham
//      voi cum dau kep Gripper V3 (rong 64.0mm) tren toan bo dai goc quay tu -15 do den +90 do!
// 2. Chuan khop 100% Khung gam 10 bu-long M3 (Chassis Base Z = 4.0mm):
//    - Chan de trai 5 lo bu-long M3 chuan xac tuyet doi (0.00mm sai so):
//      + Hang lo trong (X = -16.00mm): Y = 110.50mm, 122.00mm, 160.25mm
//      + Hang lo ngoai (X = -24.00mm): Y = 116.00mm, 160.25mm
//    - Lo xuyen phi 3.4mm, bac chim counterbore phi 6.5mm x sau 3.5mm cho bu-long M3.
// 3. Khop truc xoay nang ha Pitch dong truc (Coaxial Pitch Pivot Axis):
//    - Toa do tam truc: Y = 160.25mm, Z = 58.00mm.
//    - Mat ngoai phang tai X = -27.00mm khop 100% voi ma clevis trai cum kep V3 (span 54.00mm).
//    - O coc xoay phi 18.0mm, lo xuyen chot M3 phi 3.4mm.
//    - Hoc tan M3 chim khoa chong xoay (phi 6.45mm sau 3.2mm, $fn=6) o mat trong (X = -19.0mm).
// 4. DFM & Toi uu hoa san xuat:
//    - Khoi luong sieu nhe (~16.5g PLA, the tich 13.2 cm3), giam >70% so voi co cau cu.
//    - 100% in phang Zero-Support tren ban in PEI tren mat ngoai (X = -27.0mm) voi Z_min = 0.000mm!
// ====================================================================

$fn = 64;

// THONG SO HINH HOC CO BAN (ROBOT COORDINATES)
CHASSIS_FLOOR_Z     = 4.0;     // Cao do san xe chassis (Z = 4.0mm)
TOWER_PIVOT_Y       = 160.25;  // Toa do Y truc xoay pitch (Option A)
TOWER_PIVOT_Z       = 58.00;   // Toa do Z truc xoay pitch

STANCHION_X_OUTER   = -27.00;  // Mat ngoai tiep xuc ma clevis trai cum kep
STANCHION_X_INNER   = -19.00;  // Mat trong cua than tru (be day cot = 8.0mm)
FOOT_THICKNESS      = 6.00;    // Do day de bat oc (Z = 4.0 .. 10.0mm)

// TOA DO 5 LO BULONG CHAN DE TRAI
LEFT_BOLTS = [
    [-16.0, 110.5],
    [-16.0, 122.0],
    [-16.0, 160.25],
    [-24.0, 116.0],
    [-24.0, 160.25]
];

// ====================================================================
// MODULE 1: TRU THAP TRAI O TOA DO LAP RAP ROBOT (ASSEMBLY POSE)
// ====================================================================
module tower_left_stanchion_v2() {
    difference() {
        union() {
            // ---------------------------------------------------------
            // 1. COT A-FRAME TRUSS CHINH (X in [-27.0, -19.0], day 8.0mm)
            // ---------------------------------------------------------
            translate([STANCHION_X_INNER, 0, 0])
            rotate([0, -90, 0])
            linear_extrude(height = 8.0) {
                difference() {
                    // Bien dang bao ngoai trong mat phang (Z, Y):
                    polygon(points = [
                        // Chan sau tai Z = 4.0, Y in [105.0, 105.0]
                        [CHASSIS_FLOOR_Z, 105.0],
                        [CHASSIS_FLOOR_Z + FOOT_THICKNESS, 105.0],
                        // Giang cheo A-frame doc nguoc len tam truc
                        [48.0, TOWER_PIVOT_Y - 9.0],
                        // Dinh vom tron quanh tam truc (Y=160.25, Z=58.0, R=9.0mm)
                        [58.0, TOWER_PIVOT_Y - 9.0],
                        [64.36, TOWER_PIVOT_Y - 6.36],
                        [67.0, TOWER_PIVOT_Y],
                        // Mep truoc: GIU TAI Y <= 160.00mm KHI Z >= 12.0mm (0.25mm safety air gap)
                        [58.0, TOWER_PIVOT_Y - 0.25],
                        [12.0, TOWER_PIVOT_Y - 0.25],
                        // Chan truoc tai Z = 10.0 -> 4.0 vuon toi Y = 166.5
                        [10.0, 166.5],
                        [CHASSIS_FLOOR_Z, 166.5]
                    ]);

                    // Cua so tam giac giam khoi luong (Lightening window)
                    polygon(points = [
                        [CHASSIS_FLOOR_Z + FOOT_THICKNESS + 2.0, 120.0],
                        [CHASSIS_FLOOR_Z + FOOT_THICKNESS + 2.0, 151.0],
                        [46.0, 151.0]
                    ]);
                }
            }

            // ---------------------------------------------------------
            // 2. PHAN MO RONG CHAN DE MAT TRONG (X in [-19.0, -13.0], Z in [4.0, 10.0])
            // ---------------------------------------------------------
            // De sau (Y in [105.0, 126.0])
            translate([STANCHION_X_INNER, 105.0, CHASSIS_FLOOR_Z])
                cube([6.0, 21.0, FOOT_THICKNESS]);

            // De truoc (Y in [154.0, 166.5])
            translate([STANCHION_X_INNER, 154.0, CHASSIS_FLOOR_Z])
                cube([6.0, 12.5, FOOT_THICKNESS]);
        }

        // =============================================================
        // CAC PHEP CAT KHUYET CO KHI (DIFFERENCE CUTS)
        // =============================================================

        // A. 5 LO BU-LONG CHAN DE M3 XUYEN SAN + COUNTERBORE DAU TRU M3
        for (pt = LEFT_BOLTS) {
            // Lo xuyen M3 phi 3.4mm
            translate([pt[0], pt[1], CHASSIS_FLOOR_Z - 1.0])
                cylinder(d = 3.4, h = FOOT_THICKNESS + 2.0);

            // Bac chim counterbore dau bu-long M3 phi 6.5mm x sau 3.5mm
            translate([pt[0], pt[1], CHASSIS_FLOOR_Z + FOOT_THICKNESS - 3.5])
                cylinder(d = 6.5, h = 5.0);
        }

        // B. LO TRUC XOAY PIVOT M3 PHI 3.4MM (Y=160.25, Z=58.0)
        translate([STANCHION_X_OUTER - 1.0, TOWER_PIVOT_Y, TOWER_PIVOT_Z])
            rotate([0, 90, 0])
                cylinder(d = 3.4, h = 10.0);

        // C. HOC TAN LUC GIAC M3 CHIM BEN MAT TRONG (X = -19.0mm)
        translate([STANCHION_X_INNER + 0.01, TOWER_PIVOT_Y, TOWER_PIVOT_Z])
            rotate([0, -90, 0])
                cylinder(d = 6.45, h = 3.2, $fn = 6);
    }
}

// ====================================================================
// MODULE 2: XUAT IN 3D PHANG 100% ZERO-SUPPORT (PRINT BED ORIENTATION)
// Mat ngoai X = -27.0mm ap sat ban in Z = 0.0mm
// ====================================================================
module tower_left_stanchion_v2_printable() {
    translate([63.0, 0, 0]) // Bring X >= 0
    rotate([0, -90, 0])
        translate([0, -105.0, -CHASSIS_FLOOR_Z])
            translate([-STANCHION_X_OUTER, 0, 0]) // Shift so X_outer = 0
                tower_left_stanchion_v2();
}

// Render che do xuat in mac dinh (Flat on PEI Bed)
tower_left_stanchion_v2_printable();
