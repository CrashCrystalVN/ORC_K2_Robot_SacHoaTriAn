from PIL import Image
import os

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

for p in ["3D_Models/_user_img1.png", "3D_Models/_user_img2.png", "3D_Models/_diag_floor_holes_projected.png", "3D_Models/_diag_old_base_projected.png"]:
    if os.path.exists(p):
        im = Image.open(p)
        print(p, im.size, im.format)
