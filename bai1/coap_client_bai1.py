import asyncio
import aiocoap


async def main():
    print("CoAP Client", flush=True)

    # 1. Khởi tạo CoAP Client Context
    context = await aiocoap.Context.create_client_context()

    server_uri = "coap://localhost:5683/iot/lab/message"

    try:
        # 2. Thực hiện yêu cầu GET tới /iot/lab/message
        print("Sending GET request...", flush=True)
        print(f"URI: {server_uri}\n", flush=True)

        get_request = aiocoap.Message(code=aiocoap.Code.GET, uri=server_uri)
        get_response = await context.request(get_request).response

        print("Response:", flush=True)
        print(f"Code: {get_response.code}", flush=True)
        print(f"Payload: {get_response.payload.decode('utf-8')}\n", flush=True)

        # 3. Thực hiện yêu cầu POST gửi thông tin sinh viên
        post_payload = "Xin chao tu CoAP Client - B23DCCN768 - Lang Viet Thanh"
        print("Sending POST request...", flush=True)
        print(f"Payload: {post_payload}\n", flush=True)

        post_request = aiocoap.Message(
            code=aiocoap.Code.POST,
            uri=server_uri,
            payload=post_payload.encode("utf-8")
        )
        post_response = await context.request(post_request).response

        print("Response:", flush=True)
        print(f"Code: {post_response.code}", flush=True)
        print(f"Payload: {post_response.payload.decode('utf-8')}", flush=True)

    except Exception as e:
        print(f"Error during request: {e}", flush=True)
    finally:
        await context.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
