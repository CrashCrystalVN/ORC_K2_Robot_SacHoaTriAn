"""
create_k2_adapter.py - Tao file 3D STL & 3MF cho He Khung & Tam San K2 Control Hub V9.0
(CANTILEVER REAR-SHIFT & CAPTIVE BLIND-FLOOR NUT ARCHITECTURE - ZERO COLLISION WITH LIFT TOWERS & GRIPPER)
Dung de lap truc tiep vao khung gam ORC-X1 PRO da in san (co lap san 2 Thap Nang & Cum Gap Tru + Servo S1)
ma khong can in lai chassis!
"""

import sys
import os
import subprocess

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    redesign_script = os.path.join(script_dir, "generate_redesigned_parts.py")
    if os.path.exists(redesign_script):
        print("-> Chay generate_redesigned_parts.py de xuat cac chi tiet K2 V9.0...")
        subprocess.run([sys.executable, redesign_script], check=True)
        # Chay tiep generate_bambu_3mf.py
        bambu_script = os.path.join(script_dir, "generate_bambu_3mf.py")
        subprocess.run([sys.executable, bambu_script], check=True)
    else:
        print("[LOI] Khong tim thay generate_redesigned_parts.py!")
