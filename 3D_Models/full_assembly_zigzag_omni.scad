// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// BẢN LẮP RÁP TỔNG THỂ: KHUNG GẦM ĐỘNG CƠ ZIGZAG TẬN DỤNG TRỤC Z
// FILE: full_assembly_zigzag_omni.scad
// PHIÊN BẢN V9.0: ĐỘT PHÁ TỐI ƯU HÓA HOÀN TOÀN KHUNG GẦM VÀ BÁNH XE ĐA HƯỚNG
// GIẢI QUYẾT TRIỆT ĐỂ VẤN ĐỀ LÒI 12MM (212x212MM) -> THU GỌN VỀ CHỈ 146x176MM!
// ====================================================================

use <01_Chassis_Base_Zigzag_Omni.scad>;
use <01D_Battery_Deck_Platform.scad>;

$fn = 32;

// CẤU HÌNH BÁNH XE ĐA HƯỚNG:
WHEEL_CONFIG   = "OMNI_58"; // "OMNI_58", "OMNI_48", "MECANUM_60"

WHEEL_D        = (WHEEL_CONFIG == "OMNI_58") ? 58.0 : ((WHEEL_CONFIG == "OMNI_48") ? 48.0 : 60.0);
WHEEL_W        = (WHEEL_CONFIG == "OMNI_58") ? 16.0 : ((WHEEL_CONFIG == "OMNI_48") ? 15.0 : 28.0);
COUPLER_LEN    = 15.0; // Khớp nối lục giác GA25 ra bánh xe (Hex coupler)
CLEARANCE      = 2.0;

CHASSIS_W      = 76.0;
BOSS_OUT       = 4.0;
Z_SHAFT        = 20.0;
GROUND_CLEAR   = WHEEL_D / 2.0 - Z_SHAFT; // 9.0mm (Omni 58)

// TỌA ĐỘ 4 TRỤC ZIGZAG:
Y_RL = 24.0;
Y_RR = 54.0;
Y_FL = 86.0;
Y_FR = 142.0;

// TÍNH TOÁN PHỦ BÌ TỔNG THỂ:
// Khoảng cách từ tâm xe đến mép ngoài bánh xe:
X_WHEEL_OUT = CHASSIS_W/2.0 + BOSS_OUT + COUPLER_LEN + WHEEL_W; // 38 + 4 + 15 + 16 = 73.0 mm
TOTAL_WIDTH = 2.0 * X_WHEEL_OUT; // 146.0 mm

Y_MIN_ROBOT = min(Y_RL - WHEEL_D/2.0, 8.0); // 24 - 29 = -5.0 mm
Y_MAX_ROBOT = max(Y_FR + WHEEL_D/2.0, 168.5); // 142 + 29 = 171.0 mm
TOTAL_LENGTH = Y_MAX_ROBOT - Y_MIN_ROBOT; // 176.0 mm

echo("====================================================================");
echo("=== ORC-K2 ZIGZAG OMNI TOTAL PACKAGING REPORT ===");
echo("====================================================================");
echo("Cau hinh Banh xe:", WHEEL_CONFIG);
echo("Be rong phu bi (Total Width):", TOTAL_WIDTH, "mm (Giam tu 212mm cu!)");
echo("Chieu dai phu bi (Total Length):", TOTAL_LENGTH, "mm");
echo("Margin toi hop 200x200mm:", 200.0 - TOTAL_WIDTH, "mm (Width),", 200.0 - TOTAL_LENGTH, "mm (Length)");
echo("Margin toi hop 185x185mm:", 185.0 - TOTAL_WIDTH, "mm (Width),", 185.0 - TOTAL_LENGTH, "mm (Length)");
echo("Tuan thu kich thuoc:", (TOTAL_WIDTH <= 185.0 && TOTAL_LENGTH <= 185.0) ? "DAT 100% PASS!" : "CHECK");
echo("====================================================================");

// ====================================================================
// 1. KHUNG GẦM CHÍNH ĐỘNG CƠ ZIGZAG
// ====================================================================
color("DarkSlateGray")
    translate([0, 0, GROUND_CLEAR])
        chassis_base_zigzag_omni();

// ====================================================================
// 2. MÔ PHỎNG 4 ĐỘNG CƠ GA25 TRONG BỐ TRÍ ZIGZAG SO LE
// ====================================================================
module ga25_motor_model(is_encoder = true) {
    len = is_encoder ? 63.0 : 48.0;
    // Gearbox
    color("DimGray") cylinder(d=25.0, h=18.0);
    // Motor body
    color("Silver") translate([0, 0, 18.0]) cylinder(d=24.4, h=30.0);
    // Encoder cap if applicable
    if (is_encoder) {
        color("Black") translate([0, 0, 48.0]) cylinder(d=24.4, h=15.0);
    }
    // D-Shaft
    color("Gold") translate([0, 0, -10.0]) cylinder(d=4.0, h=10.0);
}

// 4 Động cơ GA25:
// Motor 1: Rear-Left (RL) - Encoder 63mm
translate([-CHASSIS_W/2.0 - BOSS_OUT + 3.0, Y_RL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 90, 0])
        ga25_motor_model(is_encoder = true);

// Motor 2: Rear-Right (RR) - Encoder 63mm
translate([CHASSIS_W/2.0 + BOSS_OUT - 3.0, Y_RR, Z_SHAFT + GROUND_CLEAR])
    rotate([0, -90, 0])
        ga25_motor_model(is_encoder = true);

// Motor 3: Front-Left (FL) - DC 48mm / Encoder 63mm
translate([-CHASSIS_W/2.0 - BOSS_OUT + 3.0, Y_FL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 90, 0])
        ga25_motor_model(is_encoder = true);

