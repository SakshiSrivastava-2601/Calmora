from pyexpat import model
from flask import app
from crisis_check import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat
from main import ChatRequest  # if you saved that in crisis_check.py

@app.post("/chat")
async def chat_with_bot(chat_request: ChatRequest):
    user_message = chat_request.message
    try:
        if contains_crisis_keywords(user_message):
            # Log crisis message
            log_chat(chat_request.session_id, user_message, SAFETY_MESSAGE, True)
            return {"response": SAFETY_MESSAGE, "crisis_flag": True}

        # If not a crisis, continue to Gemini
        response = model.generate_content(user_message)
        log_chat(chat_request.session_id, user_message, response.text, False)
        return {"response": response.text, "crisis_flag": False}
        
    except Exception as e:
        return {"error": str(e)}
