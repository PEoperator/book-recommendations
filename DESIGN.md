---
name: PE Operator's Book Recommendations
description: A personal book shelf set on the banner's own charcoal, lit by three bolt colours.
colors:
  charcoal: "#2d2e26"
  charcoal-deep: "#23241d"
  surface: "#383930"
  surface-hi: "#45463b"
  rule: "#4f5045"
  rule-strong: "#8a8b7c"
  chalk: "#f3f1e7"
  chalk-muted: "#c4c2b2"
  chalk-placeholder: "#b3b1a0"
  bolt-yellow: "#eeb937"
  bolt-yellow-hi: "#f6cd5c"
  bolt-blue: "#1f5fa1"
  bolt-blue-lite: "#8cb8ec"
  bolt-orange: "#e56e1f"
  bolt-orange-lite: "#f08a45"
typography:
  display:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 1.35rem + 4.6vw, 5.25rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 72"
  headline:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(1.75rem, 1.3rem + 1.6vw, 2.625rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.015em"
    fontVariation: "'wdth' 78"
  title:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 650
    lineHeight: 1.22
    fontVariation: "'wdth' 94"
  body:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 600
    letterSpacing: "0.06em"
    fontVariation: "'wdth' 112"
rounded:
  cover: "3px 6px 6px 3px"
  panel: "14px"
  control: "999px"
spacing:
  "1": "0.25rem"
  "2": "0.5rem"
  "3": "0.75rem"
  "4": "1rem"
  "5": "1.25rem"
  "6": "1.5rem"
  "8": "2rem"
  "10": "2.5rem"
  "12": "3rem"
  "16": "4rem"
components:
  button-primary:
    backgroundColor: "{colors.bolt-yellow}"
    textColor: "{colors.charcoal-deep}"
    rounded: "{rounded.control}"
    padding: "0 1.5rem"
    height: "3.25rem"
  button-primary-hover:
    backgroundColor: "{colors.bolt-yellow-hi}"
  button-outline:
    textColor: "{colors.chalk}"
    rounded: "{rounded.control}"
    padding: "0 1.5rem"
    height: "3rem"
  filter-toggle-active:
    backgroundColor: "{colors.bolt-yellow}"
    textColor: "{colors.charcoal-deep}"
    rounded: "{rounded.control}"
    height: "2.5rem"
  input-search:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.chalk}"
    rounded: "{rounded.control}"
    height: "2.875rem"
  chip-current:
    backgroundColor: "{colors.bolt-yellow}"
    textColor: "{colors.charcoal-deep}"
    rounded: "{rounded.control}"
    height: "2.5rem"
---

# Design System: PE Operator's Book Recommendations

## Overview

**Creative North Star: "The Lit Shelf"**

The whole site sits on the charcoal of PE Operator's banner art, so the banner is not a picture placed on a page; it is the page. Book covers are the content and the only large colour on screen; everything else (nav, headings, controls, rules) is chalk-on-charcoal and stays out of their way. The three bolt colours from the banner do specific jobs instead of decorating.

Density is high on catalog pages (six covers per row on desktop, two on phones) and relaxed on the home page, where Mt. Rushmore gets four big covers and the categories read like a book's table of contents.

