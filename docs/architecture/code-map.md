# Code map — inputs, outputs and execution boundaries

Use the [workflow](../../skills/hivest-portfolio-ai/references/workflow.md) for business sequencing, the [domain model](domain-and-data.md) for ownership and the [rule matrix](rules-and-validation.md) for the evidence behind each check.

## State, data and context

| Component | Input → output | Boundary |
| --- | --- | --- |
| [State](../../program/state.json), company manifest/index | Programme/case → active stage, cutoff and next work | States are maintained deliberately after gate review. |
| [Package](../../contracts/company-package.schema.json), [strategic context](../../contracts/strategic-context.schema.json) | Qualified evidence → analytical bundle | Types and meaning are described in the [dictionary](../data/DATA_DICTIONARY.md). |
| [RunContext](../../contracts/run-context.schema.json) | Workflow stage/evidence/version → resumable context | v0.2 supports MARKET_CONTEXT and OPPORTUNITIES; historical v0.1 remains version-limited. |
| [research_graph.py](../../scripts/research_graph.py) | Graph + target/changed node → bounded context or affected nodes | Dependency computation and open questions; no network research or automatic rewrite. |
| [compose_dossier.py](../../scripts/compose_dossier.py) | Company modules → pre-HITL dossier | Derived view; source/analytical files retain authority. |
| [session_checkpoint.py](../../scripts/session_checkpoint.py) | Checkpoint, accessible pinned files, independently observed Git SHA → readiness packet | Read-only metadata/input-byte checks; [resume protocol](../agent/context-and-resume.md). |
| [validate_handoff.py](../../scripts/validate_handoff.py) | Handoff envelope → metadata verdict | Capabilities are declared; external access and model transfer require real session evidence. |

## Validation and publication evidence

| Component | Input → output | Boundary |
| --- | --- | --- |
| [validate.py](../../scripts/validate.py) | Package or frozen content → structural / bounded semantic verdict | Frozen v0.2 content needs the bundle-aware library path. |
| [validate_bundle.py](../../scripts/validate_bundle.py) | Package/context/graph + optional archive → integrity verdict | `validate_freeze` library function adds bundle hash, review and accepted-unknown checks. CLI exposes bundle validation. |
| [check_prehitl.py](../../scripts/check_prehitl.py) | Company + capture archive → original-capture policy verdict | Human GO_DRAFT remains a separate decision. |
| [validate_exec.py](../../scripts/validate_exec.py) | Exec payload + canonical company bundle + archive → aligned-demo verdict | Checks figures, cutoff, bundle hash and pre-HITL capture; committee remains false. |
| [check_template_registry.py](../../scripts/check_template_registry.py) | Registry + schemas/files → declared capability consistency | Five profiles; does not dispatch/adapt content or grant release. |
| [validate_value_chain_view.py](../../scripts/validate_value_chain_view.py) | Variable-activity view → structure/reference verdict | Separate from actual rendering and evidence review. |
| [verify_render_evidence.py](../../scripts/verify_render_evidence.py) | Manifest, QA, actual PDF and PNGs → artifact/layout evidence verdict | [Render QA](../agent/render-qa-contract.md); reader review stays pending. |
| [prepare_artifact_receipt.py](../../scripts/prepare_artifact_receipt.py) | Actual file + producer/visibility/optional QA → prepared-only receipt | Local output; separate transport and independent readback required. |
| [validate_artifact_receipt.py](../../scripts/validate_artifact_receipt.py) | Receipt + independently supplied readback bytes → persistence/integrity checks | Does not fetch remote URLs or authenticate a human. |
| [publication_preflight.py](../../scripts/publication_preflight.py) | Render, receipt, actual PDF, readback/freeze/reader verdicts → release prerequisites | Conservative result remains awaiting authenticated human release. |
| [check_skill_docs.py](../../scripts/check_skill_docs.py) | Fixed route document set + skill metadata → navigation/frontmatter check | Current CI checks this fixed set; the broader recursive audit is recorded separately. |

## Rendering and CI

[Template binding](template-binding.md) maps each input contract to its renderer. Exec, strategic note, variable value chain and pedagogical rendering exist; audit remains schema-only. [Value-chain profiles](value-chain-profiles.md) details the legacy/preview distinction.

[Contract CI](../../.github/workflows/contracts.yml) runs the navigation check, registry check and unit suite. [ci_render_selector.py](../../scripts/ci_render_selector.py) selects browser QA from actual changed paths; manual dispatch also selects it. The renderer job generates three profile PDFs and nine PNGs plus manifests/QA and rejects a deliberate overflow. [Pedagogical CI](../../.github/workflows/pedagogical-render.yml) owns its separate path-filtered browser run.

The [test guide](../../tests/README.md) states exact coverage and exclusions. Private capture archives, semantic judgement, authenticated approval and live cross-model portability need independent evidence.

## History and remaining work

The [architecture register](README.md) retains historical choices and current annotations. Common narrative blocks, cross-format claim retention, authenticated publication, real client/source adaptation and portfolio consolidation remain distinct work in the [review](review-2026-11-16.md) and [roadmap](../roadmap/industrialization-backlog.md).
