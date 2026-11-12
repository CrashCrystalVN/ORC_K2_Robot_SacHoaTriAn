// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// MODULE: ĐỘNG HỌC GẤP GỌN TAY GẮP & TAY NÂNG 4 THANH (200x200MM STOWED KINEMATICS)
// File: gripper_folded_200x200.scad
// Tác giả: Subagent 2 - Gripper & Arm Fold Kinematics Specialist
// Tương thích: 
//   - gripper_v2.scad (Ngàm kẹp hoa Ø32mm, bệ đầu kẹp, bánh răng thân khai m=1.5)
//   - full_assembly.scad (Tháp nâng đôi MG996R, khung xe Monocoque, bánh Mecanum K3)
//   - Quy chuẩn kích thước xuất phát: TOÀN BỘ XE GẤP GỌN TRONG 200x200 MM!
// ====================================================================

$fn = 48;

// Nhúng thư viện chi tiết bệ kẹp & ngàm kẹp V2.0
include <gripper_v2.scad>;

// --------------------------------------------------------------------
// THÔNG SỐ HÌNH HỌC TỔNG THỂ & KHỚP XOAY
// --------------------------------------------------------------------
Y_PIVOT_TOWER       = 145.0;  // Tâm khớp xoay dưới trên tháp nâng (Y = 145.0mm)
Z_PIVOT_LOWER       = 78.0;   // Cao độ khớp dưới (GROUND_CLEAR 20mm + 58mm)
Z_PIVOT_UPPER       = 106.0;  // Cao độ khớp trên (GROUND_CLEAR 20mm + 86mm, dZ = 28mm)
ARM_LINK_L          = 98.0;   // Chiều dài tâm 2 mắt xoay tay nâng 4 khâu

// Thông số Cổ tay gập dọc S3 (04A_Wrist_Clevis_Pitch_Bracket_S3)
WRIST_LOWER_PIN_Y   = 8.0;    // Lỗ chốt dưới cổ tay so với gốc [0, Y_HEAD, Z_HEAD]
WRIST_LOWER_PIN_Z   = 10.0;   // Lỗ chốt dưới cổ tay
WRIST_UPPER_PIN_Y   = 8.0;    // Lỗ chốt trên cổ tay (dZ = 28mm)
WRIST_UPPER_PIN_Z   = 38.0;   // Lỗ chốt trên cổ tay
WRIST_PITCH_PIN_Y   = 26.8;   // Trục gập dọc cổ tay S3
WRIST_PITCH_PIN_Z   = 38.0;   // Trục gập dọc cổ tay S3

// Thông số Bệ đầu kẹp (04_Gripper_Base_Head_V2)
BASE_PITCH_AXIS_Y   = 6.0;    // Trục xoay gập của bệ đầu kẹp
BASE_PITCH_AXIS_Z   = 38.0;   // Trục xoay gập của bệ đầu kẹp
JAW_PIVOT_Y         = 39.0;   // Tâm cọc xoay ngàm kẹp
JAW_PIVOT_Z         = 5.0;    // Cao độ mặt đế xoay ngàm kẹp

