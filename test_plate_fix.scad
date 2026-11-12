$fn = 36;

// ====================================================================
// CỤM GÁ CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X ĐO TƯỜNG GIẢI MÊ CUNG V10.0
// Nửa bên Phải (+X), sử dụng mirror([1,0,0]) cho bên Trái (-X)
// Đảm bảo đối xứng tuyệt đối 100%, không bị lỗi âm kích thước cube()!
// ====================================================================
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

// ====================================================================
// 1. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V10.0 (01D_K2_Hub_Adapter_Plate V10.0)
// ====================================================================
module k2_adapter_plate_flat() {
    T_deck = 6.0;
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 6.0 mm, X in [-60, 60], Y in [-8, 82])
            translate([-60.0, -8.0, 0.0])
                cube([120.0, 90.0, T_deck]);
                
            // 1b. Gân bệ sàn mở rộng mép sườn sau (|X| in [57.0, 63.5], Y in [-8.0, 6.0], Z in [0, T_deck])
            // Đỡ liền khối 100% cho 2 gờ định vị sau K2 Hub, loại bỏ hoàn toàn hiện tượng floating!
            for (sx = [-1, 1]) {
                translate([sx > 0 ? 57.0 : -63.5, -8.0, 0.0])
                    cube([6.5, 14.0, T_deck]);
                // Vát góc chuyển tiếp mềm mại 45 độ về phía trước sườn
                hull() {
                    translate([sx > 0 ? 57.0 : -63.5, 6.0, 0.0]) cube([6.5, 0.1, T_deck]);
                    translate([sx > 0 ? 59.9 : -60.0, 10.0, 0.0]) cube([0.1, 0.1, T_deck]);
                }
            }
                
            // 2. Hai Tai Bắt Ốc Lộ Thiên Phía Sau (X in [+-25.0, +-41.0], Y in [-18.0, -8.0])
            for (sx = [-1, 1]) {
                translate([sx * 33.0 - 8.0, -18.0, 0.0])
                    cube([16.0, 11.0, T_deck]);
            }
            
            // 3. Hai Tay Vươn Bắt Trụ Trước & Khóa Nhanh Lộ Thiên (|X| in [29.2, 39.2], Y in [81.0, 102.0])
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 0.0])
                    cube([10.0, 21.0, T_deck]);
            }
            
            // 4. Hai Cụm Gá Cảm Biến Khoảng Cách Laser ToF VL53L0X Trái & Phải giải mê cung
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=0.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=0.0);
            
            // 5. CƠ CHẾ NGÀM CÀI SNAP-FIT ĐÀN HỒI CHO K2 CONTROL HUB (QUICK-SNAP SYSTEM):
            // A. Hai ngàm móc giữ đuôi K2 Hub cố định (Y = -6.0mm, X = +-42.0mm)
            for (sx = [-1, 1]) {
                translate([sx * 42.0 - 7.0, -8.0, T_deck]) {
                    cube([14.0, 3.5, 12.0]);
                    translate([0, 3.5, 10.5])
                        hull() {
                            cube([14.0, 0.1, 1.5]);
                            translate([0, 1.8, 0]) cube([14.0, 0.1, 1.5]);
                        }
                }
                // Gân tam giác gia cường chân ngàm sau
                translate([sx * 42.0 - 6.0, -4.5, T_deck])
                    hull() {
                        cube([12.0, 0.1, 5.0]);
                        translate([0, 3.0, 0]) cube([12.0, 0.1, 0.1]);
                    }
            }
            // B. Hai ngàm cài đàn hồi có lẫy bấm phía trước K2 Hub (Y = +80.0mm, X = +-56.0mm):
            for (sx = [-1, 1]) {
                translate([sx > 0 ? 56.5 : -61.5, 80.0, T_deck]) {
                    cube([5.0, 2.2, 14.0]);
                    // Mấu ngàm cài nhô về sau (-Y) 1.6mm kèm vát dốc 45° ấn tách tự động
                    translate([0, -1.6, 11.5])
                        hull() {
                            cube([5.0, 1.6, 1.2]);
                            translate([0, 1.6, 2.5]) cube([5.0, 0.1, 0.1]);
                        }
                    // Tai bấm tì ngón tay (Thumb push tab) mở nhanh nhô về trước (+Y) 3mm
                    translate([0, 2.2, 11.5])
                        hull() {
                            cube([5.0, 0.1, 2.5]);
                            translate([0, 2.8, 0]) cube([5.0, 0.1, 2.5]);
                        }
                }
            }
            // C. 4 Gờ định vị góc ôm khít K2 Control Hub (121.2 x 86.2 mm) chống xô lệch X-Y:
            for (sx = [-1, 1]) {
                // 2 gờ sau (Y in [-6.0, 4.0]): nằm trọn trên bệ sàn mở rộng Z = T_deck
                translate([sx > 0 ? 60.8 : -63.3, -6.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
                // 2 gờ trước (Y in [67.0, 72.0]): nằm trọn trên sàn đặc của sensor pod,
                // hoàn toàn tách biệt với rãnh luồn cáp (Y = 74..79) -> ZERO OVERHANG / ZERO SUPPORT!
                translate([sx > 0 ? 60.8 : -63.3, 67.0, T_deck])
                    cube([2.5, 5.0, 3.0]);
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
