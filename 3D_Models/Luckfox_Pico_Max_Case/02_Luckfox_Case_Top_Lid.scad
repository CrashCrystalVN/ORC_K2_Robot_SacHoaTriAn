$fn = 64;

// ====================================================================
// THÔNG SỐ KỸ THUẬT LUCKFOX PICO MAX / PRO & HỆ 2 ỐNG Ø8MM (C-C 48MM)
// ====================================================================
pcb_L = 72.0;          // Chiều dài chuẩn PCB Luckfox Pico Max (mm)
pcb_W = 21.0;          // Chiều rộng chuẩn PCB Luckfox Pico Max (mm)
pcb_T = 1.6;           // Độ dày PCB (mm)

cav_L = 72.8;          // Lòng trong chứa PCB dài 72.8mm (dung sai +0.8mm)
cav_W = 21.6;          // Lòng trong chứa PCB rộng 21.6mm (dung sai +0.6mm)

wall_X = 2.6;          // Độ dày vách 2 đầu USB-C / RJ45
wall_Y = 3.0;          // Độ dày vách 2 bên sườn
box_L  = cav_L + 2*wall_X; // 78.0 mm (-39.0 .. +39.0)
box_W  = cav_W + 2*wall_Y; // 27.6 mm (-13.8 .. +13.8)

rod_D  = 8.20;         // Đường kính lòng ngàm ôm ống Ø8.0mm (dung sai +0.20mm in FDM ôm khít)
rod_CC = 48.0;         // Khoảng cách tâm 2 ống = 4.8cm = 48.0mm (-24.0 và +24.0)

// Hộp bo tròn 4 góc theo trục Z (Z từ 0 đến lz)
module rounded_box_z(lx, ly, lz, r=2.4) {
    hull() {
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx*(lx/2 - r), sy*(ly/2 - r), 0])
                    cylinder(r=r, h=lz);
    }
}

// Hốc tán lục giác M3 chống xoay
module m3_nut_trap(h=3.2) {
    cylinder(d=6.35, h=h, $fn=6);
}

// ====================================================================
// CORE THÂN DƯỚI CASE LUCKFOX PICO MAX (MẶT ĐÁY Z = 0, CAO LÊN Z = 20.0mm)
// - Tọa độ Z trong module core:
//   + Z = 0.0 mm        : Mặt đáy ngoài cùng của buồng bảo vệ chân GPIO
//   + Z = 13.5 mm       : Mặt dưới của PCB Luckfox Pico Max (40 chân GPIO dài 11.5mm
//                         quay xuống từ Z=13.5 xuống Z=2.0mm -> thụt an toàn 2.0mm!)
//   + Z = 15.1 mm       : Mặt trên của PCB (pcb_T = 1.6mm)
//   + Z = 20.0 mm       : Mặt phân khuôn (Split line) ghép với Nắp trên
// - Thiết kế 2 rãnh bảo vệ chân GPIO độc lập (Y = -8.89mm và Y = +8.89mm, rộng 4.2mm)
//   giữ lại sống lưng giữa (Y = -6.79 .. +6.79mm) liền khối 100% từ đầu đến cuối,
//   vừa đỡ cứng bo mạch chống võng, vừa chống chạm chập giữa 2 hàng chân GPIO!
// ====================================================================
module luckfox_bottom_core(side_gpio_windows=false) {
    z_pcb_bot = 13.5;
    z_pcb_top = z_pcb_bot + pcb_T; // 15.1
    z_top_rim = 20.0;

