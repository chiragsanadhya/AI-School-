# Steps for Creating narration.py



# 1. Set Up Environment Variables

# Add the following keys to .env:
# GROQ_API_KEY for using Groq LLM.
# Ensure Ollama is running locally if embeddings are needed.



# 2. Import Required Libraries

# os and dotenv to manage environment variables.
# sounddevice and numpy to handle audio playback.
# TTS from Coqui TTS for text-to-speech conversion.
# Groq to interact with the Llama3 model.



# 3. Initialize Required Components

# Load API Keys from .env.
# Initialize Groq LLM with Groq(api_key=GROQ_API_KEY).
# Load the TTS Model (tts_models/en/ljspeech/tacotron2-DDC).



# 4. Generate Transformed Narration (LLM Processing)

# Define transform_text(text: str):
# Uses Groq’s Llama3-8B model.
# Creates a prompt: "Explain in simple terms: {text}".
# Sends the prompt to the Groq API and retrieves the explanation.



# 5. Convert Transformed Text to Speech

# Define narrate_text(text: str):
# Loads Tacotron2-DDC TTS model.
# Generates speech from the input text.
# Uses sounddevice to play the generated audio in real time.



# 6. Debugging and Issues Faced

# Real-Time Streaming Issue:
# Initially, TTS generated audio but didn’t play smoothly.
# Resolved by adjusting the sampling rate and using sounddevice.wait().
# TTS Model Loading Delay:
# Loading the TTS model took time, so it was optimized to initialize only once.
# Groq API Response Delay:
# Some prompts took longer to process; optimized by simplifying the LLM query.


# 7. Execution and Testing

# Added an if __name__ == "__main__" block to:
# Accept user input.
# Transform the text using transform_text(text).
# Convert and play the narration using narrate_text(text).














import os
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from TTS.api import TTS

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class TextProcessor:
    """Handles text transformation using Groq's Llama3-8B model."""

    def __init__(self, api_key: str):
        """Initialize the Groq client."""
        self.client = Groq(api_key=api_key)

    def transform(self, text: str) -> str:
        """Uses Groq's Llama3-8B model to generate an explanation."""
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Explain in simple terms: {text}"}],
        )
        return response.choices[0].message.content

class Narrator:
    """Handles text-to-speech conversion and real-time audio playback."""

    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        """Initialize the TTS model."""
        self.tts = TTS(model_name).to("cpu")

    def narrate(self, text: str):
        """Generates speech from text and plays it in real-time."""
        wav = self.tts.tts(text=text)
        sd.play(np.array(wav), samplerate=22050)
        sd.wait()

# Example usage
if __name__ == "__main__":
    text_processor = TextProcessor(api_key=GROQ_API_KEY)
    narrator = Narrator()

    selected_text = "Machine learning is a branch of artificial intelligence."
    transformed_text = text_processor.transform(selected_text)  # Get explanation from LLM
    narrator.narrate(transformed_text)  # Speak the explanation














