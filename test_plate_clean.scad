
$fn = 36;
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
// 1. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V10.0 (01D_K2_Hub_Adapter_Plate V10.0)
// TÍCH HỢP TOÀN DIỆN:
// - CƠ CHẾ NGÀM CÀI SNAP-FIT ĐÀN HỒI CHO K2 CONTROL HUB (QUICK-SNAP RETAINING SYSTEM)
// - CỤM 2 GÁ CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X ĐO TƯỜNG GIẢI MÊ CUNG
// - KIẾN TRÚC LÙI HẬU CANTILEVER NÉ 100% CẤU TRÚC GẮP TRỤ (THÁP NÂNG + SERVO S1)
// - RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI + HỆ LƯỚI LỖ 8MM
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
            }
            // B. Hai ngàm cài đàn hồi có lẫy bấm phía trước K2 Hub (Y = +80.0mm, X = +-56.0mm):
            for (sx = [-1, 1]) {
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
            }
            // C. 4 Gờ định vị góc ôm khít K2 Control Hub (121.2 x 86.2 mm) chống xô lệch X-Y:
            for (sx = [-1, 1]) {
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), -6.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), 70.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
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
