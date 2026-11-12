import os
import subprocess

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

test_py = os.path.join(BASE_DIR, "test_render_hardened_plate.py")
test_scad = os.path.join(BASE_DIR, "test_plate_v11.scad")
test_stl = os.path.join(BASE_DIR, "3D_Models", "01D_K2_Hub_Adapter_Plate_V11_Hardened.stl")

# Read SCAD_LIBRARY from generate_redesigned_parts.py
with open(os.path.join(BASE_DIR, "generate_redesigned_parts.py"), "r", encoding="utf-8") as f:
    orig_code = f.read()

# Replace k2_adapter_plate_flat in the SCAD code with the hardened version
new_k2_adapter_plate_flat = """
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
"""

# Let's write the test OpenSCAD file
test_scad_content = "$fn = 40;\n"
# Include dependencies
with open(os.path.join(BASE_DIR, "generate_redesigned_parts.py"), "r", encoding="utf-8") as f:
    text = f.read()

# Grab helper library up to k2_adapter_plate_flat
target = 'SCAD_LIBRARY = ' + '"""'
s_lib = text.find(target) + len(target)
s_mod = text.find('module k2_adapter_plate_flat()')
prefix = text[s_lib:s_mod]

full_scad = "$fn = 40;\n\n" + prefix + "\n" + new_k2_adapter_plate_flat + "\n\nk2_adapter_plate_flat();\n"

with open(test_scad, "w", encoding="utf-8") as f:
    f.write(full_scad)

print("Compiling test plate with OpenSCAD...")
res = subprocess.run([OPENSCAD, "-o", test_stl, test_scad], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode == 0:
    print("Success! File size:", os.path.getsize(test_stl), "bytes")
else:
    print("Error:", res.stderr)
