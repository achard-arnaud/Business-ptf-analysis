# Code map — execution boundaries

Use the [Hivest workflow](../../skills/hivest-portfolio-ai/references/workflow.md) for programme sequencing. For new independent cases, the [standalone skill](../../skills/standalone-company-analysis/SKILL.md) describes the procedure and the [case runtime](../agent/case-process.md) enforces the stage contracts. The historical `companies/` route does not acquire A0–A4 receipts retroactively ([ADR-0002](ADR-0002-case-process.md)).

| Component | Capability | Boundary |
|---|---|---|
| Manifest and programme state | Scope, stage and next work | Independent runs use `program_ref=null`, outside Hivest roll-ups |
| Company package | Source, fragment and claim lineage | Public research may remain a draft |
| `research_graph.py` | Dependency context and affected nodes | No web research, graph initialization or automatic rewrite |
| Standalone analysis skill | Guides routing and composition of the three-page output | Procedure only; no `Agent.py` orchestrator exists |
| [Case runtime](../../scripts/case_runtime.py) | Initializes an isolated case and its graph before collection; validates inputs, outputs and dependencies as the agent begins and completes A0–A4 | The agent gathers evidence and makes judgments. The runtime checks submitted artifacts and records attempts. |
| [Case manifest](../../workflow/case-process.json) and contracts | The manifest defines stage order and dependencies; the [manifest schema](../../contracts/case-process.schema.json) constrains it and the [artifact schema](../../contracts/case-artifacts.schema.json) defines stage data | The [engine release](../../workflow/engine-release.json) pins the shared implementation and schemas; it does not define this repository’s stage order. |
| Validators/renderers | Structural or render checks | No implied human approval |
| [Artifact receipt](../agent/artifact-receipts.md) | The [schema](../../contracts/artifact-receipt.schema.json) records the artifact location, integrity, QA, persistence and authorization metadata separately. | The [receipt validator](../../scripts/validate_artifact_receipt.py) requires independently re-read bytes with the same SHA-256 for `published_verified`. It does not publish the artifact or authenticate a decision. |
| [Publication preflight](../agent/publication-preflight.md) | The [preflight](../../scripts/publication_preflight.py) checks the receipt, PDF bytes, freeze evidence and reader review. | Even if all checks pass, it returns `AWAIT_AUTHENTICATED_HUMAN_RELEASE` and `committee_authorized=false`. Only the authorized human workflow can release the artifact to the committee. |
