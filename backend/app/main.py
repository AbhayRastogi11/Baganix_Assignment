from fastapi import FastAPI, WebSocket
from app.routes import router

app = FastAPI(title="AI Chatbot API", version="2.0")

app.include_router(router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            response = process_message(data)
            await websocket.send_text(response)
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break

def process_message(data):
    from chatbot import get_ai_response
    return get_ai_response(data)
