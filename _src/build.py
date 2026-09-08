# -*- coding: utf-8 -*-
"""Generator strony JA-HO.

Zapisuje pięć statycznych podstron do ../www/. Szablony (nagłówek, stopka,
pasek CTA) siedzą tutaj, żeby nie rozjechały się między stronami.

    python3 _src/build.py
"""
import html
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.normpath(os.path.join(HERE, "..", "www"))

from data import (COMPANY, NAV, CLIENTS, JOINERY, SERVICES, PROCESS,
                  CATEGORIES, SPONSORSHIP, FUNDING, TIMELINE, STATS, FAQ)

C = COMPANY
YEAR = date.today().year


# ---------------------------------------------------------------- pomocnicze
def e(s):
    return html.escape(str(s), quote=True)


def cat(slug):
    for c in CATEGORIES:
        if c["slug"] == slug:
            return c
    raise KeyError(slug)


def photo_order(c):
    """Najlepsze ujęcia z przodu, reszta numerycznie."""
    seen, out = set(), []
    for n in c["order"]:
        if 1 <= n <= c["count"] and n not in seen:
            out.append(n); seen.add(n)
    for n in range(1, c["count"] + 1):
        if n not in seen:
            out.append(n)
    return out


TOTAL_PHOTOS = sum(c["count"] for c in CATEGORIES)

# Polska typografia: spójników i przyimków jednoliterowych nie zostawia się na
# końcu wiersza. Doklejamy twardą spację — ale wyłącznie w treści, nigdy
# wewnątrz znaczników ani w <script>/<style>.
_PL_ONE_LETTER = re.compile(
    r"(?<![\w&#;])([aiouwzAIOUWZ]) (?=[0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])")


def pl_typo(doc):
    out, skip = [], False
    for part in re.split(r"(<[^>]+>)", doc):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<script", "<style")):
                skip = True
            elif low.startswith(("</script", "</style")):
                skip = False
            out.append(part)
        else:
            out.append(part if skip else _PL_ONE_LETTER.sub(r"\1&nbsp;", part))
    return "".join(out)


def _json(s):
    """Minimalny literał JSON do bloków LD."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


# ---------------------------------------------------------------- ikony
IC = {
  "check":  "<path d='M20 6 9 17l-5-5'/>",
  "arrow":  "<path d='M5 12h14'/><path d='m12 5 7 7-7 7'/>",
  "phone":  "<path d='M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z'/>",
  "mail":   "<rect width='20' height='16' x='2' y='4' rx='2'/><path d='m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'/>",
  "pin":    "<path d='M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z'/><circle cx='12' cy='10' r='3'/>",
  "chev":   "<path d='m6 9 6 6 6-6'/>",
  "close":  "<path d='M18 6 6 18'/><path d='m6 6 12 12'/>",
  "left":   "<path d='m15 18-6-6 6-6'/>",
  "right":  "<path d='m9 18 6-6-6-6'/>",
  "up":     "<path d='m18 15-6-6-6 6'/>",
  "zoom":   "<circle cx='11' cy='11' r='7'/><path d='m21 21-4.3-4.3'/><path d='M11 8v6'/><path d='M8 11h6'/>",
  "sun":    "<circle cx='12' cy='12' r='4'/><path d='M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41'/>",
  "moon":   "<path d='M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z'/>",
  "window": "<rect width='18' height='18' x='3' y='3' rx='1'/><path d='M3 12h18M12 3v18'/>",
  "trowel": "<path d='M3 21 8 16'/><path d='m6.5 13.5 4 4'/><path d='M12.5 3.5 20.5 11.5a1 1 0 0 1 0 1.4l-3.6 3.6a1 1 0 0 1-1.4 0L7.5 8.5z'/>",
  "ruler":  "<path d='M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4z'/><path d='m7.5 10.5 2 2M10.5 7.5l2 2M13.5 4.5l2 2M4.5 13.5l2 2'/>",
  "brush":  "<path d='M9.06 11.9 3.6 17.36a2.5 2.5 0 0 0 3.54 3.54l5.46-5.46'/><path d='M14 6.5 17.5 10'/><path d='M20.4 3.6a2 2 0 0 0-2.8 0L9 12.2l2.8 2.8 8.6-8.6a2 2 0 0 0 0-2.8z'/>",
  "layers": "<path d='m12 2 9 5-9 5-9-5 9-5z'/><path d='m3 12 9 5 9-5'/><path d='m3 17 9 5 9-5'/>",
  "plug":   "<path d='M12 22v-5'/><path d='M9 7V2M15 7V2'/><path d='M6 7h12v4a6 6 0 0 1-12 0V7z'/>",
  "grid":   "<rect width='7' height='7' x='3' y='3' rx='1'/><rect width='7' height='7' x='14' y='3' rx='1'/><rect width='7' height='7' x='14' y='14' rx='1'/><rect width='7' height='7' x='3' y='14' rx='1'/>",
  "users":  "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><path d='M22 21v-2a4 4 0 0 0-3-3.87'/><path d='M16 3.13a4 4 0 0 1 0 7.75'/>",
  "award":  "<circle cx='12' cy='8' r='6'/><path d='m8.2 13.9-1.3 7.1L12 18l5.1 3-1.3-7.1'/>",
}
# Ikona dla każdej grupy prac, po id z data.py.
SVC_IC = {"wycena": "ruler", "murarskie": "trowel", "glazura": "grid",
          "malarskie": "brush", "gipsowe": "layers", "stolarskie": "window",
          "instalacje": "plug"}


def icon(name, size=20, cls=""):
    k = ' class="%s"' % cls if cls else ""
    return ("<svg%s width='%d' height='%d' viewBox='0 0 24 24' fill='none' "
            "stroke='currentColor' stroke-width='1.75' stroke-linecap='round' "
            "stroke-linejoin='round' aria-hidden='true'>%s</svg>"
            % (k, size, size, IC[name]))


LOGO_MARK = """<svg class="brand__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">
  <path class="mk-frame" d="M20 2.6 34.6 11v18L20 37.4 5.4 29V11z" stroke="currentColor"
        stroke-width="1.7" stroke-linejoin="round" opacity=".38"/>
  <path class="mk-roof" d="M10.5 20.4 20 12.6l9.5 7.8" stroke="var(--c-brand)"
        stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="13.4" y="23" width="13.2" height="3.1" rx=".7" fill="var(--c-brick)"/>
  <rect x="15.6" y="27.4" width="8.8" height="2.6" rx=".7" fill="var(--c-brick)" opacity=".6"/>
</svg>"""


def btn(label, href, kind="", icon_name="arrow", magnetic=False, attrs=""):
    cls = "btn" + ((" " + kind) if kind else "")
    mag = " data-magnetic" if magnetic else ""
    ic = ('<span class="btn__icon">%s</span>' % icon(icon_name, 17)) if icon_name else ""
    return ('<a class="%s" href="%s"%s%s><span class="btn__ripple"></span>'
            '<span>%s</span>%s</a>' % (cls, e(href), mag, attrs, e(label), ic))


# ---------------------------------------------------------------- szkielet
def head(title, desc, page, extra=""):
    canon = C["domain"] + "/" + ("" if page == "index.html" else page)
    return """<!doctype html>
<html lang="pl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#faf8f5">
<meta name="author" content="{legal}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{name} — {descriptor}">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{domain}/assets/img/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Siedziba firmy JA-HO w Lublinie">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{domain}/assets/img/og-cover.jpg">

