#!/usr/bin/env python3
"""Build peoperator.co home IA + category pages + view-all + favorites filter."""
from __future__ import annotations

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


def mark_book_card(html: str, favorite: bool) -> str:
    """Ensure article has data-book-card and optional data-favorite."""
    # Normalize opening tag
    m = re.match(r"<article([^>]*)>", html, re.DOTALL)
    if not m:
        return html
    attrs = m.group(1) or ""
    # Remove existing data-favorite / data-book-card to re-add cleanly
    attrs = re.sub(r'\s*data-favorite="[^"]*"', "", attrs)
    attrs = re.sub(r"\s*data-book-card(?:=\"[^\"]*\")?", "", attrs)
    attrs = attrs.strip()
    parts = ['data-book-card="true"']
    if favorite:
        parts.append('data-favorite="true"')
    if attrs:
        new_open = "<article " + " ".join(parts) + " " + attrs + ">"
    else:
        new_open = "<article " + " ".join(parts) + ">"
    return new_open + html[m.end() :]


def filter_bar_html() -> str:
    return """
<div class="filter-bar" role="group" aria-label="Book filter">
  <button type="button" class="filter-btn is-active" data-filter="all" aria-pressed="true">All</button>
  <button type="button" class="filter-btn" data-filter="favorites" aria-pressed="false">⚡ Favorites</button>
</div>
""".strip()


def site_nav_html(current: str) -> str:
    def cls(name: str) -> str:
        return ' class="is-current"' if current == name else ""

    return f"""
<nav class="site-nav" aria-label="Primary">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-center gap-2 sm:gap-4 text-sm sm:text-base">
    <a href="index.html"{cls("home")}>Home</a>
    <span class="text-gray-500 hidden sm:inline" aria-hidden="true">·</span>
    <a href="index.html#categories"{cls("categories")}>Categories</a>
    <span class="text-gray-500 hidden sm:inline" aria-hidden="true">·</span>
    <a href="view-all.html"{cls("view-all")}>View all</a>
  </div>
</nav>
""".strip()


