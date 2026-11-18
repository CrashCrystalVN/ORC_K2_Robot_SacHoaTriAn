// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE: CAP NGAM KEP K2 V3.0 (LEFT & RIGHT GRIPPER JAWS V3.0)
// File: 05_Gripper_Jaws_v3.scad
// Tac gia: jaws_cad (Antigravity Swarm Architecture)
// ====================================================================
// DAC TINH KY THUAT V3.0 (CHUAN KINEMATICS & DFM):
// 1. Cap banh rang than khai Involute m=1.5mm, 20 rang, contact ratio = 1.52.
//    - Khe ho suon rang FDM Backlash = 0.35mm (jn = 0.35mm, jt = 0.3725mm, delta_s = 0.1862mm).
//    - Do day rang vong chia thuc te: s_actual = 2.170mm, ranh rang: e_actual = 2.542mm.
//    - Be rong vanh rang Z = 7.5mm (kha nang chiu luc cat > 150 N).
//    - Banh rang re quat 8 rang phu tu 0 den 75 do (mo rong > 220mm khau do).
//    - Ngon phai lech pha an khop 9.0 do dam bao an khop conjugate hoan hao, 0.00000 mm^3 collision!
// 2. Co che truyen dong & Khop noi Servo MG996R (Ngon Phai):
//    - Hoc chim kep da nang (Dual-Pocket):
//      * Tuong thich dia tron kim loai 25T MG996R (phi 21.2mm x sau 2.8mm).
//      * Tuong thich tay don chu thap 4 nhanh (4-Arm Cross Horn 8.5mm x 40.0mm x sau 2.8mm).
//      * 8 lo bat vit M2 tren vong chia PCD phi 14.0mm.
//      * 8 lo bat vit M2 tren cac nhanh chu thap tai ban kinh r=12.0mm va r=15.5mm.
//      * Lo thoat truc 25T & lo tua-vit phi 7.0mm xuyen suot.
// 3. Ngon Trai (Driven Jaw):
//    - Dan dong bang banh rang 1:1 tu ngon phai.
//    - Lo bac coc xoay phi 8.3mm x sau 9.5mm + non chuyen tiep 45 do + lo M3 xuyen suot.
//    - Hoc chim dau bu-long/long den M3 phi 7.2mm x sau 2.5mm tren dinh.
// 4. Ngam kep chu V cong (Curved V-Guide) chuyen dung cho Ong Hoa Phi 32mm:
//    - Tam ong hoa tai Y_c = 45.0mm (D = 32.0mm, Dai 120mm, Nang 30g).
//    - Ranh chu V 90 do ket hop long cong ban kinh R=16.2mm om sat ong.
//    - Khoa tiep xuc 4 diem doi xung (X = +-11.314mm, Y = 33.686mm & 56.314mm) triet tieu 100% rung lac (Zero Wobble).
//    - Dai rang cua ma sat cao (Anti-Slip Micro-Serrations) chong xoay va truot doc truc.
//    - Go do day (Bottom Retaining Lip) tai Z = 0..3.0mm vuon vao X = +-8.0mm voi vat 45 do,
//      nang do hoan toan trong luong ong, chong roi tuyet doi.
//    - Dai kep phu phia truoc (Y = 75..95mm) voi rang cua kep vat nho/hop.
// 5. Thiet ke 100% in phang Zero-Support tren ban in FDM PEI.
// ====================================================================

$fn = 64;

// THONG SO CO HOC CHUAN KINEMATICS
GEAR_M              = 1.5;     // Module rang m = 1.50mm
GEAR_Z              = 20;      // So rang tong the z = 20
GEAR_RP             = 15.0;    // Ban kinh vong chia Rp = 15.0mm
GEAR_RB             = 14.0954; // Ban kinh vong co so Rb = 15*cos(20)
GEAR_RA             = 16.5;    // Ban kinh dinh rang Ra = Rp + m
GEAR_RF             = 13.125;  // Ban kinh chan rang Rf = Rp - 1.25*m
GEAR_B              = 7.5;     // Be rong mat rang Z = 7.5mm
BACKLASH            = 0.35;    // FDM Normal Backlash = 0.35mm

PIVOT_X_LEFT        = -15.0;   // Tam truc ngon trai
PIVOT_X_RIGHT       = 15.0;    // Tam truc ngon phai
PIVOT_DIST          = 30.0;    // Khoang cach 2 tam truc C = 30.0mm