<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
<script>
/* Ustawia motyw zanim przeglądarka cokolwiek namaluje (brak błysku złego tła).
   Czyta zapisany WYBÓR; jego brak = podążamy za ustawieniem systemu. */
(function(){{
  var r = document.documentElement, wybor = null;
  r.className = "js";
  try {{ wybor = localStorage.getItem("jaho-theme"); }} catch (err) {{}}
  if (wybor === "dark" || wybor === "light") r.setAttribute("data-theme", wybor);
  var ciemny = wybor ? wybor === "dark"
                     : window.matchMedia("(prefers-color-scheme: dark)").matches;
  var m = document.querySelector('meta[name="theme-color"]');
  if (m) m.content = ciemny ? "#14100e" : "#faf8f5";
}})();
</script>
{extra}
</head>
<body>
<a class="skip-link" href="#main">Przejdź do treści</a>
""".format(title=e(title), desc=e(desc), canon=e(canon), name=e(C["name"]),
           descriptor=e(C["descriptor"]), legal=e(C["legal"]),
           domain=e(C["domain"]), extra=extra)


def header(page):
    links = "".join(
        '<a class="nav__link" href="%s"%s>%s</a>' %
        (e(h), ' aria-current="page"' if h == page else "", e(t))
        for h, t in NAV)

    sheet_links = "".join(
        '<a class="sheet__link" href="%s" style="--i:%d"%s>%s<span>%02d</span></a>' %
        (e(h), i, ' aria-current="page"' if h == page else "", e(t), i + 1)
        for i, (h, t) in enumerate(NAV))

    return """<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="index.html" aria-label="{name} — {descriptor}, strona główna">
      {mark}
      <span class="brand__text">
        <span class="brand__name">{name}</span>
        <span class="brand__sub">od {founded} roku</span>
      </span>
    </a>

    <nav class="nav" aria-label="Główna">
      <span class="nav__pill" aria-hidden="true"></span>
      {links}
    </nav>

    <div class="hdr__actions">
      <button class="iconbtn themebtn" type="button" data-theme-toggle
              aria-label="Zmień motyw">
        <span class="ic-sun">{sun}</span><span class="ic-moon">{moon}</span>
      </button>
      <a class="btn btn--sm hdr__cta" href="tel:{mobile_href}">
        <span class="btn__ripple"></span>
        <span class="btn__icon btn--phone">{phone}</span><span>{mobile}</span>
      </a>
      <button class="iconbtn burger" type="button" aria-expanded="false"
              aria-controls="mobile-nav" aria-label="Otwórz menu">
        <span class="burger__box"><i></i><i></i><i></i></span>
      </button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"></div>
</header>

<div class="sheet" id="mobile-nav">
  <div class="sheet__scrim"></div>
  <div class="sheet__panel">
    <div class="wrap">
      <nav aria-label="Mobilna">{sheet_links}</nav>
      <div class="sheet__foot">
        <a class="btn btn--block" href="tel:{mobile_href}"><span class="btn__ripple"></span>
          <span class="btn__icon btn--phone">{phone}</span><span>Zadzwoń: {mobile}</span></a>
        <a class="btn btn--outline btn--block" href="mailto:{mail}"><span class="btn__ripple"></span>
          <span class="btn__icon">{mailic}</span><span>Napisz e-mail</span></a>
      </div>
    </div>
  </div>
</div>
""".format(name=e(C["name"]), descriptor=e(C["descriptor"]), founded=C["founded"],
           mark=LOGO_MARK, links=links, sheet_links=sheet_links,
           sun=icon("sun", 19), moon=icon("moon", 19), phone=icon("phone", 16),
           mailic=icon("mail", 17), mobile=e(C["mobile"]),
           mobile_href=e(C["mobile_href"]), mail=e(C["email"]))


def cta_band():
    return """<section class="cta">
  <div class="wrap cta__in">
    <div class="cta__text" data-reveal>
      <span class="eyebrow eyebrow--deep">Bezpłatne oględziny i wycena</span>
      <h2 class="t-h2">Masz projekt do wyceny?</h2>
      <p class="t-lead">Dokonujemy oględzin, pomiarów i wyceny wstępnej. Zadzwoń
        albo napisz — odpowiadamy na każde zapytanie w ciągu 24&nbsp;godzin.</p>
    </div>
    <div class="stack" data-reveal>
      <a class="telbig" href="tel:{mobile_href}">
        <span class="telbig__ic">{phone}</span><span>{mobile}</span>
      </a>
      <div class="btn-row">
        {b1}
        {b2}
      </div>
    </div>
  </div>
</section>""".format(mobile_href=e(C["mobile_href"]), mobile=e(C["mobile"]),
                     phone=icon("phone", 21),
                     b1=btn("Formularz kontaktowy", "contact.html", "btn--onDeep", magnetic=True),
                     b2=btn("Napisz e-mail", "mailto:" + C["email"], "btn--onDeep-outline", "mail"))


def footer():
    nav_links = "".join('<li><a href="%s">%s</a></li>' % (e(h), e(t)) for h, t in NAV)
    top_cats = "".join(
        '<li><a href="projects.html#%s">%s</a></li>' % (e(c["slug"]), e(c["name"]))
        for c in CATEGORIES[:5])

    return """<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="brand" href="index.html" aria-label="{name}, strona główna">
          {mark}
          <span class="brand__text">
            <span class="brand__name">{name}</span>
            <span class="brand__sub">{descriptor}</span>
          </span>
        </a>
        <p class="ftr__about">Kompleksowe usługi remontowo-budowlane i stolarka
          budowlana na terenie Lublina i całego województwa lubelskiego —
          nieprzerwanie od {founded} roku.</p>
      </div>

      <nav aria-label="Stopka">
        <h4>Nawigacja</h4>
        <ul>{nav_links}</ul>
      </nav>

      <div>
        <h4>Kategorie realizacji</h4>
        <ul>{top_cats}</ul>
      </div>
    </div>

    <div class="ftr__grid" style="margin-top:var(--s-7)">
      <div>
        <h4>Kontakt</h4>
        <ul>
          <li><a href="tel:{mobile_href}">{phone}{mobile}</a></li>
          <li><a href="tel:{phone_href}">{phone2}{tel}</a></li>
          <li><a href="mailto:{mail}">{mailic}{mail}</a></li>
          <li><span style="display:inline-flex;gap:var(--s-2);align-items:flex-start;font-size:.9375rem">{pin}{street}, {postcode}</span></li>
        </ul>
      </div>
      <div>
        <h4>Firma</h4>
        <ul>
          <li>{legal}</li>
          <li>{person}, {role}</li>
          <li>Działamy od {founded} roku</li>
        </ul>
      </div>
      <div>
        <h4>Ponadto</h4>
        <ul>
          <li><a href="about.html#dofinansowanie">Dofinansowanie ze środków FUS</a></li>
          <li><a href="about.html#sponsoring">Sponsoring Budowlanych Lublin</a></li>
          <li><a href="services.html#faq">Najczęstsze pytania</a></li>
        </ul>
      </div>
    </div>

    <div class="ftr__bar">
      <p>&copy; 2011–{year} {legal} — {descriptor}. Wszelkie prawa zastrzeżone.</p>
      <p>{street}, {postcode}</p>
    </div>
  </div>
</footer>

