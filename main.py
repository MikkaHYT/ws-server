import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket, path):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'draw':
                await broadcast(data)
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def broadcast(data):
    if connected_clients:
        message = json.dumps(data)
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
