import asyncio
import os
import sys
import time
from bleak import BleakClient, BleakScanner

ADDRESS = "98:3D:AE:E4:F5:BA"
RX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

rx_buffer = bytearray()
rx_event = asyncio.Event()

def notification_handler(sender, data):
    global rx_buffer
    rx_buffer.extend(data)
    rx_event.set()

async def wait_for_response(timeout=2.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            await asyncio.wait_for(rx_event.wait(), timeout=0.2)
            rx_event.clear()
        except asyncio.TimeoutError:
            pass
        if b">" in rx_buffer or b"raw REPL" in rx_buffer:
            break
    res = bytes(rx_buffer)
    rx_buffer.clear()
    return res

async def execute_raw(client, code_str, timeout=5.0):
    global rx_buffer
    rx_buffer.clear()
    payload = code_str.encode('utf-8') + b'\x04'
    
    # Send in MTU-friendly chunks of 50 bytes
    for i in range(0, len(payload), 50):
        chunk = payload[i:i+50]
        await client.write_gatt_char(RX_UUID, chunk, response=False)
        await asyncio.sleep(0.02)
        
    start = time.time()
    output = bytearray()
    while time.time() - start < timeout:
        try:
            await asyncio.wait_for(rx_event.wait(), timeout=0.3)
            rx_event.clear()
            output.extend(rx_buffer)
            rx_buffer.clear()
            if b"\x04>" in output or (b"\x04" in output and len(output) > 2):
                break
        except asyncio.TimeoutError:
            pass
            
    # Raw REPL output format: OK <stdout> \x04 <stderr> \x04 >
    text = output.decode('utf-8', errors='ignore')
    return text

async def upload_file_over_ble(client, local_file_path, remote_filename):
    print(f"[-] Đang nạp tệp: {remote_filename} ({os.path.getsize(local_file_path)} bytes)...")
    with open(local_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Mở file ghi trên board
    await execute_raw(client, f"f = open('{remote_filename}', 'w')")
    
    # Ghi từng đoạn (chunk 128 ký tự để an toàn qua BLE)
    chunk_size = 120
    total = len(content)
    for i in range(0, total, chunk_size):
        chunk = content[i:i+chunk_size]
        # Escape string in Python representation
        chunk_repr = repr(chunk)
        cmd = f"f.write({chunk_repr})"
        await execute_raw(client, cmd, timeout=2.0)
        percent = min(100, int((i + len(chunk)) * 100 / total))
        print(f"\r    -> Tiến độ: {percent:3d}%", end="", flush=True)

    await execute_raw(client, "f.close()")
    print("\n    [OK] Đã hoàn tất ghi file.")

async def flash_k2_bluetooth():
    print("=" * 60)
    print(" TIẾN TRÌNH NẠP CODE TEST QUA BLUETOOTH (BLE REPL) K2 CONTROL HUB")
    print(f" Mục tiêu BLE: ohstem-yolo-uno-f5b8 ({ADDRESS})")
    print("=" * 60)

    print("[-] Đang kết nối tới mạch K2 Control Hub qua BLE...")
    async with BleakClient(ADDRESS) as client:
        print("[+] Đã kết nối Bluetooth LE thành công!")
        await client.start_notify(TX_UUID, notification_handler)

        # 1. Gửi ngắt Ctrl-C hai lần để dừng app đang chạy
        print("[-] Dừng chương trình hiện tại trên mạch...")
        await client.write_gatt_char(RX_UUID, b'\x03\x03', response=False)
        await asyncio.sleep(0.6)

        # 2. Chuyển sang chế độ Raw REPL (Ctrl-A)
        print("[-] Chuyển sang Raw REPL Mode...")
        await client.write_gatt_char(RX_UUID, b'\x01', response=False)
        await asyncio.sleep(0.5)

        # 3. Kiểm tra danh sách file hiện tại trên K2
        out = await execute_raw(client, "import os; print('FILES:', os.listdir())")
        print("[-] Danh sách file hiện tại trên hệ thống LittleFS:")
        for line in out.splitlines():
            if "FILES:" in line:
                print("   ", line.strip())

        # 4. Nạp code test vào main.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        test_main_path = os.path.join(base_dir, "Firmware", "main_test.py")
        
        await upload_file_over_ble(client, test_main_path, "main.py")

        # 5. Khởi động lại mạch để chạy code mới
        print("\n[-] Đang khởi động lại K2 Control Hub...")
        # Soft reset: gửi Ctrl-D trong raw REPL hoặc reset bằng machine.reset()
        await execute_raw(client, "import machine; machine.reset()", timeout=1.0)
        await asyncio.sleep(1.0)
        
        print("\n" + "=" * 60)
        print(">>> CHÚC MỪNG: BẢN TEST ĐÃ ĐƯỢC NẠP THÀNH CÔNG QUA BLUETOOTH! <<<")
        print(" Mạch đang tự khởi động lại và bắt đầu chạy bài test phần cứng!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(flash_k2_bluetooth())