<button class="totop" type="button" aria-label="Powrót na górę">{up}</button>
<script src="assets/js/site.js" defer></script>
</body>
</html>""".format(
        name=e(C["name"]), mark=LOGO_MARK, legal=e(C["legal"]),
        descriptor=e(C["descriptor"]), founded=C["founded"], year=YEAR,
        nav_links=nav_links, top_cats=top_cats,
        mobile=e(C["mobile"]), mobile_href=e(C["mobile_href"]),
        tel=e(C["phone"]), phone_href=e(C["phone_href"]), mail=e(C["email"]),
        street=e(C["street"]), postcode=e(C["postcode"]),
        person=e(C["person"]), role=e(C["role"]),
        phone=icon("phone", 15), phone2=icon("phone", 15), mailic=icon("mail", 15),
        pin=icon("pin", 15), up=icon("up", 19))


# ---------------------------------------------------------------- fragmenty
def jsonld(extra_nodes=None):
    """Graf Organization + WebSite + strona szczegółowa."""
    services = ", ".join(s["name"] for s in SERVICES)
    nodes = ["""{
    "@type": "GeneralContractor",
    "@id": "%(dom)s/#org",
    "name": "F.R.B. JA-HO",
    "alternateName": "%(name)s",
    "url": "%(dom)s/",
    "image": "%(dom)s/assets/img/og-cover.jpg",
    "logo": "%(dom)s/assets/img/logo-mark.png",
    "email": "%(mail)s",
    "telephone": "%(mobile_href)s",
    "foundingDate": "1999-06",
    "slogan": %(slogan)s,
    "description": "Kompleksowe usługi remontowo-budowlane i stolarka budowlana na terenie województwa lubelskiego. Firma działa od 1999 roku.",
    "founder": { "@type": "Person", "name": "Mirosław Gieracz" },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "%(street)s",
      "addressLocality": "Lublin",
      "postalCode": "20-081",
      "addressRegion": "lubelskie",
      "addressCountry": "PL"
    },
    "areaServed": { "@type": "AdministrativeArea", "name": "województwo lubelskie" },
    "knowsAbout": %(services)s,
    "sameAs": ["%(dom)s/"]
  }""" % dict(dom=C["domain"], name=C["name"], mail=C["email"],
              mobile_href=C["mobile_href"], slogan=_json(C["slogan"]),
              street=C["street"], services=_json(services))]

    nodes.append("""{
    "@type": "WebSite",
    "@id": "%s/#site",
    "url": "%s/",
    "name": "JA-HO — firma remontowo-budowlana",
    "inLanguage": "pl",
    "publisher": { "@id": "%s/#org" }
  }""" % (C["domain"], C["domain"], C["domain"]))

    if extra_nodes:
        nodes.extend(extra_nodes)
    return ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n'
            '  "@graph": [\n  %s\n  ]\n}\n</script>' % ",\n  ".join(nodes))


def banner(title, lead, page_title):
    crumb = ('<nav class="crumbs" aria-label="Okruszki"><ol>'
             '<li><a href="index.html">Start</a></li>'
             '<li><span aria-current="page">%s</span></li></ol></nav>' % e(page_title))
    return """<section class="banner">
  <div class="banner__hex" aria-hidden="true"></div>
  <div class="wrap banner__in">
    {crumb}
    <h1 class="t-h1">{title}</h1>
    <p class="t-lead">{lead}</p>
  </div>
</section>""".format(crumb=crumb, title=e(title), lead=e(lead))


def stats_block(deep=False):
    out = []
    for n, suf, k, d in STATS:
        sup = '<sup>%s</sup>' % e(suf) if suf else ""
        out.append("""<div class="stat">
      <div class="stat__n"><span data-count="{n}">{n}</span>{sup}</div>
      <div class="stat__k">{k}</div>
      <p class="stat__d">{d}</p>
    </div>""".format(n=e(n), sup=sup, k=e(k), d=e(d)))
    return '<div class="stats" data-reveal-group>%s</div>' % "".join(out)


# Ile razy powtórzyć zestaw logotypów. Musi być PARZYSTE (pętla przesuwa
# ścieżkę o -50%, więc obie połowy muszą być identyczne) i na tyle duże, żeby
# połowa ścieżki była szersza niż okno — inaczej na końcu cyklu po prawej
# stronie widać pustkę. Sześć logotypów to ok. 620 px + 6 odstępów; przy sześciu
# przebiegach połowa ma 2580–3300 px, czyli z zapasem powyżej typowego ekranu.
MARQUEE_RUNS = 6


def client_marquee(deep=False):
    """Parzysta liczba identycznych przebiegów — patrz MARQUEE_RUNS."""
    run = []
    for cl in CLIENTS:
        # Zawsze białe wersje z mono/. CSS odwraca je na jasnym tle, dzięki czemu
        # wszystkie sześć ma jedną gęstość; kolorowe oryginały mają skrajnie różną
        # jasność, a jeden z nich jest biały na białym.
        src = "assets/img/partnerzy/mono/%s.webp" % cl["file"]
        run.append(
            '<div class="marquee__item"><img src="%s" alt="%s" width="%d" height="%d" '
            'loading="lazy" decoding="async" style="height:%dpx"></div>'
            % (e(src), e(cl["name"]), cl["w"], cl["h"], cl["h"]))
    one_run = '<div class="marquee__run">%s</div>' % "".join(run)
    cls = "marquee marquee--deep" if deep else "marquee"
    names = "; ".join("%s (%s)" % (c["name"], c["sector"]) for c in CLIENTS)
    return ('<div class="%s"><p class="sr-only">Klienci: %s.</p>'
            '<div class="marquee__track" aria-hidden="true">%s</div></div>'
            % (cls, e(names), one_run * MARQUEE_RUNS))


def shot(c, n, lazy=True, sizes="(min-width:1200px) 300px, (min-width:760px) 33vw, 50vw"):
    thumb = "assets/img/thumb/%s/%d.webp" % (c["slug"], n)
    full = "assets/img/full/%s/%d.webp" % (c["slug"], n)
    alt = "%s — zdjęcie z realizacji JA-HO nr %d" % (c["name"], n)
    return ('<button class="shot" type="button" data-cat="%s" data-cat-name="%s" '
            'data-full="%s" aria-label="Powiększ: %s">'
            '<img src="%s" alt="%s" width="560" height="420" loading="%s" '
            'decoding="async" sizes="%s">'
            '<span class="shot__zoom">%s</span>'
            '<span class="shot__cap">%s</span></button>'
            % (e(c["slug"]), e(c["name"]), e(full), e(alt), e(thumb), e(alt),
               "lazy" if lazy else "eager", e(sizes), icon("zoom", 15), e(c["name"])))


def lightbox():
    return """<div class="lb" role="dialog" aria-modal="true" aria-label="Zdjęcie z realizacji"
     aria-hidden="true">
  <figure class="lb__fig">
    <button class="iconbtn lb__close" type="button" aria-label="Zamknij">{close}</button>
    <img class="lb__img" alt="">
    <figcaption class="lb__cap"></figcaption>
  </figure>
  <button class="lb__nav lb__nav--prev" type="button" aria-label="Poprzednie zdjęcie">{left}</button>
  <button class="lb__nav lb__nav--next" type="button" aria-label="Następne zdjęcie">{right}</button>
  <p class="lb__count" aria-live="polite"></p>
