"""Builds the Mapsheet site (English + French) into this folder. Run: python3 build.py"""
import pathlib, html

CSS = """
:root{--ink:#14211b;--muted:#4b5a52;--line:#dfe6e1;--bg:#f6f8f6;--card:#fff;--green:#0d6b4a;--green-2:#e5f1eb}
*{box-sizing:border-box}body{margin:0;font:17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--green)}.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header{display:flex;align-items:center;justify-content:space-between;padding:18px 0}
header .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:19px;color:var(--ink);text-decoration:none}
header img{width:36px;height:36px;border-radius:9px}header nav a{margin-left:18px;color:var(--muted);text-decoration:none;font-size:15px}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding:30px 0 50px}
.hero h1{font-size:44px;line-height:1.1;margin:0 0 16px;letter-spacing:-.02em}.hero p.lead{font-size:20px;color:var(--muted);margin:0 0 22px}
.badge{display:inline-block;background:var(--ink);color:#fff;padding:12px 20px;border-radius:12px;font-weight:600;text-decoration:none}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.facts span{background:var(--green-2);color:var(--green);padding:6px 11px;border-radius:999px;font-size:14px;font-weight:600}
.phone{width:100%;max-width:340px;justify-self:center;border-radius:36px;box-shadow:0 20px 50px rgba(20,33,27,.18);border:8px solid #111}
h2{font-size:30px;margin:0 0 18px;letter-spacing:-.01em}section{padding:36px 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.card h3{margin:0 0 6px;font-size:18px}.card p{margin:0;color:var(--muted);font-size:15.5px}
.shots{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.shots figure{margin:0}.shots img{width:100%;border-radius:22px;border:6px solid #111}
.shots figcaption{font-size:14px;color:var(--muted);margin-top:8px;text-align:center}
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.plan .price{font-size:26px;font-weight:700;margin:6px 0 10px}.plan ul{margin:0;padding-left:18px;color:var(--muted);font-size:15.5px}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-bottom:10px}summary{font-weight:600;cursor:pointer}
footer{border-top:1px solid var(--line);padding:24px 0 40px;color:var(--muted);font-size:14px}
.doc{max-width:760px}.doc h1{font-size:34px}
@media (max-width:820px){.hero{grid-template-columns:1fr}.hero h1{font-size:34px}.grid,.plans{grid-template-columns:1fr}.shots{grid-template-columns:repeat(2,1fr)}header nav{display:none}}
"""