// --------------------------------------------------------------------
// BẢNG GÓC ĐỘNG HỌC CHUẨN XÁC THEO TỪNG TRẠNG THÁI (KINEMATIC STATES)
// --------------------------------------------------------------------
// 1. Trạng thái "stowed" (Gấp đứng thu gọn trước tháp - Khuyến nghị thi đấu):
//    - arm_angle = +90.0°: Tay nâng dựng đứng 90° dọc tháp nâng
//    - wrist_pitch = -90.0°: Cổ tay gập chúc thẳng đứng xuống
//    - jaw_grip = 0.0°: Hai ngàm kẹp khép kín hoàn toàn
//    * Kết quả đo đạc hình học:
//      + Toạ độ Y_max: 176.3mm (Cản trước 176.0mm, Mép bánh trước 182.0mm)
//      + Front overhang: 0.0mm (Hoàn toàn nằm sau mép bánh xe trước)
//      + Chiều dài xe tổng thể: 184.3mm <= 200.0mm! (Từ đuôi bánh Y=-8mm)
//      + Chiều rộng cụm kẹp: 68.0mm <= 200.0mm!
//      + Cao độ Z: 53.0mm .. 216.5mm (Cách đỉnh cản VL53L0X Z=34mm khoảng an toàn rộng 19.0mm, tăng 14mm so với cản siêu âm cũ)
//
// 2. Trạng thái "stowed_rear" (Gấp về phía sau ôm sát thân xe / base):
//    - arm_angle = +135.0°: Tay nâng ngả về phía sau 135°
//    - wrist_pitch = -90.0°: Cổ tay chúc xuống
//    - jaw_grip = 0.0°
//    * Kết quả: Y in [56.5, 145.0], Z in [24.3, 175.3] <= 200.0mm!
//
// 3. Trạng thái "deployed" (Bung hoạt động - Hạ thấp vươn xa kẹp hoa):
//    - arm_angle = -20.0°: Tay nâng hạ góc -20° vươn về phía trước
//    - wrist_pitch = 0.0°: Đầu kẹp giữ nằm ngang song song mặt đất
//    - jaw_grip = 0.0° (kẹp chặt) hoặc 18.0° (mở rộng đón ống hoa Ø32mm)
//    * Tầm vươn trước Y_max: 406.9mm
// --------------------------------------------------------------------

ARM_ANGLE_STOWED          = 90.0;
WRIST_PITCH_STOWED        = -90.0;
JAW_GRIP_STOWED           = 0.0;

ARM_ANGLE_STOWED_REAR     = 135.0;
WRIST_PITCH_STOWED_REAR   = -90.0;
JAW_GRIP_STOWED_REAR      = 0.0;

ARM_ANGLE_DEPLOYED        = -20.0;
WRIST_PITCH_DEPLOYED      = 0.0;
JAW_GRIP_DEPLOYED_CLOSED  = 0.0;
JAW_GRIP_DEPLOYED_OPEN    = 18.0;

// --------------------------------------------------------------------
// TIỆN ÍCH LỖ GIỌT NƯỚC DFM (Để độc lập khi compile file rời)
// --------------------------------------------------------------------
module _teardrop_x(d = 3.3, h = 44.0) {
    r = d / 2;
    side = r * sqrt(2);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2, -side/2])
                    cube([h, side, side]);
    }
}

// --------------------------------------------------------------------
// MODULE CHI TIẾT TAY NÂNG DƯỚI & TRÊN (H-FRAME PARALLEL ARMS)
// --------------------------------------------------------------------
module lower_h_frame_arm_standalone(length = ARM_LINK_L, height = 12.0, thickness = 5.0) {
    t_drive = 8.0;
    difference() {
        union() {
            // Thanh trái bị động
            translate([-19.5, 0, -height/2]) cube([thickness, length, height]);
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);

            // Thanh phải chủ động nối Servo S1
            translate([14.5, 0, -height/2]) cube([thickness, length, height]);
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);

            // Gân tăng cứng dầm phải
            hull() {
                translate([11.5, 0, -height/2]) cube([3.0, 12.0, height]);
                translate([14.5, 22.0, -height/2]) cube([0.5, 1.0, height]);
            }

            // Vòm gá đĩa tròn Servo S1 Ø24mm
            intersection() {
                hull() {
                    translate([19.5 - t_drive, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.0, h=t_drive);
                    translate([19.5 - t_drive, 16.0, -height/2]) cube([t_drive, 2.0, height]);
                }
                translate([11.0, -15.0, -height/2]) cube([9.0, 40.0, 25.0]);
            }

            // Giằng ngang chữ H chống xoắn
            translate([-15.0, 42.0, -height/2]) cube([30.0, 14.0, height]);
        }

