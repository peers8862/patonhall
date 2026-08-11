#!/usr/bin/env python3
"""Build the Paton Hall site from the markdown in docs/.

The markdown files are the source of record. This script renders them to
static HTML at the repository root, ready for GitHub Pages.

    python3 build.py

Outputs: index.html, papers/*.html
"""

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "docs"
OUT = ROOT / "papers"

# ---------------------------------------------------------------------------
# SIGNUP FORM  —  the one thing to configure in this file.
#
# Paste your Kit (formerly ConvertKit) form action URL between the quotes.
# Find it in Kit:  Grow -> Landing Pages & Forms -> your form -> Embed -> HTML.
# It looks like:   https://app.kit.com/forms/1234567/subscriptions
#
# Two things to set up inside Kit first:
#   1. A custom field with the key  interest   (Subscribers -> custom fields),
#      so the "what brings you here" answer is stored against each subscriber.
#   2. A redirect back to this site after signup, so people are not left on a
#      Kit page  (form Settings -> after signup -> redirect to a URL).
#
# Until this is filled in, the page shows a plain email link instead, so the
# site is never broken and never shows a dead form.
# ---------------------------------------------------------------------------
SIGNUP_ACTION = ""
SIGNUP_EMAIL = "morgenpeers@outlook.com"   # fallback + fine-print contact

INTERESTS = [
    "Build nights",
    "Learning days and talks",
    "Certified electronics training",
    "Founding membership",
    "Just keeping an eye on it",
]


def signup_block() -> str:
    """The founding-member signup. Falls back to a mail link if unconfigured."""
    intro = (
        '<p class="eyebrow">Founding members</p>\n'
        "<p>The first twenty-five get a founding rate and a say in how the room "
        "runs. We open within sixty days.</p>\n"
    )

    if not SIGNUP_ACTION:
        return (
            f'<div class="signup">\n{intro}'
            f'<p style="font-family:var(--sans);font-size:0.97rem">'
            f'Email <a class="plain" href="mailto:{SIGNUP_EMAIL}'
            f'?subject=Paton%20Hall%20founding%20member">{SIGNUP_EMAIL}</a> '
            f"with your name and what brings you here, and we will put you on "
            f"the list.</p>\n</div>"
        )

    opts = "\n".join(
        f'          <option value="{html.escape(i)}">{html.escape(i)}</option>'
        for i in INTERESTS
    )
    return f"""<div class="signup">
{intro}<form class="signup-form" action="{html.escape(SIGNUP_ACTION)}" method="post">
      <div>
        <label for="su-name">Name</label>
        <input id="su-name" type="text" name="fields[first_name]"
               autocomplete="given-name" required>
      </div>
      <div>
        <label for="su-email">Email</label>
        <input id="su-email" type="email" name="email_address"
               autocomplete="email" required>
      </div>
      <div class="full">
        <label for="su-interest">What brings you here</label>
        <select id="su-interest" name="fields[interest]">
{opts}
        </select>
      </div>
      <div class="full">
        <button type="submit">Put me on the list</button>
      </div>
    </form>
    <p class="fineprint">We will email you about Paton Hall and nothing else.
    Unsubscribe in one click, any time. No sharing, no selling, no third
    parties. Questions: <a href="mailto:{SIGNUP_EMAIL}">{SIGNUP_EMAIL}</a>.</p>
</div>"""

