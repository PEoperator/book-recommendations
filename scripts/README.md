# Site build (Favorites filter + home IA)

1. `extracted_books.json` — book card HTML extracted from the prior monolithic `index.html` (271 titles). Stock Picker orphan fragment was cleaned.
2. `categories.json` — exact title → one of six category ids (includes Fiction).
3. `build_site.py` — regenerates `index.html`, six category pages, and `view-all.html`.

Rebuild:

```bash
python3 scripts/build_site.py
```

Shared runtime assets: `site.css`, `favorites.js` (All | ⚡ Favorites; no persistence).

Latest additions on home = first 5 non-Rushmore cards in live/source grid order (top under Mt. Rushmore).

Design refresh (Impeccable): pages no longer load the Tailwind CDN or Font Awesome. All styling lives in `site.css` (tokens at the top), with Archivo self-hosted from `fonts/`. Cards are re-rendered at build time from the extracted HTML. The original `<a>` tag (affiliate href), cover `src`/`alt`, title and author are kept byte-for-byte. See `DESIGN.md` for the system and `PRODUCT.md` for product context.

Social share card: `og.png` (1200x630, served at `https://peoperator.co/og.png`) is rendered from `scripts/og.html` by headless Chrome:

```bash
python3 scripts/make_og.py   # needs Google Chrome/Chromium + Pillow
```

`build_site.py` writes canonical, Open Graph and Twitter card tags into every page head (`social_meta_html`).
