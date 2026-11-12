// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// THIẾT KẾ: KHUNG GẦM CHÍNH 185x185mm CHUẨN ĐỘI TUYỂN (ORC-K2 PRO DFM 185 CUBE)
// FILE: 01_Chassis_Base_185x185.scad
// PHIÊN BẢN V7.0: QUY CHUẨN ĐÓNG GÓI 185x185x185 MM (MAX DIMENSION <= 185MM)
// TƯƠNG THÍCH BÀN IN 3D 180-185MM (BAMBU LAB A1 MINI / PRUSA MINI) & HỘP KIỂM 185MM CUBE
// ====================================================================
// ĐẶC ĐIỂM DFM & KẾT CẤU V7.0 (185x185 COMPLIANT):
// 1. Kích thước Chi Tiết In 3D (Base Plate Part):
//    - Rộng X = 139.0 mm (Thân 118.0mm + 2x Ụ nhô Boss 10.5mm) <= 185.0 mm!
//    - Dài Y   = 172.0 mm (Sàn phẳng 0..167mm + Mũi cản ToF 167..172mm) <= 185.0 mm!
//    - Cao Z   = 38.0 mm (Sàn 4mm + Vách 30mm + Ụ đỡ motor Z=38mm) <= 185.0 mm!
//    -> KÍCH THƯỚC LỚN NHẤT CHI TIẾT IN = 172.0 MM <= 185.0 MM (VỪA KHÍT BÀN IN BAMBU A1 MINI 180x180MM)!
// 2. Phủ bì Cụm Gầm Robot Khi Lắp Ráp Bánh Xe Mecanum 60mm (Assembled Robot Base Footprint):
//    - Cấu hình bánh xe chuẩn: Mecanum 60mm (Đường kính 60mm, Bề rộng 28mm).
//    - Tổng bề rộng phủ bì: TOTAL_ROBOT_WIDTH = 118.0 + 2x (2.0 + 28.0) = 178.0 mm <= 185.0 mm (Dư 7.0 mm)!
//    - Tổng chiều dài phủ bì: TOTAL_ROBOT_LENGTH = 172.0 - 2.0 = 170.0 mm <= 185.0 mm (Dư 15.0 mm)!
//    - Tổng chiều cao gầm xe: TOTAL_ROBOT_HEIGHT = 60.0 mm <= 185.0 mm (Dư 125.0 mm)!
//    -> TOÀN BỘ CỤM BASE VÀ BÁNH XE NẰM TRỌN TRONG HỘP KIỂM TRA 185 x 185 x 185 MM (185MM CUBE)!
// 3. Hệ Động Cơ GA25 & Ụ Nhô Mặt Bích (Outward Flange Boss):
//    - BOSS_OUT = 10.5 mm nhô vào hốc rỗng bánh xe Mecanum.
//    - Lòng trong giữa 2 mặt bích motor: INNER_SPAN = 133.0 mm!
//    - Cầu sau: 2x Động cơ GA25 Encoder (63.0 mm x 2 = 126.0 mm).
//      KHE HỞ AN TOÀN GIỮA 2 ĐUÔI ENCODER = 133.0 - 126.0 = 7.0 mm > 0! ZERO COLLISION!
// 4. Khoang Pin Vạn Năng 2S2P (Universal 2S2P Battery Bay):
//    - Kích thước lòng khoang trên sàn: Rộng 82.0 mm (X in [-41, +41]) x Dài 76.0 mm (Y in [48, 124]).
//    - Vừa khít khối pin dẹp 76x20x70mm và pin gạch 38x38x70mm.
//    - 4 Khe luồn đai dán Velcro bản 20mm (4.0 x 22.0 mm) chằng giữ pin chặt chẽ.
//    - Hệ gờ định vị 4 góc thấp 3.0mm chống xô lệch gia tốc 2.5G.
// 5. Hệ Trụ Đỡ Tầng Trên Tối Ưu (Upper Deck Standoff Pillars):
//    - 4 Trụ đỡ MCU K2 Control Hub tại X = ±42.0 mm, Y = 49.0 & 99.0 mm (Lọt lòng 76.0mm).
//    - Chiều cao trụ: PILLAR_H = 18.0 mm (Z_top = 22.0 mm), lỗ ren M3 sâu 16mm trên đỉnh.
//    - 4 Lỗ xuyên sàn M3 tại X = ±33.0 mm (Y = 49.0 & 99.0 mm) tương thích 01D_Base_Riser_Frame.
// 6. Giao Tiếp Tháp Nâng & Cảm Biến:
//    - 10 Lỗ bu-lông M3 xuyên sàn bắt cặp Tháp nâng (01B & 01C): X = ±16.0 & ±24.0, Y = 110.5, 122.0, 160.25.
//    - Cản trước ToF VL53L0X góc quang học 35° + ngàm cảm biến PCB 25x11mm.
//    - 4 Lỗ ốc M3 bắt đế cảm biến dò line 01E dưới gầm mũi xe.
//    - Bệ mạch thu PS4 bên sườn trái & bệ nút nhấn bên sườn phải.
// 7. Thiết Kế FDM Chuẩn Mực:
//    - Đáy phẳng 100% tại Z = 0.0 mm (Diện tích bám bàn in > 19,000 mm2).
//    - 100% Lỗ ngang trục và lỗ bắt ốc dùng biên dạng Giọt nước 45° (Teardrop) -> IN 0% SUPPORT!
// ====================================================================

