# ProgWiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [2026-10-20] create | Wiki initialized
- Domain: progressive rock (bands, musicians, instruments, sub-styles, labels, concepts)
- Structure created: SCHEMA.md, LICENSE (CC0), README.md, index.md, log.md, raw/articles/, entities/{bands,musicians,instruments,labels,substyles}/, concepts/, comparisons/, queries/

## [2026-10-20] build | 8 parallel research/writing agents
- 8 subagents each produced a cluster of sourced fiches and ingested raw sources:
  - King Crimson cluster (band, Fripp, Bruford, Wetton, Mellotron, odd-time-signatures, king-crimson-eras, king-crimson-legacy)
  - Yes cluster (band, Anderson, Squire, Howe, Wakeman, Rickenbacker 4001, concept-album, yes-vs-genesis)
  - Genesis cluster (band, Gabriel, Collins, Hackett, double-neck-guitar, charisma-records, classic-prog-vs-neo-prog)
  - ELP + Jethro Tull cluster (bands, Emerson, Lake, Palmer, Ian Anderson, hammond-organ, suite, classical-and-jazz-crossover)
  - Pink Floyd / VDGG / Gentle Giant / Camel cluster (bands, moog-synthesizer, extended-composition, analogue-synthesizer-texture)
  - Sub-styles A + labels (symphonic-prog, canterbury-scene, zeuhl, rock-in-opposition, harvest/vertigo/virgin-records, symphonic-vs-canterbury, what-is-canterbury-scene)
  - Sub-styles B (krautrock, space-rock, neo-prog, progressive-metal, virtuosity)
  - Modern cluster (rush, tool, chapman-stick, prog-rock-vs-progressive-metal)
- ~66 raw sources ingested into raw/articles/ with provenance frontmatter

## [2026-10-20] restructure | Consolidate entity layout
- Moved instruments written to top-level `instruments/` (double-neck-guitar, rickenbacker-4001-bass, hammond-organ) into `entities/instruments/`
- Moved labels written to top-level `labels/` into `entities/labels/`
- Removed duplicate hammond-organ (kept the richer version); removed empty top-level dirs
- All entities now live under `entities/<kind>/` per SCHEMA

## [2026-10-20] fix | Recompute raw sha256
- Recomputed sha256 for all raw articles from their on-disk body (hash-of-actual-body invariant); 66 files corrected

## [2026-10-20] create | progressive-rock + mellotron-vs-synthesizer
- concepts/progressive-rock.md (umbrella concept, referenced by 4 pages)
- comparisons/mellotron-vs-synthesizer.md (comparison in the canonical dict that was unassigned)

## [2026-10-20] fix | De-link dead wikilinks
- Converted [[wikilinks]] to plain text for passing-mention entities with no page (marillion, magma, henry-cow, soft-machine, dream-theater, queensryche, jon-lord, tangerine-dream, zappa, the-who, etc.) — 11 files touched

## [2026-10-20] ingest | Rush: 2112 + Moving Pictures
- raw/articles/wikipedia-2112.md, raw/articles/wikipedia-moving-pictures.md (provenance refs in entities/bands/rush.md)

## [2026-10-20] lint | 0 broken wikilinks, 1 pass
- All [[wikilinks]] resolve to existing pages; all pages have >= 2 outbound links
- All raw sha256 verified; all provenance markers resolve
- Total pages: 59 (11 bands, 14 musicians, 6 instruments, 4 labels, 8 sub-styles, 8 concepts, 6 comparisons, 2 queries)
- index.md rebuilt from actual files
## [2026-10-20] entities/references | 4 new reference pages
- Added entities/references/: magazines, blogs, radio-stations, youtube-channels (prog rock sources for ingestion)
- index.md updated (References section; total 59 -> 63)
## [2026-10-20] lint + schema | tag taxonomy aligned, README links fixed
- SCHEMA.md taxonomy: added cross-cutting slug tags (symphonic-prog, concept-album, neo-prog, progressive-metal, extended-composition)
- Normalized off-taxonomy tags in 5 pages (genre/scene/movement/keyboard -> history)
- README: `comparisons`/`queries` folder mentions converted to backticks (were lint BROKEN)
- lint.py: 0 issues on 63 pages

## [2026-10-20] entity-extraction | 14 new pages from cited-but-undocumented entities
- Scanned all 68 raw/articles/ sources against existing slugs; found cited entities with no page (2+ source citations each)
- Created 14 pages: bands (dream-theater, gong, marillion, renaissance, soft-machine, tangerine-dream), musicians (adrian-belew, peter-hammill, roger-waters, syd-barrett, tony-banks, tony-levin), labels (manticore-records), substyles (jazz-fusion)
- Added inbound wikilinks in existing pages: van-der-graaf-generator, genesis, symphonic-prog, progressive-metal, canterbury-scene, krautrock, neo-prog, zeuhl, emerson-lake-palmer
- index.md updated (63 -> 77 pages); remaining high-citation candidates noted: kevin-ayers, hugh-banton, michael-giles, mel-collins, patrick-moraz, kraftwerk, henry-cow, kansas, fates-warning, caravan, national-health, math-rock, post-rock, motorik

## [2026-10-20] lint | 2 issues, fixed
- log.md prose `comparisons/`/`queries/` folder mentions converted to backticks; lint clean on 77 pages

## [2026-10-20] newsletter | first weekly newsletter + scripts/newsletter.py
- Added `scripts/newsletter.py` (weekly generator: anniversaries from born/died/released frontmatter, recently updated pages, new raw references, queries on file)
- Created `content/newsletters/261020-ProgWiki-newsletter.md`

## [2026-10-20] newsletter | 70s-press rewrite
- Rewrote `scripts/newsletter.py` as a music-magazine dispatch: NEW RELEASES (week-of album anniversaries + nearest-upcoming preview), SPECIAL (rotating concept/label/manufacturer/query feature with prose pulled from the page), ANNIVERSARIES (birthdays/deaths + early-card fallback), BACK PAGES (recent edits, reference room, queries)
- Regenerated `content/newsletters/261020-ProgWiki-newsletter.md`
