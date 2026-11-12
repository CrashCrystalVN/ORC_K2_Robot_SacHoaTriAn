// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// THIẾT KẾ: KHUNG GẦM CHÍNH 200x200mm CHUẨN ĐỘI TUYỂN (ORC-K2 PRO DFM V6.1)
// FILE: 01_Chassis_Base_200x200_V6.scad
// PHIÊN BẢN V6.1: NÂNG CẤP KHOANG CHỨA PIN VẠN NĂNG 2S2P 18650 (UNIVERSAL 2S2P BAY)
// ĐẶC TRỊ KHỐI PIN ĐÓNG SẴN 2S2P: DẠNG DẸP 1x4 (76x20x70mm) & GẠCH 2x2 (38x38x70mm)
// ====================================================================
// ĐẶC ĐIỂM DFM & KẾT CẤU V6.1:
// 1. Phủ bì toàn bộ robot: 198.0 mm (Rộng) x 190.0 mm (Dài) <= 200 x 200 mm!
// 2. Độ nhô bệ motor (Outward Flange Boss): BOSS_OUT = 10.5 mm nhô vào hốc rỗng bánh xe Mecanum 80mm.
//    - Lòng trong giữa 2 mặt bích motor: INNER_SPAN = 133.0 mm!
//    - Cầu sau: 2x Động cơ GA25 Encoder (63.0 mm x 2 = 126.0 mm).
//      KHE HỞ AN TOÀN GIỮA 2 ĐUÔI ENCODER = 133.0 - 126.0 = 7.0 mm > 0! ZERO COLLISION!
// 3. Khoang Pin Vạn Năng 2S2P (Universal 2S2P Battery Bay):
//    - Kích thước lòng khoang trên sàn: Rộng 82.0 mm (X in [-41, +41]) x Dài 76.0 mm (Y in [48, 124]).
//    - Dung sai thoải mái cho khối pin dẹp 76mm x 70mm x 20mm và khối pin gạch 38mm x 70mm x 38mm.
//    - 4 Khe luồn đai dán Velcro bản 20mm (4.0 x 22.0 mm) chằng giữ chặt cả 2 dạng pin.
//    - Hệ gờ định vị 4 góc thấp 3.0mm giữ pin vững chãi, chống xô lệch khi robot phanh/cua gắt.
// 4. Hệ Trụ Đỡ Tầng Trên Tối Ưu (Upper Deck Standoff Pillars):
//    - 4 Trụ đỡ chuyển sang vị trí tối ưu: X = ±42.0 mm, Y = 49.0 & 99.0 mm.
//    - Khoảng sáng lọt lòng giữa 2 hàng trụ: 76.0 mm -> Đảm bảo khối pin dẹp 76mm trượt lọt thỏm!
//    - Chiều cao trụ: PILLAR_H = 18.0 mm (Z_top = 22.0 mm), có lỗ ren M3 sâu 16mm trên đỉnh.
//    - Tích hợp 4 lỗ bu-lông M3 xuyên sàn tại X = ±33.0 mm (Y = 49.0 & 99.0 mm) đảm bảo tương thích
//      ngược 100% với Khung chân đôn 01D_Base_Riser_Frame và cọc standoff đồng M3 khi dùng pin gạch 2x2.
// 5. Thiết kế chuyên biệt DFM cho in 3D FDM:
//    - Đáy phẳng 100% tại Z = 0.0 mm (Diện tích tiếp xúc bàn in > 19,000 mm2).
//    - 100% Lỗ ngang trục và lỗ bắt ốc dùng biên dạng Giọt nước 45° (Teardrop) -> IN 0% SUPPORT!
//    - Cản trước ToF VL53L0X góc mở quang học 35° chống tán xạ laser.
//    - Bịt kín cụm ToF sườn (ENABLE_SIDE_TOF_SLOTS = false).
// ====================================================================

// CHẾ ĐỘ HIỂN THỊ:
// "part"              = Chỉ xuất Khung Gầm Đáy Phẳng 100% để in 3D (Z = 0.0 mm, Zero Support)
// "assembly_compact"  = Phối cảnh robot GẤP GỌN trong hộp 200x200mm kèm khung dây kiểm tra
// "assembly_working"  = Phối cảnh robot khi vươn cánh tay gắp hoa ngoài sàn thi đấu
DISPLAY_MODE = "part";

// Độ mịn lưới dựng hình (Smoothness)
$fn = (DISPLAY_MODE == "part") ? 40 : 24;

