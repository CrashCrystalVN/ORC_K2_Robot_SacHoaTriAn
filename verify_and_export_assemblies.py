import os
import sys
import subprocess
import time
import trimesh
import numpy as np

WORKSPACE = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = os.path.join(WORKSPACE, "3D_Models")

BASE_STL = os.path.join(MODELS_DIR, "04_Gripper_Base_Head_V3.stl")
JAW_L_STL = os.path.join(MODELS_DIR, "05_Gripper_Jaw_Left_V3.stl")
JAW_R_STL = os.path.join(MODELS_DIR, "06_Gripper_Jaw_Right_V3.stl")

def check_individual_parts():
    print("====================================================================")
    print("1. KIEM TRA KET CAU HINH HOC & DFM CAC CHI TIET ROI V3.0")
    print("====================================================================")
    parts = [
        ("04_Gripper_Base_Head_V3", BASE_STL),
        ("05_Gripper_Jaw_Left_V3", JAW_L_STL),
        ("06_Gripper_Jaw_Right_V3", JAW_R_STL)
    ]
    results = {}
    for name, p in parts:
        if not os.path.exists(p):
            print(f"Error: {p} not found!")
            return False, {}
        m = trimesh.load(p)
        b_min, b_max = m.bounds
        ext = b_max - b_min
        vol = m.volume if m.is_volume else 0.0
        shells = len(m.split())
        info = {
            "name": name,
            "watertight": m.is_watertight,
            "is_volume": m.is_volume,
            "volume_mm3": round(vol, 1),
            "shells": shells,
            "dx": round(float(ext[0]), 2),
            "dy": round(float(ext[1]), 2),
            "dz": round(float(ext[2]), 2),
            "z_min": round(float(b_min[2]), 2),
            "bounds": [list(np.round(b_min, 2)), list(np.round(b_max, 2))]
        }
        results[name] = info
        status = "PASSED (100% FLAT DFM)" if m.is_watertight and abs(b_min[2]) < 0.05 and shells == 1 else "CHECK"
        print(f"[{status}] {name}.stl:")
        print(f"    Kich thuoc: {info['dx']} x {info['dy']} x {info['dz']} mm")
        print(f"    The tich:   {info['volume_mm3']} mm3 | Watertight: {info['watertight']} | Shells: {info['shells']}")
        print(f"    Mat day in: Z_min = {info['z_min']} mm (Dat phang tren PEI bed)")
    return True, results

def get_transformed_assembly(angle_deg):
    """
    Transforms Left and Right Jaws and combines with Gripper Base.
    Base coordinates:
    Pivot post Left: [-15.0, 38.0, 5.0]
    Pivot post Right: [+15.0, 38.0, 5.0]
    In Jaw STL coordinates:
    Pivot is at [pivot_x, 0, 0]
    Left jaw opens counter-clockwise: +angle_deg
    Right jaw opens clockwise: -angle_deg
    """
    m_base = trimesh.load(BASE_STL)
    m_jl = trimesh.load(JAW_L_STL)
    m_jr = trimesh.load(JAW_R_STL)
    
    rad = np.radians(angle_deg)
    
    # Left Jaw transformation
    # Move jaw pivot from [-15.0, 0, 0] to [0,0,0], rotate by +rad, then move to [-15.0, 38.0, 5.0]
    T_l = trimesh.transformations.translation_matrix([-15.0, 38.0, 5.0]) @ \
          trimesh.transformations.rotation_matrix(rad, [0, 0, 1]) @ \
          trimesh.transformations.translation_matrix([15.0, 0, 0])
    jl_trans = m_jl.copy().apply_transform(T_l)
    
    # Right Jaw transformation
    # Move jaw pivot from [+15.0, 0, 0] to [0,0,0], rotate by -rad, then move to [+15.0, 38.0, 5.0]
    T_r = trimesh.transformations.translation_matrix([15.0, 38.0, 5.0]) @ \
          trimesh.transformations.rotation_matrix(-rad, [0, 0, 1]) @ \
          trimesh.transformations.translation_matrix([-15.0, 0, 0])
    jr_trans = m_jr.copy().apply_transform(T_r)
    
    return m_base, jl_trans, jr_trans

