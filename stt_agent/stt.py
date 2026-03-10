import sounddevice as sd
import numpy as np
import tempfile
import os

from utils.display import C
from scipy.io.wavfile import write
from faster_whisper import WhisperModel



SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.1 # HOW QUIET SOUNDS AS SILENCE
SILENCE_DURATION = 0.5 # SECONDS OF SILENCE BEFORE STOPPING

model = WhisperModel("small", device="cpu", compute_type="int8")

def listen() -> str:
    """Record audio untill silence is detected. Then implement whisper"""
    print("Listening...")

    recorded_chunks = [] # collects chunks of audio
    silent_chunks = 0 # counts how many consecutive silent chunks received
    chunk_size = 1024
    silence_limit = int(SAMPLE_RATE * SILENCE_DURATION / chunk_size)

    def callback(indata, frames, time, status): # runs automatically everytime a new chunk of audio arrives from the microphone
        volume = np.linalg.norm(indata) # calculates the volume of a chunk mathematically
        recorded_chunks.append(indata.copy()) # saves a copy of the current chunk so it doesnt get overwritten

        nonlocal silent_chunks # we want to manipulate chunks outside of this function
        if volume < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

    with sd.InputStream(samplerate=SAMPLE_RATE, blocksize=chunk_size, callback=callback, channels=1): # channels=1 since 1 audio is taken,
    # callback tells sounddevice to callback everytime a chunk arrives
    # sd.InputStrea opens the microphone from our settings
        while silent_chunks < silence_limit:
            sd.sleep(100)

    print("Processing...")

    audio_data = np.concatenate(recorded_chunks, axis = 0) # recorded chunks is a list of many small arrays np.concatenate combines them
    # axis = 0 means add them end to end vertically

    with tempfile.NamedTemporaryFile(suffix=".wav",delete = False) as f:
        temp_path = f.name # gets the path to a file "in this case audio file i guess?"
        write(temp_path, SAMPLE_RATE, audio_data) # saves the audio array as a proper wav file whisper can read.

    segments, _ = model.transcribe(temp_path, language="tr") # tells whisper to expect turkish, improves accuracy significantly
    os.unlink(temp_path) # deletes the temp file

    text = " ".join(segment.text for segment in segments).strip()
    print(f"you said: {C.YELLOW}{text}{C.RESET}")
    return text


