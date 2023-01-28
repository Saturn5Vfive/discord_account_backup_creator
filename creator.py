import requests
import json
import base64
import time

def yorn(response:str, default:bool):
    if response.lower() in ["yes", "y"]:
        return True
    if response.lower() in ["no", "n"]:
        return False
    else:
        return default

user = {
    "friends":[],
    "user":[],
    "settings":[],
    "servers":[]
}

TOKEN = input("Token~")

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


#Save Friends
friends_response = json.loads(requests.get("https://discord.com/api/v8/users/@me/relationships", headers=get_headers).text)
for friend in friends_response:
    user['friends'].append(friend["id"])
    print(f"Saved Friend [{friend['id']}]")

#save user profile
user['user'] = json.loads(requests.get("https://discord.com/api/v9/users/@me", headers=get_headers).text)
print("Saved User Profile")
AVATAR_URL = f"https://cdn.discordapp.com/avatars/{user['user']['id']}/{user['user']['avatar']}.png"
user['user']['avatar_image'] = base64.b64encode(requests.get(AVATAR_URL).content).decode('utf-8')
print("Saved User avatar")

#save users settings
user['settings'] = json.loads(requests.get("https://discord.com/api/v8/users/@me/settings", headers=get_headers).text)
print("Saved User Settings")

def g_chan(server:str):
    channels = json.loads(requests.get(f"https://canary.discord.com/api/v8/guilds/{server}/channels", headers=get_headers).text)
    for channel in channels:
        if channel['type'] == 0:
            return channel['id']
    return "0"

def generate_invite(server):
    channel_proto = g_chan(server)
    print(channel_proto)
    p = {
        "max_age": 0,
        "max_uses": 0,
        "temporary": False,
        "target_type":None,
        "validate":None
    }
    invite = json.loads(requests.post(f"https://discord.com/api/v9/channels/{channel_proto}/invites", json=p, headers=get_headers).text)['code']
    time.sleep(1)
    return invite


#save servers, and an invite to said servers
guilds = json.loads(requests.get("https://discord.com/api/v9/users/@me/guilds", headers=get_headers).text)
for guild in guilds:
    invite = generate_invite(guild['id'])
    serber = [guild['id'], guild['name'], invite]
    user['servers'].append(serber)
    print("Added Server " + str(invite) + " for "  + str(guild['name'])) 


with open(user['user']['username'] + ".backup", "w+") as handle:
    handle.write(base64.b64encode(json.dumps(user).encode('utf-8')).decode('utf-8'))


