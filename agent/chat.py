import sounddevice as sd
import numpy as np

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, MODEL, SPEECH_MODEL
from app_contents import SYSTEM_PROMPT, GREETING_PROMPT
from utils.display import C, print_banner, print_menu
from utils.prompt_counter import load_balance, save_balance, print_prompt_stats


def speak(text: str, client):
    # the gemini client object for perhaps changing it in the future

    response = client.models.generate_content(
        model=SPEECH_MODEL,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(   voice_config=types.VoiceConfig(   prebuilt_voice_config=types.PrebuiltVoiceConfig(  voice_name="Charon"  )))
        ),
        contents=text,
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data
    audio_array = np.frombuffer(audio_data, dtype=np.int16) # we need this to convert raw audip bytes into numpy 16 bit array so it can play the thing

    sd.play(audio_array, samplerate = 24000)
    sd.wait()

def run():
    prompt_count = load_balance()
    print_banner()

    # Init Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    history = []


    def send(message):
        nonlocal prompt_count


        history.append(types.Content(role="user", parts=[types.Part(text=message)]))
        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=history,
        )
        reply = response.text
        history.append(types.Content(role="model", parts=[types.Part(text=reply)]))

        prompt_count -= 1
        save_balance(prompt_count)

        return reply

    # Greeting
    reply = send(GREETING_PROMPT)
    print(f"\n{C.GREEN}{C.BOLD}QuickBite:{C.RESET} {reply}\n")
    speak(reply, client)
    print_prompt_stats(prompt_count)

    while True:
        try:
            user_input = input(f"{C.YELLOW}{C.BOLD}You:{C.RESET} ").strip()

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{C.DIM}Session ended. Goodbye!{C.RESET}\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print(f"\n{C.DIM}Thanks for visiting QuickBite! 👋{C.RESET}\n")
            break

        if user_input.lower() == "menu":
            print_menu()
            continue

        # Send to Gemini
        try:
            reply = send(user_input)
            print(f"\n{C.GREEN}{C.BOLD}QuickBite:{C.RESET} {reply}\n")
            speak(reply, client)

            print_prompt_stats(prompt_count)

        except Exception as e:
            print(f"\n{C.RED}Error talking to Gemini: {e}{C.RESET}\n")
            print("Make sure your GEMINI_API_KEY is set correctly.\n")
