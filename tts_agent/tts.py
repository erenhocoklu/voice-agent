from elevenlabs.client import ElevenLabs
from elevenlabs import play
from config import ELEVENLABS_API_KEY
from utils.audio import play_audio

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak(text: str):
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="ar3cDO5c2SkHYO5joTRA",
        model_id="eleven_multilingual_v2",
        output_format="pcm_24000",
        )
    audio_data = b"".join(audio_stream)
    play_audio(audio_data)
