"""
Fast Food Order CLI — powered by Google Gemini
Usage:
    pip install google-generativeai
    export GEMINI_API_KEY=your_key_here
    python order_cli.py
"""

import os
import json

from google import genai
from google.genai import types

# ── Config ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDlZIbgKsuDtf71TNPh4EzFFSsXrl9ZXgU")
MODEL = "gemini-2.5-flash"
PROMT_FILE ="PromtCounter.json"

MENU = """
BURGERS
  Classic Burger        $5.99
  Double Smash Burger   $7.99
  Crispy Chicken Burger $6.99
  Veggie Burger         $5.49

SIDES
  French Fries (S/M/L)  $1.99 / $2.49 / $2.99
  Onion Rings           $2.99
  Coleslaw              $1.49

DRINKS
  Cola / Diet Cola      $1.49
  Lemonade              $1.99
  Water                 $0.99
  Milkshake (Choc/Vanilla/Strawberry) $3.49

EXTRAS
  Add Cheese            $0.50
  Add Bacon             $0.75
  Extra Sauce           $0.25
"""

SYSTEM_PROMPT = f"""
You are a friendly and efficient order-taker at a fast food restaurant called QuickBite.
Your job is to take the customer's food order in a natural, conversational way. Always respond in Turkish, no matter what language the customer speaks.



MENU:
{MENU}

GUIDELINES:
- Greet the customer warmly at the start.
- Help them navigate the menu if they ask.
- Confirm items as they order (e.g. "Got it — one Classic Burger!").
- Ask if they want anything else after each item.
- When the customer is done, read back the full order clearly with the total price.
- Ask for dine-in or takeaway.
- End with a friendly closing message and an order number (make one up, e.g. #042).
- Keep responses concise — this is a quick-service restaurant, not fine dining.
- If someone asks for something not on the menu, politely say it's not available and suggest alternatives.
- Do NOT make up prices. Only use prices listed in the menu above.
- Track the running order internally and always know what has been ordered so far.
"""

# ── Colors for terminal ──────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    DIM    = "\033[2m"
    RED    = "\033[91m"

# ── Main CLI ─────────────────────────────────────────────────────────────────
def print_banner():
    print(f"""
{C.YELLOW}{C.BOLD}
  ╔══════════════════════════════════╗
  ║   🍔  QuickBite Order System     ║
  ║   Powered by Google Gemini       ║
  ╚══════════════════════════════════╝
{C.RESET}
{C.DIM}Type your order naturally. Type 'menu' to see options.
Type 'quit' or 'exit' to leave.{C.RESET}
""")

def print_menu():
    print(f"\n{C.CYAN}{C.BOLD}━━━ OUR MENU ━━━{C.RESET}")
    print(MENU)

def load_balance() -> int:
    try:
        with open(PROMT_FILE, "r") as f:
            return json.load(f)["PromtCount"]
    except (FileNotFoundError, KeyError):
        return 1500
def save_balance(balance: int):
    with open(PROMT_FILE, "w") as f:
        json.dump({"PromtCount": balance}, f)
def print_promt_stats(balance: int):
    print(f"{C.RED}Promts remaning: {balance}")



def run():
    PromtCount = load_balance()
    print_banner()

    # Init Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    history = []


    def send(message):
        nonlocal PromtCount


        history.append(types.Content(role="user", parts=[types.Part(text=message)]))
        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=history,
        )
        reply = response.text
        history.append(types.Content(role="model", parts=[types.Part(text=reply)]))

        PromtCount -= 1
        save_balance(PromtCount)

        return reply



    # Opening message from AI
    reply = send("The customer just walked up to the counter. Greet them and take their order.")
    print(f"\n{C.GREEN}{C.BOLD}QuickBite:{C.RESET} {reply}\n")

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

            print_promt_stats(PromtCount)
        except Exception as e:
            print(f"\n{C.RED}Error talking to Gemini: {e}{C.RESET}\n")
            print("Make sure your GEMINI_API_KEY is set correctly.\n")

if __name__ == "__main__":
    run()