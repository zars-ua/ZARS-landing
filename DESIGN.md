---
name: ЗАРС — Лоція узбережжя
description: "Одна навігаційна карта, три фарби друку: холдинг, Французький бульвар 29, Французький бульвар 29Б."
colors:
  paper: "#ECE6DB"
  paper-deep: "#DED6C7"
  holding-ground: "#0E1620"
  holding-ground-2: "#141E2A"
  holding-field: "#23374E"
  holding-text: "#E8E2D6"
  holding-text-dim: "#9AA4B0"
  holding-ink: "#D0703F"
  holding-ink-pure: "#B05523"
  holding-ink-on-paper: "#9C4618"
  fb29-ground: "#F1EDE5"
  fb29-ground-2: "#E7E1D5"
  fb29-field: "#DCD5C6"
  fb29-text: "#1C2433"
  fb29-text-dim: "#5A6478"
  fb29-ink: "#294069"
  fb29b-ground: "#1A0F0A"
  fb29b-ground-2: "#241610"
  fb29b-field: "#2C1C14"
  fb29b-text: "#EDE3DA"
  fb29b-text-dim: "#A79589"
  fb29b-ink: "#CC6E35"
  fb29b-ink-pure: "#913814"
  holding-warn: "#E4673E"
  fb29-warn: "#A8330E"
  fb29b-warn: "#E4673E"
  fb29b-ink-on-paper: "#8A3512"
typography:
  display:
    fontFamily: "Anglecia, Georgia, serif"
    fontSize: "clamp(2.4rem, 1.6rem + 3.4vw, 4.25rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Anglecia, Georgia, serif"
    fontSize: "clamp(1.95rem, 1.35rem + 2.6vw, 3.1rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Anglecia, Georgia, serif"
    fontSize: "clamp(1.5rem, 1.1rem + 1.8vw, 2.25rem)"
    fontWeight: 400
    lineHeight: 1.18
    letterSpacing: "-0.015em"
  lead:
    fontFamily: "Anglecia, Georgia, serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "Montserrat, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
    fontFeature: "tabular-nums"
  body-small:
    fontFamily: "Montserrat, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "History, Georgia, serif"
    fontSize: "0.75rem"
    fontWeight: 400
    letterSpacing: "0.24em"
    textTransform: "uppercase"
  action:
    fontFamily: "Montserrat, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.1em"
    textTransform: "uppercase"
rounded:
  none: "0"
  hairline: "1px"
  dot: "50%"
spacing:
  gutter: "clamp(1.25rem, 4vw, 3rem)"
  bleed: "clamp(1.25rem, 5vw, 5.5rem)"
  section: "clamp(4rem, 8vw, 7.5rem)"
  block: "clamp(1.6rem, 3vw, 2.6rem)"
  cell: "clamp(1.6rem, 3vw, 2.4rem)"
  hairline: "1px"
components:
  action-primary:
    backgroundColor: "{colors.holding-ink}"
    textColor: "{colors.holding-ground}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "1.05rem 2rem"
  action-primary-hover:
    backgroundColor: "transparent"
    textColor: "{colors.holding-ink}"
  action-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.holding-ink}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "1.05rem 2rem"
  action-quiet-hover:
    backgroundColor: "{colors.holding-ink}"
    textColor: "{colors.holding-ground}"
  field-input:
    backgroundColor: "transparent"
    textColor: "{colors.holding-text}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.65rem 0"
  plate-tab:
    backgroundColor: "{colors.holding-ground}"
    textColor: "{colors.holding-text-dim}"
    typography: "{typography.body-small}"
    rounded: "{rounded.none}"
    padding: "0.9rem 1.2rem"
  plate-tab-selected:
    backgroundColor: "{colors.holding-ink}"
    textColor: "{colors.holding-ground}"
  cartouche:
    backgroundColor: "{colors.holding-ground}"
    textColor: "{colors.holding-text}"
    rounded: "{rounded.none}"
    padding: "clamp(1.1rem, 2.4vw, 1.8rem) clamp(1.2rem, 2.8vw, 2.2rem)"
---

# Design System: ЗАРС — Лоція узбережжя

## Overview

**Creative North Star: "The Coastal Chart"** (Лоція узбережжя)

