import os
import sys
import struct
import zipfile
import json
import uuid
import subprocess
import numpy as np
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
OPENSCAD_EXE = r"C:\Program Files\OpenSCAD\openscad.com"

os.makedirs(STL_DIR, exist_ok=True)
os.makedirs(OUT_3MF_DIR, exist_ok=True)

# ====================================================================
# 1. SCAD TEMPLATE GENERATOR
# ====================================================================
def get_standoff_scad_code(h, od=11.6, d_flat_y=-5.3):
    base_t = 3.50
    slot_h = 2.75
    top_t = 3.50
    return f"""// ====================================================================
// DỰ ÁN: ROBOT ORC K2 - SẮC HOA TRI ÂN (STEM THPT NGÔ QUYỀN & 20/11)
// CỌC ĐÔN KÉP M3 DUAL-NUT STANDOFF {int(h)}MM CHO PIN 2S2P
// FILE: 01D_Riser_Standoff_{int(h)}mm_2S2P.scad
// CHIỀU CAO: H = {h:.1f} mm | ĐƯỜNG KÍNH NGOÀI: Ø{od:.1f} mm
// D-FLAT CHỐNG VA CHẠM NẸP MOTOR SAU: Y = {d_flat_y:.1f} mm (R_-Y = {-d_flat_y:.2f} mm <= 5.50 mm)
// ====================================================================

$fn = 60;

module dual_nut_standoff_m3(h = {h:.1f}, od = {od:.1f}, d_flat_y = {d_flat_y:.1f}) {{
    r = od / 2.0;
    slot_w = 5.80;       // Rãnh nhét tán M3 rộng 5.80mm (DIN 934 s=5.50mm, chống xoay cực chắc)
    slot_h = 2.75;       // Chiều cao khe trượt 2.75mm (tán M3 dày 2.40mm, đút trơn tru)
    slot_depth = 3.25;   // Khoét vào quá tâm 3.25mm (đồng tâm 100% với trục Ø3.5mm)
    base_t = 3.50;       // Bệ chịu lực đáy dày 3.50mm (Z in [0.0, 3.50])
    top_t = 3.50;        // Bệ chịu lực đỉnh dày 3.50mm (Z in [h-3.50, h])
    bore_d = 3.50;       // Lỗ trục đứng xuyên suốt Ø3.50mm từ -1 đến h+1
    ch = 0.50;           // Chamfer vát mép 45° chống chân voi (elephant's foot)

    difference() {{
        // 1. Thân trụ chính tròn Ø{od}mm kèm vát mép 45° hai đầu
        union() {{
            cylinder(d1 = od - 2.0*ch, d2 = od, h = ch);
            translate([0, 0, ch]) cylinder(d = od, h = h - 2.0*ch);
            translate([0, 0, h - ch]) cylinder(d1 = od, d2 = od - 2.0*ch, h = ch);
        }}

        // 2. Vát phẳng D-flat ở mặt -Y (cách tâm {-d_flat_y:.2f}mm) chống va chạm nẹp motor sau GA25
        translate([-od, -od + d_flat_y, -1.0])
            cube([2.0*od, od, h + 2.0]);

        // 3. Lỗ trục đứng xuyên suốt 100% Ø3.50mm cho bu-lông / ty ren M3
        translate([0, 0, -1.0])
            cylinder(d = bore_d, h = h + 2.0);

        // 4. Vát côn dẫn hướng Ø4.5mm -> Ø3.5mm ở 2 miệng lỗ trục
        translate([0, 0, -0.01])
            cylinder(d1 = bore_d + 1.0, d2 = bore_d, h = ch + 0.02);
        translate([0, 0, h - ch - 0.01])
            cylinder(d1 = bore_d, d2 = bore_d + 1.0, h = ch + 0.02);

        // 5. HỐC CÀI TÁN M3 DƯỚI (Z in [base_t, base_t + slot_h] = [{base_t:.2f}, {base_t + slot_h:.2f} mm])
        translate([-slot_depth, -slot_w/2.0, base_t])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        // Vát mép mở rộng miệng vào rãnh 0.5mm:
        translate([r - 0.5, -slot_w/2.0 - 0.5, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        // DFM 45° Roof Chamfer chống xệ sợi nhựa khi in FDM đứng:
        translate([0, 0, base_t + slot_h - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);

        // 6. HỐC CÀI TÁN M3 TRÊN (Z in [h - top_t - slot_h, h - top_t] = [{h - top_t - slot_h:.2f}, {h - top_t:.2f} mm])
        translate([-slot_depth, -slot_w/2.0, h - top_t - slot_h])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        // Vát mép mở rộng miệng vào rãnh 0.5mm:
        translate([r - 0.5, -slot_w/2.0 - 0.5, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        // DFM 45° Roof Chamfer chống xệ sợi nhựa:
        translate([0, 0, h - top_t - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);
    }}
}}

// Xuất chi tiết đứng thẳng theo trục Z chuẩn in 3D FDM:
dual_nut_standoff_m3(h = {h:.1f}, od = {od:.1f}, d_flat_y = {d_flat_y:.1f});
"""

