import asyncio
import json
import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers import Code

class LightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.device_id = "light01"
        self.status = "OFF"

    async def render_get(self, request):
        """Xử lý yêu cầu GET hoặc đăng ký Observe từ Client"""
        # Kiểm tra nếu request có chứa tùy chọn Observe -> Client thực hiện đăng ký theo dõi
        if hasattr(request, 'opt') and request.opt.observe is not None:
            print("\nNew Observe registration received")

        payload = {
            "device_id": self.device_id,
            "status": self.status
        }
        json_payload = json.dumps(payload).encode('utf-8')
        return aiocoap.Message(payload=json_payload, content_format=50) # 50 = application/json

    async def render_put(self, request):
        """Xử lý yêu cầu PUT: Nhận lệnh bật/tắt đèn"""
        print("\nPUT request received:")
        try:
            data = json.loads(request.payload.decode('utf-8'))
            device = data.get("device_id")
            command = data.get("command")

            print(f"Device: {device}")
            print(f"Command: {command}")

            if command not in ["ON", "OFF"]:
                print("Lệnh không hợp lệ!")
                return aiocoap.Message(code=Code.BAD_REQUEST, payload=b"Invalid command. Use ON or OFF.")

            # Cập nhật trạng thái nếu có thay đổi
            if self.status != command:
                old_status = self.status
                self.status = command
                print(f"\nLight state changed: {old_status} -> {self.status}")
                print(f"Notify observers: {self.status}")
                
                # Báo cho aiocoap gửi thông báo Observe tới các client đã đăng ký
                self.updated_state()
            else:
                print(f"Light is already {self.status}. No change.")

            # Phản hồi lại Client với mã 2.04 Changed
            response_payload = json.dumps({"device_id": self.device_id, "status": self.status}).encode('utf-8')
            return aiocoap.Message(code=Code.CHANGED, payload=response_payload)

        except json.JSONDecodeError:
            print("Payload không đúng định dạng JSON!")
            return aiocoap.Message(code=Code.BAD_REQUEST, payload=b"Invalid JSON format.")
        except Exception as e:
            print(f"Lỗi xử lý PUT: {e}")
            return aiocoap.Message(code=Code.INTERNAL_SERVER_ERROR)

async def main():
    root = resource.Site()
    
    # Cấu hình tài nguyên tại /iot/lab/light01/status
    root.add_resource(['iot', 'lab', 'light01', 'status'], LightResource())

    # Lắng nghe tại cổng 5683
    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))

    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")
    
    # Giữ server chạy liên tục
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")