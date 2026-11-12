// ====================================================================
// DU AN: ROBOT THI DAU ORC-K2 - SAC HOA TRI AN
// MODULE: DAU KEP TAI NANG GOC MO 0 - 90 DO (GRIPPER V3.0 MG996R)
// File: gripper_v2.scad (Forward Compatibility Wrapper to 3D_Models/gripper_v3_mg996r.scad)
// ====================================================================

include <3D_Models/gripper_v3_mg996r.scad>;

module gripper_jaw_v2(is_left = true) {
    gripper_jaw_v3(is_left = is_left);
}

module gripper_base_head_v2() {
    gripper_base_head_v3();
}

module gripper_v2_assembly(grip_angle = 0.0) {
    gripper_v3_assembly(grip_angle = grip_angle);
}

module export_jaw_left() {
    export_jaw_left_v3();
}

module export_jaw_right() {
    export_jaw_right_v3();
}

module export_gripper_base() {
    export_gripper_base_v3();
}