# Ordered. Drives both the nav and the index listing.
DOCS = [
    {
        "src": "14-onepager-blended.md",
        "slug": "overview",
        "nav": "Overview",
        "title": "Overview",
        "ref": "One page",
        "name": "The whole thing, in two pages",
        "desc": "The moment, the gap in Hamilton, what the Hall is, the model, "
                "the numbers, and what we are honest about. Start here.",
    },
    {
        "src": "10-onepager-members.md",
        "slug": "members",
        "nav": "Members",
        "title": "For members",
        "ref": "One page",
        "name": "For founders and members",
        "desc": "What membership actually buys, the three tiers, and why it is "
                "not a desk.",
    },
    {
        "src": "12-onepager-industry.md",
        "slug": "industry",
        "nav": "Industry",
        "title": "For industry",
        "ref": "One page",
        "name": "For plant managers and HR",
        "desc": "Certified electronics training in Hamilton — and the Ontario "
                "grant money most employers are not claiming.",
    },
    {
        "src": "11-onepager-partners.md",
        "slug": "partners",
        "nav": "Partners",
        "title": "For partners",
        "ref": "One page",
        "name": "For colleges, the university and the City",
        "desc": "A delivery partner for work your mandate already names — "
                "including one short-term action the City has not started.",
    },
    {
        "src": "13-onepager-civic.md",
        "slug": "civic",
        "nav": "The tenancy",
        "title": "The tenancy",
        "ref": "One page",
        "name": "For the landlord, the City and insurers",
        "desc": "A plain account of the premises, the use, occupancy and code, "
                "insurance, and who runs it.",
    },
    {
        "src": "01-financials.md",
        "slug": "financials",
        "nav": "Numbers",
        "title": "The numbers",
        "ref": "Model",
        "name": "The financial model",
        "desc": "Cost base, break-even at 51 members, the path to paid staff, "
                "twelve-month scenarios, and the assumptions most likely to be wrong.",
    },
    {
        "src": "00-repository.md",
        "slug": "repository",
        "nav": "Repository",
        "title": "Repository",
        "ref": "Full",
        "name": "The repository and claims register",
        "desc": "Everything, in point form, with a status label on every claim — "
                "including the ones we have withdrawn.",
    },
]

MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"]
)


def nav(prefix: str, current: str | None) -> str:
    items = []
    for d in DOCS:
        cur = ' aria-current="page"' if d["slug"] == current else ""
        items.append(
            f'<li><a href="{prefix}papers/{d["slug"]}.html"{cur}>'
            f'{html.escape(d["nav"])}</a></li>'
        )
    return (
        '<nav class="site-nav" aria-label="Documents"><ul>'
        + "".join(items)
        + "</ul></nav>"
    )


