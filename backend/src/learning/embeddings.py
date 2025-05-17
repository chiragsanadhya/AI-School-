import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client, Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class PDFEmbedder:
    def __init__(self):
        # Initialize Supabase client
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL", ""),
            os.getenv("SUPABASE_KEY", "")
        )
        
        # Initialize Ollama embeddings
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        
        # Initialize vector store
        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            embedding=self.embeddings,
            table_name="document_embeddings",
            query_name="match_documents"
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise

    def create_chunks(self, text: str) -> List[str]:
        """Split text into chunks."""
        try:
            chunks = self.text_splitter.split_text(text)
            return chunks
        except Exception as e:
            logger.error(f"Error creating chunks: {str(e)}")
            raise

    async def process_pdf(self, pdf_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process PDF file and store embeddings in Supabase."""
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Create chunks
            chunks = self.create_chunks(text)
            
            # Prepare metadata for each chunk
            chunk_metadata = []
            for i, chunk in enumerate(chunks):
                chunk_meta = {
                    "chunk_id": i,
                    "source": pdf_path.name,
                    "chunk_index": i,
                    **(metadata or {})
                }
                chunk_metadata.append(chunk_meta)
            
            # Store in vector database
            self.vector_store.add_texts(
                texts=chunks,
                metadatas=chunk_metadata
            )
            
            return {
                "status": "success",
                "chunks": len(chunks),
                "message": f"Successfully processed PDF: {pdf_path.name}"
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise

    async def search_similar_chunks(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity."""
        try:
            results = self.vector_store.similarity_search_with_score(
                query,
                k=k
            )
            
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in results
            ]
        except Exception as e:
            logger.error(f"Error searching similar chunks: {str(e)}")
            raise 