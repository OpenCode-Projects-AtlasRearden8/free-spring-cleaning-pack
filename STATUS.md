# STATUS.md — Spring Cleaning Free Pack

Date: 2026-10-27

## What was built

A free, unbranded printable pack for cheerful seasonal cleaning, authored in
plain HTML/CSS and rendered to PDF by a single local build script:

1. **Getting Started** (`00-getting-started`) — warm, no-pressure intro:
   what's in the pack, how to start gently, and printing notes.
2. **Room-by-Room Walk-Throughs** (`01-room-walkthroughs`) — one universal
   "first lap" list plus extras for bedroom, living room, kitchen, bathroom,
   entry/hallway, and office/desk.
3. **One-Hour Zone Timers** (`02-zone-timers`) — an hour split into five
   stretches with a built-in 5-minute sit-down break, a half-hour
   low-energy variant, and a zone log table.
4. **Declutter Decision Card** (`03-declutter-decision-card`) — a
   numbered decision flow for stuck items, a sell/donate split, maybe-bin
   rules, and an exit ladder for batch decisions.
5. **Freecycle & Donate Drop Log** (`04-drop-log`) — per-bag drop log,
   method cheat sheet (charity, freecycle/Buy Nothing, pickups, specialty),
   bag go-line checklist, and a running total.
6. **Deep-Clean vs. Daily-Done** (`05-deep-vs-daily`) — coral-coded
   once-a-season deep-clean grid vs. teal-coded daily helpers, with a
   daily-done log.
7. **Windows & Wet-Weather Cheat Sheet** (`06-windows-wet-weather`) — cheap
   streak-free glass mix, cloud-day method, rainy-day indoor job list, and
   a Q&A table.
8. **Big-Ticket Refresh Wish List** (`07-big-ticket-wishlist`) — wish table,
   three-pass prioritization, 30-day hold rule, and a replace-or-repair
   quick check.

All sheets: US Letter, low-ink warm design (cream/coral/teal), shared
stylesheet `sources/pack.css` with page footers (sheet title + page numbers),
checkboxes and tables sized for handwriting.

## How to run it

Requirements: Python 3.10+, `weasyprint`, `pypdf`, `pytest` (optional).

```bash
python3 build.py               # builds all 8 PDFs into printables/
python3 build.py --strict      # also fail on layout/CSS warnings
pytest -v                      # or: python3 -m unittest discover -s tests -t .
```

Fully local: no network, accounts, secrets, or personal data. Source HTML
lives in `sources/`; finished unbranded PDFs land in `printables/`.

## Verification results

- `python3 build.py` — builds all 8 sheets, zero warnings (also verified
  with `--strict`).
- `pytest -v` — **5 passed, 8 subtests passed**, covering:
  - the expected sheet set exists in `sources/`
  - the build produces one PDF per sheet into a fresh temp dir
  - every PDF has a valid `%PDF-` header, parses with pypdf, and is
    US Letter sized (612×792 pt ±2)
  - every PDF has extractable text on its pages
  - the committed `printables/` PDFs match a fresh build of the current
    sources (page counts equal).
- `python3 -m unittest discover -s tests -t .` — **5 tests, OK** (same
  suite, runs without pytest).
- Visual inspection: rendered every sheet to PNG via `pdftoppm`; found and
  fixed two real layout bugs during that pass (see Known gaps / fixes).
- Repo hygiene: no Chinese/typo artifacts, no key/token patterns in any file.

## Known gaps / notes

- Page count per sheet is 2; several final pages are sparse (e.g. the zone
  log spills slightly onto page 2 of the timer sheet). Fine for a filler
  page, could be tightened.
- A4 users must choose "fit to page"; sheets target US Letter only.
- Fonts: uses DejaVu Sans (present on most Linux distros); on systems
  without it, WeasyPrint falls back to the default sans font.
- No build of a combined single-file pack (all sheets in one PDF); easy
  follow-up if wanted.

## Layout bug fixes made during verification (detail)

- `sources/pack.css`: `.grid-check li` float layout → `inline-block`
  (floats inside the flex wrapper broke WeasyPrint's float containment).
- Item width 31% + margin 2.5% → 29% + 2.5% (3 items per row now).
