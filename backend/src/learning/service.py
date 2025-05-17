import logging
from typing import Dict, Any, List
from pathlib import Path
from .embeddings import PDFEmbedder
from .narration import Narrator
from .rag import RAGChatbot
from .test_generation import TestGenerator

logger = logging.getLogger(__name__)

class LearningService:
    def __init__(self):
        self.embedder = PDFEmbedder()
        self.narrator = Narrator()
        self.rag = RAGChatbot()
        self.test_generator = TestGenerator()

    async def process_chapter(self, pdf_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a new chapter PDF and prepare it for all learning features."""
        try:
            # Process PDF and store embeddings
            result = await self.embedder.process_pdf(pdf_path, metadata)
            return result
        except Exception as e:
            logger.error(f"Error processing chapter: {str(e)}")
            raise

    async def get_chapter_answer(self, question: str, chapter_id: str) -> Dict[str, Any]:
        """Get answer for a question about a specific chapter."""
        try:
            # Add chapter context to the question
            context_question = f"Regarding chapter {chapter_id}: {question}"
            result = await self.rag.ask_question(context_question)
            return result
        except Exception as e:
            logger.error(f"Error getting chapter answer: {str(e)}")
            raise

    async def explain_text(self, text: str, save_audio: bool = False) -> Dict[str, Any]:
        """Generate explanation and optionally convert to speech."""
        try:
            result = await self.narrator.narrate_text(text, save_to_file=save_audio)
            return result
        except Exception as e:
            logger.error(f"Error explaining text: {str(e)}")
            raise

    async def generate_test(self, chapter_id: str, num_questions: int = 5) -> Dict[str, Any]:
        """Generate a test for a specific chapter."""
        try:
            result = await self.test_generator.generate_chapter_test(chapter_id, num_questions)
            return result
        except Exception as e:
            logger.error(f"Error generating test: {str(e)}")
            raise

    async def validate_test_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Validate a user's answer to a test question."""
        try:
            result = await self.test_generator.validate_answer(question, user_answer)
            return result
        except Exception as e:
            logger.error(f"Error validating answer: {str(e)}")
            raise

    async def search_chapter_content(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant content across chapters."""
        try:
            results = await self.embedder.search_similar_chunks(query, k)
            return results
        except Exception as e:
            logger.error(f"Error searching chapter content: {str(e)}")
            raise