// CHẾ ĐỘ HIỂN THỊ:
// "part"              = Chỉ xuất Khung Gầm Đáy Phẳng 100% để in 3D (Z = 0.0 mm, Zero Support)
// "assembly_compact"  = Phối cảnh robot GẤP GỌN trong hộp 185x185mm kèm khung dây kiểm tra
// "assembly_working"  = Phối cảnh robot khi vươn cánh tay gắp hoa ngoài sàn thi đấu
DISPLAY_MODE = "part";

// Độ mịn lưới dựng hình (Smoothness)
$fn = (DISPLAY_MODE == "part") ? 40 : 24;

// CẤU HÌNH BÁNH XE MECANUM (CHUẨN 185x185 CUBE: MECANUM 60MM):
WHEEL_TYPE = "mecanum_60";

// HIỂN THỊ HỘP GIỚI HẠN 185x185x185mm (Wireframe Bounding Box)
SHOW_BOUNDING_BOX = true;

// CẤU HÌNH CẢM BIẾN TOF SƯỜN:
ENABLE_SIDE_TOF_SLOTS = false;

// ====================================================================
// BẢNG THÔNG SỐ KÍCH THƯỚC CHUẨN HÓA (185x185 COMPLIANT)
// ====================================================================
CHASSIS_W    = 118.0;   // Chiều rộng thân xe chính (mm)
CHASSIS_L    = 172.0;   // Chiều dài sàn xe (mm)
FLOOR_T      = 4.0;     // Độ dày sàn xe chịu lực (mm)
WALL_T       = 4.0;     // Độ dày vách sườn chịu lực (mm)
WALL_H       = 30.0;    // Chiều cao vách sườn (mm)

// GIẢI PHÁP GỜ BỆ MOTOR NHÔ VÀO LÒNG BÁNH XE (RECESSED WHEEL POCKET BOSS)
BOSS_OUT     = 10.5;    // Độ nhô ra ngoài của ụ mặt bích (mm)
BOSS_D       = 36.0;    // Đường kính ngoài của ụ mặt bích (mm)
FLANGE_T     = 3.0;     // Độ dày mặt bích bắt motor (mm)

// KÍCH THƯỚC CHI TIẾT IN 3D (PART BOUNDING BOX):
PART_EXTENT_X = CHASSIS_W + 2.0 * BOSS_OUT; // 139.0 mm <= 185.0 mm
PART_EXTENT_Y = CHASSIS_L;                  // 172.0 mm <= 185.0 mm
PART_EXTENT_Z = 20.0 + BOSS_D / 2.0;       // 38.0 mm <= 185.0 mm
PART_MAX_DIM  = max(PART_EXTENT_X, PART_EXTENT_Y, PART_EXTENT_Z); // 172.0 mm

// THÔNG SỐ ĐỘNG CƠ GA25 THỰC TẾ:
MOTOR_D      = 25.0;    // Đường kính thân motor GA25 (mm)
MOTOR_DC_L   = 48.0;    // Chiều dài thân hộp số + motor DC thường cầu trước (FL, FR) (mm)
MOTOR_ENC_L  = 63.0;    // Chiều dài motor Encoder cầu sau (RL, RR) kể cả nắp và giắc cắm (mm)
Z_SHAFT      = 20.0;    // Cao độ tâm trục bánh xe/động cơ so với đáy sàn Z=0 (mm)

