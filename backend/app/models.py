from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    user: str
    message: str
    timestamp: datetime = datetime.utcnow()