The site is drawn as a navigation chart of the Odesa shoreline, not as a brochure. Every claim on it is a measurement — distances, depths, wall thicknesses in millimetres, floor plates, percentages of completion — and the visual language is the language of a printed chart: hairline rules, a cartouche, a legend, range rings taken from real OSM coordinates, a soundings scale bar. There is no adjective on screen that could not be verified, and no decorative geometry that is not carrying data.

One system prints in three inks. `<html data-chart="holding|fb29|fb29b">` swaps a block of custom properties and nothing else: the holding is a night chart in terracotta, Французький бульвар 29 is the daylight paper edition in navy, Французький бульвар 29Б is a night chart in rust. The layout, rhythm, type ramp, rules and components are byte-identical across the three; only ground, ink and text tokens change. A fourth edition would be a new `[data-chart]` block, never a new stylesheet.

Depth is drawn, never lit. There is not a single drop shadow in the build. Surfaces separate by tone (`--ground` / `--ground-2` / `--field`), by hairline (`--line`, `--line-2`) and by translucency over photography (`color-mix` plus `backdrop-filter`). Corners are square everywhere; the only curves in the system are a legend dot and the 1px softening of the focus ring. Motion is plotting, not fading: coastlines draw themselves along their own stroke length, bars grow by `scaleX` from their left origin, sections settle up by 1.4rem — and all of it collapses to a static chart under `prefers-reduced-motion`.

**Key Characteristics:**
- One chart, three ink editions, swapped by a single `data-chart` attribute on `<html>`.
- Square corners, hairline rules, zero drop shadows.
- Numbers are typeset as measurements (tabular figures, tick marks, units), never as hero-metric cards.
- Display serif for voice, CAPS-only chart face for labels, Montserrat for everything read.
- Motion is drawing; every motion has a reduced-motion null state.
- Generated geometry: the coast, the plans and the map rings come from OSM and from the client's own booklets, not from illustration.

## Colors

Three printings of one chart: a dark ground carrying a warm ink, a paper ground carrying a cold ink, and a dark brown ground carrying rust. Ink is always the single accent; there is no secondary accent anywhere in the build.

### Primary
- **Terracotta Ink** (`{colors.holding-ink}`): the holding edition's accent — logo mark, actions, soundings figures, range rings, scrollbar thumb, selection. Lightened from the brand terracotta specifically so it can carry text (measured 5.26:1 on the holding ground).
- **Brand Terracotta** (`{colors.holding-ink-pure}`): the guideline hex. Reserved for large fields and the logo. Measured 3.61:1 on the holding ground — it fails AA for text and must never be used as a text colour on the dark ground.
- **Boulevard Navy** (`{colors.fb29-ink}`): the delivered building's ink, taken straight from the ФБ29 booklet. Passes comfortably on paper (8.85:1), so here the brand hex and the text hex are the same value — no lightened variant exists or is needed.
- **Rust Ink** (`{colors.fb29b-ink}`): the under-construction edition's accent, lightened from the presentation rust to clear AA on BOTH its grounds — 5.24:1 on `--ground` and 4.89:1 on `--ground-2`. The first lightening (#C4652E) cleared the primary ground at 4.70 but measured 4.38 on the second; the token is set by the harder of the two pairs, not the easier one.
- **Presentation Rust** (`{colors.fb29b-ink-pure}`): the ФБ29Б presentation hex. 2.49:1 on its own ground — fields and lockups only, never text.
- **Ink on Paper** (`{colors.holding-ink-on-paper}`, `{colors.fb29b-ink-on-paper}`): the two dark-edition inks re-darkened for use inside a paper inset, where the ground inverts (5.12:1 and 6.51:1 on paper).

### Neutral
- **Chart Paper** (`{colors.paper}`): the inset ground. A paper insert dropped into a night chart; it carries its own text, dim, line and ink overrides so a whole section can invert without touching the page edition.
- **Daylight Ground** (`{colors.fb29-ground}`): the ФБ29 page ground. **Not a drift from Chart Paper** — a daylight chart is printed on a lighter, cooler stock than an insert glued onto a night chart. Two tokens, two jobs; do not merge them.
- **Grounds and Fields** (`{colors.holding-ground}` / `-2` / `{colors.holding-field}`, and the fb29 / fb29b equivalents): page ground, recessed band (soundings, enquiry), and the sea / image-placeholder field. Section separation is tonal, by these three steps.
- **Chart Text and Dim** (`{colors.holding-text}` / `{colors.holding-text-dim}` and edition equivalents): body ink and secondary ink. Every dim token was chosen above 4.5:1 on its own ground (7.20 / 5.10 / 6.54).
- **Hairlines** (`--line` at 16–18% and `--line-2` at 8–9% of the text colour): all borders, all grid gaps, all rules. They are derived from text, not defined per edition as hex.

