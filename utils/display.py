from app_contents import MENU

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