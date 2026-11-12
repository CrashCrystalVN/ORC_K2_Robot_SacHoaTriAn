// ====================================================================
// ORC-K2 PRO DFM V6.2 - FULL ASSEMBLY & PACKAGING VERIFICATION
// Kiểm tra lắp ghép 100% Khung gầm mới + Tháp nâng cũ (01B & 01C) + Tay gắp
// ====================================================================

$fn = 32;

// CHỌN CHẾ ĐỘ:
// MODE = "stowed"   : Gấp gọn trong hộp 200x200mm
// MODE = "working"  : Hạ cánh tay gắp hoa ngoài sàn
MODE = "working";

use <_test_front_redesign.scad>;

// THÔNG SỐ ĐỘNG HỌC TAY NÂNG VÀ ĐẦU GẮP
ARM_L = 98.0;
ARM_ANGLE = (MODE == "stowed") ? 88.0 : -20.0;
WRIST_PITCH = (MODE == "stowed") ? -90.0 : 0.0;
JAW_OPEN = (MODE == "stowed") ? 0.0 : 25.0;

// Cao độ và vị trí khớp xoay tháp nâng
Y_PIVOT = 145.0;
Z_PIVOT_LOWER = 4.0 + 58.0; // 62.0mm so với đáy sàn Z=0
Z_PIVOT_UPPER = 4.0 + 86.0; // 90.0mm (dZ = 28.0mm)

DY_ARM = ARM_L * cos(ARM_ANGLE);
DZ_ARM = ARM_L * sin(ARM_ANGLE);

Y_HEAD = Y_PIVOT + DY_ARM;
Z_HEAD = Z_PIVOT_LOWER + DZ_ARM;

// 1. KHUNG GẦM CHÍNH THIẾT KẾ MỚI (CHASSIS BASE V6.2)
color("DarkSlateGray")
    chassis_base_200x200();

// 2. CẶP THÁP NÂNG CŨ 01B & 01C (ĐÚNG NGUYÊN BẢN SPEC CỦA DỰ ÁN)
module lift_tower_left() {
    difference() {
        union() {
            translate([-28.0, 105.0, 4.0]) cube([8.0, 61.0, 90.0]);
            translate([-20.0, 105.0, 4.0]) cube([8.0, 22.5, 8.0]);
            translate([-20.0, 154.5, 4.0]) cube([8.0, 11.5, 8.0]);
            translate([-20.0, 105.0, 88.0]) cube([20.0, 13.0, 6.0]);
        }
        translate([-30.0, 127.5, 3.5]) cube([60.0, 27.0, 30.5]);
        translate([-29.0, 114.05, 47.9]) cube([10.0, 22.0, 20.2]);
        translate([-30.0, 145.0, 58.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=12.0);
        translate([-30.0, 145.0, 86.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);
        for (sy = [110.5, 122.0, 160.25]) translate([-16.0, sy, 3.5]) cylinder(d=3.3, h=10.0);
        for (sy = [116.0, 160.25]) translate([-24.0, sy, 3.5]) cylinder(d=3.0, h=14.0);
    }
}

module lift_tower_right() {
    difference() {
        union() {
            translate([20.0, 105.0, 4.0]) cube([8.0, 61.0, 90.0]);
            translate([12.0, 105.0, 4.0]) cube([8.0, 22.5, 8.0]);
            translate([12.0, 154.5, 4.0]) cube([8.0, 11.5, 8.0]);
            translate([0.0, 105.0, 88.0])  cube([20.0, 13.0, 6.0]);
        }
        translate([-30.0, 127.5, 3.5]) cube([60.0, 27.0, 30.5]);
        // Hốc Servo MG996R
        translate([19.0, 114.05, 47.9]) cube([10.0, 41.2, 20.2]);
        for (sy = [134.65 - 24.25, 134.65 + 24.25]) {
            for (sz = [58.0 - 5.0, 58.0 + 5.0]) {
                translate([19.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
            }
        }
        translate([-30.0, 145.0, 86.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);
        for (sy = [110.5, 122.0, 160.25]) translate([16.0, sy, 3.5]) cylinder(d=3.3, h=10.0);
        for (sy = [116.0, 160.25]) translate([24.0, sy, 3.5]) cylinder(d=3.0, h=14.0);
    }
}

color("SteelBlue") {
    lift_tower_left();
    lift_tower_right();
}

// 3. SERVO MG996R S1 BÊN THÁP PHẢI
color("SlateGray")
    translate([20.0, 114.05, 47.9]) cube([40.5, 20.0, 41.0]);

// 4. MÔ PHỎNG 10 TUA-VÍT SIẾT ỐC (SCREWDRIVER ACCESS PATHS)
// Các đường xi-lanh vàng thẳng đứng từ Z=75 xuống tận 10 lỗ ốc M3 để chứng minh 100% không bị cấn!
color("Gold", 0.75) {
    // 4 ốc chân trước (Y = 160.25)
    for (sx = [-24.0, -16.0, 16.0, 24.0]) {
        translate([sx, 160.25, 4.0]) cylinder(d=4.5, h=65.0);
    }
    // 6 ốc chân sau
    for (sx = [-16.0, 16.0]) {
        for (sy = [110.5, 122.0]) {
            translate([sx, sy, 4.0]) cylinder(d=4.5, h=65.0);
        }
    }
    for (sx = [-24.0, 24.0]) {
        translate([sx, 116.0, 4.0]) cylinder(d=4.5, h=65.0);
    }
}

// 5. CÁNH TAY NÂNG CHỮ H DƯỚI (03) & TRÊN (03B)
module arm_h_lower() {
    difference() {
        union() {
            translate([-19.5, 0, -6.0]) cube([5.0, ARM_L, 12.0]);
            translate([ 14.5, 0, -6.0]) cube([5.0, ARM_L, 12.0]);
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=12.0, h=5.0);
            translate([ 14.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=12.0, h=5.0);
            translate([-19.5, ARM_L, 0]) rotate([0, 90, 0]) cylinder(d=12.0, h=5.0);
            translate([ 14.5, ARM_L, 0]) rotate([0, 90, 0]) cylinder(d=12.0, h=5.0);
            translate([-14.5, 42.0, -6.0]) cube([29.0, 14.0, 12.0]);
        }
        translate([-25.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=3.3, h=50.0);
        translate([-25.0, ARM_L, 0]) rotate([0, 90, 0]) cylinder(d=3.3, h=50.0);
    }
}

color("DarkOrange")
    translate([0, Y_PIVOT, Z_PIVOT_LOWER])
        rotate([ARM_ANGLE - 90.0, 0, 0])
            arm_h_lower();

color("Peru")
    translate([0, Y_PIVOT, Z_PIVOT_UPPER])
        rotate([ARM_ANGLE - 90.0, 0, 0])
            arm_h_lower();

// 6. CỔ TAY S3 & BỆ ĐẦU KẸP
module gripper_assembly_sim() {
    // Khối bệ gá đầu kẹp
    color("ForestGreen") {
        translate([-33.0, 0, -15.0]) cube([66.0, 48.0, 30.0]);
    }
    // 2 Ngàm kẹp hoa
    color("Crimson") {
        translate([-26.0, 40.0, -10.0])
            rotate([0, 0, -JAW_OPEN])
                cube([8.0, 55.0, 18.0]);
        translate([ 18.0, 40.0, -10.0])
            rotate([0, 0, JAW_OPEN])
                cube([8.0, 55.0, 18.0]);
    }
}

translate([0, Y_HEAD, Z_HEAD])
    rotate([WRIST_PITCH, 0, 0])
        gripper_assembly_sim();
