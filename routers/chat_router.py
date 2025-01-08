from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

@router.post("/send-message")
async def send_message(request: ChatRequest):
    """Send a message to the chatbot and get a response"""
    try:
        response = await chat_service.get_response(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))