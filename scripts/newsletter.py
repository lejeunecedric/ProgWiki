#!/usr/bin/env python3
"""Weekly newsletter generator — 70s music-press style.

Builds content/newsletters/YYMMDD-<WIKINAME>-newsletter.md for the current
ISO week (Mon-Sun) from wiki frontmatter and page prose:

  * NEW RELEASES  — albums whose `released:` date falls in this week (any
                    year), written up as week-of news from the album pages
  * SPECIAL       — rotating feature on one concept / label / manufacturer /
                    query page (rotates by ISO week number)
  * ANNIVERSARIES — artists whose `born:`/`died:` falls in this week; falls
                    back to the nearest upcoming birthday
  * BACK PAGES    — recently updated pages, newly ingested references,
                    queries on file (the notice board)

Usage: WIKINAME=ProgWiki REPO=ProgWiki python3 scripts/newsletter.py
Run from the repo root. Never invents dates — only frontmatter dates are used.
"""
import os
import re
import datetime as dt

WIKINAME = os.environ.get("WIKINAME", "WIKI")
REPO = os.environ.get("REPO", os.path.basename(os.getcwd()))
TODAY = dt.date.today()
MONDAY = TODAY - dt.timedelta(days=TODAY.weekday())
SUNDAY = MONDAY + dt.timedelta(days=6)
WEEK_IDX = TODAY.isocalendar()[1]

WEEKS_BACK_UPDATED = 7
RECENT_LIMIT = 10
REF_LIMIT = 10
FALLBACK_DAYS = 45  # how far ahead to look for early cards / calendar preview

FM = re.compile(r"^---\n(.*?)\n---", re.S)
FULL_DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def parse_frontmatter(path):
    try:
        with open(path, encoding="utf-8") as f:
            m = FM.match(f.read())
        if not m:
            return {}
        fm = {}
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip("'\"")
        return fm
    except OSError:
        return {}


