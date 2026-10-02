#!/usr/bin/env python3
"""Build peoperator.co home IA + category pages + view-all + favorites/search filter."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = [
    {
        "id": "operators-builders",
        "slug": "operators-builders.html",
        "title": "Operators & Builders",
        "blurb": "Running, scaling, and building companies.",
    },
    {
        "id": "investing-capital",
        "slug": "investing-capital.html",
        "title": "Investing & Capital",
        "blurb": "Markets, capital allocation, and money.",
    },
    {
        "id": "biography-history",
        "slug": "biography-history.html",
        "title": "Biography & History",
        "blurb": "Lives, eras, and true stories.",
    },
    {
        "id": "faith-meaning",
        "slug": "faith-meaning.html",
        "title": "Faith & Meaning",
        "blurb": "Belief, purpose, and the deeper why.",
    },
    {
        "id": "mindset-judgment",
        "slug": "mindset-judgment.html",
        "title": "Mindset & Judgment",
        "blurb": "Thinking clearly and deciding well.",
    },
    {
        "id": "fiction",
        "slug": "fiction.html",
        "title": "Fiction",
        "blurb": "Novels, stories, and literary worlds.",
    },
]

CAT_BY_ID = {c["id"]: c for c in CATEGORIES}


def sort_title_key(title: str) -> str:
    t = title.strip()
    # Strip leading quotes for sort
    t = t.lstrip("\"'“”")
    # Ignore leading articles for nicer A–Z
    for prefix in ("The ", "A ", "An "):
        if t.startswith(prefix):
            t = t[len(prefix) :]
            break
    return t.casefold()


BOLT_SVG = (
    '<svg class="icon-bolt" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M14.2 1.8 4.6 13.6h6.1l-1.6 8.6 9.9-12.4h-6.3l1.5-8z" fill="currentColor"/></svg>'
)

SEARCH_SVG = (
    '<svg class="icon-search" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    '<path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
)

ARROW_SVG = (
    '<svg class="icon-arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M5 12h13m-5-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def parse_card(html: str) -> dict:
    """Pull the content of one extracted card. Anchor tag, cover src/alt, title and author
    are kept byte-for-byte (affiliate hrefs must never change)."""
    anchors = re.findall(r"<a\s[^>]*>", html)
    covers = [m for m in re.finditer(r"<img\b[^>]*>", html, re.S) if "lightning.png" not in m.group(0)]
    titles = re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S)
    authors = re.findall(r"<p[^>]*>(.*?)</p>", html, re.S)
    if not (len(anchors) == 1 and len(covers) == 1 and len(titles) == 1 and len(authors) == 1):
        raise SystemExit(f"Unexpected card structure: {html[:120]!r}")
    img = covers[0].group(0)
    src = re.search(r'\ssrc="([^"]*)"', img).group(1)
    alt_m = re.search(r'\salt="([^"]*)"', img)
    return {
        "anchor": anchors[0],
        "src": src,
        "alt": alt_m.group(1) if alt_m else "",
        "title": titles[0].strip(),
        "author": authors[0].strip(),
    }


def render_card(book: dict, variant: str = "", eager: bool = False) -> str:
    """Render one book card in the refreshed markup (content unchanged)."""
    c = parse_card(book["html"])
    attrs = ['data-book-card="true"']
    if book["favorite"]:
        attrs.append('data-favorite="true"')
    cls = "book" + (f" book--{variant}" if variant else "")
    badge = (
        '\n        <span class="bolt-badge"><img src="lightning.png" alt="Favorite" width="48" height="48" decoding="async"></span>'
        if book["favorite"]
        else ""
    )
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""<article {' '.join(attrs)} class="{cls}">
      {c['anchor']}
        <div class="book-cover-frame">
          <img src="{c['src']}" alt="{c['alt']}" class="book-cover" {loading} decoding="async" width="300" height="450">{badge}
        </div>
        <div class="book-meta">
          <h3 class="book-title">{c['title']}</h3>
          <p class="book-author">{c['author']}</p>
        </div>
      </a>
    </article>"""


