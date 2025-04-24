from groq import Groq
from src.core.config import settings
from langchain_community.chat_models import ChatOllama

class MCQService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        
    def generate_mcqs(self, context: str, num_questions: int = 5) -> list:
        prompt = self._create_mcq_prompt(context, num_questions)
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    def _create_mcq_prompt(self, context: str, num_questions: int) -> str:
        return f"""Generate {num_questions} multiple choice questions from this content:
        {context}
        Format each question as:
        Q: [Question]
        A) [Option]
        B) [Option]
        C) [Option]
        D) [Option]
        Correct: [Letter]"""

class MCQService:
    def __init__(self):
        self.client = ChatOllama(model="llama2")
        
    def generate_mcqs(self, context: str, num_questions: int = 5) -> str:
        prompt = self._create_mcq_prompt(context, num_questions)
        response = self.client.predict(prompt)
        return response
        
    def _create_mcq_prompt(self, context: str, num_questions: int) -> str:
        return f"""Generate {num_questions} multiple choice questions from this content:
        {context}
        Format each question as:
        Q: [Question]
        A) [Option]
        B) [Option]
        C) [Option]
        D) [Option]
        Correct: [Letter]"""