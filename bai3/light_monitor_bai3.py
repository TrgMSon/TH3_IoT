import asyncio
import json
from datetime import datetime
import aiocoap

SERVER_URI = 'coap://127.0.0.1:5683/iot/lab/light01/status'

async def main():
    print("Registering CoAP Observe...")
    protocol = await aiocoap.Context.create_client_context()

    # Tạo request GET với tùy chọn observe=0
    request = aiocoap.Message(code=aiocoap.GET, uri=SERVER_URI, observe=0)
    pr = protocol.request(request)

    # Lấy phản hồi đầu tiên để xác nhận đăng ký thành công
    first_response = await pr.response
    if first_response.code.is_successful():
        print("Observe registration successful\n")
    
    is_initial = True

    try:
        # Lắng nghe các thông báo tự động từ Server thông qua cơ chế Observe
        async for response in pr.observation:
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            try:
                data = json.loads(response.payload.decode('utf-8'))
                device_id = data.get("device_id", "N/A")
                status = data.get("status", "N/A")

                if is_initial:
                    print(f"{timestamp} Initial State")
                    is_initial = False
                else:
                    print(f"\n{timestamp} State Updated")

                print(f"Device: {device_id}")
                print(f"Status: {status}")

            except json.JSONDecodeError:
                print(f"{timestamp} Received raw: {response.payload.decode('utf-8')}")

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Lỗi Observe: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")