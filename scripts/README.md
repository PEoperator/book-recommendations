# Site build (Favorites filter + home IA)

1. `extracted_books.json` — book card HTML extracted from the prior monolithic `index.html` (271 titles). Stock Picker orphan fragment was cleaned.
2. `categories.json` — exact title → one of five category ids.
3. `build_site.py` — regenerates `index.html`, five category pages, and `view-all.html`.

Rebuild:

```bash
python3 scripts/build_site.py
```

Shared runtime assets: `site.css`, `favorites.js` (All | ⚡ Favorites; no persistence).
