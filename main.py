from fastapi import FastAPI , Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from cohere import Client

load_dotenv()

app = FastAPI()
co = Client(os.getenv("COHERE_API_KEY"))

class chatRequest(BaseModel):
	message: str
	history: list = []

@app.get("/test")
async def read_root():
	return {"message": "Test API"}



sessions = {}

@app.post("/chat")
async def chat(request: Request, body: chatRequest):
    user_id = request.client.host
    history = sessions.get(user_id, [])

    response = co.chat(
		model="command-a-03-2025",
        message=body.message,
        chat_history=history
    )
    # เก็บ history กลับ
    history.append({"role": "USER", "message": body.message})
    history.append({"role": "CHATBOT", "message": response.text})
    sessions[user_id] = history

    return {"reply": response.text}