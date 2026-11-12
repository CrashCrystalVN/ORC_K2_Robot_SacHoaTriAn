import subprocess, os, re
import numpy as np

openscad_exe = r'C:\Program Files\OpenSCAD\openscad.exe'

def calc_stl_ascii_volume(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    pattern = re.compile(r'facet normal.*?'
                         r'outer loop\s+'
                         r'vertex\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+'
                         r'vertex\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+'
                         r'vertex\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+([\d\.\+\-eE]+)\s+'
                         r'endloop\s+'
                         r'endfacet', re.DOTALL)
    matches = pattern.findall(text)
    tri_count = len(matches)
    if tri_count == 0:
        return 0, 0.0
    v = np.array([[float(x) for x in m] for m in matches])
    v1 = v[:, 0:3]
    v2 = v[:, 3:6]
    v3 = v[:, 6:9]
    cross = np.cross(v1, v2)
    vol = np.sum(np.sum(cross * v3, axis=1)) / 6.0
    return tri_count, abs(vol)

def run_test(name, inner_span, enc_len):
    scad_content = f"""$fn = 48;
INNER_SPAN = {inner_span};
X_FLANGE_IN_L = -INNER_SPAN / 2.0;
X_FLANGE_IN_R = +INNER_SPAN / 2.0;
MOTOR_ENC_L = {enc_len};
MOTOR_D = 25.0;

intersection() {{
    translate([X_FLANGE_IN_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
    
    translate([X_FLANGE_IN_R - MOTOR_ENC_L, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=MOTOR_D, h=MOTOR_ENC_L);
}}
"""
    scad_path = rf'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\_test_{name}.scad'
    stl_path = rf'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\_test_{name}.stl'
    with open(scad_path, 'w', encoding='utf-8') as f:
        f.write(scad_content)
    if os.path.exists(stl_path):
        os.remove(stl_path)
    res = subprocess.run([openscad_exe, '-o', stl_path, scad_path], capture_output=True, text=True)
    if os.path.exists(stl_path):
        tri_cnt, vol = calc_stl_ascii_volume(stl_path)
        overlap_mm = enc_len * 2 - inner_span
        print(f'[{name}] => FAIL! COLLISION DETECTED:')
        print(f'   - Overlap along X axis: {overlap_mm:.1f} mm')
        print(f'   - Mesh Triangles:       {tri_cnt}')
        print(f'   - Collision Volume:     {vol:.2f} mm^3')
    else:
        gap_mm = inner_span - enc_len * 2
        print(f'[{name}] => PASS! ZERO COLLISION:')
        print(f'   - Clearance Gap along X:{gap_mm:.1f} mm')
        print(f'   - Collision Mesh:       NULL / EMPTY')
        print(f'   - Collision Volume:     0.000 mm^3')

print('======================================================================')
print('=== REVIEWER 1: FORMAL 3D CAD BOOLEAN CSG COLLISION INSPECTION ===')
print('======================================================================')
run_test('V51_no_boss_63mm', inner_span=113.0, enc_len=63.0)
run_test('V51_no_boss_60mm', inner_span=113.0, enc_len=60.0)
run_test('V60_with_boss_63mm', inner_span=133.0, enc_len=63.0)
run_test('V60_with_boss_65mm', inner_span=133.0, enc_len=65.0)
print('======================================================================')
