import requests, json, pyperclip, threading, time, asyncio, aiohttp

userid = "1018544972"
placeid = "7041939546"

session = requests.Session()

cursor = ""

async def postbatch():
    global url, response, decoded

    async with aiohttp.ClientSession() as session:
        url = "https://thumbnails.roblox.com/v1/batch"
        response = await session.post(url, json = jsons)
        decoded = json.loads(await response.text())["data"]
        #print("hi")

url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={userid}"
response = session.get(url)
decoded = json.loads(response.text)["data"]

for v in decoded:
    headshot = v["imageUrl"]

hi = time.time()

while True:
    url = f"https://games.roblox.com/v1/games/{placeid}/servers/public?sortOrder=Asc&limit=100&cursor=" + cursor
    response = session.get(url)
    decoded = json.loads(response.text)

    cursor = decoded["nextPageCursor"]

    for v in decoded["data"]:
        jobid = v["id"]
        #print(f"searching {jobid}")
        jsons = []

        for v in v["playerTokens"]:
            jsons.append({"requestId": f"0:{v}:AvatarHeadshot:48x48:png:regular", "targetId": 0, "token": v, "type": "AvatarHeadShot", "size": "48x48", "format": "png"})

        url = "https://thumbnails.roblox.com/v1/batch"

        asyncio.run(postbatch())

        for v in decoded:
            if v["imageUrl"] == headshot:
                print((f"Roblox.GameLauncher.joinGameInstance({placeid}, '{jobid}')"))
                print(time.time()-hi)
                exit()

    if not cursor:
        break