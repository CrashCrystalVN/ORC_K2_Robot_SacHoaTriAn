"""
generate_redesigned_parts.py
Script thiết kế lại và xuất các file 3D STL tối ưu V5.0:
1. Tấm bắt bo mạch ORC K2 Control Hub (K2 Adapter Plate V5.0 & Monolithic Riser V5.0):
   - Đôn cao 18.0mm (tạo khe hở an toàn 4.0mm vượt nắp kẹp motor sau Z=36mm, triệt tiêu 100% va chạm).
   - 4 Hốc nhét tán M3 ngang (Side-entry Nut Slots) trượt từ mép ngoài x=+-63mm vào, đáy kín 1.2mm.
   - Trình tự lắp ráp chuẩn 2 bước: Bắt bệ xuống khung gầm trước (lỗ chìm Ø6.5mm) -> Đặt K2 Hub và siết ốc từ trên xuống vào tán ngang mà không cần luồn tay xuống gầm!
2. 2 Nẹp ôm động cơ GA25 phía sau (Rear Motor Clamps Left / Right / Universal V4.3):
   - Vòm bán nguyệt Ø26.2mm kèm miệng loe 45° (Ø27.5mm) ôm trọn mọi loại hộp số giảm tốc to.
   - Mép trong thu hẹp suốt chiều dài về X = +-40.5mm (cách trụ MCU cũ 2.5mm tuyệt đối).
3. Cụm Servo S1 nâng hạ & Cánh tay đòn V5.0 (Chuẩn Đĩa tròn Servo MG996R & Chống cấn ốc 100%):
   - Tháp nâng phải (01C V5.0): Hốc chìm tán M3 lục giác sâu 2.6mm ở mặt trong + Rãnh lượn mở rộng 1.0mm -> Triệt tiêu 100% cấn ốc với tay nâng.
   - Tay nâng dưới chữ H (03 V5.0): Hốc tròn âm Ø20.8mm ôm khít đĩa tròn MG996R + 8 lỗ M3 trên PCD Ø14mm + lỗ tâm Ø6.5mm tra vít spline + in phẳng 100% tại Z=0.
   - Khối khóa đĩa tròn S1 rời (08 V5.0): Khớp nối nhanh dành cho ai đã in tay nâng cũ, cắm vừa rãnh chữ nhật cũ mà không cần in lại cả cánh tay!
"""

import os
import subprocess
import struct
import math
import re

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OPENSCAD_COM = r"C:\Program Files\OpenSCAD\openscad.com"

os.makedirs(STL_DIR, exist_ok=True)

