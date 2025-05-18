import os
import logging
import json
from typing import List, Dict, Any
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from supabase import create_client, Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TestGenerator:
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
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY", ""),
            model_name="llama3-8b-8192"
        )
        
        # Initialize MCQ generation prompt
        self.mcq_prompt = PromptTemplate(
            input_variables=["context", "num_questions"],
            template="""Generate {num_questions} multiple choice questions based on the following educational content.
            Each question should have 4 options (A, B, C, D) and one correct answer.
            The questions should test understanding of key concepts.
            Format the response as a JSON array of objects with the following structure:
            [
                {{
                    "question": "Question text",
                    "options": {{
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D"
                    }},
                    "correct_answer": "A/B/C/D",
                    "explanation": "Brief explanation of why this is the correct answer"
                }}
            ]

            Content:
            {context}

            Questions:"""
        )
        
        # Initialize MCQ generation chain
        self.mcq_chain = LLMChain(
            llm=self.llm,
            prompt=self.mcq_prompt
        )

    async def get_chapter_content(self, chapter_id: str, k: int = 5) -> str:
        """Retrieve relevant content for a chapter."""
        try:
            # Search for chapter content
            docs = self.vector_store.similarity_search(
                f"chapter {chapter_id}",
                k=k
            )
            
            # Combine document contents
            content = "\n\n".join([doc.page_content for doc in docs])
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving chapter content: {str(e)}")
            raise

    async def generate_mcqs(self, content: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate MCQs using LLM."""
        try:
            # Generate MCQs using chain
            response = self.mcq_chain.run(
                context=content,
                num_questions=num_questions
            )
            
            # Parse JSON response
            try:
                questions = json.loads(response)
                return questions
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing MCQ response: {str(e)}")
                # Try to extract JSON from the response if it's wrapped in markdown or other text
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    questions = json.loads(json_match.group())
                    return questions
                raise
                
        except Exception as e:
            logger.error(f"Error generating MCQs: {str(e)}")
            raise

    async def generate_chapter_test(self, chapter_id: str, num_questions: int = 5) -> Dict[str, Any]:
        """Complete test generation pipeline for a chapter."""
        try:
            # Get chapter content
            content = await self.get_chapter_content(chapter_id)
            
            # Generate MCQs
            questions = await self.generate_mcqs(content, num_questions)
            
            return {
                "chapter_id": chapter_id,
                "questions": questions,
                "total_questions": len(questions)
            }
            
        except Exception as e:
            logger.error(f"Error in test generation pipeline: {str(e)}")
            raise

    async def validate_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Validate a user's answer to a question."""
        try:
            is_correct = user_answer.upper() == question["correct_answer"]
            return {
                "is_correct": is_correct,
                "correct_answer": question["correct_answer"],
                "explanation": question["explanation"]
            }
        except Exception as e:
            logger.error(f"Error validating answer: {str(e)}")
            raise 