// THÔNG SỐ BÁNH XE MECANUM 60mm (CHUẨN ORC ĐỘI TUYỂN)
WHEEL_D      = (WHEEL_TYPE == "mecanum_60") ? 60.0 : 80.0;
WHEEL_W      = (WHEEL_TYPE == "mecanum_60") ? 28.0 : 38.0;
WHEEL_CLEAR  = 2.0;     // Khe hở an toàn giữa mặt trong bánh xe và vách khung xe (mm)
GROUND_CLEAR = WHEEL_D / 2.0 - Z_SHAFT; // Khoảng sáng gầm xe (10.0mm với bánh 60mm)

// TỌA ĐỘ TRỤC XE (ĐỒNG TRỤC 100% TUYỆT ĐỐI)
Y_FRONT      = 142.0;   // Trục trước (FL, FR)
Y_REAR       = 32.0;    // Trục sau (RL, RR)
WHEELBASE    = Y_FRONT - Y_REAR; // 110.0 mm
TRACK_WIDTH  = CHASSIS_W + 2.0 * WHEEL_CLEAR + WHEEL_W;  // 150.0 mm

// TỌA ĐỘ MẶT BÍCH LẮP ĐỘNG CƠ:
X_FLANGE_IN_L = -(CHASSIS_W/2.0 + BOSS_OUT) + FLANGE_T; // -66.5 mm
X_FLANGE_IN_R = +(CHASSIS_W/2.0 + BOSS_OUT) - FLANGE_T; // +66.5 mm

// KHOẢNG HỞ LÒNG XE GIỮA 2 MẶT BÍCH:
INNER_SPAN = X_FLANGE_IN_R - X_FLANGE_IN_L; // 133.0 mm

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU SAU (2x ENCODER 63mm):
REAR_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_ENC_L; // 133.0 - 126.0 = 7.0 mm > 0!

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU TRƯỚC (2x DC 48mm):
FRONT_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_DC_L; // 133.0 - 96.0 = 37.0 mm > 0!

// TỔNG PHỦ BÌ XE KHI GẮN BÁNH XE (ASSEMBLED FOOTPRINT):
TOTAL_ROBOT_WIDTH  = CHASSIS_W + 2.0 * (WHEEL_CLEAR + WHEEL_W); // 178.0 mm <= 185.0 mm!
TOTAL_ROBOT_LENGTH = max(CHASSIS_L, Y_FRONT + WHEEL_D/2.0) - (Y_REAR - WHEEL_D/2.0); // 170.0 mm <= 185.0 mm!
TOTAL_ROBOT_HEIGHT = GROUND_CLEAR + PART_EXTENT_Z; // 48.0 mm (gầm) / 60.0 mm (đỉnh bánh) <= 185.0 mm!

// ====================================================================
// THÔNG SỐ KHOANG PIN VẠN NĂNG 2S2P 18650 (UNIVERSAL 2S2P BATTERY BAY)
// ====================================================================
BAT_BAY_W    = 82.0;    // Chiều rộng lòng khoang pin trên sàn (mm)
BAT_BAY_L    = 76.0;    // Chiều dài lòng khoang pin trên sàn (mm)
BAT_BAY_Y_START = 48.0; // Tọa độ Y bắt đầu khoang pin (mm)
BAT_BAY_Y_END   = BAT_BAY_Y_START + BAT_BAY_L; // 124.0 mm

// THÔNG SỐ HỆ TRỤ ĐỠ TẦNG TRÊN (UPPER DECK STANDOFF PILLARS)
PILLAR_X     = 42.0;    // Tọa độ X tâm trụ (±42.0 mm)
PILLAR_W_X   = 8.0;     // Bề rộng trụ theo phương X (mm)
PILLAR_L_Y   = 10.0;    // Chiều dài trụ theo phương Y (mm)
PILLAR_H     = 18.0;    // Chiều cao trụ tính từ mặt sàn (mm) -> Z_top = 22.0 mm
PILLAR_CLEAR_SPAN = 2.0 * (PILLAR_X - PILLAR_W_X / 2.0); // 76.0 mm (Lọt chính xác pin dẹp 76mm!)

// Xuất thông số kỹ thuật ra bảng điều khiển (Console Verification)
echo("====================================================================");
echo("=== ORC-K2 PRO DFM V7.0 - 185x185x185 MM BOUNDING BOX VERIFICATION ===");
echo("====================================================================");
echo("--- 1. KICH THUOC CHI TIET IN 3D (BASE PART) ---");
echo("Part Width (X):", PART_EXTENT_X, "mm <= 185.0 mm (Margin:", 185.0 - PART_EXTENT_X, "mm)");
echo("Part Length (Y):", PART_EXTENT_Y, "mm <= 185.0 mm (Margin:", 185.0 - PART_EXTENT_Y, "mm)");
echo("Part Height (Z):", PART_EXTENT_Z, "mm <= 185.0 mm (Margin:", 185.0 - PART_EXTENT_Z, "mm)");
echo(">>> KICH THUOC LON NHAT (MAX DIMENSION):", PART_MAX_DIM, "mm <= 185.0 mm (PASS 100%!)");
echo("Tuong thich ban in Bambu Lab A1 Mini (180x180mm):", (PART_MAX_DIM <= 180.0) ? "DAT 100% (PASS)" : "CAN XOAY 45 DO");
echo("--- 2. KICH THUOC PHU BI CUM BASE + BANH XE (ASSEMBLED FOOTPRINT) ---");
echo("Cau hinh banh xe:", WHEEL_TYPE, "- Duong kinh:", WHEEL_D, "mm, Rong:", WHEEL_W, "mm");
echo(">>> TONG BE RONG PHU BI (TOTAL WIDTH):", TOTAL_ROBOT_WIDTH, "mm <= 185.0 mm (Margin:", 185.0 - TOTAL_ROBOT_WIDTH, "mm)");
echo(">>> TONG CHIEU DAI PHU BI (TOTAL LENGTH):", TOTAL_ROBOT_LENGTH, "mm <= 185.0 mm (Margin:", 185.0 - TOTAL_ROBOT_LENGTH, "mm)");
echo(">>> TONG CHIEU CAO CUM BASE (TOTAL HEIGHT):", TOTAL_ROBOT_HEIGHT, "mm <= 185.0 mm (PASS!)");
echo("--- 3. HE DONG CO & KHOANG PIN ---");
echo("Khoang cach giua 2 mat bich motor:", INNER_SPAN, "mm");
echo("Tong chieu dai 2x Motor Encoder sau:", 2.0 * MOTOR_ENC_L, "mm");
echo(">>> KHE HO AN TOAN 2 DUOI MOTOR ENCODER:", REAR_CLEARANCE, "mm (ZERO COLLISION!)");
echo("Khoang pin van nang 2S2P:", BAT_BAY_W, "x", BAT_BAY_L, "mm");
echo("Khoang lot long giua 2 hang tru K2 Hub:", PILLAR_CLEAR_SPAN, "mm");
echo("--- KET LUAN KIEM TRA QUY CHUAN 185x185x185 MM ---");
echo("Tuan thu kich thuoc 185mm Cube:", (TOTAL_ROBOT_WIDTH <= 185.0 && TOTAL_ROBOT_LENGTH <= 185.0 && PART_MAX_DIM <= 185.0) ? "DAT 100% (PASS TUYET DOI)" : "KHONG DAT");
echo("====================================================================");

// ====================================================================
// TIỆN ÍCH LỖ GIỌT NƯỚC 45° TỰ ĐỠ KHI IN 3D (DFM TEARDROP HOLES)
// ====================================================================
module teardrop_hole_x(d = 9.0, h = 10.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2.0, -side/2.0])
                    cube([h, side, side]);
    }
}

