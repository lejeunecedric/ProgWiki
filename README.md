# ProgWiki

Self-updating LLM-wiki knowledge base on **progressive rock**.

A cross-linked knowledge base that keeps **entities strictly separated by kind** — bands, musicians, instruments, labels, sub-styles — and connects them through shared **concepts** (concept album, odd time signatures, the suite, virtuosity, classical/jazz crossover, extended composition) and side-by-side **comparisons**.

## Layout

- `SCHEMA.md` — the wiki's schema, conventions, tag taxonomy, and canonical slug dictionary
- `index.md` — content catalog (read this first)
- `log.md` — append-only record of every wiki action
- `entities/bands/`, `entities/musicians/`, `entities/instruments/`, `entities/labels/`, `entities/substyles/` — one page per entity, cross-linked with `[[wikilinks]]`
- `concepts/` — recurring musical/formal ideas shared across bands
- `comparisons/` — side-by-side analyses (Yes vs Genesis, symphonic vs Canterbury, Mellotron vs synthesizer…)
- `queries/` — filed questions with cited answers
- `raw/articles/` — ingested source material (verbatim, with sha256), the provenance bedrock for every page

## License

CC0 1.0 Universal (see `LICENSE`).
