# Steps for Creating rag.py
# 1. Set Up Environment Variables

# Add the following keys to .env:
# SUPABASE_URL and SUPABASE_KEY for Supabase connection.
# GROQ_API_KEY for Groq LLM API access.
# Ensure Ollama is running locally for embedding generation.




# 2. Import Required Libraries

# os and dotenv for environment variable management.
# SupabaseVectorStore for storing and retrieving embeddings.
# OllamaEmbeddings for generating embeddings.
# ChatGroq for interacting with the Groq LLM.
# PromptTemplate from langchain_core.prompts for structuring LLM queries.
# supabase.create_client to connect to the Supabase database.




# 3. Initialize Required Components

# Connect to Supabase using create_client(SUPABASE_URL, SUPABASE_KEY).
# Initialize Ollama for embedding generation using OllamaEmbeddings(model="nomic-embed-text").
# Set Up Supabase Vector Store to store embeddings and enable retrieval.
# Initialize Groq LLM with ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY).
# Define a RAG Prompt Template to structure the input for the LLM.




# 4. Retrieve Relevant Chunks from Supabase

# Define get_relevant_chunks(query: str, k=5):
# Convert the query into an embedding using embedding_model.embed_query(query).
# Perform a similarity search in Supabase using vector_store.similarity_search_by_vector(query_embedding, k=k).
# Return retrieved document chunks.



# 5. Generate Responses Using RAG

# Define chat_with_rag(query: str):
# Fetch relevant context using get_relevant_chunks(query).
# If no relevant context is found, return a fallback message.
# Format the retrieved context into a structured prompt.
# Send the prompt to Groq LLM for response generation.
# Return the generated response.




# 6. Debugging and Issues Faced

# Match-making in Supabase: Initially, the vector search didn't return relevant results due to missing or incorrectly stored embeddings. Resolved by ensuring embeddings were stored properly.
# Embedding Mismatch: The query embedding format had to match the stored document embeddings for effective similarity search.
# Groq LLM Response Format: Needed to ensure that the LLM prompt was structured correctly to provide accurate and context-aware answers.





# 7. Execution and Testing

# Added an if __name__ == "__main__" block to:
# Accept user input for a query.
# Call chat_with_rag(query).
# Print the response.































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


















