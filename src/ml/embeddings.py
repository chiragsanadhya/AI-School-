# Steps for Creating embeddings.py
# 1. Set Up Environment Variables

# Add Supabase keys (SUPABASE_URL, SUPABASE_KEY) to the .env file.
# Ensure Ollama is installed and running locally to generate embeddings.



# 2. Import Required Libraries

# fitz (PyMuPDF) for extracting text from PDFs.
# numpy for handling numerical operations.
# os and dotenv for loading environment variables.
# OllamaEmbeddings for generating embeddings using Ollama.
# SupabaseVectorStore for storing embeddings in Supabase.
# Document from langchain_core.documents to structure text for vector storage.
# supabase.create_client to connect to the Supabase database.



# 3. Initialize Supabase and Ollama

# Use create_client(SUPABASE_URL, SUPABASE_KEY) to connect to Supabase.
# Initialize OllamaEmbeddings(model="nomic-embed-text") to use Ollama locally.
# Set up SupabaseVectorStore with Supabase client and embeddings.



# 4. Load and Process PDF

# Define load_pdf(file_path) to extract text from a PDF using fitz.open(file_path).
# Define chunk_text(text, chunk_size=500) to split text into smaller parts for embedding.



# 5. Generate and Store Embeddings

# Define embed_pdf(file_path):
# Extract text from the PDF.
# Chunk the text.
# Convert chunks into Document objects.
# Store embeddings in Supabase using vector_store.add_documents(docs).



# 6. Debugging and Issues Faced

# Match-making in Supabase: Initially, Supabase similarity search did not return results correctly due to missing embeddings or incorrect table schema. Fixed by ensuring embeddings were stored properly and indexing was enabled.
# Ollama Performance: Needed to ensure Ollama was running locally before embedding generation.
# Chunking Optimization: Experimented with different chunk sizes (default: 500 words) to balance embedding quality and storage efficiency.



# 7. Execution and Testing

# Added an if __name__ == "__main__" block to call embed_pdf() with a sample PDF path.
# Tested storing and retrieving embeddings from Supabase.


































import fitz  
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

class PDFEmbedder:
    def __init__(self):
        """Initialize Supabase client, embedding model, and vector store."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        # Initialize Supabase Client
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

        # Initialize Ollama Embeddings (Local)
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")

        # Initialize Supabase Vector Store
        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            table_name="documents",  # Ensure this table exists in Supabase
            embedding=self.embedding_model
        )

    def load_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        doc = fitz.open(file_path)
        text = " ".join([page.get_text() for page in doc])
        return text

    def chunk_text(self, text: str, chunk_size: int = 500) -> list:
        """Split text into smaller chunks for embedding."""
        words = text.split()
        return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    def embed_pdf(self, file_path: str):
        """Processes a PDF file, generates embeddings via Ollama, and stores them in Supabase."""
        text = self.load_pdf(file_path)
        chunks = self.chunk_text(text)
        
        # Convert text chunks into LangChain Document objects
        docs = [Document(page_content=chunk) for chunk in chunks]
        
        # Store embeddings in Supabase Vector Store
        self.vector_store.add_documents(docs)
        
        print(f"Embeddings stored for {file_path}")

# Example usage
if __name__ == "__main__":
    embedder = PDFEmbedder()
    embedder.embed_pdf("/Users/chira/Desktop/NECESSITY/projects/AI_School/data/NCERT-Class-9-English-The-Bond-of-Love.pdf")














# import fitz  
# import numpy as np
# import os
# from dotenv import load_dotenv
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import SupabaseVectorStore
# from langchain_core.documents import Document
# from supabase import create_client, Client

# # Load environment variables from .env file
# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# # Initialize Supabase Client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Initialize Ollama Embeddings (Local)
# embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# # Initialize Supabase Vector Store
# vector_store = SupabaseVectorStore(
#     client=supabase,
#     table_name="documents",  # Ensure this table exists in Supabase
#     embedding=embedding_model
# )

# def load_pdf(file_path: str) -> str:
#     """Extract text from a PDF file."""
#     doc = fitz.open(file_path)
#     text = " ".join([page.get_text() for page in doc])
#     return text

# def chunk_text(text: str, chunk_size: int = 500) -> list:
#     """Split text into smaller chunks for embedding."""
#     words = text.split()
#     return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# def embed_pdf(file_path: str):
#     """Processes a PDF file, generates embeddings via Ollama, and stores them in Supabase."""
#     text = load_pdf(file_path)
#     chunks = chunk_text(text)
    
#     # Convert text chunks into LangChain Document objects
#     docs = [Document(page_content=chunk) for chunk in chunks]
    
#     # Store embeddings in Supabase Vector Store
#     vector_store.add_documents(docs)
    
#     print(f" Embeddings stored for {file_path}")

# # Example usage
# if __name__ == "__main__":
#     embed_pdf("/Users/chira/Desktop/NECESSITY/projects/AI_School/data/NCERT-Class-9-English-The-Bond-of-Love.pdf")
