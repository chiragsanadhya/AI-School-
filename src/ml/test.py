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

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Groq API Client
groq_client = groq.Client(api_key=GROQ_API_KEY)

def generate_embedding(text):
    """Generate embedding using Ollama"""
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]  # Returns a list of floats (vector)

def fetch_relevant_text(query, top_k=3):
    """Retrieve relevant text chunks from Supabase using vector search"""
    query_embedding = generate_embedding(query)  # Convert text to vector

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,  # Use embeddings
        "match_threshold": 0.50,
        "match_count": top_k
    }).execute()
    
    if not response.data:
        print("No relevant data found!")
        return ""

    return " ".join(item["content"] for item in response.data)

def generate_mcqs(context, num_questions=5):
    """Generate multiple-choice questions using Groq"""
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

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def main():
    """Main function to run the MCQ generator"""
    topic = input("Enter the topic for generating MCQs: ")
    
    # Fetch relevant text from Supabase
    context = fetch_relevant_text(topic)

    if not context:
        print("Could not generate questions due to insufficient data.")
        return

    # Generate MCQs using Groq
    mcqs = generate_mcqs(context)
    print("\nGenerated MCQs:\n", mcqs)

if __name__ == "__main__":
    main()
