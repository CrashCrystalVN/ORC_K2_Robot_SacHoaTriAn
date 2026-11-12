import os
import subprocess

SCAD_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

test_scad = os.path.join(SCAD_DIR, "test_hardened_snap.scad")
test_stl = os.path.join(SCAD_DIR, "test_hardened_snap.stl")

code = """$fn = 32;

// 1. Module Gờ Hãm Đuôi Liền Thân Có Gân Tam Giác & Góc Lượn R >= 3.5mm
module rear_gusseted_retaining_lip(sx = 1, T_deck = 6.0) {
    x_center = sx * 42.0;
    w_x = 18.0; // Rộng 18mm ôm vững mép sau K2 Hub
    
    // Khối vách chính dày 5.0mm (Y in [-11.0, -6.0]), cao 11.5mm (Z in [T_deck, T_deck + 11.5])
    translate([x_center - w_x/2, -11.0, T_deck]) {
        cube([w_x, 5.0, 11.5]);
        
        // Mép ngàm hãm vát nêm 45° nhô vào +Y 2.0mm (Y in [-6.0, -4.0]) ở Z = 10.0..11.5mm
        translate([0, 5.0, 9.8])
            hull() {
                cube([w_x, 0.1, 1.7]);
                translate([0, 2.0, 0.5]) cube([w_x, 0.1, 1.2]);
                translate([0, 0, 1.7]) cube([w_x, 0.1, 0.1]);
            }
            
        // Gân tam giác chịu lực khổng lồ ở mặt sau (Gusset Ribs dốc 45° từ Z=11.5 xuống Z=0)
        translate([0, -5.0, 0])
            hull() {
                cube([w_x, 0.1, 0.1]);
                translate([0, 5.0, 0]) cube([w_x, 0.1, 11.5]);
                translate([0, 5.0, 11.5]) cube([w_x, 0.1, 0.1]);
            }
    }
    
    // Vuốt góc lượn chuyển tiếp R = 3.5mm tại chân ngàm (Fillet Transition)
    translate([x_center - w_x/2, -11.0, T_deck]) {
        // Góc lượn lưng sau
        hull() {
            translate([0, -3.5, 0]) cube([w_x, 0.1, 0.1]);
            translate([0, 0, 0]) cube([w_x, 0.1, 3.5]);
        }
        // Vát chân trước chống kẹt mép bo K2 Hub
        translate([0, 5.0, 0])
            hull() {
                cube([w_x, 0.1, 1.0]);
                translate([0, 1.0, 0]) cube([w_x, 0.1, 0.1]);
            }
    }
}

// 2. Module Gờ Hãm Góc Trước Có Gân Tam Giác & Mép Vát Nêm
module front_reinforced_corner_lip(sx = 1, T_deck = 6.0) {
    x_pos = sx * 57.0 - (sx > 0 ? 0 : 7.0);
    w_x = 7.0; // Dày 7mm theo trục X
    l_y = 6.0; // Dày 6mm theo trục Y (thay vì 2.2mm mỏng manh cũ!)
    h_z = 12.0; // Cao 12mm
    
    translate([x_pos, 80.0, T_deck]) {
        // Trụ chịu lực chính dày 7.0 x 6.0 mm
        cube([w_x, l_y, h_z]);
        
        // Mép ngàm hãm vát nêm 45° nhô vào -Y 1.8mm ở Z = 10.2..12.0mm
        translate([0, -1.8, 10.2])
            hull() {
                cube([w_x, 1.8, 1.8]);
                translate([0, 1.8, 1.8]) cube([w_x, 0.1, 0.1]);
            }
            
        // Gân tam giác dốc 45° trợ lực hướng ra trước (+Y, dốc từ Z=12 xuống Z=0)
        translate([0, l_y, 0])
            hull() {
                cube([w_x, 0.1, h_z]);
                translate([0, 6.0, 0]) cube([w_x, 0.1, 0.1]);
                cube([w_x, 0.1, 0.1]);
            }
    }
    
    // Vuốt góc lượn chân đế R = 3.5mm
    translate([x_pos, 80.0, T_deck]) {
        hull() {
            translate([0, l_y, 0]) cube([w_x, 0.1, 3.5]);
            translate([0, l_y + 3.5, 0]) cube([w_x, 0.1, 0.1]);
        }
    }
}

// Giả lập mặt sàn
cube([120, 90, 6]);

// 2 ngàm đuôi gia cố
rear_gusseted_retaining_lip(1);
rear_gusseted_retaining_lip(-1);

// 2 ngàm trước gia cố
front_reinforced_corner_lip(1);
front_reinforced_corner_lip(-1);
"""

with open(test_scad, "w", encoding="utf-8") as f:
    f.write(code)

res = subprocess.run([OPENSCAD, "-o", test_stl, test_scad], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode == 0:
    print("Success! File size:", os.path.getsize(test_stl), "bytes")
else:
    print("Error:", res.stderr)
