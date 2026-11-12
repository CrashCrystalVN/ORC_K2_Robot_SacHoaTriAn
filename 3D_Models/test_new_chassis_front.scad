// Test script to verify the new VL53L0X front bumper and side ToF mounts
$fn = 32;

CHASSIS_W    = 116.0;
CHASSIS_L    = 172.0;
FLOOR_T      = 4.0;
WALL_T       = 4.0;
WALL_H       = 30.0;

module teardrop_hole_x(d = 9.0, h = 10.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2.0, -side/2.0])
                    cube([h, side, side]);
    }
}

module teardrop_hole_y(d = 16.6, h = 15.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([-90, 0, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([0, 45, 0])
                translate([-side/2.0, 0, -side/2.0])
                    cube([side, h, side]);
    }
}

module front_bumper_and_vl53l0x() {
    difference() {
        // Khối cản trước khí động học & bệ gá VL53L0X
        union() {
            hull() {
                // Mặt trước trung tâm (Y = CHASSIS_L)
                translate([-20.0, CHASSIS_L - 2.0, 0])
                    cube([40.0, 2.0, 14.0]);
                // Hai góc vát sau 45° chống móc vướng (Y = CHASSIS_L - 10.0)
                translate([-34.0, CHASSIS_L - 10.0, 0])
                    cube([68.0, 2.0, 14.0]);
                // Phần bệ đế nối vào sàn (Y = CHASSIS_L - 16.0)
                translate([-24.0, CHASSIS_L - 16.0, 0])
                    cube([48.0, 6.0, 10.0]);
            }
        }

        // 1. Cửa sổ quang học ToF phát/thu laser góc mở rộng 35° (vượt 25° FoV)
        hull() {
            // Cửa sổ trong tại mặt trước cảm biến
            translate([-5.5, CHASSIS_L - 5.6, 6.5])
                cube([11.0, 0.2, 6.0]);
            // Cửa sổ ngoài mở rộng tại mặt cản trước
            translate([-8.0, CHASSIS_L + 0.1, 5.25])
                cube([16.0, 0.2, 8.5]);
        }

        // 2. Khe trượt cài module cảm biến VL53L0X (PCB 25x11x1.6mm)
        translate([-12.8, CHASSIS_L - 5.5, FLOOR_T])
            cube([25.6, 2.4, 11.0]);

        // 3. Hốc thoáng mặt sau linh kiện SMD trên board
        translate([-10.0, CHASSIS_L - 8.5, FLOOR_T])
            cube([20.0, 3.0, 10.0]);

        // 4. Hai lỗ ốc bắt M2.5 / M3 chuẩn pitch 20.0mm (X = ±10.0mm, Z = 9.5mm)
        translate([-10.0, CHASSIS_L - 9.0, 9.5])
            teardrop_hole_y(d=3.0, h=10.0);
        translate([ 10.0, CHASSIS_L - 9.0, 9.5])
            teardrop_hole_y(d=3.0, h=10.0);

        // 5. Rãnh luồn cáp I2C (4P Dupont / JST) xuyên sàn
        translate([-7.0, CHASSIS_L - 18.0, -0.5])
            cube([14.0, 10.0, FLOOR_T + 1.0]);
    }
}

front_bumper_and_vl53l0x();
