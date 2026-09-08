# JA-HO — construction company website

Statyczna strona **F.R.B. „JA-HO”** — firmy remontowo-budowlanej działającej na
terenie województwa lubelskiego od 1999 roku. Cała treść po polsku (`lang="pl"`).

## Layout

```
_src/data.py     content — the single source of truth (company details, services,
                 categories, clients, FAQ, funding, timeline)
_src/build.py    generator — shared header/footer/CTA templates + the five pages
www/             the site itself; this is what you deploy
  assets/css/site.css   design tokens + components
  assets/js/site.js     behaviour, vanilla, no dependencies
  assets/img/           224 project photographs, hero set, client logos
img/                    source image library (copied into www/assets/img)
```

The `.html` files in `www/` are **generated**. Do not edit them by hand — change
`_src/data.py` (content) or `_src/build.py` (markup) and rebuild:

```bash
python3 _src/build.py
```

Preview locally:

```bash
cd www && python3 -m http.server 8000
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

Any static host — the whole of `www/`, no build step server-side.
Update `COMPANY["domain"]` in `_src/data.py` if the domain changes; canonical URLs,
Open Graph tags and `sitemap.xml` all derive from it.
