# Extension 08 · Knowledge Representation Choice

> The form in which knowledge is encoded determines what reasoning is possible. Different forms · different leverage.

---

## Principle

Workspaces commonly choose one knowledge representation by default and never question it:
- **Prose markdown** · easy to write · hard to query
- **Structured YAML/JSON** · machine-queryable · awkward to read
- **Vector embeddings** · semantic recall · opaque to humans · hard to debug
- **Knowledge graph (RDF / property graph)** · relational queries · setup cost
- **Symbolic / Lisp-like** · composable reasoning · learning curve

The best workspaces **mix representations strategically** by use case · not by default.

---

## Decision matrix

| Use case | Best representation |
|----------|---------------------|
| Human reading + occasional agent search | Prose markdown with structured frontmatter |
| Agent registry of entities (daemons · cron · skills) | YAML/JSON · machine-readable indices |
| Semantic recall ("what file is similar to X") | Vector embeddings (e.g., Voyager skill library) |
| Relational queries ("which rule blocks which tool") | Knowledge graph (RDF · Neo4j) |
| Symbolic reasoning ("if A and B then C") | Datalog · Lisp · constraint logic |
| Temporal events | Append-only log + structured fields |
| Procedural rules | Markdown with `Why` + `How to apply` sections |

---

## Typical workspace · representation audit template

The benchmark's `score` command introspects what the audited workspace uses. A workspace audit produces a table like:

| Layer | Representation today | Gap |
|-------|----------------------|-----|
| Documentation | Markdown · frontmatter YAML | Good |
| Skill catalog | Markdown skill manifest + folder | Good |
| Memory tiers | Markdown + folder hierarchy | Could benefit from vector layer for semantic recall |
| Entity registry | Scattered across INDEX files | Recommended: dedicated YAML registry |
| Pattern catalog | Markdown articles | Could benefit from graph layer (which patterns compose) |
| Cross-link spine | Markdown links | Risk: broken-link drift · could benefit from graph integrity check |

Each workspace gets its own row · the right answer depends on use case.

---

## Measurement

- `% of workspace content matched to right representation` (audit by reviewer · target ≥ 0.85 at L4)
- `query latency` per representation type · is the chosen form fast enough for the use?
- `% of broken cross-links` (target ≤ 0.02 at L4)

---

## Anti-patterns

- ❌ Putting structured data in prose (lose machine-readability).
- ❌ Putting human-explanation in YAML (lose readability).
- ❌ Vector embeddings as the only retrieval · opaque · can't debug failure modes.
- ❌ Knowledge graph for everything · setup cost ≫ benefit for small workspaces.

---

_Extension 08 · iter-2 · 2026-05-20_
