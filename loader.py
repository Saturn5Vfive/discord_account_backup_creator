import base64
import json
import requests
import time

UJSON = None
FILE = input("Account Backup to load~")
TOKEN = input("Where to load it~")

get_headers = {
    "x-super-properties":"eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA5LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy55b3V0dWJlLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluIjoid3d3LnlvdXR1YmUuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE2OTYxNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
    "x-discord-locale":"en-US",
    "x-debug-options":"bugReporterEnabled",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "sec-ch-ua-platform":"?Windows",
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua":"\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\",\"Chromium\";v=\"109\"",
    "referer":"https://discord.com/",
    "authorization":TOKEN
}

with open(FILE, "rb") as h:
    UJSON = json.loads(base64.b64decode(h.read()).decode('ascii'))

print("Pushing settings onto new account")
#re = requests.patch("https://canary.discord.com/api/v8/users/@me/settings", headers=get_headers, json=UJSON['settings'])


print("Saving profile picture")
with open(UJSON['user']['username'] + ".png", "wb+") as handle:
    handle.write(base64.b64decode(UJSON['user']['avatar_image']))

print("Retrieving Friends")
for friend in UJSON['friends']:
    friend_ = json.loads(requests.get(f"https://discord.com/api/v8/users/{friend}", headers=get_headers).text)
    print(f"Friend: {friend_['username']}#{friend_['discriminator']}")
    time.sleep(2)


print("Retrieving Invites")
for guild in UJSON['servers']:
    print(f"{guild[1]}:{guild[2]}")
