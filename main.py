import requests, os

FOOTBALL_TOKEN = os.getenv("FOOTBALL_TOKEN")
FB_TOKEN = os.getenv("FB_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
HEADERS = {"X-Auth-Token": FOOTBALL_TOKEN}

def post_fb(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    r = requests.post(url, data={"message": message, "access_token": FB_TOKEN})
    print(r.text)
    return r.text

# On prend LIVE + IN_PLAY + FINISHED aujourd'hui pour être sûr d'avoir quelque chose
url = "https://api.football-data.org/v4/matches?status=LIVE,IN_PLAY,PAUSED"
resp = requests.get(url, headers=HEADERS)
print(f"API status: {resp.status_code}")
data = resp.json()
print(f"Matches trouvés: {data.get('resultSet', {}).get('count', 0)}")

matches = data.get("matches", [])

if not matches:
    print("Aucun match live en ce moment, Fini")
else:
    for m in matches:
        home = m["homeTeam"]["shortName"]
        away = m["awayTeam"]["shortName"]
        comp = m["competition"]["name"]
        minute = m.get("minute", "")
        # Pour le live, le score est dans fullTime ou halfTime
        score = m["score"]
        sh = score.get("fullTime", {}).get("home")
        sa = score.get("fullTime", {}).get("away")
        if sh is None:
            sh = score.get("halfTime", {}).get("home", 0)
            sa = score.get("halfTime", {}).get("away", 0)
        
        status = m["status"]
        msg = f"⚽ {minute}' LIVE - {status}\n{home} {sh}-{sa} {away}\n🏆 {comp}\n\n#INFOscore"
        print(f"Post: {msg}")
        post_fb(msg)

print("Fini")
