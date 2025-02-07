import requests
from app.database import chat_collection
from datetime import datetime
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def get_ai_response(user_input, session_id="default"):
    try:
        # Retrieve last chat context
        last_chat = chat_collection.find_one({"session_id": session_id}, sort=[("timestamp", -1)])
        if last_chat:
            context = f"Previous: {last_chat['message']}. Now answer: {user_input}"
        else:
            context = user_input

        payload = {
            "model": "llama3.1",
            "prompt": context,
            "max_tokens": 100
        }

        # ✅ Handle streaming response
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)

        # ✅ Extract only the "response" field and concatenate it
        full_response = []
        for chunk in response.iter_lines():
            if chunk:
                try:
                    chunk_data = json.loads(chunk.decode("utf-8"))
                    if "response" in chunk_data:
                        full_response.append(chunk_data["response"])
                except json.JSONDecodeError:
                    continue  # Ignore decoding errors from partial JSON chunks

        # ✅ Join all responses into a single string
        bot_response = " ".join(full_response).strip()

        # ✅ Ensure we return a valid response
        if not bot_response:
            return "Sorry, I couldn't generate a response."

        # Store conversation in MongoDB
        chat_collection.insert_one({
            "session_id": session_id,
            "user": "User",
            "message": user_input,
            "bot_response": bot_response,
            "timestamp": datetime.utcnow()
        })

        return bot_response  # ✅ Return only the AI-generated text

    except Exception as e:
        return f"Error: {str(e)}"
