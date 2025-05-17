import os
import logging
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.llms import Groq
from supabase import create_client, Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RAGChatbot:
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
        
        # Initialize Groq LLM
        self.llm = Groq(
            api_key=os.getenv("GROQ_API_KEY", ""),
            model_name="llama3-8b-8192"
        )
        
        # Initialize prompt template
        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful educational assistant. Use the following context to answer the question.
            If you cannot find the answer in the context, say so. Keep your answers clear and concise.

            Context:
            {context}

            Question: {question}

            Answer:"""
        )
        
        # Initialize QA chain
        self.qa_chain = LLMChain(
            llm=self.llm,
            prompt=self.qa_prompt
        )

    async def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from vector store."""
        try:
            # Search for relevant documents
            docs = self.vector_store.similarity_search(
                query,
                k=k
            )
            
            # Combine document contents
            context = "\n\n".join([doc.page_content for doc in docs])
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise

    async def generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM with context."""
        try:
            # Generate answer using QA chain
            response = self.qa_chain.run(
                context=context,
                question=question
            )
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    async def ask_question(self, question: str, k: int = 3) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve context and generate answer."""
        try:
            # Get relevant context
            context = await self.get_relevant_context(question, k)
            
            # Generate answer
            answer = await self.generate_answer(question, context)
            
            return {
                "answer": answer,
                "context": context,
                "sources": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in self.vector_store.similarity_search(question, k=k)
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise 