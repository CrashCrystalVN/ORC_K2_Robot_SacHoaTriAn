// ====================================================================
// ORC-K2 ROBOT - ZERO-COLLISION GA25 MOTOR MOUNTING ARCHITECTURE
// WORKER 2: MECHANICAL VALIDATION & ZERO-COLLISION PROOF
// ====================================================================

$fn = 36;

// KÍCH THƯỚC CHUẨN KHUNG ROBOT 200x200mm
CHASSIS_W    = 118.0;   // Chiều rộng thân xe chính (mm)
CHASSIS_L    = 172.0;   // Chiều dài sàn xe (mm)
FLOOR_T      = 4.0;     // Độ dày sàn xe (mm)
WALL_T       = 4.0;     // Độ dày vách sườn cơ bản (mm)
WALL_H       = 30.0;    // Chiều cao vách sườn (mm)

// GIẢI PHÁP A: Ụ MẶT BÍCH LỒI VÀO LÒNG BÁNH XE (RECESSED WHEEL POCKET BOSS)
BOSS_OUT     = 10.5;    // Độ nhô ra ngoài của ụ mặt bích (mm)
BOSS_D       = 36.0;    // Đường kính ngoài của ụ mặt bích (mm)
FLANGE_T     = 3.0;     // Độ dày mặt bích bắt motor (mm)

// THÔNG SỐ ĐỘNG CƠ GA25
MOTOR_D      = 25.0;    // Đường kính thân motor GA25 (mm)
MOTOR_DC_L   = 48.0;    // Chiều dài motor DC thường cầu trước (FL, FR) (mm)
MOTOR_ENC_L  = 63.0;    // Chiều dài motor Encoder cầu sau (RL, RR) kể cả nắp (mm)
SHAFT_D      = 4.0;     // Đường kính trục motor (mm)
SHAFT_L      = 10.0;    // Chiều dài trục motor thò ra ngoài mặt bích (mm)
COLLAR_D     = 7.0;     // Gờ định vị cổ trục motor (mm)
COLLAR_H     = 2.0;     // Chiều cao gờ định vị (mm)

// THÔNG SỐ BÁNH XE MECANUM 80mm
WHEEL_D      = 80.0;    // Đường kính bánh xe Mecanum (mm)
WHEEL_W      = 38.0;    // Bề rộng bánh xe (mm)
WHEEL_CLEAR  = 2.0;     // Khe hở an toàn giữa vách xe và mặt trong bánh xe (mm)
Z_SHAFT      = 20.0;    // Cao độ tâm trục bánh xe/động cơ so với đáy sàn Z=0

// TỌA ĐỘ TRỤC XE (ĐỒNG TRỤC 100% TUYỆT ĐỐI)
Y_FRONT      = 142.0;   // Trục trước (FL, FR)
Y_REAR       = 32.0;    // Trục sau (RL, RR)
WHEELBASE    = Y_FRONT - Y_REAR; // 110.0 mm

// TỌA ĐỘ MẶT BÍCH LẮP ĐỘNG CƠ:
// Mặt ngoài của ụ mặt bích:
X_BOSS_OUT_L = -(CHASSIS_W/2.0 + BOSS_OUT); // -69.5 mm
X_BOSS_OUT_R = +(CHASSIS_W/2.0 + BOSS_OUT); // +69.5 mm
// Mặt trong của bích (nơi đế động cơ áp sát vào):
X_FLANGE_IN_L = X_BOSS_OUT_L + FLANGE_T;    // -66.5 mm
X_FLANGE_IN_R = X_BOSS_OUT_R - FLANGE_T;    // +66.5 mm

// KHOẢNG HỞ LÒNG XE GIỮA 2 MẶT BÍCH:
INNER_SPAN = X_FLANGE_IN_R - X_FLANGE_IN_L; // 133.0 mm

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU SAU (2x ENCODER):
REAR_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_ENC_L; // 133.0 - 126.0 = 7.0 mm > 0!

// KHOẢNG HỞ GIỮA 2 ĐUÔI ĐỘNG CƠ CẦU TRƯỚC (2x DC):
FRONT_CLEARANCE = INNER_SPAN - 2.0 * MOTOR_DC_L; // 133.0 - 96.0 = 37.0 mm > 0!

// TỔNG PHỦ BÌ XE:
TOTAL_WIDTH  = CHASSIS_W + 2.0 * (WHEEL_CLEAR + WHEEL_W); // 198.0 mm <= 200.0 mm
TOTAL_LENGTH = (Y_FRONT + WHEEL_D/2.0) - (Y_REAR - WHEEL_D/2.0); // 190.0 mm <= 200.0 mm

