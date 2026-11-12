use <01_Chassis_Base_185x185.scad>;
use <01D_Base_Riser_Frame.scad>;
// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// BẢN LẮP RÁP TỔNG THỂ ROBOT ORC K2 - CHUẨN ĐÓNG GÓI 185x185 MM (185 CUBE)
// File: full_assembly_185x185.scad
// ====================================================================
// NGUYÊN TẮC THIẾT KẾ & ĐÓNG GÓI 185x185 (185MM INSPECTION BOX COMPLIANCE):
// 1. Kích thước bao hình cụm Base + Bánh xe (Assembled Robot Base Footprint):
//    - Chiều rộng phủ bì (Total Width): X_max - X_min = 178.0 mm <= 185.0 mm (Margin >= 7.0 mm)
//    - Chiều dài phủ bì (Total Length): Y_max - Y_min = 170.0 mm <= 185.0 mm (Margin >= 15.0 mm)
//    - Chiều cao gầm xe (Base Height): 60.0 mm <= 185.0 mm (Margin >= 125.0 mm)
// 2. Kích thước chi tiết in 3D (Base Part):
//    - 139.0 x 172.0 x 38.0 mm (Max dimension = 172.0 mm <= 185.0 mm, vừa bàn in A1 Mini 180x180mm)
// 3. Cơ cấu động học tay gắp hoa:
//    - Tay nâng H-Frame kết hợp Servo MG996R (S1 Nâng, S2 Kẹp, S3 Cổ tay)
//    - Cặp Tháp nâng 01B & 01C bắt chặt bằng 10 bu-lông M3 vào khung gầm
// 4. Hệ thống điều khiển & Động lực:
//    - Mạch ORC K2 Control Hub ESP32-S3 trên bệ Adapter 01D
//    - 4 Động cơ GA25 (Cầu sau 2x Encoder 63mm có khe hở an toàn +7.0mm, ZERO COLLISION)
//    - Bộ pin Li-ion 2S2P trong khoang vạn năng 82x76mm chằng 2 đai Velcro
// ====================================================================

$fn = 32;

// THAM SỐ ĐIỀU KHIỂN:
STOWED_MODE    = true;
WHEEL_CONFIG   = "MECANUM_60";
DISPLAY_MODE   = "inspection_box"; // "assembly" hoặc "inspection_box"

// THÔNG SỐ HÌNH HỌC:
WHEEL_D        = (WHEEL_CONFIG == "MECANUM_60") ? 60.0 : 80.0;
WHEEL_W        = (WHEEL_CONFIG == "MECANUM_60") ? 28.0 : 38.0;
GROUND_CLEAR   = (WHEEL_CONFIG == "MECANUM_60") ? 10.0 : 20.0;
Z_SHAFT        = WHEEL_D / 2.0;

CHASSIS_W      = 118.0; // Bề rộng thân xe chính chuẩn ORC DFM
CHASSIS_L      = 172.0;
FLOOR_T        = 4.0;
WALL_H         = 30.0;

// Tọa độ 4 bánh xe và 4 động cơ GA25
Y_REAR_WHEEL   = 32.0;
Y_FRONT_WHEEL  = 142.0;

// Tính toán phủ bì tổng thể:
TOTAL_ROBOT_WIDTH  = CHASSIS_W + 2 * WHEEL_W + 4.0; // 178.0 mm <= 185.0 mm
TOTAL_ROBOT_LENGTH = max(CHASSIS_L, Y_FRONT_WHEEL + WHEEL_D/2.0) - (Y_REAR_WHEEL - WHEEL_D/2.0); // 170.0 mm <= 185.0 mm

echo("=====================================================");
echo("=== ORC K2 ROBOT 185x185x185 MM PACKAGING REPORT ===");
echo("=====================================================");
echo("Trang thai Robot:", STOWED_MODE ? "STOWED (GAP GON)" : "DEPLOYED (VUON HOAT DONG)");
echo("Cau hinh Banh xe:", WHEEL_CONFIG);
echo("Be rong khung xe (Chassis Width):", CHASSIS_W, "mm");
echo("Tong be rong phu bi (Total Width):", TOTAL_ROBOT_WIDTH, "mm (Gioi han <= 185.0 mm)");
echo("Tong chieu dai phu bi (Total Length):", TOTAL_ROBOT_LENGTH, "mm (Gioi han <= 185.0 mm)");
echo("Tuan thu kich thuoc 185x185mm Footprint:", (TOTAL_ROBOT_WIDTH <= 185.0 && TOTAL_ROBOT_LENGTH <= 185.0) ? "DAT 100% (PASS)" : "KHONG DAT (FAIL)");
echo("=====================================================");