# ====================================================================
# OPENSCAD DEFINITIONS
# ====================================================================
SCAD_LIBRARY = """$fn = 64;

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

// ====================================================================
// 2. KHUNG CHÂN ĐÔN ĐA NĂNG 2S2P CAO ĐỘ LỌT LÒNG 42.0MM (01D_Base_Riser_Frame)
// - Thiết kế nâng cấp ĐẶC CHẾ CHO KHỐI PIN ĐÓNG SẴN 2S2P (Dày 38mm, Rộng 38mm, Dài 70mm):
//   1. Nâng cao độ sàn tấm K2 Hub lên Z_top = 46.0mm (hoặc 48.0mm):
//      + Sàn khung gầm tại Z = 4.0mm -> Khoảng sáng gầm lọt lòng H_clear = 46.0 - 4.0 = 42.0mm!
//      + Dung sai rộng rãi: Pin 38mm + Dây đai Velcro 2mm + Khe hở an toàn 2mm = 42.0mm!
//   2. HAI THANH GIẰNG NGANG NÉ PIN 2S2P 100%:
//      + Giằng sau đặt tại Y in [-18.0, -10.0mm], Z in [Z_top - 6.0, Z_top] (nằm sau pin)
//      + Giằng trước đặt tại Y in [84.0, 92.0mm], Z in [Z_top - 6.0, Z_top] (nằm trước pin)
//      + Toàn bộ khoang giữa X in [-26.5, +26.5mm], Y in [-10.0, 84.0mm] (dài 94mm, rộng 53mm)
//        THÔNG SUỐT 100% THEO PHƯƠNG Z, pin 2S2P rút ra cắm vào hoặc nhấc lên cực kỳ dễ dàng!
//   3. 4 Chân bắt xuống khung gầm (X = +-33.0, Y = 49.0 & 99.0) hạ thẳng đứng (Drop-In):
//      + Đáy dày 4.5mm (Z = 22.0..26.5mm) dùng ốc M3x10/12mm chuẩn.
//      + Giếng đứng mở rộng Ø7.6..8.5mm thông suốt từ mặt trên xuống -> vặn ốc cực thoáng!
//   4. 4 Tai Khóa Nhanh Lộ Thiên (Y = -13.0mm phía sau & Y = 88.0mm phía trước) có Hốc Giữ Tán M3
//      Đáy Kín Chống Rơi -> Bắt tấm Plate + K2 Hub từ trên xuống hoàn toàn bên ngoài vỏ K2 Hub!
//   5. Đặt in lật úp 180° (mặt Z_top nằm sát bàn in Z = 0): IN 0% SUPPORT!
// ====================================================================
module k2_base_riser_frame(Z_top = 46.0) {
    difference() {
        union() {
            for (sx = [-1, 1]) {
                // 1. Hai Chân Trụ Sau (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, Z_top]):
                //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_top - 22.0]);
                    
                // 2. Hai Chân & Tay Trụ Trước Né Tháp Nâng (|X| in [29.2, 39.2], Y in [82.0, 102.0], Z in [22.0, Z_top]):
                //    - |X| >= 29.2mm (nằm ngoài Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
                //    - Y <= 102.0mm (dừng trước Tháp Nâng Y = 105.0mm đúng 3.0mm!)
                translate([sx * 34.2 - 5.0, 82.0, 22.0])
                    cube([10.0, 20.0, Z_top - 22.0]);
                    
                // 3. Dầm dọc trên nối liền từ Tai Sau (Y = -18.0) đến Tay Trước (Y = 85.0) tại Z in [Z_top - 7.0, Z_top]:
                translate([sx * 33.5 - 5.7, -18.0, Z_top - 7.0])
                    cube([11.4, 103.0, 7.0]);
                    
                // 4. Khối Tai Khóa Sau Lộ Thiên dày 8mm (|X| in [25.5, 40.5], Y in [-18.0, -7.0], Z in [Z_top - 8.0, Z_top]):
                translate([sx * 33.0 - 7.5, -18.0, Z_top - 8.0])
                    cube([15.0, 11.0, 8.0]);
            }
            
            // 5. Hai Thanh Giằng Ngang Chữ H Né 100% Khối Pin 2S2P:
            //    - Giằng Sau: Y in [-17.0, -9.0mm], Z in [Z_top - 6.0, Z_top]
            //    - Giằng Trước: Y in [84.0, 92.0mm], Z in [Z_top - 6.0, Z_top]
            //    -> Toàn bộ khoang trung tâm dài 93mm x rộng 53mm không bị cản trở!
            translate([-33.0, -17.0, Z_top - 6.0]) cube([66.0, 8.0, 6.0]);
            translate([-33.0, 84.0, Z_top - 6.0])  cube([66.0, 8.0, 6.0]);
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // A. 2 HỐC BẮT TRỤ SAU (X = +-33.0, Y = 47.5..50.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..Z_top mở giếng thẳng đứng Ø7.6mm
        for (sx = [-1, 1]) {
            // Lỗ trượt ốc M3 qua đáy dày 4.5mm (Z = 22.0..26.5mm):
            hull() {
                translate([sx * 33.0, 47.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 33.0, 50.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            // Nón chuyển tiếp tự đỡ 45° từ lỗ M3 lên giếng đầu ốc:
            hull() {
                translate([sx * 33.0, 47.5, 26.5]) cylinder(d1=3.6, d2=7.6, h=2.5);
                translate([sx * 33.0, 50.5, 26.5]) cylinder(d1=3.6, d2=7.6, h=2.5);
            }
            // Giếng đứng thả ốc M3 & lục giác vặn thẳng đứng từ trên xuống (Z = 28.9..Z_top+1):
            hull() {
                translate([sx * 33.0, 47.5, 28.9]) cylinder(d=7.6, h=Z_top - 27.9);
                translate([sx * 33.0, 50.5, 28.9]) cylinder(d=7.6, h=Z_top - 27.9);
            }
        }
        
        // B. 2 HỐC BẮT TRỤ TRƯỚC LỘ THIÊN (X = +-32.0..35.5, Y = 95.5..99.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..Z_top mở thông ra phía trước & mép ngoài:
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
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
            }
        }
        
        // C. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI SAU LỘ THIÊN (X = +-33.0, Y = -15.0 .. -11.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 33.0, -15.0, Z_top - 10.0]) cylinder(d=3.3, h=12.0);
                translate([sx * 33.0, -11.0, Z_top - 10.0]) cylinder(d=3.3, h=12.0);
            }
            // Rãnh khóa tán M3 có đáy đỡ 1.2mm + cửa nhét tán từ đuôi Y = -19.0:
            hull() {
                translate([sx * 33.0, -19.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 33.0, -11.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 33.0, -19.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 33.0, -11.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
        
        // D. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI TRƯỚC LỘ THIÊN (X = +-34.0, Y = 86.0 .. 90.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 12.0]) cylinder(d=3.3, h=14.0);
                translate([sx * 34.0, 90.0, Z_top - 12.0]) cylinder(d=3.3, h=14.0);
            }
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 34.0, 90.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 40.5, 88.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 34.0, 90.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 40.5, 88.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
    }
}

module k2_base_riser_frame_printable() {
    translate([0, 0, 46.0])
        rotate([180, 0, 0])
            k2_base_riser_frame(Z_top = 46.0);
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

// Trụ đệm đôn cao 24mm rời cho Pin 2S2P (H_clear = 42.0mm)
module riser_standoff_24mm_2s2p(h = 24.0) {
    difference() {
        cylinder(d=11.0, h=h);
        translate([0, 0, -1.0]) cylinder(d=3.4, h=h + 2.0);
        translate([0, 0, 5.0]) cylinder(d=7.2, h=h);
    }
}

// ====================================================================
// TRỤ ĐÔN ĐA NĂNG CÀI 2 TÁN LỤC GIÁC M3 (DUAL-NUT STANDOFF M3 ARCHITECTURE)
// Hốc cài 2 tán ngang DIN 934 (5.80 x 2.75mm), bắt 2 bu-lông M3 độc lập từ 2 đầu,
// bệ chịu lực dày 3.5mm mỗi đầu, lỗ xuyên suốt Ø3.5mm, vát phẳng D-flat né motor sau.
// ====================================================================
module dual_nut_standoff_m3(h = 26.0, od = 11.6, d_flat_y = -5.3) {
    r = od / 2.0;
    slot_w = 5.80;
    slot_h = 2.75;
    slot_depth = 3.25;
    base_t = 3.50;
    top_t = 3.50;
    bore_d = 3.50;
    ch = 0.50;

    difference() {
        union() {
            cylinder(d1 = od - 2.0*ch, d2 = od, h = ch);
            translate([0, 0, ch]) cylinder(d = od, h = h - 2.0*ch);
            translate([0, 0, h - ch]) cylinder(d1 = od, d2 = od - 2.0*ch, h = ch);
        }
        translate([-od, -od + d_flat_y, -1.0])
            cube([2.0*od, od, h + 2.0]);
        translate([0, 0, -1.0])
            cylinder(d = bore_d, h = h + 2.0);
        translate([0, 0, -0.01])
            cylinder(d1 = bore_d + 1.0, d2 = bore_d, h = ch + 0.02);
        translate([0, 0, h - ch - 0.01])
            cylinder(d1 = bore_d, d2 = bore_d + 1.0, h = ch + 0.02);

        // Hốc cài tán dưới:
        translate([-slot_depth, -slot_w/2.0, base_t])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        translate([r - 0.5, -slot_w/2.0 - 0.5, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([0, 0, base_t + slot_h - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);

        // Hốc cài tán trên:
        translate([-slot_depth, -slot_w/2.0, h - top_t - slot_h])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        translate([r - 0.5, -slot_w/2.0 - 0.5, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([0, 0, h - top_t - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);
    }
}

// Trụ đệm đôn cao 26mm rời cho Pin 2S2P (Cài 2 tán M3 kép)
module riser_standoff_26mm_2s2p(h = 26.0) {
    dual_nut_standoff_m3(h = h, od = 11.6, d_flat_y = -5.3);
}

// Trụ đệm đôn cao 44mm nguyên khối cho Pin 2S2P (Cài 2 tán M3 kép)
module riser_standoff_44mm_2s2p(h = 44.0) {
    dual_nut_standoff_m3(h = h, od = 11.6, d_flat_y = -5.3);
}

// ====================================================================
// 3. BẢN ADAPTER LIỀN KHỐI 2S2P CAO ĐỘ LỌT LÒNG 42.0MM (01D_K2_Control_Hub_Riser_Adapter_Monolithic)
// - Thiết kế ĐẶC CHẾ CHO KHỐI PIN ĐÓNG SẴN 2S2P (Dày 38mm, Rộng 38mm, Dài 70mm):
//   1. Nâng cao độ đáy sàn lọt lòng Z_bot = 46.0mm (Sàn xe Z=4.0mm -> H_clear = 42.0mm!):
//      + Đủ chỗ hoàn hảo cho Pin dày 38mm + Dây Velcro 2mm + Khe hở an toàn 2mm!
//      + Mặt sàn K2 Hub tại Z_top = 51.0mm, đỉnh K2 Hub tại Z = 77.0mm < Tâm xoay tháp nâng (Z = 78.0mm)!
//   2. Ô thoáng trung tâm mở rộng 44.0 x 44.0mm (X in [-22, 22], Y in [18, 62]):
//      + Thoát nhiệt tối đa cho Pin 2S2P và chip ESP32-S3
//      + Luồn trực tiếp cáp nguồn silicone to XT30/XT60 và dây cân bằng
//   3. Hai Chân Sau & Hai Tay Trước hạ thẳng đứng (Drop-In) né 100% tháp nâng & servo S1
//   4. Hai Cụm Gá Laser ToF VL53L0X đo tường giải mê cung tích hợp hai bên sườn
//   5. Đặt in lật úp Z_print = 0.0mm: Phẳng 100%, ZERO SUPPORT!
// ====================================================================
module k2_adapter_monolithic_v60(Z_bot = 46.0, T_deck = 5.0) {
    Z_top = Z_bot + T_deck; // 51.0mm
    
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 5.0 mm, X in [-60, 60], Y in [-8.0, 82.0]):
            translate([-60.0, -8.0, Z_bot])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Chân Đôn Sau Hạ Thẳng Đứng (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, Z_bot]):
            //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
            for (sx = [-1, 1]) {
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_bot - 22.0]);
            }
            
            // 3. Hai Tay/Chân Đôn Trước LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG 100%
            //    (|X| in [29.2, 39.2], Y in [81.0, 102.0], Z in [22.0, Z_top]):
            //    - Mép trong |X| = 29.2mm (nằm ngoài vách 2 Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
            //    - Mũi trước Y = 102.0mm (dừng trước lưng 2 Tháp Nâng & Gờ định vị Y = 105.0mm đúng 3.0mm!)
            //    - Mặt đỉnh Z = Z_top đồng phẳng 100% với sàn chính -> Đặt in lật úp phẳng 100% Zero Support!
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 22.0])
                    cube([10.0, 21.0, Z_top - 22.0]);
            }
            
            // 4. Hai Cụm Gá Cảm Biến Laser ToF VL53L0X Trái & Phải giải mê cung
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=Z_top - 12.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=Z_top - 12.0);
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // Ô thoáng trung tâm luồn dây Pin 2S2P & thông gió (44.0 x 44.0 mm - X in [-22, 22], Y in [18.0, 62.0]):
        translate([-22.0, 18.0, 20.0])
            cube([44.0, 44.0, Z_top + 2.0]);
            
        // A. 2 CHÂN ĐÔN SAU HẠ THẲNG ĐỨNG KÈM GIẾNG VẶN ỐC XUYÊN SUỐT TỪ MẶT TRÊN (X = +-31.5..35.0, Y = 46.5..51.5):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 31.5, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 35.0, 46.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 31.5, 51.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
            }
        }
        
        // B. 2 TAY/CHÂN TRƯỚC LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG (X = +-32.0..35.5, Y = 95.5..99.5):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
            }
        }
        
        // C. 4 RÃNH TRƯỢT ĐƠN GỌN GÀNG TẠI 4 GÓC K2 CONTROL HUB:
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
    translate([0, 0, 51.0])
        rotate([180, 0, 0])
            k2_adapter_monolithic_v60(Z_bot = 46.0, T_deck = 5.0);
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
// 8. KHUNG TAY NÂNG DƯỚI CHỮ H V13.0 THANH MẢNH SIÊU BỀN (LOWER H-FRAME ARM V13.0)
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
        
        // A. Hốc tròn âm Ø20.8mm sâu 2.3mm ôm trọn Đĩa tròn Servo MG996R ở mặt ngoài (X in [17.2, 19.6])
        //    Giữ thành sau dày 5.7mm đặc 100%!
        translate([17.2, 0, 0]) rotate([0, 90, 0]) cylinder(d=20.8, h=2.8);

        // B. Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([10.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);

        // C. 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm hốc chìm Ø6.0mm sâu 1.8mm ở mặt trong (X in [11.0, 12.8])
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            if (hz >= -height/2 + 0.5) {
                translate([10.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=10.0);
                translate([11.0, hy, hz]) rotate([0, 90, 0]) cylinder(d=6.0, h=1.8);
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
"""

