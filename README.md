# Spring Cleaning Free Pack

A free printable pack for cheerful seasonal cleaning: warm getting-started notes,
room-by-room walk-through lists, one-hour zone timers, a declutter decision card,
a freecycle-and-donate drop log, deep-clean vs daily-done checkboxes, a windows-and-
wet-weather cheat sheet, and a big-ticket refresh wish list.

Plain HTML/CSS sheets print to PDF with one local build script. No accounts, no
tracking, no network calls, no secrets.

## What's inside

| File | PDF output |
|------|------------|
| `sources/00-getting-started.html` | `printables/00-getting-started.pdf` — warm intro + how to use the pack |
| `sources/01-room-walkthroughs.html` | `printables/01-room-walkthroughs.pdf` — room-by-room walk-through lists |
| `sources/02-zone-timers.html` | `printables/02-zone-timers.pdf` — one-hour zone timers + zone log |
| `sources/03-declutter-decision-card.html` | `printables/03-declutter-decision-card.pdf` — declutter decision card |
| `sources/04-drop-log.html` | `printables/04-drop-log.pdf` — freecycle & donate drop log |
| `sources/05-deep-vs-daily.html` | `printables/05-deep-vs-daily.pdf` — deep-clean vs daily-done checkboxes |
| `sources/06-windows-wet-weather.html` | `printables/06-windows-wet-weather.pdf` — windows & wet-weather cheat sheet |
| `sources/07-big-ticket-wishlist.html` | `printables/07-big-ticket-wishlist.pdf` — big-ticket refresh wish list |

## Requirements

- Python 3.10+
- [WeasyPrint](https://weasyprint.org/) (`pip install weasyprint`)
- [pypdf](https://pypdf.readthedocs.io/) (`pip install pypdf`) — used by the tests
- [pytest](https://pytest.org) (`pip install pytest`) — for the test suite

## Build

```bash
python3 build.py              # renders all sheets into printables/
python3 build.py --out /tmp/x # build elsewhere
python3 build.py --strict     # treat layout warnings as errors
```

Everything runs locally. The build never accesses the network.

## Test

```bash
pytest -v                     # verifies every sheet builds a valid PDF
# or, with no pytest installed:
python3 -m unittest discover -s tests -t . -v
```

## Design notes

- All sheets target US Letter (612×792 pt); on A4 printers choose "fit to page".
- Low-ink palette by design: cream boxes, coral/teal accents, hairline rules.
- Sheets are intentionally unbranded on the page itself; the pack is a free
  printable published by Asdale Dynamics, LLC (see README credit line and footer
  note on the getting-started sheet).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
