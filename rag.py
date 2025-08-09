import os
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

# ── Config ────────────────────────────────────────────────────────────────────
# Prefer env var on Render: add GOOGLE_API_KEY in the Environment tab
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "REPLACE_ME_LOCALLY")

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "AIzaSyDwv_96yoBnczeNSWLbHSBCTPQ6gbkMVLM":
    # Don't crash locally, but warn loudly
    print("⚠️  GOOGLE_API_KEY not set; set it in Render > Environment.")

# ── Embeddings ────────────────────────────────────────────────────────────────
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# ── Vector store / Retriever ──────────────────────────────────────────────────
# Make this robust in case the index is missing
def _load_retriever():
    try:
        vs = FAISS.load_local(
            "karma_index",
            embedding,
            allow_dangerous_deserialization=True
        )
        return vs.as_retriever()
    except Exception as e:
        print(f"❌ Failed to load FAISS index from 'karma_index': {e}")
        return None

retriever = _load_retriever()

# ── Gemini via LangChain (use a supported chat model) ─────────────────────────
# Valid choices: "gemini-1.5-pro" or "gemini-1.5-flash"
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True
)

# ── Answer generation ─────────────────────────────────────────────────────────
def generate_answer(question: str, is_logged_in: bool = False, username: str = None) -> str:
    if not question or not question.strip():
        return "Please provide a valid question."

    context = ""
    if retriever is not None:
        try:
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""
        except Exception as e:
            print(f"⚠️ Retrieval failed: {e}")
    else:
        print("⚠️ No retriever available (FAISS index not loaded). Proceeding without context.")

    prompt = f"""Use the context below to answer the question as helpfully and accurately as possible.

CONTEXT:
{context}

QUESTION:
{question}

Only answer from the context. Be clear and friendly.
If the context does not contain the answer, say you couldn't find it in the provided context.
"""

    resp = llm.invoke(prompt)
    # LangChain returns an AIMessage; get text safely
    answer = getattr(resp, "content", "") or (str(resp) if resp else "")
    answer = answer.strip() or "Sorry, I couldn't find an answer in the provided context."

    # Optional post-login additions
    if is_logged_in:
        links = {
            "hotdeals": "https://yourdomain.com/hotdeals",
            "destinations": "https://yourdomain.com/destinations",
            "haathi mahal": "https://yourdomain.com/haathi-mahal"
        }
        lq = question.lower()
        for keyword, url in links.items():
            if keyword in lq:
                answer += f"\n\nYou can check more information about {keyword} here: {url}"
        if username:
            answer += f"\n\n(You are logged in as {username}.)"

    return answer

# Optional CLI test
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print("\n🧠 Gemini says:\n", generate_answer(q, is_logged_in=True, username="alice"))
