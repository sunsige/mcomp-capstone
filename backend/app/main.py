# backend/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    # TODO: Integrate NLP model
    return {"response": "This is a placeholder response."}