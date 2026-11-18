import os
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import scipy.spatial.distance

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
P_3MF = os.path.join(BASE_DIR, "3MF_Models", "Plate_Tower_2Part_Compact.3mf")

with zipfile.ZipFile(P_3MF, "r") as z:
    tree = ET.fromstring(z.read("3D/3dmodel.model"))
    ns = {
        "m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02",
        "p": "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"
    }
    
    resources = tree.find("m:resources", ns)
    objects = {}
    for obj in resources.findall("m:object", ns):
        oid = obj.attrib["id"]
        comp = obj.find("m:components/m:component", ns)
        target_path = comp.attrib["{" + ns["p"] + "}path"]
        target_oid = comp.attrib["objectid"]
        objects[oid] = (target_path, target_oid)
        
    mesh_data = {}
    for obj_file in [f for f in z.namelist() if f.startswith("3D/Objects/") and f.endswith(".model")]:
        sub_tree = ET.fromstring(z.read(obj_file))
        sub_res = sub_tree.find("m:resources", ns)
        sub_obj = sub_res.find("m:object", ns)
        verts = []
        for v in sub_obj.findall("m:mesh/m:vertices/m:vertex", ns):
            verts.append([float(v.attrib["x"]), float(v.attrib["y"]), float(v.attrib["z"])])
        verts = np.array(verts)
        mesh_data["/" + obj_file] = verts

    cfg_tree = ET.fromstring(z.read("Metadata/model_settings.config"))
    names = {}
    for obj in cfg_tree.findall("object"):
        oid = obj.attrib["id"]
        for m in obj.findall("metadata"):
            if m.attrib.get("key") == "name":
                names[oid] = m.attrib.get("value")

    build = tree.find("m:build", ns)
    instances = []
    for it in build.findall("m:item", ns):
        oid = it.attrib["objectid"]
        tr_str = it.attrib["transform"]
        tr = [float(x) for x in tr_str.split()]
        mat = np.array([
            [tr[0], tr[1], tr[2], tr[9]],
            [tr[3], tr[4], tr[5], tr[10]],
            [tr[6], tr[7], tr[8], tr[11]],
            [0, 0, 0, 1]
        ])
        sub_path, sub_oid = objects[oid]
        v_local = mesh_data[sub_path]
        v_homo = np.hstack([v_local, np.ones((len(v_local), 1))])
        v_world = (mat @ v_homo.T).T[:, :3]
        
        name = names.get(oid, f"Object_{oid}")
        instances.append({
            "id": oid,
            "name": name,
            "sub_path": sub_path,
            "verts": v_world,
            "bounds_min": v_world.min(axis=0),
            "bounds_max": v_world.max(axis=0),
            "center": 0.5 * (v_world.min(axis=0) + v_world.max(axis=0))
        })

print("=== 3MF INSTANCES AUDIT (Plate_Tower_2Part_Compact.3mf) ===")
for i, inst in enumerate(instances):
    bmin = inst["bounds_min"]
    bmax = inst["bounds_max"]
    dim = bmax - bmin
    print(f"Instance {i+1} [ID {inst['id']}]: {inst['name']}")
    print(f"  Bounding Box: X=[{bmin[0]:.2f}, {bmax[0]:.2f}] (width={dim[0]:.2f} mm)")
    print(f"                Y=[{bmin[1]:.2f}, {bmax[1]:.2f}] (length={dim[1]:.2f} mm)")
    print(f"                Z=[{bmin[2]:.4f}, {bmax[2]:.2f}] (height={dim[2]:.2f} mm)")
    print(f"  Bed Contact Z_min: {bmin[2]:.4f} mm")

print("\n=== PAIRWISE DISTANCES & GAPS ===")
inst1 = instances[0]
inst2 = instances[1]
gap_x = max(0, inst1["bounds_min"][0] - inst2["bounds_max"][0], inst2["bounds_min"][0] - inst1["bounds_max"][0])
gap_y = max(0, inst1["bounds_min"][1] - inst2["bounds_max"][1], inst2["bounds_min"][1] - inst1["bounds_max"][1])
bb_gap_2d = np.sqrt(gap_x**2 + gap_y**2) if (gap_x > 0 and gap_y > 0) else max(gap_x, gap_y)

pts1 = inst1["verts"][::5]
pts2 = inst2["verts"][::5]
dists = scipy.spatial.distance.cdist(pts1, pts2)
min_p2p = dists.min()

print(f"{inst1['name']} <-> {inst2['name']}:")
print(f"  Min 3D Surface Distance: {min_p2p:.2f} mm (Requirement: >= 15.0 mm -> {'PASS' if min_p2p >= 15.0 else 'FAIL'})")
print(f"  2D Bounding Box Clearance: {bb_gap_2d:.2f} mm (gap_x={gap_x:.2f}, gap_y={gap_y:.2f})")

print("\n=== BED MARGINS (256 x 256 mm) ===")
all_min = np.min([inst["bounds_min"] for inst in instances], axis=0)
all_max = np.max([inst["bounds_max"] for inst in instances], axis=0)
print(f"Total Plate Enclosure: X=[{all_min[0]:.2f}, {all_max[0]:.2f}], Y=[{all_min[1]:.2f}, {all_max[1]:.2f}], Z=[{all_min[2]:.4f}, {all_max[2]:.2f}]")
print(f"Margin to Bed Left (X=0): {all_min[0]:.2f} mm")
print(f"Margin to Bed Right (X=256): {256.0 - all_max[0]:.2f} mm")
print(f"Margin to Bed Front (Y=0): {all_min[1]:.2f} mm")
print(f"Margin to Bed Back (Y=256): {256.0 - all_max[1]:.2f} mm")
