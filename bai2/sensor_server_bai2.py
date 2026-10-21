import asyncio
import random
import json
import datetime
from aiocoap import Context, Message, resource, PUT, GET
import aiocoap

class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.temperature = 28.0
        self.humidity = 60.0
        # Khởi động tác vụ nền cập nhật giá trị cảm biến mỗi 3 giây
        asyncio.create_task(self.update_sensor_data())

    async def update_sensor_data(self):
        while True:
            await asyncio.sleep(3)
            # Sinh ngẫu nhiên nhiệt độ (20.0 - 40.0) và độ ẩm (30.0 - 90.0)
            self.temperature = round(random.uniform(20.0, 40.0), 1)
            self.humidity = round(random.uniform(30.0, 90.0), 1)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Data updated -> Temp: {self.temperature}°C, Hum: {self.humidity}%")

    async def render_get(self, request):
        # Tạo dữ liệu JSON trả về cho Client
        payload_data = {
            "device_id": "sensor01",
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        payload_bytes = json.dumps(payload_data).encode('utf-8')
        
        # Trả về phản hồi với mã 2.05 Content và định dạng application/json (content format code 50)
        return Message(
            code=aiocoap.Code.CONTENT,
            payload=payload_bytes,
            content_format=50 
        )

async def main():
    # Khởi tạo tài nguyên gốc và gán tài nguyên sensor
    root = resource.Site()
    root.add_resource(['iot', 'lab', 'sensor01', 'data'], SensorResource())

    # Lắng nghe trên cổng mặc định 5683
    await Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("Sensor CoAP Server started on port 5683...")

    # Giữ server chạy liên tục
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")