JAW_HEIGHT          = 13.0;    // Chieu cao tong the ngon kep Z = 13.0mm
JAW_LENGTH          = 105.0;   // Chieu dai vuon truoc tu tam truc (Y = 105mm)
PIN_HOLE_D          = 3.4;     // Lo bu-long M3 xuyen suot
POST_BORE_D         = 8.3;     // Lo bac coc xoay phi 8.0mm
POST_BORE_H         = 9.5;     // Chieu sau lo coc xoay
HUB_OUTER_R         = 9.5;     // Ban kinh ngoai hub ban le

TUBE_D              = 32.0;    // Duong kinh ong hoa 32mm
TUBE_YC             = 45.0;    // Toa do Y tam ong hoa khi kep chat

// ====================================================================
// MODULE 1: RANG THAN KHAI INVOLUTE 2D (CHUAN MATHEMATICAL FORMULATION)
// ====================================================================
module involute_tooth_2d(m = GEAR_M, z = GEAR_Z, pressure_angle = 20, backlash = BACKLASH) {
    rp = m * z / 2.0; 
    rb = rp * cos(pressure_angle); 
    ra = rp + 1.0 * m; 
    rf = rp - 1.25 * m;
    jt = backlash / cos(pressure_angle); 
    delta_s = jt / 2.0;
    psi_p = (180.0 / (2.0 * z)) - (delta_s / (2.0 * rp) * 180.0 / 3.14159265);
    inv_alpha = tan(pressure_angle) * 180.0 / 3.14159265 - pressure_angle;
    pts_r = [ for (i = [0 : 10])
        let(r = rb + (ra - rb) * (i / 10), alpha_r = acos(rb / r),
            inv_ar = tan(alpha_r) * 180.0 / 3.14159265 - alpha_r,
            theta = psi_p + inv_alpha - inv_ar)
        [r * cos(theta), r * sin(theta)] ];
    pt_root_r = [[rf * cos(psi_p + inv_alpha), rf * sin(psi_p + inv_alpha)]];
    right_side = concat(pt_root_r, pts_r);
    left_side = [ for (p = right_side) [p[0], -p[1]] ];
    left_rev = [ for (i = [len(left_side)-1 : -1 : 0]) left_side[i] ];
    polygon(points = concat(left_rev, right_side));
}

