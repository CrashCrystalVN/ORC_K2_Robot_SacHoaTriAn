"""
=============================================================================
ORC K2 CONTROL HUB (ESP32-S3) - FULL COMPREHENSIVE I2C SCANNER
=============================================================================
Quét toàn diện tất cả các cổng Grove Digital, Grove Analog và I2C Onboard:
- Cặp 1: D3 - D4 (GPIO 6, 7) cả 2 chiều thuận & đảo, tần số 100kHz & 50kHz
- Cặp 2: D5 - D6 (GPIO 8, 9) cả 2 chiều thuận & đảo, tần số 100kHz & 50kHz
- Cặp 3: D7 - D8 (GPIO 10, 17) cả 2 chiều thuận & đảo, tần số 100kHz & 50kHz
- Cổng I2C Onboard: SCL (GPIO 12), SDA (GPIO 11) cả 2 chiều, 100kHz & 50kHz
- Cặp Mở rộng Grove Analog: A0 - A1 (GPIO 1, 2) và A2 - A3 (GPIO 3, 4)
=============================================================================
"""

import time
from machine import Pin, SoftI2C

KNOWN_DEVICES = {
    0x20: "PCF8574 (Cảm biến dò Line / Mở rộng IO 8-bit - Addr 0x20)",
    0x21: "PCF8574 (Cảm biến dò Line - Addr 0x21)",
    0x22: "PCF8574 (Cảm biến dò Line - Addr 0x22)",
    0x23: "PCF8574 (Cảm biến dò Line mặc định OhStem - Addr 0x23)",
    0x24: "PCF8574 (Cảm biến dò Line - Addr 0x24)",
    0x25: "PCF8574 (Cảm biến dò Line - Addr 0x25)",
    0x26: "PCF8574 (Cảm biến dò Line - Addr 0x26)",
    0x27: "PCF8574 / LCD1602 I2C Backlight Module",
    0x29: "VL53L0X / VL53L1X ToF Laser Distance Sensor (Cảm biến khoảng cách Laser)",
    0x38: "DHT20 / AHT20 / AHT21 (Nhiệt độ, độ ẩm số)",
    0x39: "TSL2561 (Cảm biến ánh sáng cường độ cao)",
    0x3C: "Màn hình OLED 0.96/1.3 inch SSD1306/SH1106 (0x3C)",
    0x3D: "Màn hình OLED SSD1306 phụ (0x3D)",
    0x48: "ADS1115 ADC 16-bit / PCF8591",
    0x50: "AT24C32 / AT24C64 EEPROM Onboard (0x50)",
    0x54: "K2 Hub Onboard Motor Driver / Co-processor (0x54)",
    0x55: "K2 Hub Onboard Motor Driver / Co-processor (0x55)",
    0x68: "MPU6050 / MPU9250 IMU 6DOF (Con quay hồi chuyển & Gia tốc kế)",
    0x69: "MPU6050 / MPU9250 IMU phụ (0x69)",
    0x76: "BMP280 / BME280 / MS5611 (Áp suất khí quyển 0x76)",
    0x77: "BMP280 / BME280 (Áp suất khí quyển 0x77)",
}

def identify(addr):
    return KNOWN_DEVICES.get(addr, "Thiết bị I2C (Chưa rõ model)")

def scan_bus(scl, sda, freq=100000):
    s_pin, d_pin, bus = None, None, None
    devs = []
    err = None
    try:
        s_pin = Pin(scl, Pin.IN, Pin.PULL_UP)
        d_pin = Pin(sda, Pin.IN, Pin.PULL_UP)
        bus = SoftI2C(scl=s_pin, sda=d_pin, freq=freq, timeout=5000)
        devs = bus.scan()
    except Exception as e:
        err = str(e)
    finally:
        try:
            if s_pin: Pin(scl, Pin.IN)
            if d_pin: Pin(sda, Pin.IN)
        except:
            pass
    return devs, err

