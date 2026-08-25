"""Minimal base58btc (Bitcoin alphabet) codec — pure Python, MicroPython-safe."""
_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(data):
    n = 0
    for byte in data:
        n = n * 256 + byte
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = _ALPHABET[r] + out
    zeros = 0
    for byte in data:
        if byte == 0:
            zeros += 1
        else:
            break
    return ("1" * zeros) + out


def b58decode(s):
    n = 0
    for ch in s:
        idx = _ALPHABET.find(ch)
        if idx < 0:
            raise ValueError("invalid base58 character")
        n = n * 58 + idx
    out = bytearray()
    while n > 0:
        n, r = divmod(n, 256)
        out.insert(0, r)
    zeros = 0
    for ch in s:
        if ch == "1":
            zeros += 1
        else:
            break
    return bytes(bytearray(zeros) + out)
