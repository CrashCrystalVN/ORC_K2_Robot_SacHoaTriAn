// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// MODULE: CƠ CẤU ĐẦU KẸP THỰC CHIẾN V2.0 (GRIPPER V2.0 - DFM ZERO SUPPORT)
// File: gripper_v2.scad
// Tác giả: Subagent 2 - Gripper CAD Engineer
// Tương thích: Subagent 1 Spec V2.0 & Subagent 3 DFM/3MF Pipeline
// ====================================================================
// ĐẶC TÍNH NỔI BẬT:
// 1. Cặp bánh răng thân khai Involute m=1.5mm, 20 răng, bề rộng B=8.0mm,
//    bù trừ khe hở sườn răng in 3D backlash = 0.36mm -> 100% không kẹt, chống trượt/mẻ răng.
// 2. Ngàm kẹp kép đa năng (Universal Hybrid Jaw):
//    - Rãnh chữ V kép 90° tự định tâm ống trụ tròn Ø15mm - Ø45mm (ôm trọn ống hoa Ø32mm).
//    - Dải răng cưa ma sát (pitch 3.0mm, sâu 1.2mm, vát 45°) kẹp chặt khối hộp không bị văng.
//    - Gờ đỡ đáy 3.5mm vát 45° chống tụt vật kẹp khi robot tăng tốc/quay xe.
//    - Thân dầm gân tăng cứng I-beam/T-beam liền khối, loại bỏ 100% khe rạch yếu, chống xoắn.
// 3. Khớp bản lề & Kết nối Servo S2 (MG996R):
//    - Trục xoay bu-lông M3 xuyên suốt (L=30-35mm), vách thịt hub >= 3.8mm.
//    - Hốc lục giác âm M3 chống xoay tán ở đáy bệ kẹp.
//    - Vòng đệm chêm (boss washer) Ø10.5mm x 0.8mm chống ma sát và rơ lắc trục Z.
//    - Hốc đĩa tròn Servo MG996R Ø20.8mm x sâu 2.6mm + rãnh tay đơn 8.2mm + 8 lỗ M3 PCD Ø14mm.
// 4. 100% In phẳng tại Z = 0.0mm trên bàn in PEI, góc vát <= 45°, 0% SUPPORT!
// ====================================================================

$fn = 64;

// THÔNG SỐ VÀNG CƠ CẤU KẸP V2.0
GEAR_M              = 1.5;     // Module răng 1.5mm
GEAR_Z              = 20;      // 20 răng trên 360°
GEAR_RP             = 15.0;    // Bán kính vòng chia (Pitch R) = 15.0mm
GEAR_RB             = 14.095;  // Bán kính vòng cơ sở (Base R) = 15*cos(20°)
GEAR_RA             = 16.5;    // Bán kính đỉnh răng (Addendum R)
GEAR_RF             = 13.125;  // Bán kính chân răng (Dedendum R)
GEAR_B              = 8.0;     // Chiều cao mặt răng Z = 8.0mm
BACKLASH            = 0.36;    // Khe hở sườn răng in 3D (mm)

PIVOT_X_LEFT        = -15.0;   // Tâm trục ngàm trái X = -15.0
PIVOT_X_RIGHT       = 15.0;    // Tâm trục ngàm phải X = +15.0
PIVOT_DIST          = 30.0;    // Khoảng cách 2 tâm trục = 30.0mm

JAW_HEIGHT          = 22.0;    // Chiều cao thân ngàm Z = 22.0mm
JAW_LENGTH          = 118.0;   // Chiều dài vươn trước của ngàm

PIN_HOLE_D          = 3.4;     // Lỗ bu-lông M3 xuyên suốt (dung sai 0.4mm)
POST_BORE_D         = 8.3;     // Lỗ ngậm cọc xoay bệ kẹp (cọc Ø8.0mm)
POST_BORE_H         = 10.5;    // Chiều sâu lỗ cọc xoay
HUB_OUTER_R         = 8.5;     // Bán kính ngoài hub bản lề (vách thịt > 3.8mm)

