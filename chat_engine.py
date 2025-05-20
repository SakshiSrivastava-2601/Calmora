import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your Google API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Per-session memory store
session_memory_map = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        session_memory_map[session_id] = []

    # Append user message
    session_memory_map[session_id].append({"role": "user", "parts": [user_query]})

    # Generate response
    chat = model.start_chat(history=session_memory_map[session_id])
    response = chat.send_message(user_query)

    # Append assistant message
    session_memory_map[session_id].append({"role": "model", "parts": [response.text]})

    return response.text