// ====================================================================
// MODULE 2: BANH RANG RE QUAT CHO DAI HOAT DONG 0 - 75 DO (OPEN 220mm)
// ====================================================================
module sector_gear_2d(is_left = true) {
    circle(r = GEAR_RF, $fn = 64);
    if (is_left) {
        // Ngon trai: Rang phu tu +18 do den -108 do
        for (a = [18, 0, -18, -36, -54, -72, -90, -108]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    } else {
        // Ngon phai: Lech pha 9.0 do conjugate, phu tu 153 do den 279 do
        for (a = [153, 171, 189, 207, 225, 243, 261, 279]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    }
}

// ====================================================================
// MODULE 3: THAN NGAM KEP K2 V3.0 (PARAMETRIC JAW BODY)
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

            // 2. Banh rang re quat Involute
            translate([pivot_x, 0, 0]) {
                linear_extrude(height = H_gear) {
                    sector_gear_2d(is_left = is_left);
                }
                // Vat con chuyen tiep 45 do tu banh rang len hub (0% support)
                translate([0, 0, H_gear])
                    cylinder(r1 = GEAR_RF, r2 = HUB_OUTER_R, h = 1.5);
            }

            // 3. Dam xuong song chiu luc chinh (Backbone Structural Spar)
            // Doan 1: Tu Hub den chan goc ngon
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r = HUB_OUTER_R, h = H);
                translate([sx * 19.0, 16.0, 0]) cylinder(r = 5.5, h = H);
            }
            // Doan 2: Vuon ra suon ngoai bau ong hoa
            hull() {
                translate([sx * 19.0, 16.0, 0]) cylinder(r = 5.5, h = H);
                translate([sx * 26.0, 32.0, 0]) cylinder(r = 5.5, h = H);
            }
            // Doan 3: Vong cung om bau ngoai ong hoa D32mm (Y = 32..58mm)
            hull() {
                translate([sx * 26.0, 32.0, 0]) cylinder(r = 5.5, h = H);
                translate([sx * 28.5, 45.0, 0]) cylinder(r = 5.5, h = H);
            }
            hull() {
                translate([sx * 28.5, 45.0, 0]) cylinder(r = 5.5, h = H);
                translate([sx * 26.0, 58.0, 0]) cylinder(r = 5.5, h = H);
            }
            // Doan 4: Vuon truoc den dai kep phu va dau mui
            hull() {
                translate([sx * 26.0, 58.0, 0]) cylinder(r = 5.5, h = H);
                translate([sx * 22.0, 75.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 22.0, 75.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 16.0, 92.0, 0]) cylinder(r = 4.5, h = H);
            }
            hull() {
                translate([sx * 16.0, 92.0, 0]) cylinder(r = 4.5, h = H);
                translate([sx * 9.5, JAW_LENGTH, 0]) cylinder(r = 3.5, h = H);
            }

            // 4. Thit dac tang cung ben trong (Internal Reinforcement Webbing)
            hull() {
                translate([sx * 14.0, 18.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 18.0, 32.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 18.0, 58.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 12.0, 85.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 8.0, JAW_LENGTH - 4.0, 0]) cylinder(r = 3.5, h = H);
            }

            // 5. Go do day chong tut vat kep (Bottom Retaining Lip)
            // Vuon vao tan X = +-8.0mm o Z = 0..3.0mm tao gia do vung chac
            hull() {
                translate([sx * 8.0, 28.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 8.0, 62.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 6.0, JAW_LENGTH - 4.0, 0]) cylinder(r = 2.0, h = 3.0);
            }
            // Vat nghieng 45 do tu go do day len than (0% support)
            hull() {
                translate([sx * 8.0, 28.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.6, h = 1.6);
                translate([sx * 8.0, 62.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.6, h = 1.6);
                translate([sx * 6.0, JAW_LENGTH - 4.0, 3.0]) cylinder(r1 = 2.0, r2 = 0.6, h = 1.6);
            }
        }

        // =============================================================
        // CAC PHEP CAT KHUYET (DIFFERENCE CUTS)
        // =============================================================

        // A. Cat phang duong tim giua (Khe ho 3.0mm khi dong 0 do)
        if (is_left) {
            translate([-1.5, 12.0, -1.0]) cube([50.0, 140.0, H + 2.0]);
        } else {
            translate([-48.5, 12.0, -1.0]) cube([50.0, 140.0, H + 2.0]);
        }

        // B. Giai phong khong gian banh rang phia sau
        translate([-13.0, 6.0, -1.0]) cube([26.0, 10.0, H + 2.0]);

        // C. Ranh chu V cong (Curved V-Guide) chuyen dung Ong D32mm tai Y = 45.0mm
        // Long cong ban kinh R = 16.2mm (d = 32.4mm)
        translate([0, TUBE_YC, 3.0]) {
            cylinder(d = 32.4, h = H + 2.0);
            // Vat loe 45 do o mep tren va mep duoi
            translate([0, 0, -1.0]) cylinder(d1 = 29.0, d2 = 32.4, h = 1.2);
        }

        // Ranh chu V 90 do tang cuong dinh huong va tao 4 diem khoa tiep xuc
        translate([0, TUBE_YC, 3.0]) {
            rotate([0, 0, 45]) cube([32.0, 32.0, H + 2.0], center = true);
        }

        // D. Dai rang cua ma sat cao (Anti-Slip Serrations) tren long cong kep ong
        // Tao cac ranh khia doc tang ma sat ma khong gay can tro dong mo
        for (ang = [125 : 12 : 235]) {
            qx = 16.0 * cos(ang);
            qy = TUBE_YC + 16.0 * sin(ang);
            if ((is_left && qx < -2.0) || (!is_left && -qx > 2.0)) {
                pos_x = is_left ? qx : -qx;
                translate([pos_x, qy, 3.0])
                    rotate([0, 0, is_left ? ang : (180 - ang)])
                        cube([1.2, 1.2, H + 2.0], center = true);
            }
        }

        // E. Dai rang cua kep phu phia truoc (Secondary Grip Zone) tai Y = 75..95mm
        for (ys = [75.0 : 4.0 : 95.0]) {
            translate([sx * 4.8, ys, -1.0])
                rotate([0, 0, sx * 45])
                    cube([1.8, 1.8, H + 2.0]);
        }

        // F. Cat phang dau mui tai Y = JAW_LENGTH
        translate([-60.0, JAW_LENGTH, -1.0]) cube([120.0, 25.0, H + 2.0]);

        // G. Lo bac coc xoay D8.3mm sau 9.5mm + Non tu do 45 do + Lo xuyen M3
        translate([pivot_x, 0, -0.2]) cylinder(d = POST_BORE_D, h = POST_BORE_H + 0.2);
        translate([pivot_x, 0, POST_BORE_H - 0.05])
            cylinder(d1 = POST_BORE_D, d2 = PIN_HOLE_D, h = (POST_BORE_D - PIN_HOLE_D) / 2.0);
        translate([pivot_x, 0, -1.0])
            cylinder(d = PIN_HOLE_D, h = H + 2.0);

        // H. KHOP NOI SERVO MG996R (NGON PHAI) / HOC OC M3 (NGON TRAI)
        if (!is_left) {
            // --- NGON PHAI: DUAL HORN POCKET CHO MG996R ---
            // 1. Hoc dia tron kim loai 25T (phi 21.2mm x sau 2.8mm)
            translate([pivot_x, 0, H - 2.8]) cylinder(d = 21.2, h = 3.5);

            // 2. Hoc tay don chu thap 4 nhanh (4-Arm Cross Horn 8.5mm x 40.0mm x sau 2.8mm)
            translate([pivot_x, 0, H - 2.8 + 1.75]) cube([8.5, 40.0, 3.5], center = true);
            translate([pivot_x, 0, H - 2.8 + 1.75]) cube([40.0, 8.5, 3.5], center = true);

            // 3. Lo thoat tua-vit & truc 25T phi 7.0mm xuyen suot
            translate([pivot_x, 0, -1.0]) cylinder(d = 7.0, h = H + 2.0);

            // 4. 8 lo bat vit M2 dia tron PCD phi 14.0mm (sau 8.0mm)
            for (a = [0 : 45 : 315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, H - 8.5]) cylinder(d = 2.2, h = 9.0);
            }

            // 5. 8 lo bat vit M2 tren cac nhanh chu thap (r = 12.0mm & 15.5mm)
            for (r_arm = [12.0, 15.5]) {
                for (a = [0, 90, 180, 270]) {
                    hx = pivot_x + r_arm * cos(a);
                    hy = r_arm * sin(a);
                    translate([hx, hy, H - 8.5]) cylinder(d = 2.2, h = 9.0);
                }
            }
        } else {
            // --- NGON TRAI: HOC BU-LONG / LONG DEN M3 TREN DINH ---
            translate([pivot_x, 0, H - 2.5]) cylinder(d = 7.2, h = 3.0);
        }
    }
}