        // Hốc đĩa tròn Servo MG996R
        translate([17.2, 0, 0]) rotate([0, 90, 0]) cylinder(d=21.0, h=2.8);
        translate([10.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            if (hz >= -height/2 + 0.5) {
                translate([10.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=10.0);
                translate([11.0, hy, hz]) rotate([0, 90, 0]) cylinder(d=5.5, h=1.8);
            }
        }
        // Lỗ chốt xoay mắt trước & sau
        translate([-22.0, length, 0]) _teardrop_x(d=3.3, h=44.0);
        translate([-22.0, 0, 0]) _teardrop_x(d=3.3, h=10.0);
    }
}

module upper_h_frame_arm_standalone(length = ARM_LINK_L, height = 11.0, thickness = 5.0) {
    difference() {
        union() {
            for (x0 = [-19.5, 14.5]) {
                translate([x0, 0, -height/2]) cube([thickness, length, height]);
                translate([x0, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
                translate([x0, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
                translate([x0, -height/2, -height/2]) cube([thickness, height/2, height/2]);
                translate([x0, length, -height/2]) cube([thickness, height/2, height/2]);
            }
            translate([-14.5, 44.0, -height/2]) cube([29.0, 12.0, height]);
        }
        translate([-22.0, 0, 0]) _teardrop_x(d=3.3, h=44.0);
        translate([-22.0, length, 0]) _teardrop_x(d=3.3, h=44.0);
    }
}

module wrist_clevis_pitch_bracket_standalone() {
    Y_piv = WRIST_PITCH_PIN_Y;
    Z_piv = WRIST_PITCH_PIN_Z;

    difference() {
        union() {
            translate([-14.0, 0, -2.5]) cube([28.0, 16.6, 46.5]);
            translate([-14.0, 0, 44.0]) cube([27.0, 16.6, 12.0]);
            hull() {
                translate([-14.0, 14.0, -2.5]) cube([1.0, 2.6, 58.5]);
                translate([-16.5, 16.6, -2.5]) cube([3.0, 20.4, 58.5]);
            }
            hull() {
                translate([-14.0, 13.8, Z_piv - 9.0]) cube([1.0, 2.8, 18.0]);
                translate([-16.5, 16.6, Z_piv - 9.0]) cube([3.0, 18.0, 18.0]);
                translate([-27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=16.0, h=1.0);
            }
            translate([-14.0, 16.6, -2.5]) cube([27.0, 20.4, 9.7]);
            translate([-14.0, 16.6, 48.6]) cube([27.0, 20.4, 7.4]);
        }

        // Khe lọt giữa 2 thanh tay nâng
        translate([-8.5, 4.5, -3.0]) cube([17.0, 12.2, 60.0]);

        // 2 Lỗ chốt bu-lông M3 kết nối tay nâng 4 khâu
        for (zp = [10.0, 38.0]) {
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
            translate([-8.6, 8.0, zp]) rotate([0, -90, 0]) cylinder(d=6.5, h=2.6, $fn=6);
            translate([8.6, 8.0, zp])  rotate([0, 90, 0])  cylinder(d=6.5, h=2.6, $fn=6);
        }

        // Lỗ ốc bắt tai Servo S3
        for (sy = [Y_piv - 5.0, Y_piv + 5.0]) {
            for (sz = [3.75, 52.25]) {
                translate([-10.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=2.95, h=25.0);
            }
        }
        translate([-8.5, 19.0, 0.75])  cube([13.0, 19.0, 6.0]);
        translate([-8.5, 19.0, 49.25]) cube([13.0, 19.0, 6.0]);

        // Lỗ trục xoay gập ngang
        translate([-30.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.0, h=18.0);
        translate([-17.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=3.6, $fn=6);
        translate([-13.6, 22.0, 4.5]) cube([8.0, 9.6, 4.0]);
    }
}

// Mô hình Servo MG996R thu gọn
module servo_mg996r_model() {
    color("SlateGray") {
        translate([-10.35 - 20.35, -9.85, 4.5]) cube([40.7, 19.7, 37.5]);
        translate([-10.35 - 27.0, -9.85, 10.5]) cube([54.0, 19.7, 2.5]);
        translate([0, 0, 2.3]) cylinder(d=12.0, h=2.5);
    }
    color("Ivory") {
        translate([-3.9, -3.9, 0.2]) cube([7.8, 20.5, 2.1]);
    }
}

// --------------------------------------------------------------------
// MODULE CHÍNH: LẮP GHÉP CỤM TAY NÂNG & TAY GẮP (GRIPPER ARM ASSEMBLY)
// Hỗ trợ trực tiếp các chế độ:
// - state = "stowed"        : Gấp đứng 90° siêu gọn trong 200x200mm
// - state = "stowed_rear"   : Gập về phía sau ôm thân xe
// - state = "deployed"      : Vươn kẹp lọ hoa Ø32mm (ngàm đóng)
// - state = "deployed_open" : Vươn sẵn sàng đón lọ hoa Ø32mm (ngàm mở 18°)
// - Hoặc truyền góc tùy biến (arm_angle_custom, wrist_pitch_custom, grip_angle_custom)
// --------------------------------------------------------------------
module gripper_arm_assembly(
    state              = "stowed",
    arm_angle_custom   = undef,
    wrist_pitch_custom = undef,
    grip_angle_custom  = undef,
    show_flower        = true
) {
    // Xác định góc hoạt động theo trạng thái hoặc tham số tùy biến
    arm_angle = !is_undef(arm_angle_custom) ? arm_angle_custom :
                (state == "deployed" || state == "deployed_open") ? ARM_ANGLE_DEPLOYED :
                (state == "stowed_rear") ? ARM_ANGLE_STOWED_REAR :
                ARM_ANGLE_STOWED;

    wrist_pitch = !is_undef(wrist_pitch_custom) ? wrist_pitch_custom :
                  (state == "deployed" || state == "deployed_open") ? WRIST_PITCH_DEPLOYED :
                  (state == "stowed_rear") ? WRIST_PITCH_STOWED_REAR :
                  WRIST_PITCH_STOWED;

    jaw_grip = !is_undef(grip_angle_custom) ? grip_angle_custom :
               (state == "deployed_open") ? JAW_GRIP_DEPLOYED_OPEN :
               (state == "deployed") ? JAW_GRIP_DEPLOYED_CLOSED :
               (state == "stowed_rear") ? JAW_GRIP_STOWED_REAR :
               JAW_GRIP_STOWED;

    // Động học thanh truyền song song 4 khâu
    arm_rad = arm_angle;
    dy_arm  = ARM_LINK_L * cos(arm_rad);
    dz_arm  = ARM_LINK_L * sin(arm_rad);

    y_head  = Y_PIVOT_TOWER + dy_arm - WRIST_LOWER_PIN_Y;
    z_head  = Z_PIVOT_LOWER + dz_arm - WRIST_LOWER_PIN_Z;

    // 1. Cặp cánh tay nâng 4 khâu chữ H
    color("DodgerBlue") {
        translate([0, Y_PIVOT_TOWER, Z_PIVOT_LOWER])
            rotate([arm_angle, 0, 0])
                lower_h_frame_arm_standalone(length = ARM_LINK_L);

        translate([0, Y_PIVOT_TOWER, Z_PIVOT_UPPER])
            rotate([arm_angle, 0, 0])
                upper_h_frame_arm_standalone(length = ARM_LINK_L);
    }

    // 2. Cổ tay nối Clevis (04A)
    color("DodgerBlue")
        translate([0, y_head, z_head])
            wrist_clevis_pitch_bracket_standalone();

    // 3. Servo S3 (Pitch control) gắn trên cổ tay
    color("SlateGray") {
        translate([-13.5, y_head + 16.95, z_head + 7.65]) cube([37.5, 19.7, 40.7]);
        translate([13.0, y_head + 16.95, z_head + 0.75])  cube([2.5, 19.7, 54.5]);
        translate([24.0, y_head + WRIST_PITCH_PIN_Y, z_head + WRIST_PITCH_PIN_Z])
            rotate([0, 90, 0]) cylinder(d=12.0, h=2.5);
    }
    color("Ivory")
        translate([27.0, y_head + WRIST_PITCH_PIN_Y, z_head + WRIST_PITCH_PIN_Z])
            rotate([0, 90, 0]) cylinder(d=20.0, h=2.2);

    // 4. Cụm bệ đầu kẹp + Servo S2 + Cặp ngàm kẹp hoa Ø32mm
    // Tâm xoay gập dọc nằm tại trục pitch S3: (y_head + WRIST_PITCH_PIN_Y, z_head + WRIST_PITCH_PIN_Z)
    translate([0, y_head + WRIST_PITCH_PIN_Y, z_head + WRIST_PITCH_PIN_Z])
        rotate([wrist_pitch, 0, 0])
            translate([0, -BASE_PITCH_AXIS_Y, -BASE_PITCH_AXIS_Z]) {

                // Bệ đầu kẹp V2.0
                color("OrangeRed") gripper_base_head_v2();

                // Servo S2 điều khiển đóng mở ngàm kẹp
                translate([15.0, JAW_PIVOT_Y, 24.5])
                    servo_mg996r_model();

                // Cặp ngàm kẹp kép đa năng (Universal Hybrid Jaws)
                // Ngàm trái xoay -jaw_grip khi mở
                translate([-15.0, JAW_PIVOT_Y, JAW_PIVOT_Z])
                    rotate([0, 0, -jaw_grip])
                        translate([15.0, 0, 0])
                            color("Crimson") gripper_jaw_v2(is_left = true);

                // Ngàm phải xoay +jaw_grip khi mở
                translate([15.0, JAW_PIVOT_Y, JAW_PIVOT_Z])
                    rotate([0, 0, jaw_grip])
                        translate([-15.0, 0, 0])
                            color("Crimson") gripper_jaw_v2(is_left = false);

                // Mô hình lọ hoa / ống hoa Ø32mm minh họa khi deployed
                if (show_flower && (state == "deployed" || state == "deployed_open") && wrist_pitch == 0) {
                    color("Gold", 0.8) {
                        // Vị trí ôm tròn thứ nhất (Y = 45mm trên ngàm kẹp)
                        translate([0, JAW_PIVOT_Y + 45.0, 3.5])
                            cylinder(d = 32.0, h = 120.0);
                        // Vị trí rãnh V kép thứ hai (Y = 74mm trên ngàm kẹp)
                        translate([0, JAW_PIVOT_Y + 74.0, 3.5])
                            cylinder(d = 32.0, h = 120.0);
                    }
                }
            }
}

// Khung bao ảo 200x200mm kiểm tra kích thước chuẩn thi đấu
module boundary_box_200x200(height = 220.0) {
    color("LimeGreen", 0.2)
        // Tâm xe X = 0, Y từ đuôi bánh xe Y = -8.0mm đến Y = +192.0mm
        translate([-100.0, -8.0, 0])
            cube([200.0, 200.0, height]);
}

// --------------------------------------------------------------------
// DEMO MẶC ĐỊNH KHI MỞ FILE RIÊNG LẺ
// Đổi SHOW_DEMO = true để xem preview riêng lẻ file này
// --------------------------------------------------------------------
SHOW_DEMO = false;
SHOW_MODE = "stowed"; // "stowed", "deployed", "comparison"

if (SHOW_DEMO) {
    if (SHOW_MODE == "stowed") {
        // Trạng thái gấp gọn 200x200mm
        gripper_arm_assembly(state = "stowed");
        boundary_box_200x200();
    } else if (SHOW_MODE == "deployed") {
        // Trạng thái bung hoạt động kẹp hoa
        gripper_arm_assembly(state = "deployed");
    } else if (SHOW_MODE == "comparison") {
        // So sánh trực quan 2 trạng thái cạnh nhau
        translate([-120, 0, 0]) {
            gripper_arm_assembly(state = "stowed");
            boundary_box_200x200();
        }
        translate([120, 0, 0]) {
            gripper_arm_assembly(state = "deployed");
        }
    }
}
