#!/usr/bin/env python3
"""Builds Mapsheet's site from src/pages into the repo root, which GitHub Pages serves from main.

    python3 -m venv .venv && .venv/bin/pip install markdown pillow
    .venv/bin/python src/build.py && python3 src/check.py

Pages: the home page (src/pages/home.html), the privacy policy (src/pages/privacy.body.html) and the guides
(src/pages/guides/*.md, each with a Markdown copy next to its page). Also written: 404.html, sitemap.xml, llms.txt and
llms-full.txt for AI tools, and the social card img/og.png. Change UPDATED when a page's facts are rechecked.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import markdown
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
BASE = "https://coderalert0.github.io/mapsheet-site/"
APP_ID = "6832417568"
APP = f"https://apps.apple.com/us/app/id{APP_ID}"
APP_FR = f"https://apps.apple.com/ca/app/id{APP_ID}?l=fr-CA"   # the Canadian store, in French
NAME = "Mapsheet"
APP_NAME = "Mapsheet: Offline PDF Maps GPS"
TERMS = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
UPDATED = "2026-11-08"
UPDATED_LONG = date.fromisoformat(UPDATED).strftime("%B %-d, %Y")
DISCLAIMER = ("Mapsheet shows positions from your device's GPS. Check what a map shows against the ground, and don't rely on any "
              "one device for safety. Mapsheet is not affiliated with TerraGo, Esri, the USGS or NRCan; GeoPDF is a registered trademark of TerraGo Technologies.")
PUBLISHER = {"@type": "Organization", "name": NAME, "url": BASE, "logo": BASE + "img/icon-512.png"}
HOME_TITLE = "Mapsheet: Offline PDF Maps with GPS for iPhone and iPad"
HOME_DESCRIPTION = ("Your position on geospatial PDF and GeoTIFF maps with no signal. Points, tracks, area measuring, UTM and MGRS, "
                    "crew packs. Free for 3 maps; work use included.")
SUMMARY = ("Mapsheet is an offline map app for iPhone and iPad that shows your GPS position on your own geospatial PDFs "
           "(including GeoPDF files) and GeoTIFFs, with no cell signal. Field crews in forestry, tree planting, wildland fire, "
           "survey and conservation use it to add points with photos, record tracks, measure areas, go to UTM or MGRS "
           "coordinates and send maps to a whole crew.")
FACTS = [
    "Free for up to 3 maps at a time (a multi-page atlas counts as one), with every field tool and GPX, KML and CSV export. Work use is allowed on every plan, including the free one.",
    "Mapsheet Field costs $59.99 a year (two weeks free for new subscribers) or $9.99 a month in the US: unlimited maps.",
    "Mapsheet Crew costs $129.99 a year (two weeks free for new subscribers) or $19.99 a month per person in the US (organizations can buy seats through Apple Business Manager): everything in Field plus crew packs (maps, points, tracks and photos sent as one file; the crew opens them free, keeping 3 maps at a time on the free plan or every map with Field), GPS averaging over 30 seconds with the standard error, and shapefile export.",
    "Maps never lock: if a plan ends, the user keeps every map and everything on it and only can't add maps past three.",
    "Opens geospatial PDFs from ArcGIS, QGIS, Global Mapper, the USGS and NRCan (both the ISO 32000 geospatial encoding and the OGC/TerraGo LGIDict encoding, including GeoPDF files, multi-page atlases and rotated pages), GeoTIFFs and TIFFs zipped with their world file, and zipped downloads.",
    "Coordinates: decimal degrees, degrees and minutes, degrees-minutes-seconds, UTM and MGRS/USNG, shown and typed. Understands UTM on common datums, Canada's provincial systems (MTM, Quebec and Ontario Lambert, BC Albers, Alberta 10TM), Australia's MGA zones, and any projection a map defines itself (WKT or GeoTIFF keys).",
    "Field tools: GPS position with accuracy and heading in airplane mode; Bluetooth GNSS receivers that provide location to iOS; points with symbols, colours, notes and photos; tracks that keep recording with the screen locked; lines and areas in metric or imperial units with draggable corners; distance and bearing to any point.",
    "Exports GPX, KML, KMZ and CSV (with UTM columns) on every plan, shapefiles on Crew; imports GPX, KML, KMZ, CSV and zipped shapefiles.",
    "Privacy: no account, no server and no analytics. Maps, points, tracks, photos and location stay on the device. App Store privacy label: Data Not Collected.",
    "Coming in version 1.1: adding maps from a link or a QR code (incident teams' map folders on the national fire file share, direct PDF/GeoTIFF links, Avenza-style map lists, link pages), a free map list (USGS US Topo and historical topos, Forest Service FSTopo, NRCan, NSW, Queensland, LINZ Topo50; each map downloads from its publisher), offline aerial and topo map downloads (USGS for the US, LINZ imagery for New Zealand), Crew seats bought by organizations through Apple Business Manager, an offline fire overlay (current perimeters, incidents and NASA satellite hotspots for the US, Canada, Australia and New Zealand, free on every plan, each with its age and source; US fires link to their incident's map folder on the public NIFC File Share), Crew nearby (phones share positions and points over Wi-Fi/Bluetooth with no internet or server; a lead on Crew starts it, anyone joins with a code), exporting a map with your features as a geospatial PDF (Field and Crew), an offline mode that blocks all internet use, a whole-library backup file to move maps to a new device, sending maps as plain files (original PDF plus KML) to people without Mapsheet, and a Settings line showing exactly when a plan renews or a trial turns into a charge, with a reminder two days before. The online features are optional: the core app never needs a connection.",
    "Runs on iPhone and iPad with iOS 17 or later, in English and French (Canada). Launched on the App Store in November 2026. The home page and privacy policy are also in French: " + BASE + "fr/",
]


def parse(path):
    _, head, body = path.read_text().split("---\n", 2)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    meta["slug"] = path.stem
    meta["related"] = [s.strip() for s in meta.get("related", "").split(",") if s.strip()]
    meta["body"] = body.strip()
    faq_block = re.search(r"## Frequently asked questions\n(.*?)(?=\n## |\Z)", body, re.S)
    meta["faqs"] = re.findall(r"### (.+?)\n\n(.+?)(?=\n\n###|\Z)", faq_block.group(1).strip(), re.S) if faq_block else []
    source_block = re.search(r"## Sources\n(.*)", body, re.S)
    meta["sources"] = re.findall(r"- \[(.+?)\]\((.+?)\)", source_block.group(1)) if source_block else []
    return meta


def render(text):
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"], extension_configs={"toc": {"toc_depth": "2"}})
    out = md.convert(text).replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out, [(t["id"], t["name"]) for t in md.toc_tokens]


def plain(text):
    return re.sub(r"<[^>]+>", "", re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)).replace("&gt;", ">").replace("&amp;", "&").strip()


def jsonld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


DISCLAIMER_FR = ("Mapsheet affiche la position donnée par le GPS de votre appareil. Vérifiez ce que montre une carte sur le terrain et ne "
                 "comptez jamais sur un seul appareil pour votre sécurité. Mapsheet n'est affilié ni à TerraGo, ni à Esri, ni à l'USGS, ni à RNCan; "
                 "GeoPDF est une marque déposée de TerraGo Technologies.")
CHROME = {
    "en": {"skip": "Skip to content", "how": "Features", "guides": "Guides", "support": "Support", "privacy": "Privacy",
           "get": "Get the app", "tagline": "Your own maps, offline, with you on them. iPhone and iPad.", "disclaimer": DISCLAIMER,
           "app": "App", "policy": "Privacy Policy", "terms": "Terms of Use", "other": ("fr", "Français"),
           "alt": "Mapsheet showing a GPS position on a topographic map, with points, a track and an area"},
    "fr": {"skip": "Aller au contenu", "how": "Fonctions", "guides": "Guides", "support": "Aide", "privacy": "Confidentialité",
           "get": "Obtenir l'app", "tagline": "Vos propres cartes, hors ligne, avec vous dessus. iPhone et iPad.", "disclaimer": DISCLAIMER_FR,
           "app": "Application", "policy": "Politique de confidentialité", "terms": "Conditions d'utilisation", "other": ("en", "English"),
           "alt": "Mapsheet affichant une position GPS sur une carte topographique, avec des points, une trace et une surface"},
}
# Pages that exist in both languages: (English path, French path) under BASE.
TWINS = {"index": ("", "fr/"), "privacy": ("privacy.html", "fr/confidentialite.html"), "terms": ("terms.html", "fr/conditions.html")}


def page(slug, title, description, body, *, schema=(), kind="article", current="", root="", markdown_twin=False,
         robots="index,follow,max-snippet:-1,max-image-preview:large", lang="en"):
    c = CHROME[lang]
    twin = TWINS.get(slug.removeprefix("fr/"))
    url = BASE + (twin[1] if lang == "fr" else twin[0]) if twin else (BASE if slug == "index" else f"{BASE}{slug}.html")
    hreflang = ""
    if twin:
        hreflang = (f'\n<link rel="alternate" hreflang="en" href="{BASE}{twin[0]}">'
                    f'\n<link rel="alternate" hreflang="fr-CA" href="{BASE}{twin[1]}">'
                    f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{twin[0]}">')
    # The other language: this page's twin, or the other language's home page.
    other = BASE + ((twin[0] if lang == "fr" else twin[1]) if twin else ("" if lang == "fr" else "fr/"))
    e = html.escape
    alternate = f'\n<link rel="alternate" type="text/markdown" href="{root}{slug}.md">' if markdown_twin else ""
    ld = "\n".join(jsonld(item) for item in schema)
    here = lambda name: ' aria-current="page"' if name == current else ""
    home = "./" if lang == "fr" else (root or "./")
    app = APP_FR if lang == "fr" else APP
    privacy_file = "confidentialite.html" if lang == "fr" else "privacy.html"
    terms_file = "conditions.html" if lang == "fr" else "terms.html"
    return f"""<!doctype html>
