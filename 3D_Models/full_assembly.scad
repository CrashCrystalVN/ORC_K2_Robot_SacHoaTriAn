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

// THÔNG SỐ ĐỘNG HỌC CÁNH TAY SONG HÀNH 4 KHÂU CHỮ H
Y_PIVOT        = 145.0;   // Tâm khớp xoay trên tháp nâng (Y in [105, 166])
ARM_L          = 98.0;    // Chiều dài tâm 2 mắt xoay
ARM_ANGLE      = -20.0;   // Góc gập tay đòn hướng về phía trước
DY_ARM         = ARM_L * cos(ARM_ANGLE);  // 92.09 mm
DZ_ARM         = ARM_L * sin(ARM_ANGLE);  // -33.52 mm
Y_HEAD         = Y_PIVOT + DY_ARM - 8.0;  // 229.09 mm
Z_HEAD         = 78.0 + DZ_ARM - 10.0;    // 34.48 mm
WRIST_PITCH_ANGLE = 0.0;                  // 0.0° = Hạ ngang kẹp 3 trụ hoa; 90.0° = Gập đứng 90° tiết kiệm diện tích!

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
// 1D. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V9.0 (01D_K2_Hub_Adapter_Plate - CANTILEVER REAR-SHIFT)
// ====================================================================
module mcu_deck_dfm() {
    T_deck = 6.0;
    difference() {
        union() {
            translate([-60.0, -8.0, 0.0])
                cube([120.0, 90.0, T_deck]);
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 0.0])
                    cube([10.0, 21.0, T_deck]);
                hull() {
                    translate([sx * 34.2 - 5.0, 81.0, 0.0]) cube([10.0, 3.0, T_deck]);
                    translate([sx * 38.0 - 8.5, 76.0, 0.0]) cube([17.0, 6.0, T_deck]);
                }
            }
        }
        translate([-20.0, 22.0, -1.0])
            cube([40.0, 42.0, T_deck + 2.0]);
        translate([-18.0, -9.0, -1.0])
            cube([36.0, 6.0, T_deck + 2.0]);
        for (sx = [-1, 1]) {
            for (abs_x = [36.0, 44.0, 48.0, 54.0]) {
                slot_m3_with_nut_channel_z0(sx * abs_x, -4.5, sx * abs_x, 19.5, T_deck);
                slot_m3_with_nut_channel_z0(sx * abs_x, 54.5, sx * abs_x, 78.5, T_deck);
            }
            for (hy_rear = [0.0, 8.0, 16.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_rear, sx * 55.5, hy_rear, T_deck);
                side_nut_entry_port_z0(sx, hy_rear, T_deck);
            }
            for (hy_front = [58.0, 66.0, 74.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_front, sx * 55.5, hy_front, T_deck);
                side_nut_entry_port_z0(sx, hy_front, T_deck);
            }
            slot_m3_counterbored_top(sx * 31.8, 45.0, sx * 34.2, 53.0, 0.0, T_deck, 6.8, 2.0, 3.5);
            slot_m3_counterbored_top(sx * 31.0, 49.0, sx * 35.0, 49.0, 0.0, T_deck, 6.8, 2.0, 3.5);
            slot_m3_counterbored_top(sx * 32.2, 87.5, sx * 36.2, 91.5, 0.0, T_deck, 6.8, 2.0, 3.5);
            slot_m3_counterbored_top(sx * 32.0, 95.5, sx * 35.5, 99.5, 0.0, T_deck, 6.8, 2.0, 3.5);
            for (gx = [36.0, 44.0, 52.0]) {
                for (gy = [26.0, 34.0, 42.0, 50.0]) {
                    slot_m3_with_nut_channel_z0(sx * gx, gy - 1.5, sx * gx, gy + 1.5, T_deck);
                }
            }
        }
        for (gx = [-16.0, -8.0, 0.0, 8.0, 16.0]) {
            for (gy = [4.0, 12.0, 68.0, 76.0]) {
                slot_m3_with_nut_channel_z0(gx - 1.5, gy, gx + 1.5, gy, T_deck);
            }
        }
    }
}

