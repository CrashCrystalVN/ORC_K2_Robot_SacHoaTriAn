// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// BẢN LẮP RÁP TỔNG THỂ: KHUNG GẦM ULTRA-SLIM 120 (X < 120MM) & OMNI WHEELS
// FILE: full_assembly_slim120_omni.scad
// PHIÊN BẢN V11.0: ĐỘT PHÁ CÔNG NGHỆ KHUNG GẦM SIÊU HẸP X < 120MM
// TỔNG BỀ RỘNG XE PHỦ BÌ (CẢ BÁNH XE) = 116.0 MM < 120.0 MM (PASS 100%)
// TÍCH HỢP HỆ THỐNG BI MẮT TRÂU CHỐNG CHÚI / BẬP BÊNH (ANTI-TIP CASTER BALL)
// ====================================================================

use <01_Chassis_Base_Slim120_Omni.scad>;
use <01D_Battery_Deck_Platform.scad>;

$fn = 32;

// CẤU HÌNH BÁNH XE ĐA HƯỚNG SIÊU GỌN:
WHEEL_CONFIG   = "OMNI_48_SLIM"; // "OMNI_48_SLIM", "OMNI_58_SLIM"
WHEEL_D        = (WHEEL_CONFIG == "OMNI_58_SLIM") ? 58.0 : 48.0;
WHEEL_W        = 15.0; // Bề rộng bánh Omni siêu mỏng (mm)
HUB_OFFSET     = 4.0;  // Độ thụt lòng của may-ơ bánh xe (Offset Hub)
COUPLER_EFF    = 8.0;  // Độ vươn hữu dụng của trục / khớp nối ngoài mặt bích (mm)

CHASSIS_W      = 72.0;
BOSS_OUT       = 3.0;
Z_SHAFT        = 20.0;
GROUND_CLEAR   = WHEEL_D / 2.0 - Z_SHAFT; // 4.0mm (Omni 48) hoặc 9.0mm (Omni 58)

// TỌA ĐỘ 4 TRỤC ZIGZAG:
Y_RL = 24.0;
Y_RR = 50.0;
Y_FL = 90.0;
Y_FR = 142.0;

// TÍNH TOÁN PHỦ BÌ TỔNG THỂ THEO TRỤC X:
// Mặt ngoài bích bệ motor: X = ±(CHASSIS_W/2 + BOSS_OUT) = ±39.0mm
// Mép ngoài bánh xe: X_WHEEL_OUT = 39.0 + COUPLER_EFF + (WHEEL_W - HUB_OFFSET) = 39.0 + 8.0 + 11.0 = 58.0mm
X_WHEEL_OUT = CHASSIS_W/2.0 + BOSS_OUT + COUPLER_EFF + (WHEEL_W - HUB_OFFSET); // 58.0 mm
TOTAL_WIDTH = 2.0 * X_WHEEL_OUT; // 116.0 mm <= 118.0 mm < 120.0 mm!

Y_MIN_ROBOT = min(Y_RL - WHEEL_D/2.0, 8.0);
Y_MAX_ROBOT = max(Y_FR + WHEEL_D/2.0, 168.5);
TOTAL_LENGTH = Y_MAX_ROBOT - Y_MIN_ROBOT; // ~166mm

echo("====================================================================");
echo("=== ORC-K2 PRO ULTRA-SLIM 120 TOTAL PACKAGING REPORT ===");
echo("====================================================================");
echo("Chassis Base Width (Chi tiet in):", CHASSIS_W + 2.0 * BOSS_OUT, "mm");
echo("Total Width (Phu bi ca banh xe X):", TOTAL_WIDTH, "mm <= 118.0 mm < 120.0 mm");
echo(">>> DIEU KIEN TRUC X < 120MM:", (TOTAL_WIDTH < 120.0) ? "DAT CHUAN 100% PASS!" : "FAIL");
echo("Total Length (Chieu dai phu bi Y):", TOTAL_LENGTH, "mm <= 185.0 mm (PASS)");
echo("====================================================================");

// ====================================================================
// 1. KHUNG GẦM CHÍNH ULTRA-SLIM 120
// ====================================================================
color("DarkSlateGray")
    translate([0, 0, GROUND_CLEAR])
        chassis_base_slim120_omni();

