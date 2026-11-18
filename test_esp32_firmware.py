import sys
import time
import os

try:
    import usb.core
    import usb.util
except ImportError:
    print("[ERROR] pyusb chua duoc cai dat!")
    sys.exit(1)

def run_test():
    dev = usb.core.find(idVendor=0x303a, idProduct=0x4001)
    if dev is None:
        dev = usb.core.find(idVendor=0x303a, idProduct=0x1001)
        if dev is None:
            print("[ERROR] Khong tim thay ESP32-S3 tren cong USB (303A:4001 hoac 303A:1001)!")
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

    # Drain buffer
    for _ in range(5):
        read_bytes(30)

    # Interrupt with Ctrl+C x2 and friendly REPL Ctrl+B
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

    print("[+] Da ket noi MicroPython Raw REPL tren ESP32-S3!")

    test_code = """
import sys, time
print("=== KIEM TRA MODULES FIRMWARE ===")
for mod in ["hcsr04", "laser_system", "maze_strategy"]:
    try:
        __import__(mod)
        print("Module", mod, ": OK")
    except Exception as e:
        print("Module", mod, ": ERROR", e)

print("\\n=== KHOI TAO VA DOC CAM BIEN ===")
try:
    import laser_system
    ls = laser_system.LaserSystem()
    print("LaserSystem initialized.")
    for i in range(5):
        time.sleep(0.1)
        cm = ls.read_all_cm()
        raw = ls.read_all(raw=True)
        print("Sample {}: Front={:.1f}cm, Left={:.1f}cm, Right={:.1f}cm | Raw_mm={}".format(i+1, cm[0], cm[1], cm[2], raw))
    print("=== DOC CAM BIEN HOAN TAT ===")
except Exception as e:
    import sys
    print("Loi doc cam bien:")
    sys.print_exception(e)
"""

    code_bytes = test_code.strip().encode("utf-8")
    for i in range(0, len(code_bytes), 64):
        dev.write(0x02, code_bytes[i:i + 64])
        time.sleep(0.005)

    # Execute Ctrl+D
    dev.write(0x02, b"\x04")

    # Read output
    full_output = b""
    start_t = time.time()
    while time.time() - start_t < 15.0:
        chunk = read_bytes(100)
        if chunk:
            sys.stdout.write(chunk.decode("utf-8", errors="replace"))
            sys.stdout.flush()
            full_output += chunk
            if b"=== DOC CAM BIEN HOAN TAT ===" in full_output or b"Traceback" in full_output:
                break
        else:
            time.sleep(0.05)

    # Exit Raw REPL
    try:
        dev.write(0x02, b"\x02")
    except Exception:
        pass

    return True

if __name__ == "__main__":
    run_test()
