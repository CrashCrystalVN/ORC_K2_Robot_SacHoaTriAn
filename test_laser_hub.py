import sys
import time
import usb.core
import usb.util

def test_laser():
    dev = usb.core.find(idVendor=0x303a, idProduct=0x4001)
    if dev is None:
        print("[ERROR] Khong tim thay ESP32-S3 (303A:4001)!")
        return

    try:
        dev.ctrl_transfer(0x21, 0x22, 0x01, 0, None)
    except Exception:
        pass

    def read_bytes(timeout_ms=50):
        try:
            return bytes(dev.read(0x82, 1024, timeout=timeout_ms))
        except Exception:
            return b""

    # Drain
    for _ in range(5):
        read_bytes(30)

    # Interrupt and raw repl
    dev.write(0x02, b"\r\x03\x03\r\x02")
    time.sleep(0.15)
    while read_bytes(30):
        pass

    dev.write(0x02, b"\r\x01")
    time.sleep(0.15)

    buf = b""
    start_t = time.time()
    while time.time() - start_t < 2.0:
        c = read_bytes(50)
        buf += c
        if b"raw REPL" in buf:
            break

    print("[+] Da vao Raw REPL!")

    code = """
import time
import laser_system
ls = laser_system.LaserSystem(continuous=True)
time.sleep_ms(300)
print("--- DOC 10 MAU LIEN TUC ---")
for i in range(10):
    f_raw = ls.read_front(raw=True)
    f_filt = ls.read_front(raw=False)
    l_filt = ls.read_left(raw=False)
    r_filt = ls.read_right(raw=False)
    print("Mau %2d: Front(raw=%4d, filt=%4d) | Left=%4d | Right=%4d" % (i+1, f_raw, f_filt, l_filt, r_filt))
    time.sleep_ms(150)
print("=== HOAN TAT TEST LASER ===")
"""
    code_bytes = code.strip().encode("utf-8")
    for i in range(0, len(code_bytes), 64):
        dev.write(0x02, code_bytes[i:i + 64])
        time.sleep(0.005)

    dev.write(0x02, b"\x04")

    # Read output
    full_out = b""
    start_t = time.time()
    while time.time() - start_t < 15.0:
        chunk = read_bytes(100)
        if chunk:
            sys.stdout.write(chunk.decode("utf-8", errors="replace"))
            sys.stdout.flush()
            full_out += chunk
            if b"=== HOAN TAT TEST LASER ===" in full_out:
                break
        else:
            time.sleep(0.05)

    dev.write(0x02, b"\x02") # return to friendly REPL

if __name__ == "__main__":
    test_laser()

