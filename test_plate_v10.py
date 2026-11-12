import os
import subprocess

OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.com"
TEST_SCAD = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\test_plate_v10.scad"
TEST_STL = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\test_plate_v10.stl"

scad_content = """$fn = 32;

// Utility rãnh M3 đáy kín
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

// Cụm gá cảm biến khoảng cách VL53L0X
module vl53l0x_sensor_wing(is_left = true, T_deck = 6.0) {
    sx = is_left ? -1 : 1;
    difference() {
        union() {
            // Cánh vươn chịu lực nối liền mép sườn plate (X = sx*60..sx*72.5, Y = 60.0..82.0)
            hull() {
                translate([sx * 60.0, 60.0, 0.0]) cube([sx * 0.1, 22.0, T_deck]);
                translate([sx * 72.0, 62.0, 0.0]) cylinder(r=2.5, h=T_deck + 6.0);
                translate([sx * 72.0, 80.0, 0.0]) cylinder(r=2.5, h=T_deck + 6.0);
                translate([sx * 60.0, 82.0, 0.0]) cube([sx * 0.1, 0.1, T_deck]);
            }
            // 2 Ngàm kẹp đàn hồi Snap-fit giữ mép bo mạch VL53L0X (tại Y = 65.0 và Y = 77.0)
            for (py = [65.0, 77.0]) {
                translate([sx * 72.5, py - 2.5, 0.0])
                    cube([sx * 1.8, 5.0, T_deck + 7.5]);
                // Đầu móc ngàm cài có vát dốc 45° dẫn hướng ấn tách
                translate([sx * 72.5, py - 2.5, T_deck + 6.0])
                    hull() {
                        cube([sx * 1.8, 5.0, 1.5]);
                        translate([-sx * 1.1, 0, 0]) cube([sx * 0.1, 5.0, 1.0]);
                    }
            }
            // Gờ tì sau lưng bo mạch
            translate([sx * 69.8, 63.0, 0.0])
                cube([sx * 1.5, 16.0, T_deck + 5.5]);
        }
        
        // Khe cắm bo mạch VL53L0X (rộng 2.1mm cho PCB dày 1.6mm + dung sai, dài 25.0mm)
        translate([sx * 71.4, 62.5, 1.5])
            cube([sx * 2.2, 17.0, 15.0]);
            
        // Cửa sổ quang học bắn tia laser ToF 90° vuông góc thành mê cung (rộng 12.0 x cao 7.0mm kèm vát loe 35°)
        translate([sx * 68.0, 65.0, 3.0])
            cube([sx * 8.0, 12.0, 6.5]);
        hull() {
            translate([sx * 70.0, 65.0, 3.0]) cube([sx * 0.1, 12.0, 6.5]);
            translate([sx * 74.5, 63.5, 1.5]) cube([sx * 0.1, 15.0, 9.5]);
        }
        
        // 2 Lỗ ốc M2.5 / M3 bắt vít dự phòng (khoảng cách tâm 18.0mm: Y = 62.5 và Y = 80.5)
        translate([sx * 65.5, 62.5, -1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 65.5, 80.5, -1.0]) cylinder(d=3.2, h=16.0);
        translate([sx * 65.5, 62.5, 1.5]) cylinder(d=6.2, h=12.0);
        translate([sx * 65.5, 80.5, 1.5]) cylinder(d=6.2, h=12.0);
        
        // Rãnh luồn cáp I2C 4P ngầm xuyên vào trong sàn plate
        translate([sx * 59.0, 67.0, 1.0])
            cube([sx * 12.0, 8.0, 3.5]);
    }
}

// Module tấm bệ K2 Control Hub V10.0 (Snap-Fit Latch + Dual VL53L0X Wings)
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
            
            // 4. Hai Cụm Gá Cảm Biến Khoảng Cách VL53L0X Trái & Phải để giải mê cung
            vl53l0x_sensor_wing(is_left=true, T_deck=T_deck);
            vl53l0x_sensor_wing(is_left=false, T_deck=T_deck);
            
            // 5. CƠ CHẾ NGÀM CÀI SNAP-FIT ĐÀN HỒI CHO K2 CONTROL HUB (Quick-Snap Retaining Clips):
            // A. Hai ngàm móc giữ đuôi K2 Hub (Y = -6.0mm): móc cứng giữ cạnh sau K2 Hub
            for (sx = [-1, 1]) {
                translate([sx * 45.0 - 6.0, -8.0, T_deck]) {
                    cube([12.0, 3.5, 12.0]);
                    // Móc nhô về trước (+Y) 1.8mm giữ cạnh trên đuôi K2 Hub
                    translate([0, 3.5, 10.5])
                        hull() {
                            cube([12.0, 0.1, 1.5]);
                            translate([0, 1.8, 0]) cube([12.0, 0.1, 1.5]);
                        }
                }
            }
            // B. Hai ngàm cài đàn hồi lẫy bấm phía trước K2 Hub (Y = +80.0mm, X = +-50.0mm):
            //    Có vát dốc 45° dẫn hướng ấn tách + tai tì bấm mở nhanh
            for (sx = [-1, 1]) {
                translate([sx * 50.0 - 5.0, 80.0, T_deck]) {
                    // Đòn đàn hồi cantilever dày 2.2mm, cao 14.0mm
                    cube([10.0, 2.4, 14.0]);
                    // Mấu ngàm khóa nhô về sau (-Y) 1.6mm kèm vát 45°
                    translate([0, -1.6, 11.5])
                        hull() {
                            cube([10.0, 1.6, 1.2]);
                            translate([0, 1.6, 2.5]) cube([10.0, 0.1, 0.1]);
                        }
                    // Tai bấm tì ngón tay (Thumb release tab) nhô ra phía trước (+Y)
                    translate([0, 2.4, 11.5])
                        hull() {
                            cube([10.0, 0.1, 2.5]);
                            translate([0, 3.0, 0]) cube([10.0, 0.1, 2.5]);
                        }
                }
            }
            // C. 4 Gờ định vị góc ôm khít K2 Control Hub (121.2 x 86.2 mm) chống xô lệch X-Y:
            for (sx = [-1, 1]) {
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), -6.0, T_deck])
                    cube([2.5, 12.0, 3.0]);
                translate([sx * 60.8 - (sx > 0 ? 0 : 2.5), 68.0, T_deck])
                    cube([2.5, 12.0, 3.0]);
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

k2_adapter_plate_flat_v10();
"""

with open(TEST_SCAD, "w", encoding="utf-8") as f:
    f.write(scad_content)

print("Compiling test plate V10 SCAD...")
res = subprocess.run([OPENSCAD, "-o", TEST_STL, TEST_SCAD], capture_output=True, text=True)
print("Exit code:", res.returncode)
if res.returncode == 0:
    print("Success! File size:", os.path.getsize(TEST_STL), "bytes")
else:
    print("Error:", res.stderr)

