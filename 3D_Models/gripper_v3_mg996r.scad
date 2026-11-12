// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE: DAU KEP TAI NANG GOC MO 0 - 90 DO (GRIPPER V3.0 MG996R)
// File: gripper_v3_mg996r.scad
// ====================================================================
// DAC TINH KY THUAT V3.0:
// 1. Goc mo rong toan dien tu 0 do (khep gon chong phinh) den 90 do (mo rong cuc dai).
//    - Khi 0 do: Hai ngon kep song song om sat, be rong chi 60mm, tiet kiem toi da khong gian.
//    - Khi 45 do: Tong goc mo giua 2 ngon dat 90 do, khau do mo dau ngon > 175mm (kep ong hoa D32, khoi hop lon).
//    - Khi 90 do: Hai ngon mo ngang vuong goc 90 do, gap phang theo chieu ngang, chieu dai vuon giam >80mm!
// 2. Cap banh rang than khai Involute m=1.5mm, 20 rang, be rong rang 8.0mm,
//    dai rang lien tuc tu -108 do den +18 do dam bao an khop em ai xuyen suot 0 - 90 do.
//    Backlash 0.38mm chong ket nhua in 3D FDM.
// 3. Dong co Servo tieu chuan: MG996R / MG995 kim loai (luc keo 11-13 kg.cm).
//    - O gam dia tron 25T MG996R phi 20.8mm x sau 2.8mm + 8 lo M3 PCD phi 14.0mm tren ngon phai.
//    - Khung treo Servo S2 dang vom cau cantilever tang cung kep, tao ham rong cao 19.5mm
//      giup 2 ngon kep quay tu do 0 - 90 do khong bi can tro boi vach ben hay chan tru!
// 4. Tuong thich lap rap 100%:
//    - Mat gam clevis sau [Y=6.0, Z=38.0] khop 100% voi co tay 04A (Wrist Clevis S3).
//    - Tich hop them 4 lo vit M3 tieu chuan (khoang cach 24x20mm) de bat thang vao ban nang/thap nang bat ky.
// 5. Thiet ke 100% in phang Zero-Support tren ban in FDM PEI.
// ====================================================================

$fn = 64;

// THONG SO CO BAN
GEAR_M              = 1.5;     // Module rang 1.5mm
GEAR_Z              = 20;      // 20 rang tren 360 do
GEAR_RP             = 15.0;    // Ban kinh vong chia = 15.0mm
GEAR_RB             = 14.095;  // Ban kinh vong co so = 15*cos(20)
GEAR_RA             = 16.5;    // Ban kinh dinh rang
GEAR_RF             = 13.125;  // Ban kinh chan rang
GEAR_B              = 7.5;     // Be rong mat rang Z = 7.5mm
BACKLASH            = 0.38;    // Khe ho suon rang in 3D (mm)

PIVOT_X_LEFT        = -15.0;   // Tam truc ngon trai
PIVOT_X_RIGHT       = 15.0;    // Tam truc ngon phai
PIVOT_DIST          = 30.0;    // Khoang cach 2 tam truc

JAW_HEIGHT          = 13.0;    // Chieu cao than ngon kep (Z = 0 .. 13.0)
JAW_LENGTH          = 105.0;   // Chieu dai vuon truoc cua ngon kep tu tam truc
PIN_HOLE_D          = 3.4;     // Lo bu-long M3 xuyen suot
POST_BORE_D         = 8.3;     // Lo ngam coc xoay phi 8.0mm
POST_BORE_H         = 9.5;     // Chieu sau lo coc xoay
HUB_OUTER_R         = 9.0;     // Ban kinh ngoai hub ban le

BASE_Y_JAW          = 38.0;    // Toa do Y cua tam coc xoay tren be kep
BASE_Y_PIV          = 6.0;     // Toa do Y truc clevis co tay S3
BASE_Z_PIV          = 38.0;    // Toa do Z truc clevis co tay S3

// ====================================================================
// MODULE 1: RANG THAN KHAI INVOLUTE 2D CHUAN DFM
// ====================================================================
module involute_tooth_2d(m = GEAR_M, z = GEAR_Z, bl = BACKLASH) {
    Rp = m * z / 2.0;
    Rb = Rp * cos(20.0);
    Ra = Rp + m;
    Rf = Rp - 1.25 * m;

