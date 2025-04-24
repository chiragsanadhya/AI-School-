from src.ml.rag import RAGChatbot
from src.ml.narration import TextProcessor, Narrator
from src.ml.test import MCQGenerator
from src.core.config import settings
from src.services.rag_service import RAGService
from src.services.narration_service import NarrationService
from src.services.mcq_service import MCQService

class MLService:
    def __init__(self):
        self.rag_chatbot = RAGChatbot()
        self.text_processor = TextProcessor(api_key=settings.GROQ_API_KEY)
        self.narrator = Narrator()
        self.mcq_generator = MCQGenerator(api_key=settings.GROQ_API_KEY)
        self.rag_service = RAGService()
        self.narration_service = NarrationService()
        self.mcq_service = MCQService()
    
    def get_explanation(self, text: str) -> str:
        return self.text_processor.transform(text)
    
    def generate_narration(self, text: str):
        return self.narrator.narrate(text)
    
    def chat_with_context(self, message: str) -> str:
        return self.rag_chatbot.chat(message)
    
    def generate_questions(self, context: str, num_questions: int = 5) -> str:
        return self.mcq_generator.generate_mcqs(context, num_questions)