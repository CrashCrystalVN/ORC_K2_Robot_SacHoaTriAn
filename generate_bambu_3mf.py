"""
Bambu Lab A1 Multi-Plate 3MF Generator for ORC K2 Robot - Sắc Hoa Tri Ân (V4.0 - DFM 3D-PRINT OPTIMIZED EDITION)
Generates:
1. 00_ORC_K2_V3.1_Bambu_A1_All_5_Plates.3mf & 00_ORC_K2_V4.0_DFM_Bambu_A1_Core_2_Plates.3mf
2. Individual plate 3MF files in 3MF_Models/
All parts are 100% flat on the build plate (Z = 0.0 mm) and require ZERO support (enable_support = 0)!
"""

import os
import struct
import zipfile
import json
import uuid
import re

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
TEMPLATE_3MF = r"C:\Users\vuasu\Downloads\Robot.Arm.3mf"

os.makedirs(OUT_3MF_DIR, exist_ok=True)


def load_binary_stl_and_center(stl_path, rot_y_90=False):
    """
    Loads an STL file (binary or ASCII), centers the mesh around (0, 0, 0) in X, Y, Z, and returns:
      vertices: list of (x, y, z)
      triangles: list of (v1, v2, v3)
      half_extents: (hx, hy, hz) where mesh spans [-hx, +hx], [-hy, +hy], [-hz, +hz]
      orig_offset: (cx, cy, cz)
      bottom_area_ratio: percentage of bottom vertices at z == min_z
    """
    with open(stl_path, "rb") as f:
        head = f.read(80)
        is_ascii = head.startswith(b"solid") and (b"\n" in head or b"\r" in head)
        raw_tris = []
        if is_ascii:
            f.seek(0)
            text = f.read().decode("latin1", errors="ignore")
            pattern = re.compile(
                r"facet\s+normal\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
                r"outer\s+loop\s+"
                r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
                r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
                r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
                r"endloop\s+endfacet",
                re.DOTALL,
            )
            for m in pattern.finditer(text):
                vals = [float(x) for x in m.groups()]
                raw_tris.append(((vals[3], vals[4], vals[5]), (vals[6], vals[7], vals[8]), (vals[9], vals[10], vals[11])))
        else:
            num_tris = struct.unpack("<I", f.read(4))[0]
            for _ in range(num_tris):
                data = struct.unpack("<12fH", f.read(50))
                p1 = (data[3], data[4], data[5])
                p2 = (data[6], data[7], data[8])
                p3 = (data[9], data[10], data[11])
                raw_tris.append((p1, p2, p3))

    def transform_pt(pt):
        x, y, z = pt
        if rot_y_90:
            return (-z, y, x)
        return (x, y, z)

    vert_map = {}
    vertices = []
    triangles = []

    for p1, p2, p3 in raw_tris:
        idxs = []
        for pt in (p1, p2, p3):
            tpt = transform_pt(pt)
            key = (round(tpt[0], 5), round(tpt[1], 5), round(tpt[2], 5))
            if key not in vert_map:
                vert_map[key] = len(vertices)
                vertices.append(tpt)
            idxs.append(vert_map[key])
        if idxs[0] != idxs[1] and idxs[1] != idxs[2] and idxs[2] != idxs[0]:
            triangles.append((idxs[0], idxs[1], idxs[2]))

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    cx = 0.5 * (min_x + max_x)
    cy = 0.5 * (min_y + max_y)
    cz = 0.5 * (min_z + max_z)

    hx = 0.5 * (max_x - min_x)
    hy = 0.5 * (max_y - min_y)
    hz = 0.5 * (max_z - min_z)

    centered_verts = [(v[0] - cx, v[1] - cy, v[2] - cz) for v in vertices]
    return centered_verts, triangles, (hx, hy, hz), (cx, cy, cz)


