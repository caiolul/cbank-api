from starlette.websockets import WebSocket


async def websocket_endpoint(websocket):
    await websocket.accept()
    # Process incoming messages
    while True:
        mesg = await websocket.receive_text()
        print(mesg)
        await websocket.send_text(mesg.replace("Client", "Server"))
    await websocket.close()
