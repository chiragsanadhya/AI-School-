from src.ml.rag import RAGChatbot
from src.ml.narration import TextProcessor, Narrator
from src.ml.test import MCQGenerator

class MLService:
    def __init__(self):
        self.rag_chatbot = RAGChatbot()
        self.text_processor = TextProcessor(api_key=settings.GROQ_API_KEY)
        self.narrator = Narrator()
        self.mcq_generator = MCQGenerator(api_key=settings.GROQ_API_KEY)