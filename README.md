# JA-HO — construction company website

Statyczna strona **F.R.B. „JA-HO”** — firmy remontowo-budowlanej działającej na
terenie województwa lubelskiego od 1999 roku. Cała treść po polsku (`lang="pl"`).

## Layout

```
_src/data.py     treść — jedyne źródło prawdy (dane firmy, usługi, kategorie,
                 klienci, FAQ, dofinansowanie, oś czasu)
_src/build.py    generator — wspólny nagłówek/stopka/CTA + pięć podstron
*.html           wygenerowane strony — LEŻĄ W KORZENIU, bo Vercel i GitHub Pages
                 serwują właśnie stąd; podkatalog = 404
assets/css/site.css   tokeny designu + komponenty
assets/js/site.js     zachowanie, czysty JS, zero zależności
assets/img/           224 zdjęcia realizacji, hero, logotypy klientów
vercel.json           nagłówki cache + bezpieczeństwa
.vercelignore         generator i materiały źródłowe nie idą na hosting
.nojekyll             GitHub Pages ma nie przepuszczać repo przez Jekylla
img/, tlo.png         materiały źródłowe, poza repo (patrz .gitignore)
```

Pliki `.html` w korzeniu **są generowane** — nie edytuj ich ręcznie. Zmieniasz
`_src/data.py` (treść) albo `_src/build.py` (szablony) i przebudowujesz:

```bash
python3 _src/build.py
```

Podgląd lokalny:

```bash
python3 -m http.server 8000
```

## Pages

| Page | Contents |
|---|---|
| `index.html` | Hero, client wall, two pillars, stats, project mosaic, seven trade groups, process, references |
| `services.html` | Pillar one (joinery) in detail, pillar two accordion (full scope of works), process, FAQ |
| `projects.html` | 224 photographs, filterable by 10 categories, with a lightbox |
| `about.html` | Company story, timeline, stats, premises & fleet, clients, ZUS/FUS funding, sponsorship |
| `contact.html` | Contact details, enquiry form, map |

## Notes for whoever picks this up next

- **The contact form has no backend.** It composes a `mailto:` with the enquiry
  pre-filled, and the form says so on the page. If a real endpoint is added later,
  replace the `contactForm()` block in `site.js`; the markup already carries the
  right field names.
- **Język.** Cała treść siedzi w `_src/data.py`, szablony w `build.py` nie mają
  zaszytego tekstu poza nagłówkami sekcji. Generator dokleja twarde spacje po
  polskich spójnikach jednoliterowych (`pl_typo()`), żeby nie zostawały na końcu
  wiersza.
- **Theme.** Light and dark are both token-driven in `site.css`. An inline script
  in `<head>` paints the stored choice before first paint, so there is no flash.
  Tokens are defined once at `:root` and mirrored in the two dark blocks — add new
  colours in all three or dark mode will silently fall back.
- **Client logos** all come from `assets/img/partnerzy/mono/` (white knockouts).
  CSS inverts them on light grounds. The full-colour originals are kept alongside
  but are not used: their luminance varies wildly and one of them is white-on-white.
- **Photographs are archive material** (roughly 700×525, older cameras). They are
  used at card and thumbnail scale deliberately — full-bleed treatment exposes the
  resolution. The only high-resolution image is the office shot in `assets/img/hero/`.
- **Animation** is CSS-first, driven by `IntersectionObserver` for scroll reveals.
  Everything degrades: with JS off, `html:not(.js)` rules make all content visible,
  and `prefers-reduced-motion` drops movement while keeping every affordance.
- **Accessibility.** All token pairs meet WCAG AA (verified, tightest is 4.66:1).
  The category filter is a toggle-button group with `aria-pressed` — deliberately
  not a tablist, because there is one shared gallery rather than one panel per tab.

## Deploy

Dowolny hosting statyczny, prosto z korzenia repo — bez build stepu po stronie
serwera. Vercel: import repo, nic nie konfigurujesz. GitHub Pages: Settings →
Pages → Source: `main` / `/ (root)`.

### vercel.json

Schema Vercela jest ścisła (`additionalProperties: false`) — w obiektach
`headers[]` wolno użyć wyłącznie `source`, `headers`, `has` i `missing`.
Nie ma jak wstawić komentarza w samym pliku, więc uzasadnienie reguł jest tutaj:

- `assets/img/**` → `max-age=31536000, immutable`. Ścieżki zdjęć są stabilne
  i nigdy nie zmieniają treści — nowe ujęcie dostaje kolejny numer, nie nadpisuje
  starego. Rok cache'u jest bezpieczny.
- `assets/css/**` i `assets/js/**` → `max-age=0, must-revalidate`. Te pliki nie
  mają hasha w nazwie, więc po przebudowie ścieżka zostaje ta sama. Bez
  rewalidacji ludzie zobaczyliby stary arkusz albo starą wersję skryptu.
- HTML zostawiamy na domyślnym zachowaniu Vercela (też rewalidacja).
- Ostatnia reguła dokłada `X-Content-Type-Options`, `Referrer-Policy`
  i `X-Frame-Options` na wszystko.

Walidacja przed pushem, żeby nie wywalić builda na literówce:

```bash
curl -s -o /tmp/v.json https://openapi.vercel.sh/vercel.json
python3 -c "import json,jsonschema;jsonschema.Draft7Validator(json.load(open('/tmp/v.json'))).validate(json.load(open('vercel.json')))"
```
Update `COMPANY["domain"]` in `_src/data.py` if the domain changes; canonical URLs,
Open Graph tags and `sitemap.xml` all derive from it.