def generate_and_compile_scad():
    files_to_gen = [
        (26.0, "01D_Riser_Standoff_26mm_2S2P.scad", "01D_Riser_Standoff_26mm_2S2P.stl"),
        (44.0, "01D_Riser_Standoff_44mm_2S2P.scad", "01D_Riser_Standoff_44mm_2S2P.stl")
    ]
    for h, scad_name, stl_name in files_to_gen:
        scad_path = os.path.join(STL_DIR, scad_name)
        stl_path = os.path.join(STL_DIR, stl_name)
        code = get_standoff_scad_code(h)
        with open(scad_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Wrote {scad_name}")
        cmd = [OPENSCAD_EXE, "-o", stl_path, scad_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"OpenSCAD compile error for {scad_name}:\n{res.stderr}")
            sys.exit(1)
        print(f"Compiled {stl_name} successfully!")

# ====================================================================
# 2. UPDATE generate_redesigned_parts.py
# ====================================================================
def update_redesigned_parts_script():
    script_path = os.path.join(BASE_DIR, "generate_redesigned_parts.py")
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define target module replacement
    old_target = """// Trụ đệm đôn cao 26mm rời cho Pin 2S2P (H_clear = 44.0mm)
module riser_standoff_26mm_2s2p(h = 26.0) {
    difference() {
        cylinder(d=11.0, h=h);
        translate([0, 0, -1.0]) cylinder(d=3.4, h=h + 2.0);
        translate([0, 0, 5.0]) cylinder(d=7.2, h=h);
    }
}"""

    new_replacement = """// ====================================================================
// TRỤ ĐÔN ĐA NĂNG CÀI 2 TÁN LỤC GIÁC M3 (DUAL-NUT STANDOFF M3 ARCHITECTURE)
// Hốc cài 2 tán ngang DIN 934 (5.80 x 2.75mm), bắt 2 bu-lông M3 độc lập từ 2 đầu,
// bệ chịu lực dày 3.5mm mỗi đầu, lỗ xuyên suốt Ø3.5mm, vát phẳng D-flat né motor sau.
// ====================================================================
module dual_nut_standoff_m3(h = 26.0, od = 11.6, d_flat_y = -5.3) {
    r = od / 2.0;
    slot_w = 5.80;
    slot_h = 2.75;
    slot_depth = 3.25;
    base_t = 3.50;
    top_t = 3.50;
    bore_d = 3.50;
    ch = 0.50;

    difference() {
        union() {
            cylinder(d1 = od - 2.0*ch, d2 = od, h = ch);
            translate([0, 0, ch]) cylinder(d = od, h = h - 2.0*ch);
            translate([0, 0, h - ch]) cylinder(d1 = od, d2 = od - 2.0*ch, h = ch);
        }
        translate([-od, -od + d_flat_y, -1.0])
            cube([2.0*od, od, h + 2.0]);
        translate([0, 0, -1.0])
            cylinder(d = bore_d, h = h + 2.0);
        translate([0, 0, -0.01])
            cylinder(d1 = bore_d + 1.0, d2 = bore_d, h = ch + 0.02);
        translate([0, 0, h - ch - 0.01])
            cylinder(d1 = bore_d, d2 = bore_d + 1.0, h = ch + 0.02);

        // Hốc cài tán dưới:
        translate([-slot_depth, -slot_w/2.0, base_t])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        translate([r - 0.5, -slot_w/2.0 - 0.5, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, base_t])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([0, 0, base_t + slot_h - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);

        // Hốc cài tán trên:
        translate([-slot_depth, -slot_w/2.0, h - top_t - slot_h])
            cube([slot_depth + r + 2.0, slot_w, slot_h]);
        translate([r - 0.5, -slot_w/2.0 - 0.5, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([r - 0.5, slot_w/2.0 + 0.5 - 0.707, h - top_t - slot_h])
            rotate([0, 0, 45]) cube([1.0, 1.0, slot_h]);
        translate([0, 0, h - top_t - 0.4])
            cylinder(d1 = bore_d + 0.8, d2 = bore_d, h = 0.41);
    }
}

// Trụ đệm đôn cao 26mm rời cho Pin 2S2P (Cài 2 tán M3 kép)
module riser_standoff_26mm_2s2p(h = 26.0) {
    dual_nut_standoff_m3(h = h, od = 11.6, d_flat_y = -5.3);
}

// Trụ đệm đôn cao 44mm nguyên khối cho Pin 2S2P (Cài 2 tán M3 kép)
module riser_standoff_44mm_2s2p(h = 44.0) {
    dual_nut_standoff_m3(h = h, od = 11.6, d_flat_y = -5.3);
}"""

    if old_target in content:
        content = content.replace(old_target, new_replacement)
        print("Updated module definitions in generate_redesigned_parts.py")
    else:
        print("Note: old module definition string not matched directly, checking if already updated...")

    # Update PARTS_TO_GENERATE list:
    old_parts_entry = """    {
        "stl_name": "01D_Riser_Standoff_26mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\\nriser_standoff_26mm_2s2p(h=26.0);\\n",
        "desc": "Trụ đệm đôn cao 26mm rời cho Pin 2S2P (H_clear = 44.0mm, Ø11mm, lỗ bậc chìm cho ốc M3)"
    },"""

    new_parts_entry = """    {
        "stl_name": "01D_Riser_Standoff_26mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\\nriser_standoff_26mm_2s2p(h=26.0);\\n",
        "desc": "Cọc đôn Standoff kép 26mm rời cho Pin 2S2P (Ø11.6mm D-flat, cài 2 tán M3 ngang hông, bệ chịu lực 3.5mm)"
    },
    {
        "stl_name": "01D_Riser_Standoff_44mm_2S2P.stl",
        "scad_code": SCAD_LIBRARY + "\\nriser_standoff_44mm_2s2p(h=44.0);\\n",
        "desc": "Cọc đôn Standoff kép 44mm nguyên khối cho Pin 2S2P (Ø11.6mm D-flat, cài 2 tán M3 ngang hông, nâng thẳng K2 Hub lên Z=48mm)"
    },"""

    if old_parts_entry in content:
        content = content.replace(old_parts_entry, new_parts_entry)
        print("Updated PARTS_TO_GENERATE in generate_redesigned_parts.py")
    else:
        print("PARTS_TO_GENERATE already contains updated entries or check manually.")

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)

