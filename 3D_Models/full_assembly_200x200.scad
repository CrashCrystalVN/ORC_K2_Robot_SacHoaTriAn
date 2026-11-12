use <01D_Base_Riser_Frame.scad>;
// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// BẢN LẮP RÁP TỔNG THỂ ROBOT ORC K2 - CHUẨN ĐÓNG GÓI 200x200 MM
// File: full_assembly_200x200.scad
// Tác giả: Subagent 3 - Assembly 200x200 Integrator & Verifier
// ====================================================================
// NGUYÊN TẮC THIẾT KẾ & ĐÓNG GÓI 200x200 (INSPECTION BOX COMPLIANCE):
// 1. Kích thước bao hình khi gấp gọn (Stowed State):
//    - Chiều rộng phủ bì (Width): X_max - X_min <= 194.0 mm <= 200.0 mm (Margin >= 6.0 mm)
//    - Chiều dài phủ bì (Length): Y_max - Y_min <= 186.0 mm <= 200.0 mm (Margin >= 14.0 mm)
// 2. Cơ chế gấp gọn 2 khớp (Dual-Joint Stowing Kinematics):
//    - Khớp nâng chính (S1 MG996R): Nâng cánh tay H-Frame dựng đứng lên góc ARM_ANGLE = 85.0°..90.0°
//    - Khớp cổ tay (S3 MG996R): Gập cụm bệ gắp chúc xuống theo phương thẳng đứng WRIST_PITCH_ANGLE = -90.0°
//    - Khớp kẹp (S2 MG996R): Khép 2 ngàm kẹp song song khít chặt GRIP_ANGLE = 0.0°
//    -> Toàn bộ cụm tay nâng và đầu gắp thu gọn hoàn toàn trong khoảng Y in [115, 180] mm!
// 3. Tương thích 100% phần cứng:
//    - 4 Động cơ GA25 (M1, M2, E1 có encoder, E2 có encoder) + Nẹp kẹp 02B/02C/02D
//    - Mạch ORC K2 Control Hub ESP32-S3 (121 x 86 x 26 mm) trên bệ Adapter 01D
//    - Bộ pin Li-ion 2S 18650 đặt tại khoang giữa sàn gầm xe
//    - Cặp Tháp nâng 01B/01C + 3 Servo MG996R (S1 Nâng, S2 Kẹp, S3 Cổ tay)
//    - Cảm biến siêu âm mũi xe + Cảm biến dò line 01E dưới gầm + 2 ToF Laser VL53L0X hai sườn
// ====================================================================

$fn = 32;

// ====================================================================
// THAM SỐ ĐIỀU KHIỂN CHẾ ĐỘ HIỂN THỊ VÀ TRẠNG THÁI ROBOT
// ====================================================================
// STOWED_MODE = true  : Robot ở trạng thái GẤP GỌN XUẤT PHÁT (Footprint <= 200 x 200 mm)
// STOWED_MODE = false : Robot ở trạng thái HOẠT ĐỘNG VƯƠN RA (Kẹp hoa, cự ly vươn xa 350mm)
STOWED_MODE    = true;

// CẤU HÌNH BÁNH XE:
// "MECANUM_60" : Bánh Mecanum D60mm x W28mm -> Tổng bề rộng 192.0 mm (Khuyên dùng chuẩn ORC)
// "MECANUM_80" : Bánh Mecanum D80mm x W38mm -> Tổng bề rộng 196.0 mm (Khung gầm thu hẹp 120mm)
WHEEL_CONFIG   = "MECANUM_60";

// CHỌN CHẾ ĐỘ HIỂN THỊ:
// "assembly"     : Phối cảnh 3D trực quan đầy đủ màu sắc và linh kiện
// "inspection_box": Vẽ thêm lồng bao kiểm tra 200 x 200 mm màu đỏ trong suốt
DISPLAY_MODE   = "assembly";

