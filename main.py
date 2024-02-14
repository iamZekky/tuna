import os
import json
import time
import websocket
import requests
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return 'hello'

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

status = "dnd"
custom_status = "Discord.gg/SpicyCode"

token = os.getenv("TOKEN")
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}
userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

cstatus = {
    "op": 3,
    "d": {
        "since": 0,
        "activities": [
            {
                "type": 4,
                "state": custom_status,
                "name": "Custom Status",
                "id": "custom",
                "emoji": {
                    "name": "dev2",
                    "id": "963192571830599710",
                    "animated": False,
                },
            }
        ],
        "status": status,
        "afk": False,
    },
}

def keep_online(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
    ws.send(json.dumps(cstatus))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_keep_online():
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        keep_online(token, status)
        time.sleep(30)

# Start the Flask server to keep the bot alive
keep_alive()

# Run the main function to maintain the online status
run_keep_online()