### Named Rules
**The Two-Hex Ink Rule.** Every ink exists twice: the brand hex for fields and lockups, and a legibility hex for anything a reader has to read. On the holding and 29Б grounds those are different values (measured 3.61:1 and 2.49:1 for the brand hexes — both fail); on 29 they coincide. Never set text in `--ink-pure`.

**The One Ink Rule.** A page has exactly one accent. Ink marks the action, the measured figure, the current nav item, the tick marks and the chart rings — and nothing else. If a second accent seems necessary, the answer is a tonal step (`--ground-2`, `--field`) or a hairline.

**The Edition Rule.** Colour never appears as a literal in a component. Components read `--ground`, `--ink`, `--text`, `--line`; the edition is decided once, on `<html data-chart>`. The only sanctioned literals are the two identity tints on the holding page's object cards (`#294069` / `#913814` mixed into the ground), which quote each building's own ink as a preview.

## Typography

**Display Font:** Anglecia Pro Display (fallback Georgia, serif) — self-hosted woff2, Latin + Cyrillic + ґҐ subset.
**Body Font:** Montserrat 300/400/500 (fallback system-ui, sans-serif) — self-hosted woff2 subsets, one file per weight.
**Label Font:** History Pro (fallback Georgia, serif) — self-hosted woff2 subset.

All three are the client's own licensed faces. Montserrat is a deliberate, licensed keep: a design detector will flag it as over-used, and the answer is that it is the client's brand face and is subset and self-hosted here. It is not a default to be "improved".

**Character:** A chart has a hand and a stamp. Anglecia speaks — headings, measured figures, the ledger's terms, the "29" monogram — with a slight negative tracking (-0.015em) that keeps the serif tight rather than literary. History Pro is the stamp: letterspaced caps for every chart annotation. Montserrat is everything the eye actually travels along, with tabular figures on by default so columns of measurements align.

### Hierarchy
- **Display** (Anglecia 400, `clamp(2.4rem, 1.6rem + 3.4vw, 4.25rem)`, 1.02): the one `h1` per page, balanced with `text-wrap: balance`.
- **Headline** (Anglecia 400, `clamp(1.95rem, 1.35rem + 2.6vw, 3.1rem)`, 1.08): section titles.
- **Title** (Anglecia 400, `clamp(1.5rem, 1.1rem + 1.8vw, 2.25rem)`, 1.18): object and rule titles, soundings figures.
- **Lead** (Anglecia 400, 1.25rem, 1.55): the single standfirst paragraph under a heading. One per section at most.
- **Body** (Montserrat 400, 1.0625rem / 17px, 1.65, max `68ch`): all running text. 17px is a floor, chosen for a 35–65 audience; 15px (`--t-sm`) is the floor for secondary text that is still read. Nothing below 0.8125rem carries a sentence.
- **Label** (History Pro 400, 0.75rem, 0.20–0.24em tracking, uppercase): chart annotations, field labels, statuses, figure captions, nav items.

### Named Rules
**The CAPS-Only Rule.** History Pro is a caps-only face: its lowercase renders as small caps. It may only ever be set with `text-transform: uppercase` and ≥0.2em tracking, in labels, statuses, captions, nav and lockups. It must never set a sentence-case heading, a paragraph, or a line of body copy. There is no exception and no "just this once".

**The Measured Figure Rule.** A number that is a measurement is set in Anglecia in ink with its unit in dim Montserrat beside it, and it stands on a tick mark. Tabular figures are on for the whole document; never turn them off in a column of numbers.

**The No-Eyebrow Rule.** No kicker, eyebrow or label line sits above a heading as decoration. Labels exist — but they title a chart block (the cartouche, the legend head, a figure caption, a field), never a heading. Where a lockup was needed above the hero heading, it became the legend's own title block instead.

## Layout

One column, one measure. `--col` is `min(1360px, 100% - var(--bleed) * 2)` and `.wrap` centres it; the page bleed grows `clamp(1.25rem, 5vw, 5.5rem)` and the internal gutter `clamp(1.25rem, 4vw, 3rem)`. Reading measure is capped at `68ch` on every paragraph by default.

