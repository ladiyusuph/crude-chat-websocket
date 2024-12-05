from fastapi.websockets import WebSocket

class WebsocketManger:
    def __init__(self):
        self.connected_clients = []
        
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        client_ip = f"{websocket.client.host}: {websocket.client.port}"
        print(client_ip)
        self.connected_clients.append(websocket)
        message = {"client":client_ip, "message": f"Welcome"}
        
        await websocket.send_json(message)
    async def send_message(self, websocket:WebSocket, message:str):
        message = {
            "client": message["client"],
            "message":message["content"]
        }
        await websocket.send_json(message)
        
    async def disconnect(self, websocket:WebSocket):
        self.connected_clients.remove(websocket)
        print(f"Client {websocket.client.host}: {websocket.client.port} disconnected")
    
                