PARTS = [
    {
        "stl_name": "04A_Wrist_Clevis_Pitch_Bracket_S3.stl",
        "scad_code": SCAD_LIBRARY + "\nwrist_clevis_pitch_bracket_s3_printable();\n",
        "desc": "Cổ tay nối tay nâng chữ H cũ & Gá Servo S3 gập dọc 90° V7.1 (Lắp vừa 4 chốt 03 & 03B, gối xoay đồng trục M3, in phẳng Z=0, 0% Support)"
    },
    {
        "stl_name": "04_Gripper_Base_Head_V2.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_gripper_base();\n',
        "desc": "Bệ đầu kẹp V2.0 DFM (Double-Shear M3, Clevis Pitch 90°, Gá Servo S2 Bridge, 0% Support)"
    },
    {
        "stl_name": "05_Gripper_Jaw_Left_Universal_V2.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_jaw_left();\n',
        "desc": "Ngàm kẹp Trái Đa Năng V2.0 DFM (Bánh răng thân khai m=1.5mm, Rãnh V kép Ø15-45mm, Răng cưa, 0% Support)"
    },
    {
        "stl_name": "06_Gripper_Jaw_Right_Universal_V2.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_jaw_right();\n',
        "desc": "Ngàm kẹp Phải Đa Năng V2.0 DFM (Hốc đĩa tròn MG996R, Bánh răng thân khai m=1.5mm, Rãnh V kép, 0% Support)"
    },
    {
        "stl_name": "04_Gripper_Base_Head.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_gripper_base();\n',
        "desc": "Bệ đầu kẹp V2.0 (Bản tương thích tên cũ) - 0% Support"
    },
    {
        "stl_name": "05_Gripper_Jaw_Left_VGuide_Flower32.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_jaw_left();\n',
        "desc": "Hàm kẹp Trái Đa Năng V2.0 (Bản tương thích tên cũ) - 0% Support"
    },
    {
        "stl_name": "06_Gripper_Jaw_Right_VGuide_Flower32.stl",
        "scad_code": 'use <gripper_v2.scad>;\nexport_jaw_right();\n',
        "desc": "Hàm kẹp Phải Đa Năng V2.0 (Bản tương thích tên cũ) - 0% Support"
    },
    {
        "stl_name": "01D_K2_Hub_Adapter_Plate.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_plate_flat();\n",
        "desc": "Tấm sàn phẳng K2 Control Hub V10.0 (Ngàm Cài Snap-Fit Đàn Hồi Khóa Nhanh K2 Hub + Cụm 2 Gá Laser ToF VL53L0X Đo Tường Giải Mê Cung + Cantilever Né Tháp Nâng 23mm) - In phẳng Z=0"
    },
    {
        "stl_name": "01D_MCU_Control_Hub_Deck_FlatPrint.stl",
        "scad_code": SCAD_LIBRARY + "\nmcu_deck_compact_slotted_v80();\n",
        "desc": "Bệ MCU nhỏ gọn Đa Năng V10.0 (Cắt hốc né Tháp Nâng Y=102mm + Rãnh Đáy Kín Khóa Tán M3 + Rãnh trượt trụ X-Y, vừa khít Plate 1) - In phẳng Z=0"
    },
    {
        "stl_name": "01D_Base_Riser_Frame.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_base_riser_frame_printable();\n",
        "desc": "Khung chân đôn trung gian Đa Năng V10.0 (Hạ Thẳng Đứng 100% Không Cần Trượt + Né Tuyệt Đối Tháp Nâng & Servo S1 + 4 Tai Bắt Tấm Sàn Lộ Thiên) - In úp Z=0"
    },
    {
        "stl_name": "01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_monolithic_printable();\n",
        "desc": "Bản liền khối Đa Năng 1 chi tiết V10.0 (Cụm 2 Gá Laser ToF VL53L0X Giải Mê Cung + Cantilever Dời Lùi Né Cụm Gắp Trụ 23-25mm + Hạ Thẳng Đứng 100%) - In úp Z=0"
    },
    {
        "stl_name": "01D_K2_Control_Hub_Riser_Adapter_V60.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_monolithic_printable();\n",
        "desc": "Bản liền khối Đa Năng 1 chi tiết V10.0 (Đồng bộ file V60) - In úp Z=0"
    },
    {
        "stl_name": "01D_Snap_Clip_K2_Hub.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_snap_clip_modular();\n",
        "desc": "Ngàm cài đàn hồi Snap-fit rời V10.0 (Khóa nhanh K2 Control Hub tháo lắp trong 1 giây, in nằm phẳng thớ nhựa dẻo gấp 10 lần) - In phẳng Z=0"
    },
    {
        "stl_name": "01D_Riser_Standoff_18mm.stl",
        "scad_code": SCAD_LIBRARY + "\nriser_standoff_18mm();\n",
        "desc": "Trụ đệm đôn cao 18mm rời (Ø11mm, lỗ bậc chìm 14mm cho ốc M3x12/16mm)"
    },
    {
        "stl_name": "01D_Riser_Standoff_24mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\nriser_standoff_24mm_2s2p(h=24.0);\n",
        "desc": "Trụ đệm đôn cao 24mm rời cho Pin 2S2P (H_clear = 42.0mm, Ø11mm, lỗ bậc chìm cho ốc M3)"
    },
    {
        "stl_name": "01D_Riser_Standoff_26mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\nriser_standoff_26mm_2s2p(h=26.0);\n",
        "desc": "Cọc đôn Standoff kép 26mm rời cho Pin 2S2P (Ø11.6mm D-flat, cài 2 tán M3 ngang hông, bệ chịu lực 3.5mm)"
    },
    {
        "stl_name": "01D_Riser_Standoff_44mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\nriser_standoff_44mm_2s2p(h=44.0);\n",
        "desc": "Cọc đôn Standoff kép 44mm nguyên khối cho Pin 2S2P (Ø11.6mm D-flat, cài 2 tán M3 ngang hông, nâng thẳng K2 Hub lên Z=48mm)"
    },
    {
        "stl_name": "02B_GA25_Rear_Motor_Clamp_Left.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 12.0]) rotate([0, -90, 0]) ga25_rear_clamp_left();\n",
        "desc": "Nẹp động cơ GA25 Sau - Trái V4.3 (Vòm Ø26.2mm, khuyết phẳng mép trong 2.5mm, in nằm phẳng bên)"
    },
    {
        "stl_name": "02C_GA25_Rear_Motor_Clamp_Right.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 3.5]) rotate([0, -90, 0]) ga25_rear_clamp_right();\n",
        "desc": "Nẹp động cơ GA25 Sau - Phải V4.3 (Vòm Ø26.2mm, khuyết phẳng mép trong 2.5mm, in nằm phẳng bên)"
    },
    {
        "stl_name": "02_GA25_Rear_Motor_Clamp_Universal.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 4.0]) rotate([0, -90, 0]) ga25_rear_clamp_universal();\n",
        "desc": "Nẹp động cơ GA25 Sau Dùng Chung V4.3 (Vòm Ø26.2mm, đối xứng 8mm, lắp cả 2 bên)"
    },
    {
        "stl_name": "01C_Lift_Tower_Right_MG996R_FlatPrint.stl",
        "scad_code": SCAD_LIBRARY + "\nlift_tower_right_v50_printable();\n",
        "desc": "Tháp nâng phải MG996R V5.0 (Hốc chìm tán M3, rãnh lượn 1.5mm chống cấn ốc tuyệt đối) - In nằm phẳng Z=0"
    },
    {
        "stl_name": "03_Parallel_Arm_Truss_IBeam.stl",
        "scad_code": SCAD_LIBRARY + "\nlower_h_frame_arm_v13_printable();\n",
        "desc": "Khung tay nâng dưới chữ H V13.0 Thanh Mảnh Siêu Bền (Dầm cao 12mm đồng bộ thanh trên, vòm Servo Horn Ø24mm gân lượn mượt, không gờ đáy hay nêm lòi) - In phẳng Z=0"
    },
    {
        "stl_name": "08_S1_MG996R_Round_Horn_Drive_Coupler.stl",
        "scad_code": SCAD_LIBRARY + "\ns1_round_horn_drive_coupler();\n",
        "desc": "Khối khóa đĩa tròn Servo S1 rời V5.0 (Cắm vừa rãnh tay nâng cũ, không cần in lại tay nâng) - In phẳng Z=0"
    },
]

