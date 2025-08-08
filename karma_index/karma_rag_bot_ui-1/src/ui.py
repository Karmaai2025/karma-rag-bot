from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END
import threading
import sys
sys.path.append('..')  # Adjust the path to import rag.py
from rag import generate_answer

class ChatbotUI:
    def __init__(self, master):
        self.master = master
        master.title("Karma RAG Bot")

        self.label = Label(master, text="Ask a question:")
        self.label.pack()

        self.entry = Entry(master, width=50)
        self.entry.pack()

        self.ask_button = Button(master, text="Ask", command=self.ask_question)
        self.ask_button.pack()

        self.response_area = Text(master, height=15, width=50)
        self.response_area.pack()

        self.scrollbar = Scrollbar(master, command=self.response_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.response_area.config(yscrollcommand=self.scrollbar.set)

    def ask_question(self):
        question = self.entry.get()
        self.entry.delete(0, END)
        self.response_area.insert(END, f"You: {question}\n")
        self.response_area.see(END)

        threading.Thread(target=self.get_answer, args=(question,)).start()

    def get_answer(self, question):
        answer = generate_answer(question)
        self.response_area.insert(END, f"🧠 Gemini says: {answer}\n")
        self.response_area.see(END)

if __name__ == "__main__":
    root = Tk()
    chatbot_ui = ChatbotUI(root)
    root.mainloop()