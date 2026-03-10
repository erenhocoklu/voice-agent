from stt_agent.stt import listen
from google import genai
from google.genai import types
from tts_agent.tts import speak

from config import GEMINI_API_KEY, MODEL
from app_contents import SYSTEM_PROMPT, GREETING_PROMPT
from utils.display import C, print_banner, print_menu
from utils.prompt_counter import load_balance, save_balance, print_prompt_stats




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
    speak(reply)
    print_prompt_stats(prompt_count)

    while True:
        try:
            user_input = listen()
            print(f"{C.YELLOW}{C.BOLD}You: {C.RESET}{user_input}")

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
            speak(reply)

            print_prompt_stats(prompt_count)

        except Exception as e:
            print(f"\n{C.RED}Error talking to Gemini: {e}{C.RESET}\n")
            print("Make sure your GEMINI_API_KEY is set correctly.\n")