</div>""".format(close=icon("close", 20), left=icon("left", 22), right=icon("right", 22))


def contact_aside():
    rows = [
        ("phone", "Telefon komórkowy", C["mobile"], "tel:" + C["mobile_href"]),
        ("phone", "Telefon stacjonarny", C["phone"], "tel:" + C["phone_href"]),
        ("mail", "E-mail", C["email"], "mailto:" + C["email"]),
        ("pin", "Adres", C["street"] + ", " + C["postcode"], None),
    ]
    out = []
    for ic, k, v, href in rows:
        tag = "a" if href else "div"
        attr = ' href="%s"' % e(href) if href else ""
        out.append('<%s class="cinfo__row"%s><span class="cinfo__ic">%s</span>'
                   '<span><span class="cinfo__k">%s</span>'
                   '<span class="cinfo__v">%s</span></span></%s>'
                   % (tag, attr, icon(ic, 18), e(k), e(v), tag))
    return "".join(out)


def steps_block():
    return "".join(
        '<div class="step" style="--i:%d"><span class="step__bar"></span>'
        '<h3 class="t-h4">%s</h3><p>%s</p></div>' % (i, e(t), e(d))
        for i, (t, d) in enumerate(PROCESS))


# ---------------------------------------------------------------- podstrony
def page_index():
    line1 = " ".join('<span class="w"><i style="--i:%d">%s</i></span>' % (i, w)
                     for i, w in enumerate(["Budujemy", "lubelskie"]))
    line2 = " ".join('<span class="w"><i style="--i:%d">%s</i></span>' % (i + 2, w)
                     for i, w in enumerate(["od", "27", "lat."]))

    feat = ["jednorodzinne", "zabytki", "hale", "biura", "banki", "wielorodzinne"]
    tiles = []
    for slug in feat:
        c = cat(slug)
        tiles.append(
            '<a class="tile" href="projects.html#%s">'
            '<img src="assets/img/thumb/%s/%d.webp" alt="%s — realizacja JA-HO" '
            'width="560" height="420" loading="lazy" decoding="async">'
            '<span class="tile__body"><span class="tile__name">%s</span>'
            '<span class="tile__n">%d zdjęć</span></span></a>'
            % (e(slug), e(slug), c["cover"], e(c["name"]), e(c["name"]), c["count"]))

    pillar_cards = """<article class="pillar" data-reveal>
    <span class="pillar__img"><img src="assets/img/thumb/stolarka/1.webp"
      alt="Bramy garażowe dostarczone i zamontowane przez JA-HO" width="560" height="420"
      loading="lazy" decoding="async"></span>
    <span class="pillar__tag">Filar pierwszy</span>
    <h3>Stolarka budowlana</h3>
    <p>Mamy dla Państwa najlepsze rozwiązania w branży stolarki budowlanej —
      dobrane wspólnie, dostarczone na ustalony termin i zamontowane przez naszą
      własną ekipę.</p>
    {j}
    <div class="pillar__cta">{b}</div>
  </article>

  <article class="pillar" data-reveal>
    <span class="pillar__img"><img src="assets/img/thumb/jednorodzinne/6.webp"
      alt="Prace remontowo-budowlane wykonane przez JA-HO" width="560" height="420"
      loading="lazy" decoding="async"></span>
    <span class="pillar__tag">Filar drugi</span>
    <h3>Usługi remontowo-budowlane</h3>
    <p>Gwarantujemy najlepszą jakość i terminowość usług. Siedem grup prac
      w ramach jednej umowy, jednego harmonogramu i jednego kontaktu.</p>
    {s}
    <div class="pillar__cta">{b2}</div>
  </article>""".format(
        j="<ul>%s</ul>" % "".join(
            "<li>%s<span>%s</span></li>" % (icon("check", 16), e(t)) for t, _ in JOINERY),
        s="<ul>%s</ul>" % "".join(
            "<li>%s<span>%s</span></li>" % (icon("check", 16), e(s["name"]))
            for s in SERVICES[:5]),
        b=btn("Stolarka w szczegółach", "services.html#stolarka-budowlana", "btn--onDeep btn--sm"),
        b2=btn("Pełny zakres prac", "services.html#zakres", "btn--onDeep btn--sm"))

    svc_cards = "".join(
        """<article class="card">
      <span class="card__icon">{ic}</span>
      <h3 class="t-h4">{name}</h3>
      <p>{lead}</p>
      <a class="card__link" href="services.html#{id}">Zobacz zakres {ar}</a>
    </article>""".format(ic=icon(SVC_IC[s["id"]], 22), name=e(s["name"]),
                         lead=e(s["lead"]), id=e(s["id"]), ar=icon("arrow", 15))
        for s in SERVICES)

    return head(
        "Firma remontowo-budowlana Lublin | JA-HO od 1999 roku",
        "Kompleksowe usługi remontowo-budowlane i stolarka budowlana na terenie "
        "całego województwa lubelskiego. 27 lat na rynku. Bezpłatna wycena.",
        "index.html", jsonld()) + header("index.html") + """
<main id="main">

<section class="hero">
  <div class="hero__media">
    <picture>
      <source type="image/avif" sizes="100vw"
        srcset="assets/img/hero/siedziba-760.avif 760w, assets/img/hero/siedziba-1080.avif 1080w,
                assets/img/hero/siedziba-1440.avif 1440w, assets/img/hero/siedziba-1920.avif 1920w,
                assets/img/hero/siedziba-2560.avif 2560w">
      <source type="image/webp" sizes="100vw"
        srcset="assets/img/hero/siedziba-760.webp 760w, assets/img/hero/siedziba-1080.webp 1080w,
                assets/img/hero/siedziba-1440.webp 1440w, assets/img/hero/siedziba-1920.webp 1920w,
                assets/img/hero/siedziba-2560.webp 2560w">
      <img src="assets/img/hero/siedziba-1440.webp"
           alt="Siedziba i biuro budowlane JA-HO przy ul. Żołnierskiej w Lublinie"
           width="1440" height="940" fetchpriority="high" decoding="async">
    </picture>
  </div>
  <div class="hero__hex" aria-hidden="true"></div>
  <div class="hero__scrim" aria-hidden="true"></div>

  <div class="wrap hero__in">
    <div class="hero__body">
      <span class="eyebrow">Lublin &middot; lubelskie &middot; od 1999</span>
      <h1 class="t-display kinetic">
        <span class="kinetic">""" + line1 + """</span>
        <span class="kinetic">""" + line2 + """</span>
      </h1>
      <p class="hero__lead">Kompleksowe usługi remontowo-budowlane i stolarka
        budowlana na terenie całego województwa lubelskiego — z gwarancją
        najlepszej jakości i terminowości.</p>
      <div class="btn-row hero__actions">
        """ + btn("Bezpłatna wycena", "contact.html", "btn--lg", magnetic=True) + """
        """ + btn("Zobacz realizacje", "projects.html", "btn--lg btn--onDeep-outline") + """
      </div>
    </div>
  </div>
  <a class="scrollcue" href="#zaufanie"><span>Przewiń</span><i></i></a>
</section>

<section id="zaufanie" class="section--tight" style="border-bottom:1px solid var(--c-line)">
  <div class="wrap">
    <p class="t-xs center" style="letter-spacing:.14em;text-transform:uppercase;color:var(--c-ink-3);font-weight:600">
      Pracujemy dla</p>
  </div>
  """ + client_marquee() + """
</section>

