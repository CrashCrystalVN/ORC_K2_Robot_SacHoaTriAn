"""
Export Bambu Lab 3MF Production Packages
ORC K2 Robot - Sac Hoa Tri An
Generates fully compliant, ready-to-slice 3MF packages for Bambu Studio / OrcaSlicer.
"""

import os
import sys
import struct
import zipfile
import json
import uuid
import re
import numpy as np
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

TEMPLATE_CANDIDATES = [
    os.path.join(OUT_3MF_DIR, "Plate_6_K2_Control_Hub_Riser_Adapter_Patch.3mf"),
    os.path.join(OUT_3MF_DIR, "00_ORC_K2_V3.1_Bambu_A1_All_5_Plates.3mf"),
    r"C:\Users\vuasu\Downloads\Robot.Arm.3mf"
]

def load_base_project_settings():
    cfg = {}
    for cand in TEMPLATE_CANDIDATES:
        if os.path.exists(cand):
            try:
                with zipfile.ZipFile(cand, "r") as z:
                    cfg = json.loads(z.read("Metadata/project_settings.config").decode("utf-8"))
                break
            except Exception:
                continue

    # Production Preset for Bambu Lab A1
    cfg["printer_model"] = "Bambu Lab A1"
    cfg["printer_settings_id"] = "Bambu Lab A1 0.4 nozzle"
    cfg["print_settings_id"] = "0.20mm Strength @BBL A1"
    cfg["curr_bed_type"] = "Textured PEI Plate"
    cfg["wall_loops"] = "3"
    cfg["sparse_infill_density"] = "20%"
    cfg["sparse_infill_pattern"] = "gyroid"
    cfg["bottom_shell_layers"] = "4"
    cfg["top_shell_layers"] = "4"
    cfg["enable_support"] = "0"
    cfg["support_type"] = "tree(auto)"
    cfg["support_on_build_plate_only"] = "1"
    cfg["brim_type"] = "no_brim"
    cfg["filament_type"] = ["PLA"]
    cfg["filament_colour"] = ["#F98C00"]
    return cfg

def load_mesh(stl_path):
    """
    Loads STL via trimesh, centers mesh at (0,0,0) in local coords,
    returns centered vertices, triangles, half_extents (hx, hy, hz), original centroid (cx, cy, cz)
    """
    m = trimesh.load(stl_path)
    b = m.bounds
    cx = 0.5 * (b[0][0] + b[1][0])
    cy = 0.5 * (b[0][1] + b[1][1])
    cz = 0.5 * (b[0][2] + b[1][2])
    
    hx = 0.5 * (b[1][0] - b[0][0])
    hy = 0.5 * (b[1][1] - b[0][1])
    hz = 0.5 * (b[1][2] - b[0][2])
    
    centered_verts = m.vertices - np.array([cx, cy, cz])
    triangles = m.faces
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
    for v in vertices:
        lines.append(f'     <vertex x="{v[0]:.6f}" y="{v[1]:.6f}" z="{v[2]:.6f}"/>')
    lines.append('    </vertices>')
    lines.append('    <triangles>')
    for t in triangles:
        lines.append(f'     <triangle v1="{t[0]}" v2="{t[1]}" v3="{t[2]}"/>')
    lines.append('    </triangles>')
    lines.append('   </mesh>')
    lines.append('  </object>')
    lines.append(' </resources>')
    lines.append('</model>')
    return "\n".join(lines)

