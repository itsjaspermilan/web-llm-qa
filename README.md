# Webpage Q&A with Ollama

This project is a Streamlit web application that lets you:
- Input a webpage URL
- Parse and store the main content
- Ask questions about the webpage using an LLM (Ollama)

The app uses ChromaDB and Sentence Transformers to embed and store webpage content for efficient retrieval and Q&A.

## Features
- Parse any webpage and store its content for Q&A
- Embedding and semantic search with Sentence Transformers and ChromaDB
- Ask questions and get answers from Ollama LLM
- Clean, simple UI with refresh capability

## Requirements
- [Ollama](https://ollama.com/) running llama3.1:latest locally (for LLM inference)
- Python 3.11+
- ASDF for language management (optional)

## Installation & Usage
1. **Install dependencies**
   ```sh
   asdf install
   pip install -r requirements.txt
   ```
1. **Start Ollama** (in a separate terminal)
   ```sh
   ollama serve
   ollama run llama3.1
   ```
1. **Run the app**
   ```sh
   streamlit run app.py
   ```
1. **Open your browser** to [http://localhost:8501](http://localhost:8501)

## How it Works
- Enter a webpage URL and click enter.
- The app fetches and parses the main content, stores it in ChromaDB, and shows a success message.
- Ask any question about the webpage in the input box.
- The app retrieves the most relevant content chunks and sends them, along with your question, to Ollama for an answer.
- Use the refresh button to clear the session and input a new URL.

## Project Structure
- `app.py` — Main Streamlit app
- `ollama_client.py` — Handles LLM API calls
- `requirements.txt` — Python dependencies

## Configuration
- The Ollama API endpoint defaults to `http://localhost:11434/api/generate`.
- You can set the `OLLAMA_API_URL` environment variable if needed.

## License
MIT