Vertical rhythm is section-scale: `padding-block: clamp(4rem, 8vw, 7.5rem)` on every `section`, with `section + section` separated by a single faint hairline (`--line-2`). Sections are not cards; they are bands on one continuous sheet. A band changes character by taking `--ground-2` (soundings, enquiry) or by becoming a paper inset, never by floating.

Recurring grids, all two-column and all collapsing to one:
- **The two** (`minmax(0, 20rem) / 1fr`): a sticky side column (top: 7rem) against the main text.
- **The ledger / rules / awards** (`18rem / 1fr`, `22rem / 1fr`, `20rem / 1fr`): term against definition, separated by top hairlines, closed by a bottom hairline on the last row.
- **The object row** (`1.35fr / 1fr`): photograph against its card.
- **The tiled grids** (city, gallery, legend): `gap: 1px` on a `--line` background, so the grid gap *is* the rule. This is the system's signature grid device.

Breakpoints are three, and each one has a stated reason in the source: **1000px** collapses every two-column grid to one; **900px** hides the range-ring labels (over narrow text they read as typesetting errors) and gives the dark editions' hero panel a translucent backing; **720px** compacts the header (phone number out, full nav words out, logo to 62px), drops the hero to 92svh, and reflows the soundings bar to two columns.

**The Hairline Grid Rule.** Separation is a 1px line at 8–18% of the text colour, or a 1px grid gap over a `--line` background. Not a border-radius, not a box, not a shadow.

## Elevation & Depth

**This system has no shadows.** There is exactly one `box-shadow` in the entire build and it is `inset 0 0 0 1px` — a ring drawn to hollow out a legend dot, i.e. a border, not a lift. Nothing floats, nothing hovers above the sheet, nothing casts.

Depth is produced three other ways:
1. **Tonal layering.** `--ground` → `--ground-2` → `--field` is the whole vocabulary of recession. Bands that matter sit on `--ground-2`.
2. **Translucency over photography.** Where a surface must sit on an image — header, hero panel, legend, cartouche — it is `color-mix(in srgb, var(--ground) 72–94%, transparent)` plus `backdrop-filter: blur(6–14px)` plus a hairline border with a 3px top edge. The blur is how a chart overlay reads as an overlay.
3. **Gradient scrims.** Heroes carry a 100deg scrim that quiets the left of the frame so type lands on calm field; the header carries an 8rem top scrim that disappears (`opacity: 0`) the moment the page is scrolled and the header takes its own solid backing.

**The Flat Chart Rule.** Nothing in this system is lifted. If a surface needs to separate from what is behind it, it takes a tonal step, a hairline, or a blurred ground-tinted backing — in that order. A drop shadow anywhere is a defect.

## Shapes

Square. `border-radius: 0` is the default and is asserted explicitly on inputs; the only radii in the build are `50%` on the legend's 0.6rem dot and `1px` on the focus ring. Panels are rectangles with a 1px border and a **3px top edge** — the cartouche's signature, repeated on the hero title panel. Bars are plain rectangles whose width encodes a real quantity (wall thickness in millimetres via `calc(var(--mm) / 640 * 100%)`, readiness via `calc(var(--p) * 1%)`). Tick marks are 1px verticals. Links underline with a 1px gradient strip that retracts to the right on hover rather than changing colour.

**The Square Corner Rule.** Radius is zero unless the shape is literally a dot. A rounded card in this world is a foreign object.

## Components

### Actions (`.act`, `.act--quiet`)
- **Character:** a stamped instruction with a bearing line after it.
- **Shape:** square (0), 1px border in ink, padding 1.05rem 2rem, Montserrat 500 uppercase at 0.1em.
- **Primary:** ink ground, `--on-ink` text. **Quiet:** transparent ground, ink text. The two are exact inverses and swap on hover.
- **The bearing line:** a 2.4rem × 1px rule after the label, held at `scaleX(0.625)` and extending to full on hover/focus. It animates by `transform`, deliberately not by `width`, so it never reflows the button.
- **Hover / Focus:** 420ms `cubic-bezier(0.16, 1, 0.3, 1)`; focus-visible gets the same treatment as hover plus the global 2px ink outline at 3px offset.

