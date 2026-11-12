$fn = 32;

// ====================================================================
// TIỆN ÍCH HỆ RÃNH ĐƯỜNG RAY TÁN M3 ĐÁY KÍN CHỐNG RƠI V10.0
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

module side_nut_entry_port_z0(sx, y_pos, T_deck = 6.0, nut_w = 5.8) {
    hull() {
        translate([sx * 54.0, y_pos, 1.15]) cylinder(d=nut_w, h=2.8);
        translate([sx * 61.0, y_pos, 1.15]) cylinder(d=nut_w, h=2.8);
    }
    hull() {
        translate([sx * 54.0, y_pos, 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
        translate([sx * 61.0, y_pos, 3.9]) cylinder(d1=nut_w, d2=3.4, h=1.2);
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
// - Đặt ở sườn Trái (sx = -1) và sườn Phải (sx = +1) tại Y in [68.0, 84.0mm]
// - Nằm trọn vẹn trong khoảng hở giữa 2 bánh Mecanum (Y=72..102mm)
// - Bề ngang giới hạn tại |X| <= 68.8mm -> Cách mặt trong bánh xe Mecanum (|X|=71.0mm) > 2.2mm!
// - Tích hợp ngàm cài snap-fit giữ PCB VL53L0X (25 x 11mm) + Cửa sổ bắn laser 90° sườn & lỗ ốc M2.5/M3
// ====================================================================
module vl53l0x_maze_sensor_pod(is_left = true, T_deck = 6.0) {
    sx = is_left ? -1 : 1;
    difference() {
        union() {
            // Cánh vươn chịu lực nối liền mép sàn (X = sx*60..sx*68.8, Y = 66.0..82.5, Z = 0..14.0mm)
            hull() {
                translate([sx * 60.0, 66.0, 0.0]) cube([sx * 0.1, 16.5, T_deck]);
                translate([sx * 68.2, 67.5, 0.0]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 68.2, 81.0, 0.0]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([sx * 60.0, 82.5, 0.0]) cube([sx * 0.1, 0.1, T_deck]);
            }
            // 2 Ngàm cài Snap-fit đàn hồi giữ mép bo mạch VL53L0X (Y = 70.0 và Y = 78.5)
            for (py = [70.0, 78.5]) {
                translate([sx * 68.6, py - 2.2, 0.0])
                    cube([sx * 1.8, 4.4, T_deck + 7.5]);
                // Đầu móc ngàm khóa có vát dốc 45° dẫn hướng ấn tách
                translate([sx * 68.6, py - 2.2, T_deck + 6.0])
                    hull() {
                        cube([sx * 1.8, 4.4, 1.5]);
                        translate([-sx * 1.0, 0, 0]) cube([sx * 0.1, 4.4, 1.0]);
                    }
            }
            // Gờ tì sau lưng bo mạch VL53L0X
            translate([sx * 66.2, 68.0, 0.0])
                cube([sx * 1.4, 13.0, T_deck + 5.5]);
        }
        
        // Khe cắm bo mạch VL53L0X đứng (rộng 2.0mm cho PCB dày 1.6mm + dung sai, dài 25.0mm)
        translate([sx * 67.6, 67.5, 1.5])
            cube([sx * 2.1, 14.0, 15.0]);
            
        // Cửa sổ quang học bắn tia laser ToF 90° vuông góc vách tường mê cung (11.0 x 6.5mm kèm vát loe 35°)
        translate([sx * 64.5, 68.5, 2.8])
            cube([sx * 8.0, 11.0, 6.5]);
        hull() {
            translate([sx * 66.0, 68.5, 2.8]) cube([sx * 0.1, 11.0, 6.5]);
            translate([sx * 70.0, 67.5, 1.5]) cube([sx * 0.1, 13.0, 9.2]);
        }
        
        // 2 Lỗ ốc M2.5 / M3 bắt vít dự phòng (khoảng cách tâm 18.0mm: Y = 67.5 và Y = 81.5)
        translate([sx * 63.5, 67.5, -1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 81.5, -1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 63.5, 67.5, 1.5]) cylinder(d=6.0, h=12.0);
        translate([sx * 63.5, 81.5, 1.5]) cylinder(d=6.0, h=12.0);
        
        // Rãnh luồn cáp I2C 4P ngầm xuyên vào sàn plate
        translate([sx * 59.0, 71.0, 1.0])
            cube([sx * 10.0, 7.0, 3.5]);
    }
}

// ====================================================================
// TẤM BỆ ADAPTER PHẲNG ĐA NĂNG V10.0 (01D_K2_Hub_Adapter_Plate V10.0)
// TÍCH HỢP:
// 1. NGÀM CÀI SNAP-FIT ĐÀN HỒI KHÓA NHANH K2 CONTROL HUB (QUICK-SNAP LATC HES)
// 2. CỤM 2 GÁ CẢM BIẾN KHOẢNG CÁCH LASER TOF VL53L0X ĐO TƯỜNG GIẢI MÊ CUNG
// 3. KIẾN TRÚC LÙI HẬU CANTILEVER NÉ 100% CẤU TRÚC GẮP TRỤ (THÁP NÂNG + SERVO S1)
// 4. RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI + HỆ LƯỚI LỖ 8MM
// ====================================================================
module k2_adapter_plate_flat_v10() {
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
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck);
            
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
            //    Đặt ở 2 góc trước ngoài cùng (không vướng giắc Motor/Encoder/Servo)
            for (sx = [-1, 1]) {
                translate([sx * 57.0 - (sx > 0 ? 0 : 5.0), 80.0, T_deck]) {
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
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), -6.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), 70.0, T_deck])
                    cube([2.5, 10.0, 3.0]);
            }
        }
        
        // Ô thoáng trung tâm (42 x 36 mm, X in [-21, 21], Y in [19, 55])
        translate([-21.0, 19.0, -1.0])
            cube([42.0, 36.0, T_deck + 2.0]);
            
        // Tổ hợp rãnh đường ray khóa tán M3 đáy kín 2 chiều
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
            
            // Rãnh bắt trụ sau khung gầm (Y = 49.0)
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
            // Rãnh bắt trụ trước khung gầm (Y = 99.0)
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
            
            // 4 Rãnh khóa nhanh lên khung đôn
            slot_m3_counterbored_top(sx * 31.5, -13.0, sx * 34.5, -13.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 33.0, -15.0, sx * 33.0, -11.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 32.5, 88.0, sx * 35.5, 88.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 34.0, 86.0, sx * 34.0, 90.0, 0.0, T_deck);
            
            // Hệ lưới lỗ 8mm
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