<html lang="{'fr-CA' if lang == 'fr' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<meta name="msvalidate.01" content="9BEF4B135A9025BA46678C081A6365D9">
<link rel="canonical" href="{url}">{alternate}{hreflang}
<meta name="theme-color" content="#f7f6f0">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(c["alt"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}icon.png">
<link rel="apple-touch-icon" href="{root}icon.png">
<link rel="stylesheet" href="{root}style.css">
<link rel="alternate" type="text/plain" title="llms.txt" href="{root}llms.txt">
{ld}
</head>
<body>
<a class="skip" href="#main">{c["skip"]}</a>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="{home}"><img src="{root}icon.png" alt="" width="34" height="34"><span>{NAME}</span></a>
    <nav class="nav" aria-label="Site">
      <a href="{home}#how"{here("home")}>{c["how"]}</a>
      <a href="{home}#guides"{here("guides")}>{c["guides"]}</a>
      <a href="{home}#support">{c["support"]}</a>
      <a href="{home if lang == "fr" else root}{privacy_file}"{here("privacy")}>{c["privacy"]}</a>
      <a href="{other}" hreflang="{"fr-CA" if c["other"][0] == "fr" else "en"}" lang="{"fr-CA" if c["other"][0] == "fr" else "en"}">{c["other"][1]}</a>
      <a class="nav-cta" href="{app}">{c["get"]}</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="in">
    <div class="foot-about">
      <a class="brand" href="{home}"><img src="{root}icon.png" alt="" width="28" height="28"><span>{NAME}</span></a>
      <p>{c["tagline"]}</p>
      <p>© 2026 {NAME}. {c["disclaimer"]}</p>
    </div>
    <nav aria-label="Guides"><p class="foot-title">{c["guides"]}</p>{FOOTER_GUIDES.replace('href="', f'href="{root}')}</nav>
    <nav aria-label="App"><p class="foot-title">{c["app"]}</p><a href="{app}">App Store</a><a href="{home}#support">{c["support"]}</a><a href="{home if lang == "fr" else root}{privacy_file}">{c["policy"]}</a><a href="{home if lang == "fr" else root}{terms_file}">{c["terms"]}</a><a href="{root}llms.txt">llms.txt</a></nav>
  </div>
</footer>
<script src="{root}site.js"></script>
</body>
</html>
"""


def guide_page(g, by_slug):
    body_md = re.sub(r"\n## Sources\n.*", "", g["body"], flags=re.S)
    content, headings = render(body_md)
    url = f'{BASE}{g["slug"]}.html'
    e = html.escape
    sources = "".join(f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in g["sources"])
    related = "".join(f'<li><a href="{s}.html">{e(by_slug[s]["h1"])}</a></li>' for s in g["related"])
    toc = "".join(f'<li><a href="#{i}">{e(n)}</a></li>' for i, n in headings)
    body = f"""<div class="guide">
<nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">/</span> <a href="./#guides">Guides</a> <span aria-hidden="true">/</span> <span>{e(g["nav"])}</span></nav>
<article>
<h1>{e(g["h1"])}</h1>
<p class="updated">Checked against its sources on <time datetime="{UPDATED}">{UPDATED_LONG}</time></p>
<div class="answer"><h2>Short answer</h2><p>{e(g["answer"])}</p></div>
<nav class="toc" aria-label="On this page"><p class="foot-title">On this page</p><ul>{toc}</ul></nav>
{content}
<aside class="app-cta">
  <div><h2>Your maps, with you on them</h2><p>Mapsheet shows your position on geospatial PDFs and GeoTIFFs with no signal: points, tracks, areas, UTM and MGRS. Free for 3 maps, on iPhone and iPad.</p></div>
  <a class="badge" href="{APP}"><img src="img/app-store-badge.svg" alt="Download on the App Store" width="150" height="50"></a>
</aside>
<section class="sources"><h2>Sources</h2><ul>{sources}</ul><p class="muted">Guides summarize public sources. Check a map and a position against the ground before you rely on them.</p></section>
<section class="related"><h2>Related guides</h2><ul>{related}</ul></section>
</article>
</div>"""
    crumbs = [("Home", BASE), ("Guides", BASE + "#guides"), (g["nav"], url)]
    schema = [
        {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["description"],
         "datePublished": UPDATED, "dateModified": UPDATED, "mainEntityOfPage": url, "image": BASE + "img/og.png",
         "author": PUBLISHER, "publisher": PUBLISHER, "inLanguage": "en-US", "citation": [u for _, u in g["sources"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    if g["faqs"]:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in g["faqs"]]})
    return page(g["slug"], g["title"], g["description"], body, schema=schema, current="guides", markdown_twin=True)


def guide_markdown(g):
    body = re.sub(r"\]\((?!https?:)([a-z0-9-]+)\.html\)", rf"]({BASE}\1.md)", g["body"])
    return f"""# {g["h1"]}

> {g["answer"]}

Source page: {BASE}{g["slug"]}.html
Checked against its sources on {UPDATED_LONG}. Published by {NAME}, an offline PDF map app with GPS for iPhone and iPad.

{body}
"""




def social_card():
    """img/og.png: 1200x630, paper-coloured, the app's name and promise beside the first App Store screenshot."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), (247, 246, 240))
    d = ImageDraw.Draw(card)
    font = lambda size, bold=True: ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=1 if bold else 0)
    icon = Image.open(ROOT / "img" / "icon-512.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    mask = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 95, 95), 22, fill=255)
    card.paste(icon, (72, 76), mask)
    d.text((186, 96), NAME, font=font(56), fill=(12, 21, 32))
    y = 232
    for line in ["Your own maps, offline,", "with you on them."]:
        d.text((72, y), line, font=font(56), fill=(13, 107, 74) if line.startswith("with") else (12, 21, 32))
        y += 70
    d.text((72, y + 26), "GPS on geospatial PDFs and GeoTIFFs", font=font(30, False), fill=(91, 102, 112))
    d.text((72, y + 66), "for field crews. iPhone and iPad.", font=font(30, False), fill=(91, 102, 112))
    shot = Image.open(ROOT / "img" / "map.jpg").convert("RGB")
    sw = 300
    shot = shot.resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((W - sw - 90 + 6, 48 + 18, W - 90 + 6, 48 + shot.height + 18), 36, fill=70)
    from PIL import ImageFilter
    card.paste((205, 210, 200), (0, 0), shadow.filter(ImageFilter.GaussianBlur(22)))
    smask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(smask).rounded_rectangle((0, 0, shot.width - 1, shot.height - 1), 36, fill=255)
    card.paste(shot, (W - sw - 90, 48), smask)
    card.save(ROOT / "img" / "og.png", optimize=True)


# The icon at 512 for structured data and the card, from the app's 1024 artwork when it's beside this repo.
art = Path.home() / "mapsheet-app" / "App" / "Assets.xcassets" / "AppIcon.appiconset" / "icon-1024.png"
if art.exists():
    Image.open(art).convert("RGB").resize((512, 512), Image.LANCZOS).save(ROOT / "img" / "icon-512.png", optimize=True)
    Image.open(art).convert("RGB").resize((180, 180), Image.LANCZOS).save(ROOT / "img" / "icon.png", optimize=True)
    Image.open(art).convert("RGB").resize((180, 180), Image.LANCZOS).save(ROOT / "icon.png", optimize=True)   # favicon and touch icon
social_card()

guides = [parse(p) for p in sorted((PAGES / "guides").glob("*.md"))]
order = ["what-is-a-geospatial-pdf", "free-topo-maps-as-geospatial-pdf", "utm-and-mgrs-coordinates-explained", "phone-gps-accuracy-in-the-field"]
guides.sort(key=lambda g: order.index(g["slug"]) if g["slug"] in order else len(order))
by_slug = {g["slug"]: g for g in guides}
FOOTER_GUIDES = "".join(f'<a href="{g["slug"]}.html">{html.escape(g["nav"])}</a>' for g in guides)

for g in guides:
    (ROOT / f'{g["slug"]}.html').write_text(guide_page(g, by_slug))
    (ROOT / f'{g["slug"]}.md').write_text(guide_markdown(g))

# Home
cards = "".join(f'<li><a href="{g["slug"]}.html"><strong>{html.escape(g["h1"])}</strong><span>{html.escape(g["description"])}</span></a></li>' for g in guides)
home = (PAGES / "home.html").read_text().replace("{APP}", APP).replace("{GUIDES}", f'<ul class="guides">{cards}</ul>')
faqs = re.findall(r"<details><summary>(.+?)</summary><p>(.+?)</p></details>", home)
SHOTS = ["map", "point", "edit", "features"]
home_schema = [
    {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE, "description": HOME_DESCRIPTION, "publisher": PUBLISHER, "inLanguage": "en-US"},
    {"@context": "https://schema.org", "@type": "MobileApplication", "name": APP_NAME, "alternateName": NAME, "url": BASE,
     "installUrl": APP, "downloadUrl": APP, "operatingSystem": "iOS 17.0 or later", "applicationCategory": "TravelApplication",
     "applicationSubCategory": "Navigation", "description": SUMMARY, "image": BASE + "img/icon-512.png",
     "screenshot": [BASE + f"img/{n}.jpg" for n in SHOTS],
     "featureList": ["GPS position on geospatial PDFs and GeoTIFFs, offline", "Points with symbols, notes and photos",
                     "Track recording with the screen locked", "Line and area measuring with editable corners",
                     "Distance and bearing to a point", "UTM, MGRS/USNG and lat/lon coordinates",
                     "GPX, KML, KMZ and CSV export and import", "Crew packs (Crew)", "GPS averaging (Crew)", "Shapefile export (Crew)"],
     "inLanguage": ["en", "fr-CA"], "publisher": PUBLISHER,
     "offers": [{"@type": "Offer", "name": "Mapsheet (free, 3 maps at a time)", "price": "0", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Mapsheet Field, yearly", "price": "59.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Mapsheet Field, monthly", "price": "9.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Mapsheet Crew, yearly", "price": "129.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Mapsheet Crew, monthly", "price": "19.99", "priceCurrency": "USD"}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]},
]
(ROOT / "index.html").write_text(page("index", HOME_TITLE, HOME_DESCRIPTION, home, schema=home_schema, kind="website", current="home"))

# Privacy keeps its URL: the app and App Store Connect link to it.
privacy = (PAGES / "privacy.body.html").read_text()
(ROOT / "privacy.html").write_text(page("privacy", f"Privacy Policy · {NAME}", "Mapsheet has no account, no server and no analytics: your maps, points, tracks, photos and location stay on your device.",
                                        f'<div class="doc">\n{privacy}</div>', current="privacy", schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"{NAME} privacy policy", "url": f"{BASE}privacy.html",
     "dateModified": UPDATED, "publisher": PUBLISHER, "inLanguage": "en-US",
     "about": {"@type": "MobileApplication", "name": APP_NAME, "url": BASE}}]))

terms = (PAGES / "terms.body.html").read_text()
(ROOT / "terms.html").write_text(page("terms", f"Terms of Use · {NAME}", "Mapsheet's terms: a map viewer, maps from others provided as is, optional online features, and limits of liability.",
                                      f'<div class="doc">\n{terms}</div>', schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"{NAME} terms of use", "url": f"{BASE}terms.html",
     "dateModified": "2026-11-09", "publisher": PUBLISHER, "inLanguage": "en-US"}]))

