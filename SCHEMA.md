# ProgWiki Schema

## Domain
A knowledge base about **progressive rock** — the music movement spanning roughly 1966–1980 (the British "classic prog" core) and its scenes and descendants through the present. Covers the key **bands** (King Crimson, Yes, Genesis, Pink Floyd, Emerson, Lake & Palmer, Van der Graaf Generator, Gentle Giant, Jethro Tull, Camel, Rush, Tool…), the **musicians** who defined the sound (Fripp, Anderson, Squire, Howe, Wakeman, Emerson, Lake, Palmer, Gabriel, Collins, Hackett…), the signature **instruments** (Mellotron, Hammond organ, Moog synthesizer, Rickenbacker bass, double-neck guitar, Chapman Stick…), the **sub-styles** (symphonic prog, Canterbury scene, zeuhl, RIO, krautrock, space rock, neo-prog, progressive metal…), the **labels** that carried it, and the musical **concepts** that make it distinctive (concept album, odd time signatures, the suite, virtuosity, classical/jazz crossover, extended composition). English-language wiki.

**Purpose:** first-hand compiled knowledge, grounded in real sources; one page = one clear entity or lesson. Sources are ingested verbatim into `raw/` and synthesized here with provenance markers.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `king-crimson.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- Wikilinks use **bare slugs** (e.g. `[[king-crimson]]`); display text via `[[king-crimson|King Crimson]]`
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** on pages synthesizing 3+ sources, append `^[raw/articles/source-file.md]` to paragraphs whose claims trace to a specific source. Optional on single-source pages.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
confidence: high | medium | low   # optional
contested: true                    # optional, unresolved contradictions
---
```

### raw/ Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of the body below the frontmatter>
---
```

## Tag Taxonomy
- `band` — progressive rock bands (yes, king crimson, genesis, pink floyd…)
- `musician` — players, singers, composers (fripp, anderson, emerson…)
- `instrument` — signature instruments (mellotron, hammond, moog…)
- `substyle` — genres/scenes within prog (symphonic, canterbury, zeuhl, krautrock…)
- `concept` — recurring musical/formal ideas (concept album, odd metre, suite…)
- `label` — record labels central to prog (Charisma, Harvest, Vertigo, Virgin…)
- `record` — notable albums (Close to the Edge, In the Court of the Crimson King…)
- `history` — dates, timelines, band/industry events
- `music` — techniques, playing styles, notable recordings
- `comparison` — side-by-side analyses
- `query` — filed query results
- `source` — note about an ingested source
- `symphonic-prog` — slug tag, cross-cutting (canonical substyle slug)
- `concept-album` — slug tag, cross-cutting
- `neo-prog` — slug tag, cross-cutting
- `progressive-metal` — slug tag, cross-cutting
- `extended-composition` — slug tag, cross-cutting

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions
- **Split a page** when it exceeds ~200 lines
- **Archive** superseded pages to `_archive/` and remove from index

## Entity Pages
Entities live in `entities/` **subfolders by kind**:
- `entities/bands/` — King Crimson, Yes, Genesis, Pink Floyd, ELP, VDGG, Gentle Giant, Jethro Tull, Camel, Rush, Tool…
- `entities/musicians/` — players and singers (Fripp, Anderson, Squire, Howe, Wakeman, Emerson, Lake, Palmer, Gabriel, Collins, Hackett, Bruford, Ian Anderson…)
- `entities/instruments/` — Mellotron, Hammond organ, Moog synthesizer, Rickenbacker 4001 bass, double-neck guitar, Chapman Stick…
- `entities/labels/` — Charisma, Harvest, Vertigo, Virgin…
- `entities/substyles/` — symphonic prog, Canterbury scene, zeuhl, RIO, krautrock, space rock, neo-prog, progressive metal…

One page per notable entity. Overview, key facts/dates, the signature sound, relationships via `[[wikilinks]]`, sources.

## Concept Pages
One page per concept (concept album, odd time signatures, the suite, virtuosity, classical/jazz crossover, extended composition, analogue-synth texture). Definition, how it manifests in prog, canonical examples (`[[wikilinks]]` to bands/albums), related concepts.

## Comparison Pages
Side-by-side analyses in table form (e.g., Yes vs Genesis, symphonic vs Canterbury, Mellotron vs synthesizer), with verdict/synthesis and sources.

## Query Pages
A filed question with a cited multi-channel answer and a synthesis, plus open threads. See `queries/`.

## Update Policy
1. Newer sources generally supersede older ones
2. Genuinely contradictory claims: note both with dates and sources
3. Mark `contested: true` in frontmatter and flag for review

## Canonical Slug Dictionary (v1)
Bands → `king-crimson, yes, genesis, pink-floyd, emerson-lake-palmer, van-der-graaf-generator, gentle-giant, jethro-tull, camel, rush, tool`
Musicians → `robert-fripp, greg-lake, bill-bruford, john-wetton, jon-anderson, chris-squire, steve-howe, rick-wakeman, keith-emerson, carl-palmer, peter-gabriel, phil-collins, steve-hackett, ian-anderson`
Instruments → `mellotron, hammond-organ, moog-synthesizer, rickenbacker-4001-bass, double-neck-guitar, chapman-stick`
Labels → `charisma-records, harvest-records, vertigo-records, virgin-records`
Sub-styles → `symphonic-prog, canterbury-scene, zeuhl, rock-in-opposition, krautrock, space-rock, neo-prog, progressive-metal`
Concepts → `concept-album, odd-time-signatures, suite, virtuosity, classical-and-jazz-crossover, extended-composition, analogue-synthesizer-texture`
Comparisons → `yes-vs-genesis, classic-prog-vs-neo-prog, symphonic-vs-canterbury, mellotron-vs-synthesizer, king-crimson-eras, prog-rock-vs-progressive-metal`