    difference() {
        union() {
            // 1. Khối thân hộp chính (78.0 x 27.6 x 20.0 mm, Z = 0 .. 20.0)
            rounded_box_z(box_L, box_W, z_top_rim, r=2.4);

            // 2. 2 Tai bắt ốc M3 ở 2 bên sườn tại X = 0.0 mm (Z = 0 .. 20.0, phẳng tuyệt đối tại Z=0)
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(box_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=z_top_rim);
                    translate([-5.2, sy*(box_W/2 - 1.5), 0])
                        cube([10.4, 3.0, z_top_rim]);
                }
            }
        }

        // ------------------------------------------------------------
        // CÁC HỐC CẮT BÊN TRONG THÂN DƯỚI
        // ------------------------------------------------------------

        // A. Khoang chứa PCB từ Z = z_pcb_bot (13.5) lên đỉnh Z = 21.0
        translate([-cav_L/2, -cav_W/2, z_pcb_bot])
            cube([cav_L, cav_W, z_top_rim - z_pcb_bot + 2.0]);

        // B. 2 Rãnh sâu bảo vệ 2 hàng chân GPIO hàn ngược quay xuống (X = -35.2 .. +16.0mm, dài 51.2mm)
        //    Tâm 2 hàng chân tại Y = -8.89mm và Y = +8.89mm; mỗi rãnh rộng 4.2mm (Y = +-6.79 .. +-10.99mm)
        //    Xuyên suốt từ đáy Z = -0.5 lên Z = z_pcb_bot + 0.5 để cắm dây Dupont từ dưới lên dễ dàng!
        for (sy = [-1, 1]) {
            translate([-35.2, sy*8.89 - 2.1, -0.5])
                cube([51.2, 4.2, z_pcb_bot + 1.0]);
        }

        // C. 3 Hốc thoáng tản nhiệt & giảm trọng lượng trên sống lưng giữa (Y = -4.6 .. +4.6mm, Z = 2.5 .. 13.6mm)
        //    Giữ nguyên sàn đáy Z = 0..2.5mm và 2 vách ngăn đỡ PCB tại X = -18.0 và X = -1.0mm -> Liền khối 100%!
        for (x_pock = [-33.0, -15.5, 1.5]) {
            translate([x_pock, -4.6, 2.5])
                cube([14.0, 9.2, z_pcb_bot - 2.0]);
        }

        // D. Nếu dùng cho bản UnderMount (01B), mở thêm cửa sổ luồn dây ngang ở sườn và dưới sống lưng
        if (side_gpio_windows) {
            translate([-20.0, -5.0, 2.5])
                cube([32.0, 10.0, 8.5]);
        }

        // E. Hốc thoát chân hàn & chốt nhựa định vị dưới đáy cổng RJ45 (X = +16.2 .. +36.4mm)
        //    Chừa gờ đỡ PCB dày 2.2mm ở 2 bên sườn (Y = +-8.6 .. +-10.8mm) đỡ chắc cụm RJ45!
        translate([16.2, -8.5, z_pcb_bot - 4.0])
            cube([20.2, 17.0, 4.5]);

        // F. Khe cắm cổng USB Type-C ở đầu X = -39.0mm (rộng 12.6mm, cao từ Z = 13.0 lên 21.0mm)
        translate([-box_L/2 - 1.0, -6.3, z_pcb_bot - 0.5])
            cube([wall_X + 2.5, 12.6, 8.5]);
        // Hốc loe bên ngoài cho đầu bọc nhựa cáp USB-C to (rộng 14.4mm)
        translate([-box_L/2 - 0.5, -7.2, z_pcb_bot - 1.2])
            cube([1.6, 14.4, 9.5]);

        // G. Khe cổng mạng RJ45 ở đầu X = +39.0mm (rộng 16.6mm, từ Z = z_pcb_bot + 1.0 lên đỉnh)
        translate([cav_L/2 - 1.0, -8.3, z_pcb_bot + 1.0])
            cube([wall_X + 2.5, 16.6, 15.0]);

        // H. Lỗ ốc M3 + Hốc tán M3 lục giác ở 2 tai bên sườn (X = 0, Y = +-(box_W/2 + 3.2))
        for (sy = [-1, 1]) {
            translate([0, sy*(box_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=z_top_rim + 1.0);
            translate([0, sy*(box_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.2);
        }

        // I. 4 Rãnh ngàm Snap-fit ở mặt ngoài sườn (X = -26.0 và X = +26.0, Z = 15.0)
        for (sx = [-1, 1]) {
            for (sy = [-1, 1]) {
                translate([sx*26.0 - 4.0, sy*(box_W/2 - 0.8) - 0.6, 15.0])
                    cube([8.0, 1.2, 2.2]);
            }
        }
    }
}

// ====================================================================
// MODULE NGÀM KẸP 2 ỐNG Ø8.0MM PHÍA SAU LƯNG (KHOẢNG CÁCH TÂM-TÂM = 48.0MM)
// - Thiết kế ngàm chữ U ôm 205° (Snap-fit) tại X = -24.0mm và X = +24.0mm (C-C = 48.0mm)
// - Tích hợp 2 lỗ vít khóa M3 + Hốc tán M3 âm tại X = -12.0mm và X = +12.0mm
//   để bắt Thanh Khóa Kép (Dual Rod Lock Bar) khóa cứng cả 2 ống Ø8mm!
// ====================================================================
module dual_rod_clamp_block_side(z_height=20.0) {
    y_base = box_W/2;            // 13.8 mm
    y_rod_center = y_base + 7.4; // 21.2 mm
    block_thick = 11.4;          // Y từ 13.8 đến 25.2 mm

    difference() {
        union() {
            // Khối cầu nối liền lưng case (X = -31.5 .. +31.5, Y = 12.0 .. 25.2)
            hull() {
                for (sx = [-1, 1]) {
                    translate([sx*29.5, y_rod_center, 0])
                        cylinder(d=10.8, h=z_height);
                    translate([sx*31.0, y_base - 1.5, 0])
                        cylinder(d=3.0, h=z_height);
                }
            }
        }

        // 1. Giữ thông suốt lỗ ốc M3 & Hốc tán M3 của tai bắt nắp tại (X = 0, Y = box_W/2 + 3.2)
        translate([0, box_W/2 + 3.2, -0.5])
            cylinder(d=3.4, h=z_height + 1.0);
        translate([0, box_W/2 + 3.2, -0.1])
            m3_nut_trap(h=3.2);
        // Hốc mở phía trên Z = 16.5..20.5 tại (X=0, Y=box_W/2+3.2) để tai nắp trên hạ xuống ăn khớp
        hull() {
            translate([0, box_W/2 + 3.2, z_height - 0.1])
                cylinder(d=9.0, h=2.0);
            translate([-5.5, box_W/2 - 0.5, z_height - 0.1])
                cube([11.0, 2.0, 2.0]);
        }

        // 2. 2 Lòng ống Ø8.20mm tại X = -24.0mm và X = +24.0mm (Khoảng cách tâm chuẩn 48.0mm!)
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), y_rod_center, -0.5])
                cylinder(d=rod_D, h=z_height + 1.0);

            // Miệng mở Snap-fit (rộng 7.25mm < 8.20mm giúp ấn tách vào ống Ø8mm tự giữ chặt!)
            // Kèm vát loe 45° dễ ấn vào ống
            translate([sx*(rod_CC/2) - 3.625, y_rod_center, -0.5])
                cube([7.25, 10.0, z_height + 1.0]);
            hull() {
                translate([sx*(rod_CC/2) - 3.625, y_rod_center + 3.1, -0.5])
                    cube([7.25, 0.5, z_height + 1.0]);
                translate([sx*(rod_CC/2) - 5.2, y_rod_center + 5.8, -0.5])
                    cube([10.4, 0.5, z_height + 1.0]);
            }
        }

        // 3. 2 Lỗ vít M3 + Hốc tán M3 âm (tại X = -12.0mm và X = +12.0mm, xuyên theo trục Y)
        //    để bắt Thanh Khóa Kép (Dual Rod Lock Bar) ép chặt 2 ống Ø8mm!
        for (sx = [-1, 1]) {
            translate([sx*12.0, y_base + block_thick + 2.0, z_height/2])
                rotate([90, 0, 0])
                    cylinder(d=3.4, h=block_thick + 3.5);
            // Hốc nhét tán M3 từ mặt đáy Z=0 lên Z=13.0mm (Captive Nut Slot)
            translate([sx*12.0 - 2.85, y_base + 2.0, -0.1])
                cube([5.7, 2.7, z_height/2 + 3.0]);
        }
    }
}

