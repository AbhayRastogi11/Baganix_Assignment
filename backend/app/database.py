from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    chat_collection = db["chat_logs"]
    chat_collection.create_index("session_id")  # Optimize search
    print("✅ Connected to MongoDB with session support!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
