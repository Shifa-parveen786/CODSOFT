import secrets
import string
import argparse
from typing import List

# Common ambiguous characters people sometimes want to avoid
AMBIGUOUS = set("Il1O0`'\"/,\\|")

# Character sets
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"

def build_charset(use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool,
                  avoid_ambiguous: bool) -> dict:
    """Return a dict of chosen character categories -> string of characters."""
    sets = {}
    if use_lower:
        sets['lower'] = LOWER
    if use_upper:
        sets['upper'] = UPPER
    if use_digits:
        sets['digits'] = DIGITS
    if use_symbols:
        sets['symbols'] = SYMBOLS

    if avoid_ambiguous:
        for k, s in list(sets.items()):
            filtered = ''.join(ch for ch in s if ch not in AMBIGUOUS)
            sets[k] = filtered

    return sets

def generate_password(length: int = 12,
                      use_lower: bool = True,
                      use_upper: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True,
                      avoid_ambiguous: bool = False) -> str:
    """
    Generate a secure password of given length.
    Guarantees at least one char from each selected category.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    sets = build_charset(use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous)
    if not sets:
        raise ValueError("At least one character type must be enabled.")

    # If length < number of selected categories, we can't guarantee one-of-each
    categories = list(sets.keys())
    if length < len(categories):
        raise ValueError(f"length must be at least {len(categories)} to include one of each selected type.")

    # Start with one guaranteed char from each selected category
    password_chars = [secrets.choice(sets[cat]) for cat in categories]

    # Build a combined pool for remaining characters
    combined = ''.join(sets.values())
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(combined) for _ in range(remaining)]

    # Shuffle the final list securely
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def generate_many(count: int = 1, **kwargs) -> List[str]:
    """Generate multiple passwords."""
    return [generate_password(**kwargs) for _ in range(count)]

def try_copy_to_clipboard(text: str) -> bool:
    """Try to copy to clipboard using pyperclip if available. Return True on success."""
    try:
        import pyperclip # type: ignore
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="Secure Password Generator")
    parser.add_argument("--length", "-l", type=int, default=12, help="password length (default: 12)")
    parser.add_argument("--count", "-c", type=int, default=1, help="how many passwords to generate")
    parser.add_argument("--no-lower", action="store_true", help="exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true", help="exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="exclude symbols")
    parser.add_argument("--avoid-ambiguous", action="store_true", help="exclude ambiguous characters (O0Il1 etc.)")
    parser.add_argument("--copy", action="store_true", help="copy the last generated password to clipboard (requires pyperclip)")

    args = parser.parse_args()

    params = dict(
        length=args.length,
        use_lower=not args.no_lower,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        avoid_ambiguous=args.avoid_ambiguous
    )

    try:
        passwords = generate_many(count=args.count, **params)
    except ValueError as e:
        parser.error(str(e))
        return

    for i, pw in enumerate(passwords, start=1):
        print(f"{i}: {pw}")

    if args.copy and passwords:
        ok = try_copy_to_clipboard(passwords[-1])
        if ok:
            print("\n✔ Last password copied to clipboard.")
        else:
            print("\n⚠ Could not copy to clipboard (pyperclip not installed or clipboard unavailable).")

if __name__ == "__main__":
    main()
