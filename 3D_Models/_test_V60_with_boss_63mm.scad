$fn = 48;
INNER_SPAN = 133.0;
X_FLANGE_IN_L = -INNER_SPAN / 2.0;
X_FLANGE_IN_R = +INNER_SPAN / 2.0;
MOTOR_ENC_L = 63.0;
MOTOR_D = 25.0;

intersection() {
    translate([X_FLANGE_IN_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
    
    translate([X_FLANGE_IN_R - MOTOR_ENC_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
}
