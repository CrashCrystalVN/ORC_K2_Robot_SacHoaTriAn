    // ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// BẢN THIẾT KẾ HIỆN ĐẠI TỐI ƯU CƠ KHÍ & IN 3D: ORC-X1 PRO DFM (V4.0 - ZERO SUPPORT & 100% FLAT BED)
// ====================================================================
// CẢI TIẾN DFM V4.0 THUẬN LỢI TỐI ĐA ĐỂ IN 3D:
// 1. Mặt đáy khung gầm phẳng tuyệt đối 100% tại Z = 0.0 mm (Tách rời Đế đệm cảm biến dò line 01E).
// 2. Tách 2 Tháp nâng (01B & 01C) và Bệ MCU (01D) thành mô-đun in nằm phẳng 100% trên mặt bàn in:
//    - In 0% Support cho toàn bộ robot!
//    - Thớ nhựa chạy dọc suốt chiều dài tháp nâng -> Chống gãy tách lớp gấp 5 lần!
//    - Tất cả lỗ ngang trên khung gầm đều vát đỉnh Giọt nước 45° (Teardrop Holes) tự đỡ khi in FDM.
// 3. Khung tay nâng chữ H (03 & 03B) phẳng đáy 100% (khắc phục lỗi kênh 4mm do đĩa horn_boss).
// 4. Bệ đầu kẹp hoa (04) loại bỏ cầu ngang treo lơ lửng -> In 0% Support & lắp hàm kẹp từ trên xuống cực dễ!
// ====================================================================

$fn = 48;

// CHỌN CHẾ ĐỘ HIỂN THỊ:
// "assembly"     = Phối cảnh lắp ghép hoàn chỉnh Robot ORC-X1 PRO V4.0
// "print_plates" = Bố cục trải phẳng 100% các chi tiết trên mặt bàn in (Z = 0.0 mm, Zero Support)
DISPLAY_MODE   = "assembly";

// THÔNG SỐ TỔNG THỂ (CHUẨN HÓA BỘ KIT ORC OHSTEM K2 V4.0)
TOTAL_WIDTH    = 218.0;   // Bề rộng phủ bì bánh xe (khe hở an toàn 15mm mỗi bên trong mê cung 248mm)
TOTAL_LENGTH   = 176.0;   // Chiều dài khung gầm xe (22 x 8mm chuẩn OhStem)
CHASSIS_W      = 136.0;   // Bề rộng khung xe (17 x 8mm, lọt lòng 128mm -> 2 motor cách nhau 20-32mm!)
CHASSIS_L      = 176.0;   // Chiều dài sàn xe
GROUND_CLEAR   = 20.0;    // Khoảng sáng gầm xe 20.0 mm
FLOOR_T        = 4.0;     // Độ dày sàn xe chịu lực

WHEEL_D        = 80.0;    // Đường kính bánh xe Mecanum K3 (Ø80.0 mm)
WHEEL_W        = 38.0;    // Bề dày bánh xe Mecanum K3 (38.0 mm)
Z_SHAFT        = 40.0;    // Cao độ tâm trục bánh xe (Z = 40.0 mm)

// CHỌN TRẠNG THÁI TAY GẮP:
// "stowed"   = Gấp gọn tối ưu trong kích thước 200x200mm (Chuẩn thi đấu xuất phát)
// "deployed" = Bung vươn dài hoạt động kẹp hoa Ø32mm
ARM_STATE      = "stowed"; 

// THÔNG SỐ ĐỘNG HỌC CÁNH TAY SONG HÀNH 4 KHÂU CHỮ H
Y_PIVOT        = 145.0;   // Tâm khớp xoay trên tháp nâng (Y in [105, 166])
ARM_L          = 98.0;    // Chiều dài tâm 2 mắt xoay
ARM_ANGLE      = (ARM_STATE == "stowed") ? 90.0 : -20.0;
DY_ARM         = ARM_L * cos(ARM_ANGLE);  // 90°: 0.0mm; -20°: 92.09mm
DZ_ARM         = ARM_L * sin(ARM_ANGLE);  // 90°: 98.0mm; -20°: -33.52mm
Y_HEAD         = Y_PIVOT + DY_ARM - 8.0;  // 90°: 137.0mm; -20°: 229.09mm
Z_HEAD         = 78.0 + DZ_ARM - 10.0;    // 90°: 166.0mm; -20°: 34.48mm
WRIST_PITCH_ANGLE = (ARM_STATE == "stowed") ? -90.0 : 0.0; // -90.0° = Gập đứng chúc xuống siêu gọn trong 200x200mm; 0.0° = Hạ ngang kẹp hoa!
JAW_GRIP_ANGLE    = (ARM_STATE == "stowed") ? 0.0 : 0.0;   // 0.0° khép ngàm kẹp, 18.0° mở rộng đón hoa

