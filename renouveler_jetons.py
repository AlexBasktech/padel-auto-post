"""Prolonge de 60 jours les jetons Instagram et enregistre les nouveaux dans les secrets GitHub.

Variables : GH_PAT (accès « Secrets » au dépôt), GITHUB_REPOSITORY, et un jeton par compte.
Aucun jeton n'est jamais affiché dans les journaux.
"""
import base64, os, sys
import requests
from nacl import encoding, public

REPO = os.environ["GITHUB_REPOSITORY"]
PAT = os.environ.get("GH_PAT", "")
COMPTES = [("IG_ACCESS_TOKEN", "Padel"), ("IG_TOKEN_BASKTECH", "BaskTech")]
GH = {"Authorization": f"Bearer {PAT}", "Accept": "application/vnd.github+json"}


def chiffrer(cle_publique: str, valeur: str) -> str:
    cle = public.PublicKey(cle_publique.encode(), encoding.Base64Encoder())
    return base64.b64encode(public.SealedBox(cle).encrypt(valeur.encode())).decode()


def main() -> int:
    if not PAT:
        print("GH_PAT absent : renouvellement impossible (le secret n'est pas encore créé).")
        return 1
    r = requests.get(f"https://api.github.com/repos/{REPO}/actions/secrets/public-key", headers=GH, timeout=30)
    r.raise_for_status()
    pk = r.json()
    erreurs = 0
    for nom, compte in COMPTES:
        ancien = os.environ.get(nom, "")
        if not ancien:
            print(f"{compte} : secret {nom} vide, ignoré.")
            erreurs += 1
            continue
        rep = requests.get("https://graph.instagram.com/refresh_access_token",
                           params={"grant_type": "ig_refresh_token", "access_token": ancien}, timeout=30)
        if rep.status_code != 200:
            print(f"{compte} : échec du renouvellement Instagram (code {rep.status_code}) : {rep.json().get('error', {}).get('message', '?')}")
            erreurs += 1
            continue
        nouveau = rep.json()["access_token"]
        jours = rep.json().get("expires_in", 0) // 86400
        put = requests.put(f"https://api.github.com/repos/{REPO}/actions/secrets/{nom}", headers=GH, timeout=30,
                           json={"encrypted_value": chiffrer(pk["key"], nouveau), "key_id": pk["key_id"]})
        if put.status_code not in (201, 204):
            print(f"{compte} : jeton prolongé mais enregistrement refusé (code {put.status_code}).")
            erreurs += 1
            continue
        print(f"{compte} : jeton prolongé, valable encore {jours} jours, secret mis à jour.")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
