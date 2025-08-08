from fastapi import FastAPI, Request
from pydantic import BaseModel
from rag import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Karma RAG Chatbot API",
    description="API for answering questions using Gemini and RAG",
    version="1.0.0"
)

# Allow CORS for all origins (adjust as needed for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    answer = generate_answer(req.question)
    return {"answer": answer}

# Optional: Health check endpoint
@app.get("/")
async def root():
    return {"message": "Karma RAG Chatbot API is running."}