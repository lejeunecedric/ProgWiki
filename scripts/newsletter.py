#!/usr/bin/env python3
"""Weekly newsletter generator.

Scans frontmatter (born:/died:/released:) and page metadata (updated:,
ingested:) to produce content/newsletters/YYMMDD-<WIKINAME>-newsletter.md
for the current ISO week (Mon-Sun).

Usage: python3 scripts/newsletter.py
Run from the repo root.
"""
import os
import re
import datetime as dt

WIKINAME = os.environ.get("WIKINAME", "WIKI")
REPO = os.environ.get("REPO", os.path.basename(os.getcwd()))
TODAY = dt.date.today()
MONDAY = TODAY - dt.timedelta(days=TODAY.weekday())
SUNDAY = MONDAY + dt.timedelta(days=6)

WEEKS_BACK_UPDATED = 7   # pages updated within N days go in "recently updated"
RECENT_LIMIT = 12

FM = re.compile(r"^---\n(.*?)\n---", re.S)


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


def collect():
    pages = []
    for d in ("entities", "concepts", "comparisons", "queries"):
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.endswith(".md"):
                    p = os.path.join(root, fn)
                    fm = parse_frontmatter(p)
                    fm["_path"] = p
                    slug = fn[:-3]
                    fm["_slug"] = slug
                    fm["_title"] = fm.get("title", slug)
                    pages.append(fm)
    return pages


def anniversaries(pages):
    """born/died/released full dates (YYYY-MM-DD) falling in this week."""
    births, deaths, releases = [], [], []
    for fm in pages:
        for key, bucket in (("born", births), ("died", deaths), ("released", releases)):
            v = fm.get(key, "")
            m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", v)
            if not m:
                continue
            y, mo, d = map(int, m.groups())
            try:
                md = dt.date(2000, mo, d)
            except ValueError:
                continue
            wm = dt.date(2000, MONDAY.month, MONDAY.day)
            ws = dt.date(2000, SUNDAY.month, SUNDAY.day)
            in_week = wm <= md <= ws
            if SUNDAY.month < MONDAY.month:  # Dec 29-31 -> Jan 1-4 week
                in_week = md >= wm or md <= ws
            if in_week:
                age = TODAY.year - y
                if age > 0:
                    bucket.append((fm, age, y, mo, d))
    return births, deaths, releases


def recent_updated(pages):
    out = []
    cutoff = TODAY - dt.timedelta(days=WEEKS_BACK_UPDATED)
    for fm in pages:
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", fm.get("updated", ""))
        if m and dt.date(*map(int, m.groups())) >= cutoff:
            out.append((fm, m.group(0)))
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def recent_raw():
    out = []
    for d in ("raw/articles", "raw/forums"):
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            fm = parse_frontmatter(os.path.join(d, fn))
            ing = fm.get("ingested", "")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", ing):
                out.append((fn[:-3], ing, fm.get("source_url", "")))
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def link(fm):
    return f"[[{fm['_slug']}]] — {fm['_title']}"


def main():
    pages = collect()
    births, deaths, releases = anniversaries(pages)
    updated = recent_updated(pages)[:RECENT_LIMIT]
    raws = [r for r in recent_raw()
            if dt.date(*map(int, r[1].split("-"))) >= TODAY - dt.timedelta(days=WEEKS_BACK_UPDATED)]
    shown, hidden = raws[:15], raws[15:]
    queries = [fm for fm in pages if fm["_path"].startswith("queries/")]

    L = []
    L.append(f"# {REPO} weekly newsletter — week of {MONDAY.isoformat()}\n")
    L.append(f"_Generated {TODAY.isoformat()} from wiki frontmatter by `scripts/newsletter.py`._\n")

    L.append("## This week's anniversaries\n")
    if births or deaths or releases:
        for fm, age, y, mo, d in births:
            L.append(f"- **{mo:02d}-{d:02d}** — Birthday: {link(fm)} (born {y}, turns {age})")
        for fm, age, y, mo, d in deaths:
            L.append(f"- **{mo:02d}-{d:02d}** — Memorial: {link(fm)} (died {y}, {age} years ago)")
        for fm, age, y, mo, d in releases:
            L.append(f"- **{mo:02d}-{d:02d}** — Release anniversary: {link(fm)} ({y}, {age} years ago)")
    else:
        L.append("_No birthdays or release anniversaries fall in this week's window. "
                 "Pages only become eligible when frontmatter carries full dates "
                 "(`born: YYYY-MM-DD`, `released: YYYY-MM-DD`) — year-only dates can't be celebrated._")
    L.append("")

    L.append("## Recently updated pages\n")
    if updated:
        for fm, u in updated:
            L.append(f"- {u} — {link(fm)}")
    else:
        L.append("_No pages updated in the last %d days._" % WEEKS_BACK_UPDATED)
    L.append("")

    L.append("## Newly ingested references\n")
    if raws:
        for name, ing, url in shown:
            L.append(f"- {ing} — [{name}]({url})" if url else f"- {ing} — {name}")
        if hidden:
            L.append(f"\n_…and {len(hidden)} more ingested this week (see `raw/`)._")
    else:
        L.append("_No new raw sources ingested this week._")
    L.append("")

    L.append("## Queries on file\n")
    for fm in sorted(queries, key=lambda x: x.get("updated", ""), reverse=True):
        L.append(f"- {link(fm)} _(updated {fm.get('updated', '?')})_")
    L.append("")

    os.makedirs("content/newsletters", exist_ok=True)
    out = os.path.join("content", "newsletters",
                       f"{TODAY.strftime('%y%m%d')}-{WIKINAME}-newsletter.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"wrote {out} ({len(updated)} updated, {len(raws)} refs, "
          f"{len(births)} births, {len(releases)} releases)")


if __name__ == "__main__":
    main()