T = {
 "en": dict(
  lang="en", root="", other="fr/", otherName="Français", privacyFile="privacy.html",
  title="Mapsheet: Offline PDF Maps GPS — your own maps, with you on them",
  desc="Mapsheet shows where you are on geospatial PDFs (including GeoPDF®) and GeoTIFFs with no signal. Unlimited maps, work use included, crew packs, UTM and MGRS.",
  nav=("Features", "Plans", "Support"),
  h1="Your maps, offline, with you on them.",
  lead="Open a block map, a fire map or a topo — any geospatial PDF or GeoTIFF — and Mapsheet shows your position on it with no signal. Drop points with photos, record tracks, measure areas, and send maps to your whole crew at once.",
  soon="Coming soon to the App Store",
  facts=("No account", "Works with no signal", "Work use included", "English and French"),
  featH="What Mapsheet does",
  feats=[("Your maps, any source","Geospatial PDFs from ArcGIS, QGIS, Global Mapper, NRCan and USGS (GeoPDF® files included) and GeoTIFFs. Multi-page atlases, rotated pages and zipped downloads."),
         ("You on the map","GPS position, accuracy and heading on the map, even in airplane mode. Bluetooth GNSS receivers paired in iOS work automatically."),
         ("Points, tracks, areas","Points with notes and photos, tracks that keep recording with the phone locked, lines and areas measured in metres, hectares or acres."),
         ("Walk to a point","Distance and bearing from you to any point — a plot centre, a cache, a block corner."),
         ("Coordinates crews use","Lat/lon, degrees-minutes, UTM and MGRS/USNG — shown and typed. Canada's provincial systems built in: BC Albers, Alberta 10TM, MTM, Quebec Lambert."),
         ("Crew packs","A crew lead sends several maps, points and photos in one file by AirDrop or message. The crew opens it free; new points merge with theirs."),
         ("Fix it in the field","Drag a corner of an area or line to move it, tap to add one, press and hold to remove one. Mark points with symbols: plots, caches, hazards, landings."),
         ("Precise points","Average your GPS position over half a minute for a plot centre or a corner, with the standard error shown (Crew)."),
         ("Into ArcGIS and QGIS","Export GPX, KML, KMZ and CSV with UTM columns on every plan; shapefiles on Crew. Import GPX, KML and shapefiles back.")],
  shotsH="See it", shots=[("map","Your position on a USGS topo"),("point","Distance and bearing to a point"),("edit","Measure and edit an area"),("features","Points, tracks and areas")],
  plansH="Plans",
  plans=[("Free","$0",["3 maps at a time — an atlas counts once","Every field tool: GPS, points with symbols and photos, tracks, measuring, shape editing","GPX, KML and CSV export","Work use allowed"]),
         ("Field","$59.99 / year",["Unlimited maps","Work use included — no separate pro licence","Or $9.99 / month for seasonal work"]),
         ("Crew","$129.99 / year per device",["Everything in Field","Send maps to your crew as crew packs — they open them free","GPS averaging for precise points","Shapefile export","Or $19.99 / month per device"])],
  plansNote="<b>Your maps never lock.</b> If a plan ends you keep every map; you just can't add more past three. US prices; local prices in other countries. Two weeks free on yearly plans for new subscribers.",
  faqH="Questions and support",
  faq=[("Which maps work?","Geospatial PDFs (including GeoPDF® files) and GeoTIFFs, also inside a zip. A plain PDF without map coordinates can't show your position."),
       ("Do I need a signal?","No. Maps live on your phone and GPS works anywhere with a view of the sky."),
       ("Can I use it for work?","Yes, on every plan. Mapsheet doesn't charge extra for professional use."),
       ("How do I get maps onto my phone?","Share the file to Mapsheet from Mail, Files, Drive or AirDrop, or tap + in the map list. Your crew lead can send a crew pack."),
       ("Is my data shared?","No. Maps, points, tracks, photos and your position stay on your device. There's no account and no server. See the <a href='{privacy}'>privacy policy</a>.")],
  contact="Still stuck? Write to <b>laddothis at gmail dot com</b> with what happened and your device. We answer within a day.",
  foot="Mapsheet is not affiliated with Avenza Systems, TerraGo Technologies, Esri or the USGS. GeoPDF is a registered trademark of TerraGo Technologies.",
  privacyTitle="Privacy policy",
  privacy="""<p><b>Effective November 8, 2026.</b></p>
<p>Mapsheet is built so your work stays yours. It has no account, no server and no analytics.</p>
<h2>What stays on your device</h2>
<p>Your maps, the points, tracks, lines, areas and photos you add, and your position are stored only on your iPhone or iPad (and in your device backups). Mapsheet does not send them anywhere.</p>
<h2>Location</h2>
<p>Mapsheet uses your location to show where you are on your maps and to record tracks you start, including while the phone is locked if a track is recording. Your location never leaves your device.</p>
<h2>Camera and photos</h2>
<p>If you attach photos to points, they are saved with your map on your device.</p>
<h2>Sharing</h2>
<p>When you export features or send a crew pack, you choose where the file goes (AirDrop, Messages, Mail, Files…). Mapsheet only creates the file.</p>
<h2>Purchases</h2>
<p>Subscriptions are handled by Apple. Mapsheet receives only whether a subscription is active, never your payment details.</p>
<h2>Contact</h2>
<p>laddothis at gmail dot com</p>"""),
 "fr": dict(
  lang="fr-CA", root="../", other="../", otherName="English", privacyFile="confidentialite.html",
  title="Mapsheet : cartes PDF et GPS — vos cartes, avec vous dessus",
  desc="Mapsheet vous situe sur les PDF géoréférencés (y compris GeoPDF®) et les GeoTIFF, sans réseau. Cartes illimitées, usage professionnel inclus, paquets d'équipe, UTM et MGRS.",
  nav=("Fonctions", "Forfaits", "Aide"),
  h1="Vos cartes, hors ligne, avec vous dessus.",
  lead="Ouvrez un plan de bloc, une carte de feu ou une carte topo — tout PDF géoréférencé ou GeoTIFF — et Mapsheet affiche votre position, sans réseau. Ajoutez des points avec photos, enregistrez des traces, mesurez des surfaces et envoyez des cartes à toute votre équipe d'un coup.",
  soon="Bientôt sur l'App Store",
  facts=("Sans compte", "Fonctionne sans réseau", "Usage professionnel inclus", "Français et anglais"),
  featH="Ce que fait Mapsheet",
  feats=[("Vos cartes, de partout","PDF géoréférencés d'ArcGIS, QGIS, Global Mapper, RNCan et l'USGS (fichiers GeoPDF® compris) et GeoTIFF. Atlas de plusieurs pages, pages pivotées et téléchargements zippés."),
         ("Vous sur la carte","Position GPS, précision et direction sur la carte, même en mode avion. Les récepteurs GNSS Bluetooth jumelés dans iOS fonctionnent d'office."),
         ("Points, traces, surfaces","Points avec notes et photos, traces qui continuent avec l'écran verrouillé, lignes et surfaces mesurées en mètres, hectares ou acres."),
         ("Marcher vers un point","Distance et azimut entre vous et n'importe quel point — un centre de parcelle, une cache, un coin de bloc."),
         ("Les coordonnées des équipes","Lat/long, degrés-minutes, UTM et MGRS/USNG — affichées et saisies. Systèmes provinciaux intégrés : Albers C.-B., 10TM Alberta, MTM, Lambert Québec."),
         ("Paquets d'équipe","Le chef d'équipe envoie plusieurs cartes, points et photos en un seul fichier par AirDrop ou message. L'équipe l'ouvre gratuitement; les nouveaux points s'ajoutent aux siens."),
         ("Corrigez sur le terrain","Faites glisser un coin d'une surface ou d'une ligne pour le déplacer, touchez pour en ajouter un, maintenez pour le retirer. Des symboles pour vos points : parcelles, caches, dangers, jetées."),
         ("Points précis","Faites la moyenne de votre position GPS sur une demi-minute pour un centre de parcelle ou un coin, avec l'erreur type affichée (Équipe)."),
         ("Vers ArcGIS et QGIS","Exportez en GPX, KML, KMZ et CSV avec colonnes UTM avec tous les forfaits; en shapefile avec Équipe. Importez GPX, KML et shapefiles.")],
  shotsH="Aperçu", shots=[("fr-map","Votre position sur une carte topo"),("fr-point","Distance et azimut vers un point"),("fr-edit","Mesurer et modifier une surface"),("fr-features","Points, traces et surfaces")],
  plansH="Forfaits",
  plans=[("Gratuit","0 $",["3 cartes à la fois — un atlas compte pour une","Tous les outils de terrain : GPS, points avec symboles et photos, traces, mesures, modification des formes","Exportation GPX, KML et CSV","Usage professionnel permis"]),
         ("Terrain","59,99 $ US / an",["Cartes illimitées","Usage professionnel inclus — sans licence pro à part","Ou 9,99 $ US / mois pour le travail saisonnier"]),
         ("Équipe","129,99 $ US / an par appareil",["Tout ce qu'offre Terrain","Envoyez des cartes à votre équipe en paquets — ouverts gratuitement","Moyenne GPS pour des points précis","Exportation en shapefile","Ou 19,99 $ US / mois par appareil"])],
  plansNote="<b>Vos cartes ne se verrouillent jamais.</b> Si un forfait prend fin, vous gardez toutes vos cartes; vous ne pouvez simplement plus en ajouter au-delà de trois. Prix américains; l'App Store affiche le prix en dollars canadiens. Deux semaines gratuites sur les forfaits annuels pour les nouveaux abonnés.",
  faqH="Questions et aide",
  faq=[("Quelles cartes fonctionnent?","Les PDF géoréférencés (y compris les fichiers GeoPDF®) et les GeoTIFF, aussi dans un zip. Un simple PDF sans coordonnées ne peut pas afficher votre position."),
       ("Faut-il du réseau?","Non. Les cartes sont sur votre téléphone et le GPS fonctionne partout où le ciel est visible."),
       ("Puis-je l'utiliser au travail?","Oui, avec tous les forfaits. Mapsheet ne facture pas de supplément pour l'usage professionnel."),
       ("Comment mettre des cartes sur mon téléphone?","Partagez le fichier vers Mapsheet depuis Mail, Fichiers, Drive ou AirDrop, ou touchez + dans la liste des cartes. Votre chef d'équipe peut envoyer un paquet d'équipe."),
       ("Mes données sont-elles partagées?","Non. Cartes, points, traces, photos et position restent sur votre appareil. Pas de compte, pas de serveur. Voir la <a href='{privacy}'>politique de confidentialité</a>.")],
  contact="Toujours bloqué? Écrivez à <b>laddothis at gmail dot com</b> en décrivant ce qui s'est passé et votre appareil. Réponse en moins d'un jour.",
  foot="Mapsheet n'est affilié ni à Avenza Systems, ni à TerraGo Technologies, ni à Esri, ni à l'USGS. GeoPDF est une marque déposée de TerraGo Technologies.",
  privacyTitle="Politique de confidentialité",
  privacy="""<p><b>En vigueur le 8 novembre 2026.</b></p>
<p>Mapsheet est conçu pour que votre travail reste le vôtre. Pas de compte, pas de serveur, pas d'analyse d'utilisation.</p>
<h2>Ce qui reste sur votre appareil</h2>
<p>Vos cartes, les points, traces, lignes, surfaces et photos que vous ajoutez, et votre position sont stockés uniquement sur votre iPhone ou iPad (et dans ses sauvegardes). Mapsheet ne les envoie nulle part.</p>
<h2>Localisation</h2>
<p>Mapsheet utilise votre position pour vous situer sur vos cartes et enregistrer les traces que vous lancez, y compris écran verrouillé pendant un enregistrement. Votre position ne quitte jamais votre appareil.</p>
<h2>Appareil photo et photos</h2>
<p>Les photos jointes aux points sont enregistrées avec votre carte, sur votre appareil.</p>
<h2>Partage</h2>
<p>Quand vous exportez des éléments ou envoyez un paquet d'équipe, c'est vous qui choisissez la destination (AirDrop, Messages, Mail, Fichiers…). Mapsheet ne fait que créer le fichier.</p>
<h2>Achats</h2>
<p>Les abonnements sont gérés par Apple. Mapsheet sait seulement si un abonnement est actif, jamais vos données de paiement.</p>
<h2>Contact</h2>
<p>laddothis at gmail dot com</p>"""),
}

