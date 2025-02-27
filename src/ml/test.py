# Purpose:
# Handles generating MCQs (Multiple-Choice Questions) using Groq LLM and fetching relevant text from Supabase.

# Steps in Creation:
# 1. Set Up Environment Variables

# Add the following keys to .env:
# SUPABASE_URL and SUPABASE_KEY for database access.
# GROQ_API_KEY for using Groq's Llama3 model.
# 2. Import Required Libraries

# os and dotenv for environment management.
# supabase for database queries.
# groq for LLM processing.
# numpy and ollama for embeddings.
# 3. Initialize Clients

# Supabase Client to query vector embeddings.
# Groq API Client for LLM-based question generation.
# 4. Generate Embeddings for Queries

# Define generate_embedding(text: str):
# Uses Ollama locally (nomic-embed-text model).
# Returns a list of floats as the embedding.
# 5. Retrieve Relevant Context from Supabase

# Define fetch_relevant_text(query, top_k=3):
# Converts the query into an embedding.
# Calls the match_documents function in Supabase to find similar vectors.
# Returns the most relevant document chunks.
# 6. Generate MCQs using Groq

# Define generate_mcqs(context, num_questions=5):
# Constructs a structured prompt for the LLM.
# Requests the LLM to generate formatted MCQs with 4 options and the correct answer.
# Returns the formatted question set.
# 7. Execution Flow

# Uses an input prompt to get the topic.
# Fetches relevant content from Supabase.
# Passes the content to the LLM to generate questions.
# Prints the output.
# Challenges Faced:
# Supabase Matchmaking Issue:
# The vector similarity search (match_documents) did not return relevant results initially.
# Adjusted match_threshold and match_count for better accuracy.
# Embedding Consistency:
# Used nomic-embed-text consistently to ensure stored embeddings match query embeddings.
# LLM Formatting Issues:
# The generated MCQs were sometimes unstructured.
# Fixed by enforcing a strict formatting structure in the prompt.













import os
from supabase import create_client, Client
import groq
from dotenv import load_dotenv
import numpy as np
import ollama

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class SupabaseHandler:
    """Handles Supabase interactions, including vector search."""

    def __init__(self, url: str, key: str):
        """Initialize Supabase client."""
        self.client: Client = create_client(url, key)

    def fetch_relevant_text(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant text chunks from Supabase using vector search."""
        query_embedding = EmbeddingGenerator.generate_embedding(query)  # Convert text to vector

        response = self.client.rpc("match_documents", {
            "query_embedding": query_embedding,  # Use embeddings
            "match_threshold": 0.50,
            "match_count": top_k
        }).execute()

        if not response.data:
            print("No relevant data found!")
            return ""

        return " ".join(item["content"] for item in response.data)


class EmbeddingGenerator:
    """Handles text embedding generation using Ollama."""

    @staticmethod
    def generate_embedding(text: str):
        """Generate embedding using Ollama."""
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]  # Returns a list of floats (vector)


class MCQGenerator:
    """Generates multiple-choice questions using Groq LLM."""

    def __init__(self, api_key: str):
        """Initialize Groq API client."""
        self.client = groq.Client(api_key=api_key)

    def generate_mcqs(self, context: str, num_questions: int = 5) -> str:
        """Generate MCQs based on the given context."""
        prompt = f"""
        You are an expert exam maker. Based on the given content, generate {num_questions} multiple-choice questions.
        Each question should have exactly 4 options, with only one correct answer. Format it as follows:

        1. Question text?
           A) Option 1
           B) Option 2
           C) Option 3
           D) Option 4
           Correct Answer: <Option Letter>

        Content:
        {context}
        """

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


def main():
    """Main function to run the MCQ generator."""
    topic = input("Enter the topic for generating MCQs: ")

    # Initialize handlers
    supabase_handler = SupabaseHandler(SUPABASE_URL, SUPABASE_KEY)
    mcq_generator = MCQGenerator(GROQ_API_KEY)

    # Fetch relevant text from Supabase
    context = supabase_handler.fetch_relevant_text(topic)

    if not context:
        print("Could not generate questions due to insufficient data.")
        return

    # Generate MCQs using Groq
    mcqs = mcq_generator.generate_mcqs(context)
    print("\nGenerated MCQs:\n", mcqs)


if __name__ == "__main__":
    main()











