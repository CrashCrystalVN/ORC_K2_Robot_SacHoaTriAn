"""
BỘ TẠO FILE CAD STEP (ISO 10303-21) CHO ROBOT ORC K2 (4WD)
Sử dụng nhân đồ họa công nghiệp OpenCASCADE (OCP)
Thiết kế chính xác 100% Full bộ OhStem & Giải đấu "Sắc Hoa Tri Ân"
"""

import os
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import cad_core

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"=== ĐANG TẠO CÁC FILE CAD CHUẨN STEP (4WD) TẠI: {out_dir} ===")

    step_items = [
        ("01_Chassis_Lower_Base.step", cad_core.create_lower_base_4wd()),
        ("02_Chassis_Upper_Deck.step", cad_core.create_upper_deck()),
        ("03_Gripper_Jaw_Left_Flower32.step", cad_core.create_gripper_jaw(is_left=True)),
        ("03_Gripper_Jaw_Right_Flower32.step", cad_core.create_gripper_jaw(is_left=False)),
        ("04_Four_Bar_Parallel_Arm.step", cad_core.create_four_bar_arm()),
        ("05_Standoff_Pillar_M3_48mm.step", cad_core.create_standoff()),
        ("06_Ultrasonic_Sensor_Bracket.step", cad_core.create_ultrasonic_bracket()),
        ("07_TT_Motor_Mount_Bracket.step", cad_core.create_motor_bracket()),
        ("08_Gripper_Base_Bracket.step", cad_core.create_gripper_base()),
        ("09_Lift_Arm_Stanchion_Left.step", cad_core.create_lift_stanchion(is_left=True)),
        ("09_Lift_Arm_Stanchion_Right.step", cad_core.create_lift_stanchion(is_left=False)),
        ("00_ORC_K2_Full_Assembly.step", cad_core.create_full_assembly_4wd()),
    ]

    for filename, shape in step_items:
        filepath = os.path.join(out_dir, filename)
        cad_core.export_step(shape, filepath)

    print("\n>>> HOÀN THÀNH XUẤT TOÀN BỘ FILE CAD STEP CHUẨN XÁC 100%! <<<")
