"""did:key identities for MicroPython, backed by the pure-Python Ed25519 module."""
import os
import binascii

from . import ed25519
from .base58 import b58encode, b58decode

_MULTICODEC_ED25519 = b"\xed\x01"


def _b64url(data):
    s = binascii.b2a_base64(data).decode().strip()
    return s.replace("+", "-").replace("/", "_").rstrip("=")


def _b64url_decode(s):
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * ((4 - len(s) % 4) % 4)
    return binascii.a2b_base64(s)


def encode_did(public):
    return "did:key:z" + b58encode(_MULTICODEC_ED25519 + public)


def decode_did(did):
    if not did.startswith("did:key:z"):
        raise ValueError("not a did:key identifier")
    decoded = b58decode(did[len("did:key:z"):])
    if decoded[0] != 0xed or decoded[1] != 0x01:
        raise ValueError("did:key is not an Ed25519 key")
    return decoded[2:]


def fresh_nonce():
    import time
    # time.time_ns exists in CPython; MicroPython uses ticks — either is monotonic-ish.
    try:
        return str(time.time_ns())
    except AttributeError:
        return str(int(time.time() * 1000) * 1000000)


class Identity:
    """An Ed25519 did:key signing identity."""

    def __init__(self, seed):
        self._seed = seed
        self._public = ed25519.publickey(seed)
        self.did = encode_did(self._public)

    @classmethod
    def generate(cls):
        return cls(os.urandom(32))

    @classmethod
    def from_seed_hex(cls, seed_hex):
        return cls(binascii.unhexlify(seed_hex))

    def seed_hex(self):
        return binascii.hexlify(self._seed).decode()

    def sign(self, room, nonce, text):
        msg = ("%s|%s|%s" % (room, nonce, text)).encode("utf-8")
        return _b64url(ed25519.sign(msg, self._seed, self._public))


def verify(did, room, nonce, text, signature):
    try:
        public = decode_did(did)
        msg = ("%s|%s|%s" % (room, nonce, text)).encode("utf-8")
        return ed25519.verify(_b64url_decode(signature), msg, public)
    except Exception:
        return False
