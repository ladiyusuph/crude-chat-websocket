from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from manager import WebsocketManger
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(
    directory="templates",
)
manager = WebsocketManger()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.websocket("/ws")
async def connect_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    while True:
        message = await websocket.receive_json()
        print(f"Recieved message: {message}")
        for client in manager.connected_clients:
            await manager.send_message(client, message)