def build_object_model_xml(mesh_obj_id, vertices, triangles):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">',
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
        ' <resources>',
        f'  <object id="{mesh_obj_id}" p:UUID="{uuid.uuid4()}" type="model">',
        '   <mesh>',
        '    <vertices>',
    ]
    for vx, vy, vz in vertices:
        lines.append(f'     <vertex x="{vx:.6f}" y="{vy:.6f}" z="{vz:.6f}"/>')
    lines.append('    </vertices>')
    lines.append('    <triangles>')
    for v1, v2, v3 in triangles:
        lines.append(f'     <triangle v1="{v1}" v2="{v2}" v3="{v3}"/>')
    lines.append('    </triangles>')
    lines.append('   </mesh>')
    lines.append('  </object>')
    lines.append(' </resources>')
    lines.append('</model>')
    return "\n".join(lines)


def get_a1_project_settings():
    template_candidates = [
        TEMPLATE_3MF,
        os.path.join(OUT_3MF_DIR, "Plate_6_K2_Control_Hub_Riser_Adapter_Patch.3mf"),
        os.path.join(OUT_3MF_DIR, "00_ORC_K2_V3.1_Bambu_A1_All_5_Plates.3mf"),
    ]
    cfg = {}
    for cand in template_candidates:
        if os.path.exists(cand):
            with zipfile.ZipFile(cand, "r") as z:
                cfg = json.loads(z.read("Metadata/project_settings.config").decode("utf-8"))
            break
    cfg["printer_model"] = "Bambu Lab A1"
    cfg["printer_settings_id"] = "Bambu Lab A1 0.4 nozzle"
    cfg["print_settings_id"] = "0.20mm Strength @BBL A1"
    cfg["curr_bed_type"] = "Textured PEI Plate"
    cfg["wall_loops"] = "3"
    cfg["sparse_infill_density"] = "25%"
    cfg["sparse_infill_pattern"] = "gyroid"
    cfg["bottom_shell_layers"] = "4"
    cfg["top_shell_layers"] = "4"
    cfg["enable_support"] = "0"
    cfg["support_type"] = "tree(auto)"
    cfg["support_on_build_plate_only"] = "1"
    cfg["brim_type"] = "no_brim"
    cfg["filament_colour"] = ["#F98C00"]
    return json.dumps(cfg, indent=4)


# Define the unique DFM V4.0 meshes (ALL pre-oriented flat at Z=0.0, ZERO support needed!)
MESH_DEFS = {
    "chassis": {
        "stl": "01_Monocoque_Chassis_GA25_Mecanum.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "25%",
        "walls": "3",
    },
    "tower_left": {
        "stl": "01B_Lift_Tower_Left_FlatPrint.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "tower_right": {
        "stl": "01C_Lift_Tower_Right_MG996R_FlatPrint.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "mcu_deck": {
        "stl": "01D_MCU_Control_Hub_Deck_FlatPrint.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "25%",
        "walls": "3",
    },
    "line_spacer": {
        "stl": "01E_Line_Sensor_Spacer_Pod_FlatPrint.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "3",
    },
    "k2_adapter_plate": {
        "stl": "01D_K2_Hub_Adapter_Plate.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "k2_base_frame": {
        "stl": "01D_Base_Riser_Frame.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "standoff_18mm": {
        "stl": "01D_Riser_Standoff_18mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "k2_adapter_monolithic": {
        "stl": "01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "clamp_rear_left": {
        "stl": "02B_GA25_Rear_Motor_Clamp_Left.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "clamp_rear_right": {
        "stl": "02C_GA25_Rear_Motor_Clamp_Right.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "clamp_rear_uni": {
        "stl": "02_GA25_Rear_Motor_Clamp_Universal.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "clamp": {
        "stl": "02_GA25_Motor_Clamp_Cap.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "arm_lower": {
        "stl": "03_Parallel_Arm_Truss_IBeam.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "coupler_s1": {
        "stl": "08_S1_MG996R_Round_Horn_Drive_Coupler.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "50%",
        "walls": "4",
    },
    "arm_upper": {
        "stl": "03B_Upper_H_Frame_Follower_Arm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "wrist_s3": {
        "stl": "04A_Wrist_Clevis_Pitch_Bracket_S3.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "gripper_head": {
        "stl": "04_Gripper_Base_Head.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "3",
    },
    "jaw_left": {
        "stl": "05_Gripper_Jaw_Left_VGuide_Flower32.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "jaw_right": {
        "stl": "06_Gripper_Jaw_Right_VGuide_Flower32.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "horn": {
        "stl": "08_MG996R_Servo_Lever_Horn.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "80%",
        "walls": "5",
    },
    "wheel": {
        "stl": "07_Mecanum_Wheel_K3_80mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "25%",
        "walls": "3",
    },
}