// ====================================================================
// CHI TIẾT 01A: CASE BOTTOM + NGÀM KẸP 2 ỐNG Ø8MM PHÍA SAU LƯNG (KHUYÊN DÙNG SỐ 1)
// - Không che bất kỳ chân GPIO nào, không che cổng RJ45/USB-C, không che Camera/SD!
// - Manifold 100% (Volumes: 1), in phẳng tại Z=0 không cần Support!
// ====================================================================
module part_01A_bottom_sidemount() {
    union() {
        luckfox_bottom_core(side_gpio_windows=false);
        dual_rod_clamp_block_side(z_height=20.0);
    }
}

// ====================================================================
// CHI TIẾT 01B: CASE BOTTOM + NGÀM KẸP 2 ỐNG Ø8MM DƯỚI ĐÁY (UNDER-MOUNT)
// - Hai rãnh ống Ø8mm nằm ở mặt đáy (X = -24.0 và X = +24.0), xoay ngang trục Y.
// - Manifold 100% (Volumes: 1), in phẳng tại Z=0 không cần Support!
// ====================================================================
module part_01B_bottom_undermount() {
    base_h = 10.5;
    difference() {
        union() {
            translate([0, 0, base_h])
                luckfox_bottom_core(side_gpio_windows=true);

            // Đế gá dưới đáy liền khối (đỡ cả 2 tai bắt ốc M3 xuống Z=0)
            rounded_box_z(box_L, box_W, base_h + 0.5, r=2.4);
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(box_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=base_h + 0.5);
                    translate([-5.2, sy*(box_W/2 - 1.5), 0])
                        cube([10.4, 3.0, base_h + 0.5]);
                }
            }
        }

        // Lỗ xuyên suốt cho ốc M3 & hốc tán ở 2 tai bên sườn
        for (sy = [-1, 1]) {
            translate([0, sy*(box_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=base_h + 22.0);
            translate([0, sy*(box_W/2 + 3.2), -0.1])
                m3_nut_trap(h=3.5);
        }

        // 2 Rãnh ống Ø8.20mm chạy dọc trục Y tại X = -24.0mm và X = +24.0mm (tâm Z = 4.2mm)
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), box_W/2 + 1.0, 4.2])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=box_W + 2.0);
            // Khe mở Snap-fit dưới đáy Z=0 (rộng 7.25mm)
            translate([sx*(rod_CC/2) - 3.625, -box_W/2 - 1.0, -0.5])
                cube([7.25, box_W + 2.0, 4.7]);
        }

        // Cửa sổ bên hông ở khoảng giữa (X = -14.0 .. +14.0, Z = 2.5 .. base_h) để luồn dây Dupont
        translate([-14.0, -box_W/2 - 1.0, 2.5])
            cube([28.0, box_W + 2.0, base_h - 1.5]);

        // 2 Lỗ bắt ốc M3 khóa ống tại X = -17.0 và X = +17.0
        for (sx = [-1, 1]) {
            translate([sx*17.0, 0, -0.5])
                cylinder(d=3.4, h=base_h + 4.0);
            translate([sx*17.0, 0, base_h - 2.5])
                m3_nut_trap(h=3.2);
        }
    }
}

