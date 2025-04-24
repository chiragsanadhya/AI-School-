from TTS.api import TTS
import sounddevice as sd
import numpy as np
from src.core.config import settings

class NarrationService:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        
    def narrate(self, text: str):
        try:
            wav = self.tts.tts(text=text)
            sd.play(np.array(wav), samplerate=22050)
            sd.wait()
            return True
        except Exception as e:
            print(f"Narration error: {e}")
            return False