# French (for Quebec and New Brunswick crews): the home page and the privacy policy, under fr/. The guides stay in English.
FR = ROOT / "fr"
FR.mkdir(exist_ok=True)
cards_fr = "".join(f'<li><a href="../{g["slug"]}.html" hreflang="en"><strong>{html.escape(g["h1"])}</strong><span>{html.escape(g["description"])}</span></a></li>' for g in guides)
home_fr = (PAGES / "home.fr.html").read_text().replace("{APP}", APP_FR).replace("{GUIDES}", f'<ul class="guides">{cards_fr}</ul>')
faqs_fr = re.findall(r"<details><summary>(.+?)</summary><p>(.+?)</p></details>", home_fr)
HOME_TITLE_FR = "Mapsheet : cartes PDF hors ligne et GPS pour iPhone et iPad"
HOME_DESCRIPTION_FR = ("Votre position sur des PDF géoréférencés et des GeoTIFF, sans réseau. Points, traces, mesure de surfaces, UTM et MGRS, "
                       "paquets d'équipe. Gratuit pour 3 cartes.")
(FR / "index.html").write_text(page("fr/index", HOME_TITLE_FR, HOME_DESCRIPTION_FR, home_fr, kind="website", current="home", root="../", lang="fr", schema=[
    {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + "fr/", "description": HOME_DESCRIPTION_FR, "publisher": PUBLISHER, "inLanguage": "fr-CA"},
    {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "fr-CA", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs_fr]}]))
