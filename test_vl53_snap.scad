$fn = 40;

// Module gá cảm biến VL53L0X tích hợp ngàm cài snap-fit & cửa sổ laser 90° + 45°
module vl53l0x_snap_pod(is_left = true) {
    sx = is_left ? -1 : 1;
    // Tọa độ gắn trên mép sườn plate (X = sx * 60.0mm, Y = 62.0..82.0mm, Z = 0..12.0mm trên plate)
    // Cánh gá vươn ra ngoài từ |X| = 60.0 đến |X| = 72.5mm
    difference() {
        union() {
            // Khối cánh vươn chịu lực (X = sx*60..sx*72.5, Y = 61.5..82.0, Z = 0..10.0)
            hull() {
                translate([sx * 60.0, 62.0, 0.0]) cube([sx * 0.1, 20.0, 6.0]);
                translate([sx * 71.5, 64.0, 0.0]) cylinder(r=2.5, h=10.0);
                translate([sx * 71.5, 80.0, 0.0]) cylinder(r=2.5, h=10.0);
                translate([sx * 60.0, 82.0, 0.0]) cube([sx * 0.1, 0.1, 6.0]);
            }
            // 2 Ngàm cài đàn hồi Snap-fit giữ bo mạch VL53L0X (tại Y = 66.0 và Y = 78.0)
            for (py = [66.0, 78.0]) {
                translate([sx * 72.8, py - 2.0, 0.0])
                    cube([sx * 1.8, 4.0, 12.0]);
                // Đầu móc ngàm cài có vát 45° dẫn hướng ấn tách
                translate([sx * 72.8, py - 2.0, 10.5])
                    hull() {
                        cube([sx * 1.8, 4.0, 1.5]);
                        translate([-sx * 1.0, 0, 0]) cube([sx * 0.1, 4.0, 1.0]);
                    }
            }
            // Vách chống trượt & gờ tì sau cho bo mạch VL53L0X
            translate([sx * 70.0, 64.0, 0.0])
                cube([sx * 1.5, 16.0, 10.0]);
        }
        
        // Khe cắm bo mạch VL53L0X (khe rộng 2.0mm cho PCB dày 1.6mm + dung sai 0.4mm, dài 25.5mm, cao 11.5mm)
        translate([sx * 71.6, 64.0, 1.5])
            cube([sx * 2.2, 16.0, 12.0]);
            
        // Cửa sổ quang học bắn tia laser ToF 90° (rộng 12.0 x cao 7.0mm kèm vát loe 35°)
        translate([sx * 68.0, 66.0, 3.0])
            cube([sx * 8.0, 12.0, 6.5]);
        hull() {
            translate([sx * 70.5, 66.0, 3.0]) cube([sx * 0.1, 12.0, 6.5]);
            translate([sx * 74.0, 64.5, 1.5]) cube([sx * 0.1, 15.0, 9.5]);
        }
        
        // 2 Lỗ ốc M2.5 / M3 dự phòng (khoảng cách tâm 18.0mm: Y = 63.0 và Y = 81.0)
        translate([sx * 66.0, 63.5, -1.0]) cylinder(d=3.2, h=15.0);
        translate([sx * 66.0, 80.5, -1.0]) cylinder(d=3.2, h=15.0);
        // Hốc tán M3 âm dưới đáy
        translate([sx * 66.0, 63.5, 1.5]) cylinder(d=6.2, h=12.0);
        translate([sx * 66.0, 80.5, 1.5]) cylinder(d=6.2, h=12.0);
        
        // Rãnh luồn dây cảm biến I2C 4P ngầm xuyên vào sàn plate
        translate([sx * 59.0, 68.0, 1.0])
            cube([sx * 12.0, 8.0, 3.5]);
    }
}

// Render test left pod
vl53l0x_snap_pod(is_left=true);
