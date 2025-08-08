# Karma RAG Bot UI

This project is a user interface for the existing Karma RAG Bot, which utilizes a generative AI model to answer questions based on relevant documents. The UI is designed to be visually appealing and user-friendly, allowing users to interact with the chatbot seamlessly.

## Project Structure

```
karma_rag_bot_ui
├── src
│   ├── rag.py          # Contains the chatbot functionality
│   ├── ui.py           # Implements the user interface
│   └── assets
│       └── styles.css  # CSS styles for the UI
├── requirements.txt     # Lists the required Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd karma_rag_bot_ui
   ```

2. **Install dependencies**:
   Create a virtual environment and activate it, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the following command to start the chatbot UI:
   ```
   python src/ui.py
   ```

## Usage Guidelines

- Once the application is running, you will see a user-friendly interface where you can input your questions.
- Type your question in the input field and press the "Ask" button to receive a response from the chatbot.
- To exit the application, simply close the window.

## Chatbot Functionality

The chatbot leverages the `generate_answer` function from `rag.py`, which retrieves relevant documents and generates responses using the Gemini model. The UI enhances user interaction by providing a clean and intuitive layout.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.