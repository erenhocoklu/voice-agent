import json

from utils.display import C
from config import PROMPT_FILE

def load_balance() -> int:
    try:
        with open(PROMPT_FILE, "r") as f:
            return json.load(f)["Prompt Count"]
    except (FileNotFoundError, KeyError):
        return 1500
def save_balance(balance: int):
    with open(PROMPT_FILE, "w") as f:
        json.dump({"Prompt Count": balance}, f)
def print_prompt_stats(balance: int):
    print(f"{C.RED}Prompts remaining: {balance}")