def head_html(page_title: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <link rel="icon" href="/favicon.png" type="image/png" sizes="any">
  <link rel="apple-touch-icon" href="/favicon.png" sizes="180x180">
  <meta name="description" content="{description}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="site.css">
</head>
"""


HEADER_HERO = """
<body class="bg-gray-50 text-gray-800 min-h-screen flex flex-col">

  <!-- Header with your custom image -->
 <header class="relative overflow-hidden py-16 md:py-20 bg-black">
  <img src="https://raw.githubusercontent.com/PEoperator/book-recommendations/main/Untitled.jpg"
       alt="PE Operator"
       class="absolute inset-0 w-full h-full object-cover object-center">

  <!-- Dark overlay -->
  <div class="absolute inset-0 bg-black bg-opacity-60"></div>

  <!-- Text content -->
  <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
    <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-4 leading-tight drop-shadow-2xl">
      PE Operator's Book Recommendations
    </h1>
    <p class="text-lg sm:text-xl md:text-2xl lg:text-3xl drop-shadow-lg max-w-4xl mx-auto">
      Books that actually changed how I think
    </p>
  </div>
</header>
""".rstrip()


SOCIAL = """
<!-- Follow PEoperator on X, Substack, Readwise - Horizontal buttons -->
<div class="text-center my-6">
  <div class="inline-flex flex-wrap justify-center gap-5">
    <!-- X / Twitter Button -->
    <a href="https://x.com/PEoperator" target="_blank" rel="noopener"
       class="inline-flex items-center gap-3 bg-black hover:bg-gray-800 text-white font-bold py-3.5 px-7 rounded-full transition shadow-lg text-base">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
      </svg>
      Follow @PEoperator on X
    </a>

    <!-- Substack Button -->
    <a href="https://peoperator.substack.com" target="_blank" rel="noopener"
       class="inline-flex items-center gap-3 bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 px-7 rounded-full transition shadow-lg text-base">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 3.47H2v1.938h20V3.47z"/>
        <path d="M2 8.36h20v10.922c0 1.104-1.343 1.658-2.127 1.658H4.127C3.343 20.94 2 20.386 2 19.282V8.36z"/>
        <path d="M22 8.36H2v1.938h20V8.36z"/>
      </svg>
      Follow on Substack
    </a>

    <!-- Readwise Button -->
    <a href="https://readwise.io/peoperator/" target="_blank" rel="noopener"
       class="inline-flex items-center gap-3 bg-[#488BD2] hover:bg-[#3a75b8] text-white font-bold py-3.5 px-7 rounded-full transition shadow-lg text-base">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
      </svg>
      Readwise Free Trial
    </a>
  </div>
</div>
""".rstrip()


FOOTER = """
<!-- Sticky Footer -->
<footer class="w-full bg-gray-900 text-white mt-auto">
  <div class="max-w-7xl mx-auto px-6 py-10 text-center space-y-4">
    <p class="text-sm italic opacity-75 leading-snug">
      Links on this site may earn a small commission from qualifying purchases, at no extra cost to you. All earnings go straight back into the next recommendation!
    </p>
    <p class="text-base">
      Made post-workout by <a href="https://x.com/PEoperator" target="_blank" rel="noopener" class="font-bold hover:underline">@PEoperator</a> • 2025
    </p>
  </div>
</footer>
<script src="favorites.js"></script>
</body>
</html>
""".rstrip()


def section_heading(title: str) -> str:
    return f"""
    <div class="text-left mb-6 border-b-2 border-gray-900 pb-4">
      <h2 class="text-3xl md:text-4xl font-extrabold text-gray-900 tracking-tight">{title}</h2>
    </div>
""".rstrip()


def books_grid(cards: list[str], grid_id: str = "books-grid", cols: str | None = None) -> str:
    if cols is None:
        cols = "grid grid-cols-2 min-[480px]:grid-cols-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 md:gap-8"
    inner = "\n\n".join(cards)
    return f'<div id="{grid_id}" class="{cols}">\n{inner}\n</div>'


def category_menu_html() -> str:
    cards = []
    for c in CATEGORIES:
        cards.append(
            f"""
        <a class="category-card" href="{c['slug']}">
          <h3>{c['title']}</h3>
          <p>{c['blurb']}</p>
        </a>""".rstrip()
        )
    return f"""
<section id="categories" class="pb-10">
  {section_heading("Categories")}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-6">
{''.join(cards)}
  </div>
  <p class="mt-6 text-center text-gray-600">
    Or browse <a href="view-all.html" class="font-bold text-gray-900 underline hover:no-underline">View all</a> A–Z.
  </p>
</section>
""".rstrip()


def build_rushmore(books: list[dict]) -> str:
    rush = [b for b in books if b["rushmore"]]
    cards = [mark_book_card(b["html"], b["favorite"]) for b in rush]
    # Keep amber ring classes already on rushmore articles
    return f"""
<!-- MT RUSHMORE SECTION -->
<section class="pb-10" id="rushmore">
  <div class="max-w-7xl mx-auto px-6">
    {section_heading("Mt. Rushmore")}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8 mt-6">
{chr(10).join(cards)}
    </div>
    <div class="border-b-2 border-gray-900 mt-8"></div>
  </div>
</section>
""".rstrip()


def build_latest(books: list[dict]) -> str:
    # Bottom-of-file recency: last 5 in source order; display newest first
    latest = list(reversed(books[-5:]))
    cards = [mark_book_card(b["html"], b["favorite"]) for b in latest]
    cols = "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6 md:gap-8 mt-6"
    return f"""
<section class="pb-10" id="latest">
  <div class="max-w-7xl mx-auto px-6">
    {section_heading("Latest additions")}
    {books_grid(cards, grid_id="latest-grid", cols=cols)}
  </div>
</section>
""".rstrip()


def page_shell(
    page_title: str,
    description: str,
    nav_current: str,
    main_inner: str,
    include_hero: bool = True,
    include_social: bool = True,
) -> str:
    parts = [head_html(page_title, description)]
    if include_hero:
        parts.append(HEADER_HERO)
    else:
        parts.append(
            '<body class="bg-gray-50 text-gray-800 min-h-screen flex flex-col">\n'
            '<header class="bg-black text-white py-8">\n'
            '  <div class="max-w-6xl mx-auto px-4 text-center">\n'
            f'    <h1 class="text-3xl sm:text-4xl font-bold">{page_title}</h1>\n'
            "  </div>\n"
            "</header>"
        )
    parts.append(site_nav_html(nav_current))
    if include_social:
        parts.append(SOCIAL)
    parts.append(f'<main class="flex-grow max-w-7xl mx-auto px-6 py-6">\n{filter_bar_html()}\n{main_inner}\n</main>')
    parts.append(FOOTER)
    return "\n".join(parts) + "\n"


def validate_html(path: Path, text: str) -> list[str]:
    errs = []
    opens = len(re.findall(r"<article\b", text))
    closes = len(re.findall(r"</article>", text))
    if opens != closes:
        errs.append(f"{path.name}: article open={opens} close={closes}")
    # Check nested quotes in attributes (simple heuristic: attr="... " ...")
    # Count data-favorite
    fav_attr = len(re.findall(r'data-favorite="true"', text))
    lightning = len(re.findall(r"lightning\.png", text))
    # lightning appears once per favorite card; rushmore etc same
    if fav_attr and lightning and fav_attr != lightning:
        # allow mismatch note only if significant
        if abs(fav_attr - lightning) > 0:
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
        b["html"] = mark_book_card(b["html"], b["favorite"])

    # --- Home ---
    home_main = "\n\n".join(
        [
            build_rushmore(books),
            build_latest(books),
            category_menu_html(),
            """
<!-- Optional footer CTA -->
<section class="pb-6 text-center">
  <div class="inline-flex flex-wrap justify-center gap-4">
    <a href="view-all.html" class="inline-flex items-center gap-2 bg-gray-900 hover:bg-black text-white font-bold py-3 px-6 rounded-full transition shadow-lg">
      View all books A–Z
    </a>
  </div>
</section>
""".rstrip(),
        ]
    )
    home = page_shell(
        "PE Operator's Book Recommendations",
        "Hand-picked books that changed how I think — with Amazon links",
        "home",
        home_main,
        include_hero=True,
        include_social=True,
    )
    (ROOT / "index.html").write_text(home, encoding="utf-8")

    # --- Category pages ---
    for c in CATEGORIES:
        cat_books = [b for b in books if b["category"] == c["id"]]
        cat_books.sort(key=lambda b: sort_title_key(b["title"]))
        cards = [b["html"] for b in cat_books]
        empty = (
            '<p id="favorites-empty" class="favorites-empty">'
            "No favorites in this category."
            "</p>"
        )
        main_inner = f"""
<section class="pb-10">
  <div class="max-w-7xl mx-auto">
    {section_heading(c["title"])}
    <p class="text-gray-600 mb-4">{c["blurb"]} · {len(cat_books)} books · A–Z</p>
    {empty}
    {books_grid(cards)}
  </div>
</section>
""".rstrip()
        page = page_shell(
            f"{c['title']} — PE Operator Books",
            f"PE Operator book recommendations: {c['title']}",
            "categories",
            main_inner,
            include_hero=False,
            include_social=False,
        )
        (ROOT / c["slug"]).write_text(page, encoding="utf-8")

    # --- View all ---
    all_books = sorted(books, key=lambda b: sort_title_key(b["title"]))
    cards = [b["html"] for b in all_books]
    empty = (
        '<p id="favorites-empty" class="favorites-empty">'
        "No favorites in this category."
        "</p>"
    )
    # Reuse same empty copy per spec for category/view-all
    view_main = f"""
<section class="pb-10">
  <div class="max-w-7xl mx-auto">
    {section_heading("View all")}
    <p class="text-gray-600 mb-4">{len(all_books)} books · A–Z by title</p>
    {empty}
    {books_grid(cards)}
  </div>
</section>
""".rstrip()
    view_all = page_shell(
        "View all — PE Operator Books",
        "All PE Operator book recommendations A–Z",
        "view-all",
        view_main,
        include_hero=False,
        include_social=False,
    )
    (ROOT / "view-all.html").write_text(view_all, encoding="utf-8")

    # Validate
    all_errs = []
    for p in [ROOT / "index.html"] + [ROOT / c["slug"] for c in CATEGORIES] + [ROOT / "view-all.html"]:
        all_errs.extend(validate_html(p, p.read_text(encoding="utf-8")))

    # Stats
    latest_titles = [b["title"] for b in reversed(books[-5:])]
    print("Latest 5 (newest first):")
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
