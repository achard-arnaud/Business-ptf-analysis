# Documentation guide

Start with the [project showcase](../README.md). Use this guide to reach the operating contracts and the evidence behind each capability.

| Reader / task | Start here | Follow the dependency |
| --- | --- | --- |
| Business / functional data analyst | [Domain and data](architecture/domain-and-data.md) | [Data dictionary](data/DATA_DICTIONARY.md) → [business rules and checks](architecture/rules-and-validation.md) → [Sphere case](../companies/sphere/INDEX.md) |
| Engineer adapting or running the project | [Getting started](getting-started.md) | [Code map](architecture/code-map.md) → [template binding](architecture/template-binding.md) → [validation scope](../tests/README.md) |
| Functional architect | [Architecture register](architecture/README.md) | [Responsibility boundaries](architecture/end-to-end-etl.md) → [domain model](architecture/domain-and-data.md) → decision records |
| Agent continuing a company diagnosis | [Agent router](../AGENTS.md) | [Quickstart map](agent/quickstart-map.md) → one company manifest/index → [workflow](../skills/hivest-portfolio-ai/references/workflow.md) |
| Publisher / reader reviewer | [Render evidence](agent/render-qa-contract.md) | [Artifact receipt](agent/artifact-receipts.md) → [publication preflight](agent/publication-preflight.md) |
| Reviewer of project maturity | [Evidence-based FDA / FDE / architect review](architecture/review-2026-11-16.md) | Inspected contracts/code/tests → open acceptance gaps → [roadmap](roadmap/industrialization-backlog.md) |

## Authorities and document lifetimes

- **Current behaviour:** executable schemas, scripts, tests and the [template registry](../templates/registry.json), read at the same Git revision.
- **Current case status:** [programme state](../program/state.json) and each company manifest. Research material retains its own cutoff.
- **Method and judgement:** [decision rules](../contracts/decision-rules.md), [workflow](../skills/hivest-portfolio-ai/references/workflow.md) and [gates](agent/gates.md).
- **Historical decisions:** records centralised in [docs/architecture](architecture/README.md). Their original wording and reported runs remain dated evidence.
- **Historical execution reports:** [design QA](DESIGN_QA.md), [audit response](AUDIT_RESPONSE_2026-09-23.md), [exec integration](CATCHUP_EXEC_V0.3.md) and [original handoff](ORIGINAL_HANDOFF.md). Read them for provenance; use the current code map for capabilities.
- **Pinned imported references:** [pedagogical reference navigation](../skills/enterprise-ai-learning/references/README.md) resolves the original-relative links in preserved source copies.

Documentation changes follow links through schemas, validators, fixtures and tests. Update current descriptions together; retain original case artefacts, pinned imports and historical decision text. The [2026-11-16 review](architecture/review-2026-11-16.md) records this pass and its limits.
