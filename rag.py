import sys
import asyncio

# Windows-specific asyncio fix
if sys.platform.startswith("win"):
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Google API key
GOOGLE_API_KEY = "AIzaSyDwv_96yoBnczeNSWLbHSBCTPQ6gbkMVLM"

# Set up embeddings
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Load FAISS vectorstore
vectorstore = FAISS.load_local(
    "karma_index",
    embedding,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()

# Gemini via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True
)

# Answer generation
def generate_answer(question: str, is_logged_in: bool = False, username: str = None) -> str:
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the context below to answer the question as helpfully and accurately as possible:

CONTEXT:
{context}

QUESTION:
{question}

Only answer from the context. Be clear and friendly."""

    response = llm.invoke(prompt)
    answer = response.content.strip()

    # Optional post-login additions
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

        if username:
            answer += f"\n\n(You are logged in as {username}.)"

    return answer

# Optional CLI testing
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        answer = generate_answer(q, is_logged_in=True, username="alice")
        print(f"\n🧠 Gemini says: {answer}")
