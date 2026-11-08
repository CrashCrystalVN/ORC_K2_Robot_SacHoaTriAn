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
        if "303A" in p.hwid or "USB JTAG" in p.description or "Espressif" in p.description:
            return p.device
    for p in ports:
        if p.device == "COM19":
            return p.device
    return None

base_dir = os.path.dirname(os.path.abspath(__file__))
vfs_test = os.path.join(base_dir, "vfs_test_ready.bin")

print("[*] Đang lắng nghe cổng USB kết nối từ mạch OhStem K2 Control Hub...")
timeout = 60 # chờ trong 60 giây
start = time.time()

while time.time() - start < timeout:
    port = find_target_port()
    if port:
        print(f"\n[+] ĐÃ PHÁT HIỆN K2 CONTROL HUB TẠI CỔNG {port}!")
        time.sleep(1) # chờ ổn định
        
        cmd = [
            sys.executable, "-m", "esptool",
            "--port", port,
            "--baud", "921600",
            "write-flash", "0x200000", vfs_test
        ]
        print(f"[-] Đang tiến hành nạp code test vào {port}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print(f"[OK] ĐÃ NẠP THÀNH CÔNG VÀO MẠCH K2 QUA {port}!")
            # Reset board
            subprocess.run([sys.executable, "-m", "esptool", "--port", port, "run"], capture_output=True)
            print("[OK] Mạch đã khởi động lại và đang chạy code test!")
            sys.exit(0)
        else:
            print("[LỖI] esptool thất bại:")
            print(res.stderr)
            sys.exit(1)
            
    time.sleep(1.5)

print("[HẾT GIỜ] Không phát hiện thấy K2 Hub cắm vào trong 60s.")
sys.exit(2)