def shell(prefix: str, current: str | None, title: str, desc: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Paton Hall</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{prefix}styles.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22><rect width=%2216%22 height=%2216%22 fill=%22%2316212c%22/><text y=%2212%22 x=%228%22 text-anchor=%22middle%22 font-size=%2211%22 font-family=%22Georgia,serif%22 fill=%22%23f8efd6%22>P</text></svg>">
</head>
<body>
<header class="site-header">
  <div class="header-bar">
    <a class="sign" href="{prefix}index.html">Paton Hall</a>
  </div>
  {nav(prefix, current)}
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <a class="sign" href="{prefix}index.html">Paton Hall</a>
    <p>4 Breadalbane Street, Hamilton, Ontario &mdash; the preferred site. A
    former mechanics garage, in that use since about 1927, one lot back from
    King Street West. Other Hamilton properties are being actively scouted;
    the Hall is a model rather than a building.</p>
    <p>These are working documents and planning records, not commitments.
    Figures are planning models, not audited forecasts. Every load-bearing
    claim carries a status label in the
    <a href="{prefix}papers/repository.html">repository</a>, including the
    claims we have withdrawn.</p>
  </div>
</footer>
</body>
</html>
"""


def render(md_text: str) -> str:
    MD.reset()
    out = MD.convert(md_text)
    # Tables scroll inside their own box so the page body never scrolls sideways.
    out = re.sub(r"<table>", '<div class="table-scroll"><table>', out)
    out = re.sub(r"</table>", "</table></div>", out)
    # The leading status block becomes a marked note.
    out = re.sub(
        r"<p>(<strong>Status:</strong>.*?)</p>",
        r'<p class="meta">\1</p>',
        out,
        count=1,
        flags=re.S,
    )
    return out


def build_papers() -> None:
    OUT.mkdir(exist_ok=True)
    for d in DOCS:
        text = (SRC / d["src"]).read_text(encoding="utf-8")
        body = (
            '<article class="paper"><div class="wrap">\n'
            + render(text)
            + f'\n<hr>\n<p class="backlink"><a href="../index.html">'
            f"&larr; All documents</a></p>\n</div></article>"
        )
        page = shell("../", d["slug"], d["title"], d["desc"], body)
        (OUT / f'{d["slug"]}.html').write_text(page, encoding="utf-8")
        print(f'  papers/{d["slug"]}.html  <-  docs/{d["src"]}')


def doc_list() -> str:
    rows = []
    for d in DOCS:
        rows.append(
            f'    <li><a href="papers/{d["slug"]}.html">'
            f'<span class="ref">{html.escape(d["ref"])}</span>'
            f'<span class="name">{html.escape(d["name"])}</span>'
            f'<p class="desc">{html.escape(d["desc"])}</p></a></li>'
        )
    return '<ul class="docs">\n' + "\n".join(rows) + "\n  </ul>"


INDEX_BODY = """
<section class="hero">
  <figure>
    <img src="assets/img/front.jpg" alt="The front of Paton Hall: a single-storey
      rock-faced concrete block building with an open garage bay and a dark navy
      sign reading Paton Hall." width="1800" height="1361">
  </figure>
  <div class="wrap hero-text">
    <h1 class="title">Paton&nbsp;Hall</h1>
    <p class="address">Breadalbane Street &middot; Hamilton, Ontario</p>
    <p class="standfirst">A hundred-year-old garage, run as an open room for
      the people rebuilding North American industry.</p>
    <div class="prose">
      <p>A mechanics shop from about 1927 until now, and we are keeping it that
      way. Concrete floor, garage height, a bay door you can drive through.
      Benches for hardware and prototyping, boards along the wall opposite, and a
      pool table at the back that converts to another work surface. Anyone can
      join.</p>
    </div>
    <dl class="facts">
      <div><dt>In mechanical use since</dt><dd>1927</dd></div>
      <div><dt>Floor area</dt><dd>2,000 <span>sq ft</span></dd></div>
      <div><dt>Operating cost</dt><dd>$4,500 <span>/mo</span></dd></div>
      <div><dt>Members to cover it</dt><dd>51</dd></div>
    </dl>
    %(signup)s
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">The room</p>
    <div class="pair">
      <figure>
        <img src="assets/img/room-a.jpg" alt="The interior: a long open concrete
          floor, black-painted ceiling with exposed joists and fluorescent strip
          lights, painted block walls." width="1100" height="1240">
        <figcaption>Concrete floor, black ceiling, strip light. The whole room.</figcaption>
      </figure>
      <figure>
        <img src="assets/img/room-b.jpg" alt="The interior looking toward an open
          garage bay with daylight and trees beyond." width="1100" height="1240">
        <figcaption>The bay door open onto the yard.</figcaption>
      </figure>
    </div>
    <div class="prose">
      <p>On <strong>build nights</strong> the floor is given over to physical
      work &mdash; wrenching, robotics, assembly, test. Members bring their own
      tools; the Hall brings the floor, the power, the benches and the hours. The
      bay door means a robot, a rig or a pallet comes straight in, which most
      rooms in this city cannot offer.</p>
      <p>The rest of the week: open nights with the pool table running, learning
      days in engineering, physics and manufacturing practice, demos where
      members show what they built, and &mdash; once it is signed rather than
      discussed &mdash; certified electronics training.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">The documents</p>
    <div class="prose">
      <p>Written for four different readers. Take the one that fits, or read the
      overview and decide.</p>
    </div>
  </div>
  <div class="wrap">
  %(docs)s
  </div>
</section>

<section>
  <div class="wrap">
    <figure>
      <img src="assets/img/side.jpg" alt="The long side of the building in
        painted concrete block, with tall steel-frame industrial windows and a
        gravel drive." width="1800" height="1395">
      <figcaption>Steel-frame windows on the long wall. NO PARKING, hand-painted.</figcaption>
    </figure>
    <div class="prose">
      <p>The lease is one year, on a building that carries a redevelopment
      proposal, which is why the rent works. <strong>The Hall is a model rather
      than a building</strong> &mdash; this is the site we want, and other
      Hamilton properties are being actively scouted. Everything we buy comes
      apart and travels, so a change of address costs us furniture and not a
      membership.</p>
      <p>Every claim we make carries a status label &mdash; safe to use, needs
      validation, or rejected &mdash; and the rejected ones stay visible.
      Anyone can publish their wins.</p>
    </div>
  </div>
</section>
"""


def build_index() -> None:
    body = INDEX_BODY % {"docs": doc_list(), "signup": signup_block()}
    page = shell(
        "",
        None,
        "A garage in Hamilton",
        "Paton Hall — a hundred-year-old mechanics garage at 4 Breadalbane "
        "Street, Hamilton, run as an open room for technologists, engineers "
        "and founders building industrial products.",
        body,
    )
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("  index.html")


if __name__ == "__main__":
    print("Building Paton Hall site:")
    build_papers()
    build_index()
    print("Done.")
