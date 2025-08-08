# File: /karma_rag_bot_ui/karma_rag_bot_ui/src/rag.py

import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Gemini API
genai.configure(api_key="AIzaSyDwv_96yoBnczeNSWLbHSBCTPQ6gbkMVLM")

# Load vectorstore
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key="AIzaSyDwv_96yoBnczeNSWLbHSBCTPQ6gbkMVLM"
)
vectorstore = FAISS.load_local(
    "karma_index",
    embedding,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()

# Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def generate_answer(question: str) -> str:
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the context below to answer the question as helpfully and accurately as possible:

    CONTEXT:
    {context}

    QUESTION:
    {question}

    Only answer from the context. Be clear and friendly."""

    response = model.generate_content(prompt)
    return response.text.strip()