# All plates laid out in a single horizontal row (Y_origin = 0.0) so even in perspective views
# no plate appears below the primary build plate grid!
PLATE_ORIGINS = {
    1: (0.0, 0.0),
    2: (307.2, 0.0),
    3: (614.4, 0.0),
    4: (921.6, 0.0),
    5: (1228.8, 0.0),
    6: (1536.0, 0.0),
    7: (1843.2, 0.0),
    8: (2150.4, 0.0),
}

PLATES = [
    {
        "index": 1,
        "name": "Plate 1 - Khung Gam Phang + Be MCU + De Line + 4x Nap Kep (0% Support)",
        "file_slug": "Plate_1_Khung_Gam_Chinh_Chassis",
        "items": [
            {"mesh": "chassis", "name": "01_Monocoque_Chassis_Flat_DFM", "local_x": 84.0, "local_y": 128.0},
            {"mesh": "mcu_deck", "name": "01D_MCU_Control_Hub_Deck", "local_x": 204.0, "local_y": 62.0},
            {"mesh": "line_spacer", "name": "01E_Line_Sensor_Spacer_Pod", "local_x": 204.0, "local_y": 118.0},
            {"mesh": "clamp", "name": "02_GA25_Motor_Clamp_Cap_FL", "local_x": 176.0, "local_y": 170.0},
            {"mesh": "clamp", "name": "02_GA25_Motor_Clamp_Cap_FR", "local_x": 204.0, "local_y": 170.0},
            {"mesh": "clamp_rear_left", "name": "02B_GA25_Rear_Motor_Clamp_Left", "local_x": 176.0, "local_y": 222.0},
            {"mesh": "clamp_rear_right", "name": "02C_GA25_Rear_Motor_Clamp_Right", "local_x": 204.0, "local_y": 222.0},
        ],
    },
    {
        "index": 2,
        "name": "Plate 2 - 2x Thap Nang Phang + 2x Tay Nang H-Frame + Cum Tay Kep 3 Hoa V7.0 (0% Support)",
        "file_slug": "Plate_2_Tay_Nang_HFrame_Va_4x_Nap_Kep_Motor",
        "items": [
            {"mesh": "tower_left", "name": "01B_Lift_Tower_Left_FlatPrint", "local_x": 65.0, "local_y": 50.0},
            {"mesh": "tower_right", "name": "01C_Lift_Tower_Right_MG996R_FlatPrint", "local_x": 180.0, "local_y": 50.0},
            {"mesh": "arm_lower", "name": "03_Lower_H_Frame_Drive_Arm", "local_x": 36.0, "local_y": 160.0},
            {"mesh": "arm_upper", "name": "03B_Upper_H_Frame_Follower_Arm", "local_x": 84.0, "local_y": 160.0},
            {"mesh": "jaw_left", "name": "05_Gripper_Jaw_Left_3Flower_V7.1", "local_x": 130.0, "local_y": 162.0},
            {"mesh": "jaw_right", "name": "06_Gripper_Jaw_Right_3Flower_V7.1", "local_x": 168.0, "local_y": 162.0},
            {"mesh": "gripper_head", "name": "04_Gripper_Base_Head_Pitch_V7.1", "local_x": 218.0, "local_y": 116.0},
            {"mesh": "wrist_s3", "name": "04A_Wrist_Clevis_Pitch_Bracket_S3_V7.1", "local_x": 218.0, "local_y": 182.0},
            {"mesh": "horn", "name": "08_MG996R_Servo_Lever_Horn_S1", "local_x": 200.0, "local_y": 230.0},
            {"mesh": "horn", "name": "08_MG996R_Servo_Lever_Horn_S2", "local_x": 232.0, "local_y": 230.0},
        ],
    },
    {
        "index": 3,
        "name": "Plate 3 - Cum Tay Kep 3 Tru Hoa Gap Doc 90° V7.1 Rieng (Co Tay 04A + Be 04 + 2 Ham 05, 06)",
        "file_slug": "Plate_3_Cum_Tay_Kep_Hoa_Va_Tay_Gat_MG996R",
        "items": [
            {"mesh": "gripper_head", "name": "04_Gripper_Base_Head_Pitch_V7.1", "local_x": 92.0, "local_y": 55.0},
            {"mesh": "wrist_s3", "name": "04A_Wrist_Clevis_Pitch_Bracket_S3_V7.1", "local_x": 172.0, "local_y": 55.0},
            {"mesh": "jaw_left", "name": "05_Gripper_Jaw_Left_3Flower_V7.1", "local_x": 75.0, "local_y": 162.0},
            {"mesh": "jaw_right", "name": "06_Gripper_Jaw_Right_3Flower_V7.1", "local_x": 181.0, "local_y": 162.0},
            {"mesh": "coupler_s1", "name": "08_S1_MG996R_Round_Horn_Drive_Coupler", "local_x": 128.0, "local_y": 135.0},
            {"mesh": "horn", "name": "08_MG996R_Servo_Lever_Horn_S1", "local_x": 128.0, "local_y": 182.0},
            {"mesh": "horn", "name": "08_MG996R_Servo_Lever_Horn_S2", "local_x": 128.0, "local_y": 218.0},
        ],
    },
    {
        "index": 4,
        "name": "Plate 4 - Khung Gam Chinh Rieng (Chassis Standalone)",
        "file_slug": "Plate_4_Combo_Khung_Gam_Va_4x_Nap_Kep",
        "items": [
            {"mesh": "chassis", "name": "01_Monocoque_Chassis_Flat_DFM", "local_x": 128.0, "local_y": 128.0},
        ],
    },
    {
        "index": 5,
        "name": "Plate 5 - 4x Banh Xe Mecanum K3 80mm (Du Phong)",
        "file_slug": "Plate_5_4x_Banh_Xe_Mecanum_K3_80mm",
        "items": [
            {"mesh": "wheel", "name": "07_Mecanum_Wheel_K3_80mm_FL", "local_x": 78.0, "local_y": 78.0},
            {"mesh": "wheel", "name": "07_Mecanum_Wheel_K3_80mm_FR", "local_x": 178.0, "local_y": 78.0},
            {"mesh": "wheel", "name": "07_Mecanum_Wheel_K3_80mm_RL", "local_x": 78.0, "local_y": 178.0},
            {"mesh": "wheel", "name": "07_Mecanum_Wheel_K3_80mm_RR", "local_x": 178.0, "local_y": 178.0},
        ],
    },
    {
        "index": 6,
        "name": "Plate 6 - Bo K2 Hub 2 Tang V9.0 Cantilever (Ne Thap Nang 23mm + Ranh Day Kin Khoa Tan M3 + 2x Nep Motor Sau)",
        "file_slug": "Plate_6_K2_Control_Hub_Riser_Adapter_Patch",
        "items": [
            {"mesh": "k2_adapter_plate", "name": "01D_K2_Hub_Adapter_Plate_V9.0", "local_x": 74.0, "local_y": 115.0},
            {"mesh": "k2_base_frame", "name": "01D_Base_Riser_Frame_V9.0", "local_x": 196.0, "local_y": 115.0},
            {"mesh": "clamp_rear_left", "name": "02B_GA25_Rear_Motor_Clamp_Left", "local_x": 95.0, "local_y": 212.0},
            {"mesh": "clamp_rear_right", "name": "02C_GA25_Rear_Motor_Clamp_Right", "local_x": 160.0, "local_y": 212.0},
        ],
    },
    {
        "index": 7,
        "name": "Plate 7 - K2 Riser Monolithic V9.0 Cantilever (Ne Cum Gap Tru 23mm + Ranh Day Kin Giữ Tan M3 + Ha Thang Dung)",
        "file_slug": "Plate_7_K2_Monolithic_Riser_Va_Nep_Motor_Sau",
        "items": [
            {"mesh": "k2_adapter_monolithic", "name": "01D_K2_Control_Hub_Riser_Monolithic_V9.0", "local_x": 128.0, "local_y": 100.0},
            {"mesh": "clamp_rear_left", "name": "02B_GA25_Rear_Motor_Clamp_Left", "local_x": 95.0, "local_y": 205.0},
            {"mesh": "clamp_rear_right", "name": "02C_GA25_Rear_Motor_Clamp_Right", "local_x": 160.0, "local_y": 205.0},
        ],
    },
    {
        "index": 8,
        "name": "Plate 8 - Cum Servo S1 Nang Ha V5.0 (Tay Nang Duoi + Thap Phai + Khop Khoa Dia Tron S1)",
        "file_slug": "Plate_8_Cum_Servo_S1_Nang_Ha_Va_Tay_Nang",
        "items": [
            {"mesh": "arm_lower", "name": "03_Parallel_Arm_Truss_IBeam_V5.0", "local_x": 75.0, "local_y": 128.0},
            {"mesh": "tower_right", "name": "01C_Lift_Tower_Right_MG996R_V5.0", "local_x": 165.0, "local_y": 128.0},
            {"mesh": "coupler_s1", "name": "08_S1_MG996R_Round_Horn_Drive_Coupler", "local_x": 165.0, "local_y": 200.0},
        ],
    },
]


