import os
import requests

def ask_ollama(question, context, model="llama3.1:latest"):
    """
    Send a question and context to the Ollama API and return the response.
    """
    url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model,
        "prompt": f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    }
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        answer = ""
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                try:
                    obj = __import__('json').loads(data)
                    answer += obj.get("response", "")
                except Exception:
                    continue
        return answer if answer else "No answer returned."
    except Exception as e:
        return f"Error communicating with Ollama: {e}"
