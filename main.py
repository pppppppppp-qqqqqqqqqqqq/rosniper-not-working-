import requests, json, webbrowser

userid = ""
placeid = ""

session = requests.Session()

cursor = " "

def storetokens(data):
    tokens = []

    for v in data:
        jobid = v["id"]

        for v in v["playerTokens"]:
            tokens.append({"requestId": f"0:{v}:AvatarHeadshot:48x48:png:regular", "targetId": 0, "token": v, "type": "AvatarHeadShot", "size": "48x48", "format": "png", "jobid": jobid})

    return tokens

url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={userid}"
response = session.get(url)
decoded = json.loads(response.text)["data"]

headshot = decoded[0]["imageUrl"]

while cursor:
    url = f"https://games.roblox.com/v1/games/{placeid}/servers/public?sortOrder=Asc&limit=100&cursor=" + cursor
    response = session.get(url)
    decoded = json.loads(response.text)

    cursor = decoded["nextPageCursor"]
    tokens = storetokens(decoded["data"])

chunks = [tokens[i:i + 100] for i in range(0, len(tokens), 100)]

for v in range(0, len(chunks)):
    i = v

    url = "https://thumbnails.roblox.com/v1/batch"
    response = session.post(url, json = chunks[v])
    decoded = json.loads(response.text)["data"]

    for v in decoded:
        requestid = v["requestId"]

        if headshot == v["imageUrl"]:
            for v in chunks[i]:
                if requestid == v["requestId"]:
                    url = f"roblox://experiences/start?placeId={placeid}&gameInstanceId={v["jobid"]}"
                    webbrowser.open(url, new = 0, autoraise = True)