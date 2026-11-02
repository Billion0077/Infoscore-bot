import requests, time, os
FOOTBALL_TOKEN = os.getenv("FOOTBALL_TOKEN")
FB_TOKEN = os.getenv("FB_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
HEADERS = {"X-Auth-Token": FOOTBALL_TOKEN}
posted = set()
def post_fb(msg):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    r = requests.post(url, data={"message": msg, "access_token": FB_TOKEN})
    print(r.text)
print("INFOscore bot en route...")
while True:
    try:
        r = requests.get("https://api.football-data.org/v4/matches?status=IN_PLAY", headers=HEADERS)
        for m in r.json().get("matches", []):
            home = m["homeTeam"]["shortName"]
            away = m["awayTeam"]["shortName"]
            sh = m["score"]["fullTime"]["home"]
            sa = m["score"]["fullTime"]["away"]
            minute = m.get("minute", "")
            key = f"{m['id']}_{sh}_{sa}"
            if key not in posted and sh is not None:
                posted.add(key)
                post_fb(f"🚨 GOAL LIVE {minute}'\n{home} {sh}-{sa} {away}\n🏆 {m['competition']['name']}\n\n#INFOscore")
    except Exception as e:
        print(e)
    time.sleep(10)
