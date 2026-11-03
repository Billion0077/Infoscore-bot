import requests, os, json
from datetime import datetime

FOOTBALL_TOKEN = os.getenv("FOOTBALL_TOKEN")
FB_TOKEN = os.getenv("FB_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
HEADERS = {"X-Auth-Token": FOOTBALL_TOKEN}

def post_fb(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    r = requests.post(url, data={"message": message, "access_token": FB_TOKEN})
    print(f"FB: {r.text}")

# 1. Essaye LIVE d'abord
url_live = "https://api.football-data.org/v4/matches?status=LIVE,IN_PLAY,PAUSED"
data_live = requests.get(url_live, headers=HEADERS).json()
live = data_live.get("matches", [])

if live:
    for m in live:
        home = m["homeTeam"]["shortName"]
        away = m["awayTeam"]["shortName"]
        minute = m.get("minute") or "LIVE"
        sh = m["score"]["fullTime"]["home"] or m["score"]["halfTime"]["home"] or 0
        sa = m["score"]["fullTime"]["away"] or m["score"]["halfTime"]["away"] or 0
        msg = f"🔴 {minute}' EN DIRECT\n{home} {sh}-{sa} {away}\n🏆 {m['competition']['name']}\n\n#Infoscore #LIVE"
        post_fb(msg)
else:
    # Pas de live, on poste le résumé du jour (1 fois seulement si tu veux tester)
    print("Pas de live, on prend les matchs du jour")
    url_day = "https://api.football-data.org/v4/matches"
    data_day = requests.get(url_day, headers=HEADERS).json()
    todays = data_day.get("matches", [])[:4]
    
    if todays:
        msg = f"⚽ PROGRAMME DU JOUR - {datetime.now().strftime('%d/%m')}\n\n"
        for m in todays:
            h = m["homeTeam"]["shortName"]
            a = m["awayTeam"]["shortName"]
            hour = m["utcDate"][11:16]
            msg += f"{hour} - {h} vs {a} - {m['status']}\n"
        msg += "\n#Infoscore"
        # Pour le test, on poste. Après tu peux commenter cette ligne
        post_fb(msg)
    else:
        print("Rien aujourd'hui non plus")

print("Fini")
