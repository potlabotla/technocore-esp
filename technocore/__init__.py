"""technocore — a MicroPython client for technocore.chat (did:key + Ed25519)."""
from .did import Identity, verify, encode_did, decode_did, fresh_nonce

__version__ = "1.0.0"
