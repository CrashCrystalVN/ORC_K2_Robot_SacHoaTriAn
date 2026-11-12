$fn = 36;
CHASSIS_W = 118.0;
BOSS_OUT = 10.5;
FLANGE_T = 3.0;
X_FLANGE_IN_L = -(CHASSIS_W/2.0 + BOSS_OUT) + FLANGE_T; // -66.5
X_FLANGE_IN_R = +(CHASSIS_W/2.0 + BOSS_OUT) - FLANGE_T; // +66.5
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