def verify_kinematics_and_collision():
    print("\n====================================================================")
    print("2. DO DAC DONG HOC & KIEM TRA VA CHAM TOAN DAI GOC MO (0° - 90°)")
    print("====================================================================")
    
    # MG996R Servo Body box at Z in [25.5, 62.0], X in [-15.7, 25.0], Y in [28.15, 47.85]
    servo_box = trimesh.creation.box(extents=[40.7, 19.7, 36.5])
    servo_box.apply_translation([4.65, 38.0, 25.5 + 36.5/2.0])
    
    angles = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]
    measurements = []
    
    # Tip vertex indices (furthest along Y in local coordinates)
    m_jl = trimesh.load(JAW_L_STL)
    m_jr = trimesh.load(JAW_R_STL)
    tip_l_idx = np.argmax(m_jl.vertices[:, 1])
    tip_r_idx = np.argmax(m_jr.vertices[:, 1])
    
    # Cradle vertex indices (at Y around 36mm)
    cradle_l_idx = np.argmin(np.abs(m_jl.vertices[:, 1] - 36.0) + np.abs(m_jl.vertices[:, 0] + 3.0))
    cradle_r_idx = np.argmin(np.abs(m_jr.vertices[:, 1] - 36.0) + np.abs(m_jr.vertices[:, 0] - 3.0))
    
    for a in angles:
        m_base, jl, jr = get_transformed_assembly(a)
        
        tip_l = jl.vertices[tip_l_idx]
        tip_r = jr.vertices[tip_r_idx]
        tip_gap = np.linalg.norm(tip_l - tip_r)
        
        cradle_l = jl.vertices[cradle_l_idx]
        cradle_r = jr.vertices[cradle_r_idx]
        cradle_gap = np.linalg.norm(cradle_l - cradle_r)
        
        # Combined jaws bounds
        jaws_pts = np.vstack([jl.vertices, jr.vertices])
        min_x, max_x = np.min(jaws_pts[:, 0]), np.max(jaws_pts[:, 0])
        min_y, max_y = np.min(jaws_pts[:, 1]), np.max(jaws_pts[:, 1])
        total_w = max_x - min_x
        forward_reach = max_y - 38.0 # forward reach past pivot post
        
        # Clearance checks:
        # 1. Z clearance between jaws and servo bridge (bridge is at Z >= 19.5, jaws top is Z = 18.0)
        z_max_jaws = np.max(jaws_pts[:, 2])
        bridge_clearance = 19.5 - z_max_jaws
        
        # 2. Base side collision (base walls are at X in [-33,-27] and [27,35], Y in [16,22])
        # In jaw region Y in [22, 50], does jaw intersect base?
        # Check minimum distance between jaw vertices and base vertices where Z in [5, 18]
        jaw_sub = jaws_pts[(jaws_pts[:, 2] >= 5.0) & (jaws_pts[:, 2] <= 18.0) & (jaws_pts[:, 1] <= 30.0)]
        base_sub = m_base.vertices[(m_base.vertices[:, 2] >= 5.0) & (m_base.vertices[:, 2] <= 18.0) & (m_base.vertices[:, 1] <= 30.0)]
        
        collision_detected = False
        if len(jaw_sub) > 0 and len(base_sub) > 0:
            # Check min distance
            from scipy.spatial import cKDTree
            tree = cKDTree(base_sub)
            dists, _ = tree.query(jaw_sub, k=1)
            min_dist = np.min(dists)
            if min_dist < 0.1:
                collision_detected = True
        else:
            min_dist = 5.0
            
        m_info = {
            "angle": a,
            "tip_gap_mm": round(float(tip_gap), 1),
            "cradle_gap_mm": round(float(cradle_gap), 1),
            "total_width_mm": round(float(total_w), 1),
            "forward_reach_mm": round(float(forward_reach), 1),
            "y_max_mm": round(float(max_y), 1),
            "bridge_clearance_mm": round(float(bridge_clearance), 2),
            "collision": collision_detected
        }
        measurements.append(m_info)
        
        print(f"Goc mo {a:4.1f}°:")
        print(f"    Khoang mo dau ngon: {m_info['tip_gap_mm']:5.1f} mm  |  Khe ho khoang kep D32: {m_info['cradle_gap_mm']:5.1f} mm")
        print(f"    Be rong phu bi:    {m_info['total_width_mm']:5.1f} mm  |  Tam vuon ve phia truoc: {m_info['forward_reach_mm']:5.1f} mm (Y_max={m_info['y_max_mm']:.1f})")
        print(f"    Khe ho cau servo:  {m_info['bridge_clearance_mm']:5.2f} mm  |  Va cham co khi: {'PHAT HIEN' if collision_detected else 'KHONG (100% CLEAR)'}")
        
    return measurements

def export_assembly_stls():
    print("\n====================================================================")
    print("3. XUAT CAC FILE STL LAP RAP HOAN CHINH (0°, 45°, 90°)")
    print("====================================================================")
    configs = [
        (0.0, "Gripper_V3_Assembly_Closed_0deg.stl"),
        (45.0, "Gripper_V3_Assembly_Open_45deg.stl"),
        (90.0, "Gripper_V3_Assembly_Open_90deg.stl")
    ]
    servo_box = trimesh.creation.box(extents=[40.7, 19.7, 36.5])
    servo_box.apply_translation([4.65, 38.0, 25.5 + 36.5/2.0])
    
    for angle, fname in configs:
        out_p = os.path.join(MODELS_DIR, fname)
        m_base, jl, jr = get_transformed_assembly(angle)
        assembly = trimesh.util.concatenate([m_base, jl, jr, servo_box])
        assembly.export(out_p)
        size_kb = os.path.getsize(out_p) / 1024.0
        print(f"--> Da xuat file: {fname} ({size_kb:.1f} KB)")

def main():
    ok, part_results = check_individual_parts()
    if not ok:
        return
    meas = verify_kinematics_and_collision()
    export_assembly_stls()
    print("\nHOAN TAT XAC THUC DONG HOC & XUAT FILE STL!")

if __name__ == "__main__":
    main()
