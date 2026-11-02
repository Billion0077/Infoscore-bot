import requests, os
FOOTBALL_TOKEN = os.getenv("FOOTBALL_TOKEN")
FB_TOKEN = os.getenv("FB_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
HEADERS = {"X-Auth-Token": FOOTBALL_TOKEN}
def post_fb(msg):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    r = requests.post(url, data={"message": msg, "access_token": FB_TOKEN})
    print(r.text)
resp = requests.get("https://api.football-data.org/v4/matches?status=IN_PLAY", headers=HEADERS).json()
for m in resp.get("matches", []):
    home = m["homeTeam"]["shortName"]
    away = m["awayTeam"]["shortName"]
    sh = m["score"]["fullTime"]["home"]
    sa = m["score"]["fullTime"]["away"]
    minute = m.get("minute","")
    comp = m["competition"]["name"]
    if sh is not None:
        post_fb(f"⚽ {minute}' LIVE\n{home} {sh}-{sa} {away}\n🏆 {comp}\n\n#INFOscore")
print("Fini")