### Fields (`.field`)
- **Style:** no box. Transparent ground, bottom hairline only, square corners, 0.65rem vertical padding, Montserrat 400 at 17px. The label above is History Pro caps.
- **Focus:** bottom rule thickens to 2px in ink, with `padding-bottom` reduced by 1px so the baseline does not jump.
- **Select:** native `appearance: none` with a 0.5rem rotated chevron drawn from two 1px borders; `option` is repainted in `--ground` / `--text` so the native menu stays in the edition.
- **Honesty state:** with no lead endpoint configured, the form tells the visitor to phone instead of pretending the enquiry was sent. The note is ink; the error note is `{colors.<edition>-warn}` — a per-edition token, because a single red cannot clear AA on both a night ground and a paper one.

### Navigation (`.top`)
- **Style:** fixed, full-bleed, logo left and links right, History Pro caps at 0.2em tracking in dim ink.
- **States:** hover lifts to full text colour; `aria-current` is ink.
- **Stuck:** an IntersectionObserver on a 1px sentinel toggles `data-stuck`, which fades out the top scrim and brings in an 88% ground backing with a 14px blur and a hairline bottom border. The scrim exists because over a photograph the header is otherwise illegible; on the paper edition the scrim is a solid paper band instead of a fade.

### Cartouche (`.cartouche`) and Legend (`.legend`)
- **Cartouche:** the chart's title block — 1px border with a 3px top edge, 72% ground backing, 6px blur, a History Pro label, then a definition list of measurements.
- **Legend:** a 1px-gapped stack over a `--line` ground; a head with the scale statement, then one row per landmark — ink dot (solid = delivered, hollow ring = under construction), Anglecia name, dim meta. Each row is a link, and hovering it wakes the matching mark on the coastline.

### Soundings scale bar (`.soundings` / `.sounding`)
The system's answer to a stats section, and the one to copy rather than reinventing. A single row sits under one full-width ink rule; each figure hangs from its own 1px tick, with the number in Anglecia ink and the unit beneath in dim 15px. It is **not** a grid of metric cards — no boxes, no icons, no equal-height tiles. On ≤720px it becomes two columns and stays a scale bar.

### Floor-plate selector (`.plate`)
The signature component, and the most fragile. Rules that must survive any edit:
- **It never blanks.** On selection the new plan is loaded into a detached `Image()`; `src`/`srcset`/`alt`/`aspect-ratio` are swapped only in `onload`/`onerror`. The previous drawing stays on screen the whole time.
- **Loading is dimming, not emptying.** `data-loading` drops opacity to 0.45 for 320ms; the attribute is removed on swap.
- **Re-selecting the current plan returns early** (`if (img.getAttribute('src') === want) return;`) so a repeat click causes no flicker.
- **The default plan ships in the markup**, generated by `tools/build_plate_html.py`. With JS off the first plate is visible and captioned.
- **The drawing sits on paper.** The figure ground is `--paper` and the image is `mix-blend-mode: darken` — the white sheet of the scan disappears into the chart's paper while the linework stays.
- **It must fit the screen:** `max-height: 74svh` with `object-fit: contain`. A plan that requires scrolling is broken.
- Tabs are two 1px-gapped rows (section, then level); the selected tab is ink on `--on-ink` and carries `aria-pressed="true"`.

### Bars (`.wall__bar`, `.bar__fill`)
Quantities are drawn to scale and animate by `transform: scaleX()` from a left origin — never by animating `width`. Wall thickness is scaled against a 640mm maximum, readiness against 100%. The total row is heavier: 5px track, Anglecia in ink.

### Gallery and lightbox
4-column 1px-gapped grid (2 at 1000px, 1 at 720px) with a `--wide` cell spanning two; images rest at `saturate(0.82–0.88)` and come to full saturation with a 1.035–1.05 scale on hover. The lightbox is built in JS, closes on backdrop / button / Escape, locks the document scroll, and returns focus to the opener.

### Browser surfaces
Selection, focus ring, and scrollbar are themed per edition (`::selection` ink on `--on-ink`; `scrollbar-color: var(--ink) var(--ground-2)`; an 11px webkit thumb in ink with a 3px ground-2 border). The chrome the browser draws belongs to the chart too — new pages must not leave it default.