def convert_stl_to_binary(stl_path):
    with open(stl_path, "rb") as f:
        head = f.read(80)
        is_ascii = head.startswith(b"solid") and (b"\n" in head or b"\r" in head)
    if not is_ascii:
        return
    with open(stl_path, "r", errors="ignore") as f:
        text = f.read()
    pattern = re.compile(
        r"facet\s+normal\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"outer\s+loop\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"endloop\s+endfacet",
        re.DOTALL,
    )
    matches = pattern.findall(text)
    if not matches:
        return
    with open(stl_path, "wb") as f:
        header = b"Binary STL - ORC K2 DFM V5.0".ljust(80, b" ")
        f.write(header)
        f.write(struct.pack("<I", len(matches)))
        for m in matches:
            vals = [float(x) for x in m]
            f.write(struct.pack("<12fH", *vals, 0))

def render_part(part):
    stl_path = os.path.join(STL_DIR, part["stl_name"])
    temp_scad = os.path.join(STL_DIR, "_temp_" + part["stl_name"].replace(".stl", ".scad"))
    
    with open(temp_scad, "w", encoding="utf-8") as f:
        f.write(part["scad_code"])
        
    print(f"-> Đang xuất STL: {part['stl_name']} ({part['desc']})...")
    cmd = [OPENSCAD_COM, "-o", stl_path, temp_scad]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_scad):
        os.remove(temp_scad)
        
    if res.returncode == 0 and os.path.exists(stl_path):
        convert_stl_to_binary(stl_path)
        size = os.path.getsize(stl_path)
        print(f"   [OK] Đã tạo thành công {part['stl_name']} (Kích thước Binary: {size:,} bytes)")
        return True
    else:
        print(f"   [LỖI] Xuất thất bại {part['stl_name']}!")
        print("   Stderr:", res.stderr)
        return False

if __name__ == "__main__":
    print("\n====================================================================")
    print("BẮT ĐẦU XUẤT CÁC TỆP 3D STL THIẾT KẾ LẠI V5.0 THEO YÊU CẦU")
    print("====================================================================")
    success_count = 0
    for p in PARTS:
        if render_part(p):
            success_count += 1
            
    print(f"\n-> Hoàn tất xuất {success_count}/{len(PARTS)} file STL!")