def filter_bar_html(include_favorites: bool = True, placeholder: str = "Search titles &amp; authors…") -> str:
    toggles = (
        f"""  <div class="filter-toggles" role="group" aria-label="Book filter">
    <button type="button" class="filter-btn is-active" data-filter="all" aria-pressed="true">All</button>
    <button type="button" class="filter-btn" data-filter="favorites" aria-pressed="false">{BOLT_SVG}<span>Favorites</span></button>
  </div>
"""
        if include_favorites
        else ""
    )
    return f"""
<div class="filter-bar">
{toggles}  <label class="book-search-label">
    <span class="visually-hidden">Search books</span>
    {SEARCH_SVG}
    <input type="search" id="book-search" class="book-search" placeholder="{placeholder}" autocomplete="off" spellcheck="false">
  </label>
</div>
""".strip()


EMPTY_STATE = '<p id="filter-empty" class="filter-empty" role="status" aria-live="polite"></p>'


def site_nav_html(current: str) -> str:
    def cls(name: str) -> str:
        return ' class="is-current" aria-current="page"' if current == name else ""

    return f"""
<nav class="site-nav" aria-label="Primary">
  <div class="wrap site-nav-inner">
    <a href="index.html"{cls("home")}>Home</a>
    <a href="index.html#categories"{cls("categories")}>Categories</a>
    <a href="view-all.html"{cls("view-all")}>View all</a>
  </div>
</nav>
""".strip()


def category_nav_html(current_id: str | None = None) -> str:
    """Jump links across the six category pages (+ Home / View all). current_id is a category id or 'view-all'."""

    def cur(flag: bool) -> str:
        return ' class="is-current" aria-current="page"' if flag else ""

    links = [f'<a href="index.html"{cur(current_id == "home")}>Home</a>']
    for c in CATEGORIES:
        links.append(f'<a href="{c["slug"]}"{cur(current_id == c["id"])}>{c["title"]}</a>')
    links.append(f'<a href="view-all.html"{cur(current_id == "view-all")}>View all</a>')
    inner = "\n    ".join(links)
    return f"""
<nav class="category-nav" aria-label="Categories">
  <div class="wrap category-nav-inner">
    {inner}
  </div>
</nav>
""".strip()


SITE_URL = "https://peoperator.co"
SITE_NAME = "PE Operator's Book Recommendations"
SITE_TAGLINE = "Books that actually changed how I think"
OG_IMAGE = f"{SITE_URL}/og.png"
OG_IMAGE_ALT = f"{SITE_NAME}: {SITE_TAGLINE}. peoperator.co"
TWITTER_SITE = "@PEoperator"


def attr(value: str) -> str:
    """Escape for a double-quoted attribute (&, <, >, \"); apostrophes stay literal."""
    return html.escape(value, quote=False).replace('"', "&quot;")


def social_meta_html(page_title: str, description: str, path: str) -> str:
    """Canonical + Open Graph + Twitter card tags. path is '' for home or e.g. 'fiction.html'."""
    url = f"{SITE_URL}/{path}"
    return f"""  <link rel="canonical" href="{attr(url)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{attr(SITE_NAME)}">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{attr(page_title)}">
  <meta property="og:description" content="{attr(description)}">
  <meta property="og:url" content="{attr(url)}">
  <meta property="og:image" content="{attr(OG_IMAGE)}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{attr(OG_IMAGE_ALT)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="{attr(TWITTER_SITE)}">
  <meta name="twitter:title" content="{attr(page_title)}">
  <meta name="twitter:description" content="{attr(description)}">
  <meta name="twitter:image" content="{attr(OG_IMAGE)}">
  <meta name="twitter:image:alt" content="{attr(OG_IMAGE_ALT)}">
"""


