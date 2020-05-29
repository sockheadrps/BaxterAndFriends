import asyncio
import websockets


async def receive_client_slider_data(sock, path):
    try:
        while not sock.closed:
            data = await sock.recv()
            print(type(data))
            greeting = f"data received:  {data}!"
            await sock.send(greeting)
            print(f"> {greeting}")
    except websockets.exceptions.ConnectionClosedOK as e:
        pass
    finally:
        print('connection closed')


def init_server():
    start_server = websockets.serve(receive_client_slider_data, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
