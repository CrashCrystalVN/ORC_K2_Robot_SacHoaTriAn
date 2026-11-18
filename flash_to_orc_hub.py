"""
SCRIPT NẠP CODE TỰ ĐỘNG LÊN MẠCH OHSTEM ORC CONTROL HUB (ESP32-S3)
Tự động phát hiện cổng COM hoặc sử dụng COM19 mặc định.
"""

import sys
import os
import subprocess
import time
import serial.tools.list_ports
import littlefs

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_esp32_port(wait_seconds=30):
    start = time.time()
    first = True
    while time.time() - start < wait_seconds:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "BTHENUM" in p.hwid or "Bluetooth" in p.description:
                continue
            if "303A" in p.hwid or "USB JTAG" in p.description or "Espressif" in p.description or p.device == "COM19":
                return p.device
        if first:
            print("[*] Dang cho ket noi cong USB COM19 tu mach OhStem K2 Hub (ESP32-S3)...")
            first = False
        time.sleep(1.0)
    return "COM19"

def build_vfs_image(vfs_base_path, firmware_dir, output_vfs_path):
    print("[-] Đang nạp các file mã nguồn vào hệ thống tệp LittleFS...")
    with open(vfs_base_path, 'rb') as f:
        buf = bytearray(f.read())

    fs = littlefs.LittleFS(block_size=4096, block_count=512)
    fs.context.buffer = buf
    fs.mount()

    # Tự động nạp toàn bộ các file mã nguồn .py trong thư mục Firmware
    py_files = [f for f in os.listdir(firmware_dir) if f.endswith('.py')]
    priority_order = ['config.py', 'mecanum_kinematics.py', 'gamepad.py', 'drivebase.py', 'maze_strategy.py', 'main.py']
    files_to_update = [f for f in priority_order if f in py_files] + [f for f in sorted(py_files) if f not in priority_order]

    for fname in files_to_update:
        src_path = os.path.join(firmware_dir, fname)
        if not os.path.exists(src_path):
            continue
        with open(src_path, 'rb') as src:
            data = src.read()
        with fs.open(fname, 'wb') as dst:
            dst.write(data)
        print(f"    + Đã cập nhật vào VFS: {fname:<25s} ({len(data):6d} bytes)")

    fs.unmount()
    with open(output_vfs_path, 'wb') as f:
        f.write(fs.context.buffer)
    print(f"[OK] Da tao thanh cong file phan vung VFS LittleFS: {output_vfs_path}")

def flash_to_board(port, vfs_image_path):
    print(f"\n[-] Dang nap VFS image vao ESP32-S3 qua cong {port} o dia chi 0x200000...")
    cmd = [
        sys.executable, "-m", "esptool",
        "--port", port,
        "--baud", "921600",
        "write-flash", "0x200000", vfs_image_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("[LOI] Nap that bai:")
        print(res.stderr)
        return False
    print("[OK] Nap thanh cong 100% vao mach ORC Control Hub!")
    return True

def reset_board(port):
    print("[-] Dang khoi dong lai mach...")
    try:
        import esptool
        esp = esptool.cmds.detect_chip(port=port)
        esp.watchdog_reset()
        esp._port.close()
        print("[OK] Mach da duoc Watchdog Reset va khoi chay MicroPython thanh cong!")
        return
    except Exception as e:
        print("[*] Thu reset qua esptool run fallback:", e)
    cmd = [sys.executable, "-m", "esptool", "--port", port, "run"]
    subprocess.run(cmd, capture_output=True, text=True)
    print("[OK] Mach da duoc Reset va khoi chay code moi!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    firmware_dir = os.path.join(base_dir, "Firmware")
    vfs_base = os.path.join(base_dir, "vfs.bin")
    if not os.path.exists(vfs_base):
        vfs_base = os.path.join(base_dir, "vfs_ready_to_flash.bin")
        
    vfs_out = os.path.join(base_dir, "vfs_ready_to_flash.bin")
    
    port = None
    for arg in sys.argv[1:]:
        if arg.upper().startswith("COM"):
            port = arg.upper()
            break
    if not port and "--build-only" not in sys.argv:
        port = find_esp32_port()
    elif not port:
        port = "BUILD_ONLY"
    print(f"=== TIEN TRINH NAP CODE CHO ORC K2 (PORT: {port}) ===")
    
    build_vfs_image(vfs_base, firmware_dir, vfs_out)
    if "--build-only" in sys.argv:
        print("[OK] Che do --build-only: Da dong goi xong LittleFS VFS image. Khong goi esptool.")
        sys.exit(0)
    if flash_to_board(port, vfs_out):
        reset_board(port)
        print("\n>>> CHUC MUNG: CODE DA DUOC NAP TRUC TIEP VAO ORC CONTROL HUB! <<<")