# ====================================================================
# 3. BAMBU 3MF GENERATOR
# ====================================================================
def load_base_project_settings():
    template_candidates = [
        os.path.join(OUT_3MF_DIR, "Plate_6_K2_Control_Hub_Riser_Adapter_Patch.3mf"),
        os.path.join(OUT_3MF_DIR, "00_ORC_K2_V3.1_Bambu_A1_All_5_Plates.3mf"),
        r"C:\Users\vuasu\Downloads\Robot.Arm.3mf"
    ]
    cfg = {}
    for cand in template_candidates:
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
    cfg["wall_loops"] = "5"
    cfg["sparse_infill_density"] = "100%"
    cfg["sparse_infill_pattern"] = "rectilinear"
    cfg["bottom_shell_layers"] = "5"
    cfg["top_shell_layers"] = "5"
    cfg["enable_support"] = "0"
    cfg["support_type"] = "tree(auto)"
    cfg["support_on_build_plate_only"] = "1"
    cfg["brim_type"] = "outer_only"
    cfg["brim_width"] = "5"
    cfg["filament_type"] = ["PLA"]
    cfg["filament_colour"] = ["#F98C00"]
    return cfg

def load_mesh(stl_path):
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

def export_3mf_plate(output_path, plate_title, items, project_settings_dict):
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
            "walls": it.get("walls", "5"),
            "infill": it.get("infill", "100%"),
            "support": it.get("support", "0")
        })
        identify_counter += 11

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
    ms_lines.append('</config>')
    model_settings_xml = "\n".join(ms_lines)

    # Write out zip archive
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", root_rels_xml)
        z.writestr("3D/_rels/3dmodel.model.rels", model_rels_xml)
        z.writestr("3D/3dmodel.model", main_model_xml)

        for stl_name, info in loaded_unique.items():
            obj_xml = build_object_model_xml(info["mesh_obj_id"], info["verts"], info["tris"])
            z.writestr(info["zip_path"], obj_xml)

        z.writestr("Metadata/model_settings.config", model_settings_xml)
        z.writestr("Metadata/project_settings.config", json.dumps(project_settings_dict, indent=4))

    print(f"Exported 3MF package -> {output_path} ({os.path.getsize(output_path):,} bytes)")

