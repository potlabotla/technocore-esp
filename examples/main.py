# ESP32 example: connect Wi-Fi and post a signed sensor reading to a room.
# Copy the `technocore/` folder to your board, set WIFI creds + SEED, run.
import time
import network
from technocore.did import Identity
from technocore.client import Client

WIFI_SSID = "your-ssid"
WIFI_PASS = "your-pass"
ROOM = "e-sensors"          # an ephemeral room for telemetry
SEED_HEX = ""               # 32-byte hex seed; leave empty to generate one


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("wifi:", wlan.ifconfig()[0])


def main():
    connect_wifi()
    me = Identity.from_seed_hex(SEED_HEX) if SEED_HEX else Identity.generate()
    print("did:", me.did)
    agent = Client(me)
    while True:
        # Replace with a real sensor read (e.g. a DHT22 / ADC value).
        reading = time.ticks_ms() % 100
        agent.say(ROOM, "temp={}C from {}".format(reading, me.did[:16]))
        time.sleep(30)


if __name__ == "__main__":
    main()
