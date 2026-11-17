# Architecture and decision register

This directory centralises the architecture views and decision records. The existing repository convention is **`docs/architecture/`**; compatibility pages preserve earlier entry paths.

## Current architecture

| Question | Document | Executable anchor |
| --- | --- | --- |
| Which responsibilities own research, reasoning and publication? | [Extract / Transform / Publish](end-to-end-etl.md) | [Workflow](../../skills/hivest-portfolio-ai/references/workflow.md), [registry](../../templates/registry.json) |
| What are the business objects, boundaries and dates? | [Domain and data](domain-and-data.md) | [Company package](../../contracts/company-package.schema.json), [strategic context](../../contracts/strategic-context.schema.json) |
| What does each field mean? | [Data dictionary](../data/DATA_DICTIONARY.md) | Schemas and their referenced validators |
| Which business rules are checked, and by what? | [Rules and validation](rules-and-validation.md) | [Package validator](../../scripts/validate.py), [bundle validator](../../scripts/validate_bundle.py), tests |
| How do analytical objects bind to outputs? | [Template binding](template-binding.md), [value-chain profiles](value-chain-profiles.md) | Profile-specific schemas and renderers |
| Which entry points actually exist? | [Code map](code-map.md) | Scripts, tests and workflows |

## Decision records and provenance

The search of tracked files and accessible Git history found **no pre-existing numbered ADR file**. Architectural choices were recorded inside the following three documents. They retain their filenames, source text, original dates and declared status. Their placement in this register preserves history; it does not confer approval on an entire historical report.

| Record | Original location | Status / scope of authority |
| --- | --- | --- |
| [ADR-0001 — Centralise architecture records](ADR-0001-centralise-architecture-records.md) | New, 2026-11-16 | Documentation organisation authorised by the current user request. |
| [Programme design](PROGRAM_DESIGN.md) | `docs/PROGRAM_DESIGN.md` | Historical design dossier; pilot choices and reuse proposals. Approval identity/date for each methodological clause are not documented here. |
| [Sphere loopback](LOOPBACK_SPHERE_V03.md) | `docs/LOOPBACK_SPHERE_V03.md` | Historical methodological decision and reported run, 23 September 2026; programme-wide acceptance still depends on the second pilot. |
| [Cross-repository audit](CROSS_REPO_AUDIT_AND_BOOTSTRAP_2026-11-04.md) | `docs/roadmap/CROSS_REPO_AUDIT_AND_BOOTSTRAP_2026-11-04.md` | Design/review proposals, 4 November 2026; its capability findings describe that revision. |

### Read historical findings against current code

| Historical wording | Current interpretation / pointer |
| --- | --- |
| Programme design mentions an unknown maturity “score nul”. | [Decision rules](../../contracts/decision-rules.md) and the package schema require `score=null`, `status=unknown`; numeric zero is rejected. |
| Design refers to six internal modules. | The active [workflow](../../skills/hivest-portfolio-ai/references/workflow.md) has seven procedures, plus conditional references. |
| Cross-repo audit reports missing stage enums, registry and receipts. | Versioned stages, registry, receipts and resume CLI are present; see [code map](code-map.md). Real E2E acceptance remains item-specific. |
| Cross-repo audit describes browser CI as manual only. | Current [CI selection](../agent/render-ci-selection.md) selects rendering from changed paths and supports manual dispatch. |
| A historical run reports a passing count or archive check. | This is evidence about that run and its inputs. Current validation scope is in [tests/README.md](../../tests/README.md). |

For new decisions, assign a stable ADR ID, state the scope/status and approval evidence, explain the options and consequences, and specify a review trigger. Record a successor when changing a substantive decision. Keep executable contract details at their owning schema/script and link to them.

- [ADR-0002 — Executable cases](ADR-0002-case-process.md): RUN/BUILD, stage I/O and pins.
- [ADR-0003 — Loopback](ADR-0003-loopback.md): trace-based diagnostics and BUILD experiments.