def page(t, title, body, path_to_root):
    other_href = t["other"] + ("" if t["lang"] == "en" else "")
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(t['desc'])}"><link rel="icon" href="{path_to_root}img/icon.png">
<link rel="stylesheet" href="{path_to_root}style.css"></head><body><div class="wrap">
<header><a class="brand" href="index.html"><img src="{path_to_root}img/icon.png" alt="">Mapsheet</a>
<nav><a href="index.html#features">{t['nav'][0]}</a><a href="index.html#plans">{t['nav'][1]}</a><a href="index.html#support">{t['nav'][2]}</a><a href="{other_href}">{t['otherName']}</a></nav></header>
{body}
<footer>© 2026 Mapsheet · <a href="{t['privacyFile']}">{t['privacyTitle']}</a> · {t['foot']}</footer></div></body></html>"""

for key, t in T.items():
    out = pathlib.Path("." if key == "en" else "fr")
    r = "" if key == "en" else "../"
    feats = "".join(f"<div class='card'><h3>{a}</h3><p>{b}</p></div>" for a, b in t["feats"])
    shots = "".join(f"<figure><img src='{r}img/{s}.jpg' alt='{c}' loading='lazy'><figcaption>{c}</figcaption></figure>" for s, c in t["shots"])
    plans = "".join(f"<div class='card plan'><h3>{n}</h3><div class='price'>{p}</div><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>" for n, p, items in t["plans"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a.format(privacy=t['privacyFile'])}</p></details>" for q, a in t["faq"])
    facts = "".join(f"<span>{f}</span>" for f in t["facts"])
    hero_img = "map" if key == "en" else "fr-map"
    body = f"""<div class="hero"><div><h1>{t['h1']}</h1><p class="lead">{t['lead']}</p><span class="badge">{t['soon']}</span><div class="facts">{facts}</div></div>
<img class="phone" src="{r}img/{hero_img}.jpg" alt=""></div>
<section id="features"><h2>{t['featH']}</h2><div class="grid">{feats}</div></section>
<section><h2>{t['shotsH']}</h2><div class="shots">{shots}</div></section>
<section id="plans"><h2>{t['plansH']}</h2><div class="plans">{plans}</div><p style="color:var(--muted);font-size:14px">{t['plansNote']}</p></section>
<section id="support"><h2>{t['faqH']}</h2>{faq}<p>{t['contact']}</p></section>"""
    (out / "index.html").write_text(page(t, t["title"], body, r))
    (out / t["privacyFile"]).write_text(page(t, t["privacyTitle"] + " — Mapsheet", f"<div class='doc'><h1>{t['privacyTitle']}</h1>{t['privacy']}</div>", r))
pathlib.Path("style.css").write_text(CSS)
# The paywall links privacy.html; French readers get a pointer page too.
print("built index.html, privacy.html, fr/index.html, fr/confidentialite.html")