def export_3mf_package(output_path, plate_title, items, project_settings_dict):
    """
    items is a list of dicts:
    {
        "stl_name": "...",
        "display_name": "...",
        "pos_x": float,
        "pos_y": float,
        "walls": "3",
        "infill": "20%",
        "support": "0"
    }
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

    # Group unique meshes
    unique_stl_names = []
    for it in items:
        if it["stl_name"] not in unique_stl_names:
            unique_stl_names.append(it["stl_name"])

    loaded_unique = {}
    stl_to_mesh_id = {}
    next_id = 1
    for stl_name in unique_stl_names:
        mesh_obj_id = next_id
        next_id += 1
        stl_path = os.path.join(STL_DIR, stl_name)
        verts, tris, (hx, hy, hz), (cx, cy, cz) = load_mesh(stl_path)
        loaded_unique[stl_name] = {
            "mesh_obj_id": mesh_obj_id,
            "model_path": f"/3D/Objects/object_{mesh_obj_id}.model",
            "zip_path": f"3D/Objects/object_{mesh_obj_id}.model",
            "verts": verts,
            "tris": tris,
            "hx": hx, "hy": hy, "hz": hz,
            "cx": cx, "cy": cy, "cz": cz
        }
        stl_to_mesh_id[stl_name] = mesh_obj_id

    # Place instances
    placed = []
    identify_counter = 1001
    for it in items:
        wrapper_id = next_id
        next_id += 1
        m_info = loaded_unique[it["stl_name"]]
        world_x = it["pos_x"]
        world_y = it["pos_y"]
        world_z = m_info["hz"] # Places bottom at Z = 0.0000 exactly!
        placed.append({
            "wrapper_id": wrapper_id,
            "mesh_obj_id": m_info["mesh_obj_id"],
            "model_path": m_info["model_path"],
            "name": it["display_name"],
            "stl_name": it["stl_name"],
            "world_x": world_x,
            "world_y": world_y,
            "world_z": world_z,
            "cx": m_info["cx"],
            "cy": m_info["cy"],
            "cz": m_info["cz"],
            "hz": m_info["hz"],
            "face_count": len(m_info["tris"]),
            "identify_id": identify_counter,
            "walls": it.get("walls", "3"),
            "infill": it.get("infill", "20%"),
            "support": it.get("support", "0")
        })
        identify_counter += 11

    # 3D/_rels/3dmodel.model.rels
    rels_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for idx, stl_name in enumerate(unique_stl_names, start=1):
        mp = loaded_unique[stl_name]["model_path"]
        rels_lines.append(
            f' <Relationship Target="{mp}" Id="rel-{idx}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        )
    rels_lines.append('</Relationships>')
    model_rels_xml = "\n".join(rels_lines)

    # 3D/3dmodel.model
    main_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">',
        ' <metadata name="Application">BambuStudio-02.05.03.61</metadata>',
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
        f' <metadata name="Title">{plate_title}</metadata>',
        ' <resources>',
    ]
    for rec in placed:
        main_lines.append(f'  <object id="{rec["wrapper_id"]}" p:UUID="{uuid.uuid4()}" type="model">')
        main_lines.append('   <components>')
        main_lines.append(
            f'    <component p:path="{rec["model_path"]}" objectid="{rec["mesh_obj_id"]}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0" />'
        )
        main_lines.append('   </components>')
        main_lines.append('  </object>')
    main_lines.append(' </resources>')
    main_lines.append(f' <build p:UUID="{uuid.uuid4()}">')
    for rec in placed:
        main_lines.append(
            f'  <item objectid="{rec["wrapper_id"]}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 {rec["world_x"]:.4f} {rec["world_y"]:.4f} {rec["world_z"]:.4f}" printable="1" />'
        )
    main_lines.append(' </build>')
    main_lines.append('</model>')
    main_model_xml = "\n".join(main_lines)

    # Metadata/model_settings.config
    ms_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<config>',
    ]
    for rec in placed:
        ms_lines.append(f'  <object id="{rec["wrapper_id"]}">')
        ms_lines.append(f'    <metadata key="name" value="{rec["name"]}"/>')
        ms_lines.append('    <metadata key="extruder" value="1"/>')
        ms_lines.append(f'    <metadata key="enable_support" value="{rec["support"]}"/>')
        ms_lines.append(f'    <metadata key="wall_loops" value="{rec["walls"]}"/>')
        ms_lines.append(f'    <metadata key="sparse_infill_density" value="{rec["infill"]}"/>')
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

    ms_lines.append('  <plate>')
    ms_lines.append('    <metadata key="plater_id" value="1"/>')
    safe_title = plate_title.replace("&", "&amp;")
    ms_lines.append(f'    <metadata key="plater_name" value="{safe_title}"/>')
    ms_lines.append('    <metadata key="locked" value="false"/>')
    ms_lines.append('    <metadata key="filament_map_mode" value="Auto For Flush"/>')
    ms_lines.append('    <metadata key="filament_maps" value="1"/>')
    ms_lines.append('    <metadata key="filament_volume_maps" value="0"/>')
    for rec in placed:
        ms_lines.append('    <model_instance>')
        ms_lines.append(f'      <metadata key="object_id" value="{rec["wrapper_id"]}"/>')
        ms_lines.append('      <metadata key="instance_id" value="0"/>')
        ms_lines.append(f'      <metadata key="identify_id" value="{rec["identify_id"]}"/>')
        ms_lines.append('    </model_instance>')
    ms_lines.append('  </plate>')

    ms_lines.append('  <assemble>')
    for rec in placed:
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
    for idx in range(1, len(unique_stl_names) + 1):
        cut_lines.append(f' <object id="{idx}">')
        cut_lines.append('  <cut_id id="0" check_sum="1" connectors_cnt="0"/>')
        cut_lines.append(' </object>')
    cut_lines.append('</objects>')
    cut_info_xml = "\n".join(cut_lines)

    project_settings_str = json.dumps(project_settings_dict, indent=4)

    # Write zip file
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("3D/3dmodel.model", main_model_xml)
        zf.writestr("3D/_rels/3dmodel.model.rels", model_rels_xml)
        for stl_name, info in loaded_unique.items():
            obj_xml = build_object_model_xml(info["mesh_obj_id"], info["verts"], info["tris"])
            zf.writestr(info["zip_path"], obj_xml)
        zf.writestr("Metadata/project_settings.config", project_settings_str)
        zf.writestr("Metadata/model_settings.config", model_settings_xml)
        zf.writestr("Metadata/slice_info.config", slice_info_xml)
        zf.writestr("Metadata/cut_information.xml", cut_info_xml)

    print(f"[OK] Generated: {output_path}")

def main():
    settings = load_base_project_settings()

    print("=== EXPORTING BAMBU LAB 3MF PACKAGES ===")
    
    # ----------------------------------------------------
    # FILE 1: Chassis Base 185x185 & 200x200 (Latest V7.0 / V6 with 10 tower holes, 2S2P bay)
    # ----------------------------------------------------
    file1_185_path = os.path.join(OUT_3MF_DIR, "01_Chassis_Base_185x185_Bambu.3mf")
    file1_185_plate_path = os.path.join(OUT_3MF_DIR, "Plate_1_Chassis_Base_185x185.3mf")
    file1_path = os.path.join(OUT_3MF_DIR, "01_Chassis_Base_200x200_Bambu.3mf")
    file1_v6_path = os.path.join(OUT_3MF_DIR, "Plate_1_Chassis_Base_200x200_V6.3mf")
    
    file1_185_items = [
        {
            "stl_name": "01_Chassis_Base_185x185.stl",
            "display_name": "01_Chassis_Base_185x185_DFM_Production",
            "pos_x": 128.0,
            "pos_y": 128.0,
            "walls": "3",
            "infill": "20%",
            "support": "0"
        }
    ]
    export_3mf_package(
        file1_185_path,
        "Plate 1 - Khung Gam Chassis 185x185 (Max Dimension 172mm <= 185mm Cube - 0% Support)",
        file1_185_items,
        settings
    )
    export_3mf_package(
        file1_185_plate_path,
        "Plate 1 - Khung Gam Chassis 185x185 (Max Dimension 172mm <= 185mm Cube - 0% Support)",
        file1_185_items,
        settings
    )

    file1_items = [
        {
            "stl_name": "01_Chassis_Base_200x200.stl",
            "display_name": "01_Chassis_Base_200x200_V6_Production",
            "pos_x": 128.0,
            "pos_y": 128.0,
            "walls": "3",
            "infill": "20%",
            "support": "0"
        }
    ]
    export_3mf_package(
        file1_path,
        "Plate 1 - Khung Gam Chassis 200x200 (10 Lo Oc Thap Nang + Khoang Pin 2S2P - 0% Support)",
        file1_items,
        settings
    )
    # Also save as Plate_1_Chassis_Base_200x200_V6.3mf
    export_3mf_package(
        file1_v6_path,
        "Plate 1 - Khung Gam Chassis 200x200 V6 (10 Lo Oc Thap Nang + Khoang Pin 2S2P - 0% Support)",
        file1_items,
        settings
    )

    # ----------------------------------------------------
    # FILE 2: Combo lắp ráp Pin 2S2P & K2 Hub
    # ----------------------------------------------------
    # Items:
    # 1. 01D_Base_Riser_Frame.stl
    # 2. 01D_K2_Hub_Adapter_Plate_V11_Hardened.stl
    # 3. 02_GA25_Rear_Motor_Clamp_Universal.stl (x2)
    file2_path = os.path.join(OUT_3MF_DIR, "Plate_K2_Hub_Riser_2S2P_Pack.3mf")
    file2_items = [
        {
            "stl_name": "01D_K2_Hub_Adapter_Plate_V11_Hardened.stl",
            "display_name": "01D_K2_Hub_Adapter_Plate_V11_Hardened",
            "pos_x": 80.0,
            "pos_y": 110.0,
            "walls": "4",
            "infill": "25%",
            "support": "0"
        },
        {
            "stl_name": "01D_Base_Riser_Frame.stl",
            "display_name": "01D_Base_Riser_Frame_2S2P",
            "pos_x": 202.0,
            "pos_y": 110.0,
            "walls": "4",
            "infill": "30%",
            "support": "0"
        },
        {
            "stl_name": "02_GA25_Rear_Motor_Clamp_Universal.stl",
            "display_name": "02_GA25_Rear_Motor_Clamp_Universal_Left",
            "pos_x": 85.0,
            "pos_y": 215.0,
            "walls": "4",
            "infill": "40%",
            "support": "0"
        },
        {
            "stl_name": "02_GA25_Rear_Motor_Clamp_Universal.stl",
            "display_name": "02_GA25_Rear_Motor_Clamp_Universal_Right",
            "pos_x": 135.0,
            "pos_y": 215.0,
            "walls": "4",
            "infill": "40%",
            "support": "0"
        }
    ]
    export_3mf_package(
        file2_path,
        "Plate K2 Hub Riser 2S2P Pack (Khung Don 2S2P + Tam Be V11 Hardened + 2x Nep Motor Sau Universal)",
        file2_items,
        settings
    )

    # ----------------------------------------------------
    # FILE 3: Bản Liền Khối Monolithic Riser Adapter
    # ----------------------------------------------------
    file3_path = os.path.join(OUT_3MF_DIR, "Plate_K2_Monolithic_Riser_Adapter.3mf")
    file3_items = [
        {
            "stl_name": "01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl",
            "display_name": "01D_K2_Control_Hub_Riser_Adapter_Monolithic_V60",
            "pos_x": 128.0,
            "pos_y": 128.0,
            "walls": "4",
            "infill": "25%",
            "support": "0"
        }
    ]
    export_3mf_package(
        file3_path,
        "Plate K2 Monolithic Riser Adapter (Ban Lien Khoi Riser Don + Be Hub K2 + Nep Motor Sau - In 1 Lan)",
        file3_items,
        settings
    )

    print("\n>>> All 3 requested Bambu Lab 3MF packages generated successfully!")

if __name__ == "__main__":
    main()
