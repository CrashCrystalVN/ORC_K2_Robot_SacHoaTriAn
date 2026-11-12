import zipfile
import xml.etree.ElementTree as ET
import glob
import os

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

for p3mf in glob.glob("3MF_Models/*.3mf"):
    with zipfile.ZipFile(p3mf, 'r') as z:
        print(f"\n=== 3MF FILE: {p3mf} ===")
        namelist = z.namelist()
        print("Files in 3MF:", [n for n in namelist if n.endswith('.model') or n.endswith('.config')])
        # Read 3D/3dmodel.model
        if "3D/3dmodel.model" in namelist:
            xml_data = z.read("3D/3dmodel.model")
            root = ET.fromstring(xml_data)
            # Find objects / metadata
            for item in root.iter():
                if "name" in item.attrib:
                    print("  Item name:", item.attrib["name"])
                if item.tag.endswith("mesh"):
                    # count vertices
                    v_count = len(list(item.find('{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertices') or []))
                    t_count = len(list(item.find('{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangles') or []))
                    print(f"  Mesh vertices: {v_count}, triangles: {t_count}")
