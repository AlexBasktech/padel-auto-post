"""Publie le post Instagram du jour pour @padelautourdemoi.fr.

Lancé chaque matin par GitHub Actions. Lit posts.json, prend l'image
posts/AAAA-MM-JJ.jpg du jour, la publie via l'API Instagram, puis
envoie un e-mail de contrôle (via Resend, si la clé est configurée).
"""
import json
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

API = "https://graph.instagram.com/v24.0"
TZ = ZoneInfo("Africa/Casablanca")

IG_USER_ID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]  # fourni par GitHub Actions
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RESEND_KEY = os.environ.get("RESEND_API_KEY", "")
MAIL_TO = os.environ.get("MAIL_TO", "alex@basktech.io")
MAIL_FROM = os.environ.get("MAIL_FROM", "Padel Auto <onboarding@resend.dev>")


def send_mail(subject, text):
    if not RESEND_KEY:
        print("Pas de RESEND_API_KEY : e-mail non envoyé.")
        return
    r = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_KEY}"},
        json={"from": MAIL_FROM, "to": [MAIL_TO], "subject": subject, "text": text},
        timeout=30,
    )
    print("E-mail :", r.status_code, r.text[:200])


def api(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=60)
    data = r.json()
    if r.status_code != 200 or "error" in data:
        raise RuntimeError(f"Erreur API Instagram ({path}) : {data}")
    return data


def main():
    day = os.environ.get("POST_DATE") or datetime.now(TZ).strftime("%Y-%m-%d")
    day_fr = datetime.strptime(day, "%Y-%m-%d").strftime("%d/%m/%y")

    posts = json.load(open("posts.json", encoding="utf-8"))
    if day not in posts:
        print(f"Aucun post prévu le {day_fr}.")
        return

    caption = posts[day]
    image_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts/{day}.jpg"
    print("Image :", image_url)

    try:
        # 1. Créer le conteneur média
        container = api("POST", f"{IG_USER_ID}/media", image_url=image_url, caption=caption)["id"]

        # 2. Attendre qu'Instagram ait traité l'image
        for _ in range(20):
            status = api("GET", container, fields="status_code").get("status_code")
            if status == "FINISHED":
                break
            if status == "ERROR":
                raise RuntimeError("Instagram n'a pas pu traiter l'image.")
            time.sleep(5)

        # 3. Publier
        media_id = api("POST", f"{IG_USER_ID}/media_publish", creation_id=container)["id"]
        link = api("GET", media_id, fields="permalink").get("permalink", "")
    except Exception as e:
        send_mail(f"❌ Échec du post Padel du {day_fr}", f"La publication a échoué :\n\n{e}")
        print(e)
        sys.exit(1)

    print("Publié :", link)
    send_mail(
        f"✅ Post Padel du {day_fr} publié",
        f"Le post du {day_fr} est en ligne :\n{link}\n\n--- Texte publié ---\n{caption}",
    )


if __name__ == "__main__":
    main()
