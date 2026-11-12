import os
import glob
import re

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

scad_files = glob.glob("3D_Models/*.scad")
for sf in scad_files:
    with open(sf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if "10" in content or "khung" in content.lower() or "base" in content.lower():
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if any(k in line.lower() for k in ["10 lỗ", "10 lo", "10-hole", "10 hole", "khung", "tháp nâng", "riser", "adapter"]):
                if any(k in line.lower() for k in ["10 lỗ", "10 lo", "10-hole", "10 hole", "10"]):
                    print(f"{sf}:{i+1} -> {line.strip()}")
