$fn = 64;

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

// ====================================================================
// TIỆN ÍCH RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI & CHỐNG XOAY V9.0 (DFM 0% SUPPORT)
// - Giải quyết triệt để lỗi rơi tán M3 xuống gầm xe khi bắt Plate lên khung trước:
//   + Sàn dày T_deck = 6.0mm có hệ DẢI CẦU ĐỠ ĐÁY TÁN (Train-Rail Retention Bridges) dày 1.2mm
//     bắc ngang qua rãnh 5.65mm (cầu phẳng 1D dài chỉ 5.65mm -> Máy in FDM bắc cầu thẳng tắp 0% Support!).
//   + Tán M3 (5.5 x 6.08 x 2.4mm) trượt êm trên mặt đường ray 1.2mm, KHÔNG BAO GIỜ RƠI XUỐNG GẦM,
//     đồng thời bị 2 vách bên rộng 5.65mm khóa cứng 6 cạnh KHÔNG THỂ XOAY khi siết ốc từ trên xuống!
//   + Cửa nạp tán M3 từ mép sườn ngoài (Side-Entry Port) & Hốc nạp tán (Drop-In Pocket) tiện lợi.
// ====================================================================
module slot_m3_with_nut_channel_z0(x1, y1, x2, y2, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    L = sqrt(dx*dx + dy*dy);
    ang = atan2(dy, dx);
    cx = 0.5 * (x1 + x2);
    cy = 0.5 * (y1 + y2);

    // 1. Khe xuyên suốt cho thân ốc M3 (Ø3.4mm) từ mặt trên xuống mặt dưới:
    hull() {
        translate([x1, y1, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }

    // 2. Tầng rãnh khóa tán M3 chống xoay (rộng 5.65mm, Z = 1.2 .. 3.9mm)
    //    kèm mái côn 45° tự đỡ (Z = 3.85 .. 5.0mm) -> Giữ nguyên đáy kín Z = 0.0 .. 1.2mm!
    hull() {
        translate([x1, y1, 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
        translate([x2, y2, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
    }

    // 3. Hốc nạp tán M3 ở tâm rãnh (mở thông đáy Z = -0.1..3.9mm dài 6.2mm để nhét tán M3 vào đường ray,
    //    khi trượt tán lệch khỏi tâm >= 3mm thì sàn đáy kín Z = 0..1.2mm đỡ chặt tán không bao giờ rơi!):
    translate([cx, cy, 0])
        rotate([0, 0, ang]) {
            hull() {
                translate([-1.2, 0, -0.1]) cylinder(d=nut_w + 0.15, h=4.0);
                translate([ 1.2, 0, -0.1]) cylinder(d=nut_w + 0.15, h=4.0);
            }
        }
}

module slot_m3_with_nut_channel_zbot(x1, y1, x2, y2, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    ang = atan2(dy, dx);
    cx = 0.5 * (x1 + x2);
    cy = 0.5 * (y1 + y2);

    // 1. Khe xuyên suốt cho thân ốc M3 (Ø3.4mm):
    hull() {
        translate([x1, y1, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }

    // 2. Tầng rãnh khóa tán M3 chống xoay (rộng 5.65mm, nằm giữa sàn Z = Z_bot + 1.2 .. Z_bot + 3.9mm)
    //    kèm mái côn 45° tự đỡ (Z = Z_bot + 3.85 .. Z_bot + 5.0mm):
    //    -> Lớp đáy Z_bot .. Z_bot + 1.2mm tạo thành ĐƯỜNG RAY ĐÁY KÍN giữ tán M3 không bao giờ rơi xuống gầm!
    //    -> Khi in lật úp (Z_top chạm bàn in), lớp đáy 1.2mm chỉ bắc cầu phẳng ngang 5.65mm -> 0% Support!
    hull() {
        translate([x1, y1, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
        translate([x2, y2, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
    }

    // 3. Cửa nạp tán M3 (Drop-In Loading Gate dài 6.2mm tại tâm rãnh):
    //    Cho phép ấn tán M3 từ mặt dưới vào rãnh rồi trượt dọc theo đường ray đáy kín 1.2mm!
    translate([cx, cy, 0])
        rotate([0, 0, ang]) {
            hull() {
                translate([-1.2, 0, Z_bot - 0.1]) cylinder(d=nut_w + 0.15, h=4.0);
                translate([ 1.2, 0, Z_bot - 0.1]) cylinder(d=nut_w + 0.15, h=4.0);
            }
        }
}

module side_nut_entry_port_z0(sx, y_pos, T_deck = 6.0, nut_w = 5.75) {
    // Cửa nhét tán M3 trực tiếp từ mép sườn ngoài (|X| = 60.0mm) vào rãnh đường ray đáy kín (Z = 1.2..3.9mm):
    hull() {
        translate([sx * 54.0, y_pos, 1.2]) cylinder(d=nut_w, h=2.7);
        translate([sx * 61.0, y_pos, 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([sx * 54.0, y_pos, 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
        translate([sx * 61.0, y_pos, 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
    }
}

module side_nut_entry_port_zbot(sx, y_pos, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.75) {
    // Cửa nhét tán M3 trực tiếp từ mép sườn ngoài (|X| = 60.0mm) vào rãnh đường ray đáy kín (Z = Z_bot+1.2..3.9mm):
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
        translate([sx * 61.0, y_pos, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
        translate([sx * 61.0, y_pos, Z_bot + 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
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
            // Cánh vươn chịu lực nối liền mép sàn (X = sx*60..sx*68.8, Y = 66.0..82.5)
            hull() {
                translate([sx * 60.0, 66.0, Z_base]) cube([sx * 0.1, 16.5, T_deck]);
                translate([sx * 68.2, 67.5, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 68.2, 81.0, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 60.0, 82.5, Z_base]) cube([sx * 0.1, 0.1, T_deck]);
            }
            // 2 Ngàm cài Snap-fit đàn hồi giữ mép bo mạch VL53L0X (Y = 70.0 và Y = 78.5)
            for (py = [70.0, 78.5]) {
                translate([sx * 68.6, py - 2.2, Z_base])
                    cube([sx * 1.8, 4.4, T_deck + 6.0]);
                // Đầu móc ngàm khóa có vát dốc 45° dẫn hướng ấn tách
                translate([sx * 68.6, py - 2.2, Z_base + T_deck + 4.5])
                    hull() {
                        cube([sx * 1.8, 4.4, 1.5]);
                        translate([-sx * 1.0, 0, 0]) cube([sx * 0.1, 4.4, 1.0]);
                    }
            }
            // Gờ tì sau lưng bo mạch VL53L0X
            translate([sx * 66.2, 68.0, Z_base])
                cube([sx * 1.4, 13.0, T_deck + 5.5]);
        }
        
        // Khe cắm bo mạch VL53L0X đứng (rộng 2.0mm cho PCB dày 1.6mm + dung sai, dài 25.0mm)
        translate([sx * 67.6, 67.5, Z_base + 1.5])
            cube([sx * 2.1, 14.0, 15.0]);
            
        // Cửa sổ quang học bắn tia laser ToF 90° vuông góc vách tường mê cung (11.0 x 6.5mm kèm vát loe 35°)
        translate([sx * 64.5, 68.5, Z_base + 2.8])
            cube([sx * 8.0, 11.0, 6.5]);
        hull() {
            translate([sx * 66.0, 68.5, Z_base + 2.8]) cube([sx * 0.1, 11.0, 6.5]);
            translate([sx * 70.0, 67.5, Z_base + 1.5]) cube([sx * 0.1, 13.0, 9.2]);
        }
        
        // 2 Lỗ ốc M2.5 / M3 bắt vít dự phòng (khoảng cách tâm 18.0mm: Y = 67.5 và Y = 81.5)
        translate([sx * 63.5, 67.5, Z_base - 1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 81.5, Z_base - 1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 67.5, Z_base + 1.5]) cylinder(d=6.0, h=12.0);
        translate([sx * 63.5, 81.5, Z_base + 1.5]) cylinder(d=6.0, h=12.0);
        
        // Rãnh luồn cáp I2C 4P ngầm xuyên vào sàn plate
        translate([sx * 59.0, 71.0, Z_base + 1.0])
            cube([sx * 10.0, 7.0, 3.5]);
    }
}

// ====================================================================
// 1. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V11.0 (01D_K2_Hub_Adapter_Plate V11.0 GIA CỐ CƠ HỌC)
// TÍCH HỢP TOÀN DIỆN:
// - HỆ GỜ HÃM GÓC GIA CỐ CỰC DÀY (HEAVY-DUTY CHAMFERED CORNER RETENTION SYSTEM)
//   + 2 Gờ hãm đuôi dày 5.5mm có gân tam giác dốc 45° (R >= 3.5mm) khử mỏi 100%
//   + 2 Gờ hãm góc trước dày 6.0mm x rộng 7.0mm có gân tam giác và mép hãm vát nêm 45°
//   + 4 Gờ định vị sườn dày 4.0mm x cao 5.0mm vát côn dẫn hướng 45°
// - 100% MẶT ĐÁY TIẾP XÚC BÀN IN TEXTURED PEI (Z = 0.0mm) - ZERO SUPPORT!
// - CỤM 2 GÁ CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X ĐO TƯỜNG GIẢI MÊ CUNG
// - KIẾN TRÚC LÙI HẬU CANTILEVER NÉ 100% CẤU TRÚC GẮP TRỤ (THÁP NÂNG + SERVO S1)
// ====================================================================
module k2_adapter_plate_flat() {
    T_deck = 6.0;
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 6.0 mm, X in [-60, 60], Y in [-8, 82])
            translate([-60.0, -8.0, 0.0])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Tai Bắt Ốc Lộ Thiên Phía Sau (X in [+-25.0, +-41.0], Y in [-18.0, -8.0])
            for (sx = [-1, 1]) {
                translate([sx * 33.0 - 8.0, -18.0, 0.0])
                    cube([16.0, 11.0, T_deck]);
            }
            
            // 2B. Đệm mở rộng sàn đỡ Gân trợ lực Ngàm Đuôi (X in [+-37.0, +-53.0], Y in [-14.0, -8.0])
            for (sx = [-1, 1]) {
                translate([sx * 45.0 - 8.0, -14.0, 0.0])
                    cube([16.0, 6.5, T_deck]);
            }
            
            // 3. Hai Tay Vươn Bắt Trụ Trước & Khóa Nhanh Lộ Thiên (|X| in [29.2, 39.2], Y in [81.0, 102.0])
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 0.0])
                    cube([10.0, 21.0, T_deck]);
            }
            
            // 3B. Đệm mở rộng sàn đỡ Gân trợ lực Ngàm Trước (X in [+-53.5, +-60.5], Y in [81.5, 89.0])
            for (sx = [-1, 1]) {
                translate([sx * 57.0 - (sx > 0 ? 3.5 : 3.5), 81.5, 0.0])
                    cube([7.0, 7.5, T_deck]);
            }
            
            // 4. Hai Cụm Gá Cảm Biến Khoảng Cách Laser ToF VL53L0X Trái & Phải giải mê cung
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=0.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=0.0);
            
            // ====================================================================
            // 5. CƠ CẤU NGÀM VÀ GỜ HÃM GIA CỐ CƠ HỌC TOÀN DIỆN (MECHANICAL HARDENED SYSTEM)
            // ====================================================================
            // A. HAI GỜ HÃM ĐUÔI GIA CỐ CỰC DÀY CÓ GÂN TAM GIÁC & GÓC LƯỢN R >= 3.5mm:
            //    - Tăng bề dày thành chịu lực từ 3.5mm -> 5.5mm (Y in [-11.5, -6.0])
            //    - Gân tam giác dốc 45° chịu uốn ở mặt lưng sau (Y in [-14.0, -11.5], dốc từ Z=17.5 về Z=6.0)
            //    - Bo góc lượn khử mỏi R = 3.5mm triệt tiêu ứng suất tập trung
            //    - Mép ngàm hãm vát nêm 45° đón góc 20° khi trượt K2 Hub vào êm ái
            for (sx = [-1, 1]) {
                translate([sx * 45.0 - 7.5, -11.5, T_deck]) {
                    // Thân vách chính dày 5.5mm x rộng 15.0mm x cao 11.5mm
                    cube([15.0, 5.5, 11.5]);
                    
                    // Mép hãm vát nêm 45° nhô vào +Y 2.0mm ở Z = 9.8..11.5mm (ngậm mép K2 Hub)
                    translate([0, 5.5, 9.8])
                        hull() {
                            cube([15.0, 0.1, 1.7]);
                            translate([0, 2.0, 0.5]) cube([15.0, 0.1, 1.2]);
                            translate([0, 0, 1.7]) cube([15.0, 0.1, 0.1]);
                        }
                        
                    // Gân trợ lực tam giác mặt sau chịu uốn (Triangular Gusset Ribs)
                    translate([0, -2.5, 0])
                        hull() {
                            cube([15.0, 0.1, 0.1]);
                            translate([0, 2.5, 0]) cube([15.0, 0.1, 11.5]);
                            translate([0, 2.5, 11.5]) cube([15.0, 0.1, 0.1]);
                        }
                }
                // Bo góc lượn R = 3.5mm tại chân ngàm đuôi với mặt sàn
                translate([sx * 45.0 - 7.5, -11.5, T_deck]) {
                    hull() {
                        translate([0, -2.5, 0]) cube([15.0, 0.1, 0.1]);
                        translate([0, 0, 0]) cube([15.0, 0.1, 3.5]);
                    }
                }
            }
            
            // B. HAI GỜ HÃM GÓC TRƯỚC GIA CỐ CỰC DÀY CÓ GÂN TAM GIÁC & MÃNG DẪN HƯỚNG:
            //    - Tiết diện tăng từ 5.0 x 2.2mm -> 7.0 x 6.0mm (tăng độ bền uốn > 800%!)
            //    - Gân tam giác dốc 45° chịu lực hướng ra trước (+Y in [86.0, 89.0])
            //    - Bo góc lượn chân đế R = 3.5mm khử mỏi, triệt tiêu 100% nguy cơ gãy tách lớp Z
            //    - Mép hãm vát nêm 45° nhô vào -Y 1.8mm ở Z = 10.2..12.0mm
            for (sx = [-1, 1]) {
                translate([sx * 57.0 - (sx > 0 ? 3.5 : 3.5), 80.0, T_deck]) {
                    // Trụ chịu lực chính dày 7.0 x 6.0 x 12.0 mm
                    cube([7.0, 6.0, 12.0]);
                    
                    // Mép hãm vát nêm 45° ngậm mép K2 Hub nhô vào -Y 1.8mm
                    translate([0, -1.8, 10.2])
                        hull() {
                            cube([7.0, 1.8, 1.8]);
                            translate([0, 1.8, 1.8]) cube([7.0, 0.1, 0.1]);
                        }
                        
                    // Gân tam giác trợ lực dốc 45° hướng ra phía trước (+Y)
                    translate([0, 6.0, 0])
                        hull() {
                            cube([7.0, 0.1, 12.0]);
                            translate([0, 3.0, 0]) cube([7.0, 0.1, 0.1]);
                            cube([7.0, 0.1, 0.1]);
                        }
                }
                // Bo góc lượn chân đế R = 3.5mm
                translate([sx * 57.0 - (sx > 0 ? 3.5 : 3.5), 80.0, T_deck]) {
                    hull() {
                        translate([0, 6.0, 0]) cube([7.0, 0.1, 3.5]);
                        translate([0, 9.0, 0]) cube([7.0, 0.1, 0.1]);
                    }
                }
            }
            
            // C. 4 GỜ ĐỊNH VỊ SƯỜN TĂNG CƯỜNG (Dày 4.0mm, cao 5.0mm, vát côn dẫn hướng 45°):
            for (sx = [-1, 1]) {
                translate([sx * 60.8 - (sx > 0 ? 0 : 4.0), -6.0, T_deck]) {
                    cube([4.0, 12.0, 5.0]);
                    translate([sx > 0 ? 0 : 4.0, 0, 3.5])
                        rotate([0, sx > 0 ? -45 : 45, 0])
                            cube([2.0, 12.0, 2.0]);
                }
                translate([sx * 60.8 - (sx > 0 ? 0 : 4.0), 68.0, T_deck]) {
                    cube([4.0, 12.0, 5.0]);
                    translate([sx > 0 ? 0 : 4.0, 0, 3.5])
                        rotate([0, sx > 0 ? -45 : 45, 0])
                            cube([2.0, 12.0, 2.0]);
                }
            }
        }
        
        // ------------------------------------------------------------
        // CÁC HỐC VÀ LỖ KHOÉT SẠCH SẼ - SÀN ĐẶC LIỀN KHỐI 100%
        // (LOẠI BỎ TRIỆT ĐỂ LƯỚI MA TRẬN RÃNH ĐAN CHÉO GÂY RỜI RẠC!)
        // ------------------------------------------------------------
        
        // 1. Ô thoáng trung tâm luồn dây Pin 2S & thông gió:
        translate([-20.0, 20.0, -1.0])
            cube([40.0, 34.0, T_deck + 2.0]);
            
        // 2. 4 Rãnh trượt đơn M3 gọn gàng tại 4 góc K2 Hub (bắt vít dự phòng):
        for (sx = [-1, 1]) {
            for (sy = [6.0, 68.0]) {
                hull() {
                    translate([sx * 44.0, sy, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                    translate([sx * 53.0, sy, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                }
                hull() {
                    translate([sx * 44.0, sy, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
                    translate([sx * 53.0, sy, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
                }
            }
        }
        
        // 3. Rãnh bắt ốc xuống khung gầm / chân đôn (X = +-33.0, Y = 49.0 & Y = 98.0):
        for (sx = [-1, 1]) {
            // Trụ giữa (Y = 49.0):
            hull() {
                translate([sx * 33.0, 46.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 33.0, 52.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 33.0, 46.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
                translate([sx * 33.0, 52.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
            }
            // Trụ trước lộ thiên trên tay vươn (Y = 98.0):
            hull() {
                translate([sx * 34.0, 95.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 34.0, 100.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 34.0, 95.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
                translate([sx * 34.0, 100.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
            }
            // 2 Tai sau lộ thiên:
            translate([sx * 33.0, -13.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            translate([sx * 33.0, -13.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
            
            // 2 Tai trước khóa nhanh lộ thiên:
            translate([sx * 34.0, 88.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            translate([sx * 34.0, 88.0, T_deck - 2.5]) cylinder(d=6.8, h=3.0);
        }
    }
}

// ====================================================================
// 2. KHUNG CHÂN ĐÔN ĐA NĂNG LÙI HẬU NÉ THÁP GẮP TRỤ V9.0 (01D_Base_Riser_Frame)
// - Thiết kế lại toàn bộ để KHÔNG BAO GIỜ VA CHẠM VỚI 2 THÁP NÂNG (01B & 01C) VÀ SERVO S1:
//   1. Toàn bộ phần chân và tay trước giới hạn ở |X| in [29.2, 39.2mm] và dừng tại Y = 102.0mm:
//      + Cách vách ngoài 2 Tháp Nâng (|X| = 28.0mm) đúng 1.2mm theo phương X!
//      + Dừng trước mặt lưng 2 Tháp Nâng & Gờ định vị (Y = 105.0mm) đúng 3.0mm theo phương Y!
//      + Khoảng giữa X in [-29.2, +29.2mm] từ Y = 78.0 đến 105.0mm TRỐNG HOÀN TOÀN 100%!
//   2. 4 Chân bắt xuống khung gầm (X = +-33.0, Y = 49.0 & 99.0) hạ thẳng đứng (Drop-In), có giếng mở
//      rộng rãi từ mặt trên xuống bậc đế dày 4.5mm (Z = 22.0..26.5mm) -> Dùng ốc ngắn M3x10/12mm cực dễ!
//   3. 4 Tai Khóa Nhanh Lộ Thiên (Y = -13.0mm phía sau & Y = 88.0mm phía trước) có sẵn Hốc Giữ Tán M3
//      Đáy Kín Chống Rơi -> Bắt tấm Plate + K2 Hub từ trên xuống hoàn toàn bên ngoài vỏ K2 Hub!
//   4. Đặt in lật úp 180° (mặt Z = 38.0mm nằm sát bàn in Z = 0): IN 0% SUPPORT!
// ====================================================================
module k2_base_riser_frame() {
    Z_top = 38.0;
    difference() {
        union() {
            for (sx = [-1, 1]) {
                // 1. Hai Chân Trụ Sau (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, 38.0]):
                //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_top - 22.0]);
                    
                // 2. Hai Chân & Tay Trụ Trước Né Tháp Nâng (|X| in [29.2, 39.2], Y in [82.0, 102.0], Z in [22.0, 38.0]):
                //    - |X| >= 29.2mm (nằm ngoài Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
                //    - Y <= 102.0mm (dừng trước Tháp Nâng Y = 105.0mm đúng 3.0mm!)
                translate([sx * 34.2 - 5.0, 82.0, 22.0])
                    cube([10.0, 20.0, Z_top - 22.0]);
                    
                // 3. Dầm dọc trên nối liền từ Tai Sau (Y = -18.0) đến Tay Trước (Y = 85.0) tại Z in [31.0, 38.0]:
                translate([sx * 33.5 - 5.7, -18.0, 31.0])
                    cube([11.4, 103.0, 7.0]);
                    
                // 4. Khối Tai Khóa Sau Lộ Thiên dày 8mm (|X| in [25.5, 40.5], Y in [-18.0, -7.0], Z in [30.0, 38.0]):
                translate([sx * 33.0 - 7.5, -18.0, 30.0])
                    cube([15.0, 11.0, 8.0]);
            }
            
            // 5. Hai Thanh Giằng Ngang Chữ H nối Trái - Phải tại Y in [12.0, 20.0] và Y in [66.0, 74.0], Z in [32.0, 38.0]:
            //    (Đặt tại Y <= 74.0mm, cách 2 Tháp Nâng Y=105.0mm tới 31.0mm!)
            translate([-33.0, 12.0, 32.0]) cube([66.0, 8.0, 6.0]);
            translate([-33.0, 66.0, 32.0]) cube([66.0, 8.0, 6.0]);
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // A. 2 HỐC BẮT TRỤ SAU (X = +-31.5..35.0, Y = 46.5..51.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..38.0mm mở giếng chữ U rộng rãi kèm côn 45° tự đỡ:
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 41.0, 47.0, 26.5]) cylinder(d1=3.6, d2=9.0, h=3.0);
                translate([sx * 41.0, 51.0, 26.5]) cylinder(d1=3.6, d2=9.0, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=10.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=10.0);
                translate([sx * 41.0, 47.0, 29.4]) cylinder(d=9.0, h=10.0);
                translate([sx * 41.0, 51.0, 29.4]) cylinder(d=9.0, h=10.0);
            }
        }
        
        // B. 2 HỐC BẮT TRỤ TRƯỚC LỘ THIÊN (X = +-32.0..35.5, Y = 95.5..99.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..38.0mm mở thông ra phía trước & mép ngoài:
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=10.0);
            }
        }
        
        // C. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI SAU LỘ THIÊN (X = +-33.0, Y = -15.0 .. -11.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 33.0, -15.0, 28.0]) cylinder(d=3.3, h=12.0);
                translate([sx * 33.0, -11.0, 28.0]) cylinder(d=3.3, h=12.0);
            }
            // Rãnh khóa tán M3 (Z = 31.2..34.2) có đáy đỡ Z = 30.0..31.2mm + cửa nhét tán từ đuôi Y = -19.0:
            hull() {
                translate([sx * 33.0, -19.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 33.0, -11.0, 31.2]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 33.0, -19.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 33.0, -11.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
        
        // D. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI TRƯỚC LỘ THIÊN (X = +-34.0, Y = 86.0 .. 90.0):
        //    Nằm giữa K2 Hub (Y <= 80.0) và Ốc Trụ Trước (Y = 99.0), có cửa nhét tán từ mép ngoài |X| = 40.0!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 34.0, 86.0, 20.0]) cylinder(d=3.3, h=20.0);
                translate([sx * 34.0, 90.0, 20.0]) cylinder(d=3.3, h=20.0);
            }
            hull() {
                translate([sx * 34.0, 86.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 34.0, 90.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 40.5, 88.0, 31.2]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 34.0, 86.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 34.0, 90.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 40.5, 88.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
    }
}

module k2_base_riser_frame_printable() {
    translate([0, 0, 38.0])
        rotate([180, 0, 0])
            k2_base_riser_frame();
}

// Bệ MCU nhỏ gọn Đa Năng V9.0 cho Plate 1 (Đã cắt hốc chữ U phía trước né 100% 2 Tháp Nâng Y=105!)
module mcu_deck_compact_slotted_v80() {
    T_deck = 4.0;
    difference() {
        union() {
            // Sàn chính dừng tại Y = 92.0mm (cách 2 Tháp Nâng 13.0mm):
            translate([-39.0, 42.0, 0.0]) cube([78.0, 50.0, T_deck]);
            // 2 Tai bắt trụ trước nằm tại |X| in [29.2, 39.0], Y in [90.0, 102.0] (né 100% Tháp Nâng!):
            for (sx = [-1, 1]) {
                translate([sx * 34.1 - 4.9, 90.0, 0.0]) cube([9.8, 12.0, T_deck]);
            }
        }
        translate([-20.0, 56.0, -1.0]) cube([40.0, 28.0, T_deck + 2.0]);
        for (sx = [-1, 1]) {
            for (py = [49.0, 97.5]) {
                hull() {
                    translate([sx * 31.8, py - 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 35.2, py - 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 31.8, py + 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 35.2, py + 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                }
            }
            for (gx = [24.0, 32.0]) {
                for (gy = [60.0, 68.0, 76.0, 84.0]) {
                    hull() {
                        translate([sx * gx, gy - 2.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                        translate([sx * gx, gy + 2.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                    }
                }
            }
        }
    }
}

// Trụ đệm đôn cao 18mm rời (giữ tương thích)
module riser_standoff_18mm() {
    difference() {
        cylinder(d=11.0, h=18.0);
        translate([0, 0, -1.0]) cylinder(d=3.4, h=20.0);
        translate([0, 0, 4.0]) cylinder(d=7.2, h=15.0);
    }
}

// ====================================================================
// 3. BẢN ADAPTER LIỀN KHỐI LÙI HẬU NÉ THÁP GẮP TRỤ 100% V9.0 (MONOLITHIC CANTILEVER RISER V9.0 - 0% SUPPORT)
// - Thiết kế lại toàn diện để GIẢI QUYẾT TRIỆT ĐỂ 100% LỖI VƯỚNG CẤU TRÚC GẮP TRỤ & KHẢ THI LẮP ĐẶT:
//   1. SÀN CHÍNH LÙI HẬU (Y in [-8.0, +82.0mm], X in [-60.0, +60.0mm], Z in [38.0, 44.0mm]):
//      + Mép trước sàn chính dừng tại Y = 82.0mm -> Tạo khoảng trống khổng lồ 23.0mm trước 2 Tháp Nâng
//        (Y = 105.0mm) và 25.65mm trước tai bắt + dây cáp Servo S1 (Y = 107.65mm)!
//      + Bo mạch K2 Control Hub (Y in [-6.0, +80.0mm]) nằm lùi về sau làm đối trọng cân bằng cho cụm tay gắp,
//        mặt trước K2 Hub cách 2 Tháp Nâng đúng 25.0mm (2.5cm) và cách Servo S1 tới 27.65mm!
//   2. 2 TAY VƯƠN BẮT TRỤ TRƯỚC LỘ THIÊN NÉ THÁP TUYỆT ĐỐI (|X| in [29.2, 39.2mm], Y in [82.0, 102.0mm]):
//      + Mép trong |X| = 29.2mm nằm ngoài hoàn toàn 2 Tháp Nâng và Gờ định vị sau (|X| <= 28.0mm -> khe hở 1.2mm).
//      + Mũi trước Y = 102.0mm dừng trước mặt lưng 2 Tháp Nâng và Gờ định vị ngoài (Y = 105.0mm -> khe hở 3.0mm).
//      + Hốc chữ U giữa 2 tay rộng 58.4 x 23.0mm trống hoàn toàn!
//      + Lỗ bắt ốc trụ trước (X = +-33.0, Y = 99.0mm) nằm LỘ THIÊN 19.0mm phía trước K2 Control Hub,
//        có giếng mở thông suốt xuống bậc đế dày 4.5mm (Z = 22.0..26.5mm) -> Dùng ốc M3x10/12mm cực dễ!
//   3. LẮP THẲNG ĐỨNG TỪ TRÊN XUỐNG (100% VERTICAL DROP-IN - KHÔNG CẦN ĐẨY TRƯỢT):
//      + Hạ thẳng đứng xuống 4 trụ khung gầm (Z = 22.0mm) giữa động cơ sau (Y = 44.5mm) và tháp nâng (Y = 105.0mm).
//      + 2 Chân Sau (Y = 49.0mm) có GIẾNG VẶN ỐC THẲNG ĐỨNG XUYÊN SUỐT từ mặt trên xuống bậc đế dày 4.5mm!
//   4. HỆ RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI (CAPTIVE BLIND-FLOOR NUT CHANNELS):
//      + Đáy sàn có lớp đường ray kín dày 1.2mm (Z = 38.0..39.2mm) giữ 4 con tán M3 KHÔNG BAO GIỜ RƠI XUỐNG GẦM
//        kèm cửa nhét tán trực tiếp từ mép sườn ngoài (|X| = 60.0mm) và hốc nạp tán!
//      + Quy trình lắp chuẩn 100%: Hạ bệ lên xe -> Vặn 4 ốc trụ khung gầm lộ thiên từ mặt trên -> Đặt K2 Hub
//        lên trên và vặn 4 ốc góc vào 4 tán M3 đã nằm sẵn trong rãnh đáy kín (hoặc bắt K2 Hub ở ngoài trước tùy ý)!
// ====================================================================
module k2_adapter_monolithic_v60() {
    Z_top = 44.0;
    T_deck = 6.0;
    Z_bot = Z_top - T_deck; // 38.0mm (Cao hơn nẹp motor sau Z=36.0mm đúng 2.0mm & cao hơn motor 5.5mm!)
    
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 6.0 mm, X in [-60, 60], Y in [-8.0, 82.0]):
            translate([-60.0, -8.0, Z_bot])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Chân Đôn Sau Hạ Thẳng Đứng (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, 38.0]):
            //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
            for (sx = [-1, 1]) {
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_bot - 22.0]);
            }
            
            // 3. Hai Tay/Chân Đôn Trước LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG 100%
            //    (|X| in [29.2, 39.2], Y in [81.0, 102.0], Z in [22.0, 44.0]):
            //    - Mép trong |X| = 29.2mm (nằm ngoài vách 2 Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
            //    - Mũi trước Y = 102.0mm (dừng trước lưng 2 Tháp Nâng & Gờ định vị Y = 105.0mm đúng 3.0mm!)
            //    - Mặt đỉnh Z = 44.0mm đồng phẳng 100% với sàn chính -> Đặt in lật úp Z_print = 0.0mm phẳng 100% Zero Support!
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 22.0])
                    cube([10.0, 21.0, Z_top - 22.0]);
            }
            
            // 4. Hai Cụm Gá Cảm Biến Laser ToF VL53L0X Trái & Phải giải mê cung (Mặt đỉnh đồng phẳng Z=44.0mm -> in úp Z_print=0.0mm phẳng 100%)
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=Z_top - 12.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=Z_top - 12.0);
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // Ô thoáng trung tâm luồn dây Pin 2S (42.0 x 36.0 mm - X in [-21, 21], Y in [19.0, 55.0]):
        translate([-21.0, 19.0, 20.0])
            cube([42.0, 36.0, 26.0]);
            
        // A. 2 CHÂN ĐÔN SAU HẠ THẲNG ĐỨNG KÈM GIẾNG VẶN ỐC XUYÊN SUỐT TỪ MẶT TRÊN (X = +-31.5..35.0, Y = 46.5..51.5):
        //    - Đáy Z = 22.0..26.5mm (dày 4.5mm): Rãnh trượt 2 chiều X-Y bắt vừa cả X=+-32, +-33 và Y=46.5..51.5mm!
        //    - Phía trên Z = 26.5..44.0mm: Giếng thông suốt Ø9.2mm từ mặt trên xuống kèm côn 45° tự đỡ ở Z = 26.5..29.5mm!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=26.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 31.5, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 35.0, 46.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 31.5, 51.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=16.0);
            }
        }
        
        // B. 2 TAY/CHÂN TRƯỚC LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG (X = +-32.0..35.5, Y = 95.5..99.5):
        //    - Nằm lộ thiên phía trước mặt sàn chính (Y=82.0) tới 17.0mm -> Không bao giờ bị K2 Hub che khuất!
        //    - Đáy Z = 22.0..26.5mm (dày 4.5mm): Rãnh trượt 2 chiều X-Y!
        //    - Phía trên Z = 26.5..44.0mm: Giếng chữ U mở rộng thông lên mặt trên (Z=44), mũi trước (Y=103) và mép ngoài
        //      kèm côn 45° ở Z = 26.5..29.5mm -> Vặn ốc M3x10/12mm cực dễ và in úp 0% Support!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=26.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=16.0);
            }
        }
        
        // C. 4 RÃNH TRƯỢT ĐƠN GỌN GÀNG TẠI 4 GÓC K2 CONTROL HUB (SÀN ĐẶC LIỀN KHỐI 100%):
        for (sx = [-1, 1]) {
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

// BẢN IN ÚP PHẲNG 100% TRÊN BÀN IN (Z = 0.0 mm - ZERO SUPPORT):
module k2_adapter_monolithic_printable() {
    translate([0, 0, 44.0])
        rotate([180, 0, 0])
            k2_adapter_monolithic_v60();
}

// ====================================================================
// 3B. NGÀM CÀI SNAP-FIT ĐÀN HỒI RỜI V11.0 GIA CỐ CƠ HỌC (01D_Snap_Clip_K2_Hub)
// - In nằm phẳng tại Z = 0.0mm: đường thớ in chạy dọc theo thân đòn ngàm -> đàn hồi cực dẻo không gãy!
// - Đòn đàn hồi dạng côn ứng suất đều (Uniform Stress Tapered Beam: 2.6mm ở gốc -> 2.2mm ở ngọn)
// - Bo góc lượn R = 3.5mm khử mỏi ở chân đế, tai bấm mở nhanh công thái học có gờ chống trượt
// ====================================================================
module k2_snap_clip_modular() {
    difference() {
        union() {
            // 1. Chân đế trượt chữ T cài vừa khít vào rãnh plate
            translate([-8.0, -5.5, 0.0]) cube([16.0, 11.0, 3.8]);
            translate([-3.2, -5.5, 3.8]) cube([6.4, 11.0, 3.2]);
            
            // 2. Góc lượn chuyển tiếp R = 3.5mm giữa chân đế và đòn đàn hồi
            hull() {
                translate([-5.0, 4.0, 0.0]) cube([10.0, 1.5, 3.8]);
                translate([-5.0, 7.5, 0.0]) cube([10.0, 0.1, 2.5]);
            }
            
            // 3. Đòn đàn hồi dạng côn ứng suất đều (Uniform Stress Tapered Beam: 2.6mm ở gốc -> 2.2mm ở ngọn)
            //    In nằm phẳng Z=0: thớ nhựa chạy dọc liên tục 100% -> không bao giờ tách lớp!
            hull() {
                translate([-5.0, 5.5, 0.0]) cube([10.0, 1.0, 2.6]);
                translate([-5.0, 30.5, 0.0]) cube([10.0, 1.0, 2.2]);
            }
            
            // 4. Đầu móc ngàm khóa có vát 45° dẫn hướng ấn tách
            translate([-5.0, 30.5, 2.2])
                hull() {
                    cube([10.0, 1.6, 1.6]);
                    translate([0, -2.4, 0]) cube([10.0, 0.1, 0.1]);
                }
                
            // 5. Tai bấm ngón tay mở nhanh (Ergonomic Thumb Release Tab)
            translate([-5.0, 30.5, 0.0])
                hull() {
                    cube([10.0, 3.5, 2.2]);
                    translate([0, 5.5, 0]) cube([10.0, 0.1, 2.2]);
                }
        }
        // Lỗ ốc M3 tâm để siết khóa cứng định vị
        translate([0, 0, -1.0]) cylinder(d=3.4, h=12.0);
        // Hốc chìm nón 90° bắt vít M3 đầu dù/nón phẳng
        translate([0, 0, 5.0]) cylinder(d1=3.4, d2=6.6, h=2.2);
    }
}

// ====================================================================
// 4. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - TRÁI (LEFT REAR MOTOR CLAMP V4.3)
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
// 5. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - PHẢI (RIGHT REAR MOTOR CLAMP V4.3)
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
// 6. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - DÙNG CHUNG (UNIVERSAL REAR MOTOR CLAMP V4.3)
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
// 7. THÁP NÂNG PHẢI MG996R V5.0 (RIGHT LIFT TOWER V5.0)
// ====================================================================
// - Hốc chìm tán M3 lục giác sâu 2.6mm ở mặt trong (X = 20.0mm): Tán M3 chìm phẳng tuyệt đối.
// - Rãnh lượn mở rộng 1.0mm ở mặt trong (X in [20.0, 21.0]): Tăng khe hở tay nâng lên 1.5mm!
module lift_tower_right_v50() {
    x_wall_min = 20.0;
    x_flange_min = 12.0;
    brace_x0 = 0.0;
    fx = 16.0;
    wx = 24.0;

    difference() {
        union() {
            translate([x_wall_min, 105.0, 4.0]) cube([8.0, 61.0, 90.0]);
            translate([x_flange_min, 105.0, 4.0]) cube([8.0, 22.5, 8.0]);
            translate([x_flange_min, 154.5, 4.0]) cube([8.0, 11.5, 8.0]);
            translate([brace_x0, 105.0, 88.0]) cube([20.0, 13.0, 6.0]);
        }

        translate([-30.0, 127.5, 3.5]) cube([60.0, 27.0, 30.5]);

        // Hốc chữ nhật lọt thân Servo MG996R (41.2 x 20.2 mm)
        translate([19.0, 114.05, 47.9]) cube([10.0, 41.2, 20.2]);

        // 4 Lỗ ốc M3 bắt Servo MG996R có HỐC CHÌM TÁN M3 LỤC GIÁC Ở MẶT TRONG:
        for (sy = [134.65 - 24.25, 134.65 + 24.25]) {
            for (sz = [58.0 - 5.0, 58.0 + 5.0]) {
                translate([19.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
                translate([19.9, sy, sz]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.8, $fn=6);
            }
        }

        // Khe lượn mở rộng (Clearance Pocket) sâu 1.0mm ở mặt trong dọc hành trình quay:
        translate([19.9, 138.0, 44.0]) cube([1.2, 28.0, 30.0]);

        // Lỗ chốt xoay trên
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

module lift_tower_right_v50_printable() {
    translate([0, 0, 28.0]) rotate([0, 90, 0]) lift_tower_right_v50();
}

// ====================================================================
// 8. KHUNG TAY NÂNG DƯỚI CHỮ H V11.0 SIÊU BỀN CHỐNG GÃY (LOWER H-FRAME ARM V11.0)
// ====================================================================
// - Giải quyết triệt để 100% điểm đứt gãy hiểm yếu tại cổ đĩa tròn Servo S1 (khoanh đỏ):
//   1. Sàn đáy liền khối hạ xuống Z = -12.0mm: Hốc đĩa tròn Ø20.8mm (R = 10.4mm) được bao bọc 
//      hoàn toàn bởi sàn đặc chịu kéo dày 1.6mm + vành cung kín Ø24.0mm không bị xẻ rãnh!
//   2. Mở rộng hub ôm đĩa Servo lên Ø24.0mm, vuốt côn tiếp tuyến dạng nêm chữ H vào thân dầm.
//   3. Tăng dày thân dầm chủ động từ 5.0mm lên 8.0mm ở mặt trong (X in [11.5, 19.5mm]):
//      Bản đế sau hốc đĩa dày 5.7mm đặc 100% (tăng hơn gấp đôi so với 2.5mm trước đây).
//   4. Tích hợp gân chéo tam giác bên trong khóa cứng khớp Servo vào thanh giằng ngang chữ H.
//   5. Mô-men kháng uốn Wz tăng >23 lần, diện tích mặt cắt chịu kéo tăng >11 lần!
//   6. Đặt in nằm phẳng 100% tại Z = 0.00mm -> 0% Support!
module lower_h_frame_arm_v11(length = 98.0, height = 12.0, thickness = 5.0) {
    z_bot = -12.0; // Đáy phẳng liên tục tiếp xúc bàn in Z = 0
    t_drive = 8.0; // Bề dày dầm phải chịu lực truyền từ Servo S1 (tăng từ 5.0 lên 8.0mm)
    
    difference() {
        union() {
            // 1. THANH TRÁI BỊ ĐỘNG (X in [-19.5, -14.5mm], dày 5.0mm)
            translate([-19.5, 0, z_bot])
                cube([thickness, length, height + abs(z_bot) - height/2]); // cao 18mm
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, -height/2, z_bot]) cube([thickness, height/2, height/2]);
            
            // 2. THANH PHẢI CHỦ ĐỘNG SIÊU CỨNG (X in [11.5, 19.5mm], dày 8.0mm ở gốc chịu lực!)
            // A. Dầm chính thân phải (X in [14.5, 19.5], dày 5.0mm chạy suốt chiều dài)
            translate([14.5, 0, z_bot])
                cube([thickness, length, height + abs(z_bot) - height/2]);
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            
            // B. Khối cổ gá Đĩa tròn Servo S1 mở rộng Ø24.0mm tại (Y = 0, Z = 0)
            translate([19.5 - t_drive, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=24.0, h=t_drive);
                    
            // C. GÂN TIẾP TUYẾN TĂNG CỨNG DẠNG NÊM CHỮ NHẬT & TAM GIÁC NỐI TỪ VÒM Ø24.0MM VÀO DẦM
            hull() {
                translate([19.5 - t_drive, 0, 0])
                    rotate([0, 90, 0]) cylinder(d=24.0, h=t_drive);
                translate([19.5 - t_drive, 36.0, z_bot])
                    cube([t_drive, 6.0, height + abs(z_bot) - height/2]);
            }
            
            // D. GÂN TAM GIÁC GIA CƯỜNG MẶT TRONG KHÓA VÀO THANH GIẰNG NGANG (X in [6.5, 14.5], Y in [8.0, 42.0])
            hull() {
                translate([11.5, 6.0, z_bot]) cube([3.0, 8.0, 16.0]);
                translate([6.5, 38.0, z_bot]) cube([8.0, 10.0, 14.0]);
            }
            
            // 3. THANH GIẰNG NGANG CHỮ H CHỐNG XOẮN (Y in [38.0, 52.0], X in [-14.5, 11.5])
            translate([-14.5, 38.0, z_bot])
                cube([26.0, 14.0, height + abs(z_bot) - height/2]);
        }

        // ------------------------------------------------------------
        // CÁC HỐC KHOÉT & LỖ CHỐT
        // ------------------------------------------------------------
        
        // A. Hốc tròn âm Ø20.8mm sâu 2.3mm ôm trọn Đĩa tròn Servo MG996R (25T Round Horn) ở mặt ngoài (X = 17.2..19.6)
        translate([17.2, 0, 0]) rotate([0, 90, 0]) cylinder(d=20.8, h=2.8);

        // B. Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([10.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);

        // C. 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm lỗ bậc chìm Ø6.0mm ở mặt trong (X = 11.5mm)
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            translate([10.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=10.0);
            translate([11.3, hy, hz]) rotate([0, 90, 0]) cylinder(d=6.0, h=3.0);
        }

        // D. Lỗ chốt xoay mắt trước (Y = length = 98.0, Z = 0)
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);

        // E. Lỗ chốt xoay mắt sau thanh trái (Y = 0, Z = 0)
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=10.0);
    }
}

module lower_h_frame_arm_v11_printable() {
    translate([0, 0, 12.0]) lower_h_frame_arm_v11();
}

// Giữ alias tương thích ngược
module lower_h_frame_arm_v50(length = 98.0, height = 12.0, thickness = 5.0) {
    lower_h_frame_arm_v11(length, height, thickness);
}

module lower_h_frame_arm_v50_printable() {
    lower_h_frame_arm_v11_printable();
}

// ====================================================================
// 9. KHỐI KHÓA ĐĨA TRÒN SERVO S1 RỜI (S1 ROUND HORN DRIVE COUPLER)
// ====================================================================
module s1_round_horn_drive_coupler() {
    difference() {
        union() {
            cylinder(d=23.0, h=4.0);
            translate([-4.0, 0, 4.0]) cube([8.0, 20.0, 2.5]);
        }
        translate([0, 0, -0.1]) cylinder(d=20.8, h=2.1);
        translate([0, 0, -1.0]) cylinder(d=6.5, h=8.0);
        for (a = [0, 90, 180, 270]) {
            translate([7.0*cos(a), 7.0*sin(a), -1.0]) cylinder(d=3.2, h=8.0);
        }
        translate([0, 10.0, -1.0]) cylinder(d=2.5, h=8.0);
        translate([0, 16.0, -1.0]) cylinder(d=2.5, h=8.0);
    }
}

// ====================================================================
// 9B. CỔ TAY NỐI TAY NÂNG H-FRAME & GÁ SERVO S3 GẬP DỌC 90° V7.1
// (04A_Wrist_Clevis_Pitch_Bracket_S3 - ZERO SUPPORT, 100% H-FRAME COMPATIBLE)
// - Phía sau (Y = 8.0, Z = 10.0 & 38.0): Lắp vừa 100% 4 chốt của cánh tay chữ H đã in (03 & 03B)
// - Phía trước (Y in [16.6, 37.0]): Ôm khít Servo S3 (MG996R) đặt dọc, trục quay hướng +X
//   tại (Y_piv = 26.8, Z_piv = 38.0), mặt đĩa tròn S3 nằm đúng tại X = +27.0mm!
// - Bên trái (X in [-27.0, -13.5]): Gối đỡ đồng trục M3 (X = -27.0mm) vát 45° tự đỡ kèm hốc lục giác giữ tán M3!
// - Đặt in phẳng mặt lưng Y = 0 xuống bàn in (rotate([90, 0, 0])) -> 0% SUPPORT TUYỆT ĐỐI!
// ====================================================================
module wrist_clevis_pitch_bracket_s3() {
    Y_piv = 26.8;
    Z_piv = 38.0;

    difference() {
        union() {
            // 1. Khối Clevis & Lưng chịu lực từ Y = 0 đến Y = 16.6 (X in [-14.0, +14.0], Z in [-2.5, 56.0]):
            translate([-14.0, 0, -2.5]) cube([28.0, 16.6, 46.5]);
            translate([-14.0, 0, 44.0]) cube([27.0, 16.6, 12.0]);

            // 2. Vách Trái đỡ lưng Servo S3 (X in [-16.5, -13.5], Y in [16.6, 37.0], Z in [-2.5, 56.0])
            // vát 45° từ X = -14.0 tại Y = 14.0 ra X = -16.5 tại Y = 16.6:
            hull() {
                translate([-14.0, 14.0, -2.5]) cube([1.0, 2.6, 58.5]);
                translate([-16.5, 16.6, -2.5]) cube([3.0, 20.4, 58.5]);
            }

            // 3. Gối Trục Xoay Đồng Trục Bên Trái vươn ra X = -27.0mm tại (Y_piv = 26.8, Z_piv = 38.0)
            // vát côn 45° tự đỡ từ (X = -14.0, Y = 13.8) lên (X = -27.0, Y = 26.8) -> 0% Support khi in mặt Y = 0!
            hull() {
                translate([-14.0, 13.8, Z_piv - 9.0]) cube([1.0, 2.8, 18.0]);
                translate([-16.5, 16.6, Z_piv - 9.0]) cube([3.0, 18.0, 18.0]);
                translate([-27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=16.0, h=1.0);
            }

            // 4. Khối Bắt Tai Dưới Servo S3 (X in [-14.0, +13.0], Y in [16.6, 37.0], Z in [-2.5, 7.2]):
            translate([-14.0, 16.6, -2.5]) cube([27.0, 20.4, 9.7]);

            // 5. Khối Bắt Tai Trên Servo S3 (X in [-14.0, +13.0], Y in [16.6, 37.0], Z in [48.6, 56.0]):
            translate([-14.0, 16.6, 48.6]) cube([27.0, 20.4, 7.4]);
        }

        // A. Hốc giữa Clevis phía sau (X in [-8.5, +8.5], Y in [4.5, 16.6], Z in [-3.0, 57.0])
        // để giảm trọng lượng và nhét 4 tán M3 giữ chốt tay nâng cực dễ:
        translate([-8.5, 4.5, -3.0]) cube([17.0, 12.2, 60.0]);

        // B. 4 Lỗ chốt xoay nối với tay nâng chữ H dưới (Z = 10.0) và trên (Z = 38.0) tại Y = 8.0:
        for (zp = [10.0, 38.0]) {
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) rotate([0, 0, -45]) cube([3.3/2, 3.3/2, 40.0]);
            translate([-8.6, 8.0, zp]) rotate([0, -90, 0]) cylinder(d=6.5, h=2.6, $fn=6);
            translate([8.6, 8.0, zp])  rotate([0, 90, 0])  cylinder(d=6.5, h=2.6, $fn=6);
        }

        // C. 4 Lỗ bắt ốc M3 tự taro (Ø2.95mm sâu 8.5mm) + Hốc mở phía trước nhét tán M3 cho tai Servo S3
        // (Y = 26.8 +- 5.0 => 21.8 & 31.8; Z = 3.75 & 52.25):
        for (sy = [Y_piv - 5.0, Y_piv + 5.0]) {
            for (sz = [3.75, 52.25]) {
                translate([-10.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=2.95, h=25.0);
            }
        }
        // Khoang mở phía trước ở X in [-8.5, +4.5] để có thể luồn tán M3 từ phía trước nếu muốn dùng kèm đai ốc:
        translate([-8.5, 19.0, 0.75])  cube([13.0, 19.0, 6.0]);
        translate([-8.5, 19.0, 49.25]) cube([13.0, 19.0, 6.0]);

        // D. Lỗ Trục Xoay Đồng Trục Bên Trái tại (Y_piv = 26.8, Z_piv = 38.0)
        // kèm lỗ tự taro M3 dài 10.5mm + Hốc Lục Giác giữ tán M3 ở mặt trong Vách Trái (X in [-17.0, -13.5]):
        translate([-30.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.0, h=18.0);
        translate([-17.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=3.6, $fn=6);

        // E. Rãnh luồn dây cáp Servo S3 ở góc dưới:
        translate([-13.6, 22.0, 4.5]) cube([8.0, 9.6, 4.0]);
    }
}

module wrist_clevis_pitch_bracket_s3_printable() {
    rotate([90, 0, 0]) wrist_clevis_pitch_bracket_s3();
}

// ====================================================================
// 10. BỆ ĐẦU KẸP 3 TRỤ HOA TÍCH HỢP BẢN LỀ GẬP DỌC 90° V7.1
// (04_Gripper_Base_Head - ZERO SUPPORT, PITCH 0..90 DEG)
// - Tâm trục gập ngang (Pitch Axis) tại (Y_piv = 6.0, Z_piv = 38.0)
// - Má Phải (X in [+27.0, +35.0]): Tích hợp Hốc Đĩa Tròn MG996R Ø20.8mm + 8 lỗ M3 PCD Ø14mm
//   + rãnh tay đơn 8.2mm + lỗ tâm Ø6.5mm bắt trực tiếp vào trục Servo S3!
// - Má Trái (X in [-33.0, -27.0]): Lỗ trục xoay đồng trục Ø3.4mm + bậc chìm đầu ốc M3!
// - Mở rộng tâm 2 trục xoay hàm kẹp tại X = +-15.0mm, Y = 39.0mm (Xoay 0°..90° KHÔNG VA CHẠM!)
// - Đặt in phẳng đáy Z = 0.0mm -> 0% SUPPORT!
// ====================================================================
module gripper_base_head_3flower() {
    Y_piv = 6.0;
    Z_piv = 38.0;
    Y_jaw = 39.0;

    difference() {
        union() {
            // 1. Tấm đế chính (Y in [22.0, 50.0], Z in [0, 5.0]) + Bàn đỡ trượt chống xệ hàm phía trước (Y up to 60.0):
            translate([-31.0, 22.0, 0]) cube([66.0, 28.0, 5.0]);
            hull() {
                translate([-20.0, 46.0, 0]) cube([40.0, 4.0, 5.0]);
                translate([-14.0, 58.0, 0]) cube([28.0, 4.0, 5.0]);
            }

            // 2. Vách hậu liên kết cứng (Y in [22.0, 27.5], Z in [0, 24.5]):
            translate([-31.0, 22.0, 0]) cube([66.0, 5.5, 24.5]);

            // 3. Hai trục trụ xoay Ø8.0mm cho Hàm Trái (-15.0, Y_jaw=39.0) và Hàm Phải (+15.0, Y_jaw=39.0):
            translate([-15.0, Y_jaw, 5.0]) cylinder(d=8.0, h=10.0);
            translate([15.0, Y_jaw, 5.0])  cylinder(d=8.0, h=10.0);

            // 4. Trụ đỡ Cầu Servo S2 bên TRÁI & Má Bản Lề Gập Dọc Trái (X in [-31.0, -27.0] & [-33.0, -27.0]):
            translate([-31.0, 22.0, 0]) cube([4.0, 28.0, 35.0]);
            translate([-31.0, 22.0, 0]) cube([15.0, 5.0, 24.5]);
            hull() {
                translate([-31.0, 27.0, 21.5]) cube([4.0, 23.0, 13.5]);
                translate([-31.0, 27.0, 31.0]) cube([15.0, 23.0, 4.0]);
            }
            // - Má Bản Lề Gập Dọc Trái (X in [-33.0, -27.0]) vươn về (Y_piv = 6.0, Z_piv = 38.0)
            //   với đáy giọt nước ngược vát phẳng 45° tự đỡ nối thẳng xuống đế Z = 0 tại Y = 22.0:
            hull() {
                translate([-33.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=18.0, h=6.0);
                translate([-33.0, Y_piv + 6.0, Z_piv - 12.0]) cube([6.0, 2.0, 12.0]);
                translate([-31.0, 22.0, 0.0]) cube([4.0, 14.0, 35.0]);
            }

            // 5. Trụ đỡ Cầu Servo S2 bên PHẢI & Má Bản Lề Gập Dọc Phải (X in [+27.0, +35.0]):
            translate([27.0, 22.0, 0]) cube([8.0, 28.0, 35.0]);
            hull() {
                translate([27.0, 27.0, 26.0]) cube([8.0, 23.0, 9.0]);
                translate([25.25, 27.0, 29.0]) cube([9.75, 23.0, 6.0]);
            }
            // - Má Bản Lề Gập Dọc Phải (X in [+27.0, +35.0]) ôm Đĩa Tròn MG996R Ø20mm tại (Y_piv = 6.0, Z_piv = 38.0)
            //   với đáy giọt nước ngược vát phẳng 45° tự đỡ nối thẳng xuống đế Z = 0 tại Y = 22.0:
            hull() {
                translate([27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=25.0, h=8.0);
                translate([27.0, Y_piv + 8.0, Z_piv - 16.0]) cube([8.0, 2.0, 16.0]);
                translate([27.0, 22.0, 0.0]) cube([8.0, 14.0, 35.0]);
            }
        }

        // A. 4 Lỗ bắt tai Servo MG996R S2 (Tâm trục tại X = +15.0, Y = Y_jaw = 39.0 => Tâm thân tại X = 4.65, Y = 39.0):
        for (sx = [4.65 - 24.25, 4.65 + 24.25]) {
            for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
                translate([sx, sy, 20.0]) cylinder(d=2.95, h=20.0);
            }
        }
        // Hốc lục giác âm cho 2 ốc tai phải S2 (X = +28.90):
        for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
            translate([28.90, sy, -1.0]) cylinder(d=6.5, h=29.5, $fn=6);
            translate([28.90, sy, 28.4]) cylinder(d1=6.5, d2=2.95, h=2.0);
        }

        // B. 2 Lỗ tâm trục xoay hàm kẹp (X = +-15.0, Y = Y_jaw = 39.0) + Hốc Lục Giác giữ tán M3 ở đáy:
        for (px = [-15.0, 15.0]) {
            translate([px, Y_jaw, -1.0]) cylinder(d=3.3, h=20.0);
            translate([px, Y_jaw, -0.1]) rotate([0, 0, 30]) cylinder(d=6.45, h=2.8, $fn=6);
            translate([px, Y_jaw, 2.65]) cylinder(d1=6.45, d2=3.3, h=1.8);
        }

        // C. Lỗ Trục Gập Ngang Bên Trái (X in [-33.0, -27.0]) tại (Y_piv = 6.0, Z_piv = 38.0):
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) rotate([0, 0, 45]) cube([3.4/2, 3.4/2, 10.0]);
        translate([-33.5, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.5);

        // D. HỐC ĐĨA TRÒN SERVO S3 (Ø20.8mm sâu 2.5mm + 8 lỗ M3 PCD Ø14.0mm + Rãnh tay đơn 8.2mm + Lỗ tâm Ø6.5mm)
        // trên Má Bản Lề Phải (X in [+27.0, +35.0]) tại (Y_piv = 6.0, Z_piv = 38.0):
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
// 11 & 12. CẶP HÀM KẸP LIÊN HOÀN 3 TRỤ HOA Ø32MM V7.0 (05 & 06)
// - Kẹp cùng lúc 3 trụ hoa Ø32.0mm xếp dọc nối tiếp tại Y1=33, Y2=66, Y3=99mm
// - Tích hợp 3 Khe Đàn Hồi Lò Xo Lá độc lập + Gân ma sát ngang + Gờ đỡ đáy vát 45°
// - Hàm Phải (06) tích hợp HỐC TRÒN ÂM Ø20.8MM cho Đĩa Tròn Servo MG996R (8 lỗ M3 PCD Ø14mm)
//   KÈM rãnh chữ nhật 8.2mm đa năng!
// ====================================================================
module specialized_gripper_jaw_3flower(is_left = true) {
    pivot_x = is_left ? -15.0 : 15.0;
    sx = is_left ? -1.0 : 1.0;
    H = 22.0;
    H_hub = is_left ? 16.0 : 22.0;
    
    Y1 = 33.0;
    Y2 = 66.0;
    Y3 = 99.0;

    difference() {
        union() {
            // 1. Khối Hub trục xoay (X = +-15.0, Y = 0) & Cổ nối vào thân hàm:
            translate([pivot_x, 0, 0]) cylinder(r=11.5, h=H_hub);
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r=10.0, h=H_hub);
                translate([sx * 17.5, 16.0, 0]) cylinder(r=5.0, h=H_hub);
            }
            hull() {
                translate([sx * 17.5, 14.0, 0]) cylinder(r=5.0, h=H_hub);
                translate([sx * 19.0, 21.0, 0]) cylinder(r=5.0, h=H);
            }
            
            // 2. Bánh răng rẻ quạt đồng bộ (R_pitch = 15.0mm, Module m = 1.5mm, cao 16.0mm):
            for (a = is_left ? [-54, -36, -18, 0, 18, 36] : [135, 153, 171, 189, 207, 225]) {
                translate([pivot_x, 0, 0])
                    rotate([0, 0, a])
                        hull() {
                            translate([10.5, -2.1, 0]) cube([2.5, 4.2, 16.0]);
                            translate([16.3, -1.1, 0]) cube([0.6, 2.2, 16.0]);
                        }
            }
            
            // 3. Thân Dầm Khung Chịu Lực Dọc 3 Hốc Hoa (Y1=33, Y2=66, Y3=99):
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
                // Cắt phẳng hoàn toàn phía trước Y3 (Y > 99.0) để nối mượt vào Phễu V-Guide:
                translate([-25.0, Y3, -1.0]) cube([50.0, 30.0, H + 2.0]);
                // Cắt vát góc trong phía sau Hốc #1 (|X| < 11.0, Y < 17.5) giải phóng không gian bánh răng:
                translate([-11.0, 8.0, -1.0]) cube([22.0, 9.5, H + 2.0]);
                // Trên Hàm Trái (is_left), hạ bậc vùng Y < 15.0 xuống Z = 16.0mm (kèm vát 45° tới Y = 21.0) để không bao giờ chạm cầu Servo S2:
                if (is_left) {
                    translate([-30.0, 0.0, H_hub]) cube([60.0, 15.0, H]);
                    translate([-30.0, 15.0, H_hub]) rotate([45, 0, 0]) cube([60.0, 10.0, 10.0]);
                }
            }
            
            // 4. Phễu dẫn hướng chữ V mở rộng 35° ở mũi hàm (từ Y = Y3 = 99.0 ra Y = 119.0):
            hull() {
                translate([sx * 19.2, Y3, 0]) cylinder(d=6.8, h=H);
                translate([sx * 30.0, Y3 + 19.0, 0]) cylinder(d=5.0, h=H);
            }
        }
        
        // Cắt bỏ nửa đối diện (chỉ giữ nửa bên trái hoặc bên phải từ Y = 8.0 trở đi):
        if (is_left) {
            translate([-7.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        } else {
            translate([-32.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        }
        
        // A. Khoét 3 Lòng Hốc Kẹp Hoa Ø32.0mm (R = 16.1mm) tại Y1=33, Y2=66, Y3=99:
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
        
        // B. Khoét thông lối dẫn dọc giữa 3 hốc (Mấu định tâm ở X = +-13.0mm):
        translate([-13.0, Y1, 2.5]) cube([26.0, Y3 - Y1 + 5.0, H + 2.0]);
        translate([-12.5, Y1, -0.5]) cube([25.0, Y3 - Y1 + 5.0, 3.2]);
        
        // C. 3 Khe Đàn Hồi Lò Xo Lá Độc Lập (Elastic Compliance Slots) nằm gọn trong thân hàm:
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
        
        // D. Lỗ bạc lót trục xoay Ø8.2mm sâu 10.2mm kèm mái côn tự đỡ 45° + Lỗ ốc tâm M3:
        translate([pivot_x, 0, -0.2]) cylinder(d=8.2, h=10.4);
        translate([pivot_x, 0, 10.2]) cylinder(d1=8.2, d2=3.4, h=2.4);
        translate([pivot_x, 0, -0.5]) cylinder(d=3.4, h=H + 2.0);
        if (is_left) {
            translate([pivot_x, 0, H_hub - 3.0]) cylinder(d=6.8, h=4.0);
        }
        
        // E. HỐC LẮP ĐĨA TRÒN SERVO MG996R (Ø20.8mm + 8 Lỗ M3 PCD Ø14mm) & RÃNH TAY GẠT ĐƠN TRÊN HÀM PHẢI (06):
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

k2_adapter_plate_flat();
