import streamlit as st
import requests
from bs4 import BeautifulSoup
from ollama_client import ask_ollama
import chromadb
from sentence_transformers import SentenceTransformer

st.title("Webpage Q&A with Ollama")

# Add a refresh button at the top
refresh = st.button("🔄 Refresh / Input New URL", key="refresh")
if refresh:
    st.session_state.clear()
    st.session_state["Enter a webpage URL:"] = ""
    st.rerun()

# Initialize ChromaDB client and collection
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("webpages")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Input for webpage URL
url = st.text_input("Enter a webpage URL:", key="Enter a webpage URL:")

# Placeholder for webpage content
doc_content = ""

if url:
    try:
        with st.spinner("Loading and parsing webpage..."):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract main text content
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            doc_content = "\n".join(paragraphs)
            # Show a success alert instead of displaying the parsed content
            st.success("Webpage has been parsed and stored for Q&A.")

            # Chunk the content for embedding
            chunk_size = 500
            chunks = [doc_content[i:i+chunk_size] for i in range(0, len(doc_content), chunk_size)]
            embeddings = embedder.encode(chunks).tolist()
            ids = [f"{url}_chunk_{i}" for i in range(len(chunks))]

            # Remove all previous chunks from the collection before upserting new ones
            # This ensures only the current page's context is present
            all_ids = collection.get()["ids"]
            if all_ids:
                collection.delete(ids=all_ids)

            # Store in ChromaDB
            collection.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=[{"url": url}]*len(chunks))
    except Exception as e:
        st.error(f"Failed to fetch or parse the webpage: {e}")

# Input for user question
if doc_content:
    question = st.text_input("Ask a question about the webpage:")
    if question:
        # Embed the question and search for relevant chunks
        q_embedding = embedder.encode([question])[0].tolist()
        results = collection.query(query_embeddings=[q_embedding], n_results=3)
        context = "\n".join(results["documents"][0]) if results["documents"] else doc_content[:4000]
        with st.spinner("Getting answer from Ollama..."):
            answer = ask_ollama(question, context)
        st.subheader("Answer:")
        st.write(answer)
