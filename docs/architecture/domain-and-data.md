# Domain model: a company diagnostic linked to a decision

The unit of work is **one company, one research cutoff and one decision question**. The portfolio coordinates multiple company diagnostics. An opportunity describes a proposed operational improvement; its evidence and prerequisites determine what can be concluded.

## Business objects and relationships

| Object / grain | Relationship | Canonical representation |
| --- | --- | --- |
| Programme / portfolio | Selects company entities and the pilot → cluster → fund sequence. | [State](../../program/state.json), [roster](../../program/roster.json) |
| Company diagnostic at cutoff | Owns the evidence bundle, eight maturity dimensions, value chain and use cases. | `companies/<id>/package.json`, manifest and index |
| Source capture | Supplies one or more located fragments; `origin_id` records the common origin of reused material. | Package `sources[]`, external archive |
| Fragment | Belongs to one source and carries locator, excerpt and hash. | Package `fragments[]` |
| Claim | Uses fragments or basis claims, retains scope, epistemic status and contradiction links. | Package `claims[]` |
| Market driver | Connects external signals, company exposure and an economic mechanism to candidate opportunities. | Package `drivers[]`, market coverage |
| Value-chain activity | Describes value/friction/controls and links opportunities back to the business process. | Package `value_chain[]` |
| Use case | Links evidence, drivers, activity, baseline, KPI, dependencies and five hard gates. | Package `use_cases[]`, context `opportunity_links[]` |
| Decision and content version | References reviewed package/bundle hashes, accepted unknowns and final content freeze. | [RunContext](../../contracts/run-context.schema.json), [content schema](../../contracts/three-pager.schema.json) |
| Output and receipt | Project content into a layout; record bytes, QA and publication/readback separately. | Profile payload, render manifest, [artifact receipt](../../contracts/artifact-receipt.schema.json) |

The [data dictionary](../data/DATA_DICTIONARY.md) defines field semantics and units. The [rule matrix](rules-and-validation.md) identifies what the validators enforce.

## Data preparation and presentation boundaries

| Familiar data-platform responsibility | Representation here | Integration boundary |
| --- | --- | --- |
| Raw / acquired | Authorised original bytes or explicitly scoped excerpts outside public Git. | Source URI, actual hash, rights and capture kind. Acquisition is human/agent-assisted. |
| Staging / qualification | Source and fragment registries; typed claims, dates, scope and contradictions. | Package schema and epistemic validation. There is no general ERP/CRM connector layer. |
| Curated analytical objects | Drivers, activities, maturity, opportunities and strategic context. | Company bundle and declared dependencies; [wiki](../../wiki/INDEX.md) holds shared sector context. |
| Decision/reporting projection | Executive payload, audit content, fund note or pedagogical sheet. | [Profile-specific binding](template-binding.md), renderer and QA. |

These are responsibilities, not new `raw/staging/marts` directories. The repository's evidence→analysis→presentation layers serve its current purpose. A future operational data feed would require an explicit input contract, credentials/rights, mapping, idempotence and acceptance tests.

## Time, history and replay

`cutoff` bounds the research view. Publication date, access date, claim observation and validity dates describe different events. `revenue_year` identifies the reporting year; a render build revision identifies the software used to create an output.

Git versions controlled knowledge and code. External captures and receipts identify bytes at a location; the [checkpoint](../../contracts/session-checkpoint.schema.json) pins accessible inputs and output dependencies. The resume CLI compares those bytes and the independently observed Git SHA. This supports bounded replay checks; exact regeneration also depends on external archive availability and compatible runtime/browser/fonts.

There is no portfolio time-series fact table or automated T-versus-T−1 variance engine. Comparing company histories requires preserving scope, reporting period, units, source versions and accepted decisions. The [review](review-2026-11-16.md) tracks that remaining gap.

## Ownership and extension

Company manifests own workflow state, schemas own shape, business rules own decision policy, and humans own approval. The registry owns declared profile capabilities. The renderer owns layout.

Keep product, fund-note and learning workstreams explicit. The [external GreenYellow example](../../examples/three-pagers/greenyellow/README.md) illustrates an asset/service business model; its presence does not add a portfolio entity. A new source or sector first enters its appropriate data contract, then an analytical mapping, then a tested output profile.