def head_html(page_title: str, description: str, path: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page_title, quote=False)}</title>
  <link rel="icon" href="/favicon.png" type="image/png" sizes="any">
  <link rel="apple-touch-icon" href="/favicon.png" sizes="180x180">
  <meta name="description" content="{attr(description)}">
{social_meta_html(page_title, description, path)}  <meta name="theme-color" content="#2d2e26">
  <link rel="preload" href="fonts/archivo-latin-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="site.css">
</head>
"""


SOCIAL = """
<!-- Follow PEoperator on X, Substack, Readwise -->
<div class="social">
  <a href="https://x.com/PEoperator" target="_blank" rel="noopener" class="social-link">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
    </svg>
    Follow @PEoperator on X
  </a>
  <a href="https://peoperator.substack.com" target="_blank" rel="noopener" class="social-link social-link--substack">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M22 3.47H2v1.938h20V3.47z"/>
      <path d="M2 8.36h20v10.922c0 1.104-1.343 1.658-2.127 1.658H4.127C3.343 20.94 2 20.386 2 19.282V8.36z"/>
      <path d="M22 8.36H2v1.938h20V8.36z"/>
    </svg>
    Follow on Substack
  </a>
  <a href="https://readwise.io/peoperator/" target="_blank" rel="noopener" class="social-link social-link--readwise">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
    </svg>
    Readwise Free Trial
  </a>
</div>
""".strip()


FOOTER = """
<footer class="site-footer">
  <div class="wrap site-footer-inner">
    <div class="footer-recommend">
      <a href="https://x.com/intent/tweet?text=Book%20rec%20for%20%40PEoperator%3A%20%5Bdelete%20this%20and%20provide%20your%20book%20recommendation%21%5D"
         target="_blank" rel="noopener"
         class="x-recommend-btn"
         aria-label="Recommend a book to @PEoperator on X">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </svg>
        Recommend a book
      </a>
      <p class="footer-note">Tweet a rec to @PEoperator</p>
    </div>
    <div class="footer-fine">
      <p class="footer-disclosure">
        Links on this site may earn a small commission from qualifying purchases, at no extra cost to you. All earnings go straight back into the next recommendation!
      </p>
      <p class="footer-credit">
        Made post-workout by <a href="https://x.com/PEoperator" target="_blank" rel="noopener">@PEoperator</a> • 2025
      </p>
    </div>
  </div>
</footer>
<script src="favorites.js"></script>
</body>
</html>
""".strip()


def section_heading(title: str, meta: str = "", heading_id: str = "", icon: str = "") -> str:
    hid = f' id="{heading_id}"' if heading_id else ""
    meta_html = f'\n      <p class="section-meta">{meta}</p>' if meta else ""
    return f"""
    <div class="section-head">
      <h2 class="section-title"{hid}>{icon}{title}</h2>{meta_html}
    </div>
""".rstrip()


def books_grid(cards: list[str], grid_id: str = "books-grid", extra_class: str = "") -> str:
    inner = "\n\n    ".join(cards)
    cls = "book-grid" + (f" {extra_class}" if extra_class else "")
    return f'<div id="{grid_id}" class="{cls}">\n    {inner}\n  </div>'


def category_menu_html(books: list[dict]) -> str:
    from collections import Counter

    counts = Counter(b["category"] for b in books)
    rows = []
    for c in CATEGORIES:
        n = counts.get(c["id"], 0)
        rows.append(
            f"""
    <li>
      <a class="category-card" href="{c['slug']}">
        <h3 class="category-name">{c['title']}</h3>
        <p class="category-blurb">{c['blurb']}</p>
        <span class="category-count">{n} books</span>
        {ARROW_SVG}
      </a>
    </li>""".rstrip()
        )
    return f"""
<section id="categories" class="section section-categories" aria-labelledby="categories-title">
  {section_heading("Categories", f"{len(books)} books · {len(CATEGORIES)} categories", "categories-title")}
  <ul class="category-index" role="list">{''.join(rows)}
  </ul>
  <p class="section-foot">
    Or browse <a href="view-all.html">View all</a> A–Z.
  </p>