<section class="section">
  <div class="wrap">
    <div class="head head--split" data-reveal>
      <div class="head__text">
        <span class="eyebrow">Dwa filary</span>
        <h2 class="t-h2">Wszystko, czego potrzebuje budynek — od jednego wykonawcy</h2>
        <p class="t-lead">Od 1999 roku pracujemy na dwóch frontach: stolarka, która
          zamyka budynek, i branże, które go wykańczają. Większość klientów
          potrzebuje obu — więc robimy jedno i drugie, w jednym harmonogramie.</p>
      </div>
      <div>""" + btn("Pełna oferta", "services.html", "btn--outline") + """</div>
    </div>

    <div class="grid grid--2">
      """ + pillar_cards + """
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">W liczbach</span>
      <h2 class="t-h2">Dwadzieścia siedem lat, udokumentowane</h2>
      <p class="t-lead">To nie deklaracja, tylko zapis fotograficzny. Każda kategoria
        niżej prowadzi do prawdziwych zdjęć z prawdziwych budów w regionie.</p>
    </div>
    """ + stats_block() + """
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head head--split" data-reveal>
      <div class="head__text">
        <span class="eyebrow">Wybrane realizacje</span>
        <h2 class="t-h2">Od domów jednorodzinnych po zabytkowe elewacje</h2>
        <p class="t-lead">Dziesięć kategorii prac, """ + str(TOTAL_PHOTOS) + """ zdjęć.
          Domy, bloki, hale przemysłowe, placówki bankowe, biura, budynki
          użyteczności publicznej i obiekty pod ochroną konserwatorską.</p>
      </div>
      <div>""" + btn("Wszystkie realizacje", "projects.html", "btn--outline") + """</div>
    </div>

    <div class="mosaic" data-reveal-group>
      """ + "".join(tiles) + """
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Filar drugi w całości</span>
      <h2 class="t-h2">Siedem grup prac w ramach jednej umowy</h2>
      <p class="t-lead">Gwarantujemy najlepszą jakość i terminowość usług. Bez
        ruletki podwykonawców i bez zrzucania winy za opóźnienia między ekipami.</p>
    </div>
    <div class="grid grid--3" data-reveal-group>
      """ + svc_cards + """
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--wide-left">
    <div data-reveal>
      <span class="eyebrow">Jak pracujemy</span>
      <h2 class="t-h2" style="margin:var(--s-4) 0">Cztery kroki od telefonu do gotowej roboty</h2>
      <p class="t-body">Stała kontrola, nadzór i kontakt z klientem pozwalają nam
        szybko rozwiązywać ewentualne usterki czy reklamacje — dlatego większość
        zleceń nadal przychodzi z polecenia naszych byłych i obecnych klientów.</p>
      <div class="btn-row" style="margin-top:var(--s-6)">
        """ + btn("Rozpocznij współpracę", "contact.html") + """
      </div>
    </div>
    <div class="media-frame" data-reveal>
      <img src="assets/img/thumb/firma/1.webp"
           alt="Flota samochodowa firmy JA-HO" width="560" height="420"
           loading="lazy" decoding="async">
    </div>
  </div>

  <div class="wrap" style="margin-top:clamp(2.5rem,2rem+3vw,4rem)">
    <div class="steps" data-reveal>
      """ + steps_block() + """
    </div>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap split">
    <div data-reveal>
      <span class="eyebrow eyebrow--deep">Referencje</span>
      <h2 class="t-h2" style="margin:var(--s-4) 0">Pracujemy dla firm, które znasz</h2>
      <p class="t-lead">Stała współpraca z sektorem bankowym, spożywczym,
        piwowarskim i motoryzacyjnym — klienci, którzy wracają do nas kontrakt
        po kontrakcie. Najlepszą referencją jest jednak klient przysłany przez
        innego klienta.</p>
      <div class="btn-row" style="margin-top:var(--s-6)">
        """ + btn("Poznaj naszą firmę", "about.html", "btn--onDeep-outline") + """
      </div>
    </div>
    <div data-reveal>
      <figure class="quote" style="background:rgba(255,255,255,.06);border-color:var(--c-deep-line)">
        <blockquote style="color:#fff">""" + e(C["motto"]) + """</blockquote>
        <figcaption>
          <span class="quote__avatar">MG</span>
          <span>
            <span class="quote__who" style="color:#fff">""" + e(C["person"]) + """</span><br>
            <span class="quote__role">właściciel, dyrektor generalny</span>
          </span>
        </figcaption>
      </figure>
    </div>
  </div>

  <div class="wrap" style="margin-top:var(--s-7)">
    """ + client_marquee(deep=True) + """
  </div>
</section>

""" + cta_band() + """
</main>
""" + footer()


def page_services():
    joinery_items = "".join(
        """<article class="card">
      <span class="card__num">0{i}</span>
      <h3 class="t-h4">{t}</h3>
      <p>{d}</p>
    </article>""".format(i=i + 1, t=e(t), d=e(d)) for i, (t, d) in enumerate(JOINERY))

    acc_items = []
    for i, s in enumerate(SERVICES):
        lis = "".join('<li style="--i:%d">%s<span>%s</span></li>'
                      % (j, icon("check", 16), e(x)) for j, x in enumerate(s["items"]))
        acc_items.append("""<div class="acc__item" id="{id}">
      <h3 style="margin:0">
        <button class="acc__btn" type="button" id="b-{id}" aria-expanded="false"
                aria-controls="p-{id}">
          <span class="acc__idx">{n:02d}</span>
          <span class="acc__q">{name}</span>
          <span class="acc__chev">{chev}</span>
        </button>
      </h3>
      <div class="acc__panel" id="p-{id}" role="region" aria-labelledby="b-{id}">
        <div><div class="acc__body">
          <p class="acc__lead">{lead}</p>
          <ul class="acc__list">{lis}</ul>
        </div></div>
      </div>
    </div>""".format(id=e(s["id"]), n=i + 1, name=e(s["name"]), lead=e(s["lead"]),
                     lis=lis, chev=icon("chev", 17)))

    faq_items = []
    for i, (q, a) in enumerate(FAQ):
        faq_items.append("""<div class="acc__item">
      <h3 style="margin:0">
        <button class="acc__btn" type="button" id="fb-{i}" aria-expanded="false"
                aria-controls="f-{i}">
          <span class="acc__q">{q}</span>
          <span class="acc__chev">{chev}</span>
        </button>
      </h3>
      <div class="acc__panel" id="f-{i}" role="region" aria-labelledby="fb-{i}">
        <div><div class="acc__body"><p style="--i:0">{a}</p></div></div>
      </div>
    </div>""".format(i=i, q=e(q), a=e(a), chev=icon("chev", 17)))

    faq_ld = """{
    "@type": "FAQPage",
    "@id": "%s/services.html#faq",
    "mainEntity": [%s]
  }""" % (C["domain"], ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_json(q), _json(a)) for q, a in FAQ))

    svc_ld = """{
    "@type": "Service",
    "@id": "%s/services.html#service",
    "serviceType": "Usługi remontowo-budowlane i stolarka budowlana",
    "provider": { "@id": "%s/#org" },
    "areaServed": { "@type": "AdministrativeArea", "name": "województwo lubelskie" },
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "name": "Usługi remontowo-budowlane",
      "itemListElement": [%s]
    }
  }""" % (C["domain"], C["domain"], ",".join(
        '{"@type":"Offer","itemOffered":{"@type":"Service","name":%s,"description":%s}}'
        % (_json(s["name"]), _json("; ".join(s["items"]))) for s in SERVICES))

    return head(
        "Oferta — stolarka i usługi remontowo-budowlane | JA-HO",
        "Doradztwo, dostawa i montaż okien, drzwi i bram garażowych oraz pełny zakres "
        "prac: murarskie, tynkarskie, glazura, malowanie, gipsy i instalacje.",
        "services.html", jsonld([svc_ld, faq_ld])) + header("services.html") + """
<main id="main">

