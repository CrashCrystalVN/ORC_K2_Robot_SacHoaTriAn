 = 48;
// V5.1 without boss:
INNER_SPAN = 113.0;
X_FLANGE_IN_L = -INNER_SPAN / 2.0; // -56.5
X_FLANGE_IN_R = +INNER_SPAN / 2.0; // +56.5
MOTOR_ENC_L = 63.0;
MOTOR_D = 25.0;

intersection() {
    // Left motor
    translate([X_FLANGE_IN_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
    
    // Right motor
    translate([X_FLANGE_IN_R - MOTOR_ENC_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
}
