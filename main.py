import config
import json
import time
import websocket
import requests

status = "dnd"
token = config.token
custom_status = "Discord.gg/SpicyCode"
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
                    #Uncomment the below lines if you want an emoji in the status
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
    ws.send(json.dumps(cstatus))  # Add this line to set custom status
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_keep_online():
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        keep_online(token, status)
        time.sleep(30)

run_keep_online()
