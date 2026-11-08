"""
=============================================================================
SCRIPT NẠP BẢN TEST PHẦN CỨNG TOÀN DIỆN CHO OHSTEM K2 CONTROL HUB (ESP32-S3)
=============================================================================
"""

import sys
import os
import subprocess
import time
import littlefs

try:
    import serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_esp32_port():
    if HAS_SERIAL:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # VID 303A: Espressif USB Serial/JTAG or CP210x/CH340
            if "303A" in p.hwid or "USB JTAG" in p.description or "Espressif" in p.description:
                return p.device
        for p in ports:
            if "COM" in p.device and p.device != "COM1":
                return p.device
    return "COM19"

def build_test_vfs_image(vfs_base_path, test_main_path, output_vfs_path):
    print("[-] Đang nạp mã nguồn test vào hệ thống tệp LittleFS...")
    with open(vfs_base_path, 'rb') as f:
        buf = bytearray(f.read())

    fs = littlefs.LittleFS(block_size=4096, block_count=512)
    fs.context.buffer = buf
    fs.mount()

    # Nạp nội dung file main_test.py thành main.py trong hệ thống LittleFS
    with open(test_main_path, 'rb') as src:
        data = src.read()
    with fs.open('main.py', 'wb') as dst:
        dst.write(data)
    print(f"    + Đã cập nhật main.py bằng bản TEST ({len(data)} bytes)")

    fs.unmount()
    with open(output_vfs_path, 'wb') as f:
        f.write(fs.context.buffer)
    print(f"[OK] Đã tạo thành công file phân vùng VFS Test: {output_vfs_path}")

def flash_to_board(port, vfs_image_path):
    print(f"\n[-] Đang nạp VFS Test vào ESP32-S3 qua cổng {port} ở địa chỉ 0x200000...")
    cmd = [
        sys.executable, "-m", "esptool",
        "--port", port,
        "--baud", "921600",
        "write-flash", "0x200000", vfs_image_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("[LỖI] Nạp thất bại:")
        print(res.stderr)
        return False
    print("[OK] Nạp thành công 100% bản TEST vào mạch OhStem K2 Control Hub!")
    return True

def reset_board(port):
    print("[-] Đang khởi động lại mạch...")
    cmd = [sys.executable, "-m", "esptool", "--port", port, "run"]
    subprocess.run(cmd, capture_output=True, text=True)
    print("[OK] Mạch đã được khởi động lại và bắt đầu chạy bài test!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_main = os.path.join(base_dir, "Firmware", "main_test.py")
    vfs_base = os.path.join(base_dir, "vfs.bin")
    if not os.path.exists(vfs_base):
        vfs_base = os.path.join(base_dir, "vfs_ready_to_flash.bin")
    vfs_out = os.path.join(base_dir, "vfs_test_ready.bin")

    port = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("COM") else find_esp32_port()
    print(f"=== TIẾN TRÌNH NẠP CODE TEST CHO K2 CONTROL HUB (CỔNG: {port}) ===")

    build_test_vfs_image(vfs_base, test_main, vfs_out)
    
    if "--build-only" in sys.argv:
        print("[OK] Đã đóng gói xong VFS Test. Bỏ qua bước nạp.")
        sys.exit(0)

    if flash_to_board(port, vfs_out):
        reset_board(port)
        print("\n>>> HOÀN TẤT: CODE TEST ĐÃ ĐƯỢC NẠP THÀNH CÔNG VÀO K2 HUB! <<<")
    else:
        print(f"\n[NHẮC NHỞ] Nếu cổng {port} không kết nối được, vui lòng kiểm tra:")
        print("  1. Cáp Type-C đã cắm chắc chắn vào cổng Type-C của mạch K2.")
        print("  2. Công tắc nguồn của K2 Control Hub đã bật (ON).")
        print("  3. Đóng Serial Monitor hoặc ứng dụng khác đang chiếm cổng COM.")