// Motor 4: Front-Right (FR) - DC 48mm / Encoder 63mm
translate([CHASSIS_W/2.0 + BOSS_OUT - 3.0, Y_FR, Z_SHAFT + GROUND_CLEAR])
    rotate([0, -90, 0])
        ga25_motor_model(is_encoder = true);

// ====================================================================
// 3. MÔ PHỎNG 4 BÁNH XE ĐA HƯỚNG OMNI 58MM + KHỚP NỐI LỤC GIÁC
// ====================================================================
module omni_wheel_sim() {
    // Khớp nối lục giác đồng (Hex Coupler)
    color("Goldenrod")
        rotate([0, 90, 0])
            cylinder(d=12.0, h=COUPLER_LEN, $fn=6);

    // Bánh xe Omni
    translate([COUPLER_LEN, 0, 0]) {
        color("DarkSlateGray") {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
        }
        // Con lăn cao su (Rollers)
        color("Black") {
            for (i = [0:7]) {
                rotate([i * 45, 0, 0])
                    translate([WHEEL_W/2.0, WHEEL_D/2.0 - 4.0, 0])
                        rotate([0, 90, 0])
                            cylinder(d=8.0, h=WHEEL_W * 0.8, center=true);
            }
        }
    }
}

// Lắp 4 bánh xe:
// Bánh RL (Left):
translate([-(CHASSIS_W/2.0 + BOSS_OUT), Y_RL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 180, 0]) omni_wheel_sim();

// Bánh RR (Right):
translate([CHASSIS_W/2.0 + BOSS_OUT, Y_RR, Z_SHAFT + GROUND_CLEAR])
    omni_wheel_sim();

// Bánh FL (Left):
translate([-(CHASSIS_W/2.0 + BOSS_OUT), Y_FL, Z_SHAFT + GROUND_CLEAR])
    rotate([0, 180, 0]) omni_wheel_sim();

// Bánh FR (Right):
translate([CHASSIS_W/2.0 + BOSS_OUT, Y_FR, Z_SHAFT + GROUND_CLEAR])
    omni_wheel_sim();

// ====================================================================
// 4. KIẾN TRÚC TẬN DỤNG TRỤC Z: TẦNG ĐỠ PIN 2S2P & MẠCH K2 HUB
// ====================================================================

// TẦNG 1 (Z = 34.0 mm): SÀN ĐỠ PIN 2S2P (01D_Battery_Deck_Platform)
color("DarkCyan", 0.9) {
    translate([0, 69.0, GROUND_CLEAR + 34.0])
        battery_deck_platform();
}

// KHỐI PIN LI-ION 2S2P (ĐẶT TRÊN SÀN TẦNG 1):
color("RoyalBlue", 0.9)
    translate([-19.0, 34.0, GROUND_CLEAR + 37.5])
        cube([38.0, 70.0, 38.0]); // Dạng gạch 2x2 siêu gọn!

// TẦNG 2 (Z = 76.0 mm): BO MẠCH ORC K2 CONTROL HUB
color("MediumSeaGreen", 0.85) {
    // 4 Cọc standoff đỡ Hub
    for (cx = [-28.0, 28.0]) {
        for (cy = [45.0, 95.0]) {
            translate([cx, cy, GROUND_CLEAR + 37.5])
                cylinder(d=6.0, h=38.0);
        }
    }
    // Bo mạch K2 Hub
    translate([-43.0, 35.0, GROUND_CLEAR + 76.0])
        cube([86.0, 65.0, 12.0]);
}

// ====================================================================
// 5. CỤM THÁP NÂNG 01B/01C & TAY GẮP HOA GẬP GỌN (STOWED)
// ====================================================================
// Tháp Trái (01B)
color([0.95, 0.45, 0.1, 0.85]) {
    translate([-28.0, 135.5, GROUND_CLEAR + 49.0])
        rotate([0, 90, 0])
            import("01B_Lift_Tower_Left_FlatPrint.stl");
}

// Tháp Phải (01C)
color([1.0, 0.55, 0.05, 0.85]) {
    translate([28.0, 0, GROUND_CLEAR])
        rotate([0, -90, 0])
            import("01C_Lift_Tower_Right_MG996R_FlatPrint.stl");
}

// ====================================================================
// 6. KHUNG DÂY SO SÁNH KÍCH THƯỚC (BOUNDING BOX COMPARISON)
// ====================================================================

// HỘP GIỚI HẠN 185x185x185 MM (ĐỎ)
color("Red", 0.3) {
    translate([-92.5, 0, 0]) {
        cube([185, 1.5, 1.5]);
        cube([1.5, 185, 1.5]);
        translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
        translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        translate([0, 0, 183.5]) {
            cube([185, 1.5, 1.5]);
            cube([1.5, 185, 1.5]);
            translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
            translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        }
        cube([1.5, 1.5, 185]);
        translate([183.5, 0, 0]) cube([1.5, 1.5, 185]);
        translate([0, 183.5, 0]) cube([1.5, 1.5, 185]);
        translate([183.5, 183.5, 0]) cube([1.5, 1.5, 185]);
    }
}

// ĐƯỜNG BAO 212x212 MM BỊ LÒI CŨ (VÀNG CAM - SO SÁNH TRỰC QUAN)
color("Orange", 0.5) {
    translate([-106.0, -16.0, 0]) {
        // Khung đáy 212x212mm
        cube([212.0, 2.0, 2.0]);
        cube([2.0, 212.0, 2.0]);
        translate([0, 210.0, 0]) cube([212.0, 2.0, 2.0]);
        translate([210.0, 0, 0]) cube([2.0, 212.0, 2.0]);
    }
}
