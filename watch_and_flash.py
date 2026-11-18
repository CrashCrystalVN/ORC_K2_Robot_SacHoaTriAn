import os
import sys
import time
import subprocess
import serial.tools.list_ports

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_target_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "BTHENUM" in p.hwid or "Bluetooth" in p.description or p.device in ["COM11", "COM12", "COM1"]:
            continue
        if "303A" in p.hwid or "USB JTAG" in p.description or "Espressif" in p.description or p.device == "COM19":
            return p.device
    return None

base_dir = os.path.dirname(os.path.abspath(__file__))
vfs_ready = os.path.join(base_dir, "vfs_ready_to_flash.bin")

if not os.path.exists(vfs_ready):
    print("[ERROR] Khong tim thay file vfs_ready_to_flash.bin!")
    sys.exit(1)

print("=" * 70)
print("TIEN TRINH TU DONG NAP FIRMWARE K2 CONTROL HUB (ESP32-S3)")
print("File partition LittleFS: vfs_ready_to_flash.bin (2,097,152 bytes)")
print("Huong dan kich hoat nap:")
print("  -> Nhan GIU nut BOOT tren mach K2")
print("  -> Bam nut RST (Reset) 1 lan roi tha nut BOOT")
print("  -> Mach se lap tuc chuyen vao che do ROM Bootloader (COM19)")
print("=" * 70)
print("[*] Dang lang nghe ket noi cong COM...")

timeout = 180 # Cho trong 3 phut
start = time.time()
dots = 0

while time.time() - start < timeout:
    port = find_target_port()
    if port:
        print(f"\n[+] DA PHAT HIEN K2 CONTROL HUB TAI CONG {port}!")
        time.sleep(0.8) # Cho cong on dinh
        
        cmd = [
            sys.executable, "-m", "esptool",
            "--port", port,
            "--baud", "921600",
            "write-flash", "0x200000", vfs_ready
        ]
        print(f"[-] Dang tien hanh nap Firmware LittleFS vao dia chi 0x200000 ({port})...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print(f"[OK] DA NAP THANH CONG 100% VAO MACH K2 QUA {port}!")
            # Reset board to start MicroPython
            print("[-] Dang khoi dong lai mach vao MicroPython...")
            subprocess.run([sys.executable, "-m", "esptool", "--port", port, "run"], capture_output=True)
            print("[OK] Mach da duoc Reset va dang khoi chay Firmware moi!")
            sys.exit(0)
        else:
            print("[LOI] esptool that bai:")
            print(res.stderr)
            sys.exit(1)
            
    dots += 1
    if dots % 10 == 0:
        elapsed = int(time.time() - start)
        print(f"[*] Dang cho (da troi qua {elapsed}s / {timeout}s)... Nhan BOOT + RST de nap.")
    time.sleep(1.0)

print("\n[HET GIO] Khong phat hien thay K2 Hub chuyen ve COM19 trong thoi gian cho.")
sys.exit(2)