### Motion
`.plot` (opacity + 1.4rem rise, 700/900ms, delays 90/180/270ms) and `.draw` (`stroke-dashoffset` from the path's own measured length, 1600–2600ms) are the only two motion primitives; both use `--ease: cubic-bezier(0.16, 1, 0.3, 1)`. The `prefers-reduced-motion` block resolves `.plot` to its rest state, `.draw` to a completed line, and clamps all animation and transition durations to 0.01ms; the JS checks the same media query and marks everything plotted immediately.

**The Plotted-Not-Faded Rule.** Things arrive by being drawn: a line along its length, a bar from its origin, a section settling into place. Nothing pops, scales in from 0.9, slides in from the side, or parallaxes. Every motion has a reduced-motion null state, and the page must be complete and legible without any of it.

## Assets as design material

The chart's geometry is generated, and the generators in `tools/` are part of the system:
- `build_map.py` builds `assets/map/coast.svg` from an Overpass extract of the real coastline and boulevard plus Nominatim coordinates, on a frame with equal scale on both axes so the range rings state true distances. The coastline is a claim about the place, so it is never drawn by hand.
- `build_plans.py` extracts floor plates from the client's booklets losslessly at 1200/2400px WebP; 2400 is the zoom size.
- `build_images.py` crops to a fixed aspect with a stated focal point and emits multi-width WebP; every shipping raster is registered in `assets/img/manifest.json` with its provenance.
- `build_plate_html.py` + `inline_partials.py` write the shared logo, coast and form blocks into the pages once, so the site stays buildless and the HTML stays directly editable.
- `build_video.sh` makes the 29Б hero loop by concatenating a 2.28s clip with its own reverse — a seamless loop with no cut.

**The Generated Geometry Rule.** If a shape encodes a fact — a coast, a plan, a wall thickness, a distance ring — it is produced by a tool from a source, not illustrated. Re-run the tool; do not nudge the path.

## Do's and Don'ts

### Do:
- **Do** add a new edition as a `[data-chart='name']` block of the same token names, and switch it on `<html>`. Never fork the stylesheet.
- **Do** run every text colour against its ground before shipping: 4.5:1 minimum. The measured set is 5.26 / 8.85 / 5.24 for the three inks on their primary grounds and 7.20 / 5.10 / 6.54 for the dim tokens. `tools/check_contrast.py` walks all 31 pairs and exits non-zero on any failure — run it after touching a colour.
- **Do** keep `--paper` (#ECE6DB) and the fb29 `--ground` (#F1EDE5) as separate tokens — insert stock and daylight stock are different materials.
- **Do** set every measurement as a sounding: tick, Anglecia figure in ink, dim unit beneath.
- **Do** animate quantity with `transform: scaleX()` from a left origin.
- **Do** ship the default state in markup — the first floor plate, the poster frame, the full nav — so the page works with JS off.
- **Do** theme selection, focus ring and scrollbar for any new edition.
- **Do** cap running text at `68ch` and keep body at 17px / labels at 12px caps.

### Don't:
- **Don't** put a drop shadow on anything. Separate by tone, hairline, or blurred ground-tinted backing.
- **Don't** round a corner. Radius is 0 except for a literal dot.
- **Don't** set body copy, sentence-case headings or any lowercase text in History Pro — it is a caps-only face and its lowercase renders as small caps.
- **Don't** set text in `--ink-pure`. Those hexes measure 3.61:1 and 2.49:1 on their grounds and are for fields and the logo only.
- **Don't** put an eyebrow, kicker or label line above a heading. Labels title chart blocks, not headings.
- **Don't** build a stats section as a grid of metric cards; it is a scale bar.
- **Don't** let the floor-plate view go empty between selections, and don't animate a plan swap with anything but the 320ms opacity dim.
- **Don't** hardcode an edition colour inside a component; read `--ink` / `--ground` / `--text` / `--line`.
- **Don't** hand-draw geometry that encodes a fact — regenerate it from `tools/`.
- **Don't** replace Montserrat because a detector calls it over-used. It is the client's licensed brand face, subset and self-hosted.

### Contrast defects found at documentation time — both closed
Recording them because the fix is part of the system, not because they still bite:

- The form's error note was a hardcoded `#E4673E`, measuring 2.56:1 on the ФБ29 paper ground. It became a per-edition `--warn` token: `#E4673E` on the two night editions (5.05 and 5.27 on `--ground-2`), `#A8330E` on paper (5.72 / 5.13). A single red cannot serve both.
- `--ink` measured 4.38:1 on `--ground-2` in the 29Б edition, so the ink-coloured figures in the soundings and enquiry bands sat under AA. The rust was lifted from `#C4652E` to `#CC6E35`, which clears both grounds.

The lesson is written into `tools/check_contrast.py`: a token must be set by the worst ground it will ever sit on, and the check must run on every colour change.