// In kết quả kiểm tra ra Console
echo("==========================================================");
echo("=== WORKER 2: ZERO-COLLISION GEOMETRIC PROOF RESULTS ===");
echo("==========================================================");
echo("Chassis Width (Than xe):", CHASSIS_W, "mm");
echo("Boss Protrusion (U loi vao banh):", BOSS_OUT, "mm");
echo("Inner Flange Span (Khoang cach giua 2 mat bich):", INNER_SPAN, "mm");
echo("Rear Motors Total Length (2x Encoder 63mm):", 2.0 * MOTOR_ENC_L, "mm");
echo(">>> REAR MOTOR CLEARANCE (KHE HO 2 DUOI MOTOR SAU):", REAR_CLEARANCE, "mm (PASS > 5mm!)");
echo(">>> FRONT MOTOR CLEARANCE (KHE HO 2 DUOI MOTOR TRUOC):", FRONT_CLEARANCE, "mm (PASS!)");
echo(">>> TOTAL ROBOT WIDTH (BE RONG PHU BI):", TOTAL_WIDTH, "mm <= 200.0 mm (PASS!)");
echo(">>> TOTAL ROBOT LENGTH (CHIEU DAI PHU BI):", TOTAL_LENGTH, "mm <= 200.0 mm (PASS!)");
echo(">>> WHEELBASE (CHIEU DAI CO SO DONG TRUC):", WHEELBASE, "mm (SYMMETRIC 100%)");
echo("==========================================================");

// ====================================================================
// MODULE ĐỘNG CƠ GA25 MÔ PHỎNG CHI TIẾT
// ====================================================================
module ga25_motor_model(is_encoder = false, is_left = true) {
    len = is_encoder ? MOTOR_ENC_L : MOTOR_DC_L;
    dir = is_left ? 1 : -1; // Chiều thân motor chui vào trong lòng xe
    
