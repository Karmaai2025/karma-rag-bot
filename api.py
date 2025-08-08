from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from rag import generate_answer
from fastapi.middleware.cors import CORSMiddleware
import traceback
import os

app = FastAPI(
    title="Karma RAG Chatbot API",
    description="API for answering questions using Gemini and RAG",
    version="1.0.0"
)

# Allow CORS for all origins (adjust for production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class QuestionRequest(BaseModel):
    question: str

# Response body model
class AnswerResponse(BaseModel):
    answer: str

# Main chatbot endpoint
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    try:
        answer = generate_answer(req.question)
        return {"answer": answer}
    except Exception as e:
        print("❌ Error in /ask endpoint:")
        traceback.print_exc()  # This will show detailed error in Render logs
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Karma RAG Chatbot API is running."}
