import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
MODEL = "gemini-2.5-flash"
SPEECH_MODEL = "gemini-2.5-flash-preview-tts"
PROMPT_FILE ="PromptCounter.json"
