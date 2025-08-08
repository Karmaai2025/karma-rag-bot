import streamlit as st
from rag import generate_answer

# Dummy users
USERS = {
    "alice": "password1",
    "bob": "password2",
    "charlie": "password3"
}

def login():
    st.title("🔒 Karma Chatbot Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    if login_btn:
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

def chatbot():
    st.title("🧠 Karma RAG Chatbot")
    st.write(f"Hello, {st.session_state['username']}! Ask your question below:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Type your question...", key="input")

    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append(("user", user_input))
        with st.spinner("Thinking..."):
            answer = generate_answer(
                user_input,
                is_logged_in=True,
                username=st.session_state["username"]
            )
        st.session_state.chat_history.append(("bot", answer))
        st.rerun()

    for sender, message in st.session_state.chat_history:
        bubble_class = "user-bubble" if sender == "user" else "bot-bubble"
        st.markdown(
            f'<div class="chat-bubble {bubble_class}">{message}</div>',
            unsafe_allow_html=True,
        )

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# CSS for chat bubbles
st.markdown(
    """
    <style>
    .chat-bubble {
        background: #f0f2f6;
        border-radius: 1.2em;
        padding: 1em;
        margin-bottom: 1em;
        max-width: 80%;
        font-size: 1.1em;
    }
    .user-bubble {
        background: #d1e7dd;
        margin-left: auto;
        text-align: right;
    }
    .bot-bubble {
        background: #f8d7da;
        margin-right: auto;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    chatbot()