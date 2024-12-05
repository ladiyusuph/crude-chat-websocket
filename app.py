from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import WebsocketManger
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")
manager = WebsocketManger()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.websocket("/ws")
async def connect_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                message = await websocket.receive_json()
                print(f"Received message: {message}")
                
                # Broadcast to all connected clients
                for client in manager.connected_clients.copy():
                    try:
                        await manager.send_message(client, message)
                    except Exception as e:
                        print(f"Error broadcasting to a client: {e}")
                        await manager.disconnect(client)
            except WebSocketDisconnect:
                break
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(websocket)