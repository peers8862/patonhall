# Paton Hall

A hundred-year-old mechanics garage in Hamilton, Ontario, run as an open room for
technologists, engineers and founders building industrial products.

This repository is the business case and its supporting documents, published as a
static site.

## Structure

- `docs/` — the markdown documents, which are the **source of record**
- `papers/` — generated HTML, one page per document
- `index.html`, `styles.css`, `assets/` — the site
- `build.py` — regenerates `papers/` and `index.html` from `docs/`

## Building

```
python3 build.py
```

Requires `markdown` (`pip install markdown`). Edit the markdown in `docs/`, run the
build, and the site follows. Do not hand-edit files in `papers/` — they are
overwritten.

## The documents

| Page | For |
|---|---|
| Overview | Everyone. Start here. |
| Members | Founders and prospective members |
| Industry | Plant managers and HR |
| Partners | Colleges, the university, the City |
| The tenancy | Landlord, City, insurers |
| Numbers | The financial model |
| Repository | Everything, plus the claims register |

## A note on the claims register

Every load-bearing claim in these documents carries an ID and a status — **Safe to
Use**, **Needs Validation**, or **Rejected**. The rejected and withdrawn claims stay
visible in `docs/00-repository.md` §13. Corrections are published, not buried.

These are working documents and planning records, not commitments. Figures are
planning models, not audited forecasts.
