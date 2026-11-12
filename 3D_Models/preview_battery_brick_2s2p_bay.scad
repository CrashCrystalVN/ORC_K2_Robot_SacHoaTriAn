// ====================================================================
// Dá»° Ã N: ORC K2 ROBOT "Sáº®C HOA TRI Ã‚N" - STEM THPT NGÃ” QUYá»€N
// BÃ€N GIAO: KHOANG CHá»¨A PIN Gáº CH 2S2P 18650 & KIá»‚M TRA KHOáº¢NG Há»ž 3D
// File: preview_battery_brick_2s2p_bay.scad
// ====================================================================

$fn = 40;

GROUND_CLEAR = 10.0;
FLOOR_T      = 4.0;
CHASSIS_W    = 134.0;
CHASSIS_L    = 172.0;
WALL_H       = 28.0;

Y_REAR_WHEEL  = 32.0;
Y_FRONT_WHEEL = 140.0;
Z_SHAFT       = 30.0;

use <full_assembly_200x200.scad>;
use <01D_Base_Riser_Frame.scad>;

// Module cáº­n cáº£nh khoang pin gáº¡ch 2S2P
module battery_bay_scene() {
    // 1. Khung gáº§m chÃ­nh
    color("LightSteelBlue", 0.95)
        translate([0, 0, GROUND_CLEAR])
            chassis_base();

    // 2. 4 Ä á»™ng cÆ¡ GA25 (Cáº§u sau cÃ³ Encoder, cáº§u trÆ°á»›c DC)
    for (side = [-1, 1]) {
        // Sau (Encoder)
        translate([side * (CHASSIS_W/2 - 2.0), Y_REAR_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
        // TrÆ°á»›c
        translate([side * (CHASSIS_W/2 - 2.0), Y_FRONT_WHEEL, GROUND_CLEAR + 20.0])
            rotate([0, side > 0 ? 0 : 180, 0])
                ga25_motor_model();
    }

    // 3. Khá»‘i Pin Gáº¡ch 2S2P 18650 (38 x 38 x 70 mm) kÃ¨m 2 Ä‘ai Velcro & Jack XT30
    translate([0, 0, GROUND_CLEAR])
        battery_brick_2s2p(with_strap = true, with_cable = true);

    // 4. Khung Ä‘Ã´n Riser Frame (Hiá»ƒn thá»‹ mÃ u xanh mian trong suá»‘t Ä‘á»ƒ tháº¥y rÃµ lÃ²ng khoang)
    color("DeepSkyBlue", 0.45)
        translate([0, 0, GROUND_CLEAR])
            k2_base_riser_frame_2s2p(Z_top = 46.0);

    // 5. Bá»‡ Ä‘Ã¡y K2 Hub (Z = 46.0mm) thá»ƒ hiá»‡n máº·t pháº³ng tráº§n tÄ©nh khÃ´ng 4.0mm
    color("OrangeRed", 0.25)
        translate([-58.0, 10.0, GROUND_CLEAR + 46.0])
            cube([116.0, 80.0, 2.0]);

    // 6. CÃ¡c thanh thÆ°á»›c Ä‘o khoáº£ng há»Ÿ 3D trá»±c quan (Visual Clearance Indicators)
    // Khoáº£ng há»Ÿ cáº§u sau (Delta Y = 6.5mm)
    color("LimeGreen") {
        translate([-12.0, 44.5, GROUND_CLEAR + FLOOR_T + 10.0])
            cube([24.0, 6.5, 3.0]);
    }
    // Khoáº£ng há»Ÿ cáº§u trÆ°á»›c (Delta Y = 6.5mm)
    color("LimeGreen") {
        translate([-12.0, 121.0, GROUND_CLEAR + FLOOR_T + 10.0])
            cube([24.0, 6.5, 3.0]);
    }
    // Khoáº£ng há»Ÿ tÄ©nh khÃ´ng trÃªn lÆ°ng pin (Delta Z = 4.0mm)
    color("Yellow") {
        translate([-10.0, 70.0, GROUND_CLEAR + FLOOR_T + 38.0])
            cube([20.0, 20.0, 4.0]);
    }
    // Khoáº£ng há»Ÿ 2 bÃªn sÆ°á» n vá»›i chÃ¢n khung Ä‘Ã´n (Delta X = 7.5mm má»—i bÃªn)
    color("Cyan") {
        translate([-26.5, 75.0, GROUND_CLEAR + FLOOR_T + 10.0])
            cube([7.5, 12.0, 3.0]);
        translate([19.0, 75.0, GROUND_CLEAR + FLOOR_T + 10.0])
            cube([7.5, 12.0, 3.0]);
    }
}

battery_bay_scene();
