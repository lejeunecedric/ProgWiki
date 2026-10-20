<div align="center">

<img src="assets/progwiki-hero.jpg" alt="ProgWiki — floating islands with grand piano, pipe organ and Mellotron above a cosmic prog-rock landscape" width="100%">

# ProgWiki 🎹

**A self-updating, cross-linked LLM knowledge base on progressive rock.**

*Every claim traceable to an ingested source. Every entity cross-linked into one hypertext.*

![Pages](https://img.shields.io/badge/pages-59-4c1d95) ![Raw sources](https://img.shields.io/badge/raw_sources-68-0f766e) ![Wikilinks](https://img.shields.io/badge/linked-hypertext-b45309) ![License](https://img.shields.io/badge/license-CC0_1.0-lightgrey)

</div>

---

## What is this?

ProgWiki is a **dataset-shaped encyclopedia** built for LLM consumption and human reading alike. It covers progressive rock — the British "classic prog" core (1966–1980) and its scenes and descendants — in short, dense, sourced pages.

Two rules hold the whole thing together:

1. **Entities are kept strictly apart by kind.** A band is not a musician is not an instrument is not a sub-style. Each gets its own page, in its own folder.
2. **Concepts are the crossroads.** The recurring musical ideas — the concept album, odd time signatures, the suite, virtuosity — get their own pages too, and every band, musician and instrument links back to them. That's what turns 59 isolated fiches into one knowledge graph.

Every paragraph whose claims trace to a source carries a provenance marker, and every source lives verbatim in `raw/` with its sha256.

## At a glance

| Kind | Count | Examples |
|---|---|---|
| 🎸 Bands | 11 | [[king-crimson]], [[yes]], [[genesis]], [[pink-floyd]], [[rush]] |
| 🧑‍🎤 Musicians | 14 | [[robert-fripp]], [[chris-squire]], [[keith-emerson]], [[peter-gabriel]] |
| 🎛️ Instruments | 6 | [[mellotron]], [[hammond-organ]], [[moog-synthesizer]], [[chapman-stick]] |
| 🏷️ Labels | 4 | [[charisma-records]], [[harvest-records]], [[vertigo-records]] |
| 🗺️ Sub-styles | 8 | [[symphonic-prog]], [[canterbury-scene]], [[zeuhl]], [[krautrock]] |
| 🧩 Concepts | 8 | [[concept-album]], [[odd-time-signatures]], [[suite]], [[virtuosity]] |
| ⚖️ Comparisons | 6 | yes-vs-genesis, mellotron-vs-synthesizer, king-crimson-eras |
| ❓ Queries | 2 | *Why is King Crimson the yardstick of serious prog?*, *What is the Canterbury scene?* |
| **Total pages** | **59** | + **68** ingested raw sources |

## How it's organized

```text
ProgWiki/
├── SCHEMA.md              ← the contract: conventions, tag taxonomy, slug dictionary
├── index.md               ← START HERE — catalog of every page, one line each
├── log.md                 ← append-only record of every wiki action
├── entities/
│   ├── bands/             ← one page per band, cross-linked
│   ├── musicians/         ← players and singers
│   ├── instruments/       ← the signature gear
│   ├── labels/            ← the record labels that carried prog
│   └── substyles/         ← scenes and genres within prog
├── concepts/              ← shared ideas: the glue between entities
├── comparisons/           ← side-by-side analyses with a verdict
├── queries/               ← filed questions with cited answers
└── raw/articles/          ← ingested sources (verbatim, sha256-stamped)
```

## Provenance

Every page carries:

- **frontmatter** — `type`, `tags`, `sources`, `confidence`
- **`^[raw/articles/…]` markers** on each sourced paragraph
- **raw sources** in `raw/articles/`, each stamped with its `source_url` and the sha256 of its stored body

Recompute any hash yourself:

```bash
python3 - <<'PY'
import hashlib, re, pathlib
for f in pathlib.Path("raw/articles").glob("*.md"):
    t = f.read_text(); m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    assert hashlib.sha256(t[m.end():].encode()).hexdigest() == \
           re.search(r"sha256: ([0-9a-f]{64})", m.group(1)).group(1), f.name
print("all raw hashes OK")
PY
```

## How to browse

1. Open **[index.md](index.md)** — it lists all 59 pages with a one-line summary.
2. Follow the `[[wikilinks]]`. From [[king-crimson]] you'll reach [[mellotron]], [[odd-time-signatures]], [[bill-bruford]] — and back through them to [[symphonic-prog]] and beyond.
3. Want a synthesis instead? Read the `comparisons/` and `queries/` pages.

## Self-updating

The wiki grows the same way it was built: file a question as a `queries/` page, ingest its sources into `raw/`, write the entity/concept pages it calls for, update `index.md` and `log.md`, and link everything into the existing graph. The rules live in **[SCHEMA.md](SCHEMA.md)** — conventions, page thresholds (create only when central or backed by 2+ sources), and the canonical slug dictionary that keeps every link resolving.

## License

CC0 1.0 Universal — see [LICENSE](LICENSE).

---

<div align="center">
<sub>Built as an LLM-wiki knowledge base: raw provenance + synthesized, wikilinked English fiches. No invented dates, albums or quotes.</sub>
</div>
