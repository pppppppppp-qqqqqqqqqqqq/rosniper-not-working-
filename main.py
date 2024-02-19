import requests, json, webbrowser

userid = "1018544972"
placeid = "2788229376"

session = requests.Session()

cursor = " "

def splitlist(list, x):
    for i in range(0, len(list), x):
        yield list[i:i + x]

def storetokens(data):
    list = []

    for v in data:
        jobid = v["id"]

        for v in v["playerTokens"]:
            list.append({"requestId": f"0:{v}:AvatarHeadshot:48x48:png:regular", "targetId": 0, "token": v, "type": "AvatarHeadShot", "size": "48x48", "format": "png", "jobid": jobid})

    return list

url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={userid}"
response = session.get(url)
decoded = json.loads(response.text)["data"]

headshot = decoded[0]["imageUrl"]

while cursor:
    url = f"https://games.roblox.com/v1/games/{placeid}/servers/public?sortOrder=Asc&limit=100&cursor=" + cursor
    response = session.get(url)
    decoded = json.loads(response.text)

    cursor = decoded["nextPageCursor"]
    tokens = list(splitlist(storetokens(decoded["data"]), 100))

for v in range(0, len(tokens)):
    i = v

    url = "https://thumbnails.roblox.com/v1/batch"
    response = session.post(url, json = tokens[v])
    decoded = json.loads(response.text)["data"]

    print(decoded)

    for v in decoded:
        token = v["requestId"].replace("0:", "", ).replace(":", "").replace("AvatarHeadshot48x48pngregular", "")

        if v["imageUrl"] == headshot:
            for v in tokens[i]:
                if token == v["token"]:
                    url = f"roblox://experiences/start?placeId={placeid}&gameInstanceId={v["jobid"]}"
                    webbrowser.open(url, new = 0, autoraise = True)
                    #print((f"Roblox.GameLauncher.joinGameInstance({placeid}, '{v["jobid"]}')"))