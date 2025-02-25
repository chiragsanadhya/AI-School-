import os
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGChatbot:
    """A Retrieval-Augmented Generation (RAG) chatbot using Supabase, Ollama, and Groq."""

    def __init__(self, k=5):
        """Initialize Supabase client, embedding model, vector store, and LLM."""
        self.k = k  # Number of relevant chunks to retrieve

        # Supabase Credentials
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        # Groq API Key
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        # Create Supabase client
        self.supabase_client = create_client(self.supabase_url, self.supabase_key)

        # Initialize Ollama Embedding Model (Same model used for document embeddings)
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")

        # Connect to Supabase Vector Store
        self.vector_store = SupabaseVectorStore(
            client=self.supabase_client,
            embedding=self.embedding_model,  # Ensure queries are converted into embeddings
            table_name="documents"
        )

        # Initialize Groq LLM
        self.llm = ChatGroq(model_name="llama3-8b-8192", api_key=self.groq_api_key)

        # RAG Prompt Template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="You are an AI assistant. Use the following context to answer the question.\n\n"
                     "Context:\n{context}\n\n"
                     "Question: {question}\n\n"
                     "Answer:"
        )

    def get_relevant_chunks(self, query: str):
        """Retrieves relevant stored embeddings from Supabase based on user query."""
        # ✅ Convert query to embedding
        query_embedding = self.embedding_model.embed_query(query)
        
        if not query_embedding:
            print("⚠️ Query embedding is empty. Check embedding model.")
            return []
        
        # ✅ Perform similarity search in Supabase
        results = self.vector_store.similarity_search_by_vector(query_embedding, k=self.k)
        
        if not results:
            print("⚠️ No relevant documents found in vector database.")
            return []
        
        # ✅ Print retrieved document chunks (for debugging)
        print(f"\n📄 Retrieved {len(results)} relevant document(s):")
        for i, doc in enumerate(results):
            print(f"{i+1}. {doc.page_content[:200]} ...")  # Show first 200 chars
        
        return results

    def chat(self, query: str):
        """Fetches relevant context and generates an answer using Groq LLM."""
        # ✅ Retrieve relevant document chunks
        context_docs = self.get_relevant_chunks(query)
        
        if not context_docs:
            return "Sorry, I couldn't find relevant information."

        # ✅ Format retrieved context
        context = "\n\n".join([doc.page_content for doc in context_docs])

        # ✅ Create LLM prompt
        prompt = self.prompt_template.format(context=context, question=query)
        
        print("\n📝 Final Prompt to LLM:")
        print(prompt[:500] + "...")  # Print first 500 characters

        # ✅ Generate response using Groq LLM
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return "An error occurred while generating the response."

# Example usage
if __name__ == "__main__":
    chatbot = RAGChatbot()
    question = input("\nAsk a question: ")
    answer = chatbot.chat(question)
    print("\n🤖 AI Answer:", answer)
















# import os
# from langchain_community.vectorstores import SupabaseVectorStore
# from langchain_groq import ChatGroq
# from langchain_ollama import OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate
# from supabase import create_client
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Supabase Credentials
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# # Groq API Key
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Create Supabase client
# supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Initialize Ollama Embedding Model (Same model used for document embeddings)
# embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# # Connect to Supabase Vector Store
# vector_store = SupabaseVectorStore(
#     client=supabase_client,
#     embedding=embedding_model,  # Ensure queries are converted into embeddings
#     table_name="documents"
# )

# # Initialize Groq LLM
# llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)

# # RAG Prompt Template
# prompt_template = PromptTemplate(
#     input_variables=["context", "question"],
#     template="You are an AI assistant. Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
# )

# def get_relevant_chunks(query: str, k=5):
#     """Retrieves relevant stored embeddings from Supabase based on user query."""
    
#     # ✅ Convert query to embedding
#     query_embedding = embedding_model.embed_query(query)
    
#     if not query_embedding:
#         print("⚠️ Query embedding is empty. Check embedding model.")
#         return []
    
    

#     # ✅ Perform similarity search in Supabase
#     results = vector_store.similarity_search_by_vector(query_embedding, k=k)
    
#     if not results:
#         print("⚠️ No relevant documents found in vector database.")
#         return []
    
#     # ✅ Print retrieved document chunks (for debugging)
#     print(f"\n📄 Retrieved {len(results)} relevant document(s):")
#     for i, doc in enumerate(results):
#         print(f"{i+1}. {doc.page_content[:200]} ...")  # Show first 200 chars
    
#     return results

# def chat_with_rag(query: str):
#     """Fetches relevant context and generates an answer using Groq LLM."""
    
#     # ✅ Retrieve relevant document chunks
#     context_docs = get_relevant_chunks(query)
    
#     if not context_docs:
#         return "Sorry, I couldn't find relevant information."

#     # ✅ Format retrieved context
#     context = "\n\n".join([doc.page_content for doc in context_docs])

#     # ✅ Create LLM prompt
#     prompt = prompt_template.format(context=context, question=query)
    
#     print("\n📝 Final Prompt to LLM:")
#     print(prompt[:500] + "...")  # Print first 500 characters

#     # ✅ Generate response using Groq LLM
#     try:
#         response = llm.invoke(prompt)
#         return response
#     except Exception as e:
#         print(f"❌ LLM Error: {e}")
#         return "An error occurred while generating the response."

# # Example usage
# if __name__ == "__main__":
#     question = input("\nAsk a question: ")
#     answer = chat_with_rag(question)
#     print("\n🤖 AI Answer:", answer)