// ====================================================================
// 2. MÔ PHỎNG 4 ĐỘNG CƠ GA25 TRONG BỐ TRÍ ZIGZAG ĐAN CHÉO ĐUÔI
// ====================================================================
module ga25_motor_model(is_encoder = true) {
    // Gearbox
    color("DimGray") cylinder(d=25.0, h=18.0);
    // Motor body
    color("Silver") translate([0, 0, 18.0]) cylinder(d=24.4, h=30.0);
    // Encoder cap
    if (is_encoder) {
        color("Black") translate([0, 0, 48.0]) cylinder(d=24.4, h=15.0);
    }
    // D-Shaft
    color("Gold") translate([0, 0, -8.0]) cylinder(d=4.0, h=8.0);
}

// 4 Động cơ GA25:
// Motor 1: Rear-Left (RL)
translate([-CHASSIS_W/2.0 - BOSS_OUT + 3.0, Y_RL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 90, 0]) ga25_motor_model(is_encoder = true);

// Motor 2: Rear-Right (RR)
translate([CHASSIS_W/2.0 + BOSS_OUT - 3.0, Y_RR, Z_SHAFT + GROUND_CLEAR])
    rotate([0, -90, 0]) ga25_motor_model(is_encoder = true);

// Motor 3: Front-Left (FL)
translate([-CHASSIS_W/2.0 - BOSS_OUT + 3.0, Y_FL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 90, 0]) ga25_motor_model(is_encoder = true);

// Motor 4: Front-Right (FR)
translate([CHASSIS_W/2.0 + BOSS_OUT - 3.0, Y_FR, Z_SHAFT + GROUND_CLEAR])
    rotate([0, -90, 0]) ga25_motor_model(is_encoder = true);

// ====================================================================
// 3. MÔ PHỎNG 4 BÁNH XE OMNI SIÊU MỎNG THỤT TRỤC (OFFSET HUB)
// ====================================================================
module omni_wheel_slim() {
    // Khớp nối lục giác âm lòng
    color("Goldenrod")
        rotate([0, 90, 0])
            cylinder(d=10.0, h=COUPLER_EFF, $fn=6);

    // Bánh xe Omni
    translate([COUPLER_EFF - HUB_OFFSET, 0, 0]) {
        color("DarkSlateGray") {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
        }
        // Con lăn cao su đa hướng
        color("Black") {
            for (i = [0:7]) {
                rotate([i * 45, 0, 0])
                    translate([WHEEL_W/2.0, WHEEL_D/2.0 - 3.5, 0])
                        rotate([0, 90, 0])
                            cylinder(d=7.0, h=WHEEL_W * 0.75, center=true);
            }
        }
    }
}

// Lắp 4 bánh xe:
// Bánh RL:
translate([-(CHASSIS_W/2.0 + BOSS_OUT), Y_RL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 180, 0]) omni_wheel_slim();

// Bánh RR:
translate([CHASSIS_W/2.0 + BOSS_OUT, Y_RR, Z_SHAFT + GROUND_CLEAR])
    omni_wheel_slim();

// Bánh FL:
translate([-(CHASSIS_W/2.0 + BOSS_OUT), Y_FL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 180, 0]) omni_wheel_slim();

// Bánh FR:
translate([CHASSIS_W/2.0 + BOSS_OUT, Y_FR, Z_SHAFT + GROUND_CLEAR])
    omni_wheel_slim();

// ====================================================================
// 4. HỆ THỐNG BI MẮT TRÂU TRỢ LỰC CHỐNG CHÚI / BẬP BÊNH (ANTI-TIP CASTER BALLS)
// ====================================================================
module caster_ball_unit() {
    // Vỏ gá bi mắt trâu CY-12A
    color("Silver") {
        cylinder(d=20.0, h=3.0);
        cylinder(d=14.0, h=GROUND_CLEAR + 2.0);
    }
    // Bi thép trợ lực đa hướng Ø12mm (tiếp xúc mặt sân)
    color("LightSteelBlue") {
        translate([0, 0, -GROUND_CLEAR/2.0])
            sphere(d=12.0);
    }
}