// ====================================================================
// CHI TIẾT 01C: CASE BOTTOM GÁ DỌC SONG SONG GIỮA 2 ỐNG (VERTICAL MOUNT)
// - Dành cho trường hợp muốn đặt chiều dài 72mm của Luckfox chạy dọc song song với 2 ống,
//   2 cánh tay đòn vươn sang 2 bên tới Y = -24.0mm và Y = +24.0mm (Khoảng cách tâm 48.0mm).
// - Manifold 100% (Volumes: 1), in phẳng tại Z=0!
// ====================================================================
module part_01C_bottom_vertical() {
    arm_L = 32.0; // X từ -16.0 đến +16.0
    union() {
        luckfox_bottom_core(side_gpio_windows=false);

        difference() {
            // Cánh gá ngang vươn ra Y = +-29.5mm
            hull() {
                for (sy = [-1, 1]) {
                    translate([-arm_L/2, sy*24.0, 0])
                        cylinder(d=11.5, h=13.5);
                    translate([ arm_L/2, sy*24.0, 0])
                        cylinder(d=11.5, h=13.5);
                }
            }
            // Không lấn vào lòng hộp chính & 2 rãnh GPIO
            translate([-cav_L/2, -cav_W/2, -1.0])
                cube([cav_L, cav_W, 25.0]);

            // Giữ thông suốt lỗ ốc M3 & hốc tán ở X=0, Y = +-(box_W/2 + 3.2)
            for (sy = [-1, 1]) {
                translate([0, sy*(box_W/2 + 3.2), -0.5])
                    cylinder(d=3.4, h=22.0);
                translate([0, sy*(box_W/2 + 3.2), -0.1])
                    m3_nut_trap(h=3.2);
            }

            // 2 Rãnh ống Ø8.20mm chạy dọc theo trục X tại Y = -24.0mm và Y = +24.0mm (C-C = 48.0mm)
            for (sy = [-1, 1]) {
                translate([-arm_L/2 - 6.0, sy*(rod_CC/2), 4.2])
                    rotate([0, 90, 0])
                        cylinder(d=rod_D, h=arm_L + 12.0);
                // Miệng mở Snap-fit phía dưới Z=0 (rộng 7.25mm)
                translate([-arm_L/2 - 6.0, sy*(rod_CC/2) - 3.625, -0.5])
                    cube([arm_L + 12.0, 7.25, 4.7]);

                // Lỗ ốc M3 khóa nắp kẹp tại X = +-11.0, Y = sy*18.0
                for (sx = [-1, 1]) {
                    translate([sx*11.0, sy*18.0, -0.5])
                        cylinder(d=3.4, h=15.0);
                    translate([sx*11.0, sy*18.0, 10.5])
                        m3_nut_trap(h=3.5);
                }
            }
        }
    }
}