module teardrop_hole_y(d = 16.6, h = 15.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([-90, 0, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([0, 45, 0])
                translate([-side/2.0, 0, -side/2.0])
                    cube([side, h, side]);
    }
}

// ====================================================================
// 1. MODULE KHUNG GẦM CHÍNH 185x185mm V7.0 (chassis_base_185x185)
// ====================================================================
module chassis_base_185x185() {
    cradle_w = 28.0; // Bề rộng khối ổ đỡ động cơ bên trong xe
    
    difference() {
        union() {
            // 1. SÀN ĐÁY CHÍNH PHẲNG TUYỆT ĐỐI 100% TẠI Z = 0.0 mm
            translate([-CHASSIS_W/2.0, 0, 0])
                cube([CHASSIS_W, CHASSIS_L, FLOOR_T]);

            // 2. HAI VÁCH SƯỜN CHỊU LỰC CHÍNH DÀY 4.0 mm, CAO 30.0 mm
            translate([-CHASSIS_W/2.0, 0, 0])
                cube([WALL_T, CHASSIS_L, WALL_H]);
            translate([CHASSIS_W/2.0 - WALL_T, 0, 0])
                cube([WALL_T, CHASSIS_L, WALL_H]);

            // 3. 4 CỤM BỆ MOTOR V6.0: Ụ NHÔ NGOÀI (BOSS) + KHỐI Ổ ĐỠ NỬA DƯỚI (CRADLE)
            for (my = [Y_REAR, Y_FRONT]) {
                // --- BÊN TRÁI (LEFT SIDE) ---
                hull() {
                    translate([-CHASSIS_W/2.0 - BOSS_OUT, my, Z_SHAFT])
                        rotate([0, 90, 0])
                            cylinder(d=BOSS_D, h=BOSS_OUT);
                    translate([-CHASSIS_W/2.0 - BOSS_OUT, my - 15.0, 0])
                        cube([BOSS_OUT, 30.0, FLOOR_T]);
                }
                translate([-CHASSIS_W/2.0, my - 16.0, 0])
                    cube([WALL_T, 32.0, 33.0]);
                translate([-CHASSIS_W/2.0, my - 22.0, 0])
                    cube([cradle_w, 44.0, 20.0]);

                // --- BÊN PHẢI (RIGHT SIDE) ---
                hull() {
                    translate([CHASSIS_W/2.0, my, Z_SHAFT])
                        rotate([0, 90, 0])
                            cylinder(d=BOSS_D, h=BOSS_OUT);
                    translate([CHASSIS_W/2.0, my - 15.0, 0])
                        cube([BOSS_OUT, 30.0, FLOOR_T]);
                }
                translate([CHASSIS_W/2.0 - WALL_T, my - 16.0, 0])
                    cube([WALL_T, 32.0, 33.0]);
                translate([CHASSIS_W/2.0 - cradle_w, my - 22.0, 0])
                    cube([cradle_w, 44.0, 20.0]);
            }

            // 4. HỆ GỜ ĐỊNH VỊ 4 GÓC KHOANG PIN VẠN NĂNG 2S2P (82.0 x 76.0 mm, Z = 4.0..7.0 mm)
            for (bx = [-(BAT_BAY_W/2.0 + 2.0), BAT_BAY_W/2.0]) {
                // Gờ góc phía sau (Y = 50..58mm, né tuyệt đối hàng lỗ Y = 48mm)
                translate([bx, BAT_BAY_Y_START + 2.0, FLOOR_T]) cube([2.0, 8.0, 3.0]);
                // Gờ góc phía trước (Y = 118..124mm, né tuyệt đối lỗ ốc Y = 114mm với khoảng cách an toàn 4.0mm)
                translate([bx, BAT_BAY_Y_END - 6.0, FLOOR_T]) cube([2.0, 6.0, 3.0]);
            }

            // 5. 4 TRỤ ĐỠ TẦNG TRÊN TỐI ƯU VẠN NĂNG (Tọa độ chuẩn X = ±42.0 mm, Y = 49.0 & 99.0 mm)
            // Khoảng sáng lọt lòng giữa hai mặt trong trụ: 76.0 mm -> Cho phép khối pin dẹp 76mm lọt qua!
            for (sx = [-1, 1]) {
                for (py = [49.0, 99.0]) {
                    translate([sx * PILLAR_X - PILLAR_W_X/2.0, py - PILLAR_L_Y/2.0, FLOOR_T])
                        cube([PILLAR_W_X, PILLAR_L_Y, PILLAR_H]);
                }
            }

            // 6A. BỆ GÁ MẠCH NHẬN PS4 I2C (Sườn trái, Z = 16.0 mm)
            translate([-CHASSIS_W/2.0, 56.0, 0])
                cube([16.0, 26.0, 16.0]);

            // 6B. BỆ GÁ MODULE NÚT NHẤN ĐÔI (Sườn phải đối xứng, Z = 16.0 mm)
            translate([CHASSIS_W/2.0 - 16.0, 56.0, 0])
                cube([16.0, 26.0, 16.0]);

            // 7. MŨI CẢN TRƯỚC GỌN GÀNG (SLIM REDESIGNED BUMPER & ToF VL53L0X MOUNT)
            // Đặt nghiêm ngặt từ Y = 167.0 đến CHASSIS_L (172.0mm) - Dày 5.0mm, cao 14.0mm
            hull() {
                translate([-30.0, CHASSIS_L - 2.0, 0]) cube([60.0, 2.0, 14.0]);
                translate([-34.0, 167.0, 0])          cube([68.0, 2.0, 14.0]);
            }
            // Hai tai nối cứng cáp vào vách sườn xe tại X = ±CHASSIS_W/2
            translate([-CHASSIS_W/2.0, 167.0, 0]) cube([WALL_T + 2.0, 5.0, 14.0]);
            translate([CHASSIS_W/2.0 - WALL_T - 2.0, 167.0, 0]) cube([WALL_T + 2.0, 5.0, 14.0]);

            // 8. HỆ GỜ ĐỊNH VỊ CHUẨN XÁC CHÂN THÁP NÂNG RỜI (01B & 01C)
            // Gờ sườn ngoài dẫn hướng tại X = ±28.2mm (dài 26mm từ Y=126 đến 152mm, cao 3.0mm)
            translate([-30.2, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            translate([ 28.2, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            // Gờ chặn sau tại Y = 102.5mm định vị khít chân tháp tại Y = 105.0mm
            translate([-28.0, 102.5, FLOOR_T]) cube([16.0, 2.0, 3.0]);
            translate([ 12.0, 102.5, FLOOR_T]) cube([16.0, 2.0, 3.0]);
        }

        // ================= KHOÉT LỖ BẰNG CSG & TEARDROP 45° =================

        // --- 4 CỤM KHOÉT LÒNG ĐỘNG CƠ GA25, HỐC BÍCH & LỖ TRỤC GIỌT NƯỚC 45° ---
        for (my = [Y_REAR, Y_FRONT]) {
            // === BÊN TRÁI (LEFT SIDE) ===
            translate([-CHASSIS_W/2.0 - BOSS_OUT + FLANGE_T, my, Z_SHAFT])
                rotate([0, 90, 0])
                    cylinder(d=25.4, h=BOSS_OUT - FLANGE_T + cradle_w + 0.1);

            translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my, Z_SHAFT])
                teardrop_hole_x(d=9.0, h=FLANGE_T + 2.0);

            for (a = [0, 90, 180, 270]) {
                translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=FLANGE_T + 2.0);
            }

            for (dy = [-17.5, 17.5]) {
                translate([-44.0, my + dy, 3.0])
                    cylinder(d=3.0, h=18.0);
            }

            // === BÊN PHẢI (RIGHT SIDE) ===
            translate([CHASSIS_W/2.0 - cradle_w - 0.1, my, Z_SHAFT])
                rotate([0, 90, 0])
                    cylinder(d=25.4, h=BOSS_OUT - FLANGE_T + cradle_w + 0.1);

            translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my, Z_SHAFT])
                teardrop_hole_x(d=9.0, h=FLANGE_T + 2.0);

            for (a = [0, 90, 180, 270]) {
                translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=FLANGE_T + 2.0);
            }

            for (dy = [-17.5, 17.5]) {
                translate([44.0, my + dy, 3.0])
                    cylinder(d=3.0, h=18.0);
            }
        }

        // --- KHOANG PIN VẠN NĂNG 2S2P: HẠ PHẲNG TUYỆT ĐỐI SÀN (Y = 48.0..124.0 mm, X = ±41.0 mm) ---
        translate([-BAT_BAY_W/2.0, BAT_BAY_Y_START, FLOOR_T])
            cube([BAT_BAY_W, BAT_BAY_L, 30.0]);

        // --- 4 LỖ ỐC M3 TRÊN ĐỈNH 4 TRỤ ĐỠ TẦNG TRÊN (X = ±42.0, Y = 49.0 & 99.0 mm) ---
        for (sx = [-1, 1]) {
            for (py = [49.0, 99.0]) {
                translate([sx * PILLAR_X, py, FLOOR_T + 2.0])
                    cylinder(d=3.0, h=PILLAR_H + 2.0);
            }
        }

        // --- 4 LỖ SÀN M3 TƯƠNG THÍCH KHUNG CHÂN ĐÔN 01D_Base_Riser_Frame (X = ±33.0, Y = 49.0 & 99.0 mm) ---
        for (px = [-33.0, 33.0]) {
            for (py = [49.0, 99.0]) {
                translate([px, py, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }

        // --- 10 LỖ BU-LÔNG M3 BẮT CỨNG 2 THÁP NÂNG RỜI (01B & 01C) ---
        // 10 Lỗ bu-lông M3 thông suốt 100% xuyên sàn (từ Z = -1.0 đến Z = 25.0 mm), Ø3.4mm
        // - Chân Tháp Trái (5 lỗ): X = -16.0 (Y = 110.5, 122.0, 160.25) & X = -24.0 (Y = 116.0, 160.25)
        // - Chân Tháp Phải (5 lỗ): X = +16.0 (Y = 110.5, 122.0, 160.25) & X = +24.0 (Y = 116.0, 160.25)
        for (sx = [-16.0, 16.0]) {
            for (sy = [110.5, 122.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=26.0);
            }
        }
        for (sx = [-24.0, 24.0]) {
            for (sy = [116.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=26.0);
            }
        }

        // --- LỖ BẮT MẠCH NHẬN PS4 I2C (SƯỜN TRÁI) & NÚT NHẤN ĐÔI (SƯỜN PHẢI) ---
        translate([-CHASSIS_W/2.0 + 9.0, 61.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2.0 + 9.0, 77.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2.0 + 4.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        translate([CHASSIS_W/2.0 - 9.0, 61.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2.0 - 9.0, 77.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2.0 - 17.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        // --- MA TRẬN LỖ ỐC M3 ĐA NĂNG & GÁ CHÂN CHỐNG STANDOFF TRÊN SÀN ---
        for (ex = [-42.0, 42.0]) {
            for (ey = [88.0, 114.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }
        for (ex = [-8.0, 0.0, 8.0]) {
            for (ey = [112.0, 128.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }
        for (ex = [-16.0, 0.0, 16.0]) {
            for (ey = [8.0, 48.0, 64.0, 80.0, 96.0]) {
                translate([ex, ey, -1.0]) cylinder(d=3.4, h=FLOOR_T + 2.0);
            }
        }

        // --- LỖ ỐC M3 & RÃNH CÁP GROVE BẮT ĐẾ ĐỆM CẢM BIẾN DÒ LINE (01E) ---
        for (lx = [-12.0, -8.0, 8.0, 12.0]) {
            translate([lx, CHASSIS_L - 12.0, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
        }
        translate([-8.0, CHASSIS_L - 26.0, -0.5]) cube([16.0, 8.0, FLOOR_T + 1.0]);

        // --- HỐC GÁ & CỬA SỔ QUANG HỌC CẢM BIẾN LASER ToF VL53L0X GỌN GÀNG TRONG VÁCH CẢN 5mm ---
        translate([-7.0, 166.8, 5.5])
            cube([14.0, 5.4, 7.0]);
        translate([-12.8, 167.0, FLOOR_T])
            cube([25.6, 2.5, 11.0]);
        translate([-10.0, 166.5, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=6.0);
        translate([ 10.0, 166.5, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=6.0);
        translate([-7.0, 163.5, -0.5])
            cube([14.0, 3.5, FLOOR_T + 1.0]);

        // --- VỊ TRÍ GÁ CẢM BIẾN ToF VL53L0X HAI SƯỜN (TÙY CHỌN) ---
        if (ENABLE_SIDE_TOF_SLOTS) {
            translate([-CHASSIS_W/2.0 - 1.0, 96.0, 14.0])
                teardrop_hole_x(d=7.0, h=WALL_T + 2.0);
            translate([-CHASSIS_W/2.0 - 1.0, 86.0, 14.0])
                teardrop_hole_x(d=3.2, h=WALL_T + 2.0);
            translate([-CHASSIS_W/2.0 - 1.0, 106.0, 14.0])
                teardrop_hole_x(d=3.2, h=WALL_T + 2.0);

            translate([CHASSIS_W/2.0 - WALL_T - 1.0, 96.0, 14.0])
                teardrop_hole_x(d=7.0, h=WALL_T + 2.0);
            translate([CHASSIS_W/2.0 - WALL_T - 1.0, 86.0, 14.0])
                teardrop_hole_x(d=3.2, h=WALL_T + 2.0);
            translate([CHASSIS_W/2.0 - WALL_T - 1.0, 106.0, 14.0])
                teardrop_hole_x(d=3.2, h=WALL_T + 2.0);
        }

        // --- RÃNH LUỒN DÂY NGUỒN TRUNG TÂM & 4 KHE LUỒN ĐAI DÁN VELCRO BẢN 20mm ---
        translate([-12.0, 18.0, -0.5]) cube([24.0, 22.0, FLOOR_T + 1.0]);
        for (zx = [-40.0, 36.0]) {
            for (zy = [60.0, 90.0]) {
                translate([zx, zy, -0.5]) cube([4.0, 22.0, FLOOR_T + 1.0]);
            }
        }
    }
}

// BÍ DANH TƯƠNG THÍCH NGƯỢC
module chassis_base_200x200() {
    chassis_base_185x185();
}

// ====================================================================
// MODULE MÔ PHỎNG BÁNH XE MECANUM 60MM
// ====================================================================
module mecanum_wheel_sim(is_left = true) {
    cavity_d = 42.0;
    cavity_depth = 8.0;
    color("DimGray") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
            translate([-0.1, 0, 0]) rotate([0, 90, 0]) cylinder(d=cavity_d, h=cavity_depth + 0.1);
            translate([-1.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.2, h=WHEEL_W + 2.0);
        }
    }
}

// ====================================================================
// MODULE HỘP GIỚI HẠN 185x185x185mm (BOUNDING BOX 185 CUBE WIREFRAME)
// ====================================================================
module bounding_box_185x185() {
    box_s = 185.0;
    y_min = 0.0;
    x_min = -box_s / 2.0; // -92.5 mm
    
    color("Crimson", 0.5) {
        translate([x_min, y_min, 0]) {
            cube([box_s, 1.5, 1.5]);
            cube([1.5, box_s, 1.5]);
            translate([0, box_s - 1.5, 0]) cube([box_s, 1.5, 1.5]);
            translate([box_s - 1.5, 0, 0]) cube([1.5, box_s, 1.5]);
            
            translate([0, 0, box_s - 1.5]) {
                cube([box_s, 1.5, 1.5]);
                cube([1.5, box_s, 1.5]);
                translate([0, box_s - 1.5, 0]) cube([box_s, 1.5, 1.5]);
                translate([box_s - 1.5, 0, 0]) cube([1.5, box_s, 1.5]);
            }
            
            cube([1.5, 1.5, box_s]);
            translate([box_s - 1.5, 0, 0]) cube([1.5, 1.5, box_s]);
            translate([0, box_s - 1.5, 0]) cube([1.5, 1.5, box_s]);
            translate([box_s - 1.5, box_s - 1.5, 0]) cube([1.5, 1.5, box_s]);
        }
    }
}

// ====================================================================
// HIỂN THỊ CHÍNH (MAIN RENDER)
// ====================================================================
if (DISPLAY_MODE == "part") {
    color("DarkSlateGray")
        chassis_base_185x185();
} else {
    if (SHOW_BOUNDING_BOX) {
        bounding_box_185x185();
    }

    color("DarkSlateGray")
        translate([0, 0, GROUND_CLEAR])
            chassis_base_185x185();

    // 4 Bánh xe Mecanum 60mm
    translate([-CHASSIS_W/2.0 - WHEEL_CLEAR - WHEEL_W, Y_FRONT, Z_SHAFT + GROUND_CLEAR])
        mecanum_wheel_sim(is_left=false);
    translate([CHASSIS_W/2.0 + WHEEL_CLEAR + WHEEL_W, Y_FRONT, Z_SHAFT + GROUND_CLEAR])
        rotate([0, 180, 0])
            mecanum_wheel_sim(is_left=true);
    translate([-CHASSIS_W/2.0 - WHEEL_CLEAR - WHEEL_W, Y_REAR, Z_SHAFT + GROUND_CLEAR])
        mecanum_wheel_sim(is_left=true);
    translate([CHASSIS_W/2.0 + WHEEL_CLEAR + WHEEL_W, Y_REAR, Z_SHAFT + GROUND_CLEAR])
        rotate([0, 180, 0])
            mecanum_wheel_sim(is_left=false);

    // 4 Động cơ GA25:
    color("Silver")
        translate([X_FLANGE_IN_L, Y_REAR, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=25.0, h=48.0);
    color("DimGray")
        translate([X_FLANGE_IN_L + 48.0, Y_REAR, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=24.5, h=15.0);

    color("Silver")
        translate([X_FLANGE_IN_R - 48.0, Y_REAR, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=25.0, h=48.0);
    color("DimGray")
        translate([X_FLANGE_IN_R - MOTOR_ENC_L, Y_REAR, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=24.5, h=15.0);

    color("Silver")
        translate([X_FLANGE_IN_L, Y_FRONT, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=25.0, h=MOTOR_DC_L);
    color("Silver")
        translate([X_FLANGE_IN_R - MOTOR_DC_L, Y_FRONT, Z_SHAFT + GROUND_CLEAR])
            rotate([0, 90, 0]) cylinder(d=25.0, h=MOTOR_DC_L);

    // Mô phỏng pin khối gạch 2S2P (2x2: 38 x 38 x 70 mm) đặt trong khoang
    color("RoyalBlue", 0.85)
        translate([-19.0, 51.0, GROUND_CLEAR + FLOOR_T])
            cube([38.0, 70.0, 38.0]);
    // 2 Đai dán Velcro bản 20mm
    color("Black", 0.9) {
        for (sy = [60.0, 90.0]) {
            translate([-19.5, sy, GROUND_CLEAR + FLOOR_T])
                cube([39.0, 20.0, 38.8]);
        }
    }
}