""" + banner(
        "Nasza oferta",
        "Oferujemy Państwu profesjonalne i kompleksowe usługi budowlane na terenie "
        "całego województwa lubelskiego — oparte na dwóch filarach, których "
        "większość realizacji potrzebuje razem.",
        "Oferta") + """

<section class="section" id="stolarka-budowlana">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Filar pierwszy</span>
      <h2 class="t-h2">Stolarka budowlana</h2>
      <p class="t-lead">Mamy dla Państwa najlepsze rozwiązania w branży stolarki
        budowlanej. Od pierwszej rozmowy o współczynnikach przenikania ciepła po
        moment uszczelnienia ostatniego ościeża — jedna ekipa i jedna
        odpowiedzialność.</p>
    </div>

    <div class="grid grid--4" data-reveal-group>
      """ + joinery_items + """
    </div>

    <div class="split" style="margin-top:clamp(2.5rem,2rem+4vw,4.5rem)">
      <div class="media-frame" data-reveal>
        <img src="assets/img/thumb/stolarka/6.webp"
             alt="Monter JA-HO podczas montażu stolarki drzwiowej na budowie"
             width="560" height="420" loading="lazy" decoding="async">
      </div>
      <div data-reveal>
        <h3 class="t-h3" style="margin-bottom:var(--s-4)">Od tego zaczynała się firma</h3>
        <p class="t-body">Sprzedaż i montaż stolarki budowlanej były podstawą
          działalności, kiedy firma powstawała w czerwcu 1999 roku. Zostały w ofercie
          do dziś — teraz jako uzupełnienie prac remontowo-budowlanych, dzięki czemu
          wymiana okna nigdy nie musi czekać na drugiego wykonawcę, który obrobi
          ościeża.</p>
        <div class="btn-row" style="margin-top:var(--s-6)">
          """ + btn("Realizacje: stolarka", "projects.html#stolarka", "btn--outline") + """
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="zakres">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Filar drugi</span>
      <h2 class="t-h2">Usługi remontowo-budowlane</h2>
      <p class="t-lead">Gwarantujemy najlepszą jakość i terminowość usług. Poniżej
        pełny zakres prac — rozwiń interesującą Cię kategorię.</p>
    </div>

    <div class="acc" data-reveal>
      """ + "".join(acc_items) + """
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Przebieg realizacji</span>
      <h2 class="t-h2">Cztery kroki, bez niespodzianek</h2>
    </div>
    <div class="steps" data-reveal>
      """ + steps_block() + """
    </div>
  </div>
</section>

<section class="section section--alt" id="faq">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Pytania</span>
      <h2 class="t-h2">Najczęściej zadawane</h2>
    </div>
    <div class="acc" data-single data-reveal>
      """ + "".join(faq_items) + """
    </div>
  </div>
</section>

""" + cta_band() + """
</main>
""" + footer()


def page_projects():
    tabs = ['<button class="tab" type="button" data-slug="all" aria-pressed="true">'
            'Wszystkie<span class="tab__n">%d</span></button>' % TOTAL_PHOTOS]
    for c in CATEGORIES:
        tabs.append('<button class="tab" type="button" data-slug="%s" '
                    'aria-pressed="false">%s'
                    '<span class="tab__n">%d</span></button>'
                    % (e(c["slug"]), e(c["short"]), c["count"]))

    # Przeplatamy kategorie, żeby domyślny widok „Wszystkie” wyglądał jak
    # przekrój portfolio, a nie jak 60 zdjęć hal pod rząd.
    queues = [(c, photo_order(c)) for c in CATEGORIES]
    shots, idx = [], 0
    while any(q for _, q in queues):
        for c, q in queues:
            if q:
                # Tylko pierwszy rząd galerii ładuje się od razu.
                shots.append(shot(c, q.pop(0), lazy=(idx >= 4)))
                idx += 1

    cards = "".join(
        """<article class="card">
      <span class="card__num">{n:02d}</span>
      <h3 class="t-h4">{name}</h3>
      <p>{desc}</p>
      <a class="card__link" href="#{slug}" data-jump="{slug}">{count} zdjęć {ar}</a>
    </article>""".format(n=i + 1, name=e(c["name"]), desc=e(c["desc"]),
                         slug=e(c["slug"]), count=c["count"], ar=icon("arrow", 15))
        for i, c in enumerate(CATEGORIES))

    gallery_ld = """{
    "@type": "ImageGallery",
    "@id": "%s/projects.html#gallery",
    "name": "Realizacje JA-HO",
    "description": "%d zdjęć z %d kategorii prac remontowo-budowlanych i stolarskich w województwie lubelskim.",
    "isPartOf": { "@id": "%s/#site" }
  }""" % (C["domain"], TOTAL_PHOTOS, len(CATEGORIES), C["domain"])

    return head(
        "Realizacje — %d zdjęć z naszych budów | JA-HO" % TOTAL_PHOTOS,
        "Domy, hale, zabytki, placówki bankowe i biura — %d udokumentowanych zdjęć "
        "z realizacji JA-HO na terenie województwa lubelskiego." % TOTAL_PHOTOS,
        "projects.html", jsonld([gallery_ld])) + header("projects.html") + """
<main id="main">

""" + banner(
        "Nasze realizacje",
        "%d zdjęć w %d kategoriach — udokumentowany zapis tego, co zbudowaliśmy, "
        "wyremontowaliśmy i odrestaurowaliśmy w województwie lubelskim."
        % (TOTAL_PHOTOS, len(CATEGORIES)),
        "Realizacje") + """

<section class="section--tight" style="position:sticky;top:var(--header-h);z-index:40;
     background:color-mix(in srgb,var(--c-bg) 92%,transparent);backdrop-filter:blur(14px);
     border-bottom:1px solid var(--c-line);padding-block:var(--s-4)">
  <div class="wrap">
    <div class="tabs" role="group" aria-label="Filtruj realizacje według kategorii" data-filter-tabs>
      """ + "".join(tabs) + """
    </div>
    <p class="sr-only" role="status" data-filter-status></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="gallery" data-gallery data-reveal>
      """ + "".join(shots) + """
    </div>
    <p class="gallery__empty" hidden>Brak zdjęć w tej kategorii.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Kategorie</span>
      <h2 class="t-h2">Co obejmuje każda kategoria</h2>
      <p class="t-lead">Dziesięć rodzajów prac — od domu pod klucz po stolarkę
        konserwatorską w zabytkowej ceglanej elewacji.</p>
    </div>
    <div class="grid grid--3" data-reveal-group>
      """ + cards + """
    </div>
  </div>
</section>

