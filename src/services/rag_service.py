from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama

class RAGService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = None
        self.chain = None
        
    def initialize_knowledge_base(self, texts: list[str]):
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOllama(model="llama2"),
            retriever=self.vector_store.as_retriever()
        )
    
    def get_response(self, query: str) -> str:
        if not self.chain:
            return "Knowledge base not initialized"
        response = self.chain({"question": query})
        return response["answer"]