// Module Ngàm cài đàn hồi rời dùng cho bản Monolithic (01D_Snap_Clip_K2_Hub)
// In nằm phẳng tại Z = 0.0mm (lớp in chạy dọc thớ nhựa -> đàn hồi gấp 10 lần không gãy)
module k2_snap_clip_modular() {
    difference() {
        union() {
            // Chân đế trượt cài vào rãnh plate (bản đế chữ T dày 4.0mm)
            translate([-8.0, -6.0, 0.0]) cube([16.0, 12.0, 3.8]);
            // Đòn đàn hồi đứng (hoặc nằm phẳng khi in)
            translate([-5.0, 6.0, 0.0]) cube([10.0, 26.0, 2.4]);
            // Đầu móc ngàm khóa kèm vát dốc 45°
            translate([-5.0, 30.5, 2.4])
                hull() {
                    cube([10.0, 1.5, 1.4]);
                    translate([0, -2.0, 0]) cube([10.0, 0.1, 0.1]);
                }
            // Tai bấm ngón tay mở nhanh
            translate([-5.0, 30.5, 0.0])
                hull() {
                    cube([10.0, 3.5, 2.4]);
                    translate([0, 5.0, 0]) cube([10.0, 0.1, 2.4]);
                }
        }
        // Lỗ ốc M3 bắt khóa chốt nếu cần
        translate([0, 0, -1.0]) cylinder(d=3.3, h=6.0);
    }
}

k2_adapter_plate_flat_v10();