</section>
""".rstrip()


def build_home_search_results(books: list[dict]) -> str:
    """Full catalog grid for home site-wide search (hidden until query is non-empty)."""
    all_books = sorted(books, key=lambda b: sort_title_key(b["title"]))
    cards = [render_card(b) for b in all_books]
    return f"""
<!-- HOME SITE-WIDE SEARCH RESULTS (shown when search query is non-empty) -->
<section class="section section-search" id="home-search-results" hidden aria-hidden="true">
  {section_heading("Search results")}
  <p class="search-count" id="home-search-count" aria-live="polite"></p>
  {EMPTY_STATE}
  {books_grid(cards, grid_id="home-search-grid")}
</section>
""".rstrip()


def build_rushmore(books: list[dict]) -> str:
    rush = [b for b in books if b["rushmore"]]
    cards = [render_card(b, variant="rushmore", eager=True) for b in rush]
    return f"""
<!-- MT RUSHMORE SECTION -->
<section class="section section-rushmore" id="rushmore" aria-labelledby="rushmore-title">
  {section_heading("Mt. Rushmore", f"{len(rush)} books", "rushmore-title", BOLT_SVG)}
  <div class="rushmore-grid">
    {(chr(10) + "    ").join(cards)}
  </div>
</section>
""".rstrip()


def build_latest(books: list[dict]) -> str:
    # Top of live grid under Mt. Rushmore: first 5 non-rushmore in source order
    latest = [b for b in books if not b.get("rushmore")][:5]
    cards = [render_card(b) for b in latest]
    return f"""
<section class="section section-latest" id="latest" aria-labelledby="latest-title">
  {section_heading("Latest additions", "5 most recent", "latest-title")}
  {books_grid(cards, grid_id="latest-grid", extra_class="latest-grid")}
</section>
""".rstrip()


def masthead_home(total: int) -> str:
    return f"""
<header class="masthead masthead--home">
  {site_nav_html("home")}
  <div class="wrap">
    <div class="banner">
      <img src="Untitled.jpg" alt="PE Operator" width="1479" height="367" fetchpriority="high">
    </div>
    <div class="masthead-grid">
      <div class="masthead-copy">
        <h1 class="display">PE Operator's Book Recommendations</h1>
        <p class="tagline">Books that actually changed how I think</p>
      </div>
      <div class="masthead-tools">
        {filter_bar_html(include_favorites=False, placeholder=f"Search all {total} books…")}
      </div>
      {SOCIAL}
    </div>
  </div>
</header>
""".strip()


def masthead_page(title: str, meta: str, nav_current: str, catnav_current: str) -> str:
    return f"""
<header class="masthead masthead--page">
  {site_nav_html(nav_current)}
  <div class="wrap">
    <div class="banner banner--strip" aria-hidden="true">
      <img src="Untitled.jpg" alt="" width="1479" height="367">
    </div>
    <h1 class="display display--page">{title}</h1>
    <p class="page-meta">{meta}</p>
  </div>
  {category_nav_html(catnav_current)}
</header>
""".strip()


def page_shell(
    page_title: str, description: str, path: str, header: str, main_inner: str, body_attrs: str = ""
) -> str:
    extra = (" " + body_attrs.strip()) if body_attrs.strip() else ""
    parts = [
        head_html(page_title, description, path),
        f'<body class="site"{extra}>',
        '<a class="skip-link" href="#main">Skip to books</a>',
        header,
        f'<main id="main" class="wrap main">\n{main_inner}\n</main>',
        FOOTER,
    ]
    return "\n".join(parts) + "\n"


def catalog_main(cards: list[str], search_placeholder: str) -> str:
    return f"""
<div class="toolbar">
  {filter_bar_html(include_favorites=True, placeholder=search_placeholder)}
</div>
<section class="section section-catalog" aria-labelledby="books-title">
  <h2 class="visually-hidden" id="books-title">Books</h2>
  {EMPTY_STATE}
  {books_grid(cards)}