// 1. Khung gầm chính
module chassis_plate() {
    chassis_base_185x185();
}

// 2. Bánh xe Mecanum 60mm
module mecanum_wheel_60(is_left = true) {
    color("Goldenrod") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 12.0, h=5.0);
            translate([WHEEL_W - 4.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 12.0, h=5.0);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.2, h=WHEEL_W + 2);
        }
    }
    color("DimGray") {
        for (i = [0:7]) {
            rotate([i * 45, 0, 0])
                translate([WHEEL_W/2, WHEEL_D/2 - 4.5, 0])
                    rotate([0, is_left ? 45 : -45, 0])
                        cylinder(d=9.0, h=WHEEL_W * 0.85, center=true);
        }
    }
}

// 3. Động cơ GA25
module ga25_motor_model() {
    color("DarkGray") {
        rotate([0, 90, 0]) cylinder(d=25.0, h=21.0);
        translate([21.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.0, h=10.0);
    }
    color("Silver") {
        translate([-31.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.4, h=31.0);
    }
    color("Black") {
        translate([-43.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.4, h=12.0);
    }
}

// Lắp ráp tổng thể Base Robot 185x185
module robot_base_185_assembly() {
    // 1. Khung gầm chính
    color("DarkSlateGray")
        translate([0, 0, GROUND_CLEAR])
            chassis_plate();

    // 2. 4 Động cơ GA25
    for (side = [-1, 1]) {
        translate([side * (CHASSIS_W/2 - 2.0), Y_REAR_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
        translate([side * (CHASSIS_W/2 - 2.0), Y_FRONT_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
    }

    // 3. 4 Bánh xe Mecanum 60mm
    for (side = [-1, 1]) {
        translate([side * (CHASSIS_W/2 + (side > 0 ? 2.0 : -WHEEL_W - 2.0)), Y_REAR_WHEEL, Z_SHAFT])
            mecanum_wheel_60(is_left = (side < 0));
        translate([side * (CHASSIS_W/2 + (side > 0 ? 2.0 : -WHEEL_W - 2.0)), Y_FRONT_WHEEL, Z_SHAFT])
            mecanum_wheel_60(is_left = (side > 0));
    }

    // 4. Khối pin 2S2P trong khoang
    color("RoyalBlue", 0.85)
        translate([-19.0, 51.0, GROUND_CLEAR + FLOOR_T])
            cube([38.0, 70.0, 38.0]);

    // 5. Mạch điều khiển ORC K2 Control Hub ESP32-S3 (Z = 51.0..77.0mm)
    color("Black")
        translate([-60.5, 30.0, GROUND_CLEAR + 46.0])
            cube([121.0, 86.0, 26.0]);
    color("DarkOrange")
        translate([-42.0, 35.0, GROUND_CLEAR + 72.0])
            cube([84.0, 76.0, 0.8]);

    // 6. Lồng kiểm tra quy chuẩn 185 x 185 x 185 mm (Inspection Box 185 Cube)
    if (DISPLAY_MODE == "inspection_box") {
        box_s = 185.0;
        x_min = -box_s / 2.0; // -92.5 mm
        y_min = 0.0;
        
        color("Red", 0.12) {
            translate([x_min, y_min, 0])
                cube([box_s, box_s, box_s]);
        }
        color("Red") {
            translate([x_min, y_min, 0]) cube([box_s, 2.0, 2.0]);
            translate([x_min, y_min + box_s - 2.0, 0]) cube([box_s, 2.0, 2.0]);
            translate([x_min, y_min, 0]) cube([2.0, box_s, 2.0]);
            translate([x_min + box_s - 2.0, y_min, 0]) cube([2.0, box_s, 2.0]);
            
            translate([x_min, y_min, box_s - 2.0]) cube([box_s, 2.0, 2.0]);
            translate([x_min, y_min + box_s - 2.0, box_s - 2.0]) cube([box_s, 2.0, 2.0]);
            translate([x_min, y_min, box_s - 2.0]) cube([2.0, box_s, 2.0]);
            translate([x_min + box_s - 2.0, y_min, box_s - 2.0]) cube([2.0, box_s, 2.0]);

            translate([x_min, y_min, 0]) cube([2.0, 2.0, box_s]);
            translate([x_min + box_s - 2.0, y_min, 0]) cube([2.0, 2.0, box_s]);
            translate([x_min, y_min + box_s - 2.0, 0]) cube([2.0, 2.0, box_s]);
            translate([x_min + box_s - 2.0, y_min + box_s - 2.0, 0]) cube([2.0, 2.0, box_s]);
        }
    }
}

robot_base_185_assembly();
