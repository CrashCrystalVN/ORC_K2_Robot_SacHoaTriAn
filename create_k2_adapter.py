"""
create_k2_adapter.py - Tao file 3D STL & 3MF cho He Khung & Tam San K2 Control Hub V10.0
(QUICK-SNAP RETAINING LATCHES & DUAL VL53L0X TOF LASER MAZE-SOLVER WINGS)
Tich hop ngam cai dan hoi snap-fit cho K2 Hub + 2 Cum ga Laser ToF VL53L0X do vach giai me cung +
Cantilever lui hau cach 2 Thap Nang 23mm, Zero va cham!
"""

import sys
import os
import subprocess

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    redesign_script = os.path.join(script_dir, "generate_redesigned_parts.py")
    if os.path.exists(redesign_script):
        print("-> Chay generate_redesigned_parts.py de xuat cac chi tiet K2 V10.0...")
        subprocess.run([sys.executable, redesign_script], check=True)
        # Chay tiep generate_bambu_3mf.py
        bambu_script = os.path.join(script_dir, "generate_bambu_3mf.py")
        subprocess.run([sys.executable, bambu_script], check=True)
    else:
        print("[LOI] Khong tim thay generate_redesigned_parts.py!")