</section>
""".strip()


def validate_html(path: Path, text: str) -> list[str]:
    errs = []
    opens = len(re.findall(r"<article\b", text))
    closes = len(re.findall(r"</article>", text))
    if opens != closes:
        errs.append(f"{path.name}: article open={opens} close={closes}")
    fav_attr = len(re.findall(r'data-favorite="true"', text))
    lightning = len(re.findall(r"lightning\.png", text))
    if fav_attr != lightning:
        errs.append(f"{path.name}: data-favorite={fav_attr} lightning.png={lightning}")
    return errs


def main() -> None:
    extracted = json.loads((ROOT / "scripts" / "extracted_books.json").read_text(encoding="utf-8"))
    categories = json.loads((ROOT / "scripts" / "categories.json").read_text(encoding="utf-8"))

    books = extracted["books"]
    for b in books:
        cat = categories.get(b["title"])
        if not cat:
            raise SystemExit(f"Missing category for: {b['title']!r}")
        b["category"] = cat

    total = len(books)

    # --- Home ---
    # Order: search-results (hidden) first so it appears above IA when shown,
    # then Rushmore → categories → Latest → CTA (empty-query home IA).
    home_main = "\n\n".join(
        [
            build_home_search_results(books),
            build_rushmore(books),
            category_menu_html(books),
            build_latest(books),
            """
<section class="section-cta" id="home-view-all-cta">
  <a href="view-all.html" class="btn-outline">
    View all books A–Z
  </a>
</section>
""".strip(),
        ]
    )
    home = page_shell(
        SITE_NAME,
        f"{SITE_TAGLINE}. {total} hand-picked recommendations across {len(CATEGORIES)} categories, with Amazon links.",
        "",
        masthead_home(total),
        home_main,
        body_attrs='data-page="home"',
    )
    (ROOT / "index.html").write_text(home, encoding="utf-8")

    # --- Category pages ---
    for c in CATEGORIES:
        cat_books = [b for b in books if b["category"] == c["id"]]
        cat_books.sort(key=lambda b: sort_title_key(b["title"]))
        cards = [render_card(b) for b in cat_books]
        page = page_shell(
            f"{c['title']} — PE Operator Books",
            f"{c['blurb']} {len(cat_books)} hand-picked books, A–Z, from {SITE_NAME}.",
            c["slug"],
            masthead_page(c["title"], f"{c['blurb']} · {len(cat_books)} books · A–Z", "categories", c["id"]),
            catalog_main(cards, f"Search {c['title'].replace('&', '&amp;')}…"),
        )
        (ROOT / c["slug"]).write_text(page, encoding="utf-8")

    # --- View all ---
    all_books = sorted(books, key=lambda b: sort_title_key(b["title"]))
    cards = [render_card(b) for b in all_books]
    view_all = page_shell(
        "View all — PE Operator Books",
        f"All {len(all_books)} books from {SITE_NAME}, A–Z by title across {len(CATEGORIES)} categories.",
        "view-all.html",
        masthead_page("View all", f"{len(all_books)} books · A–Z by title", "view-all", "view-all"),
        catalog_main(cards, f"Search all {len(all_books)} books…"),
    )
    (ROOT / "view-all.html").write_text(view_all, encoding="utf-8")

    # Validate
    all_errs = []
    for p in [ROOT / "index.html"] + [ROOT / c["slug"] for c in CATEGORIES] + [ROOT / "view-all.html"]:
        all_errs.extend(validate_html(p, p.read_text(encoding="utf-8")))

    # Stats
    latest_titles = [b["title"] for b in books if not b.get("rushmore")][:5]
    print("Latest 5 (top of live grid under Rushmore):")
    for t in latest_titles:
        print(" -", t)
    print("Favorites total:", sum(1 for b in books if b["favorite"]))
    from collections import Counter

    print("Category counts:", dict(Counter(b["category"] for b in books)))
    if all_errs:
        print("VALIDATION ERRORS:")
        for e in all_errs:
            print(" ", e)
        raise SystemExit(1)
    print("Build OK — no validation errors")


if __name__ == "__main__":
    main()
