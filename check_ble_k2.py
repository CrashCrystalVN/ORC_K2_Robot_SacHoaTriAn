import asyncio
import os
import sys
import time
from bleak import BleakClient

ADDRESS = "98:3D:AE:E4:F5:BA"
RX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

rx_buf = bytearray()
rx_event = asyncio.Event()

def on_rx(sender, data):
    global rx_buf
    rx_buf.extend(data)
    rx_event.set()

async def wait_output(timeout=3.0):
    global rx_buf
    start = time.time()
    out = bytearray()
    while time.time() - start < timeout:
        try:
            await asyncio.wait_for(rx_event.wait(), timeout=0.2)
            rx_event.clear()
            out.extend(rx_buf)
            rx_buf.clear()
            if b'>' in out:
                break
        except asyncio.TimeoutError:
            pass
    return bytes(out)

async def send_raw(client, code_str, timeout=5.0):
    global rx_buf
    rx_buf.clear()
    payload = code_str.encode('utf-8') + b'\x04'
    for i in range(0, len(payload), 20):
        chunk = payload[i:i+20]
        await client.write_gatt_char(RX_UUID, chunk, response=True)
    res = await wait_output(timeout)
    return res.decode('utf-8', errors='replace')

async def main():
    print(f"Connecting to {ADDRESS}...")
    async with BleakClient(ADDRESS) as client:
        print("Connected!")
        await client.start_notify(TX_UUID, on_rx)
        # Ctrl-C
        print("Sending Ctrl-C...")
        await client.write_gatt_char(RX_UUID, b'\x03\x03', response=True)
        await asyncio.sleep(0.5)
        # Ctrl-A (Raw REPL)
        print("Sending Ctrl-A (Raw REPL)...")
        await client.write_gatt_char(RX_UUID, b'\x01', response=True)
        await asyncio.sleep(0.5)
        print("Raw REPL buffer:", bytes(rx_buf))
        rx_buf.clear()

        # Execute os.listdir()
        print("Querying files on board...")
        res = await send_raw(client, "import os\nprint('FILES:', os.listdir())")
        print("Result:\n", res)

        # Check flash free space
        res_space = await send_raw(client, "import os\ns = os.statvfs('/')\nprint('FREE_KB:', (s[0]*s[3])//1024)")
        print("Result space:\n", res_space)

if __name__ == "__main__":
    asyncio.run(main())
