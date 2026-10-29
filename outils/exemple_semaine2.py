import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import gen, gen_bt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = "/tmp/_p.png"

def save(make, kicker, big, sub, dest):
    make(TMP, kicker, big, sub)
    Image.open(TMP).convert("RGB").save(dest, quality=92)

# ---------- PADEL ----------
PAD_TAIL = "\n\n🏟️ {offer}\n👉 Lien dans la bio\n\n{tags}"
pad = json.load(open(f"{REPO}/posts.json", encoding="utf-8"))

# Correction du 30/10 : chiffres actuels du site (Occitanie 220, Nouvelle-Aquitaine 206, PACA 202)
save(gen.make, "Les chiffres", "Top 3\nRégions", "Occitanie 220 Clubs, Nouvelle-Aquitaine 206, PACA 202. Et chez toi ?", f"{REPO}/posts/2026-10-30.jpg")
pad["2026-10-30"] = ("Le podium des régions du Padel 🏆\n🥇 Occitanie : 220 Clubs\n🥈 Nouvelle-Aquitaine : 206 Clubs\n🥉 Provence-Alpes-Côte d'Azur : 202 Clubs\n"
                     "Et ta région, elle est où ? Dis-le en commentaire 👇\n\n🏟️ Ton Club n'est pas encore Premium ? C'est dès 29 €/mois.\n👉 Lien dans la bio\n\n#Padel #PadelFrance #Occitanie #NouvelleAquitaine #PACA #Chiffres")

W2 = [
 ("2026-11-02", "Belgique", "106\nClubs", "de Padel en Belgique. Les Clubs autour de toi, triés par distance.",
  "106 Clubs de Padel référencés en Belgique 🇧🇪\nTu cherches un Terrain près de chez toi ? Active ta position : les Clubs les plus proches s'affichent, triés par distance. Gratuit, sans compte.",
  "Tu gères un Club ? Passe Premium dès 29 €/mois pour te démarquer auprès des Joueurs.", "#Padel #PadelBelgique #Belgique #ClubDePadel #PadelLife"),
 ("2026-11-03", "Maroc", "58\nClubs", "de Padel référencés au Maroc. Trouve le plus proche de toi.",
  "58 Clubs de Padel référencés au Maroc 🇲🇦\nEn voyage ou à la maison, trouve le Club le plus proche en quelques secondes. Gratuit, sans compte.",
  "Club de Padel au Maroc ? Passe Premium dès 29 €/mois et gagne en visibilité auprès des Joueurs.", "#Padel #PadelMaroc #Maroc #ClubDePadel #PadelLife"),
 ("2026-11-04", "Île-de-France", "151\nClubs", "Paris, Hauts-de-Seine, Yvelines, Essonne… trouve le Club le plus proche.",
  "151 Clubs de Padel en Île-de-France 🗼\nParis, Hauts-de-Seine, Yvelines, Essonne, Val-d'Oise… Trouve le Club le plus proche et appelle-le directement depuis la fiche. Gratuit, sans compte.",
  "Club d'Île-de-France ? Avec l'offre Premium dès 29 €/mois, ton Club est mis en avant auprès des Joueurs.", "#Padel #IleDeFrance #Paris #PadelFrance #ClubDePadel"),
 ("2026-11-05", "Les chiffres", "Régions\n4 à 6", "Auvergne-Rhône-Alpes 191 Clubs, Île-de-France 151, Hauts-de-France 102. Et chez toi ?",
  "Les régions du Padel, suite du classement 📊\n4. Auvergne-Rhône-Alpes : 191 Clubs\n5. Île-de-France : 151 Clubs\n6. Hauts-de-France : 102 Clubs\nEt ta région, elle est où ? Dis-le en commentaire 👇",
  "Ton Club n'est pas encore Premium ? C'est dès 29 €/mois.", "#Padel #PadelFrance #AuvergneRhoneAlpes #IleDeFrance #HautsDeFrance #Chiffres"),
 ("2026-11-06", "Grandes villes", "4 Clubs", "Bordeaux, Toulouse et Tarbes comptent chacune 4 Clubs de Padel. Et ta ville ?",
  "Bordeaux, Toulouse, Tarbes : 4 Clubs de Padel dans chacune de ces villes 🎾\nEn déplacement ? Tape ta destination et trouve les Clubs en quelques secondes. Gratuit, sans compte.",
  "Club en ville ? Passe Premium dès 29 €/mois pour remonter auprès des Joueurs.", "#Padel #Bordeaux #Toulouse #Tarbes #PadelFrance #ClubDePadel"),
 ("2026-11-07", "Spécial Clubs", "Passe en\nmode Live", "Ton Club passe son terrain en Live et remonte en tête de sa ville.",
  "Clubs de Padel, ce post est pour vous 📣\nEn mode Live, votre Club passe son Terrain en Live et remonte en tête de sa ville auprès des Joueurs qui cherchent où jouer.",
  "L'offre Premium, c'est dès 29 €/mois. Infos : padelautourdemoi.fr/pro (lien dans la bio)", "#Padel #ClubDePadel #GerantDeClub #PadelBusiness #PadelFrance"),
 ("2026-11-08", "Équipement", "Trouve ton\néquipement", "Trouve un magasin ou un constructeur de Padel sur padelautourdemoi.fr.",
  "Besoin de matériel pour ton Padel ? 🛒\nTrouve un magasin ou un constructeur sur padelautourdemoi.fr. Gratuit, sans compte.",
  "Ton Club n'est pas encore Premium ? C'est dès 29 €/mois.", "#Padel #EquipementPadel #MagasinPadel #PadelFrance #PadelLife"),
]
for d, k, b, s, cap, offer, tags in W2:
    save(gen.make, k, b, s, f"{REPO}/posts/{d}.jpg")
    pad[d] = cap + PAD_TAIL.format(offer=offer, tags=tags)