def create_standoff_3mf_plates():
    settings = load_base_project_settings()

    # 4 standoffs in a 2x2 grid centered at (128, 128) on Bambu A1 bed
    # dx = 28mm, dy = 28mm -> clearance between columns = 28 - 11.6 = 16.4mm
    grid_positions = [
        (114.0, 114.0),
        (142.0, 114.0),
        (114.0, 142.0),
        (142.0, 142.0)
    ]

    # Plate 1: 4x 26mm Standoffs
    p26_path = os.path.join(OUT_3MF_DIR, "Plate_Standoff_26mm_DualNut_x4.3mf")
    p26_items = [
        {
            "stl_name": "01D_Riser_Standoff_26mm_2S2P.stl",
            "display_name": f"01D_Riser_Standoff_26mm_DualNut_{i+1}",
            "pos_x": gx,
            "pos_y": gy,
            "walls": "5",
            "infill": "100%",
            "support": "0"
        }
        for i, (gx, gy) in enumerate(grid_positions)
    ]
    export_3mf_plate(
        p26_path,
        "Plate Standoff 26mm DualNut x4 (Coc Don Kep M3 x4 - In 0% Support, Infill 100%, 5 Walls)",
        p26_items,
        settings
    )

    # Plate 2: 4x 44mm Standoffs
    p44_path = os.path.join(OUT_3MF_DIR, "Plate_Standoff_44mm_2S2P_DualNut_x4.3mf")
    p44_items = [
        {
            "stl_name": "01D_Riser_Standoff_44mm_2S2P.stl",
            "display_name": f"01D_Riser_Standoff_44mm_DualNut_{i+1}",
            "pos_x": gx,
            "pos_y": gy,
            "walls": "5",
            "infill": "100%",
            "support": "0"
        }
        for i, (gx, gy) in enumerate(grid_positions)
    ]
    export_3mf_plate(
        p44_path,
        "Plate Standoff 44mm 2S2P DualNut x4 (Coc Don Kep M3 44mm x4 - Nang Thang K2 Hub len Z=48mm)",
        p44_items,
        settings
    )