def page_body(path, max_chars=700):
    """Readable prose from a wiki page (frontmatter + markup stripped)."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return ""
    m = FM.match(text)
    if m:
        text = text[m.end():]
    text = re.sub(r"\^\[.*?\]", "", text)                        # provenance
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)   # [[a|b]]
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)              # [[a]]
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)         # [t](u)
    text = re.sub(r"^#+ .*$", "", text, flags=re.M)              # headings
    text = re.sub(r"^> .*$", "", text, flags=re.M)               # blockquotes
    text = re.sub(r"^[-*] .*$", "", text, flags=re.M)            # bullets
    paras = [re.sub(r"\s+", " ", p).strip()
             for p in re.split(r"\n\s*\n", text)]
    paras = [p for p in paras if len(p) > 40]
    out = " ".join(paras)
    if not out:
        return ""
    return out[:max_chars].rsplit(".", 1)[0].strip() + "."


def first_sentences(text, n=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:n])


def collect():
    pages = []
    for d in ("entities", "concepts", "comparisons", "queries"):
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.endswith(".md"):
                    p = os.path.join(root, fn)
                    fm = parse_frontmatter(p)
                    fm["_path"] = p
                    fm["_slug"] = fn[:-3]
                    fm["_title"] = fm.get("title", fn[:-3])
                    pages.append(fm)
    return pages


def md_in_week(mo, d):
    """(month, day) anniversary falls in this week — Dec->Jan wrap safe."""
    try:
        md = dt.date(2000, mo, d)
    except ValueError:
        return False
    wm = dt.date(2000, MONDAY.month, MONDAY.day)
    ws = dt.date(2000, SUNDAY.month, SUNDAY.day)
    if SUNDAY.month < MONDAY.month:  # e.g. Dec 29 -> Jan 4
        return md >= wm or md <= ws
    return wm <= md <= ws


def days_away(mo, d):
    """Days until the next occurrence of (mo, d), >= 0."""
    try:
        nxt = dt.date(TODAY.year, mo, d)
    except ValueError:
        nxt = dt.date(TODAY.year, 3, 1)  # Feb 29
    if nxt < TODAY:
        try:
            nxt = dt.date(TODAY.year + 1, mo, d)
        except ValueError:
            nxt = dt.date(TODAY.year + 1, 3, 1)
    return (nxt - TODAY).days


def album_pages(pages):
    return [fm for fm in pages if "/albums/" in fm["_path"]]


def artist_pages(pages):
    return [fm for fm in pages
            if any(k in fm["_path"] for k in ("/musicians/", "/players/", "/people/"))]


def feature_candidates(pages):
    return [fm for fm in pages
            if fm["_path"].startswith("concepts/")
            or "/labels/" in fm["_path"]
            or "/manufacturers/" in fm["_path"]
            or fm["_path"].startswith("queries/")]


def feature_kind(fm):
    if fm["_path"].startswith("concepts/"):
        return "concept"
    if fm["_path"].startswith("queries/"):
        return "query"
    if "/labels/" in fm["_path"]:
        return "label"
    return "manufacturer"


# ------------------------------------------------------------------ sections

def section_new_releases(pages):
    """Albums released this week (any year) — the news desk."""
    rows = []
    for fm in album_pages(pages):
        m = FULL_DATE.match(fm.get("released", ""))
        if not m:
            continue
        y, mo, d = map(int, m.groups())
        if md_in_week(mo, d):
            rows.append((fm, y, mo, d))
    rows.sort(key=lambda r: (r[2], r[3]))

    L = ["## New releases this week\n"]
    if rows:
        L.append("The rack is full this week. Long-players that hit the "
                 "shops in this very week of history:\n")
        for fm, y, mo, d in rows:
            age = TODAY.year - y
            prose = (first_sentences(page_body(fm["_path"], 500))
                     or "A record that helped write the rulebook.")
            month = dt.date(2000, mo, d).strftime("%B") + f" {d}"
            L.append(f"### {fm['_title']} ({y})\n")
            L.append(f"**{month}, {y}** — {age} years ago this week: {prose} "
                     f"Full story in [[{fm['_slug']}]].\n")
    else:
        L.append("No anniversary pressings fall inside this week's window — "
                 "the crates only yield a story when an album page carries a "
                 "full `released: YYYY-MM-DD` in its frontmatter.\n")
        near = []
        for fm in album_pages(pages):
            m = FULL_DATE.match(fm.get("released", ""))
            if m:
                y, mo, d = map(int, m.groups())
                near.append((days_away(mo, d), fm, y))
        near.sort(key=lambda r: r[0])
        if near:
            L.append("**Coming up on the calendar** (dates from the wiki):\n")
            for days, fm, y in near[:3]:
                when = TODAY + dt.timedelta(days=days)
                L.append(f"- **{fm['_title']}** ({y}) — the needle drops in "
                         f"{days} day{'s' if days != 1 else ''} "
                         f"({when.isoformat()}), [[{fm['_slug']}]]")
            L.append("")
    return L


def section_special(pages):
    cands = feature_candidates(pages)
    L = ["## Special\n"]
    if not cands:
        L.append("_No concept, label, manufacturer or query pages on file yet._\n")
        return L
    fm = cands[WEEK_IDX % len(cands)]
    prose = page_body(fm["_path"], 800)
    L.append(f"**This issue's special: {fm['_title']}** ({feature_kind(fm)})\n")
    if prose:
        L.append(prose + "\n")
    L.append(f"Dig deeper in [[{fm['_slug']}]].\n")
    return L


def section_birthdays(pages):
    L = ["## Anniversaries\n"]
    births, deaths = [], []
    for fm in artist_pages(pages):
        m = FULL_DATE.match(fm.get("born", ""))
        if m and md_in_week(int(m.group(2)), int(m.group(3))):
            births.append((fm, int(m.group(1))))
        m = FULL_DATE.match(fm.get("died", ""))
        if m and md_in_week(int(m.group(2)), int(m.group(3))):
            deaths.append((fm, int(m.group(1))))
    if births or deaths:
        for fm, y in births:
            age = TODAY.year - y
            prose = first_sentences(page_body(fm["_path"], 500))
            L.append(f"### Many happy returns, {fm['_title']}\n")
            L.append(f"Born {y} — turning **{age}** this week. {prose}\n")
        for fm, y in deaths:
            prose = first_sentences(page_body(fm["_path"], 500))
            L.append(f"### Raising a glass: {fm['_title']}\n")
            L.append(f"Left us in {y}, {TODAY.year - y} years ago this week. {prose}\n")
    else:
        near = []
        for fm in artist_pages(pages):
            m = FULL_DATE.match(fm.get("born", ""))
            if m:
                y, mo, d = map(int, m.groups())
                near.append((days_away(mo, d), fm, y))
        near.sort(key=lambda r: r[0])
        if near and near[0][0] <= FALLBACK_DAYS:
            days, fm, y = near[0]
            age = TODAY.year - y + 1
            prose = first_sentences(page_body(fm["_path"], 500))
            L.append("No birthdays inside this week's window, so the cards "
                     "go out early:\n")
            L.append(f"### {fm['_title']} ({y})\n")
            L.append(f"The candles come out in {days} day"
                     f"{'s' if days != 1 else ''} — turning **{age}**. {prose}\n")
        else:
            L.append("_No artist pages with a full `born: YYYY-MM-DD` in "
                     "frontmatter yet — add dates and this column fills itself._\n")
    return L


def section_back_pages(pages):
    L = ["## Back pages\n"]
    cutoff = TODAY - dt.timedelta(days=WEEKS_BACK_UPDATED)
    upd = []
    for fm in pages:
        m = FULL_DATE.match(fm.get("updated", ""))
        if m and dt.date(*map(int, m.groups())) >= cutoff:
            upd.append((m.group(0), fm))
    upd.sort(key=lambda x: x[0], reverse=True)
    L.append("### Recent edits\n")
    if upd:
        for u, fm in upd[:RECENT_LIMIT]:
            L.append(f"- {u} — [[{fm['_slug']}]] — {fm['_title']}")
        if len(upd) > RECENT_LIMIT:
            L.append(f"- _…and {len(upd) - RECENT_LIMIT} more_")
    else:
        L.append("_No pages touched this week._")
    L.append("")

    L.append("### New in the reference room\n")
    raws = []
    for d in ("raw/articles", "raw/forums"):
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            fm = parse_frontmatter(os.path.join(d, fn))
            ing = fm.get("ingested", "")
            if FULL_DATE.match(ing) and dt.date(*map(int, ing.split("-"))) >= cutoff:
                raws.append((ing, fn[:-3], fm.get("source_url", "")))
    raws.sort(key=lambda x: x[0], reverse=True)
    if raws:
        for ing, name, url in raws[:REF_LIMIT]:
            L.append(f"- [{name}]({url})" if url else f"- {name}")
        if len(raws) > REF_LIMIT:
            L.append(f"\n_…and {len(raws) - REF_LIMIT} more (see `raw/`)._")
    else:
        L.append("_Nothing ingested this week._")
    L.append("")

    qs = sorted([fm for fm in pages if fm["_path"].startswith("queries/")],
                key=lambda x: x.get("updated", ""), reverse=True)
    if qs:
        L.append("### Queries on file\n")
        for fm in qs:
            L.append(f"- [[{fm['_slug']}]] — {fm['_title']} "
                     f"_(updated {fm.get('updated', '?')})_")
        L.append("")
    return L


def main():
    pages = collect()
    L = [f"# THE {REPO.upper()} DISPATCH\n",
         f"*Vol. {WEEK_IDX} — week of {MONDAY.isoformat()} to {SUNDAY.isoformat()}, "
         f"printed {TODAY.isoformat()} by `scripts/newsletter.py`*\n"]
    L += section_new_releases(pages)
    L += section_special(pages)
    L += section_birthdays(pages)
    L += section_back_pages(pages)

    os.makedirs("content/newsletters", exist_ok=True)
    out = os.path.join("content", "newsletters",
                       f"{TODAY.strftime('%y%m%d')}-{WIKINAME}-newsletter.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"wrote {out} ({len(L)} lines)")


if __name__ == "__main__":
    main()
