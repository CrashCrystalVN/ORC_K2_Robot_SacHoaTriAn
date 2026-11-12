import sys
import os
import time
import subprocess
import littlefs

base_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
vfs_dump = os.path.join(base_dir, "vfs_dump_current.bin")
vfs_scan = os.path.join(base_dir, "vfs_scan_i2c.bin")

# 1. Read current VFS
with open(vfs_dump, 'rb') as f:
    buf = bytearray(f.read())

fs = littlefs.LittleFS(block_size=4096, block_count=512)
fs.context.buffer = buf
fs.mount()

# Backup original main.py
with fs.open('main.py', 'rb') as f:
    orig_main = f.read()

with open(os.path.join(base_dir, "main_original_backup.py"), 'wb') as f:
    f.write(orig_main)

# Read scan_i2c_ports.py
scan_py_path = os.path.join(base_dir, "Firmware", "scan_i2c_ports.py")
with open(scan_py_path, 'r', encoding='utf-8') as f:
    scan_code = f.read()

# Create special runner main.py that redirects output to file scan_result.txt
runner_code = """
import sys
import time

log_file = open('scan_result.txt', 'w')

class Logger:
    def write(self, s):
        try:
            sys.__stdout__.write(s)
        except Exception:
            pass
        try:
            log_file.write(s)
            log_file.flush()
        except Exception:
            pass
    def flush(self):
        try:
            sys.__stdout__.flush()
        except Exception:
            pass
        try:
            log_file.flush()
        except Exception:
            pass

logger = Logger()
sys.stdout = logger

print("=== ESP32-S3 BOOTED: STARTING I2C SCAN ===")

try:
    import pins
    print("pins module attributes:", [x for x in dir(pins) if not x.startswith('_')])
    print("D3_PIN =", getattr(pins, 'D3_PIN', None))
    print("D4_PIN =", getattr(pins, 'D4_PIN', None))
    print("D5_PIN =", getattr(pins, 'D5_PIN', None))
    print("D6_PIN =", getattr(pins, 'D6_PIN', None))
    print("D7_PIN =", getattr(pins, 'D7_PIN', None))
    print("D8_PIN =", getattr(pins, 'D8_PIN', None))
except Exception as e:
    print("Error importing pins:", e)

try:
    import setting
    print("SCL_PIN =", getattr(setting, 'SCL_PIN', None))
    print("SDA_PIN =", getattr(setting, 'SDA_PIN', None))
except Exception as e:
    print("Error importing setting:", e)

""" + scan_code + """

try:
    print("\\n[RUNNING SCAN]...")
    res = scan_all_ports(verbose=True)
    print("SCAN_COMPLETED_SUCCESSFULLY")
except Exception as e:
    print("SCAN_FAILED_WITH_EXCEPTION:", e)

log_file.write("\\n=== SCAN FINISHED ===\\n")
log_file.close()

# Blink onboard LED or NeoPixel to indicate done
try:
    from yolo_uno import neopix, hex_to_rgb
    neopix.show(0, hex_to_rgb('#00ff00'))
except Exception:
    pass

while True:
    time.sleep(1)
"""

with fs.open('main.py', 'wb') as f:
    f.write(runner_code.encode('utf-8'))

fs.unmount()

with open(vfs_scan, 'wb') as f:
    f.write(fs.context.buffer)

print(f"[OK] Generated {vfs_scan}")

# 2. Flash to board at 0x200000
cmd_flash = [
    sys.executable, "-m", "esptool",
    "--port", "COM19",
    "--baud", "921600",
    "write-flash", "0x200000", vfs_scan
]
print("[-] Flashing scan VFS to COM19...")
res = subprocess.run(cmd_flash, capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Flash error:", res.stderr)
    sys.exit(1)

# 3. Reset board
print("[-] Resetting board...")
cmd_reset = [sys.executable, "-m", "esptool", "--port", "COM19", "run"]
res_rst = subprocess.run(cmd_reset, capture_output=True, text=True)
print(res_rst.stdout)

print("[-] Waiting 6 seconds for ESP32-S3 to scan and write scan_result.txt...")
time.sleep(6)

# 4. Dump back VFS to read scan_result.txt
print("[-] Reading back VFS from board...")
vfs_dump_after = os.path.join(base_dir, "vfs_dump_after_scan.bin")
cmd_dump = [
    sys.executable, "-m", "esptool",
    "--port", "COM19",
    "--baud", "921600",
    "read-flash", "0x200000", "0x200000", vfs_dump_after
]
res_dump = subprocess.run(cmd_dump, capture_output=True, text=True)
if res_dump.returncode != 0:
    print("Dump error:", res_dump.stderr)
    sys.exit(1)

# 5. Extract scan_result.txt
with open(vfs_dump_after, 'rb') as f:
    buf_after = bytearray(f.read())

fs_after = littlefs.LittleFS(block_size=4096, block_count=512)
fs_after.context.buffer = buf_after
fs_after.mount()

print("\nFiles in VFS after scan:")
for fn in fs_after.listdir('/'):
    print(" -", fn)

if 'scan_result.txt' in fs_after.listdir('/'):
    with fs_after.open('scan_result.txt', 'rb') as f:
        scan_content = f.read().decode('utf-8', errors='replace')
    print("\n" + "=" * 60)
    print(">>> NỘI DUNG SCAN_RESULT.TXT TỪ MẠCH THỰC TẾ <<<")
    print("=" * 60)
    print(scan_content)
    print("=" * 60)
    with open(os.path.join(base_dir, "scan_result_from_board.txt"), 'w', encoding='utf-8') as out_f:
        out_f.write(scan_content)
else:
    print("\n[!] Không tìm thấy file scan_result.txt trong VFS sau khi quét!")

# 6. Restore original main.py to board
print("\n[-] Restoring original main.py...")
with fs.open('main.py', 'wb') as f:
    f.write(orig_main)
try:
    fs.remove('scan_result.txt')
except Exception:
    pass
fs.unmount()

vfs_restored = os.path.join(base_dir, "vfs_restored.bin")
with open(vfs_restored, 'wb') as f:
    f.write(fs.context.buffer)

cmd_restore = [
    sys.executable, "-m", "esptool",
    "--port", "COM19",
    "--baud", "921600",
    "write-flash", "0x200000", vfs_restored
]
res_restore = subprocess.run(cmd_restore, capture_output=True, text=True)
print("[+] Original firmware restored:", res_restore.returncode == 0)

# Reset again to run original firmware
subprocess.run([sys.executable, "-m", "esptool", "--port", "COM19", "run"], capture_output=True)
print("[OK] Finished.")
