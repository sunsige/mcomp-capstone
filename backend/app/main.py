from fastapi import FastAPI
from pydantic import BaseModel
from .indexing.indexer import index_document
from .utils.api_utils import query_deepseek

app = FastAPI()

class DocumentRequest(BaseModel):
    pdf_path: str

class ChatRequest(BaseModel):
    prompt: str

@app.post("/index")
async def index_document_endpoint(request: DocumentRequest):
    index, keywords = index_document(request.pdf_path)
    return {"message": "Document indexed successfully!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = query_deepseek(request.prompt)
    return {"response": response}