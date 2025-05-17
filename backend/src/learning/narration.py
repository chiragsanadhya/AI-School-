import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np
from groq import Groq
from TTS.api import TTS
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Narrator:
    def __init__(self):
        # Initialize Groq client
        self.groq_client = Groq(
            api_key=os.getenv("GROQ_API_KEY", "")
        )
        
        # Initialize TTS
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        
        # Audio settings
        self.sample_rate = 22050  # TTS default sample rate

    async def generate_explanation(self, text: str) -> str:
        """Generate a simplified explanation using Groq's Llama3-8B."""
        try:
            prompt = f"""Please explain the following text in a clear and educational way, 
            suitable for students. Keep the explanation concise and easy to understand:

            Text: {text}

            Explanation:"""
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant that explains concepts clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            raise

    async def text_to_speech(self, text: str, output_path: Optional[Path] = None) -> str:
        """Convert text to speech and optionally save to file."""
        try:
            if output_path:
                # Generate and save audio file
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_path)
                )
                return str(output_path)
            else:
                # Generate audio in memory
                audio = self.tts.tts(text=text)
                return audio
                
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            raise

    async def play_audio(self, audio_data: np.ndarray):
        """Play audio data using sounddevice."""
        try:
            sd.play(audio_data, self.sample_rate)
            sd.wait()  # Wait until audio is finished playing
        except Exception as e:
            logger.error(f"Error playing audio: {str(e)}")
            raise

    async def narrate_text(self, text: str, save_to_file: bool = False) -> Dict[str, Any]:
        """Complete narration pipeline: explain text and convert to speech."""
        try:
            # Generate explanation
            explanation = await self.generate_explanation(text)
            
            if save_to_file:
                # Save to file
                output_path = Path("uploads/audio") / f"narration_{hash(text)}.mp3"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                audio_path = await self.text_to_speech(explanation, output_path)
                return {
                    "explanation": explanation,
                    "audio_path": audio_path
                }
            else:
                # Generate and play audio
                audio_data = await self.text_to_speech(explanation)
                await self.play_audio(audio_data)
                return {
                    "explanation": explanation,
                    "audio_played": True
                }
                
        except Exception as e:
            logger.error(f"Error in narration pipeline: {str(e)}")
            raise 