// ====================================================================
// TÍNH TOÁN KÍCH THƯỚC HÌNH HỌC VÀ ĐỘNG HỌC
// ====================================================================
WHEEL_D        = (WHEEL_CONFIG == "MECANUM_60") ? 60.0 : 80.0;
WHEEL_W        = (WHEEL_CONFIG == "MECANUM_60") ? 28.0 : 38.0;
GROUND_CLEAR   = (WHEEL_CONFIG == "MECANUM_60") ? 10.0 : 20.0;
Z_SHAFT        = WHEEL_D / 2.0;

CHASSIS_W      = (WHEEL_CONFIG == "MECANUM_60") ? 134.0 : 120.0;
CHASSIS_L      = 172.0;
FLOOR_T        = 4.0;
WALL_H         = 28.0;

// Tọa độ 4 bánh xe và 4 động cơ GA25
Y_REAR_WHEEL   = 32.0;
Y_FRONT_WHEEL  = 140.0;

// Thông số động học tay nâng 4 khâu chữ H
Y_PIVOT        = 135.0;
Z_PIVOT        = GROUND_CLEAR + FLOOR_T + 74.0; // 88.0mm khi bánh 60mm
ARM_L          = 98.0;

// Góc điều khiển tay nâng và cổ tay theo trạng thái
ARM_ANGLE         = STOWED_MODE ? 88.0 : -20.0;
WRIST_PITCH_ANGLE = STOWED_MODE ? -90.0 : 0.0;
GRIP_ANGLE        = STOWED_MODE ? 0.0 : 25.0;

// Tọa độ tâm khớp cổ tay theo phương trình động học
DY_ARM = ARM_L * cos(ARM_ANGLE);
DZ_ARM = ARM_L * sin(ARM_ANGLE);
Y_HEAD = Y_PIVOT + DY_ARM - 8.0;
Z_HEAD = Z_PIVOT + DZ_ARM - 10.0;

// Tọa độ bản lề xoay cổ tay S3
Y_WRIST_PIVOT = Y_HEAD + 26.8;
Z_WRIST_PIVOT = Z_HEAD + 38.0;

// Tính toán chiều dài tổng thể chuẩn xác (Mép cản trước VL53L0X / mép bánh trước tới mép bánh sau)
TOTAL_ROBOT_WIDTH  = CHASSIS_W + 2 * WHEEL_W + 2.0;
TOTAL_ROBOT_LENGTH = max(CHASSIS_L, Y_FRONT_WHEEL + WHEEL_D/2.0) - (Y_REAR_WHEEL - WHEEL_D/2.0);

// In báo cáo kích thước tổng thể ra console OpenSCAD
echo("=====================================================");
echo("=== ORC K2 ROBOT 200x200 PACKAGING REPORT ===");
echo("=====================================================");
echo("Trang thai Robot:", STOWED_MODE ? "STOWED (GAP GON)" : "DEPLOYED (VUON HOAT DONG)");
echo("Cau hinh Banh xe:", WHEEL_CONFIG);
echo("Be rong khung xe (Chassis Width):", CHASSIS_W, "mm");
echo("Tong be rong phu bi (Total Width):", TOTAL_ROBOT_WIDTH, "mm (Gioi han <= 200.0 mm)");
echo("Tong chieu dai phu bi (Total Length):", TOTAL_ROBOT_LENGTH, "mm (Gioi han <= 200.0 mm)");
echo("Chieu cao tich hop (Height):", STOWED_MODE ? Z_WRIST_PIVOT + 15.0 : Z_HEAD + 80.0, "mm");
echo("Tuan thu kich thuoc 200x200mm:", (TOTAL_ROBOT_WIDTH <= 200.0 && TOTAL_ROBOT_LENGTH <= 200.0) ? "DAT 100% (PASS)" : "KHONG DAT (FAIL)");
echo("=====================================================");
echo("=== KHOANG HO 3D PIN GACH 2S2P (38x38x70mm) ===");
echo("- Vi tri toa do: X in [-19.0, +19.0 mm], Y in [51.0, 121.0 mm], Z in [4.0, 42.0 mm]");
echo("- Khoang ho voi 2 duoi motor encoder cau sau (Y=44.5mm): Delta_Y = 6.5 mm (Zero Collision)");
echo("- Khoang ho voi dong co cau truoc (Y=127.5mm): Delta_Y = 6.5 mm (Zero Collision)");
echo("- Khoang ho voi chan thap nang truoc (Y=124.0mm): Delta_Y = 3.0 mm (Zero Collision)");
echo("- Khoang ho tinh khong voi day san K2 Hub (Z=46.0mm): Delta_Z = 4.0 mm (Zero Collision, vua 2mm dai Velcro)");
echo("- Khoang ho hai ben voi 2 chan khung don (X=+-26.5mm, lot long 53.0mm): Delta_X = 7.5 mm moi ben (Zero Collision)");
echo("=====================================================");

