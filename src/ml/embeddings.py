import fitz  # PyMuPDF for extracting text from PDFs
import numpy as np
import faiss
from langchain_ollama import OllamaEmbeddings

# Initialize Ollama Embeddings
embedding_model = OllamaEmbeddings(model="llama3")

def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    doc = fitz.open(file_path)
    text = " ".join([page.get_text() for page in doc])
    return text

def chunk_text(text: str, chunk_size: int = 500) -> list:
    """Split text into smaller chunks for embedding."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def get_ollama_embeddings(texts: list) -> list[np.array]:
    """Generate embeddings using LangChain's OllamaEmbeddings."""
    return [np.array(embedding_model.embed_query(text)) for text in texts]

def store_embeddings(embeddings: list[np.array]):
    """Save embeddings in FAISS vector database."""
    d = len(embeddings[0])  # Embedding dimension
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))

    # Save FAISS index
    faiss.write_index(index, "ml/embeddings/faiss_index")

def embed_pdf(file_path: str):
    """Processes a PDF file, generates embeddings via Ollama, and stores them."""
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = get_ollama_embeddings(chunks)
    store_embeddings(embeddings)
    print(f"✅ Embeddings stored successfully for {file_path}")

# Example usage
if __name__ == "__main__":
    embed_pdf("data/sample_chapter.pdf")
