import os
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from TTS.api import TTS

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def transform_text(text):
    """
    Uses Groq's Llama3-8B model to generate an explanation.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"Explain in simple terms: {text}"}],
    )
    return response.choices[0].message.content

def narrate_text(text):
    """
    Generates speech from the given text and plays it in real-time.
    """
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to("cpu")
    wav = tts.tts(text=text)
    sd.play(np.array(wav), samplerate=22050)
    sd.wait()

# Example usage
selected_text = "Machine learning is a branch of artificial intelligence."
transformed_text = transform_text(selected_text)  # Get explanation from LLM
narrate_text(transformed_text)  # Speak the explanation
