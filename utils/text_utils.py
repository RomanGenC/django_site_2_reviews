import random
import string

from utils.constants import DEFAULT_PASSWORD_LENGHT, DEFAULT_SPECIAL_SYMBOLS


def generate_password(length: int = DEFAULT_PASSWORD_LENGHT) -> str:
    rand = random.SystemRandom()
    symbols = string.ascii_letters + string.digits + DEFAULT_SPECIAL_SYMBOLS
    result = ''.join(rand.choices(symbols, k=length))

    return result
