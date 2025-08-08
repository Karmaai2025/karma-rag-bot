# rag_chat.py

import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Gemini API
genai.configure(api_key="AIzaSyA_5lIT4kc-Ni5OoS44HmVQvuDT8bRBJTA")  # ← Replace with your actual API key

# Load your FAISS index
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

# Set up Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

def generate_answer(question: str) -> str:
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the context below to answer the question:

    CONTEXT:
    {context}

    QUESTION:
    {question}

    Be accurate, concise, and friendly. Only answer based on the context provided.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# CLI Interface
if __name__ == "__main__":
    while True:
        user_question = input("\nAsk a question (or type 'exit'): ")
        if user_question.lower() == "exit":
            break
        answer = generate_answer(user_question)
        print(f"\n🧠 Gemini says: {answer}")
