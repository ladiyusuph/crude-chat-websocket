from fastapi.websockets import WebSocket

class WebsocketManger:
    def __init__(self):
        self.connected_clients = []
       
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        client_ip = f"{websocket.client.host}: {websocket.client.port}"
        print(f"Client connected: {client_ip}")
        self.connected_clients.append(websocket)
       
    async def send_message(self, websocket: WebSocket, message: dict):
        try:
            formatted_message = {
                "client": message.get("client", "Unknown"),
                "content": message.get("content", "")
            }
            await websocket.send_json(formatted_message)
        except Exception as e:
            print(f"Error sending message: {e}")
            await self.disconnect(websocket)
       
    async def disconnect(self, websocket: WebSocket):
        try:
            self.connected_clients.remove(websocket)
            client_ip = f"{websocket.client.host}: {websocket.client.port}"
            print(f"Client disconnected: {client_ip}")
        except ValueError:
            pass  # Client already removed