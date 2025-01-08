import google.generativeai as genai
from typing import Dict, Optional
import os
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

class ChatService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat(history=[])

    async def get_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Get response from the chatbot"""
        try:
            system_prompt = """You are a knowledgeable assistant specialized in Vedic literature, 
            particularly the Rig Veda. Help users understand the verses, their meanings, and their 
            significance in today's context. Always provide sources or references when discussing 
            specific verses. If you're not sure about something, be honest about it."""

            prompt = f"{system_prompt}\n\nUser: {message}"
            if context and context.get('current_verse'):
                verse = context['current_verse']
                prompt += f"\n\nCurrent verse context:\nSanskrit: {verse.get('sanskrit', '')}\nTranslation: {verse.get('translation', '')}"

            response = await asyncio.to_thread(
                self.chat.send_message, prompt
            )
            
            return response.text

        except Exception as e:
            print(f"Error in get_chat_response: {str(e)}")
            return "I apologize, but I encountered an error. Please try asking your question again."