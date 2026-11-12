import os
import subprocess

OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.com"
TEST_SCAD = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\test_arm_v11.scad"
TEST_STL = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\test_arm_v11.stl"

scad_content = """$fn = 48;

module teardrop_hole_x(d = 3.3, h = 44.0) {
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
// THIẾT KẾ LẠI KHUNG TAY NÂNG DƯỚI CHỮ H SIÊU CỨNG V11.0 (INDESTRUCTIBLE LOWER H-FRAME ARM)
// - Giải quyết triệt để 100% lỗi gãy ở cổ đĩa tròn Servo S1 (đoạn màu đỏ khoanh tròn):
//   1. Không bao giờ cắt đứt gờ đáy: Đáy sàn hạ sâu xuống Z = -12.0mm -> Hốc đĩa tròn Ø20.8mm (bán kính 10.4mm)
//      được bao bọc trọn vẹn bởi thành đáy đặc dày 1.6mm + gờ vòng cung ngoài dày 2.0mm!
//   2. Vòm tròn ôm đĩa Servo mở rộng lên Ø24.0mm đối xứng hoàn hảo, vát lượn côn tiếp tuyến mượt mà vào thân dầm.
//   3. Tăng dày thành trong dầm chịu lực từ 5.0mm lên 8.0mm (X in [11.5, 19.5mm]) -> Bản đế sau đĩa dày 5.8mm đặc 100%!
//   4. Tích hợp gân chéo tam giác bên trong khóa cứng khớp Servo vào thanh giằng ngang chữ H (Y = 42mm).
//   5. Đặt in phẳng đáy Z = 0.0mm -> 0% Support!
// ====================================================================
module lower_h_frame_arm_v11(length = 98.0, height = 12.0, thickness = 5.0) {
    z_bot = -12.0; // Đáy phẳng liên tục tiếp xúc bàn in Z = 0
    t_drive = 8.0; // Bề dày dầm phải chịu lực truyền từ Servo S1 (tăng từ 5.0 lên 8.0mm)
    
    difference() {
        union() {
            // 1. THANH TRÁI BỊ ĐỘNG (X in [-19.5, -14.5mm], dày 5.0mm)
            translate([-19.5, 0, z_bot])
                cube([thickness, length, height + abs(z_bot) - height/2]); // cao 18mm
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, -height/2, z_bot]) cube([thickness, height/2, height/2]);
            
            // 2. THANH PHẢI CHỦ ĐỘNG SIÊU CỨNG (X in [11.5, 19.5mm], dày 8.0mm ở gốc chịu lực!)
            // A. Dầm chính thân phải (X in [14.5, 19.5], dày 5.0mm chạy suốt chiều dài)
            translate([14.5, 0, z_bot])
                cube([thickness, length, height + abs(z_bot) - height/2]);
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            
            // B. Khối cổ gá Đĩa tròn Servo S1 mở rộng Ø24.0mm tại (Y = 0, Z = 0)
            translate([19.5 - t_drive, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=24.4, h=t_drive);
                    
            // C. GÂN TIẾP TUYẾN TĂNG CỨNG DẠNG NÊM CHỮ NHẬT & TAM GIÁC NỐI TỪ VÒM Ø24.4MM VÀO DẦM
            //    (X in [11.5, 19.5], Y in [0, 42.0], Z in [z_bot, +12.2])
            hull() {
                translate([19.5 - t_drive, 0, 0])
                    rotate([0, 90, 0]) cylinder(d=24.4, h=t_drive);
                translate([19.5 - t_drive, 36.0, z_bot])
                    cube([t_drive, 6.0, height + abs(z_bot) - height/2]);
            }
            
            // D. GÂN TAM GIÁC GIA CƯỜNG MẶT TRONG KHÓA VÀO THANH GIẰNG NGANG (X in [6.5, 14.5], Y in [8.0, 42.0])
            hull() {
                translate([11.5, 6.0, z_bot]) cube([3.0, 8.0, 16.0]);
                translate([6.5, 38.0, z_bot]) cube([8.0, 10.0, 14.0]);
            }
            
            // 3. THANH GIẰNG NGANG CHỮ H CHỐNG XOẮN (Y in [38.0, 52.0], X in [-14.5, 11.5])
            translate([-14.5, 38.0, z_bot])
                cube([26.0, 14.0, height + abs(z_bot) - height/2]);
        }

        // ------------------------------------------------------------
        // CÁC HỐC KHOÉT & LỖ CHỐT
        // ------------------------------------------------------------
        
        // A. Hốc tròn âm Ø20.8mm sâu 2.3mm ôm trọn Đĩa tròn Servo MG996R (25T Round Horn) ở mặt ngoài (X = 17.2..19.6)
        translate([17.2, 0, 0]) rotate([0, 90, 0]) cylinder(d=20.8, h=2.8);

        // B. Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([10.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);

        // C. 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm lỗ bậc chìm Ø6.0mm ở mặt trong (X = 11.5mm)
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            translate([10.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=10.0);
            translate([11.3, hy, hz]) rotate([0, 90, 0]) cylinder(d=6.0, h=3.0);
        }

        // D. Lỗ chốt xoay mắt trước (Y = length = 98.0, Z = 0)
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);

        // E. Lỗ chốt xoay mắt sau thanh trái (Y = 0, Z = 0)
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=10.0);
        
        // F. Vát mép 45° ở mũi trước (Y in [88.0, 99.0], Z in [z_bot, -6.0]) để lọt êm vào Clevis cổ tay S3
        for (sx = [-19.6, 14.4]) {
            translate([sx, length - 10.0, z_bot - 0.1])
                rotate([45, 0, 0])
                    cube([thickness + 0.2, 12.0, 10.0]);
        }
    }
}

// Bản in phẳng 100% tại Z = 0.0mm (Zero Support):
module lower_h_frame_arm_v11_printable() {
    translate([0, 0, 12.0])
        lower_h_frame_arm_v11();
}

lower_h_frame_arm_v11_printable();
"""

with open(TEST_SCAD, "w", encoding="utf-8") as f:
    f.write(scad_content)

print("Compiling test arm V11 SCAD...")
res = subprocess.run([OPENSCAD, "-o", TEST_STL, TEST_SCAD], capture_output=True, text=True)
print("Exit code:", res.returncode)
if res.returncode == 0:
    print("Success! File size:", os.path.getsize(TEST_STL), "bytes")
else:
    print("Error:", res.stderr)