def create_bambu_3mf(plates_to_include, output_path, project_settings_str, loaded_meshes):
    """
    Creates a Bambu Studio / OrcaSlicer native 3MF package containing one or more build plates.
    """
    content_types_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="gcode" ContentType="text/x.gcode"/>
</Types>"""

    root_rels_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>"""

    used_mesh_keys = []
    for pl in plates_to_include:
        for it in pl["items"]:
            if it["mesh"] not in used_mesh_keys:
                used_mesh_keys.append(it["mesh"])

    mesh_key_to_ids = {}
    next_id = 1
    for mk in used_mesh_keys:
        mesh_obj_id = next_id
        next_id += 1
        mesh_key_to_ids[mk] = {
            "mesh_obj_id": mesh_obj_id,
            "model_path": f"/3D/Objects/object_{mesh_obj_id}.model",
            "zip_path": f"3D/Objects/object_{mesh_obj_id}.model",
        }

    placed_records = []
    identify_counter = 1001
    for pl_idx, pl in enumerate(plates_to_include, start=1):
        px_origin, py_origin = PLATE_ORIGINS.get(pl_idx, (0.0, 0.0)) if len(plates_to_include) > 1 else (0.0, 0.0)
        for it in pl["items"]:
            wrapper_id = next_id
            next_id += 1
            mk = it["mesh"]
            m_info = mesh_key_to_ids[mk]
            verts, tris, (hx, hy, hz), (cx, cy, cz) = loaded_meshes[mk]
            world_x = px_origin + it["local_x"]
            world_y = py_origin + it["local_y"]
            world_z = hz  # places bottom of centered mesh exactly at Z = 0.0 on the build plate
            placed_records.append({
                "plate_idx": pl_idx,
                "plate_name": pl["name"],
                "wrapper_id": wrapper_id,
                "mesh_obj_id": m_info["mesh_obj_id"],
                "model_path": m_info["model_path"],
                "name": it["name"],
                "mesh_key": mk,
                "world_x": world_x,
                "world_y": world_y,
                "world_z": world_z,
                "local_x": it["local_x"],
                "local_y": it["local_y"],
                "hz": hz,
                "cx": cx,
                "cy": cy,
                "cz": cz,
                "face_count": len(tris),
                "identify_id": identify_counter,
            })
            identify_counter += 11

    rels_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for idx, mk in enumerate(used_mesh_keys, start=1):
        mp = mesh_key_to_ids[mk]["model_path"]
        rels_lines.append(
            f' <Relationship Target="{mp}" Id="rel-{idx}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        )
    rels_lines.append('</Relationships>')
    model_rels_xml = "\n".join(rels_lines)

    main_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">',
        ' <metadata name="Application">BambuStudio-02.05.03.61</metadata>',
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
        ' <metadata name="Title">ORC K2 Robot - Sac Hoa Tri An V4.0 (DFM 3D-Print Optimized - Zero Support)</metadata>',
        ' <resources>',
    ]
    for rec in placed_records:
        main_lines.append(f'  <object id="{rec["wrapper_id"]}" p:UUID="{uuid.uuid4()}" type="model">')
        main_lines.append('   <components>')
        main_lines.append(
            f'    <component p:path="{rec["model_path"]}" objectid="{rec["mesh_obj_id"]}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0" />'
        )
        main_lines.append('   </components>')
        main_lines.append('  </object>')
    main_lines.append(' </resources>')
    main_lines.append(f' <build p:UUID="{uuid.uuid4()}">')
    for rec in placed_records:
        main_lines.append(
            f'  <item objectid="{rec["wrapper_id"]}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 {rec["world_x"]:.4f} {rec["world_y"]:.4f} {rec["world_z"]:.4f}" printable="1" />'
        )
    main_lines.append(' </build>')
    main_lines.append('</model>')
    main_model_xml = "\n".join(main_lines)

    ms_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<config>',
    ]
    for rec in placed_records:
        mdef = MESH_DEFS[rec["mesh_key"]]
        ms_lines.append(f'  <object id="{rec["wrapper_id"]}">')
        ms_lines.append(f'    <metadata key="name" value="{rec["name"]}"/>')
        ms_lines.append('    <metadata key="extruder" value="1"/>')
        ms_lines.append(f'    <metadata key="enable_support" value="{mdef["support"]}"/>')
        ms_lines.append(f'    <metadata key="wall_loops" value="{mdef["walls"]}"/>')
        ms_lines.append(f'    <metadata key="sparse_infill_density" value="{mdef["infill"]}"/>')
        ms_lines.append(f'    <metadata face_count="{rec["face_count"]}"/>')
        ms_lines.append(f'    <part id="{rec["mesh_obj_id"]}" subtype="normal_part">')
        ms_lines.append(f'      <metadata key="name" value="{rec["name"]}"/>')
        ms_lines.append('      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>')
        ms_lines.append('      <metadata key="source_object_id" value="0"/>')
        ms_lines.append('      <metadata key="source_volume_id" value="0"/>')
        ms_lines.append(f'      <metadata key="source_offset_x" value="{rec["cx"]:.4f}"/>')
        ms_lines.append(f'      <metadata key="source_offset_y" value="{rec["cy"]:.4f}"/>')
        ms_lines.append(f'      <metadata key="source_offset_z" value="{rec["cz"]:.4f}"/>')
        ms_lines.append(
            f'      <mesh_stat face_count="{rec["face_count"]}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>'
        )
        ms_lines.append('    </part>')
        ms_lines.append('  </object>')

    for pl_idx, pl in enumerate(plates_to_include, start=1):
        ms_lines.append('  <plate>')
        ms_lines.append(f'    <metadata key="plater_id" value="{pl_idx}"/>')
        ms_lines.append(f'    <metadata key="plater_name" value="{pl["name"].replace("&", "&amp;")}"/>')
        ms_lines.append('    <metadata key="locked" value="false"/>')
        ms_lines.append('    <metadata key="filament_map_mode" value="Auto For Flush"/>')
        ms_lines.append('    <metadata key="filament_maps" value="1"/>')
        ms_lines.append('    <metadata key="filament_volume_maps" value="0"/>')
        for rec in placed_records:
            if rec["plate_idx"] == pl_idx:
                ms_lines.append('    <model_instance>')
                ms_lines.append(f'      <metadata key="object_id" value="{rec["wrapper_id"]}"/>')
                ms_lines.append('      <metadata key="instance_id" value="0"/>')
                ms_lines.append(f'      <metadata key="identify_id" value="{rec["identify_id"]}"/>')
                ms_lines.append('    </model_instance>')
        ms_lines.append('  </plate>')

    ms_lines.append('  <assemble>')
    for rec in placed_records:
        ms_lines.append(
            f'   <assemble_item object_id="{rec["wrapper_id"]}" instance_id="0" transform="1 0 0 0 1 0 0 0 1 {rec["world_x"]:.4f} {rec["world_y"]:.4f} {rec["world_z"]:.4f}" offset="0 0 0" />'
        )
    ms_lines.append('  </assemble>')
    ms_lines.append('</config>')
    model_settings_xml = "\n".join(ms_lines)

    slice_info_xml = """<?xml version="1.0" encoding="UTF-8"?>
<config>
  <header>
    <header_item key="X-BBL-Client-Type" value="slicer"/>
    <header_item key="X-BBL-Client-Version" value="02.05.03.61"/>
  </header>
</config>"""

    cut_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<objects>']
    for idx in range(1, len(used_mesh_keys) + 1):
        cut_lines.append(f' <object id="{idx}">')
        cut_lines.append('  <cut_id id="0" check_sum="1" connectors_cnt="0"/>')
        cut_lines.append(' </object>')
    cut_lines.append('</objects>')
    cut_info_xml = "\n".join(cut_lines)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("3D/3dmodel.model", main_model_xml)
        zf.writestr("3D/_rels/3dmodel.model.rels", model_rels_xml)
        for mk in used_mesh_keys:
            m_info = mesh_key_to_ids[mk]
            verts, tris, _, _ = loaded_meshes[mk]
            obj_xml = build_object_model_xml(m_info["mesh_obj_id"], verts, tris)
            zf.writestr(m_info["zip_path"], obj_xml)
        zf.writestr("Metadata/project_settings.config", project_settings_str)
        zf.writestr("Metadata/model_settings.config", model_settings_xml)
        zf.writestr("Metadata/slice_info.config", slice_info_xml)
        zf.writestr("Metadata/cut_information.xml", cut_info_xml)