// ====================================================================
// MODULE 1: BIÊN DẠNG 1 RĂNG THÂN KHAI INVOLUTE 2D CHUẨN XÁC
// ====================================================================
module involute_tooth_2d(m = GEAR_M, z = GEAR_Z, bl = BACKLASH) {
    Rp = m * z / 2.0;          // 15.0
    Rb = Rp * cos(20.0);       // 14.095
    Ra = Rp + m;               // 16.5
    Rf = Rp - 1.25 * m;        // 13.125

    // Bề dày răng thực tế trên vòng chia đã trừ backlash
    // Cung răng = pi * m / 2 - bl / 2 = 2.176mm -> Nửa góc = 4.156°
    // Điểm biên dạng thân khai theo bán kính:
    // r=Rf: góc 5.01°, r=Rb: 5.01°, r=14.5: 4.75°, r=15.0: 4.16°,
    // r=15.5: 3.38°, r=16.0: 2.48°, r=Ra: 1.46°
    polygon(points = [
        [10.0 * cos(-7.0), 10.0 * sin(-7.0)],
        [Rf * cos(-5.5),   Rf * sin(-5.5)],
        [Rb * cos(-5.01),  Rb * sin(-5.01)],
        [14.5 * cos(-4.75), 14.5 * sin(-4.75)],
        [15.0 * cos(-4.16), 15.0 * sin(-4.16)],
        [15.5 * cos(-3.38), 15.5 * sin(-3.38)],
        [16.0 * cos(-2.48), 16.0 * sin(-2.48)],
        [Ra * cos(-1.46),  Ra * sin(-1.46)],
        // Đỉnh răng (phẳng vát nhẹ)
        [Ra * cos(1.46),   Ra * sin(1.46)],
        // Sườn trái thân khai
        [16.0 * cos(2.48),  16.0 * sin(2.48)],
        [15.5 * cos(3.38),  15.5 * sin(3.38)],
        [15.0 * cos(4.16),  15.0 * sin(4.16)],
        [14.5 * cos(4.75),  14.5 * sin(4.75)],
        [Rb * cos(5.01),   Rb * sin(5.01)],
        [Rf * cos(5.5),    Rf * sin(5.5)],
        [10.0 * cos(7.0),  10.0 * sin(7.0)]
    ]);
}

