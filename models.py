from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # dummy response logic
    return {"response": f"You said: {request.query}", "session_id": request.session_id}


