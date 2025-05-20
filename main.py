from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware  # ✅ import CORS middleware
import google.generativeai as genai
import os
from uuid import uuid4
from datetime import datetime
from logger import log_chat  # make sure logger.py has log_chat function

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # ✅ Allow Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Define request body
class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(default_factory=lambda: str(uuid4()))

# Define route
@app.post("/chat")
async def chat_with_bot(chat_request: ChatRequest):
    try:
        user_message = chat_request.message
        response = model.generate_content(user_message)
        bot_reply = response.text

        # Simple keyword-based crisis detection
        crisis_keywords = ["suicide", "kill myself", "end my life", "hopeless", "can't go on"]
        is_crisis = any(word in user_message.lower() for word in crisis_keywords)

        log_chat(
            session_id=chat_request.session_id,
            query=user_message,
            response=bot_reply,
            is_crisis=is_crisis
        )

        return {"response": bot_reply, "crisis_flag": is_crisis}
    except Exception as e:
        return {"error": str(e)}