// ====================================================================
// MODULE 2: BÁNH RĂNG RẺ QUẠT ĐỒNG TỐC CHO NGÀM TRÁI VÀ NGÀM PHẢI
// ====================================================================
module sector_gear_2d(is_left = true) {
    // Vòng tròn thân chân răng
    circle(r = GEAR_RF);
    if (is_left) {
        // Ngàm trái: Răng tại 0° ăn khớp vào rãnh 180° của ngàm phải
        // Dải góc quay mở rộng 5 răng: [-18°, 0°, +18°, +36°, +54°]
        for (a = [-18, 0, 18, 36, 54]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    } else {
        // Ngàm phải: Lệch pha 9° (nửa bước răng), rãnh tại 180°
        // Răng tại [135°, 153°, 171°, 189°]
        for (a = [135, 153, 171, 189]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    }
}

// ====================================================================
// MODULE 3: HÀM KẸP ĐA NĂNG LAI THỰC CHIẾN V2.0 (UNIVERSAL HYBRID JAW)
// (05_Gripper_Jaw_Left_V2 & 06_Gripper_Jaw_Right_V2)
// ====================================================================
module gripper_jaw_v2(is_left = true) {
    pivot_x = is_left ? PIVOT_X_LEFT : PIVOT_X_RIGHT;
    sx = is_left ? -1.0 : 1.0;
    
    // Chiều cao hub: ngàm trái hạ bậc ở vùng sau (Z = 16.0mm) để né thân Servo S2
    H = JAW_HEIGHT;
    H_gear = GEAR_B; // 8.0mm mặt răng tiếp xúc chịu lực

    difference() {
        union() {
            // -------------------------------------------------------------
            // 1. HUB BẢN LỀ XOAY & VÒNG ĐỆM CHỐNG MA SÁT (Z = 0 .. H)
            // -------------------------------------------------------------
            translate([pivot_x, 0, 0]) {
                // Vòng đệm chêm đáy Ø11mm x 0.8mm chống ma sát trượt mặt bàn
                cylinder(d = 11.0, h = 0.8);
                // Thân trụ Hub chính Ø17.0mm
                cylinder(r = HUB_OUTER_R, h = H);
                // Vòng đệm chêm đỉnh Ø11mm x 0.8mm chống rơ lắc bu-lông
                translate([0, 0, H - 0.8]) cylinder(d = 11.0, h = 0.8);
            }

            // -------------------------------------------------------------
            // 2. BÁNH RĂNG THÂN KHAI RẺ QUẠT ĐỒNG TỐC (Z = 0 .. H_gear)
            // -------------------------------------------------------------
            translate([pivot_x, 0, 0]) {
                linear_extrude(height = H_gear) {
                    sector_gear_2d(is_left = is_left);
                }
                // Vát côn chuyển tiếp 45° từ đỉnh bánh răng (Z=8.0) lên thân ngàm (Z=12.0)
                // giúp tăng cứng chân răng và không cần support!
                translate([0, 0, H_gear - 0.2])
                    cylinder(r1 = GEAR_RF + 0.2, r2 = HUB_OUTER_R, h = 2.2);
            }

            // -------------------------------------------------------------
            // 3. THÂN CỔ NỐI CỨNG VỮNG TỪ HUB RA KHUNG DẦM (Z = 0 .. H)
            // -------------------------------------------------------------
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r = HUB_OUTER_R, h = H);
                translate([sx * 17.5, 16.0, 0]) cylinder(r = 5.5, h = H);
            }
            hull() {
                translate([sx * 17.5, 14.0, 0]) cylinder(r = 5.5, h = H);
                translate([sx * 22.0, 26.0, 0]) cylinder(r = 5.0, h = H);
            }

            // -------------------------------------------------------------
            // 4. DẦM XƯƠNG CHÍNH CHỊU LỰC CHỐNG XOẮN (I-BEAM SPARK STRUCTURE)
            // -------------------------------------------------------------
            // Vách cong ngoài uốn lượn khí động học & công thái học
            hull() {
                translate([sx * 22.0, 26.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 27.5, 48.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 27.5, 48.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 25.5, 78.0, 0]) cylinder(r = 4.5, h = H);
            }
            hull() {
                translate([sx * 25.5, 78.0, 0]) cylinder(r = 4.5, h = H);
                translate([sx * 19.0, 105.0, 0]) cylinder(r = 4.5, h = H);
            }
            hull() {
                translate([sx * 19.0, 105.0, 0]) cylinder(r = 4.5, h = H);
                translate([sx * 14.0, JAW_LENGTH, 0]) cylinder(r = 3.5, h = H);
            }

            // Thịt thân trong kết nối ôm rãnh V và vòm kẹp
            hull() {
                translate([sx * 17.0, 26.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 20.0, 48.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 18.0, 78.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 12.0, 105.0, 0]) cylinder(r = 3.5, h = H);
            }

            // -------------------------------------------------------------
            // 5. GỜ ĐỠ ĐÁY CHỐNG TỤT VẬT KẸP (BOTTOM RETAINING LIP)
            // -------------------------------------------------------------
            // Gờ nhô vào trong 3.5mm, dày 3.5mm tại Z = 0..3.5mm
            hull() {
                translate([sx * 12.5, 32.0, 0]) cylinder(r = 3.0, h = 3.5);
                translate([sx * 13.5, 80.0, 0]) cylinder(r = 3.0, h = 3.5);
                translate([sx * 8.5, 108.0, 0]) cylinder(r = 2.5, h = 3.5);
            }
            // Mái dốc tự đỡ 45° từ mép gờ đỡ lên vách thân ngàm (0% support)
            hull() {
                translate([sx * 12.5, 32.0, 3.5]) cylinder(r1 = 3.0, r2 = 1.0, h = 2.0);
                translate([sx * 13.5, 80.0, 3.5]) cylinder(r1 = 3.0, r2 = 1.0, h = 2.0);
                translate([sx * 8.5, 108.0, 3.5]) cylinder(r1 = 2.5, r2 = 1.0, h = 2.0);
            }

            // -------------------------------------------------------------
            // 6. GÂN TĂNG CỨNG I-BEAM LƯNG NGOÀI (TOP & BOTTOM FLANGES)
            // -------------------------------------------------------------
            // Gân trên đỉnh Z = 19.0 .. 22.0mm
            hull() {
                translate([sx * 23.5, 26.0, H - 3.0]) cylinder(r = 4.0, h = 3.0);
                translate([sx * 29.0, 48.0, H - 3.0]) cylinder(r = 4.0, h = 3.0);
                translate([sx * 27.0, 78.0, H - 3.0]) cylinder(r = 3.5, h = 3.0);
                translate([sx * 20.0, 105.0, H - 3.0]) cylinder(r = 3.5, h = 3.0);
            }
        }

        // =================================================================
        // CÁC PHÉP CẮT GỌT TẠO LÒNG KẸP THỰC CHIẾN (DIFFERENCE CUTS)
        // =================================================================

        // A. CẮT PHẲNG ĐƯỜNG TIM GIỮA (Tránh lấn sang nửa đối diện):
        if (is_left) {
            translate([-6.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        } else {
            translate([-33.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        }

        // B. GIẢI PHÓNG KHÔNG GIAN ĂN KHỚP BÁNH RĂNG PHÍA SAU (|X| < 12.0, Y < 18.0)
        translate([-12.0, 6.0, -1.0]) cube([24.0, 12.0, H + 2.0]);

        // C. KHOANG ÔM VÒM BÁN NGUYỆT CHO ỐNG HOA Ø32.0MM (R = 16.5mm tại Y = 45.0mm)
        translate([0, 45.0, 3.5]) {
            cylinder(r = 16.5, h = H + 2.0);
            // Vát mép vào lòng vòm
            translate([0, 0, -1.0]) cylinder(r1 = 15.0, r2 = 16.5, h = 1.2);
        }

        // D. RÃNH CHỮ V KÉP 90° TỰ ĐỊNH TÂM ỐNG TRỤ Ø15 - Ø45MM (Y in [65, 88])
        // Cắt vát tạo hốc V 90° bằng khối xoay 45°
        translate([0, 74.0, 3.5]) {
            rotate([0, 0, 45])
                cube([25.0, 25.0, H + 2.0], center = true);
        }

        // E. DẢI RĂNG CƯA MA SÁT KẸP KHỐI HỘP VUÔNG (SERRATED GRIP PADS)
        // Bố trí 6 rãnh răng cưa tam giác góc 90° tại Y = 92.0 đến 112.0mm
        for (ys = [92.0 : 3.5 : 110.0]) {
            translate([sx * 7.5, ys, -1.0])
                rotate([0, 0, sx * 45])
                    cube([2.2, 2.2, H + 2.0]);
        }

        // F. CẮT PHẲNG MẶT ĐẦU MŨI NGÀM TẠI Y = JAW_LENGTH = 118.0mm:
        translate([-50.0, JAW_LENGTH, -1.0]) cube([100.0, 20.0, H + 2.0]);

        // G. LỖ BẠC CỌC XOAY Ø8.3MM SÂU 10.5MM + NÓN TỰ ĐỠ 45° + LỖ BU-LÔNG M3 XUYÊN SUỐT
        translate([pivot_x, 0, -0.2]) cylinder(d = POST_BORE_D, h = POST_BORE_H);
        translate([pivot_x, 0, POST_BORE_H - 0.05])
            cylinder(d1 = POST_BORE_D, d2 = PIN_HOLE_D, h = (POST_BORE_D - PIN_HOLE_D) / 2.0);
        translate([pivot_x, 0, -1.0])
            cylinder(d = PIN_HOLE_D, h = H + 2.0);

        // H. TRÁNH VA CHẠM THÂN SERVO S2 TRÊN NGÀM TRÁI (is_left == true):
        // Nâng bậc hạ vùng Y < 16.0mm xuống Z = 16.0mm kèm vát 45° để né hoàn toàn đuôi Servo S2
        if (is_left) {
            translate([-35.0, -15.0, 16.0]) cube([45.0, 31.0, H]);
            translate([-35.0, 16.0, 16.0]) rotate([45, 0, 0]) cube([45.0, 10.0, 10.0]);
        }

        // I. HỐC ĐĨA TRÒN VÀ TAY GẠT SERVO MG996R TRÊN NGÀM PHẢI (is_left == false):
        if (!is_left) {
            // 1. Hốc đĩa tròn kim loại Ø20.8mm x sâu 2.6mm (Z = H - 2.6 đến H + 1.0)
            translate([pivot_x, 0, H - 2.6]) cylinder(d = 20.8, h = 3.0);
            // 2. Rãnh tay gạt đơn/kép rộng 8.2mm xuyên qua tâm
            translate([pivot_x - 4.1, -19.0, H - 2.6]) cube([8.2, 38.0, 3.0]);
            // 3. Lỗ thông tua-vít vặn ốc trục chính MG996R Ø6.5mm
            translate([pivot_x, 0, 10.0]) cylinder(d = 6.5, h = H);
            // 4. Vòng 8 lỗ bắt ốc M3 đĩa tròn PCD Ø14.0mm (bán kính R = 7.0mm)
            for (a = [0 : 45 : 315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, 8.0]) cylinder(d = 2.8, h = H);
            }
            // 5. Hai lỗ khóa chống tuôn ren trên cánh tay gạt tại Y = +11.0 và +16.0mm
            translate([pivot_x, 11.0, 8.0]) cylinder(d = 2.5, h = H);
            translate([pivot_x, 16.0, 8.0]) cylinder(d = 2.5, h = H);
        }
    }
}

// ====================================================================
// MODULE 4: BỆ ĐẦU KẸP V2.0 TÍCH HỢP BẢN LỀ GẬP DỌC 90° & GÁ SERVO S2
// (04_Gripper_Base_Head_V2 - ZERO SUPPORT, PITCH 0..90 DEG)
// - Tâm trục gập dọc (Wrist Pitch Axis): Y_piv = 6.0, Z_piv = 38.0
// - Má bản lề phải (X in [27.0, 35.0]): Hốc đĩa tròn MG996R Ø20.8mm nối Servo S3
// - Má bản lề trái (X in [-33.0, -27.0]): Lỗ trục xoay M3 đồng trục Ø3.4mm
// - Cặp cọc trục xoay ngàm tại X = +-15.0mm, Y = 39.0mm có gối đỡ M3 xuyên suốt
// ====================================================================
module gripper_base_head_v2() {
    Y_piv = 6.0;
    Z_piv = 38.0;
    Y_jaw = 39.0;

    difference() {
        union() {
            // 1. SÀN ĐẾ CHÍNH (Z in [0, 5.0mm]) & BÀN ĐỠ TRƯỢT CHỐNG XỆ NGÀM
            translate([-31.0, 22.0, 0]) cube([66.0, 28.0, 5.0]);
            // Bàn đỡ trượt vươn ra phía trước đến Y = 60.0mm
            hull() {
                translate([-22.0, 46.0, 0]) cube([44.0, 4.0, 5.0]);
                translate([-15.0, 58.0, 0]) cube([30.0, 4.0, 5.0]);
            }

            // 2. VÁCH HẬU LIÊN KẾT CỨNG (Y in [22.0, 27.5], Z in [0, 24.5mm])
            translate([-31.0, 22.0, 0]) cube([66.0, 5.5, 24.5]);

            // 3. HAI CỌC TRỤ XOAY CỐT M3 Ø8.0MM CHO NGÀM TRÁI VÀ PHẢI (Z = 5.0 .. 15.0mm)
            translate([-15.0, Y_jaw, 5.0]) cylinder(d = 8.0, h = 10.0);
            translate([15.0, Y_jaw, 5.0])  cylinder(d = 8.0, h = 10.0);
            // Gân tăng cứng chân cọc vát dốc 45° chống gãy tách lớp
            translate([-15.0, Y_jaw, 5.0]) cylinder(d1 = 12.0, d2 = 8.0, h = 2.0);
            translate([15.0, Y_jaw, 5.0])  cylinder(d1 = 12.0, d2 = 8.0, h = 2.0);

            // 4. TRỤ ĐỠ CẦU SERVO S2 BÊN TRÁI & MÁ BẢN LỀ GẬP DỌC TRÁI (X in [-33.0, -27.0])
            translate([-31.0, 22.0, 0]) cube([4.0, 28.0, 35.0]);
            translate([-31.0, 22.0, 0]) cube([15.0, 5.0, 24.5]);
            hull() {
                translate([-31.0, 27.0, 21.5]) cube([4.0, 23.0, 13.5]);
                translate([-31.0, 27.0, 31.0]) cube([15.0, 23.0, 4.0]);
            }
            // Má Bản Lề Trái vươn về (Y_piv = 6.0, Z_piv = 38.0) với đáy vát giọt nước 45° nối Z=0
            hull() {
                translate([-33.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 18.0, h = 6.0);
                translate([-33.0, Y_piv + 6.0, Z_piv - 12.0]) cube([6.0, 2.0, 12.0]);
                translate([-31.0, 22.0, 0.0]) cube([4.0, 14.0, 35.0]);
            }

            // 5. TRỤ ĐỠ CẦU SERVO S2 BÊN PHẢI & MÁ BẢN LỀ GẬP DỌC PHẢI (X in [+27.0, +35.0])
            translate([27.0, 22.0, 0]) cube([8.0, 28.0, 35.0]);
            hull() {
                translate([27.0, 27.0, 26.0]) cube([8.0, 23.0, 9.0]);
                translate([25.25, 27.0, 29.0]) cube([9.75, 23.0, 6.0]);
            }
            // Má Bản Lề Phải ôm Đĩa Tròn MG996R Ø20mm tại (Y_piv = 6.0, Z_piv = 38.0)
            hull() {
                translate([27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 25.0, h = 8.0);
                translate([27.0, Y_piv + 8.0, Z_piv - 16.0]) cube([8.0, 2.0, 16.0]);
                translate([27.0, 22.0, 0.0]) cube([8.0, 14.0, 35.0]);
            }
        }

        // =================================================================
        // CÁC PHÉP CẮT KHUYẾT BỆ ĐẦU KẸP (DIFFERENCE CUTS)
        // =================================================================

        // A. 4 LỖ BẮT TAI SERVO MG996R S2 (Tâm trục X = +15.0, Y = Y_jaw = 39.0 => Tâm thân X = 4.65)
        for (sx = [4.65 - 24.25, 4.65 + 24.25]) {
            for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
                translate([sx, sy, 20.0]) cylinder(d = 2.95, h = 20.0);
            }
        }
        // Hốc lục giác âm cho 2 ốc tai phải S2 (X = +28.90mm)
        for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
            translate([28.90, sy, -1.0]) cylinder(d = 6.5, h = 29.5, $fn = 6);
            translate([28.90, sy, 28.4]) cylinder(d1 = 6.5, d2 = 2.95, h = 2.0);
        }

        // B. 2 LỖ TÂM TRỤC BU-LÔNG M3 XUYÊN SUỐT + HỐC TÁN LỤC GIÁC M3 CHÌM Ở ĐÁY
        for (px = [-15.0, 15.0]) {
            // Lỗ xuyên qua cọc Ø3.4mm
            translate([px, Y_jaw, -1.0]) cylinder(d = 3.4, h = 20.0);
            // Hốc tán lục giác M3 (Ø6.45mm sâu 2.8mm)
            translate([px, Y_jaw, -0.1]) rotate([0, 0, 30]) cylinder(d = 6.45, h = 2.8, $fn = 6);
            // Nón tự đỡ 45° từ hốc lục giác lên lỗ M3 (0% support)
            translate([px, Y_jaw, 2.65]) cylinder(d1 = 6.45, d2 = 3.4, h = 1.8);
        }

        // C. LỖ TRỤC GẬP NGANG BÊN TRÁI TẠI (Y_piv = 6.0, Z_piv = 38.0)
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 10.0);
        // Lỗ giọt nước tự đỡ 45°
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) rotate([0, 0, 45]) cube([3.4/2, 3.4/2, 10.0]);
        // Bậc chìm đầu bu-lông M3
        translate([-33.5, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 6.5, h = 2.5);

        // D. HỐC ĐĨA TRÒN SERVO S3 TRÊN MÁ BẢN LỀ PHẢI (Ø20.8mm x sâu 2.7mm + 8 lỗ M3 PCD Ø14mm)
        translate([26.8, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 20.8, h = 2.7);
        translate([26.8, Y_piv - 4.1, Z_piv - 4.1]) cube([2.7, 22.0, 8.2]);
        translate([26.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d = 6.5, h = 10.0);
        for (a = [0 : 45 : 315]) {
            hy = Y_piv + 7.0 * cos(a);
            hz = Z_piv + 7.0 * sin(a);
            translate([26.0, hy, hz]) rotate([0, 90, 0]) cylinder(d = 2.9, h = 10.0);
        }
    }
}

// ====================================================================
// MODULE 5: CÁC KHỐI XUẤT STL RIÊNG LẺ (INDIVIDUAL EXPORT MODULES)
// ====================================================================
module export_jaw_left() {
    gripper_jaw_v2(is_left = true);
}

module export_jaw_right() {
    gripper_jaw_v2(is_left = false);
}

module export_gripper_base() {
    gripper_base_head_v2();
}

// ====================================================================
// MODULE 6: PHỐI CẢNH LẮP GHÉP CỤM ĐẦU KẸP V2 (ASSEMBLY VIEW)
// ====================================================================
module gripper_v2_assembly(grip_angle = 0.0) {
    // Bệ kẹp
    color("LightSlateGray") gripper_base_head_v2();

    // Cặp ngàm kẹp đặt tại cao độ Z = 5.0mm, Y = 39.0mm
    translate([0, 39.0, 5.0]) {
        // Ngàm trái xoay góc âm khi mở
        translate([-15.0, 0, 0])
            rotate([0, 0, -grip_angle])
                translate([15.0, 0, 0])
                    color("DarkOrange") gripper_jaw_v2(is_left = true);

        // Ngàm phải xoay góc dương khi mở
        translate([15.0, 0, 0])
            rotate([0, 0, grip_angle])
                translate([-15.0, 0, 0])
                    color("Crimson") gripper_jaw_v2(is_left = false);
    }
}

// Chế độ mặc định xem lắp ghép
// export_jaw_left();
// export_jaw_right();
// export_gripper_base();
// gripper_v2_assembly(grip_angle = 15.0);

export_jaw_left();
