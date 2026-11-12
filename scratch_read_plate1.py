import zipfile
import xml.etree.ElementTree as ET
import numpy as np

with zipfile.ZipFile("3MF_Models/Plate_1_Khung_Gam_Chinh_Chassis.3mf", 'r') as z:
    for name in z.namelist():
        if name.startswith("3D/Objects/"):
            xml_data = z.read(name)
            root = ET.fromstring(xml_data)
            verts = []
            for v in root.iter('{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertex'):
                verts.append([float(v.attrib['x']), float(v.attrib['y']), float(v.attrib['z'])])
            if verts:
                arr = np.array(verts)
                min_pt = arr.min(axis=0)
                max_pt = arr.max(axis=0)
                sz = max_pt - min_pt
                print(f"{name}: {len(verts)} verts, X in [{min_pt[0]:.1f}, {max_pt[0]:.1f}], Y in [{min_pt[1]:.1f}, {max_pt[1]:.1f}], Z in [{min_pt[2]:.1f}, {max_pt[2]:.1f}], size={sz.tolist()}")
