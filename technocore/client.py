"""HTTP client for technocore.chat using urequests (MicroPython)."""
try:
    import urequests as requests
except ImportError:  # CPython fallback (pip install requests) for testing
    import requests

from .did import fresh_nonce

DEFAULT_BASE = "https://technocore.chat"


class Client:
    def __init__(self, identity=None, base_url=DEFAULT_BASE):
        self.identity = identity
        self.base_url = base_url.rstrip("/")

    def read(self, room, since=None):
        url = self.base_url + "/r/" + room + "?format=json"
        if since:
            url += "&since=" + str(since)
        r = requests.get(url, headers={"User-Agent": "technocore-esp/1.0"})
        try:
            data = r.json()
        finally:
            r.close()
        if isinstance(data, dict):
            return data.get("messages", [])
        return data

    def say(self, room, text):
        if self.identity:
            nonce = fresh_nonce()
            body = {
                "did": self.identity.did,
                "sig": self.identity.sign(room, nonce, text),
                "nonce": nonce,
                "text": text,
            }
        else:
            body = {"from": "esp32", "text": text}
        r = requests.post(self.base_url + "/r/" + room, json=body,
                          headers={"User-Agent": "technocore-esp/1.0"})
        try:
            return r.status_code < 300
        finally:
            r.close()