// ====================================================================
// CHI TIẾT 02: NẮP TRÊN BẢO VỆ LUCKFOX PICO MAX (TOP LID)
// - Đã xoay lật ngửa (mặt đỉnh nằm tại Z = 0.0mm) để in 3D phẳng 100% không cần Support!
// - Manifold 100% (Volumes: 1).
// ====================================================================
module part_02_top_lid_printable() {
    lid_H = 12.0;      // Chiều cao phần thân nắp tính từ mặt đỉnh (Z=0) xuống mặt ghép (Z=12.0)
    top_T = 2.2;       // Độ dày trần nắp

    difference() {
        union() {
            // 1. Khối hộp nắp chính (78.0 x 27.6 x 12.0 mm, Z = 0 .. 12.0)
            rounded_box_z(box_L, box_W, lid_H, r=2.4);

            // 2. 2 Tai bắt ốc M3 ở X = 0.0 mm khớp với thân dưới (Z = 0 .. 12.0)
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(box_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=lid_H);
                    translate([-5.2, sy*(box_W/2 - 1.5), 0])
                        cube([10.4, 3.0, lid_H]);
                }
            }

            // 3. 4 Chân ngàm Snap-fit vươn từ vách ngoài xuống Z = lid_H + 5.0mm
            for (sx = [-1, 1]) {
                for (sy = [-1, 1]) {
                    translate([sx*26.0 - 3.5, sy*(box_W/2 - 1.3) - 0.65, 0])
                        cube([7.0, 1.3, lid_H + 5.0]);
                    // Gờ móc Snap-fit hướng vào trong
                    hull() {
                        translate([sx*26.0 - 3.5, sy*(box_W/2 - 1.65) - 0.5, lid_H + 3.6])
                            cube([7.0, 1.0, 1.2]);
                        translate([sx*26.0 - 3.5, sy*(box_W/2 - 1.3) - 0.5, lid_H + 2.6])
                            cube([7.0, 0.7, 2.2]);
                    }
                }
            }
        }

        // ------------------------------------------------------------
        // CÁC HỐC KHOÉT TRÊN NẮP
        // ------------------------------------------------------------

        // A. Khoang rỗng lòng nắp (từ Z = top_T lên Z = lid_H + 1)
        translate([-cav_L/2, -cav_W/2, top_T])
            cube([cav_L, cav_W, lid_H + 2.0]);

        // B. Khe cổng mạng RJ45 ở đầu X = +15.0 .. +39.5mm (rộng 16.8mm)
        translate([cav_L/2 - 1.0, -8.4, top_T])
            cube([wall_X + 2.5, 16.8, lid_H + 2.0]);
        // Cửa sổ bấm lẫy hạt mạng RJ45 trên mặt nắp (X = +28.0 .. +39.5, rộng 14.0mm)
        translate([28.0, -7.0, -0.5])
            cube([12.0, 14.0, top_T + 1.0]);

        // C. Khe luồn cáp Camera MIPI CSI + Dây pin RTC (X = +6.5 .. +16.2mm, rộng 16.5mm)
        translate([6.5, -8.25, -0.5])
            cube([9.7, 16.5, top_T + 1.5]);

        // D. Khe tản nhiệt trực tiếp trên chip RV1106 (X = -11.5 .. +4.5mm)
        for (xpos = [-9.5, -5.5, -1.5, 2.5]) {
            hull() {
                translate([xpos, -5.5, -0.5]) cylinder(d=2.4, h=top_T + 1.5);
                translate([xpos,  5.5, -0.5]) cylinder(d=2.4, h=top_T + 1.5);
            }
        }

        // E. Cửa sổ rút/cắm thẻ nhớ MicroSD (TF Card) & Bấm nút BOOT / RESET (X = -32.0 .. -13.5mm)
        hull() {
            for (sx = [-30.5, -14.5])
                for (sy = [-6.0, 6.0])
                    translate([sx, sy, -0.5])
                        cylinder(d=3.6, h=top_T + 1.5);
        }

        // F. Khe thoát cổng USB Type-C ở đầu X = -39.0mm
        translate([-box_L/2 - 1.0, -6.3, lid_H - 3.5])
            cube([wall_X + 2.5, 12.6, 5.0]);

        // G. 2 Rãnh dọc trên nắp (Y = +-8.89mm, X = -35.0 .. +15.5mm)
        //    Tránh cấn mối hàn chân GPIO mặt trên
        for (sy = [-1, 1]) {
            translate([-35.0, sy*8.89 - 1.4, 0.9])
                cube([50.5, 2.8, top_T + 2.0]);
        }

        // H. Lỗ ốc M3 + Hốc chìm đầu ốc M3 ở 2 tai bên sườn (X = 0)
        for (sy = [-1, 1]) {
            translate([0, sy*(box_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=lid_H + 2.0);
            translate([0, sy*(box_W/2 + 3.2), -0.1])
                cylinder(d=6.2, h=2.8);
        }
    }
}

