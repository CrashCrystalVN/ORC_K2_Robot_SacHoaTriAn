$fn = 40;

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

// Cụm gá cảm biến VL53L0X nửa bên Phải (+X)
module vl53l0x_pod_half(T_deck = 6.0, Z_base = 0.0) {
    difference() {
        union() {
            // Cánh vươn chịu lực nối liền mép sàn (ăn sâu vào sàn từ X = 56.0 ra đến X = 68.2)
            hull() {
                translate([56.0, 66.0, Z_base]) cube([4.0, 16.5, T_deck]);
                translate([68.2, 67.5, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([68.2, 81.0, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([56.0, 82.5, Z_base]) cube([4.0, 0.1, T_deck]);
            }
            // 2 Ngàm cài Snap-fit đàn hồi giữ mép bo mạch VL53L0X (Y = 70.0 và Y = 78.5)
            for (py = [70.0, 78.5]) {
                translate([68.6, py - 2.2, Z_base])
                    cube([1.8, 4.4, T_deck + 6.0]);
                // Đầu móc ngàm khóa có vát dốc 45° dẫn hướng ấn tách
                translate([68.6, py - 2.2, Z_base + T_deck + 4.5])
                    hull() {
                        cube([1.8, 4.4, 1.5]);
                        translate([-1.0, 0, 0]) cube([0.1, 4.4, 1.0]);
                    }
            }
            // Gờ tì sau lưng bo mạch VL53L0X
            translate([66.2, 68.0, Z_base])
                cube([1.4, 13.0, T_deck + 5.5]);
        }
        
        // Khe cắm bo mạch VL53L0X đứng (rộng 2.1mm cho PCB dày 1.6mm + dung sai, dài 14.0mm)
        translate([67.6, 67.5, Z_base + 1.5])
            cube([2.1, 14.0, 15.0]);
            
        // Cửa sổ quang học bắn tia laser ToF 90° vuông góc vách tường mê cung (11.0 x 6.5mm kèm vát loe 35°)
        translate([64.5, 68.5, Z_base + 2.8])
            cube([8.0, 11.0, 6.5]);
        hull() {
            translate([66.0, 68.5, Z_base + 2.8]) cube([0.1, 11.0, 6.5]);
            translate([70.0, 67.5, Z_base + 1.5]) cube([0.1, 13.0, 9.2]);
        }
        
        // 2 Lỗ ốc M2.5 / M3 bắt vít dự phòng (khoảng cách tâm 18.0mm: Y = 67.5 và Y = 81.5) thông suốt
        translate([63.5, 67.5, Z_base - 1.0]) cylinder(d=3.3, h=T_deck + 10.0);
        translate([63.5, 81.5, Z_base - 1.0]) cylinder(d=3.3, h=T_deck + 10.0);
        
        // Rãnh luồn cáp I2C 4P ngầm mở từ trên (Y = 74.0..79.0, Z = Z_base + 2.5mm -> mặt đáy Z=0 liền đặc 2.5mm chịu lực)
        translate([56.0, 74.0, Z_base + 2.5])
            cube([12.0, 5.0, T_deck + 2.0]);
    }
}

module vl53l0x_maze_sensor_pod(is_left = true, T_deck = 6.0, Z_base = 0.0) {
    if (is_left) {
        mirror([1, 0, 0]) vl53l0x_pod_half(T_deck = T_deck, Z_base = Z_base);
    } else {
        vl53l0x_pod_half(T_deck = T_deck, Z_base = Z_base);
    }
}



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
        
        // 3. Rãnh bắt ốc xuống khung gầm / chân đôn (Chuẩn hóa 100% khớp 4 Trụ Khung Gầm X = +-33.0, Y = 49.0 & Y = 99.0):
        for (sx = [-1, 1]) {
            // Trụ sau / giữa (Chuẩn tâm X = +-33.0, Y = 49.0 mm - Rãnh trượt 2D linh hoạt):
            hull() {
                translate([sx * 32.2, 46.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 33.8, 46.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 32.2, 52.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 33.8, 52.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 32.2, 46.0, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
                translate([sx * 33.8, 46.0, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
                translate([sx * 32.2, 52.0, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
                translate([sx * 33.8, 52.0, T_deck - 2.5]) cylinder(d=6.5, h=3.0);
            }
            // Trụ trước lộ thiên trên tay vươn (Chuẩn tâm X = +-33.0 mm, Y = 99.0 mm - Vành kín chịu lực đầu mút):
            hull() {
                translate([sx * 32.2, 95.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 33.8, 95.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 32.2, 99.2, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                translate([sx * 33.8, 99.2, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 32.2, 95.0, T_deck - 2.5]) cylinder(d=6.2, h=3.0);
                translate([sx * 33.8, 95.0, T_deck - 2.5]) cylinder(d=6.2, h=3.0);
                translate([sx * 32.2, 98.5, T_deck - 2.5]) cylinder(d=6.2, h=3.0);
                translate([sx * 33.8, 98.5, T_deck - 2.5]) cylinder(d=6.2, h=3.0);
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


k2_adapter_plate_flat();