""" + cta_band() + """
</main>
""" + lightbox() + """
<script>
/* Kafelki kategorii przenoszą do galerii z nałożonym filtrem. */
document.addEventListener("click", function (ev) {
  var a = ev.target.closest("[data-jump]");
  if (!a) return;
  ev.preventDefault();
  var tab = document.querySelector('.tab[data-slug="' + a.dataset.jump + '"]');
  if (tab) { tab.click(); tab.scrollIntoView({ block: "nearest", inline: "center" }); }
  var g = document.querySelector("[data-gallery]");
  if (g) g.scrollIntoView({ behavior: "smooth", block: "start" });
});
</script>
""" + footer()


def page_about():
    tl = "".join(
        """<div class="tl__item" data-reveal>
      <span class="tl__dot"></span>
      <span class="tl__yr">{y}</span>
      <h3>{t}</h3>
      <p>{d}</p>
    </div>""".format(y=e(y), t=e(t), d=e(d)) for y, t, d in TIMELINE)

    fleet = "".join(
        '<div class="media-frame"><img src="assets/img/thumb/firma/%d.webp" '
        'alt="Siedziba i flota firmy JA-HO, zdjęcie %d" '
        'width="560" height="420" loading="lazy" decoding="async"></div>' % (n, n)
        for n in (1, 2, 3))

    sp = SPONSORSHIP
    sponsor_shots = "".join(
        '<div class="media-frame"><img src="assets/img/thumb/%s/%d.webp" '
        'alt="Sponsoring sekcji rugby Budowlani Lublin przez JA-HO, zdjęcie %d" '
        'width="560" height="420" loading="lazy" decoding="async"></div>'
        % (sp["slug"], n, n) for n in sp["order"][:3])

    clients_rows = "".join(
        """<div class="cinfo__row">
      <span class="cinfo__ic">{ic}</span>
      <span><span class="cinfo__k">{sector}</span>
      <span class="cinfo__v">{name}</span></span>
    </div>""".format(ic=icon("award", 18), sector=e(cl["sector"]), name=e(cl["name"]))
        for cl in CLIENTS)

    f = FUNDING
    about_ld = """{
    "@type": "AboutPage",
    "@id": "%s/about.html#page",
    "name": "O firmie F.R.B. JA-HO",
    "isPartOf": { "@id": "%s/#site" },
    "about": { "@id": "%s/#org" }
  }""" % (C["domain"], C["domain"], C["domain"])

    return head(
        "O nas — firma remontowo-budowlana od 1999 roku | JA-HO",
        "F.R.B. „JA-HO” powstała w czerwcu 1999 roku. Dwadzieścia siedem lat prac "
        "remontowo-budowlanych i stolarki na terenie województwa lubelskiego.",
        "about.html", jsonld([about_ld])) + header("about.html") + """
<main id="main">

""" + banner(
        "O nas",
        "Od 1999 roku budujemy, remontujemy i wykańczamy — na terenie Lublina "
        "i całego województwa lubelskiego.",
        "O nas") + """

<section class="section">
  <div class="wrap split split--wide-left">
    <div data-reveal>
      <span class="eyebrow">Nasza historia</span>
      <h2 class="t-h2" style="margin:var(--s-4) 0">Dwadzieścia siedem lat, dwa profile, jeden standard</h2>
      <p class="t-body">Firma powstała w czerwcu 1999 roku jako działalność
        handlowo-usługowa. Podstawą działalności była sprzedaż i montaż stolarki
        budowlanej.</p>
      <p class="t-body">W lipcu 2004 roku, po wejściu Polski do Unii Europejskiej,
        zmieniliśmy siedzibę i profil działalności firmy na wyłącznie usługowy.
        Głównym naszym zajęciem stały się remonty mieszkań, biur oraz wykończenia
        wnętrz, a uzupełnieniem oferty pozostała sprzedaż i montaż stolarki
        budowlanej.</p>
      <p class="t-body">Nasza firma wyposażona jest w profesjonalne elektronarzędzia
        do wszystkich robót. Wieloletnie doświadczenie pracowników w tej branży, ich
        kwalifikacje i regularne szkolenia pozwalają nam podnosić jakość
        wykonywanych usług, spełniając stale rosnące wymagania naszych klientów.</p>
      <p class="t-body">Stała kontrola, nadzór i kontakt z klientem pozwalają na
        szybkie rozwiązywanie ewentualnych usterek czy reklamacji. F.R.B. „JA-HO”
        kładzie duży nacisk na jakość wykonywanych usług, czego dowodem są klienci
        z polecenia od naszych byłych, obecnych i stałych zleceniodawców.</p>
    </div>
    <div class="stack" data-reveal>
      <figure class="quote">
        <blockquote>""" + e(C["motto"]) + """</blockquote>
        <figcaption>
          <span class="quote__avatar">MG</span>
          <span>
            <span class="quote__who">""" + e(C["person"]) + """</span><br>
            <span class="quote__role">właściciel, dyrektor generalny</span>
          </span>
        </figcaption>
      </figure>
      <div class="media-frame">
        <img src="assets/img/hero/siedziba-1080.webp"
             alt="Siedziba firmy JA-HO przy ul. Żołnierskiej w Lublinie"
             width="1080" height="705" loading="lazy" decoding="async">
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Kamienie milowe</span>
      <h2 class="t-h2">Jak tu doszliśmy</h2>
    </div>
    <div class="tl">""" + tl + """</div>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow eyebrow--deep">W liczbach</span>
      <h2 class="t-h2">Dorobek do dziś</h2>
    </div>
    """ + stats_block(deep=True) + """
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Nasza firma</span>
      <h2 class="t-h2">Siedziba i flota</h2>
      <p class="t-lead">Aby szybko i profesjonalnie realizować powierzone nam prace,
        dysponujemy nowoczesną flotą i własnym sprzętem.</p>
    </div>
    <div class="grid grid--3" data-reveal-group>""" + fleet + """</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap split">
    <div data-reveal>
      <span class="eyebrow">Referencje</span>
      <h2 class="t-h2" style="margin:var(--s-4) 0">Klienci, dla których pracujemy</h2>
      <p class="t-body">Nasza firma stale współpracuje z klientami z sektora
        bankowego, spożywczego, piwowarskiego i motoryzacyjnego. Najlepszą
        referencją są jednak dla nas klienci z polecenia — od naszych byłych,
        obecnych i stałych zleceniodawców.</p>
      <div class="btn-row" style="margin-top:var(--s-6)">
        """ + btn("Zobacz realizacje", "projects.html", "btn--outline") + """
      </div>
    </div>
    <div class="cinfo" data-reveal>""" + clients_rows + """</div>
  </div>
</section>

<section class="section" id="dofinansowanie">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Dofinansowanie</span>
      <h2 class="t-h2">""" + e(f["title"]) + """</h2>
      <p class="t-lead">""" + e(f["lead"]) + """</p>
    </div>

    <div class="fund" data-reveal>
      <div class="fund__emblems">
        <img src="assets/img/thumb/firma/flaga.webp" alt="Flaga Rzeczypospolitej Polskiej"
             width="140" height="88" loading="lazy" decoding="async">
        <img src="assets/img/thumb/firma/godlo.webp" alt="Godło Rzeczypospolitej Polskiej"
             width="100" height="118" loading="lazy" decoding="async">
      </div>
      <div>
        <p class="t-body">""" + e(f["body"]) + """</p>
        <div class="fund__figs">
          <div class="stat">
            <div class="stat__n" style="font-size:clamp(1.5rem,1.2rem+1.4vw,2rem)">""" + e(f["grant"]) + """</div>
            <div class="stat__k">""" + e(f["grant_label"]) + """</div>
          </div>
          <div class="stat">
            <div class="stat__n" style="font-size:clamp(1.5rem,1.2rem+1.4vw,2rem)">""" + e(f["total"]) + """</div>
            <div class="stat__k">""" + e(f["total_label"]) + """</div>
          </div>
          <div class="stat">
            <div class="stat__k" style="margin-top:0">""" + e(f["project"]) + """</div>
            <p class="stat__d">tytuł projektu</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="sponsoring">
  <div class="wrap">
    <div class="head" data-reveal>
      <span class="eyebrow">Społeczność</span>
      <h2 class="t-h2">""" + e(sp["title"]) + """</h2>
      <p class="t-lead">""" + e(sp["desc"]) + """</p>
    </div>
    <div class="grid grid--3" data-reveal-group>""" + sponsor_shots + """</div>
  </div>
</section>

