from fastapi import APIRouter, WebSocket
from app.chatbot import get_ai_response
from app.database import chat_collection
from datetime import datetime

router = APIRouter()

# ✅ Add a regular HTTP endpoint so Swagger UI shows something
@router.get("/test")
async def test_api():
    return {"message": "API is working!"}


@router.websocket("/ws/{user_id}")  # ✅ Ensure this matches frontend URL
async def chat_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        try:
            # ✅ Receive plain text instead of JSON
            data = await websocket.receive_text()
            bot_response = get_ai_response(data, session_id=user_id)

            # ✅ Store user interaction in MongoDB
            chat_collection.insert_one({
                "user_id": user_id,
                "message": data,
                "bot_response": bot_response,
                "timestamp": datetime.utcnow()
            })

            # ✅ Send response back to frontend
            await websocket.send_text(bot_response)
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break