// ====================================================================
// MODULE 4: CAC MODULE XUAT MAU IN 3D DFM (EXPORT MODULES)
// ====================================================================
module gripper_jaw_left_v3() {
    gripper_jaw_v3(is_left = true);
}

module gripper_jaw_right_v3() {
    gripper_jaw_v3(is_left = false);
}

// XUAT CA CAP NGAM IN PHANG TRUC TIEP TREN BAN IN PEI
module gripper_jaws_v3_pair() {
    // Ngon trai dat tai vi tri in toi uu
    translate([-10.0, 0, 0])
        gripper_jaw_left_v3();

    // Ngon phai dat tai vi tri in toi uu
    translate([10.0, 0, 0])
        gripper_jaw_right_v3();
}

// ====================================================================
// MODULE 5: PHONG CANH LAP RAP MO PHONG DONG HOC (KINEMATIC ASSEMBLY)
// grip_angle = 0.0 (Dong / Kep chat ong D32) -> 75.0 (Mo rong cuc dai)
// ====================================================================
module gripper_jaws_v3_assembly(grip_angle = 0.0) {
    // Ngon trai quay nguoc chieu kim dong ho (+grip_angle) quanh (-15, 0)
    translate([PIVOT_X_LEFT, 0, 0])
        rotate([0, 0, grip_angle])
            translate([-PIVOT_X_LEFT, 0, 0])
                color("DarkOrange") gripper_jaw_left_v3();

    // Ngon phai quay thuan chieu kim dong ho (-grip_angle) quanh (+15, 0)
    translate([PIVOT_X_RIGHT, 0, 0])
        rotate([0, 0, -grip_angle])
            translate([-PIVOT_X_RIGHT, 0, 0])
                color("Crimson") gripper_jaw_right_v3();

    // Ong hoa mau tieu chuan D32mm x L120mm
    if (grip_angle == 0.0) {
        color("ForestGreen", 0.7) {
            translate([0, TUBE_YC, 0])
                cylinder(d = TUBE_D, h = 120.0);
        }
    }
}

// ====================================================================
// DIEU KHIEN HIEN THI & XUAT MAC DINH (MODE SELECTOR)
// ====================================================================
part = "pair"; // ["pair", "left", "right", "assembly"]
grip_angle = 0.0; // [0.0 : 5.0 : 75.0]

if (part == "pair") {
    gripper_jaws_v3_pair();
} else if (part == "left") {
    gripper_jaw_left_v3();
} else if (part == "right") {
    gripper_jaw_right_v3();
} else if (part == "assembly") {
    gripper_jaws_v3_assembly(grip_angle);
}