def run_scan():
    tests = [
        # Cặp 1: D3 - D4 (GPIO 6, 7)
        {"port": "Grove 1 (D3-D4)", "dir": "THUẬN (SCL=D3/GPIO6, SDA=D4/GPIO7)", "scl": 6, "sda": 7},
        {"port": "Grove 1 (D3-D4)", "dir": "ĐẢO  (SCL=D4/GPIO7, SDA=D3/GPIO6)", "scl": 7, "sda": 6},

        # Cặp 2: D5 - D6 (GPIO 8, 9)
        {"port": "Grove 2 (D5-D6)", "dir": "THUẬN (SCL=D5/GPIO8, SDA=D6/GPIO9)", "scl": 8, "sda": 9},
        {"port": "Grove 2 (D5-D6)", "dir": "ĐẢO  (SCL=D6/GPIO9, SDA=D5/GPIO8)", "scl": 9, "sda": 8},

        # Cặp 3: D7 - D8 (GPIO 10, 17)
        {"port": "Grove 3 (D7-D8)", "dir": "THUẬN (SCL=D7/GPIO10, SDA=D8/GPIO17)", "scl": 10, "sda": 17},
        {"port": "Grove 3 (D7-D8)", "dir": "ĐẢO  (SCL=D8/GPIO17, SDA=D7/GPIO10)", "scl": 17, "sda": 10},

        # Cổng I2C Onboard (GPIO 12, 11)
        {"port": "I2C Onboard (SCL-SDA)", "dir": "THUẬN (SCL=GPIO12, SDA=GPIO11)", "scl": 12, "sda": 11},
        {"port": "I2C Onboard (SCL-SDA)", "dir": "ĐẢO  (SCL=GPIO11, SDA=GPIO12)", "scl": 11, "sda": 12},

        # Mở rộng Analog Grove: A0 - A1 (GPIO 1, 2)
        {"port": "Grove Analog (A0-A1)", "dir": "THUẬN (SCL=A0/GPIO1, SDA=A1/GPIO2)", "scl": 1, "sda": 2},
        {"port": "Grove Analog (A0-A1)", "dir": "ĐẢO  (SCL=A1/GPIO2, SDA=A0/GPIO1)", "scl": 2, "sda": 1},

        # Mở rộng Analog Grove: A2 - A3 (GPIO 3, 4)
        {"port": "Grove Analog (A2-A3)", "dir": "THUẬN (SCL=A2/GPIO3, SDA=A3/GPIO4)", "scl": 3, "sda": 4},
        {"port": "Grove Analog (A2-A3)", "dir": "ĐẢO  (SCL=A3/GPIO4, SDA=A2/GPIO3)", "scl": 4, "sda": 3},
    ]

    print("\n" + "=" * 78)
    print("   BẮT ĐẦU QUÉT I2C TOÀN DIỆN TRÊN K2 HUB (ESP32-S3)")
    print("   Tần số thử nghiệm: 100 kHz (Chuẩn) và 50 kHz (Dây dài/trở kéo thấp)")
    print("=" * 78)

    found_list = []

    for t in tests:
        p_name = t["port"]
        p_dir  = t["dir"]
        scl    = t["scl"]
        sda    = t["sda"]

        for freq in [100000, 50000]:
            f_khz = freq // 1000
            devs, err = scan_bus(scl, sda, freq)
            if devs:
                print("[PHÁT HIỆN] {} @ {}kHz | {}:".format(p_name, f_khz, p_dir))
                for d in devs:
                    h = "0x{:02X}".format(d)
                    name = identify(d)
                    print("            -> Hex: {} (Dec: {:3d}) : {}".format(h, d, name))
                found_list.append({
                    "port": p_name,
                    "dir": p_dir,
                    "scl": scl,
                    "sda": sda,
                    "freq": f_khz,
                    "devs": devs
                })
            elif err:
                print("[LỖI PIN ] {} @ {}kHz | {}: {}".format(p_name, f_khz, p_dir, err))
            else:
                print("[TRỐNG   ] {} @ {}kHz | {}".format(p_name, f_khz, p_dir))

    print("\n" + "=" * 78)
    print("               BẢNG TỔNG KẾT TOÀN BỘ CẢM BIẾN TRÊN K2 HUB")
    print("=" * 78)
    
    grouped = {}
    for item in found_list:
        k = (item["port"], item["dir"], item["scl"], item["sda"])
        if k not in grouped:
            grouped[k] = {"freqs": [], "devs": item["devs"]}
        grouped[k]["freqs"].append(str(item["freq"]) + "kHz")

    if grouped:
        for (port, p_dir, scl, sda), data in grouped.items():
            freq_str = ", ".join(data["freqs"])
            print("* CỔNG: {} [SCL=GPIO{}, SDA=GPIO{}]".format(port, scl, sda))
            print("  - Chiều chân: {}".format(p_dir))
            print("  - Tần số đáp ứng: {}".format(freq_str))
            for d in data["devs"]:
                h = "0x{:02X}".format(d)
                print("  - Thiết bị: {} (Dec {}) -> {}".format(h, d, identify(d)))
            print("-" * 78)
    else:
        print("KHÔNG CÓ THIẾT BỊ NÀO ĐƯỢC PHÁT HIỆN.")

    print("=== HOAN TAT TOAN BO QUET I2C ===")

if __name__ == "__main__":
    run_scan()