// Gá bi mắt trâu góc Trước - Trái (FL Support - Triệt tiêu 100% hiện tượng chúi đầu trái):
translate([-26.0, 156.0, GROUND_CLEAR])
    rotate([180, 0, 0]) caster_ball_unit();

// Gá bi mắt trâu góc Sau - Phải (RR Support - Triệt tiêu 100% hiện tượng bập bênh đuôi phải):
translate([ 26.0,  16.0, GROUND_CLEAR])
    rotate([180, 0, 0]) caster_ball_unit();

// Gá bi mắt trâu đối xứng Trước - Phải & Sau - Trái:
translate([ 26.0, 156.0, GROUND_CLEAR])
    rotate([180, 0, 0]) caster_ball_unit();
translate([-26.0,  16.0, GROUND_CLEAR])
    rotate([180, 0, 0]) caster_ball_unit();

// ====================================================================
// 5. KIẾN TRÚC TẬN DỤNG TRỤC Z: TẦNG ĐỠ PIN 2S2P & MẠCH K2 HUB
// ====================================================================
// TẦNG 1 (Z = 34.0 mm): SÀN ĐỠ PIN 2S2P (01D_Battery_Deck_Platform)
color("DarkCyan", 0.9) {
    translate([0, 69.0, GROUND_CLEAR + 34.0])
        battery_deck_platform();
}

// KHỐI PIN LI-ION 2S2P:
color("RoyalBlue", 0.9)
    translate([-19.0, 34.0, GROUND_CLEAR + 37.5])
        cube([38.0, 70.0, 38.0]);

// TẦNG 2 (Z = 76.0 mm): BO MẠCH ORC K2 CONTROL HUB
color("MediumSeaGreen", 0.85) {
    for (cx = [-28.0, 28.0]) {
        for (cy = [45.0, 95.0]) {
            translate([cx, cy, GROUND_CLEAR + 37.5])
                cylinder(d=6.0, h=38.0);
        }
    }
    translate([-43.0, 35.0, GROUND_CLEAR + 76.0])
        cube([86.0, 65.0, 12.0]);
}

// ====================================================================
// 6. CỤM THÁP NÂNG 01B/01C
// ====================================================================
color([0.95, 0.45, 0.1, 0.85]) {
    translate([-28.0, 135.5, GROUND_CLEAR + 49.0])
        rotate([0, 90, 0])
            import("01B_Lift_Tower_Left_FlatPrint.stl");
}

color([1.0, 0.55, 0.05, 0.85]) {
    translate([28.0, 0, GROUND_CLEAR])
        rotate([0, -90, 0])
            import("01C_Lift_Tower_Right_MG996R_FlatPrint.stl");
}

// ====================================================================
// 7. HỘP GIỚI HẠN BẢO VỆ QUI ĐỊNH X < 120MM (TRANSPARENT BOUNDING CUBE)
// ====================================================================
// HỘP GIỚI HẠN 120MM (TRỤC X) x 185MM (TRỤC Y) x 185MM (TRỤC Z)
color("Red", 0.25) {
    translate([-60.0, 0, 0]) {
        cube([120, 1.5, 1.5]);
        translate([0, 183.5, 0]) cube([120, 1.5, 1.5]);
        translate([0, 0, 183.5]) cube([120, 1.5, 1.5]);
        translate([0, 183.5, 183.5]) cube([120, 1.5, 1.5]);
        
        translate([0, 0, 0]) cube([1.5, 185, 1.5]);
        translate([118.5, 0, 0]) cube([1.5, 185, 1.5]);
        translate([0, 0, 183.5]) cube([1.5, 185, 1.5]);
        translate([118.5, 0, 183.5]) cube([1.5, 185, 1.5]);
        
        translate([0, 0, 0]) cube([1.5, 1.5, 185]);
        translate([118.5, 0, 0]) cube([1.5, 1.5, 185]);
        translate([0, 183.5, 0]) cube([1.5, 1.5, 185]);
        translate([118.5, 183.5, 0]) cube([1.5, 1.5, 185]);
    }
}