json.dump(pad, open(f"{REPO}/posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- BASKTECH ----------
bt = json.load(open(f"{REPO}/basktech/posts.json", encoding="utf-8"))
CTA = "🔎 Ton site est-il visible par ChatGPT, Gemini ou Perplexity ? Teste-le sur basktech.eus/test-visibilite-ia\n👉 Lien dans la bio"
TAGS = "#BaskTech #PaysBasque #Bayonne #Baiona #IA #NoCode #TPE #Entrepreneurs #EuskalHerria"
B2 = [
 ("2026-11-03", "Agents IA", "24 h/24", "Des agents IA qui travaillent en automatique, même en dehors des heures de bureau.",
  "Agents IA : 24 h/24 — Ils prennent en charge des tâches récurrentes et travaillent en automatique, même en dehors des heures de bureau. Ta structure devient plus réactive."),
 ("2026-11-04", "Automatisation", "Make\net n8n", "On connecte tes logiciels du quotidien pour automatiser les tâches répétitives.",
  "Make et n8n — On connecte les logiciels de ton quotidien pour automatiser les tâches répétitives : du temps gagné et moins d'erreurs."),
 ("2026-11-05", "No-code", "Sans\ncoder", "Des outils construits avec Notion, Airtable ou Webflow.",
  "Sans coder — On construit des outils sans code avec Notion, Airtable ou Webflow, adaptés à ton activité."),
 ("2026-11-06", "Pour qui ?", "Pour\ntoi", "Auto-entrepreneurs, TPE, PME, associations et collectivités du Pays Basque.",
  "Pour qui ? — Auto-entrepreneurs, TPE, PME, associations et collectivités du Pays Basque : on t'accompagne sur l'IA, l'automatisation et le no-code."),
 ("2026-11-07", "Association", "Depuis\n2023", "Association loi 1901 à Bayonne, présente sur le terrain en Iparralde et Hegoalde.",
  "Depuis 2023 — La BaskTech est une association loi 1901 basée à Bayonne, présente sur le terrain en Iparralde et Hegoalde. Notre mission : mettre les technologies émergentes au service du territoire."),
 ("2026-11-08", "De A à Z", "Du projet\nen ligne", "Accompagnement de bout en bout, de l'idée à la mise en production.",
  "Du projet en ligne — On t'accompagne de bout en bout, de l'idée à la mise en production."),
 ("2026-11-09", "Sur mesure", "Chaque\nprojet", "est différent. Parle-nous du tien sur basktech.eus.",
  "Chaque projet est différent — Parle-nous du tien : IA, automatisation, no-code, visibilité auprès des IA."),
]
for d, k, b, s, cap in B2:
    save(gen_bt.make, k, b, s, f"{REPO}/basktech/posts/{d}.jpg")
    bt[d] = f"{cap}\n\n{CTA}\n\n{TAGS}"
json.dump(bt, open(f"{REPO}/basktech/posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# planche de contrôle
import glob
fs = [f"{REPO}/posts/2026-10-30.jpg"] + [f"{REPO}/posts/{d[0]}.jpg" for d in W2] + [f"{REPO}/basktech/posts/{d[0]}.jpg" for d in B2]
th = [Image.open(f).resize((270, 338)) for f in fs]
cols = 5
sheet = Image.new("RGB", (270*cols, 338*((len(th)+cols-1)//cols)), "white")
for i, t in enumerate(th): sheet.paste(t, ((i % cols)*270, (i//cols)*338))
sheet.save("/tmp/claude-0/-home-claude/88e184ad-0028-5743-8a8c-1a3d5f0182a7/scratchpad/planche2.jpg")
print("ok", len(fs))