// ====================================================================
// CHI TIẾT 03: THANH KHÓA KÉP 2 ỐNG Ø8MM (KHOẢNG CÁCH TÂM 48.0MM)
// - Đế dày 8.0mm liền khối (cầu nối đáy dày 4.4mm cứng vững 100%, Volumes: 1).
// - Tích hợp cả cặp lỗ M3 ở X = ±12.0mm (cho bản 01A) và X = ±17.0mm (cho bản 01B)
//   trên cùng 1 thanh khóa đa năng + 2 nắp kẹp đơn cho bản 01C!
// ====================================================================
module universal_dual_rod_lock_bar() {
    bar_H = 8.0;
    difference() {
        // Thân thanh khóa kép dài 61mm, rộng 15mm, cao 8.0mm (Z = 0 .. 8.0)
        hull() {
            for (sx = [-1, 1])
                translate([sx*23.0, 0, 0])
                    cylinder(d=15.0, h=bar_H);
        }

        // 2 Lòng ôm ống Ø8.20mm tại X = -24.0mm và X = +24.0mm (tâm cách nhau đúng 48.0mm)
        // Đặt tâm ống ở Z = bar_H + 0.5 = 8.5mm -> ngoạm sâu 3.6mm vào mặt trên (còn lại đáy dày 4.4mm liền khối!)
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), 0, bar_H + 0.5])
                rotate([90, 0, 0])
                    cylinder(d=rod_D, h=20.0, center=true);
        }

        // Cặp lỗ ốc M3 tại X = ±12.0mm (khớp 100% với bản 01A SideMount)
        // & Cặp lỗ ốc M3 tại X = ±17.0mm (khớp 100% với bản 01B UnderMount)
        for (xpos = [-17.0, -12.0, 12.0, 17.0]) {
            translate([xpos, 0, -0.5])
                cylinder(d=3.4, h=bar_H + 1.0);
            // Hốc âm đầu ốc M3 ở mặt lưng Z = 0 .. 2.8mm
            translate([xpos, 0, -0.1])
                cylinder(d=6.2, h=2.8);
        }
    }
}

