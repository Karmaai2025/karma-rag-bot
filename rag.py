import sys
import asyncio

if sys.platform.startswith("win"):
    try :
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

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

def generate_answer(question: str, is_logged_in: bool = False, username: str = None) -> str:
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the context below to answer the question as helpfully and accurately as possible:

    CONTEXT:
    {context}

    QUESTION:
    {question}

    Only answer from the context. Be clear and friendly."""

    response = model.generate_content(prompt)
    answer = response.text.strip()

    # Add post-login links if user is logged in
    if is_logged_in:
        links = {
            "hotdeals": "https://yourdomain.com/hotdeals",
            "destinations": "https://yourdomain.com/destinations",
            "haathi mahal": "https://yourdomain.com/haathi-mahal"
        }
        lower_q = question.lower()
        for keyword, url in links.items():
            if keyword in lower_q:
                answer += f"\n\nYou can check more information about {keyword} [here]({url})."

        # Example: user-specific message
        if username:
            answer += f"\n\n(You are logged in as {username}.)"

    return answer

# Example for CLI testing
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        answer = generate_answer(q, is_logged_in=True, username="alice")
        print(f"\n🧠 Gemini says: {answer}")
