import typing as t

from fastapi.logger import logger
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://127.0.0.1',
    'http://127.0.0.1:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


async def send_message(message: t.Dict[str, t.Any]) -> bool:
    async with httpx.AsyncClient() as client:
        client.headers.update({'Authorization': 'apikey cbf46e80-3e00-4642-8f3a-369b8707304d'})
        data = {
            'method': 'publish',
            'params': {
                'channel': 'signal',
                'data': message
            }
        }
        response: httpx.Response = await client.post(
            url='http://centrifugal:8000/api',
            json=data,
        )
        logger.info(f'message: {message}, response: {response.json()}')
        try:
            response.raise_for_status()
            return True
        except Exception:
            return False


@app.post('/api/message/')
async def read_message(message: t.Dict[str, t.Any]) -> t.Dict[str, bool]:
    status = await send_message(message)
    return {'status': status}


class SocketManager:
    def __init__(self):
        self.active_connections: t.List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data):
        print('send >>>', data)
        for connection in self.active_connections:
            await connection.send_json(data)


manager = SocketManager()


@app.websocket('/signal')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data and data['type'] == 'ping':
                await websocket.send_json({'type': 'pong'})
            elif data:
                await manager.broadcast(data)
    except (WebSocketDisconnect, RuntimeError):
        manager.disconnect(websocket)