module part_03_rod_clamp_locks() {
    universal_dual_rod_lock_bar();
}

// ====================================================================
// BẢN LẮP RÁP MINH HỌA TRỰC QUAN (FULL ASSEMBLY PREVIEW KÈM BO LUCKFOX & 2 ỐNG Ø8MM)
// ====================================================================
module luckfox_board_mockup() {
    z_pcb_bot = 13.5;
    // PCB màu đen (72 x 21 x 1.6mm)
    color([0.15, 0.15, 0.18])
        translate([-pcb_L/2, -pcb_W/2, z_pcb_bot])
            cube([pcb_L, pcb_W, pcb_T]);

    // Đế nhựa vàng GPIO hàn ngược dưới đáy PCB + 40 chân kim loại quay xuống dưới (Z = 2.0 .. 13.5mm)
    for (sy = [-1, 1]) {
        color([0.95, 0.8, 0.1])
            translate([-35.4, sy*8.89 - 1.25, z_pcb_bot - 2.5])
                cube([50.8, 2.5, 2.5]);
        color([0.85, 0.75, 0.3])
            for (i = [0:19]) {
                translate([-34.13 + i*2.54, sy*8.89, z_pcb_bot - 11.5])
                    cylinder(d=0.64, h=12.8, $fn=12);
            }
    }

    // Cổng RJ45 bạc ở đầu X = +15.5 .. +36.5mm
    color([0.78, 0.80, 0.82])
        translate([15.5, -8.0, z_pcb_bot + pcb_T])
            cube([21.0, 16.0, 13.3]);

    // Cổng USB-C bạc ở đầu X = -36.5 .. -29.0mm
    color([0.78, 0.80, 0.82])
        translate([-36.5, -4.5, z_pcb_bot + pcb_T])
            cube([7.5, 9.0, 3.2]);

    // Chip RV1106 ở giữa
    color([0.1, 0.1, 0.1])
        translate([-8.0, -5.0, z_pcb_bot + pcb_T])
            cube([11.0, 11.0, 1.4]);
}

module assembly_preview() {
    // 1. Thân dưới 01A (Màu xanh dương)
    color([0.20, 0.55, 0.90, 0.95])
        part_01A_bottom_sidemount();

    // 2. Bo mạch Luckfox Pico Max (chân GPIO quay xuống dưới)
    luckfox_board_mockup();

    // 3. Nắp trên 02 (Màu cam hổ phách, nâng nhẹ 8mm dạng Exploded View để thấy rõ bên trong)
    color([0.95, 0.55, 0.15, 0.90])
        translate([0, 0, 38.0])
            rotate([180, 0, 0])
                part_02_top_lid_printable();

    // 4. Hai thanh trụ tròn Ø8.0mm màu đen cách nhau đúng 48.0mm (tâm tại X = -24.0 và X = +24.0)
    color([0.18, 0.18, 0.20])
        for (sx = [-1, 1]) {
            translate([sx*24.0, 21.2, -16.0])
                cylinder(d=8.0, h=54.0);
        }

    // 5. Thanh khóa kép 2 ống Ø8mm ở phía sau
    color([0.25, 0.78, 0.45])
        translate([0, 33.5, 10.0])
            rotate([90, 0, 0])
                universal_dual_rod_lock_bar();
}

part_02_top_lid_printable();
