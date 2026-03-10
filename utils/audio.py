import sounddevice as sd
import numpy as np

def play_audio(audio_data: bytes, samplerate: int = 24000):
    """Convert raw audio bytes and play them through speakers."""
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    sd.play(audio_array, samplerate=samplerate)
    sd.wait()