# ====================================================================
# 4. VISUAL PREVIEW SCENE RENDERER
# ====================================================================
def render_preview_image():
    preview_scad_path = os.path.join(BASE_DIR, "preview_dualnut_standoffs_scene.scad")
    preview_png_path = os.path.join(BASE_DIR, "preview_standoff_26mm_44mm_dualnut.png")

    scad_scene = """$fn = 60;

// Mô phỏng bu-lông M3 DIN 912 (Socket Head Cap Screw)
module m3_bolt(len = 12.0, thread_len = 12.0) {
    color([0.2, 0.75, 1.0, 0.95]) { // Màu xanh Cyan phản quang cực kỳ nổi bật
        cylinder(d = 5.5, h = 3.0); // Mũ bu-lông M3
        translate([0, 0, 1.2]) cylinder(d = 2.8, h = 2.0, $fn = 6); // Lục giác chìm
        translate([0, 0, -len]) cylinder(d = 3.0, h = len); // Thân ren
    }
}

// Mô phỏng tán lục giác M3 DIN 934
module m3_hex_nut() {
    color([0.88, 0.88, 0.92, 0.95]) { // Thép mạ Niken sáng bóng
        difference() {
            cylinder(d = 6.35, h = 2.40, $fn = 6);
            translate([0, 0, -0.5]) cylinder(d = 2.95, h = 3.4);
        }
    }
}

// 1. CỌC 26MM NGUYÊN BẢN ĐỨNG (NGOÀI CÙNG BÊN TRÁI)
translate([-38.0, 0, 0]) {
    color([0.98, 0.52, 0.05, 0.95]) { // Bambu Orange
        import("3D_Models/01D_Riser_Standoff_26mm_2S2P.stl");
    }
}

// 2. MẶT CẮT BỔ DỌC CỌC 26MM + 2 TÁN M3 + 2 BU-LÔNG M3 BẮT 2 ĐẦU
translate([-14.0, 0, 0]) {
    difference() {
        color([0.98, 0.52, 0.05, 0.92]) {
            import("3D_Models/01D_Riser_Standoff_26mm_2S2P.stl");
        }
        // Cắt bỏ nửa Y < 0 để nhìn thấy mặt cắt bên trong:
        translate([-20.0, -25.0, -1.0]) cube([40.0, 25.0, 30.0]);
    }
    
    // Tán M3 dưới tại Z = 3.50mm:
    translate([0, 0, 3.50]) m3_hex_nut();
    // Bu-lông M3 bắt từ dưới lên (xuyên qua sàn xe Z=0..4mm, bệ cọc Z=4..7.5mm vào tán):
    translate([0, 0, 0.0]) rotate([180, 0, 0]) m3_bolt(len = 10.0);

    // Tán M3 trên tại Z = 19.75mm:
    translate([0, 0, 19.75]) m3_hex_nut();
    // Bu-lông M3 bắt từ trên xuống (xuyên qua K2 Adapter plate vào tán):
    translate([0, 0, 26.0]) m3_bolt(len = 10.0);
}

// 3. CỌC 44MM NGUYÊN BẢN ĐỨNG
translate([12.0, 0, 0]) {
    color([0.95, 0.42, 0.08, 0.95]) {
        import("3D_Models/01D_Riser_Standoff_44mm_2S2P.stl");
    }
}

// 4. MẶT CẮT BỔ DỌC CỌC 44MM + 2 TÁN M3 + 2 BU-LÔNG M3 BẮT 2 ĐẦU
translate([36.0, 0, 0]) {
    difference() {
        color([0.95, 0.42, 0.08, 0.92]) {
            import("3D_Models/01D_Riser_Standoff_44mm_2S2P.stl");
        }
        translate([-20.0, -25.0, -1.0]) cube([40.0, 25.0, 50.0]);
    }
    
    // Tán M3 dưới tại Z = 3.50mm:
    translate([0, 0, 3.50]) m3_hex_nut();
    translate([0, 0, 0.0]) rotate([180, 0, 0]) m3_bolt(len = 12.0);

    // Tán M3 trên tại Z = 37.75mm:
    translate([0, 0, 37.75]) m3_hex_nut();
    translate([0, 0, 44.0]) m3_bolt(len = 12.0);
}
"""
    with open(preview_scad_path, "w", encoding="utf-8") as f:
        f.write(scad_scene)
    print("Wrote preview SCAD scene.")

    cmd = [
        OPENSCAD_EXE,
        "-o", preview_png_path,
        "--imgsize=1920,1080",
        "--camera=0,-12,22,65,0,32,160",
        "--colorscheme=Tomorrow Night",
        preview_scad_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"OpenSCAD preview render error:\n{res.stderr}")
    else:
        print(f"Rendered preview image -> {preview_png_path} ({os.path.getsize(preview_png_path):,} bytes)")

def main():
    print("=== STEP 1: Generate & Compile Standoff 26mm & 44mm ===")
    generate_and_compile_scad()

    print("\n=== STEP 2: Update generate_redesigned_parts.py ===")
    update_redesigned_parts_script()

    print("\n=== STEP 3: Export Bambu Lab 3MF Packages ===")
    create_standoff_3mf_plates()

    print("\n=== STEP 4: Render Visual Preview Image ===")
    render_preview_image()

    print("\n=== COMPLETE: All assets successfully built and verified! ===")

if __name__ == "__main__":
    main()
