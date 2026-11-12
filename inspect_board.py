import asyncio, time
from bleak import BleakClient

ADDRESS = '98:3D:AE:E4:F5:BA'
RX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'

rx_buf = bytearray()
rx_event = asyncio.Event()

def on_rx(sender, data):
    global rx_buf
    rx_buf.extend(data)
    rx_event.set()

async def exec_cmd(client, code):
    global rx_buf
    rx_buf.clear()
    payload = code.encode('utf-8') + b'\x04'
    for i in range(0, len(payload), 20):
        await client.write_gatt_char(RX_UUID, payload[i:i+20], response=True)
        await asyncio.sleep(0.01)
    
    out = bytearray()
    start = time.time()
    while time.time() - start < 4.0:
        try:
            await asyncio.wait_for(rx_event.wait(), timeout=0.3)
            rx_event.clear()
            out.extend(rx_buf)
            rx_buf.clear()
            if b'\x04' in out or b'>' in out:
                break
        except asyncio.TimeoutError:
            pass
    return out.decode('utf-8', errors='replace')

async def main():
    print("Connecting to", ADDRESS, "...")
    async with BleakClient(ADDRESS) as client:
        print("Connected!")
        await client.start_notify(TX_UUID, on_rx)
        # Ctrl-C to interrupt, then Ctrl-A to enter raw REPL
        await client.write_gatt_char(RX_UUID, b'\x03\x03\x01', response=True)
        await asyncio.sleep(0.5)
        
        print("--- LIST FILES ---")
        res = await exec_cmd(client, "import os\nprint(os.listdir())\n")
        print(res)

        print("--- MAIN.PY CONTENT ---")
        res_main = await exec_cmd(client, "f=open('main.py'); print(f.read()[:500]); f.close()\n")
        print(res_main)

if __name__ == "__main__":
    asyncio.run(main())

