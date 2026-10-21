import asyncio
import json
import aiocoap

SERVER_URI = 'coap://127.0.0.1:5683/iot/lab/light01/status'

async def send_put_command(protocol, command):
    print("\nSending PUT request...")
    payload = {
        "device_id": "light01",
        "command": command
    }
    encoded_payload = json.dumps(payload).encode('utf-8')
    request = aiocoap.Message(code=aiocoap.PUT, uri=SERVER_URI, payload=encoded_payload)

    try:
        response = await protocol.request(request).response
        print(f"Response Code: {response.code}")
        if response.code.is_successful():
            if command == "ON":
                print("Da bat den light01")
            elif command == "OFF":
                print("Da tat den light01")
        else:
            print(f"Lỗi từ server: {response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"Lỗi khi gửi PUT: {e}")

async def send_get_status(protocol):
    print("\nSending GET request...")
    request = aiocoap.Message(code=aiocoap.GET, uri=SERVER_URI)

    try:
        response = await protocol.request(request).response
        print("Response:")
        print(response.payload.decode('utf-8'))
    except Exception as e:
        print(f"Lỗi khi gửi GET: {e}")

async def main():
    protocol = await aiocoap.Context.create_client_context()
    loop = asyncio.get_running_loop()

    while True:
        # Sử dụng run_in_executor để input() không chặn vòng lặp bất đồng bộ
        cmd = await loop.run_in_executor(None, input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
        cmd = cmd.strip().upper()

        if cmd == "EXIT":
            print("Ket thuc chuong trinh.")
            break
        elif cmd in ["ON", "OFF"]:
            await send_put_command(protocol, cmd)
        elif cmd == "STATUS":
            await send_get_status(protocol)
        else:
            print("Lenh khong hop le! Vui long nhap ON, OFF, STATUS hoac EXIT.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController client stopped.")