**Key Characteristics:**
- One ground colour (#2d2e26) shared with the banner art; footer one step deeper.
- Covers as objects: bound-edge radius, soft drop shadow, faint spine crease. No white card boxes.
- Lightning badge (`lightning.png`) on every favourite, cut out of the ground with a 3px charcoal ring.
- One variable family (Archivo) doing every role through width + weight.

## Colors

Sampled from `Untitled.jpg`: charcoal ground, and the yellow, blue and orange bolts.

### Primary
- **Bolt Yellow** (#eeb937): favourites (badge, Favorites toggle icon), current page (nav underline, current chip), the primary action ("Recommend a book"), the Mt. Rushmore rule, text selection, focus of the search field. 7.6:1 on charcoal.

### Secondary
- **Bolt Blue Lite** (#8cb8ec): keyboard focus rings everywhere; the Readwise icon. The raw banner blue (#1f5fa1) is too dark for text on charcoal and stays in the art.

### Tertiary
- **Bolt Orange** (#e56e1f / lite #f08a45): hover energy only (category arrow on hover, Substack icon). Never body text.

### Neutral
- **Charcoal** (#2d2e26): page ground and banner background.
- **Charcoal Deep** (#23241d): footer; text on yellow.
- **Surface** (#383930) / **Surface Hi** (#45463b): search field rest / hover.
- **Rule** (#4f5045): decorative hairlines. **Rule Strong** (#8a8b7c): control borders (3:1+).
- **Chalk** (#f3f1e7, 12.1:1): primary text. **Chalk Muted** (#c4c2b2, 7.6:1): authors, blurbs, meta. **Chalk Placeholder** (#b3b1a0, 5.4:1 on surface).

### Named Rules
**The Covers Own Colour Rule.** Large fields of colour belong to book covers. UI colour is limited to the three bolt roles above.
**The Yellow Means Him Rule.** Yellow marks PE Operator's taste or the current place: favourites, Mt. Rushmore, current page, the one primary action.

## Typography

**Display / Body / Label Font:** Archivo variable (self-hosted `fonts/archivo-*-var.woff2`, wdth 62–125, wght 100–900), fallback system-ui.

**Character:** A grotesque that can go condensed and heavy like the bold cover type on the shelf, normal width for reading, and expanded for small labels, so one family carries the whole hierarchy.

### Hierarchy
- **Display** (800, wdth 72, clamp 2.5–5.25rem, lh 0.94): home h1.
- **Page title** (800, wdth 72, clamp 2.25–4.25rem): category / View all h1.
- **Headline** (800, wdth 78, clamp 1.75–2.625rem, lh 1): section headings.
- **Category name** (750, wdth 82, clamp 1.3–1.75rem): category index rows.
- **Title** (650, wdth 94, 1rem, lh 1.22): book titles; Rushmore titles 700, wdth 86, up to 1.375rem.
- **Body** (400, 1rem, lh 1.5): blurbs, notes. Author line 0.875rem muted.
- **Label** (600, wdth 112, 0.8125rem, +0.06em, uppercase, tabular nums): nav, chips, counts, section meta.

## Layout

Container `max-width: 82rem` with fluid gutter `clamp(1rem, 3.5vw, 2.5rem)`. Spacing scale on a 4px base (`--s-1`…`--s-20`). Sections open with `clamp(3rem, 2rem + 4vw, 5.5rem)` above and `2rem` between heading rule and content (more above a heading than below).

- **Book grid:** 2 columns under 560px; `auto-fill minmax(10rem, 1fr)` to 1199px; 6 columns at 1200px+.
- **Mt. Rushmore:** 2×2 under 768px, 4 across above.
- **Latest additions:** 5 across at 900px+; a scroll-snap rail (42% wide items) under 640px.
- **Category index:** one column on phones, two columns at 768px+, hairline-separated rows.
- **Catalog toolbar** (All | Favorites + search): sticky at 640px+, static on phones.
- **Category chips:** wrap on desktop, one swipeable row with an edge fade under 768px.

## Elevation & Depth

Flat ground, depth only on books. Covers carry the only shadows; they lift on hover.

### Shadow Vocabulary
- **Cover rest** (`0 1px 2px rgb(0 0 0 / .45), 0 12px 24px -10px rgb(0 0 0 / .65)`)
- **Cover lift** (`0 2px 4px rgb(0 0 0 / .4), 0 22px 36px -14px rgb(0 0 0 / .75)`): hover, with `translateY(-5px)`.
- **Badge** (`0 0 0 3px #2d2e26, 0 4px 10px rgb(0 0 0 / .5)`).

## Shapes

Covers `3px 6px 6px 3px` (bound edge left). Banner panels 14px. Controls (toggles, search, chips, buttons) are pills. Rows and sections are separated by 1px hairlines, never boxes.

## Components

### Buttons
- **Primary ("Recommend a book"):** bolt-yellow pill, charcoal-deep text, 3.25rem tall; hover yellow-hi + 1px lift.
- **Outline ("View all books A–Z"):** 2px yellow border, chalk text; hover fills yellow.

### Filter toggle (All | Favorites)
Segmented pill with a 1px rule-strong outline. Active segment is yellow with charcoal text; the Favorites segment carries an SVG bolt. Turning Favorites on plays the one authored motion: every visible badge "strikes" (scale + brightness, 600ms ease-out; disabled under reduced motion).

### Inputs / Search
Surface pill with a 1px rule-strong border and an SVG magnifier; focus = yellow border + 2px yellow outline. Placeholder names the scope ("Search all 271 books…", "Search Fiction…").

### Navigation
Primary nav: expanded uppercase labels, muted; current page yellow with a 2px underline. Category chips: label type in pills; current chip filled yellow.

### Book (signature)
Cover frame + badge + title + author inside one link. The extracted card HTML is re-rendered at build time, keeping the original `<a>` tag, cover `src`/`alt`, title and author byte-for-byte.

### Category row
Name (condensed 750), blurb, count label, arrow; hover turns the name yellow and slides the arrow in orange.

## Do's and Don'ts

### Do:
- **Do** keep the ground #2d2e26 so the banner art blends in with no seams.
- **Do** use yellow only for favourites, current state and the single primary action.
- **Do** keep every affiliate `href` byte-identical; change markup around it, never the tag.
- **Do** keep focus rings bolt-blue-lite (#8cb8ec), 3px.

### Don't:
- **Don't** put covers back in white card boxes; white covers vanish into them.
- **Don't** use emoji as icons (the old "⚡" label); use the SVG bolt or `lightning.png`.
- **Don't** place text over the banner art; set it beneath on charcoal.
- **Don't** add coloured glow shadows; shadows stay neutral and offset.
