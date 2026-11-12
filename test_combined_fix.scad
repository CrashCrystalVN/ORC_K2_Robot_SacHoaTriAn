$fn = 36;

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
                
            // 1b. Gân bệ sàn mở rộng mép sườn sau (|X| in [57.0, 65.0], Y in [-8.0, 6.0], Z in [0, T_deck])
            // Đỡ liền khối 100% cho 2 gờ định vị sau K2 Hub, loại bỏ hoàn toàn hiện tượng floating!
            for (sx = [-1, 1]) {
                translate([sx > 0 ? 57.0 : -65.0, -8.0, 0.0])
                    cube([8.0, 14.0, T_deck]);
                hull() {
                    translate([sx > 0 ? 57.0 : -65.0, 6.0, 0.0]) cube([8.0, 0.1, T_deck]);
                    translate([sx > 0 ? 59.9 : -60.0, 10.0, 0.0]) cube([0.1, 0.1, T_deck]);
                }
            }
                
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
            
            // 5. CƠ CẤU NGÀM VÀ GỜ HÃM GIA CỐ CƠ HỌC TOÀN DIỆN
            // A. HAI GỜ HÃM ĐUÔI GIA CỐ CỰC DÀY CÓ GÂN TAM GIÁC:
            for (sx = [-1, 1]) {
                translate([sx * 45.0 - 7.5, -11.5, T_deck]) {
                    cube([15.0, 5.5, 11.5]);
                    translate([0, 5.5, 9.8])
                        hull() {
                            cube([15.0, 0.1, 1.7]);
                            translate([0, 2.0, 0.5]) cube([15.0, 0.1, 1.2]);
                            translate([0, 0, 1.7]) cube([15.0, 0.1, 0.1]);
                        }
                    translate([0, -2.5, 0])
                        hull() {
                            cube([15.0, 0.1, 0.1]);
                            translate([0, 2.5, 0]) cube([15.0, 0.1, 11.5]);
                            translate([0, 2.5, 11.5]) cube([15.0, 0.1, 0.1]);
                        }
                }
                translate([sx * 45.0 - 7.5, -11.5, T_deck]) {
                    hull() {
                        translate([0, -2.5, 0]) cube([15.0, 0.1, 0.1]);
                        translate([0, 0, 0]) cube([15.0, 0.1, 3.5]);
                    }
                }
            }
            
            // B. HAI GỜ HÃM GÓC TRƯỚC GIA CỐ CỰC DÀY:
            for (sx = [-1, 1]) {
                translate([sx * 57.0 - (sx > 0 ? 3.5 : 3.5), 80.0, T_deck]) {
                    cube([7.0, 6.0, 12.0]);
                    translate([0, -1.8, 10.2])
                        hull() {
                            cube([7.0, 1.8, 1.8]);
                            translate([0, 1.8, 1.8]) cube([7.0, 0.1, 0.1]);
                        }
                    translate([0, 6.0, 0])
                        hull() {
                            cube([7.0, 0.1, 12.0]);
                            translate([0, 3.0, 0]) cube([7.0, 0.1, 0.1]);
                            cube([7.0, 0.1, 0.1]);
                        }
                }
                translate([sx * 57.0 - (sx > 0 ? 3.5 : 3.5), 80.0, T_deck]) {
                    hull() {
                        translate([0, 6.0, 0]) cube([7.0, 0.1, 3.5]);
                        translate([0, 9.0, 0]) cube([7.0, 0.1, 0.1]);
                    }
                }
            }
            
            // C. 4 GỜ ĐỊNH VỊ SƯỜN TĂNG CƯỜNG (Dày 4.0mm, cao 5.0mm, vát côn dẫn hướng 45°):
            for (sx = [-1, 1]) {
                // 2 Gờ sau: Đặt trên bệ sàn mở rộng Z = T_deck
                translate([sx * 60.8 - (sx > 0 ? 0 : 4.0), -6.0, T_deck]) {
                    cube([4.0, 12.0, 5.0]);
                    translate([sx > 0 ? 0 : 4.0, 0, 3.5])
                        rotate([0, sx > 0 ? -45 : 45, 0])
                            cube([2.0, 12.0, 2.0]);
                }
                // 2 Gờ trước: Đặt trên cánh vươn sensor pod (Y in [67.0, 72.0]), tách rời rãnh cáp Y=74..79:
                translate([sx * 60.8 - (sx > 0 ? 0 : 4.0), 67.0, T_deck]) {
                    cube([4.0, 5.0, 5.0]);
                    translate([sx > 0 ? 0 : 4.0, 0, 3.5])
                        rotate([0, sx > 0 ? -45 : 45, 0])
                            cube([2.0, 5.0, 2.0]);
                }
            }
        }
        
        // ------------------------------------------------------------
        // CÁC HỐC VÀ LỖ KHOÉT SẠCH SẼ - SÀN ĐẶC LIỀN KHỐI 100%
        // (MẶT ĐÁY Z = 0.0 PHẲNG TUYỆT ĐỐI, TIẾP XÚC 100% VỚI BÀN IN)
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

k2_adapter_plate_flat();
