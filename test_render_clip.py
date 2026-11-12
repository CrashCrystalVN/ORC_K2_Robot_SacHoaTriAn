import os
import subprocess

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

test_clip_scad = os.path.join(BASE_DIR, "test_clip_v11.scad")
test_clip_stl = os.path.join(BASE_DIR, "3D_Models", "01D_Snap_Clip_K2_Hub_V11_Hardened.stl")

clip_scad = """$fn = 40;

module k2_snap_clip_modular_hardened() {
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
            // Gờ chống trượt ngón tay
            translate([-5.0, 33.0, 2.2])
                cylinder(d=1.4, h=10.0);
        }
        // Lỗ ốc M3 tâm để siết khóa cứng định vị
        translate([0, 0, -1.0]) cylinder(d=3.4, h=12.0);
        // Hốc chìm nón 90° bắt vít M3 đầu dù/nón phẳng
        translate([0, 0, 5.0]) cylinder(d1=3.4, d2=6.6, h=2.2);
    }
}

k2_snap_clip_modular_hardened();
"""

with open(test_clip_scad, "w", encoding="utf-8") as f:
    f.write(clip_scad)

res = subprocess.run([OPENSCAD, "-o", test_clip_stl, test_clip_scad], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode == 0:
    print("Success! File size:", os.path.getsize(test_clip_stl), "bytes")
else:
    print("Error:", res.stderr)