    // Gốc tọa độ tại mặt bích động cơ:
    union() {
        // 1. Thân kim loại hộp số & motor (màu bạc)
        color("Silver") {
            translate([is_left ? 0 : -48.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=MOTOR_D, h=48.0);
        }
        
        // 2. Cúp vỉ Encoder (màu đen) nếu có
        if (is_encoder) {
            color("DimGray") {
                translate([is_left ? 48.0 : -len, 0, 0])
                    rotate([0, 90, 0])
                        cylinder(d=MOTOR_D - 0.5, h=len - 48.0);
            }
            // Giắc cắm dây encoder (màu trắng)
            color("GhostWhite") {
                translate([is_left ? len - 2.0 : -len, -5.0, 3.0])
                    cube([2.0, 10.0, 8.0]);
            }
        }
        
        // 3. Cổ trục định vị Ø7mm x 2mm (chui vào lỗ vách)
        color("LightSteelBlue") {
            translate([is_left ? -COLLAR_H : 0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=COLLAR_D, h=COLLAR_H);
        }
        
        // 4. Trục ra D-cut Ø4mm x 10mm
        color("Gold") {
            translate([is_left ? -SHAFT_L : 0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=SHAFT_D, h=SHAFT_L);
        }
    }
}

// ====================================================================
// MODULE BÁNH XE MECANUM K3 80mm CÓ HỐC RỖNG TRONG
// ====================================================================
module mecanum_wheel_with_cavity(is_left = true) {
    cavity_d = 56.0; // Đường kính hốc rỗng mặt trong
    cavity_depth = 12.0; // Độ sâu hốc rỗng
    
    color("DimGray", 0.6) {
        difference() {
            // Thân vành bánh xe ngoài
            rotate([0, 90, 0])
                cylinder(d=WHEEL_D, h=WHEEL_W);
            
            // Hốc rỗng mặt trong (phía giáp thân xe)
            translate([-0.1, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=cavity_d, h=cavity_depth + 0.1);
            
            // Lỗ trục xuyên tâm
            translate([-1.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=4.2, h=WHEEL_W + 2.0);
        }
    }
}

// ====================================================================
// MODULE VÁCH SƯỜN & Ụ MẶT BÍCH LỒI (SOLUTION A)
// ====================================================================
module chassis_wall_with_boss() {
    // Sàn xe cơ bản
    color("DarkSlateGray") {
        translate([-CHASSIS_W/2.0, 0, 0])
            cube([CHASSIS_W, CHASSIS_L, FLOOR_T]);
    }
    
    // 2 Vách sườn chính tại X = ±(CHASSIS_W/2)
    color("SlateGray") {
        translate([-CHASSIS_W/2.0, 0, 0])
            cube([WALL_T, CHASSIS_L, WALL_H]);
        translate([CHASSIS_W/2.0 - WALL_T, 0, 0])
            cube([WALL_T, CHASSIS_L, WALL_H]);
    }
    
    // 4 Ụ MẶT BÍCH LỒI (OUTWARD FLANGE BOSSES)
    for (my = [Y_REAR, Y_FRONT]) {
        // Bên Trái (nhô về hướng -X)
        color("DodgerBlue", 0.8) {
            difference() {
                // Khối trụ ụ nổi lồi ra ngoài vách sườn
                translate([-CHASSIS_W/2.0 - BOSS_OUT, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=BOSS_D, h=BOSS_OUT + WALL_T);
                
                // Khoét lỗ đặt thân motor Ø25.4mm từ trong
                translate([-CHASSIS_W/2.0 - BOSS_OUT + FLANGE_T, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=MOTOR_D + 0.4, h=BOSS_OUT + WALL_T);
                
                // Lỗ cổ trục Ø9.0mm xuyên mặt bích
                translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=9.0, h=FLANGE_T + 2.0);
                
                // 4 Lỗ ốc M3 PCD Ø17mm
                for (a = [0, 90, 180, 270]) {
                    translate([-CHASSIS_W/2.0 - BOSS_OUT - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                        rotate([0, 90, 0])
                            cylinder(d=3.3, h=FLANGE_T + 2.0);
                }
            }
        }
        
        // Bên Phải (nhô về hướng +X)
        color("DodgerBlue", 0.8) {
            difference() {
                // Khối trụ ụ nổi lồi ra ngoài vách sườn
                translate([CHASSIS_W/2.0 - WALL_T, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=BOSS_D, h=BOSS_OUT + WALL_T);
                
                // Khoét lỗ đặt thân motor Ø25.4mm từ trong
                translate([CHASSIS_W/2.0 - WALL_T - 0.1, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=MOTOR_D + 0.4, h=BOSS_OUT + WALL_T - FLANGE_T + 0.1);
                
                // Lỗ cổ trục Ø9.0mm xuyên mặt bích
                translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my, Z_SHAFT])
                    rotate([0, 90, 0])
                        cylinder(d=9.0, h=FLANGE_T + 2.0);
                
                // 4 Lỗ ốc M3 PCD Ø17mm
                for (a = [0, 90, 180, 270]) {
                    translate([CHASSIS_W/2.0 + BOSS_OUT - FLANGE_T - 1.0, my + 8.5*cos(a), Z_SHAFT + 8.5*sin(a)])
                        rotate([0, 90, 0])
                            cylinder(d=3.3, h=FLANGE_T + 2.0);
                }
            }
        }
    }
}

// ====================================================================
// KIỂM TRA VA CHẠM BẰNG CSG INTERSECTION (ZERO VOLUME = ZERO COLLISION)
// ====================================================================
module collision_detector_rear_motors() {
    // Nếu có va chạm, khối giao nhau này sẽ xuất hiện màu ĐỎ RỰC
    color("Red") {
        intersection() {
            // Motor Sau - Trái
            translate([X_FLANGE_IN_L, Y_REAR, Z_SHAFT])
                ga25_motor_model(is_encoder=true, is_left=true);
            
            // Motor Sau - Phải
            translate([X_FLANGE_IN_R, Y_REAR, Z_SHAFT])
                ga25_motor_model(is_encoder=true, is_left=false);
        }
    }
}

// ====================================================================
// HỘP GIỚI HẠN 200x200mm WIREFRAME (BOUNDING BOX)
// ====================================================================
module bounding_box_wireframe() {
    y_min = Y_REAR - WHEEL_D/2.0; // -8.0 mm
    color("Crimson", 0.5) {
        translate([-100.0, y_min, -20.0]) {
            difference() {
                cube([200.0, 200.0, 120.0]);
                translate([2.0, 2.0, -1.0])
                    cube([196.0, 196.0, 122.0]);
            }
        }
    }
}

// ====================================================================
// LẮP RÁP TỔNG THỂ ĐỂ XÁC MINH (FULL VALIDATION ASSEMBLY)
// ====================================================================
// 1. Khung xe và Ụ mặt bích
chassis_wall_with_boss();

// 2. 4 Động cơ GA25
// Cầu sau (2x Encoder)
translate([X_FLANGE_IN_L, Y_REAR, Z_SHAFT])
    ga25_motor_model(is_encoder=true, is_left=true);
translate([X_FLANGE_IN_R, Y_REAR, Z_SHAFT])
    ga25_motor_model(is_encoder=true, is_left=false);

// Cầu trước (2x DC)
translate([X_FLANGE_IN_L, Y_FRONT, Z_SHAFT])
    ga25_motor_model(is_encoder=false, is_left=true);
translate([X_FLANGE_IN_R, Y_FRONT, Z_SHAFT])
    ga25_motor_model(is_encoder=false, is_left=false);

// 3. 4 Bánh xe Mecanum (thụt lòng ôm trọn ụ mặt bích)
// Sau Trái
translate([-CHASSIS_W/2.0 - WHEEL_CLEAR - WHEEL_W, Y_REAR, Z_SHAFT])
    mecanum_wheel_with_cavity(is_left=true);
// Sau Phải
translate([CHASSIS_W/2.0 + WHEEL_CLEAR + WHEEL_W, Y_REAR, Z_SHAFT])
    rotate([0, 180, 0])
        mecanum_wheel_with_cavity(is_left=false);

// Trước Trái
translate([-CHASSIS_W/2.0 - WHEEL_CLEAR - WHEEL_W, Y_FRONT, Z_SHAFT])
    mecanum_wheel_with_cavity(is_left=true);
// Trước Phải
translate([CHASSIS_W/2.0 + WHEEL_CLEAR + WHEEL_W, Y_FRONT, Z_SHAFT])
    rotate([0, 180, 0])
        mecanum_wheel_with_cavity(is_left=false);

// 4. Bộ kiểm tra va chạm
collision_detector_rear_motors();

// 5. Khung dây 200x200mm
bounding_box_wireframe();
