#!/usr/bin/env python3
"""Weekly newsletter generator — 70s music-press style.

Builds content/newsletters/YYMMDD-<WIKINAME>-newsletter.md for the current
ISO week (Mon-Sun) from wiki frontmatter and page prose:

  * NEW RELEASES  — records newly found this week in the references (album
                    pages updated this week), written up from the album pages
  * SPECIAL       — rotating feature on one concept / label / manufacturer /
                    query page (rotates by ISO week number)
  * ANNIVERSARIES — artists whose `born:`/`died:` falls in THIS week only

External-audience rules: no [[wikilinks]], no references to wiki internals
(frontmatter, raw/, scripts). Only current-week anniversaries are celebrated.
No wiki housekeeping sections (recent edits, queries on file) — this reads
like a music paper, not a changelog.

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
    """Records newly found this week (album pages updated this week)."""
    cutoff = TODAY - dt.timedelta(days=WEEKS_BACK_UPDATED)
    rows = []
    for fm in album_pages(pages):
        m = FULL_DATE.match(fm.get("updated", ""))
        if m and dt.date(*map(int, m.groups())) >= cutoff:
            rows.append((fm.get("updated", ""), fm))
    rows.sort(key=lambda r: r[0], reverse=True)

    L = ["## New releases this week\n"]
    if rows:
        L.append("Fresh finds in the record crates — long-players that joined "
                 "the collection this week:\n")
        for u, fm in rows[:RECENT_LIMIT]:
            prose = (first_sentences(page_body(fm["_path"], 500))
                     or "A record that helped write the rulebook.")
            L.append(f"### {fm['_title']}\n")
            L.append(f"{prose}\n")
        if len(rows) > RECENT_LIMIT:
            L.append(f"_…and {len(rows) - RECENT_LIMIT} more._\n")
    else:
        L.append("Nothing new in the crates this week — the dig continues.\n")
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
        L.append("_No birthdays or memorial dates fall inside this week's "
                 "window — the cards stay in the drawer until someone earns "
                 "one._\n")
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
            L.append(f"- {u} — {fm['_title']}")
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
            pretty = name.replace("-", " ")
            pretty = re.sub(r"^wikipedia ", "", pretty).strip().capitalize()
            L.append(f"- [{pretty}]({url})" if url else f"- {pretty}")
        if len(raws) > REF_LIMIT:
            L.append(f"\n_…and {len(raws) - REF_LIMIT} more._")
    else:
        L.append("_Nothing ingested this week._")
    L.append("")

    qs = sorted([fm for fm in pages if fm["_path"].startswith("queries/")],
                key=lambda x: x.get("updated", ""), reverse=True)
    if qs:
        L.append("### Queries on file\n")
        for fm in qs:
            L.append(f"- {fm['_title']} _(updated {fm.get('updated', '?')})_")
        L.append("")
    return L


def main():
    pages = collect()
    L = [f"# THE {REPO.upper()} DISPATCH\n",
         f"*Vol. {WEEK_IDX} — week of {MONDAY.isoformat()} to {SUNDAY.isoformat()}*\n"]
    L += section_new_releases(pages)
    L += section_special(pages)
    L += section_birthdays(pages)

    os.makedirs("content/newsletters", exist_ok=True)
    out = os.path.join("content", "newsletters",
                       f"{TODAY.strftime('%y%m%d')}-{WIKINAME}-newsletter.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"wrote {out} ({len(L)} lines)")


if __name__ == "__main__":
    main()
