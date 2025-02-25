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














# import os
# import sounddevice as sd
# import numpy as np
# from dotenv import load_dotenv
# from groq import Groq
# from TTS.api import TTS

# # Load environment variables
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Initialize Groq client
# client = Groq(api_key=GROQ_API_KEY)

# def transform_text(text):
#     """
#     Uses Groq's Llama3-8B model to generate an explanation.
#     """
#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[{"role": "user", "content": f"Explain in simple terms: {text}"}],
#     )
#     return response.choices[0].message.content

# def narrate_text(text):
#     """
#     Generates speech from the given text and plays it in real-time.
#     """
#     tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to("cpu")
#     wav = tts.tts(text=text)
#     sd.play(np.array(wav), samplerate=22050)
#     sd.wait()

# # Example usage
# selected_text = "Machine learning is a branch of artificial intelligence."
# transformed_text = transform_text(selected_text)  # Get explanation from LLM
# narrate_text(transformed_text)  # Speak the explanation