privacy_fr = (PAGES / "privacy.body.fr.html").read_text()
(FR / "confidentialite.html").write_text(page("fr/privacy", f"Politique de confidentialité · {NAME}",
                                      "Mapsheet n'a ni compte, ni serveur, ni analyse : vos cartes, points, traces, photos et votre position restent sur l'appareil.",
                                      f'<div class="doc">\n{privacy_fr}</div>', current="privacy", root="../", lang="fr", schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"Politique de confidentialité de {NAME}", "url": f"{BASE}fr/confidentialite.html",
     "dateModified": UPDATED, "publisher": PUBLISHER, "inLanguage": "fr-CA", "about": {"@type": "MobileApplication", "name": APP_NAME, "url": BASE}}]))

terms_fr = (PAGES / "terms.body.fr.html").read_text()
(FR / "conditions.html").write_text(page("fr/terms", f"Conditions d'utilisation · {NAME}",
                                         "Les conditions de Mapsheet : un visualiseur de cartes, des cartes de tiers fournies telles quelles, des fonctions en ligne facultatives et des limites de responsabilité.",
                                         f'<div class="doc">\n{terms_fr}</div>', root="../", lang="fr", schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"Conditions d'utilisation de {NAME}", "url": f"{BASE}fr/conditions.html",
     "dateModified": "2026-11-09", "publisher": PUBLISHER, "inLanguage": "fr-CA"}]))