""" + cta_band() + """
</main>
""" + footer()


def page_contact():
    scope_opts = "".join('<option value="%s">%s</option>' % (e(s["name"]), e(s["name"]))
                         for s in SERVICES)

    contact_ld = """{
    "@type": "ContactPage",
    "@id": "%s/contact.html#page",
    "name": "Kontakt — JA-HO",
    "isPartOf": { "@id": "%s/#site" },
    "about": { "@id": "%s/#org" }
  }""" % (C["domain"], C["domain"], C["domain"])

    return head(
        "Kontakt — bezpłatne oględziny i wycena | JA-HO Lublin",
        "Zadzwoń pod 695 225 505 albo napisz. Bezpłatne oględziny, pomiary i wycena "
        "wstępna na terenie województwa lubelskiego. Odpowiadamy w 24 godziny.",
        "contact.html", jsonld([contact_ld])) + header("contact.html") + """
<main id="main">

""" + banner(
        "Kontakt z nami",
        "Dokonujemy oględzin, pomiarów i wyceny wstępnej. Zadzwoń albo napisz — "
        "odpowiadamy na wszystkie pytania w ciągu 24 godzin.",
        "Kontakt") + """

<section class="section">
  <div class="wrap contact-grid">
    <div data-reveal>
      <span class="pill pill--live" style="margin-bottom:var(--s-5)"><i></i>Odpowiadamy w 24 godziny</span>
      <h2 class="t-h3" style="margin-bottom:var(--s-5)">Porozmawiaj z nami bezpośrednio</h2>
      <div class="cinfo">""" + contact_aside() + """</div>

      <div class="card" style="margin-top:var(--s-6)">
        <span class="card__icon">""" + icon("users", 22) + """</span>
        <h3 class="t-h4">""" + e(C["person"]) + """</h3>
        <p>""" + e(C["role"]) + """ — osoba, z którą faktycznie porozmawiasz
          o zakresie prac, terminie i cenie.</p>
      </div>

      <ul class="checks" style="margin-top:var(--s-6)">
        <li>""" + icon("check", 17) + """<span>Bezpłatne oględziny i pomiary na miejscu</span></li>
        <li>""" + icon("check", 17) + """<span>Wycena wstępna z pisemnym zakresem prac</span></li>
        <li>""" + icon("check", 17) + """<span>Obsługa całego województwa lubelskiego</span></li>
        <li>""" + icon("check", 17) + """<span>Transport materiałów na plac budowy po naszej stronie</span></li>
      </ul>
    </div>

    <div data-reveal>
      <h2 class="t-h3" style="margin-bottom:var(--s-5)">Wyślij zapytanie</h2>
      <form class="form" data-mailto=\"""" + e(C["email"]) + """\" novalidate>
        <div class="form__row">
          <div class="field">
            <label for="f-name">Imię i nazwisko <span class="req" aria-hidden="true">*</span></label>
            <input id="f-name" name="name" type="text" autocomplete="name" required
                   placeholder="Jan Kowalski">
          </div>
          <div class="field">
            <label for="f-phone">Telefon <span class="req" aria-hidden="true">*</span></label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" required
                   placeholder="600 000 000">
          </div>
        </div>

        <div class="form__row">
          <div class="field">
            <label for="f-email">E-mail</label>
            <input id="f-email" name="email" type="email" autocomplete="email"
                   placeholder="jan@przyklad.pl">
          </div>
          <div class="field">
            <label for="f-place">Gdzie jest inwestycja?</label>
            <input id="f-place" name="place" type="text" placeholder="Lublin, Świdnik, Puławy…">
          </div>
        </div>

        <div class="field">
          <label for="f-scope">Czego potrzebujesz?</label>
          <select id="f-scope" name="scope">
            <option value="">Wybierz kategorię…</option>
            <option value="Stolarka budowlana">Stolarka budowlana (okna, drzwi, bramy garażowe)</option>
            """ + scope_opts + """
            <option value="Coś innego">Coś innego</option>
          </select>
        </div>

        <div class="field">
          <label for="f-msg">Opisz zakres prac <span class="req" aria-hidden="true">*</span></label>
          <textarea id="f-msg" name="message" required
            placeholder="Orientacyjny zakres, metraż lub wielkość obiektu oraz termin, w którym chcesz zrealizować prace."></textarea>
          <p class="field__hint">Im więcej szczegółów podasz, tym dokładniejsza
            będzie pierwsza wycena.</p>
        </div>

        <div class="btn-row">
          <button class="btn btn--lg" type="submit"><span class="btn__ripple"></span>
            <span>Wyślij zapytanie</span><span class="btn__icon">""" + icon("mail", 17) + """</span></button>
          <a class="btn btn--lg btn--outline" href="tel:""" + e(C["mobile_href"]) + """">
            <span class="btn__ripple"></span>
            <span class="btn__icon btn--phone">""" + icon("phone", 17) + """</span>
            <span>Albo zadzwoń: """ + e(C["mobile"]) + """</span></a>
        </div>
        <p class="form__note" data-form-note>Ten formularz otwiera Twój program
          pocztowy z gotowym zapytaniem — nic nie jest zapisywane na tej stronie.
          Wolisz porozmawiać? Zadzwoń pod """ + e(C["mobile"]) + """.</p>
      </form>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="head head--split" data-reveal>
      <div class="head__text">
        <span class="eyebrow">Jak nas znaleźć</span>
        <h2 class="t-h2">""" + e(C["street"]) + """, """ + e(C["postcode"]) + """</h2>
        <p class="t-lead">Nasze biuro i biuro budowlane w Lublinie. Pracujemy na
          terenie całego województwa lubelskiego — jeśli inwestycja leży dalej,
          zapytaj, a powiemy wprost, czy logistyka ma sens.</p>
      </div>
      <div>""" + btn("Otwórz w Mapach Google",
                     "https://www.google.com/maps/search/?api=1&query=" +
                     "ul.+Zolnierska+7,+20-081+Lublin", "btn--outline", "pin",
                     attrs=' target="_blank" rel="noopener"') + """</div>
    </div>

    <div class="map" data-reveal>
      <iframe title="Mapa z lokalizacją biura JA-HO przy ul. Żołnierskiej 7 w Lublinie"
        src="https://www.openstreetmap.org/export/embed.html?bbox=22.53%2C51.23%2C22.59%2C51.26&amp;layer=mapnik&amp;marker=51.2465%2C22.5601"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>

""" + cta_band() + """
</main>
""" + footer()


# ---------------------------------------------------------------- dodatki
def sitemap():
    urls = []
    for h, _ in NAV:
        loc = C["domain"] + "/" + ("" if h == "index.html" else h)
        pri = "1.0" if h == "index.html" else "0.8"
        urls.append("  <url><loc>%s</loc><changefreq>monthly</changefreq>"
                    "<priority>%s</priority></url>" % (e(loc), pri))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % C["domain"]


# ---------------------------------------------------------------- main
PAGES = {
    "index.html": page_index,
    "services.html": page_services,
    "projects.html": page_projects,
    "about.html": page_about,
    "contact.html": page_contact,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in PAGES.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(pl_typo(fn()))
        print("  %-16s %6.1f kB" % (name, os.path.getsize(p) / 1024))

    for name, body in (("sitemap.xml", sitemap()), ("robots.txt", robots())):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(body)
        print("  %-16s ok" % name)

    print("\n%d zdjęć w %d kategoriach." % (TOTAL_PHOTOS, len(CATEGORIES)))


if __name__ == "__main__":
    main()