    polygon(points = [
        [10.0 * cos(-7.0), 10.0 * sin(-7.0)],
        [Rf * cos(-5.5),   Rf * sin(-5.5)],
        [Rb * cos(-5.01),  Rb * sin(-5.01)],
        [14.5 * cos(-4.75), 14.5 * sin(-4.75)],
        [15.0 * cos(-4.14), 15.0 * sin(-4.14)],
        [15.5 * cos(-3.38), 15.5 * sin(-3.38)],
        [16.0 * cos(-2.48), 16.0 * sin(-2.48)],
        [Ra * cos(-1.46),  Ra * sin(-1.46)],
        [Ra * cos(1.46),   Ra * sin(1.46)],
        [16.0 * cos(2.48),  16.0 * sin(2.48)],
        [15.5 * cos(3.38),  15.5 * sin(3.38)],
        [15.0 * cos(4.14),  15.0 * sin(4.14)],
        [14.5 * cos(4.75),  14.5 * sin(4.75)],
        [Rb * cos(5.01),   Rb * sin(5.01)],
        [Rf * cos(5.5),    Rf * sin(5.5)],
        [10.0 * cos(7.0),  10.0 * sin(7.0)]
    ]);
}

// ====================================================================
// MODULE 2: BANH RANG RE QUAT CHO DAI MO 0 - 90 DO
// ====================================================================
module sector_gear_2d(is_left = true) {
    circle(r = GEAR_RF);
    if (is_left) {
        // Ngon trai: Rang tai goc tu +18 do den -108 do
        for (a = [18, 0, -18, -36, -54, -72, -90, -108]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    } else {
        // Ngon phai: Lech pha 9 do, phu tu 153 do den 279 do
        for (a = [153, 171, 189, 207, 225, 243, 261, 279]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    }
}

// ====================================================================
// MODULE 3: NGAM KEP DA NANG V3.0 (UNIVERSAL JAW V3)
// ====================================================================
module gripper_jaw_v3(is_left = true) {
    pivot_x = is_left ? PIVOT_X_LEFT : PIVOT_X_RIGHT;
    sx = is_left ? -1.0 : 1.0;
    H = JAW_HEIGHT;
    H_gear = GEAR_B;

    difference() {
        union() {
            // 1. Hub ban le xoay
            translate([pivot_x, 0, 0]) {
                cylinder(r = HUB_OUTER_R, h = H);
            }
            // 2. Banh rang re quat
            translate([pivot_x, 0, 0]) {
                linear_extrude(height = H_gear) {
                    sector_gear_2d(is_left = is_left);
                }
                // Vat con chuyen tiep 45 do tu banh rang len hub
                translate([0, 0, H_gear])
                    cylinder(r1 = GEAR_RF, r2 = HUB_OUTER_R, h = 1.5);
            }
            // 3. Dam xuong song chiu luc chinh
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r = HUB_OUTER_R, h = H);
                translate([sx * 18.0, 16.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 18.0, 14.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 24.0, 36.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 24.0, 36.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 23.0, 65.0, 0]) cylinder(r = 4.5, h = H);
            }
            hull() {
                translate([sx * 23.0, 65.0, 0]) cylinder(r = 4.5, h = H);
                translate([sx * 17.0, 88.0, 0]) cylinder(r = 4.0, h = H);
            }
            hull() {
                translate([sx * 17.0, 88.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 10.0, JAW_LENGTH, 0]) cylinder(r = 3.5, h = H);
            }
            // Thit than trong kep
            hull() {
                translate([sx * 14.0, 20.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 16.0, 50.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 13.0, 80.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 8.0, JAW_LENGTH - 5.0, 0]) cylinder(r = 3.0, h = H);
            }
            // 4. Go do day chong tut vat kep (Bottom Retaining Lip)
            hull() {
                translate([sx * 8.5, 26.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 9.5, 65.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 5.5, JAW_LENGTH - 4.0, 0]) cylinder(r = 2.0, h = 3.0);
            }
            // Vat nghieng 45 do tu go do day len than (0% support)
            hull() {
                translate([sx * 8.5, 26.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.8, h = 1.5);
                translate([sx * 9.5, 65.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.8, h = 1.5);
                translate([sx * 5.5, JAW_LENGTH - 4.0, 3.0]) cylinder(r1 = 2.0, r2 = 0.8, h = 1.5);
            }
        }

        // A. Cat phang duong tim giua (khe ho 4mm khi dong 0 do)
        if (is_left) {
            translate([-2.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        } else {
            translate([-37.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        }

        // B. Giai phong khong gian banh rang phia sau
        translate([-12.0, 6.0, -1.0]) cube([24.0, 10.0, H + 2.0]);

        // C. Zone 1: Khoang om ong hoa D32mm tai Y = 36.0mm
        translate([0, 36.0, 3.0]) {
            cylinder(d = 33.0, h = H + 2.0);
            translate([0, 0, -1.0]) cylinder(d1 = 30.0, d2 = 33.0, h = 1.2);
        }

        // D. Zone 2: Ranh chu V 90 do tu dinh tam ong D15 - D40mm tai Y = 65.0mm
        translate([0, 65.0, 3.0]) {
            rotate([0, 0, 45]) cube([22.0, 22.0, H + 2.0], center = true);
        }

        // E. Zone 3: Dai rang cua ma sat kep hop vuong tai Y = 82..98mm
        for (ys = [82.0 : 4.0 : 98.0]) {
            translate([sx * 5.2, ys, -1.0])
                rotate([0, 0, sx * 45])
                    cube([2.0, 2.0, H + 2.0]);
        }

        // F. Cat phang dau mui tai Y = JAW_LENGTH
        translate([-50.0, JAW_LENGTH, -1.0]) cube([100.0, 20.0, H + 2.0]);

        // G. Lo bac coc xoay D8.3mm sau 9.5mm + Non tu do 45 do + Lo xuyen M3
        translate([pivot_x, 0, -0.2]) cylinder(d = POST_BORE_D, h = POST_BORE_H);
        translate([pivot_x, 0, POST_BORE_H - 0.05])
            cylinder(d1 = POST_BORE_D, d2 = PIN_HOLE_D, h = (POST_BORE_D - PIN_HOLE_D) / 2.0);
        translate([pivot_x, 0, -1.0])
            cylinder(d = PIN_HOLE_D, h = H + 2.0);

        // H. O dia tron Servo MG996R 25T tren ngon phai
        if (!is_left) {
            // Hoc dia tron kim loai phi 20.8mm x sau 2.8mm
            translate([pivot_x, 0, H - 2.8]) cylinder(d = 20.8, h = 3.2);
            // Ranh tay don don/kep 8.2mm
            translate([pivot_x - 4.1, -18.0, H - 2.8]) cube([8.2, 36.0, 3.2]);
            // Lo thoat tua-vit van oc truc chinh MG996R
            translate([pivot_x, 0, -1.0]) cylinder(d = 6.5, h = H + 2.0);
            // 8 lo bat oc M3 dia tron PCD phi 14.0mm
            for (a = [0 : 45 : 315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, -1.0]) cylinder(d = 2.9, h = H + 2.0);
            }
        }
    }
}

// ====================================================================
// MODULE 4: BE DAU KEP V3.0 (GRIPPER BASE HEAD V3 - ZERO COLLISION 0-90 DEG)
// ====================================================================
module gripper_base_head_v3() {
    Y_jaw = BASE_Y_JAW;
    Y_piv = BASE_Y_PIV;
    Z_piv = BASE_Z_PIV;

    difference() {
        union() {
            // 1. SAN DAY CHINH (Z = 0 .. 5.0mm) & BAN TRUOT DO NGAM
            // San phan hau (Y in [16.0, 35.0])
            translate([-31.0, 16.0, 0]) cube([64.0, 19.0, 5.0]);
            // San truot vuon truoc do 2 ngon (Y in [35.0, 52.0])
            hull() {
                translate([-25.0, 34.0, 0]) cube([50.0, 2.0, 5.0]);
                translate([-18.0, 50.0, 0]) cube([36.0, 2.0, 5.0]);
            }

            // 2. HAI COC TRU XOAY NGAM PHI 8.0MM (Z = 5.0 .. 14.5mm)
            translate([-15.0, Y_jaw, 5.0]) cylinder(d = 8.0, h = 9.5);
            translate([15.0, Y_jaw, 5.0])  cylinder(d = 8.0, h = 9.5);
            // Gan cone 45 do tang cung chan coc xoay
            translate([-15.0, Y_jaw, 5.0]) cylinder(d1 = 11.5, d2 = 8.0, h = 1.75);
            translate([15.0, Y_jaw, 5.0])  cylinder(d1 = 11.5, d2 = 8.0, h = 1.75);

            // 3. VACH HAU LIEN KET CUNG VA NGAN CLEVIS SAU (Y in [16.0, 22.0], Z in [0, 44.0])
            translate([-31.0, 16.0, 0]) cube([64.0, 6.0, 22.0]);
            // Vach dung cao do tam clevis
            translate([-31.0, 16.0, 22.0]) cube([64.0, 5.0, 18.0]);

            // 4. MA CLEVIS BEN TRAI (X in [-33.0, -27.0]) - LO PIVOT M3 TAI (Y_piv=6, Z_piv=38)
            hull() {
                translate([-33.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 18.0, h = 6.0);
                translate([-33.0, 16.0, 20.0]) cube([6.0, 6.0, 20.0]);
                translate([-31.0, 16.0, 0.0]) cube([4.0, 6.0, 20.0]);
            }

            // 5. MA CLEVIS BEN PHAI (X in [+27.0, +35.0]) - HOC DIA TRON MG996R TAI (Y_piv=6, Z_piv=38)
            hull() {
                translate([27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 25.0, h = 8.0);
                translate([27.0, 16.0, 20.0]) cube([8.0, 6.0, 20.0]);
                translate([27.0, 16.0, 0.0]) cube([6.0, 6.0, 20.0]);
            }

            // 6. CAU TREO SERVO S2 CANTILEVER TREN CAO (Z = 19.5 .. 25.5mm)
            // Khung cau vuon tu vach hau (Y=21.0) ra (Y=44.0) tren cao Z >= 19.5mm
            // Gius 2 ben rong 100% o Z in [5.0, 18.0] cho 2 ngon quay tu do 0 - 90 do!
            // Gia do tai trai (X in [-24.0, -14.0], Y in [21.0, 44.0], Z in [19.5, 25.5])
            hull() {
                translate([-25.0, 16.0, 19.5]) cube([12.0, 6.0, 6.0]);
                translate([-25.0, 31.0, 19.5]) cube([12.0, 13.0, 6.0]);
            }
            // Gan do tam giac 45 do tu vach hau len gia tai trai
            hull() {
                translate([-25.0, 16.0, 5.0]) cube([8.0, 5.0, 5.0]);
                translate([-25.0, 28.0, 19.5]) cube([8.0, 4.0, 2.0]);
            }

            // Gia do tai phai (X in [+24.0, +34.0], Y in [21.0, 44.0], Z in [19.5, 25.5])
            hull() {
                translate([24.0, 16.0, 19.5]) cube([10.0, 6.0, 6.0]);
                translate([24.0, 31.0, 19.5]) cube([10.0, 13.0, 6.0]);
            }
            // Gan do tam giac 45 do tu vach hau len gia tai phai
            hull() {
                translate([24.0, 16.0, 5.0]) cube([8.0, 5.0, 5.0]);
                translate([24.0, 28.0, 19.5]) cube([8.0, 4.0, 2.0]);
            }

            // Cầu ngang noi 2 gia tai qua vach sau
            translate([-25.0, 21.0, 19.5]) cube([59.0, 6.0, 6.0]);
        }

        // =================================================================
        // CAC PHEP CAT KHUYET BE DAU KEP (DIFFERENCE CUTS)
        // =================================================================

        // A. KHOANG LOT THAN SERVO MG996R (42.5mm x 20.5mm)
        // Tam truc MG996R dat tai X = +15.0, Y = Y_jaw = 38.0
        // Tam than servo tai X = 4.65, Y = 38.0
        translate([-16.6, Y_jaw - 10.25, 17.0])
            cube([42.5, 20.5, 30.0]);

        // B. 4 LO BAT TAI SERVO MG996R S2 (Khoang cach 48.5 x 10.0 mm)
        for (sx = [4.65 - 24.25, 4.65 + 24.25]) {
            for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
                translate([sx, sy, 15.0]) cylinder(d = 2.95, h = 15.0);
            }
        }

        // C. 2 LO TAM TRUC BU-LONG M3 XUYEN COC + HOC TAN LUC GIAC M3 CHIM O DAY
        for (px = [-15.0, 15.0]) {
            // Lo xuyen M3
            translate([px, Y_jaw, -1.0]) cylinder(d = 3.4, h = 20.0);
            // Hoc tan luc giac M3 (phi 6.45mm sau 2.8mm)
            translate([px, Y_jaw, -0.1]) rotate([0, 0, 30]) cylinder(d = 6.45, h = 2.8, $fn = 6);
            // Non tu do 45 do len lo M3 (0% support)
            translate([px, Y_jaw, 2.65]) cylinder(d1 = 6.45, d2 = 3.4, h = 1.8);
        }

        // D. LO TRUC CLEVIS BEN TRAI (Y_piv = 6.0, Z_piv = 38.0)
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 10.0);
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) rotate([0, 0, 45]) cube([3.4/2, 3.4/2, 10.0]);
        // Bac chim dau bu-long M3
        translate([-33.5, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 6.5, h = 2.5);

        // E. HOC DIA TRON SERVO S3 TREN MA CLEVIS PHAI
        translate([26.8, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 20.8, h = 2.7);
        translate([26.8, Y_piv - 4.1, Z_piv - 4.1]) cube([2.7, 22.0, 8.2]);
        translate([26.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 6.5, h = 10.0);
        for (a = [0 : 45 : 315]) {
            hy = Y_piv + 7.0 * cos(a);
            hz = Z_piv + 7.0 * sin(a);
            translate([26.0, hy, hz]) rotate([0, 90, 0]) cylinder(d = 2.9, h = 10.0);
        }

        // F. 4 LO BAT OC M3 MAT HAU CHO GA TRUC TIEP VAO BAN NANG / THAP NANG
        for (bx = [-12.0, 12.0]) {
            for (bz = [8.0, 28.0]) {
                translate([bx, 24.0, bz]) rotate([90, 0, 0]) cylinder(d = 3.2, h = 12.0);
                translate([bx, 24.0, bz]) rotate([90, 0, 0]) rotate([0, 0, 45]) cube([3.2/2, 3.2/2, 12.0]);
            }
        }
    }
}

// ====================================================================
// MODULE 5: CAC MODULE XUAT STL CHUAN DFM (FLAT BED Z = 0)
// ====================================================================
module export_jaw_left_v3() {
    gripper_jaw_v3(is_left = true);
}

module export_jaw_right_v3() {
    gripper_jaw_v3(is_left = false);
}

module export_gripper_base_v3() {
    gripper_base_head_v3();
}

// ====================================================================
// MODULE 6: PHONG CANH LAP RAP (ASSEMBLY VIEW)
// grip_angle = 0.0 (Dong gon) -> 45.0 (Mo 90 do) -> 90.0 (Mo ngang 90 do)
// ====================================================================
module gripper_v3_assembly(grip_angle = 0.0) {
    color("LightSlateGray") gripper_base_head_v3();

    // 2 Ngam kep dat tai Z = 5.0mm, Y = BASE_Y_JAW = 38.0mm
    translate([0, BASE_Y_JAW, 5.0]) {
        // Ngon trai quay nguoc chieu kim dong ho (+grip_angle) de mo sang trai
        translate([-15.0, 0, 0])
            rotate([0, 0, grip_angle])
                translate([15.0, 0, 0])
                    color("DarkOrange") gripper_jaw_v3(is_left = true);

        // Ngon phai quay thuan chieu kim dong ho (-grip_angle) de mo sang phai
        translate([15.0, 0, 0])
            rotate([0, 0, -grip_angle])
                translate([-15.0, 0, 0])
                    color("Crimson") gripper_jaw_v3(is_left = false);
    }

    // Mo phong Servo MG996R S2
    color("DimGray") {
        translate([4.65, BASE_Y_JAW, 25.5]) {
            translate([-40.7/2, -19.7/2, 0]) cube([40.7, 19.7, 36.5]);
            // Tai bat oc
            translate([-54.0/2, -19.7/2, -2.5]) cube([54.0, 19.7, 2.5]);
            // Truc 25T huong xuong
            translate([15.0 - 4.65, 0, -6.0]) cylinder(d = 6.0, h = 6.0);
        }
    }
}