# 404 is served at any depth, so its links are absolute.
missing = '<div class="doc"><h1>Page not found</h1><p>That page has moved or never existed.</p><p><a href="/mapsheet-site/">Go to Mapsheet\'s home page</a> or read <a href="/mapsheet-site/what-is-a-geospatial-pdf.html">what makes a PDF geospatial</a>.</p></div>'
(ROOT / "404.html").write_text(page("404", f"Page not found · {NAME}", "This page could not be found.", missing, robots="noindex", root="/mapsheet-site/"))

# Sitemap
urls = ([(BASE, "1.0"), (f"{BASE}fr/", "0.9")] + [(f'{BASE}{g["slug"]}.html', "0.8") for g in guides]
        + [(f"{BASE}privacy.html", "0.3"), (f"{BASE}fr/confidentialite.html", "0.3"), (f"{BASE}terms.html", "0.3"), (f"{BASE}fr/conditions.html", "0.3")])
entries = "".join(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n')
# robots.txt only counts at a host's root, so on github.io this copy is a pointer for tools that read it here; the sitemap
# is submitted to the search engines directly.
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

# llms.txt and the full text for AI tools
facts = "\n".join(f"- {f}" for f in FACTS)
links = "\n".join(f'- [{g["h1"]}]({BASE}{g["slug"]}.md): {g["description"]}' for g in guides)
(ROOT / "llms.txt").write_text(f"""# {NAME}

> {SUMMARY}

{DISCLAIMER} Facts on this site were checked on {UPDATED_LONG}. When citing a guide, link its page.

## Key facts

{facts}

## Guides

{links}

## App

- [App Store listing]({APP}): {APP_NAME}, for iPhone and iPad, iOS 17 or later
- [Home page]({BASE}): What Mapsheet does, plans, questions and support
- [Privacy Policy]({BASE}privacy.html): No account, no server, no analytics; everything stays on the device
- [Terms of Use]({BASE}terms.html): Mapsheet's terms (map data as is, optional online features, limits of liability), on top of Apple's standard license agreement ({TERMS})

## Optional

- [Full text]({BASE}llms-full.txt): The facts, the questions and answers, every guide and the privacy policy in one Markdown file
""")
qa = "\n\n".join(f"### {plain(q)}\n\n{plain(a)}" for q, a in faqs)
privacy_md = re.sub(r"<li>", "- ", privacy)
privacy_md = re.sub(r"<h2>(.+?)</h2>", r"## \1", privacy_md)
privacy_md = re.sub(r"<h1>(.+?)</h1>", r"", privacy_md)
privacy_md = "\n".join(l.strip() for l in plain(privacy_md.replace("laddothis at gmail dot com", "laddothis@gmail.com")).splitlines() if l.strip())
privacy_md = re.sub(r"\n(## )", r"\n\n\1", privacy_md)
full = [f"# {NAME}\n\n> {SUMMARY}\n\n{DISCLAIMER} Checked on {UPDATED_LONG}. Source: {BASE}\n\n## Key facts\n\n{facts}\n\n## Questions and answers\n\n{qa}"]
full += [guide_markdown(g) for g in guides]
full.append(f"# Mapsheet privacy policy\n\nSource page: {BASE}privacy.html\n\n{privacy_md}\n")
(ROOT / "llms-full.txt").write_text("\n\n---\n\n".join(full))
(ROOT / ".nojekyll").write_text("")
print(f"built home, privacy, their French pages, 404 and {len(guides)} guides")
