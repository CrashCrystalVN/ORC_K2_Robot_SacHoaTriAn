import os, subprocess, struct, collections
import trimesh

OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

def run_scad(scad_code, out_stl):
    scad_file = out_stl.replace(".stl", ".scad")
    with open(scad_file, "w", encoding="utf-8") as f:
        f.write(scad_code)
    res = subprocess.run([OPENSCAD, "-o", out_stl, scad_file], capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR running OpenSCAD on", scad_file)
        print(res.stderr)
        return False
    return True

def analyze_stl(stl_file):
    if not os.path.exists(stl_file):
        return {"error": "File not found"}
    mesh = trimesh.load(stl_file)
    # Check watertight, connected components, bounds
    shells = mesh.split()
    bounds = mesh.bounds
    return {
        "file": os.path.basename(stl_file),
        "is_watertight": mesh.is_watertight,
        "is_volume": mesh.is_volume,
        "volume": float(mesh.volume) if mesh.is_volume else 0.0,
        "num_shells": len(shells),
        "z_min": float(bounds[0][2]),
        "z_max": float(bounds[1][2]),
        "dx": float(bounds[1][0] - bounds[0][0]),
        "dy": float(bounds[1][1] - bounds[0][1]),
        "dz": float(bounds[1][2] - bounds[0][2]),
    }

if __name__ == "__main__":
    print("Helper ready")
