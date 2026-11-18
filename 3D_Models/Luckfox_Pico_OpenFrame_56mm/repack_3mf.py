import zipfile
import trimesh
import os
import xml.etree.ElementTree as ET
import re

dir_path = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\Luckfox_Pico_OpenFrame_56mm"
mf_path = os.path.join(dir_path, "Luckfox_Pico_OpenFrame_56mm_RodMount_Bambu_A1.3mf")
mf_temp = os.path.join(dir_path, "Luckfox_Pico_OpenFrame_56mm_RodMount_Bambu_A1_updated.3mf")

# Mapping object file to STL file
object_stl_map = {
    "3D/Objects/object_1.model": ("01A_Luckfox_OpenFrame_UnderMount_56mm.stl", 1),
    "3D/Objects/object_2.model": ("02A_Rod_Clamp_Dual_Bar_56mm.stl", 2),
    "3D/Objects/object_3.model": ("03_Luckfox_PCB_Top_Retainer.stl", 3),
    "3D/Objects/object_4.model": ("04_VL53L5CX_V2_Sensor_Bracket.stl", 4),
    "3D/Objects/object_5.model": ("01B_Luckfox_OpenFrame_BackMount_56mm.stl", 5),
    "3D/Objects/object_6.model": ("02B_Rod_Clamp_BackMount_56mm.stl", 6),
}

# Part ID to face count mapping
face_counts = {}
center_offsets = {}

# 1. Load each STL and generate object_X.model XML content
generated_models = {}

with zipfile.ZipFile(mf_path, "r") as z_in:
    for obj_file, (stl_name, obj_id) in object_stl_map.items():
        stl_path = os.path.join(dir_path, stl_name)
        mesh = trimesh.load(stl_path)
        
        # Read original UUID
        orig_xml = z_in.read(obj_file).decode("utf-8")
        uuid_match = re.search(r'p:UUID="([^"]+)"', orig_xml)
        uuid_val = uuid_match.group(1) if uuid_match else "00000000-0000-0000-0000-000000000000"
        
        # Compute bounding box centers
        min_b, max_b = mesh.bounds[0], mesh.bounds[1]
        cx = (min_b[0] + max_b[0]) / 2.0
        cy = (min_b[1] + max_b[1]) / 2.0
        cz = (min_b[2] + max_b[2]) / 2.0
        
        center_offsets[obj_id] = (cx, cy, cz)
        face_counts[obj_id] = len(mesh.faces)
        
        # Centered vertices
        verts = mesh.vertices - [cx, cy, cz]
        faces = mesh.faces
        
        # Build 3MF model XML
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">',
            ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
            ' <resources>',
            f'  <object id="{obj_id}" p:UUID="{uuid_val}" type="model">',
            '   <mesh>',
            '    <vertices>'
        ]
        for v in verts:
            xml_lines.append(f'     <vertex x="{v[0]:.6f}" y="{v[1]:.6f}" z="{v[2]:.6f}"/>')
        xml_lines.append('    </vertices>')
        xml_lines.append('    <triangles>')
        for f in faces:
            xml_lines.append(f'     <triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>')
        xml_lines.append('    </triangles>')
        xml_lines.append('   </mesh>')
        xml_lines.append('  </object>')
        xml_lines.append(' </resources>')
        xml_lines.append('</model>')
        
        generated_models[obj_file] = '\n'.join(xml_lines).encode('utf-8')
        print(f"Generated {obj_file} from {stl_name}: {len(verts)} vertices, {len(faces)} faces, center Z={cz:.2f}mm")

    # 2. Update model_settings.config face counts and offsets
    settings_content = z_in.read("Metadata/model_settings.config").decode("utf-8")
    
    # We update face_count attributes and source_offsets
    root = ET.fromstring(settings_content)
    for obj in root.findall("object"):
        part = obj.find("part")
        if part is not None:
            part_id = int(part.get("id"))
            if part_id in face_counts:
                fc = str(face_counts[part_id])
                cx, cy, cz = center_offsets[part_id]
                
                # Update face_count metadata on object
                for m in obj.findall("metadata"):
                    if m.get("face_count") is not None:
                        m.set("face_count", fc)
                
                # Update mesh_stat
                mesh_stat = part.find("mesh_stat")
                if mesh_stat is not None:
                    mesh_stat.set("face_count", fc)
                
                # Update offsets
                for m in part.findall("metadata"):
                    key = m.get("key")
                    if key == "source_offset_x":
                        m.set("value", f"{cx:.4f}")
                    elif key == "source_offset_y":
                        m.set("value", f"{cy:.4f}")
                    elif key == "source_offset_z":
                        m.set("value", f"{cz:.4f}")
                        
    updated_settings = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    # 3. Create updated 3MF archive
    with zipfile.ZipFile(mf_temp, "w", compression=zipfile.ZIP_DEFLATED) as z_out:
        for item in z_in.infolist():
            if item.filename in generated_models:
                z_out.writestr(item, generated_models[item.filename])
            elif item.filename == "Metadata/model_settings.config":
                z_out.writestr(item, updated_settings)
            else:
                z_out.writestr(item, z_in.read(item.filename))

# Replace original 3MF with updated 3MF
os.replace(mf_temp, mf_path)
print("\nRepacked 3MF successfully replaced:", mf_path)