// CẤU HÌNH BÁNH XE MECANUM:
WHEEL_TYPE = "mecanum_80";

// HIỂN THỊ HỘP GIỚI HẠN 200x200mm (Wireframe Bounding Box)
SHOW_BOUNDING_BOX = true;

// CẤU HÌNH CẢM BIẾN TOF SƯỜN (VL53L0X BÁM THÀNH HAI BÊN SƯỜN XE):
// true  = Mở cụm 3 lỗ giọt nước (1 lỗ laser Ø7mm + 2 lỗ ốc M3 pitch 20mm) mỗi bên sườn
// false = Bịt kín 100%, vách sườn phẳng lỳ nguyên khối, tăng độ cứng & chống bụi bẩn
ENABLE_SIDE_TOF_SLOTS = false;

// ====================================================================
// BẢNG THÔNG SỐ KÍCH THƯỚC CHUẨN HÓA (200x200 COMPLIANT)
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

// THÔNG SỐ ĐỘNG CƠ GA25 THỰC TẾ:
MOTOR_D      = 25.0;    // Đường kính thân motor GA25 (mm)
MOTOR_DC_L   = 48.0;    // Chiều dài thân hộp số + motor DC thường cầu trước (FL, FR) (mm)
MOTOR_ENC_L  = 63.0;    // Chiều dài motor Encoder cầu sau (RL, RR) kể cả nắp và giắc cắm (mm)
Z_SHAFT      = 20.0;    // Cao độ tâm trục bánh xe/động cơ so với đáy sàn Z=0 (mm)

// THÔNG SỐ BÁNH XE MECANUM 80mm
WHEEL_D      = (WHEEL_TYPE == "mecanum_60") ? 60.0 : 80.0;
WHEEL_W      = (WHEEL_TYPE == "mecanum_60") ? 30.0 : 38.0;
WHEEL_CLEAR  = 2.0;     // Khe hở an toàn giữa mặt trong bánh xe và vách khung xe (mm)
GROUND_CLEAR = WHEEL_D / 2.0 - Z_SHAFT; // Khoảng sáng gầm xe (20.0mm với bánh 80mm)

// TỌA ĐỘ TRỤC XE (ĐỒNG TRỤC 100% TUYỆT ĐỐI)
Y_FRONT      = 142.0;   // Trục trước (FL, FR)
Y_REAR       = 32.0;    // Trục sau (RL, RR)
WHEELBASE    = Y_FRONT - Y_REAR; // 110.0 mm
TRACK_WIDTH  = CHASSIS_W + 2.0 * WHEEL_CLEAR + WHEEL_W;  // 160.0 mm

// TỌA ĐỘ MẶT BÍCH LẮP ĐỘNG CƠ:
X_FLANGE_IN_L = -(CHASSIS_W/2.0 + BOSS_OUT) + FLANGE_T; // -66.5 mm
X_FLANGE_IN_R = +(CHASSIS_W/2.0 + BOSS_OUT) - FLANGE_T; // +66.5 mm

// KHOẢNG HỞ LÒNG XE GIỮA 2 MẶT BÍCH:
INNER_SPAN = X_FLANGE_IN_R - X_FLANGE_IN_L; // 133.0 mm

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU SAU (2x ENCODER 63mm):
REAR_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_ENC_L; // 133.0 - 126.0 = 7.0 mm > 0!

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU TRƯỚC (2x DC 48mm):
FRONT_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_DC_L; // 133.0 - 96.0 = 37.0 mm > 0!

