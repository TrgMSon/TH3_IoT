import asyncio
import datetime
import aiocoap
import aiocoap.resource as resource


class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.message = "Xin chao tu CoAP Server"
        self.last_post_message = None

    async def render_get(self, request):
        """Xử lý yêu cầu GET: Trả về thông điệp chào mừng từ Server"""
        print("\nGET request received: /iot/lab/message", flush=True)
        return aiocoap.Message(
            code=aiocoap.Code.CONTENT,  # 2.05 Content
            payload=self.message.encode("utf-8")
        )

    async def render_post(self, request):
        """Xử lý yêu cầu POST: Nhận thông điệp từ Client, hiển thị nội dung và thời gian"""
        payload_text = request.payload.decode("utf-8")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.last_post_message = payload_text

        print("\nPOST request received:", flush=True)
        print(f"Payload: {payload_text}", flush=True)
        print(f"Time: {current_time}", flush=True)

        # Trả về phản hồi xác nhận với mã 2.04 Changed
        return aiocoap.Message(
            code=aiocoap.Code.CHANGED,  # 2.04 Changed
            payload="Server da nhan thong diep".encode("utf-8")
        )


async def main():
    root = resource.Site()

    # Cung cấp tài nguyên có URI: /iot/lab/message
    root.add_resource(['iot', 'lab', 'message'], MessageResource())

    # Khởi tạo CoAP Server lắng nghe trên cổng 5683
    # Binds 127.0.0.1 và ::1 để hỗ trợ cả localhost và 127.0.0.1 trên Windows
    servers = []
    s1 = await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    servers.append(s1)
    try:
        s2 = await aiocoap.Context.create_server_context(root, bind=('::1', 5683))
        servers.append(s2)
    except Exception:
        pass

    print("CoAP Server started on port 5683", flush=True)

    try:
        await asyncio.get_running_loop().create_future()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        for s in servers:
            await s.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
