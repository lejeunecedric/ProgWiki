#!/usr/bin/env python3
"""B3Wiki lint — run from repo root: python3 scripts/lint.py
Checks: broken wikilinks, orphans, index completeness, frontmatter,
tags vs SCHEMA taxonomy, entity folder discipline, non-English pages."""
import os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
issues = []

# taxonomy from SCHEMA.md
schema = open(os.path.join(R, "SCHEMA.md")).read()
m = re.search(r"## Tag Taxonomy\n(.*?)\n\n", schema, re.S)
tax_block = m.group(1) if m else ""
TAX = set(re.findall(r"- `([a-z-]+)`", tax_block))

# folder → allowed subject rule (players = organists only etc. — semantic, we check structural hints)
ENT_RULES = {
    "instruments": None, "players": None, "manufacturers": None,
    "bands": None, "albums": None, "labels": None, "people": None,
}

slugs, meta = set(), {}
for sub in ["entities", "concepts", "comparisons", "queries"]:
    for root, _, fs in os.walk(os.path.join(R, sub)):
        for f in fs:
            if f.endswith(".md") and f != "index.md" and f != "SCHEMA.md" and f != "_index.md":
                slugs.add(f[:-3])

nonword = re.compile(r"\b(le|la|les|des|une|un|et|der|die|das|und|het|een)\b", re.I)
for root, _, fs in os.walk(R):
    if ".git" in root: continue
    for f in fs:
        if not f.endswith(".md") or f == "_index.md": continue
        p = os.path.join(root, f); rel = os.path.relpath(p, R)
        txt = open(p, encoding="utf-8", errors="replace").read()
        links = [l.split("/")[-1] for l in re.findall(r"\[\[([^\]|#]+)", txt)]
        if f == "AGENTS.md": links = [l for l in links if l != "slug"]  # [[slug]] is a literal example
        for l in links:
            if l in ("wikilinks", "page-a", "page-b", "..."): continue
            if l not in slugs: issues.append(f"BROKEN  {rel}: [[{l}]]")
        # frontmatter check for wiki pages
        top = rel.split(os.sep)[0]
        if top in ("entities", "concepts", "comparisons", "queries") and f not in ("index.md",):
            m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
            if not m: issues.append(f"FRONT   {rel}: missing frontmatter"); continue
            fm = m.group(1)
            for field in ("title:", "created:", "updated:", "type:", "tags:", "sources:"):
                if field not in fm: issues.append(f"FRONT   {rel}: missing {field[:-1]}")
            tm = re.search(r"tags: \[(.*?)\]", fm)
            if tm:
                for t in [t.strip() for t in tm.group(1).split(",")]:
                    if t and t not in TAX: issues.append(f"TAG     {rel}: '{t}' not in taxonomy")
            # entity folder discipline
            parts = rel.split(os.sep)
            if parts[0] == "entities" and len(parts) == 3:
                folder, slug = parts[1], parts[2][:-3]
                if folder == "players":
                    for bad in ("band", "quartet", "trio", "orchestra", "group"):
                        if bad in slug: issues.append(f"FOLDER  {rel}: looks like a band, not a player")
                if folder == "labels" and not re.search(r"records|label|beat", txt[:400].lower()):
                    issues.append(f"FOLDER  {rel}: check this is really a record label")
            # non-English heuristic (only for page bodies, skip log/index) — WARNING only:
            # flags legitimate cases too ("à la", foreign names like "van der Wal", quoted foreign press)
            if nonword.search(txt) and f not in ("README.md",):
                hits = ", ".join(sorted({w.lower() for w in nonword.findall(txt)})[:5])
                print(f"warn LANG? {rel}: possible non-English words: {hits}")
        # orphan + inbound
        for l in set(links):
            pass
inbound = {s: 0 for s in slugs}
for root, _, fs in os.walk(R):
    if ".git" in root: continue
    for f in fs:
        if f.endswith(".md") and f != "_index.md" and f not in ("SCHEMA.md", "log.md"):
            txt = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for l in re.findall(r"\[\[([^\]|#]+)", txt):
                l = l.split("/")[-1]
                if l in inbound and l not in (f[:-3],): inbound[l] += 1
for s, n in inbound.items():
    if n == 0: issues.append(f"ORPHAN  {s}.md: no inbound links")

# index completeness
idx = open(os.path.join(R, "index.md")).read()
for s in sorted(slugs):
    if s not in idx: issues.append(f"INDEX   {s}.md not in index.md")

print(f"{len(slugs)} wiki pages")
if issues:
    print(f"\n{len(issues)} issues:")
    for i in sorted(issues): print(" ", i)
    sys.exit(1)
print("Lint clean ✔")
