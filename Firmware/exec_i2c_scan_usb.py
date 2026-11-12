"""
=============================================================================
ORC K2 HUB (ESP32-S3) - USB CDC RAW REPL EXECUTION RUNNER
=============================================================================
"""

import sys
import time
import os

try:
    import usb.core
    import usb.util
except ImportError:
    print("[ERROR] pyusb chưa được cài đặt!")
    sys.exit(1)

def run_scanner_stream():
    dev = usb.core.find(idVendor=0x303a, idProduct=0x4001)
    if dev is None:
        dev = usb.core.find(idVendor=0x303a, idProduct=0x1001)
        if dev is None:
            print("[ERROR] Không tìm thấy ESP32-S3 trên cổng USB!")
            return False

    try:
        dev.ctrl_transfer(0x21, 0x22, 0x01, 0, None)
    except Exception:
        pass

    def read_bytes(timeout_ms=50):
        try:
            return bytes(dev.read(0x82, 1024, timeout=timeout_ms))
        except Exception:
            return b""

    # Drain any lingering bytes in buffer
    for _ in range(5):
        read_bytes(30)

    # Interrupt whatever is running with Ctrl+C x2 and switch to friendly REPL (Ctrl+B)
    dev.write(0x02, b"\r\x03\x03\r\x02")
    time.sleep(0.15)
    while read_bytes(30):
        pass

    # Enter Raw REPL (Ctrl+A)
    dev.write(0x02, b"\r\x01")
    time.sleep(0.15)

    buf = b""
    start_t = time.time()
    while time.time() - start_t < 2.0:
        c = read_bytes(50)
        buf += c
        if b"raw REPL; CTRL-B to exit" in buf:
            break

    if b"raw REPL" not in buf:
        dev.write(0x02, b"\x02\r\x03\x03\r\x01")
        time.sleep(0.2)
        buf = read_bytes(200)

    print("[+] Đã kết nối MicroPython Raw REPL trên ESP32-S3!")

    # Đọc mã lệnh scan_i2c_ports.py
    scan_script_path = os.path.join(os.path.dirname(__file__), "scan_i2c_ports.py")
    with open(scan_script_path, "r", encoding="utf-8") as f:
        code_str = f.read()

    print(f"[+] Đang nạp mã quét ({len(code_str)} bytes)...")
    code_bytes = code_str.encode("utf-8")
    for i in range(0, len(code_bytes), 64):
        dev.write(0x02, code_bytes[i:i + 64])
        time.sleep(0.005)

    print("[+] Kích hoạt thực thi (Ctrl+D)...")
    dev.write(0x02, b"\x04")

    # Đợi ACK xác nhận chạy (OK)
    ack = b""
    start_t = time.time()
    while time.time() - start_t < 3.0:
        c = read_bytes(50)
        ack += c
        if b"OK" in ack:
            break

    print("[+] Bắt đầu nhận luồng dữ liệu thời gian thực:\n" + "-" * 78)

    full_output = b""
    start_t = time.time()
    done_marker = "=== HOAN TAT TOAN BO QUET I2C ==="

    while time.time() - start_t < 60.0:
        chunk = read_bytes(100)
        if chunk:
            sys.stdout.write(chunk.decode("utf-8", errors="replace"))
            sys.stdout.flush()
            full_output += chunk
            if done_marker.encode("utf-8") in full_output:
                break
        else:
            time.sleep(0.05)

    print("-" * 78)
    print("[+] Hoàn tất quá trình quét I2C!")

    # Thoát Raw REPL về REPL bình thường (Ctrl+B)
    try:
        dev.write(0x02, b"\x02")
    except Exception:
        pass

    return True

if __name__ == "__main__":
    run_scanner_stream()