def main():
    print("Loading and centering DFM V4.0 STL meshes for Bambu Lab A1...")
    loaded_meshes = {}
    for mk, mdef in MESH_DEFS.items():
        stl_path = os.path.join(STL_DIR, mdef["stl"])
        verts, tris, (hx, hy, hz), (cx, cy, cz) = load_binary_stl_and_center(
            stl_path, rot_y_90=mdef["rot_y_90"]
        )
        loaded_meshes[mk] = (verts, tris, (hx, hy, hz), (cx, cy, cz))
        print(
            f"  [{mk:12s}] verts={len(verts):5d}, tris={len(tris):5d}, footprint={2*hx:6.2f}x{2*hy:6.2f}mm, height={2*hz:6.2f}mm, z_bottom={cz-hz:6.2f}mm"
        )

    project_settings_str = get_a1_project_settings()

    # 1. Master 2-Plate Complete Robot Print Set (Everything except kit wheels on just 2 plates, 0% Support!)
    core_2_plates_path = os.path.join(OUT_3MF_DIR, "00_ORC_K2_V4.0_DFM_Bambu_A1_Full_Robot_2_Plates.3mf")
    create_bambu_3mf(PLATES[:2], core_2_plates_path, project_settings_str, loaded_meshes)
    print(f"Created Full Robot 2-Plate 3MF: {core_2_plates_path}")

    # 2. Also update the existing filenames so any open file in user's slicer gets updated
    all_5_plates_path = os.path.join(OUT_3MF_DIR, "00_ORC_K2_V3.1_Bambu_A1_All_5_Plates.3mf")
    create_bambu_3mf(PLATES, all_5_plates_path, project_settings_str, loaded_meshes)
    print(f"Updated Master 5-Plate 3MF:     {all_5_plates_path}")

    core_3_plates_path = os.path.join(OUT_3MF_DIR, "00_ORC_K2_V3.1_Bambu_A1_Core_3_Plates.3mf")
    create_bambu_3mf(PLATES[:3], core_3_plates_path, project_settings_str, loaded_meshes)
    print(f"Updated Core 3-Plate 3MF:       {core_3_plates_path}")

    # 3. Individual single-plate 3MF files
    for pl in PLATES:
        single_plate_path = os.path.join(OUT_3MF_DIR, f"{pl['file_slug']}.3mf")
        create_bambu_3mf([pl], single_plate_path, project_settings_str, loaded_meshes)
        print(f"Updated Single Plate 3MF:       {single_plate_path}")

    print("All DFM V4.0 3MF files generated successfully!")


if __name__ == "__main__":
    main()
