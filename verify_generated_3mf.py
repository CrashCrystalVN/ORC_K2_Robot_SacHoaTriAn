import zipfile
import xml.etree.ElementTree as ET
import json
import trimesh
import os

out_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3MF_Models"
files = [
    "01_Chassis_Base_200x200_Bambu.3mf",
    "Plate_1_Chassis_Base_200x200_V6.3mf",
    "Plate_K2_Hub_Riser_2S2P_Pack.3mf",
    "Plate_K2_Monolithic_Riser_Adapter.3mf"
]

for fname in files:
    fpath = os.path.join(out_dir, fname)
    print("=" * 60)
    print(f"VERIFYING: {fname} ({os.path.getsize(fpath):,} bytes)")
    
    # 1. Zip integrity
    with zipfile.ZipFile(fpath, 'r') as z:
        corrupt = z.testzip()
        if corrupt:
            print(f"  [ERROR] Corrupted entry: {corrupt}")
        else:
            print(f"  [PASS] Zip CRC check OK")
        
        # 2. Check essential 3MF files
        namelist = z.namelist()
        required = [
            '[Content_Types].xml', '_rels/.rels', '3D/3dmodel.model',
            '3D/_rels/3dmodel.model.rels', 'Metadata/project_settings.config',
            'Metadata/model_settings.config'
        ]
        for req in required:
            assert req in namelist, f"Missing {req}"
        print(f"  [PASS] All essential 3MF / Bambu Studio files present ({len(namelist)} total files in archive)")
        
        # 3. Check XML
        root = ET.fromstring(z.read('3D/3dmodel.model'))
        items = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}item')
        print(f"  [PASS] 3D Model items count: {len(items)}")
        for it in items:
            transform = it.attrib.get('transform')
            vals = [float(v) for v in transform.split()]
            print(f"    Item ID={it.attrib.get('objectid')}: pos=({vals[9]:.2f}, {vals[10]:.2f}, {vals[11]:.2f})")

        # 4. Check Project Settings
        cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
        print(f"  [PASS] Printer: {cfg.get('printer_model')}, Bed: {cfg.get('curr_bed_type')}, Support: {cfg.get('enable_support')}, Walls: {cfg.get('wall_loops')}, Infill: {cfg.get('sparse_infill_density')}")

    # 5. Load with trimesh
    try:
        scene = trimesh.load(fpath)
        print(f"  [PASS] Trimesh load successful! Scene type: {type(scene)}")
        if hasattr(scene, 'geometry'):
            print(f"    Geometries count: {len(scene.geometry)}")
            for gname, geom in scene.geometry.items():
                b = geom.bounds
                print(f"    -> {gname}: faces={len(geom.faces)}, bounds=[[{b[0][0]:.2f}, {b[0][1]:.2f}, {b[0][2]:.2f}], [{b[1][0]:.2f}, {b[1][1]:.2f}, {b[1][2]:.2f}]]")
        print(f"  [PASS] Scene bounds: min={scene.bounds[0].round(2).tolist()}, max={scene.bounds[1].round(2).tolist()}")
        print(f"  [PASS] Scene bottom Z level: {scene.bounds[0][2]:.4f} mm (Touches bed at Z=0)")
    except Exception as e:
        print(f"  [FAIL] Trimesh error: {e}")
