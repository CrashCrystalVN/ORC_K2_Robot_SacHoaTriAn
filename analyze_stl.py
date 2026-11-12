import re
from collections import defaultdict, deque

def parse_ascii_stl(filename):
    with open(filename, "r", errors="ignore") as f:
        content = f.read()
    facets = content.split("facet normal")
    triangles = []
    for facet in facets[1:]:
        verts = re.findall(r"vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)", facet)
        if len(verts) == 3:
            v1 = tuple(float(x) for x in verts[0])
            v2 = tuple(float(x) for x in verts[1])
            v3 = tuple(float(x) for x in verts[2])
            triangles.append((v1, v2, v3))
    return triangles

triangles = parse_ascii_stl("C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/test_combined_fix.stl")
def quant(v):
    return (round(v[0], 2), round(v[1], 2), round(v[2], 2))

adj = defaultdict(set)
vert_to_tri = defaultdict(list)
for idx, (v1, v2, v3) in enumerate(triangles):
    q1, q2, q3 = quant(v1), quant(v2), quant(v3)
    for q in (q1, q2, q3):
        for other_tri in vert_to_tri[q]:
            adj[idx].add(other_tri)
            adj[other_tri].add(idx)
        vert_to_tri[q].append(idx)

visited = set()
components = []
for idx in range(len(triangles)):
    if idx not in visited:
        comp = []
        queue = deque([idx])
        visited.add(idx)
        while queue:
            curr = queue.popleft()
            comp.append(curr)
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        components.append(comp)

print(f"Found {len(components)} connected components:")
for c_idx, comp in enumerate(components):
    xs, ys, zs = [], [], []
    for tri_idx in comp:
        for v in triangles[tri_idx]:
            xs.append(v[0])
            ys.append(v[1])
            zs.append(v[2])
    print(f"Component {c_idx+1}: {len(comp)} triangles, X=[{min(xs):.2f}, {max(xs):.2f}], Y=[{min(ys):.2f}, {max(ys):.2f}], Z=[{min(zs):.2f}, {max(zs):.2f}]")