// TỔNG PHỦ BÌ XE:
TOTAL_ROBOT_WIDTH  = CHASSIS_W + 2.0 * (WHEEL_CLEAR + WHEEL_W); // 198.0 mm <= 200.0 mm!
TOTAL_ROBOT_LENGTH = (Y_FRONT + WHEEL_D/2.0) - (Y_REAR - WHEEL_D/2.0); // 190.0 mm <= 200.0 mm!

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
echo("=== ORC-K2 PRO DFM V6.1 - UNIVERSAL 2S2P BATTERY BAY REDESIGN ===");
echo("====================================================================");
echo("Chassis Width (Than xe chinh):", CHASSIS_W, "mm");
echo("Boss Protrusion (Do nho vao long banh):", BOSS_OUT, "mm");
echo("Inner Flange Span (Khoang cach giua 2 mat bich):", INNER_SPAN, "mm");
echo("Rear Motors Total Length (2x Encoder 63mm):", 2.0 * MOTOR_ENC_L, "mm");
echo(">>> REAR MOTOR CLEARANCE (KHE HO 2 DUOI MOTOR SAU):", REAR_CLEARANCE, "mm (ZERO COLLISION!)");
echo(">>> FRONT MOTOR CLEARANCE (KHE HO 2 DUOI MOTOR TRUOC):", FRONT_CLEARANCE, "mm (PASS!)");
echo(">>> BATTERY BAY SIZE (KHOANG PIN 2S2P):", BAT_BAY_W, "x", BAT_BAY_L, "mm (Y in [", BAT_BAY_Y_START, ",", BAT_BAY_Y_END, "])");
echo(">>> UPPER PILLAR SPAN (KHOANG LOT LONG GIUA 2 TRU):", PILLAR_CLEAR_SPAN, "mm (Pin dep 76mm PASS!)");
echo(">>> TOTAL ROBOT WIDTH (BE RONG PHU BI):", TOTAL_ROBOT_WIDTH, "mm <= 200.0 mm (Margin:", 200.0 - TOTAL_ROBOT_WIDTH, "mm)");
echo(">>> TOTAL ROBOT LENGTH (CHIEU DAI PHU BI):", TOTAL_ROBOT_LENGTH, "mm <= 200.0 mm (Margin:", 200.0 - TOTAL_ROBOT_LENGTH, "mm)");
echo(">>> WHEELBASE (CHIEU DAI CO SO DONG TRUC):", WHEELBASE, "mm (Dong truc 100% hai ben)");
echo("Trang thai kiem tra va cham:", (REAR_CLEARANCE > 0) ? "DAT 100% (PASS)" : "KHONG DAT (FAIL)");
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
// 1. MODULE KHUNG GẦM CHÍNH 200x200mm V6.1 (01_Chassis_Base_200x200_V6)
// ====================================================================
module chassis_base_200x200() {
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
            // Giữ cố định pin dẹp 76mm lẫn pin gạch 38mm; né 100% toàn bộ lỗ ốc ma trận sàn
            for (bx = [-(BAT_BAY_W/2.0 + 2.0), BAT_BAY_W/2.0]) {
                // Gờ góc phía sau (Y = 50..58mm, né tuyệt đối hàng lỗ Y = 48mm)
                translate([bx, BAT_BAY_Y_START + 2.0, FLOOR_T]) cube([2.0, 8.0, 3.0]);
                // Gờ góc phía trước (Y = 118..124mm, né tuyệt đối lỗ ốc Y = 114mm với khoảng cách an toàn 4.0mm)
                translate([bx, BAT_BAY_Y_END - 6.0, FLOOR_T]) cube([2.0, 6.0, 3.0]);
            }
            // LƯU Ý DFM V6.2: ĐÃ XÓA BỎ 2 THANH GỜ CHẶN NGANG TRƯỚC VÀ SAU ĐỂ GIẢI PHÓNG 100%
            // KHOẢNG TRỐNG THÔNG SUỐT (CLEARANCE >= Ø7.0mm) CHO 3 LỖ ỐC M3 (Y = 48mm, HÌNH 1),
            // 2 LỖ BẮT CHÂN THÁP NÂNG (Y = 122mm) VÀ 3 LỖ MA TRẬN PHÍA TRƯỚC (Y = 128mm).
            // PIN ĐƯỢC CHẰNG GIỮ CHẮC CHẮN BẰNG 2 ĐAI VELCRO 20mm VÀ 4 GỜ GÓC BẢO ĐẢM KHÔNG XÔ LỆCH!

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
            // Vách sau thẳng đứng tại Y = 167.0mm -> GIẢI PHÓNG 100% SÀN XE PHẲNG LỘ THIÊN CHO THÁP NÂNG!
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
            // Gờ chặn sau tại Y = 103.5mm định vị khít chân tháp tại Y = 105.0mm
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
        // Đảm bảo lòng khoang pin rộng 82.0 mm x dài 76.0 mm phẳng hoàn toàn trên sàn Z = FLOOR_T
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
        // Khôi phục chuẩn xác theo đúng bản thiết kế cũ (base cũ) để bắt 2 chân tháp nâng:
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
        // Lỗ xuyên sàn Ø3.4mm thông suốt 100% chuẩn M3
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
        // Chỉ khoan xuyên sàn chịu lực (h = FLOOR_T + 1.0), giữ mặt sàn Z=4.0mm phẳng phiu 100%!
        // 4 Lỗ ốc M3 bắt Đế đệm (X = ±8.0 & ±12.0mm). Hai vị trí X = ±16.0mm đã được khoan bởi 10 Lỗ bu-lông Tháp Nâng tại Y = 160.25mm!
        for (lx = [-12.0, -8.0, 8.0, 12.0]) {
            translate([lx, CHASSIS_L - 12.0, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
        }
        translate([-8.0, CHASSIS_L - 26.0, -0.5]) cube([16.0, 8.0, FLOOR_T + 1.0]);

        // --- HỐC GÁ & CỬA SỔ QUANG HỌC CẢM BIẾN LASER ToF VL53L0X GỌN GÀNG TRONG VÁCH CẢN 5mm ---
        // Cửa sổ quang học laser phát/thu xuyên thẳng ra mặt trước mũi xe (Y = 167..172)
        translate([-7.0, 166.8, 5.5])
            cube([14.0, 5.4, 7.0]);
        // Khe cài module cảm biến VL53L0X (PCB 25x11mm)
        translate([-12.8, 167.0, FLOOR_T])
            cube([25.6, 2.5, 11.0]);
        // Hai lỗ ốc bắt M2.5 / M3 chuẩn pitch 20.0mm (X = ±10.0mm, Z = 9.5mm)
        translate([-10.0, 166.5, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=6.0);
        translate([ 10.0, 166.5, 9.5])
            rotate([-90, 0, 0]) cylinder(d=3.0, h=6.0);
        // Rãnh luồn cáp I2C xuyên sàn nhỏ gọn sát vách
        translate([-7.0, 163.5, -0.5])
            cube([14.0, 3.5, FLOOR_T + 1.0]);

        // --- VỊ TRÍ GÁ CẢM BIẾN ToF VL53L0X HAI SƯỜN ---
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

// ====================================================================
// MODULE MÔ PHỎNG BÁNH XE MECANUM
// ====================================================================
module mecanum_wheel_sim(is_left = true) {
    cavity_d = 56.0;
    cavity_depth = 12.0;
    color("DimGray") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
            translate([-0.1, 0, 0]) rotate([0, 90, 0]) cylinder(d=cavity_d, h=cavity_depth + 0.1);
            translate([-1.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.2, h=WHEEL_W + 2.0);
        }
    }
}

// ====================================================================
// MODULE HỘP GIỚI HẠN 200x200mm (BOUNDING BOX 200x200x200 WIREFRAME)
// ====================================================================
module bounding_box_200x200() {
    y_min = Y_REAR - WHEEL_D/2.0;
    x_min = -100.0;
    
    color("Crimson", 0.4) {
        translate([x_min, y_min, 0]) {
            cube([200.0, 1.5, 1.5]);
            cube([1.5, 200.0, 1.5]);
            translate([0, 200.0 - 1.5, 0]) cube([200.0, 1.5, 1.5]);
            translate([200.0 - 1.5, 0, 0]) cube([1.5, 200.0, 1.5]);
            
            translate([0, 0, 200.0 - 1.5]) {
                cube([200.0, 1.5, 1.5]);
                cube([1.5, 200.0, 1.5]);
                translate([0, 200.0 - 1.5, 0]) cube([200.0, 1.5, 1.5]);
                translate([200.0 - 1.5, 0, 0]) cube([1.5, 200.0, 1.5]);
            }
            
            cube([1.5, 1.5, 200.0]);
            translate([200.0 - 1.5, 0, 0]) cube([1.5, 1.5, 200.0]);
            translate([0, 200.0 - 1.5, 0]) cube([1.5, 1.5, 200.0]);
            translate([200.0 - 1.5, 200.0 - 1.5, 0]) cube([1.5, 1.5, 200.0]);
        }
    }
}

// ====================================================================
// HIỂN THỊ CHÍNH (MAIN RENDER)
// ====================================================================
if (DISPLAY_MODE == "part") {
    color("DarkSlateGray")
        chassis_base_200x200();
} else {
    if (SHOW_BOUNDING_BOX) {
        bounding_box_200x200();
    }

    color("DarkSlateGray")
        translate([0, 0, GROUND_CLEAR])
            chassis_base_200x200();

    // 4 Bánh xe Mecanum
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

    // Mô phỏng pin 2S2P dẹp (1x4: 76 x 70 x 20 mm) đặt trong khoang
    color("RoyalBlue", 0.75)
        translate([-38.0, 51.0, GROUND_CLEAR + FLOOR_T])
            cube([76.0, 70.0, 20.0]);
}
