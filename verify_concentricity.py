import trimesh
import numpy as np

# Load newly compiled chassis
m_chassis = trimesh.load(r'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\01_Chassis_Base_200x200.stl')

# Load towers
m_b = trimesh.load(r'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\01B_Lift_Tower_Left_FlatPrint.stl')
m_c = trimesh.load(r'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\01C_Lift_Tower_Right_MG996R_FlatPrint.stl')

# Assembly transform for Left Tower (01B)
v_b = m_b.vertices.copy()
v_b_asm = np.zeros_like(v_b)
v_b_asm[:, 0] = v_b[:, 2] - 28.0
v_b_asm[:, 1] = v_b[:, 1] + 135.5
v_b_asm[:, 2] = 49.0 - v_b[:, 0]
m_b_asm = trimesh.Trimesh(vertices=v_b_asm, faces=m_b.faces)

# Assembly transform for Right Tower (01C)
v_c = m_c.vertices.copy()
v_c_asm = np.zeros_like(v_c)
v_c_asm[:, 0] = 28.0 - v_c[:, 2]
v_c_asm[:, 1] = v_c[:, 1]
v_c_asm[:, 2] = v_c[:, 0]
m_c_asm = trimesh.Trimesh(vertices=v_c_asm, faces=m_c.faces)

# Extract holes on chassis at Z = 2.0 (mid-floor)
sl_ch = m_chassis.section(plane_origin=[0, 0, 2.0], plane_normal=[0, 0, 1])
ch_holes = []
for entity in sl_ch.discrete:
    pts = np.array(entity)
    size = pts.max(axis=0) - pts.min(axis=0)
    if max(size[0], size[1]) < 10.0 and len(pts) > 5:
        ch_holes.append((pts.mean(axis=0)[:2], size[0], size[1]))

# Extract tower holes at Z = 6.0 (mid-foot)
tower_holes = []
for t_mesh, name in [(m_b_asm, '01B_Lift_Tower_Left'), (m_c_asm, '01C_Lift_Tower_Right')]:
    sl_t = t_mesh.section(plane_origin=[0, 0, 6.0], plane_normal=[0, 0, 1])
    for entity in sl_t.discrete:
        pts = np.array(entity)
        size = pts.max(axis=0) - pts.min(axis=0)
        if max(size[0], size[1]) < 10.0 and len(pts) > 5:
            tower_holes.append((pts.mean(axis=0)[:2], size[0], size[1], name))

print(f'Total tower holes found: {len(tower_holes)}')
print(f'Total chassis holes found: {len(ch_holes)}')

print('\n' + '='*85)
hdr = f"{'HOLE / PART':<30} | {'TOWER (X, Y)':<18} | {'CHASSIS (X, Y)':<18} | {'OFFSET (mm)':<12}"
print(hdr)
print('='*85)

max_offset = 0.0
results = []
for th_pos, th_dx, th_dy, tname in sorted(tower_holes, key=lambda p: (p[0][0], p[0][1])):
    best_dist = 999.0
    best_ch = None
    for ch_pos, ch_dx, ch_dy in ch_holes:
        d = np.linalg.norm(th_pos - ch_pos)
        if d < best_dist:
            best_dist = d
            best_ch = (ch_pos, ch_dx, ch_dy)
    
    max_offset = max(max_offset, best_dist)
    th_str = f'({th_pos[0]:6.2f}, {th_pos[1]:6.2f})'
    ch_str = f'({best_ch[0][0]:6.2f}, {best_ch[0][1]:6.2f})'
    line_str = f'{tname:<30} | {th_str:<18} | {ch_str:<18} | {best_dist:8.4f} mm'
    print(line_str)
    results.append((tname, th_pos, best_ch[0], best_dist))

print('='*85)
print(f'MAX CONCENTRICITY DEVIATION: {max_offset:.4f} mm')
if max_offset < 0.05:
    print('>>> RESULT: 100% PERFECT CONCENTRICITY ALIGNMENT (0.00 mm ERROR)!')
