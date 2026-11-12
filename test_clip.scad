$fn = 32;
module k2_snap_clip_modular() {
    difference() {
        union() {
            // Chân đế trượt chữ T cài vừa khít vào rãnh hạt đậu của tấm plate
            translate([-8.0, -5.5, 0.0]) cube([16.0, 11.0, 3.8]);
            translate([-3.2, -5.5, 3.8]) cube([6.4, 11.0, 3.2]);
            // Đòn đàn hồi đứng (in nằm phẳng tại Z=0)
            translate([-4.5, 5.5, 0.0]) cube([9.0, 26.5, 2.4]);
            // Đầu móc ngàm khóa có vát 45 độ
            translate([-4.5, 30.5, 2.4])
                hull() {
                    cube([9.0, 1.5, 1.5]);
                    translate([0, -2.2, 0]) cube([9.0, 0.1, 0.1]);
                }
            // Tai bấm ngón tay mở nhanh (Thumb tab)
            translate([-4.5, 30.5, 0.0])
                hull() {
                    cube([9.0, 3.2, 2.4]);
                    translate([0, 5.0, 0]) cube([9.0, 0.1, 2.4]);
                }
        }
        // Lỗ ốc M3 tâm để siết khóa cứng nếu muốn
        translate([0, 0, -1.0]) cylinder(d=3.3, h=10.0);
    }
}
k2_snap_clip_modular();