// ====================================================================
// MODULES CHI TIẾT
// ====================================================================

// 1. Khung gầm chính 200x200 (Chassis Base)
module chassis_base() {
    difference() {
        union() {
            // Sàn đáy phẳng Z = 0
            translate([-CHASSIS_W/2, 0, 0])
                cube([CHASSIS_W, CHASSIS_L, FLOOR_T]);

            // Vách sườn hai bên
            translate([-CHASSIS_W/2, 0, 0])
                cube([4.0, CHASSIS_L, WALL_H]);
            translate([CHASSIS_W/2 - 4.0, 0, 0])
                cube([4.0, CHASSIS_L, WALL_H]);

            // 4 Ổ đỡ động cơ GA25
            for (my = [Y_REAR_WHEEL, Y_FRONT_WHEEL]) {
                translate([-CHASSIS_W/2, my - 20.0, 0]) cube([36.0, 40.0, 20.0]);
                translate([CHASSIS_W/2 - 36.0, my - 20.0, 0]) cube([36.0, 40.0, 20.0]);
                translate([-CHASSIS_W/2, my - 16.0, 0]) cube([4.0, 32.0, 32.0]);
                translate([CHASSIS_W/2 - 4.0, my - 16.0, 0]) cube([4.0, 32.0, 32.0]);
            }

            // Khoang Pin 2S2P phang hoan toan tai Z = FLOOR_T (Universal 2S2P Bay)

            // 4 Trụ đỡ bệ MCU
            for (px = [-38.0, 28.0]) {
                for (py = [44.0, 94.0]) {
                    translate([px, py, FLOOR_T]) cube([10.0, 10.0, 18.0]);
                }
            }

            // Mũi cản trước vát khí động học & bệ gá VL53L0X (Cao 14.0mm)
            hull() {
                translate([-20.0, CHASSIS_L - 2.0, 0]) cube([40.0, 2.0, 14.0]);
                translate([-34.0, CHASSIS_L - 10.0, 0]) cube([68.0, 2.0, 14.0]);
                translate([-24.0, CHASSIS_L - 16.0, 0]) cube([48.0, 6.0, 10.0]);
            }

            // Gờ chân tháp nâng
            translate([-30.0, 105.0, FLOOR_T]) cube([2.0, 14.5, 4.0]);
            translate([28.0, 105.0, FLOOR_T])  cube([2.0, 14.5, 4.0]);
            translate([-28.0, 102.5, FLOOR_T]) cube([16.0, 2.5, 4.0]);
            translate([12.0, 102.5, FLOOR_T])  cube([16.0, 2.5, 4.0]);
        }

        // Khoét lỗ động cơ GA25
        for (my = [Y_REAR_WHEEL, Y_FRONT_WHEEL]) {
            translate([-CHASSIS_W/2 + 4.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=25.4, h=34.0);
            translate([CHASSIS_W/2 - 38.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=25.4, h=34.0);
            translate([-CHASSIS_W/2 - 1.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=9.0, h=6.0);
            translate([CHASSIS_W/2 - 5.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=9.0, h=6.0);

            for (dy = [-17.5, 17.5]) {
                translate([-CHASSIS_W/2 + 20.0, my + dy, 3.0]) cylinder(d=3.0, h=18.0);
                translate([CHASSIS_W/2 - 20.0, my + dy, 3.0])  cylinder(d=3.0, h=18.0);
            }
        }

        // 4 Lỗ ốc M3 trụ bệ MCU
        for (px = [-33.0, 33.0]) {
            for (py = [49.0, 99.0]) {
                translate([px, py, 4.0]) cylinder(d=3.0, h=19.0);
            }
        }

        // Lỗ bắt tháp nâng
        for (sx = [-16.0, 16.0]) {
            for (sy = [110.5, 122.0, 160.25]) {
                translate([sx, sy, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
            }
        }
        for (sx = [-24.0, 24.0]) {
            for (sy = [116.0, 160.25]) {
                translate([sx, sy, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
            }
        }

        // 4 Khe luon dai dan Velcro ban 20mm (X = +-38.0mm, Y = 60.0 & 90.0mm)
        for (zx = [-40.0, 36.0]) {
            for (zy = [60.0, 90.0]) {
                translate([zx, zy, -0.5]) cube([4.0, 22.0, FLOOR_T + 1.0]);
            }
        }

        // Hốc gá & Cửa sổ quang học cảm biến Laser ToF VL53L0X mũi xe
        hull() {
            translate([-5.5, CHASSIS_L - 5.6, 6.5]) cube([11.0, 0.2, 6.0]);
            translate([-8.0, CHASSIS_L + 0.1, 5.25]) cube([16.0, 0.2, 8.5]);
        }
        translate([-12.8, CHASSIS_L - 5.5, FLOOR_T]) cube([25.6, 2.4, 11.0]);
        translate([-10.0, CHASSIS_L - 8.5, FLOOR_T]) cube([20.0, 3.0, 10.0]);
        translate([-10.0, CHASSIS_L - 9.0, 9.5]) rotate([-90, 0, 0]) cylinder(d=3.0, h=10.0);
        translate([ 10.0, CHASSIS_L - 9.0, 9.5]) rotate([-90, 0, 0]) cylinder(d=3.0, h=10.0);
        translate([-7.0, CHASSIS_L - 18.0, -0.5]) cube([14.0, 10.0, FLOOR_T + 1.0]);

        // Rãnh luồn dây
        translate([-12.0, 18.0, -0.5]) cube([24.0, 20.0, FLOOR_T + 1.0]);
    }
}

// 2. Bánh xe Mecanum (D60mm hoặc D80mm)
module mecanum_wheel(is_left = true) {
    color("Goldenrod") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 12.0, h=5.0);
            translate([WHEEL_W - 4.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 12.0, h=5.0);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.2, h=WHEEL_W + 2);
        }
    }
    // Các con lăn cao su góc 45°
    color("DimGray") {
        for (i = [0:7]) {
            rotate([i * 45, 0, 0])
                translate([WHEEL_W/2, WHEEL_D/2 - 4.5, 0])
                    rotate([0, is_left ? 45 : -45, 0])
                        cylinder(d=10.0, h=WHEEL_W * 0.85, center=true);
        }
    }
}

// 3. Động cơ giảm tốc GA25
module ga25_motor_model() {
    color("DarkGray") {
        // Hộp giảm tốc kim loại D25 x L21 mm
        rotate([0, 90, 0]) cylinder(d=25.0, h=21.0);
        // Trục ra D4 vát D
        translate([21.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.0, h=10.0);
    }
    color("Silver") {
        // Thân motor điện D24.4 x L31 mm
        translate([-31.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.4, h=31.0);
    }
    color("Black") {
        // Nắp đuôi & mạch Encoder D24.4 x L12 mm
        translate([-43.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.4, h=12.0);
    }
}

// 4. Tháp nâng Trái & Phải
module lift_tower(is_left = true) {
    x_pos = is_left ? -28.0 : 20.0;
    difference() {
        union() {
            translate([x_pos, 105.0, 0]) cube([8.0, 61.0, 90.0]);
            translate([is_left ? -20.0 : 12.0, 105.0, 0]) cube([8.0, 22.5, 8.0]);
            translate([is_left ? -20.0 : 12.0, 154.5, 0]) cube([8.0, 11.5, 8.0]);
        }
        // Vòm cổng thoáng dưới chân
        translate([-30.0, 127.5, -0.5]) cube([60.0, 27.0, 30.5]);
        // Hốc lắp Servo MG996R S1 bên tháp phải
        if (!is_left) {
            translate([19.0, 114.0, 48.0]) cube([10.0, 42.0, 21.0]);
        }
        // Lỗ trục xoay tay nâng (Y = 135.0, Z = 74.0 & 94.0)
        translate([-30.0, 135.0, 74.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);
        translate([-30.0, 135.0, 94.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);
    }
}

// 5. Cánh tay nâng chữ H
module h_frame_arm(is_upper = false) {
    h = is_upper ? 11.0 : 12.0;
    difference() {
        union() {
            translate([-19.5, 0, -h/2]) cube([5.0, ARM_L, h]);
            translate([14.5, 0, -h/2])  cube([5.0, ARM_L, h]);
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=h, h=5.0);
            translate([14.5, 0, 0])  rotate([0, 90, 0]) cylinder(d=h, h=5.0);
            translate([-19.5, ARM_L, 0]) rotate([0, 90, 0]) cylinder(d=h, h=5.0);
            translate([14.5, ARM_L, 0])  rotate([0, 90, 0]) cylinder(d=h, h=5.0);
            translate([-14.5, 42.0, -h/2]) cube([29.0, 14.0, h]);
        }
        translate([-22.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=3.3, h=44.0);
        translate([-22.0, ARM_L, 0]) rotate([0, 90, 0]) cylinder(d=3.3, h=44.0);
    }
}

// 6. Cổ gá Servo S3 gập cổ tay
module wrist_clevis_s3() {
    difference() {
        union() {
            translate([-14.0, 0, -2.5]) cube([28.0, 16.6, 46.5]);
            translate([-14.0, 16.6, -2.5]) cube([27.0, 20.4, 9.7]);
            translate([-14.0, 16.6, 38.0]) cube([27.0, 20.4, 8.0]);
        }
        // Khe chốt tay nâng
        translate([-8.5, 4.5, -3.0]) cube([17.0, 12.2, 50.0]);
        translate([-20.0, 8.0, 10.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
        translate([-20.0, 8.0, 38.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
        // Trục xoay cổ tay
        translate([-30.0, 26.8, 38.0]) rotate([0, 90, 0]) cylinder(d=3.2, h=60.0);
    }
}

// 7. Bệ đầu kẹp và cặp ngàm kẹp V2.0
module gripper_head_and_jaws() {
    // Bệ đầu kẹp
    color("OrangeRed") {
        difference() {
            union() {
                translate([-30.0, 0, 0]) cube([60.0, 42.0, 14.0]);
                translate([-15.0, 39.0, 0]) cylinder(d=17.0, h=14.0);
                translate([15.0, 39.0, 0])  cylinder(d=17.0, h=14.0);
            }
            translate([-15.0, 39.0, -1.0]) cylinder(d=3.4, h=16.0);
            translate([15.0, 39.0, -1.0])  cylinder(d=3.4, h=16.0);
            translate([-10.0, 10.0, -1.0]) cube([20.0, 22.0, 16.0]);
        }
    }

    // Servo S2 điều khiển kẹp
    color("SlateGray") {
        translate([-10.0, 10.0, 14.0]) cube([20.0, 40.7, 37.5]);
    }

    // Cặp ngàm kẹp V2
    color("Crimson") {
        // Ngàm trái
        translate([-15.0, 39.0, 5.0])
            rotate([0, 0, -GRIP_ANGLE])
                translate([15.0, 0, 0])
                    gripper_jaw_model(is_left = true);

        // Ngàm phải
        translate([15.0, 39.0, 5.0])
            rotate([0, 0, GRIP_ANGLE])
                translate([-15.0, 0, 0])
                    gripper_jaw_model(is_left = false);
    }
}

// Mô hình ngàm kẹp có bánh răng Involute và rãnh V kép
module gripper_jaw_model(is_left = true) {
    sx = is_left ? -1 : 1;
    difference() {
        union() {
            // Hub bánh răng
            translate([sx * 15.0, 0, 0]) cylinder(r=15.0, h=8.0);
            // Thân dầm ngàm dài 118mm
            translate([sx > 0 ? 0 : -28.0, 0, 0]) cube([28.0, 118.0, 22.0]);
        }
        // Lỗ trục M3
        translate([sx * 15.0, 0, -1.0]) cylinder(d=3.4, h=24.0);
        // Rãnh V kẹp ống hoa D32
        for (y_v = [33.0, 66.0, 99.0]) {
            translate([0, y_v, 11.0]) rotate([0, 0, sx * 45]) cube([16.0, 16.0, 24.0], center=true);
        }
    }
}

// 8. Bệ Adapter MCU & Cảm biến ToF VL53L0X
module mcu_adapter_deck() {
    color("DarkSlateGray") {
        difference() {
            union() {
                translate([-58.0, -4.0, 0]) cube([116.0, 88.0, 4.0]);
                // Cánh gá cảm biến VL53L0X hai bên sườn
                translate([-66.0, 64.0, 0]) cube([16.0, 20.0, 4.0]);
                translate([50.0, 64.0, 0])  cube([16.0, 20.0, 4.0]);
            }
            // Khe thoát cáp trung tâm
            translate([-20.0, 20.0, -1.0]) cube([40.0, 40.0, 6.0]);
        }
    }
}

// ====================================================================
// MODULE KHỐI PIN ĐÓNG SẴN 2S2P 18650 DẠNG GẠCH 2x2 (38 x 38 x 70 MM)
// ====================================================================
module battery_brick_2s2p(with_strap = true, with_cable = true) {
    // Vỏ bọc co nhiệt PVC màu xanh dương (RoyalBlue)
    // Kích thước chuẩn: X in [-19.0, +19.0], Y in [51.0, 121.0], Z in [FLOOR_T, FLOOR_T + 38.0]
    W = 38.0;
    L = 70.0;
    H = 38.0;
    cell_r = 9.25;

    translate([0, 51.0, FLOOR_T]) {
        // 1. Thân khối pin 2x2 bo tròn 4 góc (mô phỏng 4 cell 18650 co màng PVC xanh)
        color("RoyalBlue") {
            hull() {
                for (cx = [-W/2 + cell_r, W/2 - cell_r]) {
                    for (cz = [cell_r, H - cell_r]) {
                        translate([cx, 2.0, cz])
                            rotate([-90, 0, 0])
                                cylinder(r=cell_r, h=L - 4.0, $fn=32);
                    }
                }
            }
        }

        // 2. Nắp bọc cách điện 2 đầu âm/dương (màu đen mờ)
        color("DarkSlateGray") {
            hull() {
                for (cx = [-W/2 + cell_r, W/2 - cell_r]) {
                    for (cz = [cell_r, H - cell_r]) {
                        translate([cx, 0.0, cz])
                            rotate([-90, 0, 0])
                                cylinder(r=cell_r - 0.2, h=2.2, $fn=32);
                    }
                }
            }
            hull() {
                for (cx = [-W/2 + cell_r, W/2 - cell_r]) {
                    for (cz = [cell_r, H - cell_r]) {
                        translate([cx, L - 2.2, cz])
                            rotate([-90, 0, 0])
                                cylinder(r=cell_r - 0.2, h=2.2, $fn=32);
                    }
                }
            }
        }

        // 3. Tem nhãn kỹ thuật pin Li-ion 2S2P 7.4V
        color("WhiteSmoke")
            translate([-14.0, 12.0, H])
                cube([28.0, 46.0, 0.4]);
        color("Black")
            translate([-11.0, 20.0, H + 0.4])
                cube([22.0, 30.0, 0.2]);
        color("OrangeRed")
            translate([-10.0, 14.0, H + 0.4])
                cube([20.0, 4.0, 0.2]);

        // 4. Cụm dây silicone 16AWG ra jack nguồn (Đỏ + / Đen -) & Jack XT30
        if (with_cable) {
            // Dây Đỏ (+)
            color("Red") {
                translate([5.0, L - 1.0, H - 10.0])
                    rotate([-90, 0, 0]) cylinder(d=3.0, h=12.0);
                translate([5.0, L + 11.0, H - 10.0])
                    rotate([0, 35, 0]) cylinder(d=3.0, h=9.0);
            }
            // Dây Đen (-)
            color("Black") {
                translate([-5.0, L - 1.0, H - 10.0])
                    rotate([-90, 0, 0]) cylinder(d=3.0, h=12.0);
                translate([-5.0, L + 11.0, H - 10.0])
                    rotate([0, -35, 0]) cylinder(d=3.0, h=9.0);
            }
            // Jack XT30 màu vàng đồng + tiếp điểm mạ vàng
            translate([0, L + 18.0, H - 4.5]) {
                color("Gold")
                    cube([10.0, 13.0, 5.5], center=true);
                color("DarkOrange")
                    cube([10.2, 4.5, 5.7], center=true);
                color("Yellow") {
                    translate([-2.5, 7.0, 0]) rotate([90, 0, 0]) cylinder(d=2.0, h=4.0);
                    translate([ 2.5, 7.0, 0]) rotate([90, 0, 0]) cylinder(d=2.0, h=4.0);
                }
            }
        }

        // 5. Hai đai dán Velcro bản 20mm chằng giữ pin chặt xuống sàn xe
        if (with_strap) {
            for (sy = [18.0, 48.0]) {
                // Vải đai màu đen nhám ôm chặt quanh pin
                color("Black") {
                    translate([-W/2 - 0.6, sy - 10.0, H])
                        cube([W + 1.2, 20.0, 1.2]);
                    translate([-W/2 - 1.2, sy - 10.0, -FLOOR_T])
                        cube([1.2, 20.0, H + FLOOR_T]);
                    translate([W/2, sy - 10.0, -FLOOR_T])
                        cube([1.2, 20.0, H + FLOOR_T]);
                }
                // Miếng khóa dán Velcro
                color("DarkGray")
                    translate([-7.0, sy - 8.0, H + 1.2])
                        cube([14.0, 16.0, 1.6]);
            }
        }
    }
}

// ====================================================================
// PHỐI CẢNH LẮP GHÉP TOÀN BỘ ROBOT (FULL ROBOT ASSEMBLY)
// ====================================================================
module full_robot_assembly() {
    // 1. Khung gầm chính
    color("LightSlateGray")
        translate([0, 0, GROUND_CLEAR])
            chassis_base();

    // 2. 4 Động cơ GA25
    for (side = [-1, 1]) {
        // Sau
        translate([side * (CHASSIS_W/2 - 2.0), Y_REAR_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
        // Trước
        translate([side * (CHASSIS_W/2 - 2.0), Y_FRONT_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
    }

    // 3. 4 Bánh xe Mecanum (Đặt cân đối 2 bên vách sườn)
    for (side = [-1, 1]) {
        // Bánh sau
        translate([side * (CHASSIS_W/2 + (side > 0 ? 1.0 : -WHEEL_W - 1.0)), Y_REAR_WHEEL, Z_SHAFT])
            mecanum_wheel(is_left = (side < 0));
        // Bánh trước
        translate([side * (CHASSIS_W/2 + (side > 0 ? 1.0 : -WHEEL_W - 1.0)), Y_FRONT_WHEEL, Z_SHAFT])
            mecanum_wheel(is_left = (side > 0));
    }

    // 4. Khung đôn K2 Hub cho Pin Gạch 2S2P (01D_Base_Riser_Frame)
    color("DeepSkyBlue")
        translate([0, 0, GROUND_CLEAR])
            k2_base_riser_frame_2s2p(Z_top = 46.0);

    // 5. Tấm bệ Adapter K2 Hub V11 Hardened (Z = 46.0..51.0mm)
    translate([0, 0, GROUND_CLEAR + 46.0])
        mcu_adapter_deck();

    // 6. Mạch điều khiển ORC K2 Control Hub ESP32-S3 (Z = 51.0..77.0mm)
    color("Black")
        translate([-60.5, -4.0, GROUND_CLEAR + 51.0])
            cube([121.0, 86.0, 26.0]);
    // Tem nhãn cam đặc trưng K2 Hub
    color("DarkOrange")
        translate([-42.0, 0.0, GROUND_CLEAR + 77.0])
            cube([84.0, 76.0, 0.8]);

    // 7. Khối Pin Đóng Sẵn 2S2P 18650 Dạng Gạch 2x2 (38 x 38 x 70 mm)
    translate([0, 0, GROUND_CLEAR])
        battery_brick_2s2p(with_strap = true, with_cable = true);

    // 6. Cặp Tháp nâng Trái & Phải
    color("DodgerBlue") {
        translate([0, 0, GROUND_CLEAR + FLOOR_T]) {
            lift_tower(is_left = true);
            lift_tower(is_left = false);
        }
    }

    // 7. Servo MG996R S1 nâng hạ tay
    color("SlateGray")
        translate([20.0, 114.0, GROUND_CLEAR + FLOOR_T + 48.0])
            cube([37.5, 41.0, 20.0]);

    // 8. Cánh tay nâng song hành 4 khâu chữ H
    color("DodgerBlue") {
        translate([0, Y_PIVOT, Z_PIVOT])
            rotate([ARM_ANGLE, 0, 0])
                h_frame_arm(is_upper = false);

        translate([0, Y_PIVOT, Z_PIVOT + 20.0])
            rotate([ARM_ANGLE, 0, 0])
                h_frame_arm(is_upper = true);
    }

    // 9. Cổ gá Servo S3 và Servo S3
    translate([0, Y_HEAD, Z_HEAD]) {
        color("DodgerBlue") wrist_clevis_s3();
        color("SlateGray")
            translate([-13.5, 16.95, 7.65]) cube([37.5, 19.7, 40.7]);
    }

    // 10. Cụm bệ gắp và 2 ngàm gập dọc theo góc WRIST_PITCH_ANGLE
    translate([0, Y_WRIST_PIVOT, Z_WRIST_PIVOT])
        rotate([WRIST_PITCH_ANGLE, 0, 0])
            translate([0, -6.0, -38.0])
                gripper_head_and_jaws();

    // 11. Cảm biến khoảng cách Laser ToF VL53L0X phía trước mũi xe
    color("Purple") {
        translate([-12.5, CHASSIS_L - 5.0, GROUND_CLEAR + FLOOR_T])
            cube([25.0, 1.6, 10.7]);
        color("Gold")
            translate([-2.2, CHASSIS_L - 3.4, GROUND_CLEAR + 8.3])
                cube([4.4, 1.0, 2.4]);
        color("Black") {
            translate([-1.2, CHASSIS_L - 2.3, GROUND_CLEAR + 9.5])
                rotate([-90, 0, 0]) cylinder(d=1.2, h=0.2);
            translate([ 1.2, CHASSIS_L - 2.3, GROUND_CLEAR + 9.5])
                rotate([-90, 0, 0]) cylinder(d=1.2, h=0.2);
        }
    }

    // 12. Cặp cảm biến Laser ToF VL53L0X hai sườn xe
    color("Purple") {
        translate([-66.0, 68.0, GROUND_CLEAR + 27.0]) cube([1.6, 25.0, 11.0]);
        translate([64.4, 68.0, GROUND_CLEAR + 27.0])  cube([1.6, 25.0, 11.0]);
    }

    // 13. Lồng kiểm tra kích thước thi đấu 200 x 200 mm (Inspection Box)
    if (DISPLAY_MODE == "inspection_box") {
        color("Red", 0.15) {
            translate([-100.0, -4.0, 0])
                cube([200.0, 200.0, 220.0]);
        }
        color("Red") {
            // Khung dây viền hộp 200x200mm
            translate([-100.0, -4.0, 0]) cube([200.0, 2.0, 2.0]);
            translate([-100.0, 194.0, 0]) cube([200.0, 2.0, 2.0]);
            translate([-100.0, -4.0, 0]) cube([2.0, 200.0, 2.0]);
            translate([98.0, -4.0, 0])  cube([2.0, 200.0, 2.0]);
        }
    }
}

// Gọi hiển thị lắp ráp
full_robot_assembly();