// ====================================================================
// 1D_ALT. KHUNG ĐÔN LIỀN KHỐI ĐA NĂNG CHO K2 CONTROL HUB V9.0
// (CANTILEVER REAR-SHIFT + ZERO TOWER COLLISION + CAPTIVE BLIND-FLOOR NUT RAILS)
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
            
            for (abs_x = [36.0, 44.0, 48.0, 54.0]) {
                slot_m3_with_nut_channel_zbot(sx * abs_x, -4.5, sx * abs_x, 19.5, Z_bot, T_deck);
                slot_m3_with_nut_channel_zbot(sx * abs_x, 54.5, sx * abs_x, 78.5, Z_bot, T_deck);
            }
            for (hy_rear = [0.0, 8.0, 16.0]) {
                slot_m3_with_nut_channel_zbot(sx * 30.0, hy_rear, sx * 55.5, hy_rear, Z_bot, T_deck);
                side_nut_entry_port_zbot(sx, hy_rear, Z_bot, T_deck);
            }
            for (hy_front = [58.0, 66.0, 74.0]) {
                slot_m3_with_nut_channel_zbot(sx * 30.0, hy_front, sx * 55.5, hy_front, Z_bot, T_deck);
                side_nut_entry_port_zbot(sx, hy_front, Z_bot, T_deck);
            }
            for (gx = [36.0, 44.0, 52.0]) {
                for (gy = [26.0, 34.0, 42.0, 50.0]) {
                    slot_m3_with_nut_channel_zbot(sx * gx, gy - 1.5, sx * gx, gy + 1.5, Z_bot, T_deck);
                }
            }
        }
        for (gx = [-16.0, -8.0, 0.0, 8.0, 16.0]) {
            for (gy = [4.0, 12.0, 68.0, 76.0]) {
                slot_m3_with_nut_channel_zbot(gx - 1.5, gy, gx + 1.5, gy, Z_bot, T_deck);
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
// 3A. KHUNG TAY NÂNG DƯỚI CHỮ H ĐÁY PHẲNG 100% (03_Parallel_Arm_Truss_IBeam V5.0)
// ====================================================================
// Chuẩn hóa 100% cho Đĩa tròn Servo MG996R (25T Round Horn):
// - Hốc tròn âm Ø20.8mm sâu 2.5mm ở mặt ngoài thanh phải (ôm trọn đĩa tròn Ø20mm).
// - 8 Lỗ ốc M3 trên vòng chia PCD Ø14.0mm (r = 7.0mm) kèm lỗ bậc chìm Ø6.0mm ở mặt trong.
// - Lỗ tâm xuyên suốt Ø6.5mm: Tra chìa vặn ốc khóa trục 25T mà không cần tháo tay nâng!
// - Đáy phẳng tuyệt đối 100% tại Z = -6.0mm: Đặt in phẳng trực tiếp trên bàn in -> 0% SUPPORT!
module lower_h_frame_arm(length = 98.0, height = 12.0, thickness = 5.0) {
    difference() {
        union() {
            // Thanh trái (X in [-19.5, -14.5])
            translate([-19.5, 0, -height/2]) cube([thickness, length, height]);
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, -height/2, -height/2]) cube([thickness, height/2, height/2]);
            translate([-19.5, length, -height/2]) cube([thickness, height/2, height/2]);

            // Thanh phải (X in [14.5, 19.5])
            translate([14.5, 0, -height/2]) cube([thickness, length, height]);
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([14.5, length, -height/2]) cube([thickness, height/2, height/2]);

            // Gờ vòm tròn tăng cứng ôm đĩa tròn Servo (d = 23.0mm) ở gốc thanh phải:
            intersection() {
                translate([14.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=23.0, h=thickness);
                translate([14.0, -12.0, -height/2]) cube([thickness + 1.0, 24.0, 20.0]);
            }
            translate([14.5, -height/2, -height/2]) cube([thickness, height/2, height/2]);

            // Thanh giằng ngang chữ H chống xoắn (X in [-14.5, 14.5])
            translate([-14.5, 42.0, -height/2]) cube([29.0, 14.0, height]);
        }

        // Hốc tròn âm Ø20.8mm sâu 2.5mm ở mặt ngoài thanh phải (X in [17.0, 19.6])
        translate([17.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=20.8, h=3.0);

        // Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([13.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=7.0);

        // 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm lỗ bậc chìm Ø6.0mm ở mặt trong
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            if (hz >= -height/2 + 1.0) {
                translate([13.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=7.0);
                translate([13.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=6.0, h=2.2);
            }
        }

        // Lỗ chốt xoay mắt trước
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);

        // Lỗ chốt xoay mắt sau thanh trái
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=10.0);
    }
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
// 4. BỆ ĐẦU KẸP 3 TRỤ HOA TÍCH HỢP BẢN LỀ GẬP DỌC 90° V7.1 - 0% SUPPORT (04_Gripper_Base_Head)
// ====================================================================
module gripper_base_head() {
    Y_piv = 6.0;
    Z_piv = 38.0;
    Y_jaw = 39.0;

    difference() {
        union() {
            translate([-31.0, 22.0, 0]) cube([66.0, 28.0, 5.0]);
            hull() {
                translate([-20.0, 46.0, 0]) cube([40.0, 4.0, 5.0]);
                translate([-14.0, 58.0, 0]) cube([28.0, 4.0, 5.0]);
            }
            translate([-31.0, 22.0, 0]) cube([66.0, 5.5, 24.5]);
            translate([-15.0, Y_jaw, 5.0]) cylinder(d=8.0, h=10.0);
            translate([15.0, Y_jaw, 5.0])  cylinder(d=8.0, h=10.0);

            translate([-31.0, 22.0, 0]) cube([4.0, 28.0, 35.0]);
            translate([-31.0, 22.0, 0]) cube([15.0, 5.0, 24.5]);
            hull() {
                translate([-31.0, 27.0, 21.5]) cube([4.0, 23.0, 13.5]);
                translate([-31.0, 27.0, 31.0]) cube([15.0, 23.0, 4.0]);
            }
            hull() {
                translate([-33.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=18.0, h=6.0);
                translate([-33.0, Y_piv + 6.0, Z_piv - 12.0]) cube([6.0, 2.0, 12.0]);
                translate([-31.0, 22.0, 0.0]) cube([4.0, 14.0, 35.0]);
            }

            translate([27.0, 22.0, 0]) cube([8.0, 28.0, 35.0]);
            hull() {
                translate([27.0, 27.0, 26.0]) cube([8.0, 23.0, 9.0]);
                translate([25.25, 27.0, 29.0]) cube([9.75, 23.0, 6.0]);
            }
            hull() {
                translate([27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=25.0, h=8.0);
                translate([27.0, Y_piv + 8.0, Z_piv - 16.0]) cube([8.0, 2.0, 16.0]);
                translate([27.0, 22.0, 0.0]) cube([8.0, 14.0, 35.0]);
            }
        }

        for (sx = [4.65 - 24.25, 4.65 + 24.25]) {
            for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
                translate([sx, sy, 20.0]) cylinder(d=2.95, h=20.0);
            }
        }
        for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
            translate([28.90, sy, -1.0]) cylinder(d=6.5, h=29.5, $fn=6);
            translate([28.90, sy, 28.4]) cylinder(d1=6.5, d2=2.95, h=2.0);
        }
        for (px = [-15.0, 15.0]) {
            translate([px, Y_jaw, -1.0]) cylinder(d=3.3, h=20.0);
            translate([px, Y_jaw, -0.1]) rotate([0, 0, 30]) cylinder(d=6.45, h=2.8, $fn=6);
            translate([px, Y_jaw, 2.65]) cylinder(d1=6.45, d2=3.3, h=1.8);
        }

        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) rotate([0, 0, 45]) cube([3.4/2, 3.4/2, 10.0]);
        translate([-33.5, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.5);

        translate([26.8, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=20.8, h=2.7);
        translate([26.8, Y_piv - 4.1, Z_piv - 4.1]) cube([2.7, 22.0, 8.2]);
        translate([26.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);
        for (a = [0:45:315]) {
            hy = Y_piv + 7.0 * cos(a);
            hz = Z_piv + 7.0 * sin(a);
            translate([26.0, hy, hz]) rotate([0, 90, 0]) cylinder(d=2.9, h=10.0);
        }
    }
}

// ====================================================================
// 5 & 6. CẶP HÀM KẸP LIÊN HOÀN 3 TRỤ HOA Ø32mm V7.0 (05 & 06)
// ====================================================================
module specialized_gripper_jaw(is_left = true) {
    pivot_x = is_left ? -15.0 : 15.0;
    sx = is_left ? -1.0 : 1.0;
    H = 22.0;
    H_hub = is_left ? 16.0 : 22.0;
    Y1 = 33.0;
    Y2 = 66.0;
    Y3 = 99.0;

    difference() {
        union() {
            translate([pivot_x, 0, 0]) cylinder(r=11.5, h=H_hub);
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r=10.0, h=H_hub);
                translate([sx * 17.5, 16.0, 0]) cylinder(r=5.0, h=H_hub);
            }
            hull() {
                translate([sx * 17.5, 14.0, 0]) cylinder(r=5.0, h=H_hub);
                translate([sx * 19.0, 21.0, 0]) cylinder(r=5.0, h=H);
            }
            for (a = is_left ? [-54, -36, -18, 0, 18, 36] : [135, 153, 171, 189, 207, 225]) {
                translate([pivot_x, 0, 0])
                    rotate([0, 0, a])
                        hull() {
                            translate([10.5, -2.1, 0]) cube([2.5, 4.2, 16.0]);
                            translate([16.3, -1.1, 0]) cube([0.6, 2.2, 16.0]);
                        }
            }
            difference() {
                union() {
                    for (yk = [Y1, Y2, Y3]) {
                        translate([0, yk, 0]) cylinder(r=23.0, h=H);
                    }
                    if (is_left) {
                        translate([-23.0, 20.0, 0]) cube([7.5, 79.0, H]);
                    } else {
                        translate([15.5, 20.0, 0])  cube([7.5, 79.0, H]);
                    }
                }
                translate([-25.0, Y3, -1.0]) cube([50.0, 30.0, H + 2.0]);
                translate([-11.0, 8.0, -1.0]) cube([22.0, 9.5, H + 2.0]);
                if (is_left) {
                    translate([-30.0, 0.0, H_hub]) cube([60.0, 15.0, H]);
                    translate([-30.0, 15.0, H_hub]) rotate([45, 0, 0]) cube([60.0, 10.0, 10.0]);
                }
            }
            hull() {
                translate([sx * 19.2, Y3, 0]) cylinder(d=6.8, h=H);
                translate([sx * 30.0, Y3 + 19.0, 0]) cylinder(d=5.0, h=H);
            }
        }

        if (is_left) {
            translate([-7.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        } else {
            translate([-32.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        }

        for (yk = [Y1, Y2, Y3]) {
            translate([0, yk, 0]) {
                translate([0, 0, -0.5]) cylinder(r=14.9, h=2.0);
                translate([0, 0, 1.4])  cylinder(r1=14.9, r2=16.1, h=1.2);
                translate([0, 0, 2.5])  cylinder(r=16.1, h=H + 2.0);
                for (zg = [6.5, 11.5, 16.5]) {
                    translate([0, 0, zg]) cylinder(r1=16.1, r2=16.6, h=0.8);
                    translate([0, 0, zg + 0.8]) cylinder(r1=16.6, r2=16.1, h=0.8);
                }
            }
        }

        translate([-13.0, Y1, 2.5]) cube([26.0, Y3 - Y1 + 5.0, H + 2.0]);
        translate([-12.5, Y1, -0.5]) cube([25.0, Y3 - Y1 + 5.0, 3.2]);

        for (yk = [Y1, Y2, Y3]) {
            for (ang = is_left ? [166, 175, 184] : [-14, -5, 4]) {
                hull() {
                    translate([19.2 * cos(ang), yk + 19.2 * sin(ang), -1.0])
                        cylinder(d=2.0, h=H + 2.0, $fn=16);
                    translate([19.2 * cos(ang + 9), yk + 19.2 * sin(ang + 9), -1.0])
                        cylinder(d=2.0, h=H + 2.0, $fn=16);
                }
            }
        }

        translate([pivot_x, 0, -0.2]) cylinder(d=8.2, h=10.4);
        translate([pivot_x, 0, 10.2]) cylinder(d1=8.2, d2=3.4, h=2.4);
        translate([pivot_x, 0, -0.5]) cylinder(d=3.4, h=H + 2.0);
        if (is_left) {
            translate([pivot_x, 0, H_hub - 3.0]) cylinder(d=6.8, h=4.0);
        }

        if (!is_left) {
            translate([pivot_x, 0, H - 2.5]) cylinder(d=20.8, h=3.0);
            translate([pivot_x - 4.1, -4.1, H - 2.5]) cube([8.2, 23.0, 3.0]);
            translate([pivot_x, 0, 12.6]) cylinder(d=6.5, h=10.0);
            for (a = [0:45:315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, 11.0]) cylinder(d=2.9, h=12.0);
            }
            translate([pivot_x, 11.0, 12.0]) cylinder(d=2.5, h=11.0);
            translate([pivot_x, 16.0, 12.0]) cylinder(d=2.5, h=11.0);
        }
    }
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
                    translate([0, 39.0, 5.0]) specialized_gripper_jaw(is_left=true);
                    translate([0, 39.0, 5.0]) specialized_gripper_jaw(is_left=false);
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
