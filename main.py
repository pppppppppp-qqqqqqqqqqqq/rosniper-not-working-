import requests
from json import loads
from pyperclip import copy

userid = ""
placeid = ""

session = requests.session()

url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={userid}"
response = session.get(url)
decoded = loads(response.text)["data"]

for v in decoded:
    headshot = v["imageUrl"]

url = f"https://games.roblox.com/v1/games/{placeid}/servers/public?sortOrder=Asc&limit=100"
response = session.get(url)
decoded = loads(response.text)

cursor = decoded["nextPageCursor"]

while True:
    if cursor:
        url = f"https://games.roblox.com/v1/games/{placeid}/servers/public?sortOrder=Asc&limit=100&cursor={cursor}"
        response = session.get(url)
        decoded = loads(response.text)

    cursor = decoded["nextPageCursor"]

    for v in decoded["data"]:
        jobid = v["id"]

        print(f"searching {jobid}")

        for v in v["playerTokens"]:
            url = "https://thumbnails.roblox.com/v1/batch"
            response = session.post(url, json = [{"requestId": f"0:{v}:AvatarHeadshot:48x48:png:regular", "targetId": 0, "token": v, "type": "AvatarHeadShot", "size": "48x48", "format": "png"}])
            decoded = loads(response.text)["data"]

            for v in decoded:
                if v["imageUrl"] == headshot:
                    exit(copy(f"Roblox.GameLauncher.joinGameInstance({placeid},  '{jobid}')"))