// ====================================================================
// TIỆN ÍCH LỖ GIỌT NƯỚC 45° TỰ ĐỠ KHI IN 3D (DFM TEARDROP HOLES)
// ====================================================================
module teardrop_hole_x(d = 9.0, h = 10.0) {
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

module teardrop_hole_y(d = 16.6, h = 15.0) {
    r = d / 2;
    side = r * sqrt(2);
    union() {
        rotate([-90, 0, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([0, 45, 0])
                translate([-side/2, 0, -side/2])
                    cube([side, h, side]);
    }
}

// ====================================================================
// 1A. KHUNG GẦM CHÍNH ĐÁY PHẲNG 100% (01_Monocoque_Chassis_GA25_Mecanum)
// ====================================================================
module monocoque_chassis_dfm() {
    difference() {
        union() {
            // 1. Sàn đáy chính phẳng tuyệt đối 100% tại Z = 0.0 mm
            translate([-CHASSIS_W/2, 0, 0])
                cube([CHASSIS_W, CHASSIS_L, FLOOR_T]);

            // 2. Hai vách sườn chịu lực & mặt bích động cơ dày 4.0 mm, cao 30.0 mm
            translate([-CHASSIS_W/2, 0, 0])
                cube([4.0, CHASSIS_L, 30.0]);
            translate([CHASSIS_W/2 - 4.0, 0, 0])
                cube([4.0, CHASSIS_L, 30.0]);

            // 3. 4 Ổ đỡ nửa dưới động cơ GA25
            for (my = [32.0, 142.0]) {
                translate([-CHASSIS_W/2, my - 22.0, 0])
                    cube([38.0, 44.0, 20.0]);
                translate([CHASSIS_W/2 - 38.0, my - 22.0, 0])
                    cube([38.0, 44.0, 20.0]);
                translate([-CHASSIS_W/2, my - 16.0, 0])
                    cube([4.0, 32.0, 33.0]);
                translate([CHASSIS_W/2 - 4.0, my - 16.0, 0])
                    cube([4.0, 32.0, 33.0]);
            }

            // 4. 4 Gờ định vị thấp 3mm giữ Pin Li-ion 2S 18650
            for (bx = [-21.5, 18.5]) {
                for (by = [52.0, 90.0]) {
                    translate([bx, by, FLOOR_T]) cube([3.0, 8.0, 3.0]);
                }
            }

            // 5. 4 Trụ đỡ Bệ MCU (10 x 10 x 18 mm, Z = 4.0..22.0 mm) - Đỉnh phẳng để bắt Bệ MCU rời
            for (px = [-38.0, 28.0]) {
                for (py = [44.0, 94.0]) {
                    translate([px, py, FLOOR_T]) cube([10.0, 10.0, 18.0]);
                }
            }

            // 6A & 6B. Bệ gá Mạch nhận PS4 I2C (Trái) & Nút nhấn đôi (Phải)
            translate([-CHASSIS_W/2, 56.0, 0])
                cube([16.0, 26.0, 16.0]);
            translate([CHASSIS_W/2 - 16.0, 56.0, 0])
                cube([16.0, 26.0, 16.0]);

            // 7. Mũi cản trước bảo vệ & gá Cảm biến khoảng cách Siêu âm OhStem
            translate([-34.0, CHASSIS_L - 10.0, 0])
                cube([68.0, 10.0, 28.0]);
            translate([-26.0, CHASSIS_L - 16.0, 0])
                cube([52.0, 6.0, 10.0]);

            // 8. Gờ định vị chân Tháp Nâng Rời Trái & Phải
            translate([-30.0, 105.0, FLOOR_T]) cube([2.0, 14.5, 4.0]);
            translate([28.0, 105.0, FLOOR_T])  cube([2.0, 14.5, 4.0]);
            translate([-28.0, 102.5, FLOOR_T]) cube([16.0, 2.5, 4.0]);
            translate([12.0, 102.5, FLOOR_T])  cube([16.0, 2.5, 4.0]);
        }

        // --- KHOÉT LỖ ĐỘNG CƠ GA25 & MẶT BÍCH GIỌT NƯỚC 45° ---
        for (my = [32.0, 142.0]) {
            translate([-CHASSIS_W/2 + 4.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=25.4, h=36.0);
            translate([-CHASSIS_W/2 - 1.0, my, 20.0])
                teardrop_hole_x(d=9.0, h=6.0);
            for (a = [0, 90, 180, 270]) {
                translate([-CHASSIS_W/2 - 1.0, my + 8.5*cos(a), 20.0 + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=6.0);
            }

            translate([CHASSIS_W/2 - 40.0, my, 20.0])
                rotate([0, 90, 0]) cylinder(d=25.4, h=36.0);
            translate([CHASSIS_W/2 - 5.0, my, 20.0])
                teardrop_hole_x(d=9.0, h=6.0);
            for (a = [0, 90, 180, 270]) {
                translate([CHASSIS_W/2 - 5.0, my + 8.5*cos(a), 20.0 + 8.5*sin(a)])
                    teardrop_hole_x(d=3.3, h=6.0);
            }

            for (dy = [-17.5, 17.5]) {
                translate([-44.0, my + dy, 3.0]) cylinder(d=3.0, h=18.0);
                translate([44.0, my + dy, 3.0]) cylinder(d=3.0, h=18.0);
            }
        }

        // 4 Lỗ ốc M3 trên đỉnh 4 Trụ đỡ Bệ MCU
        for (px = [-33.0, 33.0]) {
            for (py = [49.0, 99.0]) {
                translate([px, py, 4.0]) cylinder(d=3.0, h=19.0);
            }
        }

        // 10 Lỗ bu-lông M3 bắt cứng 2 Tháp Nâng Rời Trái & Phải
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

        // Lỗ bắt Mạch nhận I2C sườn trái & Nút nhấn đôi sườn phải
        translate([-CHASSIS_W/2 + 9.0, 61.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2 + 9.0, 77.0, 4.0]) cylinder(d=4.2, h=14.0);
        translate([-CHASSIS_W/2 + 4.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        translate([CHASSIS_W/2 - 9.0, 61.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2 - 9.0, 77.0, 4.0]) cylinder(d=3.4, h=14.0);
        translate([CHASSIS_W/2 - 17.0, 58.0, 6.0]) cube([13.0, 22.0, 4.0]);

        // Ma trận lỗ ốc M3 dự phòng trên sàn xe
        for (ex = [-50.0, -42.0, 42.0, 50.0]) {
            for (ey = [88.0, 104.0, 114.0]) {
                translate([ex, ey, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
            }
        }
        for (ex = [-8.0, 0.0, 8.0]) {
            for (ey = [112.0, 128.0]) {
                translate([ex, ey, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
            }
        }
        for (ex = [-16.0, 0.0, 16.0]) {
            for (ey = [8.0, 48.0, 64.0, 80.0, 96.0]) {
                translate([ex, ey, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
            }
        }

        // Lỗ ốc M3 & Rãnh cáp Grove tại mũi xe bắt Đế đệm Cảm biến dò line
        for (lx = [-16.0, -12.0, -8.0, 8.0, 12.0, 16.0]) {
            translate([lx, 160.0, -0.5]) cylinder(d=3.2, h=FLOOR_T + 1.0);
        }
        translate([-8.0, 146.0, -0.5]) cube([16.0, 8.0, FLOOR_T + 1.0]);

        // 2 Mắt cảm biến siêu âm OhStem Ø16.6mm (biên dạng Giọt nước 45° tự đỡ)
        translate([-13.0, CHASSIS_L - 11.0, 14.0]) teardrop_hole_y(d=16.6, h=15.0);
        translate([13.0, CHASSIS_L - 11.0, 14.0])  teardrop_hole_y(d=16.6, h=15.0);
        translate([-24.4, CHASSIS_L - 10.5, 4.0])  cube([48.8, 3.5, 22.0]);
        translate([-8.0, CHASSIS_L - 13.0, -0.5])  cylinder(d=3.2, h=12.0);
        translate([8.0, CHASSIS_L - 13.0, -0.5])   cylinder(d=3.2, h=12.0);
        translate([-21.0, CHASSIS_L - 11.0, 14.0]) teardrop_hole_y(d=3.2, h=15.0);
        translate([21.0, CHASSIS_L - 11.0, 14.0])  teardrop_hole_y(d=3.2, h=15.0);

        // Rãnh luồn dây điện & 4 Khe dây rút giữ Pin
        translate([-12.0, 18.0, -0.5]) cube([24.0, 22.0, FLOOR_T + 1.0]);
        for (zx = [-24.0, 20.0]) {
            for (zy = [56.0, 86.0]) {
                translate([zx, zy, -0.5]) cube([4.0, 8.0, FLOOR_T + 1.0]);
            }
        }
    }
}

// ====================================================================
// 1B & 1C. CẶP THÁP NÂNG CÁNH TAY RỜI IN PHẲNG 100% (01B & 01C)
// ====================================================================
module lift_tower_dfm(is_left = true) {
    x_wall_min = is_left ? -28.0 : 20.0;
    x_flange_min = is_left ? -20.0 : 12.0;
    brace_x0 = is_left ? -20.0 : 0.0;
    fx = is_left ? -16.0 : 16.0;
    wx = is_left ? -24.0 : 24.0;

    difference() {
        union() {
            // Tấm vách tháp chính dày 8.0 mm (Mặt ngoài tại X = ±28.0 phẳng tuyệt đối 100% để đặt nằm in!)
            translate([x_wall_min, 105.0, 4.0]) cube([8.0, 61.0, 90.0]);
            // 2 Đế chữ L dưới chân (chân sau & chân trước)
            translate([x_flange_min, 105.0, 4.0]) cube([8.0, 22.5, 8.0]);
            translate([x_flange_min, 154.5, 4.0]) cube([8.0, 11.5, 8.0]);
            // Tai giằng ngang đỉnh tháp
            translate([brace_x0, 105.0, 88.0]) cube([20.0, 13.0, 6.0]);
        }

        // Vòm cổng dưới chân tháp
        translate([-30.0, 127.5, 3.5]) cube([60.0, 27.0, 30.5]);

        if (!is_left) {
            // Hốc chữ nhật lắp Servo MG996R (41.2 x 20.2 mm)
            translate([19.0, 114.05, 47.9]) cube([10.0, 41.2, 20.2]);
            // 4 Lỗ ốc M3 bắt Servo MG996R có HỐC CHÌM TÁN M3 LỤC GIÁC Ở MẶT TRONG:
            for (sy = [134.65 - 24.25, 134.65 + 24.25]) {
                for (sz = [58.0 - 5.0, 58.0 + 5.0]) {
                    translate([19.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
                    translate([19.9, sy, sz]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.8, $fn=6);
                }
            }
            // Khe lượn mở rộng (Clearance Pocket) sâu 1.0mm ở mặt trong X in [20.0, 21.0] dọc hành trình quay:
            translate([19.9, 138.0, 44.0]) cube([1.2, 28.0, 30.0]);
        } else {
            // Ô thoáng giảm trọng lượng trên Tháp Trái
            translate([-29.0, 114.05, 47.9]) cube([10.0, 22.0, 20.2]);
            translate([-30.0, 145.0, 58.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=12.0);
        }

        // Lỗ chốt xoay trên (Y = 145.0, Z = 86.0)
        translate([-30.0, 145.0, 86.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);

        // Lỗ bu-lông M3 bắt xuống sàn khung gầm
        for (sy = [110.5, 122.0, 160.25]) {
            translate([fx, sy, 3.5]) cylinder(d=3.3, h=10.0);
        }
        for (sy = [116.0, 160.25]) {
            translate([wx, sy, 3.5]) cylinder(d=3.0, h=14.0);
        }
    }
}

// ====================================================================
// TIỆN ÍCH HỆ RÃNH ĐƯỜNG RAY TÁN M3 "BLIND-FLOOR CAPTIVE" V9.0 (ĐÁY KÍN CHỐNG RƠI + KHÓA 6 CẠNH CHỐNG XOAY)
// ====================================================================
module slot_m3_with_nut_channel_z0(x1, y1, x2, y2, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    len_xy = sqrt(dx*dx + dy*dy);
    cx = (x1 + x2) / 2.0;
    cy = (y1 + y2) / 2.0;
    hull() {
        translate([x1, y1, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }
    hull() {
        translate([x1, y1, 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.25);
        translate([x2, y2, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.25);
    }
    if (len_xy >= 12.0) {
        translate([cx, cy, -0.5])
            cylinder(d=nut_w + 0.55, h=4.4);
    }
}

module slot_m3_with_nut_channel_zbot(x1, y1, x2, y2, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    len_xy = sqrt(dx*dx + dy*dy);
    cx = (x1 + x2) / 2.0;
    cy = (y1 + y2) / 2.0;
    hull() {
        translate([x1, y1, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }
    hull() {
        translate([x1, y1, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.25);
        translate([x2, y2, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.25);
    }
    if (len_xy >= 12.0) {
        translate([cx, cy, Z_bot - 0.5])
            cylinder(d=nut_w + 0.55, h=4.4);
    }
}

module side_nut_entry_port_z0(sx, y_pos, T_deck = 6.0, nut_w = 5.8) {
    hull() {
        translate([sx * 54.0, y_pos, 1.15]) cylinder(d=nut_w, h=2.8);
        translate([sx * 62.0, y_pos, 1.15]) cylinder(d=nut_w, h=2.8);
    }
    hull() {
        translate([sx * 54.0, y_pos, 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
        translate([sx * 62.0, y_pos, 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
    }
}

module side_nut_entry_port_zbot(sx, y_pos, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.8) {
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 1.15]) cylinder(d=nut_w, h=2.8);
        translate([sx * 62.0, y_pos, Z_bot + 1.15]) cylinder(d=nut_w, h=2.8);
    }
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
        translate([sx * 62.0, y_pos, Z_bot + 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
    }
}

module slot_m3_counterbored_top(x1, y1, x2, y2, Z_base = 0.0, T_deck = 6.0, cb_d = 6.8, cb_h = 2.0, slot_d = 3.4) {
    hull() {
        translate([x1, y1, Z_base - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, Z_base - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }
    hull() {
        translate([x1, y1, Z_base + T_deck - cb_h]) cylinder(d=cb_d, h=cb_h + 1.0);
        translate([x2, y2, Z_base + T_deck - cb_h]) cylinder(d=cb_d, h=cb_h + 1.0);
    }
}

// ====================================================================
// CỤM GÁ CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X ĐO TƯỜNG GIẢI MÊ CUNG V10.0
// - Đặt ở sườn Trái (sx = -1) và sườn Phải (sx = +1) tại Y in [66.0, 82.5mm]
// - Nằm trọn vẹn trong khoảng hở giữa 2 bánh Mecanum (Y = 72..102mm)
// - Bề ngang giới hạn tại |X| <= 68.8mm -> Cách mặt trong bánh xe Mecanum (|X|=71.0mm) > 2.2mm!
// - Tích hợp ngàm cài snap-fit giữ PCB VL53L0X (25 x 11mm) + Cửa sổ bắn laser 90° sườn & lỗ ốc M2.5/M3
// ====================================================================
module vl53l0x_maze_sensor_pod(is_left = true, T_deck = 6.0, Z_base = 0.0) {
    sx = is_left ? -1 : 1;
    difference() {
        union() {
            hull() {
                translate([sx * 60.0, 66.0, Z_base]) cube([sx * 0.1, 16.5, T_deck]);
                translate([sx * 68.2, 67.5, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 68.2, 81.0, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 60.0, 82.5, Z_base]) cube([sx * 0.1, 0.1, T_deck]);
            }
            for (py = [70.0, 78.5]) {
                translate([sx * 68.6, py - 2.2, Z_base])
                    cube([sx * 1.8, 4.4, T_deck + 6.0]);
                translate([sx * 68.6, py - 2.2, Z_base + T_deck + 4.5])
                    hull() {
                        cube([sx * 1.8, 4.4, 1.5]);
                        translate([-sx * 1.0, 0, 0]) cube([sx * 0.1, 4.4, 1.0]);
                    }
            }
            translate([sx * 66.2, 68.0, Z_base])
                cube([sx * 1.4, 13.0, T_deck + 5.5]);
        }
        translate([sx * 67.6, 67.5, Z_base + 1.5])
            cube([sx * 2.1, 14.0, 15.0]);
        translate([sx * 64.5, 68.5, Z_base + 2.8])
            cube([sx * 8.0, 11.0, 6.5]);
        hull() {
            translate([sx * 66.0, 68.5, Z_base + 2.8]) cube([sx * 0.1, 11.0, 6.5]);
            translate([sx * 70.0, 67.5, Z_base + 1.5]) cube([sx * 0.1, 13.0, 9.2]);
        }
        translate([sx * 63.5, 67.5, Z_base - 1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 81.5, Z_base - 1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 67.5, Z_base + 1.5]) cylinder(d=6.0, h=12.0);
        translate([sx * 63.5, 81.5, Z_base + 1.5]) cylinder(d=6.0, h=12.0);
        translate([sx * 59.0, 71.0, Z_base + 1.0])
            cube([sx * 10.0, 7.0, 3.5]);
    }
}

// ====================================================================
// 1D. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V10.0 (01D_K2_Hub_Adapter_Plate - SNAP-FIT & DUAL VL53L0X)
// ====================================================================
module mcu_deck_dfm() {
    T_deck = 6.0;
    difference() {
        union() {
            translate([-60.0, -8.0, 0.0])
                cube([120.0, 90.0, T_deck]);
            for (sx = [-1, 1]) {
                translate([sx * 33.0 - 8.0, -18.0, 0.0])
                    cube([16.0, 11.0, T_deck]);
                translate([sx * 34.2 - 5.0, 81.0, 0.0])
                    cube([10.0, 21.0, T_deck]);
            }
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=0.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=0.0);
            for (sx = [-1, 1]) {
                translate([sx * 42.0 - 7.0, -8.0, T_deck]) {
                    cube([14.0, 3.5, 12.0]);
                    translate([0, 3.5, 10.5])
                        hull() {
                            cube([14.0, 0.1, 1.5]);
                            translate([0, 1.8, 0]) cube([14.0, 0.1, 1.5]);
                        }
                }
                translate([sx * 57.0 - (sx > 0 ? 0 : 5.0), 80.0, T_deck]) {
                    cube([5.0, 2.2, 14.0]);
                    translate([0, -1.6, 11.5])
                        hull() {
                            cube([5.0, 1.6, 1.2]);
                            translate([0, 1.6, 2.5]) cube([5.0, 0.1, 0.1]);
                        }
                    translate([0, 2.2, 11.5])
                        hull() {
                            cube([5.0, 0.1, 2.5]);
                            translate([0, 2.8, 0]) cube([5.0, 0.1, 2.5]);
                        }
                }
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), -6.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), 70.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
            }
        }
        translate([-21.0, 19.0, -1.0])
            cube([42.0, 36.0, T_deck + 2.0]);
        for (sx = [-1, 1]) {
            for (abs_x = [32.0, 40.0, 48.0, 54.0]) {
                slot_m3_with_nut_channel_z0(sx * abs_x, -4.5, sx * abs_x, 19.5, T_deck);
                slot_m3_with_nut_channel_z0(sx * abs_x, 54.5, sx * abs_x, 78.5, T_deck);
            }
            for (hy_rear = [-2.0, 5.0, 12.0, 18.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_rear, sx * 55.5, hy_rear, T_deck);
                side_nut_entry_port_z0(sx, hy_rear, T_deck);
            }
            for (hy_front = [56.0, 62.0, 69.0, 76.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_front, sx * 55.5, hy_front, T_deck);
                side_nut_entry_port_z0(sx, hy_front, T_deck);
            }
            hull() {
                translate([sx * 31.5, 45.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.0, 45.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 31.5, 52.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.0, 52.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 31.5, 45.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 35.0, 45.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 31.5, 52.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 35.0, 52.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
            }
            hull() {
                translate([sx * 32.0, 95.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.5, 95.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 32.0, 99.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.5, 99.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 32.0, 95.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 35.5, 95.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 32.0, 99.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 35.5, 99.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
            }
            slot_m3_counterbored_top(sx * 31.5, -13.0, sx * 34.5, -13.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 33.0, -15.0, sx * 33.0, -11.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 32.5, 88.0, sx * 35.5, 88.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 34.0, 86.0, sx * 34.0, 90.0, 0.0, T_deck);
            for (gx = [44.0, 52.0]) {
                for (gy = [25.0, 33.0, 41.0]) {
                    slot_m3_with_nut_channel_z0(sx * gx, gy - 1.5, sx * gx, gy + 1.5, T_deck);
                }
            }
        }
        for (gx = [-16.0, -8.0, 0.0, 8.0, 16.0]) {
            for (gy = [0.0, 8.0, 64.0, 72.0]) {
                slot_m3_with_nut_channel_z0(gx - 1.5, gy, gx + 1.5, gy, T_deck);
            }
        }
    }
}

// ====================================================================
// 1D_ALT. KHUNG ĐÔN LIỀN KHỐI ĐA NĂNG CHO K2 CONTROL HUB V10.0
// (CANTILEVER REAR-SHIFT + DUAL VL53L0X PODS + ZERO TOWER COLLISION)
// ====================================================================
module k2_hub_riser_adapter() {
    Z_top = 44.0;
    T_deck = 6.0;
    Z_bot = Z_top - T_deck; // 38.0mm
    
    difference() {
        union() {
            translate([-60.0, -8.0, Z_bot])
                cube([120.0, 90.0, T_deck]);
                
            for (sx = [-1, 1]) {
                translate([sx * 33.0 - 7.0, 44.5, 22.0])
                    cube([14.0, 11.5, Z_bot - 22.0]);
                translate([sx * 34.2 - 5.0, 81.0, 22.0])
                    cube([10.0, 21.0, Z_top - 22.0]);
                hull() {
                    translate([sx * 34.2 - 5.0, 81.0, 28.0]) cube([10.0, 2.0, Z_top - 28.0]);
                    translate([sx * 36.0 - 7.5, 76.0, Z_bot]) cube([15.0, 6.0, T_deck]);
                }
            }
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=Z_top - 12.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=Z_top - 12.0);
        }
        
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 8.0, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([16.0, 4.5, 9.0]);
        }
        
        translate([-20.0, 22.0, 20.0])
            cube([40.0, 42.0, 26.0]);
        translate([-18.0, -9.0, Z_bot - 1.0])
            cube([36.0, 6.0, T_deck + 2.0]);
            
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.8, 46.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 34.2, 46.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 31.8, 52.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 34.2, 52.5, 20.0]) cylinder(d=3.5, h=6.6);
            }
            hull() {
                translate([sx * 31.8, 46.5, 26.5]) cylinder(d1=3.5, d2=9.2, h=3.2);
                translate([sx * 34.2, 46.5, 26.5]) cylinder(d1=3.5, d2=9.2, h=3.2);
                translate([sx * 31.8, 52.5, 26.5]) cylinder(d1=3.5, d2=9.2, h=3.2);
                translate([sx * 34.2, 52.5, 26.5]) cylinder(d1=3.5, d2=9.2, h=3.2);
            }
            hull() {
                translate([sx * 31.8, 46.5, 29.6]) cylinder(d=9.2, h=16.0);
                translate([sx * 34.2, 46.5, 29.6]) cylinder(d=9.2, h=16.0);
                translate([sx * 31.8, 52.5, 29.6]) cylinder(d=9.2, h=16.0);
                translate([sx * 34.2, 52.5, 29.6]) cylinder(d=9.2, h=16.0);
            }
            
            hull() {
                translate([sx * 32.8, 95.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 34.8, 95.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 32.8, 99.5, 20.0]) cylinder(d=3.5, h=6.6);
                translate([sx * 34.8, 99.5, 20.0]) cylinder(d=3.5, h=6.6);
            }
            hull() {
                translate([sx * 32.8, 95.5, 26.5]) cylinder(d1=3.5, d2=8.0, h=2.8);
                translate([sx * 34.8, 95.5, 26.5]) cylinder(d1=3.5, d2=8.0, h=2.8);
                translate([sx * 32.8, 99.5, 26.5]) cylinder(d1=3.5, d2=8.0, h=2.8);
                translate([sx * 34.8, 99.5, 26.5]) cylinder(d1=3.5, d2=8.0, h=2.8);
            }
            hull() {
                translate([sx * 34.2, 95.0, 29.2]) cylinder(d=8.4, h=16.0);
                translate([sx * 34.2, 99.2, 29.2]) cylinder(d=8.4, h=16.0);
            }
            
            // 4 Rãnh trượt đơn M3 gọn gàng tại 4 góc K2 Control Hub (Sàn đặc liền khối 100%):
            for (sy = [6.0, 68.0]) {
                hull() {
                    translate([sx * 44.0, sy, Z_bot - 1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                    translate([sx * 53.0, sy, Z_bot - 1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                }
                hull() {
                    translate([sx * 44.0, sy, Z_top - 2.5]) cylinder(d=6.5, h=3.0);
                    translate([sx * 53.0, sy, Z_top - 2.5]) cylinder(d=6.5, h=3.0);
                }
            }
        }
    }
}

// ====================================================================
// 1E. ĐẾ ĐỆM CẢM BIẾN DÒ LINE RỜI IN PHẲNG 100% (01E_Line_Sensor_Spacer_Pod)
// ====================================================================
module line_sensor_spacer_dfm() {
    difference() {
        translate([-26.0, 148.0, -6.0]) cube([52.0, 24.0, 6.0]);
        for (lx = [-16.0, -12.0, -8.0, 8.0, 12.0, 16.0]) {
            translate([lx, 160.0, -6.5]) cylinder(d=3.3, h=7.0);
        }
        translate([-8.0, 146.0, -6.5]) cube([16.0, 8.0, 7.0]);
    }
}

// ====================================================================
// 2A. NẮP KẸP ĐỘNG CƠ GA25 PHÍA TRƯỚC (TIÊU CHUẨN)
// ====================================================================
module ga25_clamp_cap() {
    difference() {
        union() {
            translate([-12.0, -22.0, 0.6]) cube([24.0, 44.0, 5.4]);
            translate([-12.0, -14.2, 0]) cube([24.0, 28.4, 16.0]);
        }
        translate([-13.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=24.8, h=26.0);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
    }
}

// ====================================================================
// 2B. NẮP KẸP ĐỘNG CƠ GA25 PHÍA SAU - TRÁI (LEFT REAR MOTOR CLAMP V4.3)
// - Vòm bán nguyệt tăng lên Ø26.2mm kèm vát miệng loe 45° (Ø27.5mm) ôm trọn hộp số to!
// - Toàn bộ mép trong (cả tai lẫn vòm) thu hẹp về x = +3.5mm -> Cách trụ MCU cũ 2.5mm suốt chiều dài!
// ====================================================================
module ga25_rear_clamp_left() {
    difference() {
        union() {
            translate([-12.0, -22.0, 0.6]) cube([15.5, 12.0, 5.4]);
            translate([-12.0, -14.5, 0.0]) cube([15.5, 29.0, 16.0]);
            translate([-12.0, 10.0, 0.6]) cube([15.5, 12.0, 5.4]);
        }
        translate([-13.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=20.0);
        translate([-13.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([2.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
        translate([3.5, 22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
        translate([3.5, -22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
    }
}

// ====================================================================
// 2C. NẮP KẸP ĐỘNG CƠ GA25 PHÍA SAU - PHẢI (RIGHT REAR MOTOR CLAMP V4.3)
// - Vòm bán nguyệt tăng lên Ø26.2mm kèm vát miệng loe 45° (Ø27.5mm)
// - Toàn bộ mép trong thu hẹp về x = -3.5mm -> Cách trụ MCU cũ 2.5mm suốt chiều dài!
// ====================================================================
module ga25_rear_clamp_right() {
    difference() {
        union() {
            translate([-3.5, -22.0, 0.6]) cube([15.5, 12.0, 5.4]);
            translate([-3.5, -14.5, 0.0]) cube([15.5, 29.0, 16.0]);
            translate([-3.5, 10.0, 0.6]) cube([15.5, 12.0, 5.4]);
        }
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=20.0);
        translate([-4.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([11.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
        translate([-3.5, 22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
        translate([-3.5, -22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
    }
}

// ====================================================================
// 2D. NẮP KẸP ĐỘNG CƠ GA25 PHÍA SAU - DÙNG CHUNG (UNIVERSAL REAR MOTOR CLAMP V4.3)
// Thu hẹp đối xứng cả 2 bên x in [-4.0, +4.0] (rộng 8mm) -> Cách trụ MCU 2.0mm ở cả 2 bên!
// ====================================================================
module ga25_rear_clamp_universal() {
    difference() {
        union() {
            translate([-4.0, -22.0, 0.6]) cube([8.0, 12.0, 5.4]);
            translate([-4.0, -14.5, 0.0]) cube([8.0, 29.0, 16.0]);
            translate([-4.0, 10.0, 0.6]) cube([8.0, 12.0, 5.4]);
        }
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=10.0);
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([2.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
    }
}

// ====================================================================
// 3A. KHUNG TAY NÂNG DƯỚI CHỮ H V12.0 SIÊU BỀN CHỐNG GÃY (03_Parallel_Arm_Truss_IBeam V12.0)
// ====================================================================
// - Giải quyết triệt để 100% 2 yêu cầu cải tiến thực tế từ Bambu Studio:
//   1. Loại bỏ triệt để vết cắt lẹm vào cổ dầm:
//      + Hốc đĩa tròn Ø20.8mm chỉ khoét mặt ngoài (X >= 17.2mm), không phạm vào dầm chính.
//      + Đai tròn đặc Ø26.0mm bao quanh 360 độ (dày 2.6mm đặc 100%), thành sau dày 5.7mm.
//      + Cổ nối tiếp tuyến gân tăng cứng (fillet R >= 4.0mm) vuốt mượt từ vòm Ø26mm vào dầm.
//   2. 2 Vấu chặn góc hình nêm:
//      + Chân vấu vát 45 độ theo phương bàn in Z -> 0% Support trên bàn in FDM!
//      + Tăng diện tích tiếp xúc chân vấu bám dầm trải dài Y in [-6.0, +12.0mm] (dài 18mm).
//      + Bo góc R >= 1.5mm ở chân vấu tiêu tán xung lực va đập hành trình.
//   3. Đặt in nằm phẳng 100% tại Z = 0.00mm, 1 Single Shell, 100% Watertight Manifold!
// ====================================================================
// 3A. KHUNG TAY NÂNG DƯỚI CHỮ H V13.0 THANH MẢNH SIÊU BỀN (03_Parallel_Arm_Truss_IBeam)
// ====================================================================
// - Tối ưu hóa 100% theo yêu cầu thanh mảnh đồng bộ thanh trên (03B) & loại bỏ gờ lòi:
//   1. Thân dầm chuẩn cao 12.0mm, dày 5.0mm thanh mảnh đồng bộ tuyệt đối với thanh trên.
//   2. Loại bỏ triệt để 100% 2 dải gờ/đế lòi ra dưới đáy 2 bên tai bản lề!
//      Đầu tai bản lề bo tròn đồng tâm R = 6.0mm quanh lỗ Ø3.2mm, phẳng phiu liền mạch với dầm.
//   3. Khớp Servo Horn: Vòm ôm đĩa tròn Ø24.0mm cắt phẳng đáy Z = 0, gân lượn tiếp tuyến mượt mà
//      (fillet R >= 4.0mm kết thúc gọn tại Y = 16mm, KHÔNG đắp dốc khổng lồ dọc thân dầm).
//      Thành dầm chịu lực dày 8.0mm tại gốc (X in [11.5, 19.5]), giữ thành sau hốc dày 5.7mm đặc 100%,
//      thịt quanh hốc ốc chìm M3 dày 4.4mm đặc (> 2.0mm).
//   4. Loại bỏ hoàn toàn 2 khối nêm chặn góc (theo yêu cầu user: không để nhô cục thô kệch).
//   5. Đặt in nằm phẳng 100% tại Z = 0.00mm, 1 Single Shell, 100% Watertight Manifold, 0% Support!
module lower_h_frame_arm_v13(length = 98.0, height = 12.0, thickness = 5.0) {
    t_drive = 8.0; // Bề dày dầm phải tại ngàm Servo S1 (8.0mm: X in [11.5, 19.5])
    
    difference() {
        union() {
            // --------------------------------------------------------
            // 1. THANH TRÁI BỊ ĐỘNG (X in [-19.5, -14.5], dày 5.0mm, cao 12.0mm)
            // --------------------------------------------------------
            translate([-19.5, 0, -height/2])
                cube([thickness, length, height]);
                
            // Tai bản lề tròn đồng tâm R = 6.0mm quanh 2 lỗ chốt xoay (Z in [-6, +6])
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);

            // --------------------------------------------------------
            // 2. THANH PHẢI CHỦ ĐỘNG (X in [14.5, 19.5], dày 5.0mm, cao 12.0mm)
            // --------------------------------------------------------
            translate([14.5, 0, -height/2])
                cube([thickness, length, height]);
                
            // Tai bản lề trước bên phải tròn đồng tâm R = 6.0mm
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);

            // Gân chuyển tiếp dày dầm phải từ 8.0mm ở gốc (X=11.5) về 5.0mm (X=14.5)
            // Vuốt thuôn mượt mà ở mặt trong từ Y=12mm đến Y=22mm
            hull() {
                translate([11.5, 0, -height/2]) cube([3.0, 12.0, height]);
                translate([14.5, 22.0, -height/2]) cube([0.5, 1.0, height]);
            }

            // --------------------------------------------------------
            // 3. VÒM GÁ ĐĨA TRÒN SERVO S1 Ø24.0mm & GÂN LƯỢN CHUYỂN TIẾP R=4.0mm
            //    (Đáy phẳng 100% tại Z = -6.0mm, không dốc khổng lồ dọc thân dầm!)
            // --------------------------------------------------------
            intersection() {
                hull() {
                    // Vòm tròn ôm đĩa Servo Ø24.0mm tại gốc (Y = 0, Z = 0)
                    translate([19.5 - t_drive, 0, 0])
                        rotate([0, 90, 0]) cylinder(d=24.0, h=t_drive);
                        
                    // Gân lượn vuốt tiếp tuyến mượt mà vào dầm cao 12mm (kết thúc tại Y = 16.0mm)
                    translate([19.5 - t_drive, 16.0, -height/2])
                        cube([t_drive, 2.0, height]);
                }
                // Giới hạn đáy Z >= -height/2 = -6.0mm để mặt đáy phẳng tuyệt đối 100%
                translate([11.0, -15.0, -height/2])
                    cube([9.0, 40.0, 25.0]);
            }

            // --------------------------------------------------------
            // 4. THANH GIẰNG NGANG CHỮ H CHỐNG XOẮN (Lồng sâu 0.5mm cả 2 đầu X)
            // --------------------------------------------------------
            translate([-15.0, 42.0, -height/2])
                cube([30.0, 14.0, height]);
        }

        // ------------------------------------------------------------
        // CÁC HỐC KHOÉT & LỖ CHỐT
        // ------------------------------------------------------------
        
        // A. Hốc tròn âm Ø21.0mm sâu 2.3mm ôm trọn Đĩa tròn Servo MG996R ở mặt ngoài (X in [17.2, 19.6])
        //    Giữ thành sau dày 5.7mm đặc 100%, KHÔNG CẮT VÀO DẦM!
        translate([17.2, 0, 0]) rotate([0, 90, 0]) cylinder(d=21.0, h=2.8);

        // B. Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([10.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);

        // C. 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm hốc chìm Ø5.5mm sâu 1.8mm ở mặt trong (X in [11.0, 12.8])
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            if (hz >= -height/2 + 0.5) {
                translate([10.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=10.0);
                translate([11.0, hy, hz]) rotate([0, 90, 0]) cylinder(d=5.5, h=1.8);
            }
        }

        // D. Lỗ chốt xoay mắt trước (Y = length = 98.0, Z = 0)
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);

        // E. Lỗ chốt xoay mắt sau thanh trái (Y = 0, Z = 0)
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=10.0);
    }
}

module lower_h_frame_arm_v13_printable() {
    translate([0, 0, 6.0])
        lower_h_frame_arm_v13();
}

// Giữ alias tương thích ngược
module lower_h_frame_arm_v12(length = 98.0, height = 12.0, thickness = 5.0) {
    lower_h_frame_arm_v13(length, height, thickness);
}

module lower_h_frame_arm_v12_printable() {
    lower_h_frame_arm_v13_printable();
}

module lower_h_frame_arm_v11(length = 98.0, height = 12.0, thickness = 5.0) {
    lower_h_frame_arm_v13(length, height, thickness);
}

module lower_h_frame_arm_v11_printable() {
    lower_h_frame_arm_v13_printable();
}

module lower_h_frame_arm_v50(length = 98.0, height = 12.0, thickness = 5.0) {
    lower_h_frame_arm_v13(length, height, thickness);
}

module lower_h_frame_arm_v50_printable() {
    lower_h_frame_arm_v13_printable();
}

module lower_h_frame_arm(length = 98.0, height = 12.0, thickness = 5.0) {
    lower_h_frame_arm_v13(length, height, thickness);
}

// ====================================================================
// 3B. KHUNG TAY NÂNG TRÊN CHỮ H ĐÁY PHẲNG 100% (03B_Upper_H_Frame_Follower_Arm)
// ====================================================================
module upper_h_frame_arm(length = 98.0, height = 11.0, thickness = 5.0) {
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
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=44.0);
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);
    }
}

// ====================================================================
// 4A. CỔ TAY NỐI TAY NÂNG H-FRAME & GÁ SERVO S3 GẬP DỌC 90° V7.1
// (04A_Wrist_Clevis_Pitch_Bracket_S3 - ZERO SUPPORT, 100% H-FRAME COMPATIBLE)
// ====================================================================
module wrist_clevis_pitch_bracket_s3() {
    Y_piv = 26.8;
    Z_piv = 38.0;

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

        translate([-8.5, 4.5, -3.0]) cube([17.0, 12.2, 60.0]);

        for (zp = [10.0, 38.0]) {
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) rotate([0, 0, -45]) cube([3.3/2, 3.3/2, 40.0]);
            translate([-8.6, 8.0, zp]) rotate([0, -90, 0]) cylinder(d=6.5, h=2.6, $fn=6);
            translate([8.6, 8.0, zp])  rotate([0, 90, 0])  cylinder(d=6.5, h=2.6, $fn=6);
        }

        for (sy = [Y_piv - 5.0, Y_piv + 5.0]) {
            for (sz = [3.75, 52.25]) {
                translate([-10.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=2.95, h=25.0);
            }
        }
        translate([-8.5, 19.0, 0.75])  cube([13.0, 19.0, 6.0]);
        translate([-8.5, 19.0, 49.25]) cube([13.0, 19.0, 6.0]);

        translate([-30.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.0, h=18.0);
        translate([-17.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=3.6, $fn=6);

        translate([-13.6, 22.0, 4.5]) cube([8.0, 9.6, 4.0]);
    }
}

// ====================================================================
// 4, 5 & 6. CỤM ĐẦU KẸP V2.0 THỰC CHIẾN (GRIPPER V2.0 - 0% SUPPORT DFM)
// - Bệ đầu kẹp 04_Gripper_Base_Head_V2
// - Cặp ngàm kẹp đa năng 05 & 06 (Bánh răng Involute m=1.5mm, Rãnh V kép, Răng cưa)
// ====================================================================
include <gripper_v2.scad>;
include <gripper_folded_200x200.scad>;

module gripper_base_head() {
    gripper_base_head_v2();
}

module specialized_gripper_jaw(is_left = true) {
    gripper_jaw_v2(is_left = is_left);
}

// ====================================================================
// 7. BÁNH XE MECANUM K3 Ø80mm x 38mm
// ====================================================================
module mecanum_wheel_k3(is_left = true) {
    color("Goldenrod") {
        difference() {
            rotate([0, 90, 0]) cylinder(d=WHEEL_D, h=WHEEL_W);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 14.0, h=7.0);
            translate([WHEEL_W - 6.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=WHEEL_D - 14.0, h=7.0);
            translate([-1, 0, 0]) rotate([0, 90, 0]) cylinder(d=4.2, h=WHEEL_W + 2);
        }
    }
    color("DimGray") {
        for (i = [0:8]) {
            angle = i * 40;
            rotate([angle, 0, 0])
            translate([WHEEL_W/2, (WHEEL_D/2 - 5.5), 0])
            rotate([0, is_left ? 45 : -45, 0])
            cylinder(d=12.5, h=15.0, center=true);
        }
    }
}

// ====================================================================
// 8. MÔ HÌNH SERVO MG996R KÈM CÁNH TAY GẠT (SERVO HORN)
// ====================================================================
module servo_mg996r_vertical_down() {
    color("SlateGray") {
        translate([-10.35 - 20.35, -9.85, 4.5]) cube([40.7, 19.7, 37.5]);
        difference() {
            translate([-10.35 - 27.0, -9.85, 10.5]) cube([54.0, 19.7, 2.5]);
            for (sx = [-10.35 - 24.25, -10.35 + 24.25]) {
                for (sy = [-5.0, 5.0]) {
                    translate([sx, sy, 9.5]) cylinder(d=3.4, h=5.0);
                }
            }
        }
        translate([0, 0, 2.3]) cylinder(d=12.0, h=2.5);
    }
    color("Ivory") {
        translate([-3.9, -3.9, 0.2]) cube([7.8, 20.5, 2.1]);
    }
}

// ====================================================================
// HIỂN THỊ THEO CHẾ ĐỘ (ASSEMBLY HOẶC BÀN IN 3D PHẲNG Z = 0.0)
// ====================================================================
if (DISPLAY_MODE == "assembly") {
    // 1. Khung gầm chính Đáy Phẳng + 2 Tháp nâng rời + Bệ MCU rời + Đế đệm dò line rời
    color("DarkSlateGray")
        translate([0, 0, GROUND_CLEAR])
            monocoque_chassis_dfm();

    color("SteelBlue") {
        translate([0, 0, GROUND_CLEAR]) lift_tower_dfm(is_left=true);
        translate([0, 0, GROUND_CLEAR]) lift_tower_dfm(is_left=false);
    }

    // 1D. Bệ chuyển tiếp Adapter Riser đôn cao 15mm bắt khít 4 trụ cũ
    color("Teal")
        translate([0, 0, GROUND_CLEAR])
            k2_hub_riser_adapter();

    color("DimGray")
        translate([0, 0, GROUND_CLEAR])
            line_sensor_spacer_dfm();

    // 2. 4 Nắp kẹp động cơ GA25 màu cam thể thao (tại X = ±44.0mm)
    color("OrangeRed") {
        // 2 Nẹp trước (Y = 142.0) dùng nắp tiêu chuẩn
        translate([-44.0, 142.0, Z_SHAFT]) ga25_clamp_cap();
        translate([44.0, 142.0, Z_SHAFT]) ga25_clamp_cap();
        
        // 2 Nẹp sau (Y = 32.0) thiết kế lại vát khuyết góc trong tránh 100% va chạm với trụ MCU đã in!
        translate([-44.0, 32.0, Z_SHAFT]) ga25_rear_clamp_left();
        translate([44.0, 32.0, Z_SHAFT]) ga25_rear_clamp_right();
    }

    // 3. 4 Động cơ kim loại GA25-370 6V 250RPM
    color("Silver") {
        translate([-64.0, 142.0, Z_SHAFT]) rotate([0, 90, 0]) cylinder(d=25.0, h=48.0);
        translate([64.0 - 48.0, 142.0, Z_SHAFT]) rotate([0, 90, 0]) cylinder(d=25.0, h=48.0);
        translate([-64.0, 32.0, Z_SHAFT]) rotate([0, 90, 0]) cylinder(d=25.0, h=54.0);
        translate([64.0 - 54.0, 32.0, Z_SHAFT]) rotate([0, 90, 0]) cylinder(d=25.0, h=54.0);
    }

    // 4. 4 Bánh xe Mecanum K3 Ø80mm x 38mm
    translate([-109.0, 142.0, Z_SHAFT]) mecanum_wheel_k3(is_left=false);
    translate([109.0 - WHEEL_W, 142.0, Z_SHAFT]) mecanum_wheel_k3(is_left=true);
    translate([-109.0, 32.0, Z_SHAFT]) mecanum_wheel_k3(is_left=true);
    translate([109.0 - WHEEL_W, 32.0, Z_SHAFT]) mecanum_wheel_k3(is_left=false);

    // 5A & 5B. Cảm biến Siêu âm & Cảm biến Dò đường 4 mắt OhStem
    color("MediumSeaGreen") {
        translate([-24.0, CHASSIS_L - 10.0, GROUND_CLEAR + 4.0]) cube([48.0, 2.0, 22.0]);
        translate([-13.0, CHASSIS_L + 4.0, GROUND_CLEAR + 14.0]) rotate([90, 0, 0]) cylinder(d=16.0, h=12.0);
        translate([13.0, CHASSIS_L + 4.0, GROUND_CLEAR + 14.0]) rotate([90, 0, 0]) cylinder(d=16.0, h=12.0);
    }
    color("DarkBlue")
        translate([-24.0, 148.0, GROUND_CLEAR - 8.5])
            cube([48.0, 24.0, 2.5]);

    // 6. Khối Pin Li-ion 2S 18650 7.4V
    color("RoyalBlue")
        translate([-18.0, 50.0, GROUND_CLEAR + FLOOR_T + 1.0])
            cube([36.0, 54.0, 17.0]);

    // 7. Mạch điều khiển trung tâm ORC K2 Control Hub THỰC TẾ OhStem (121.0 x 86.0 x 26.0 mm)
    // Dời lùi Cantilever Y = -6.0..+80.0mm (Cách mặt sau Tháp Nâng Y=105.0mm đúng 25.0mm và cách Servo S1 27.65mm!)
    color("Black")
        translate([-60.5, -6.0, GROUND_CLEAR + 44.0])
            cube([121.0, 86.0, 26.0]);
    // Tem nhãn màu cam đặc trưng trên nóc K2 Control Hub
    color("DarkOrange")
        translate([-42.0, -1.0, GROUND_CLEAR + 70.0])
            cube([84.0, 76.0, 0.8]);

    // 7B. CẶP CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X HAI BÊN SƯỜN ĐO TƯỜNG GIẢI MÊ CUNG V10.0
    color("Purple") {
        // Cảm biến VL53L0X Trái (đo thành mê cung bên Trái)
        translate([-68.2, 68.0, GROUND_CLEAR + 35.5]) cube([1.6, 25.0, 11.0]);
        // Cảm biến VL53L0X Phải (đo thành mê cung bên Phải)
        translate([66.6, 68.0, GROUND_CLEAR + 35.5]) cube([1.6, 25.0, 11.0]);
    }
    // Tia laser hồng ngoại ToF 90° phát sang 2 bên vách mê cung (màu đỏ mờ trực quan)
    color("Crimson", 0.4) {
        translate([-68.2 - 120.0, 74.0, GROUND_CLEAR + 40.0]) cube([120.0, 2.0, 2.0]);
        translate([68.2, 74.0, GROUND_CLEAR + 40.0]) cube([120.0, 2.0, 2.0]);
    }

    // 8. SERVO MG996R S1
    color("SlateGray") {
        translate([22.0, 114.3, GROUND_CLEAR + 48.15]) cube([37.5, 40.7, 19.7]);
        translate([28.0, 107.65, GROUND_CLEAR + 48.15]) cube([2.5, 54.0, 19.7]);
    }

    // 9. KHUNG CÁNH TAY NÂNG SONG HÀNH 4 KHÂU CHỮ H
    color("DodgerBlue") {
        translate([0, Y_PIVOT, 78.0])
            rotate([ARM_ANGLE, 0, 0])
                lower_h_frame_arm(length = ARM_L);
        translate([0, Y_PIVOT, 106.0])
            rotate([ARM_ANGLE, 0, 0])
                upper_h_frame_arm(length = ARM_L);
    }

    // 10A. Cổ tay nối tay nâng H-frame & Gá Servo S3 gập dọc 90° (04A)
    color("DodgerBlue")
        translate([0, Y_HEAD, Z_HEAD])
            wrist_clevis_pitch_bracket_s3();

    // 10B. SERVO MG996R S3 (Cổ tay gập dọc 0°..90°)
    color("SlateGray") {
        translate([-13.5, Y_HEAD + 16.95, Z_HEAD + 7.65]) cube([37.5, 19.7, 40.7]);
        translate([13.0, Y_HEAD + 16.95, Z_HEAD + 0.75])  cube([2.5, 19.7, 54.5]);
        translate([24.0, Y_HEAD + 26.8, Z_HEAD + 38.0]) rotate([0, 90, 0]) cylinder(d=12.0, h=2.5);
    }
    color("Ivory")
        translate([27.0, Y_HEAD + 26.8, Z_HEAD + 38.0]) rotate([0, 90, 0]) cylinder(d=20.0, h=2.2);

    // 10C. Cụm bệ đầu kẹp 3 trụ hoa + Servo S2 + 2 Ngàm kẹp (Xoay dọc WRIST_PITCH_ANGLE quanh trục X tại Y_HEAD+26.8, Z_HEAD+38.0)
    translate([0, Y_HEAD + 26.8, Z_HEAD + 38.0])
        rotate([WRIST_PITCH_ANGLE, 0, 0])
            translate([0, -6.0, -38.0]) {
                color("OrangeRed") gripper_base_head();

                // 11. SERVO MG996R S2
                translate([15.0, 39.0, 24.5])
                    servo_mg996r_vertical_down();

                // 12. Cặp hàm kẹp liên hoàn 3 trụ hoa Ø32mm V7.1
                color("Crimson") {
                    translate([-15.0, 39.0, 5.0])
                        rotate([0, 0, -JAW_GRIP_ANGLE])
                            translate([15.0, 0, 0])
                                specialized_gripper_jaw(is_left=true);
                    translate([15.0, 39.0, 5.0])
                        rotate([0, 0, JAW_GRIP_ANGLE])
                            translate([-15.0, 0, 0])
                                specialized_gripper_jaw(is_left=false);
                }

                // 13. 3 Ống hoa mẫu Ø32.0 mm x Cao 120.0 mm được kẹp cùng lúc
                if (WRIST_PITCH_ANGLE == 0) {
                    color("Gold", 0.75) {
                        for (yk = [33.0, 66.0, 99.0]) {
                            translate([0, 39.0 + yk, -Z_HEAD + 10.0])
                                cylinder(d=32.0, h=120.0);
                        }
                    }
                }
            }
} else {
    // BỐ CỤC ĐẶT PHẲNG 100% TRÊN MẶT BÀN IN (Z = 0.0 mm - ZERO SUPPORT)
    color("DarkOrange") {
        // 1. Khung gầm chính phẳng đáy 100% tại Z = 0
        monocoque_chassis_dfm();

        // 2. Khung chuyen tiep K2 Control Hub Adapter Plate dat phang tai Z = 0
        translate([120, 0, 44.0]) rotate([180, 0, 0]) k2_hub_riser_adapter();

        // 3. Đế đệm cảm biến dò line đặt phẳng tại Z = 0
        translate([120, -40, 6.0]) line_sensor_spacer_dfm();

        // 4. Hai Tháp nâng Trái & Phải xoay nằm phẳng mặt ngoài tại Z = 0
        translate([160, 0, 28.0]) rotate([0, -90, 0]) lift_tower_dfm(is_left=true);
        translate([270, 0, 28.0]) rotate([0, 90, 0])  lift_tower_dfm(is_left=false);

        // 5. Hai khung tay nâng chữ H phẳng đáy tại Z = 0
        translate([-120, 20, 6.0]) lower_h_frame_arm();
        translate([-180, 20, 5.5]) upper_h_frame_arm();

        // 6. Cổ tay 04A, Bệ đầu kẹp 04 & 2 Hàm kẹp 05, 06 phẳng đáy tại Z = 0
        translate([-80, 140, 0])  rotate([90, 0, 0]) wrist_clevis_pitch_bracket_s3();
        translate([-140, 140, 0]) gripper_base_head();
        translate([-210, 140, 0]) specialized_gripper_jaw(is_left=true);
        translate([-270, 140, 0]) specialized_gripper_jaw(is_left=false);

        // 7. Cặp nẹp động cơ sau thiết kế lại (in nằm phẳng mặt bên tại Z = 0)
        translate([60, -40, 12.0]) rotate([0, -90, 0]) ga25_rear_clamp_left();
        translate([95, -40, 12.0]) rotate([0, 90, 0])  ga25_rear_clamp_right();
    }
}
