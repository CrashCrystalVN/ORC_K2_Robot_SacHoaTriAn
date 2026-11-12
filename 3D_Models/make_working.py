with open(r'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\_test_full_assembly_check.scad', 'r', encoding='utf-8') as f:
    text = f.read()

text_working = text.replace('MODE = "stowed";', 'MODE = "working";')

with open(r'C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\_test_working.scad', 'w', encoding='utf-8') as f:
    f.write(text_working)
print('Wrote _test_working.scad successfully')
