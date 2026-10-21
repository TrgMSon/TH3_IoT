import asyncio
import json
import datetime
from aiocoap import Context, Message, GET
import aiocoap

async def main():
    # Tạo ngữ cảnh client
    protocol = await Context.create_client_context()
    uri = "coap://127.0.0.1:5683/iot/lab/sensor01/data"

    print(f"Monitoring Client started. Polling data from {uri} every 3 seconds...\n")

    try:
        while True:
            request = Message(code=GET, uri=uri)
            try:
                # Gửi yêu cầu và chờ phản hồi (timeout 4 giây)
                response = await protocol.request(request).response
                
                if response.code == aiocoap.Code.CONTENT:
                    # Parse dữ liệu JSON nhận được từ payload
                    data = json.loads(response.payload.decode('utf-8'))
                    
                    device_id = data.get("device_id")
                    temperature = data.get("temperature")
                    humidity = data.get("humidity")
                    receive_time = datetime.datetime.now().strftime('%H:%M:%S')

                    print(f"[{receive_time}] Received sensor data")
                    print(f"Device: {device_id}")
                    print(f"Temperature: {temperature} C")
                    print(f"Humidity: {humidity} %")

                    # Kiểm tra các điều kiện cảnh báo theo yêu cầu
                    has_warning = False
                    if temperature > 35:
                        print("CANH BAO: Nhiet do cao")
                        has_warning = True
                    if humidity < 40:
                        print("CANH BAO: Do am thap")
                        has_warning = True
                    
                    if not has_warning:
                        print("Trang thai: Binh thuong")
                        
                    print("-" * 30)
                else:
                    print(f"Error response code: {response.code}")

            except Exception as e:
                print(f"Failed to connect or fetch data: {e}")

            # Đợi 3 giây trước lần polling tiếp theo
            await asyncio.sleep(3)

    except KeyboardInterrupt:
        print("\nMonitoring Client stopped by user.")

if __name__ == "__main__":
    asyncio.run(main())