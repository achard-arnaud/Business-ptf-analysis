# Business rules and their validation evidence

The [decision rules](../../contracts/decision-rules.md) own business policy. Schemas define shape; scripts enforce bounded invariants; people review meaning and authorise decisions. This matrix connects those layers without introducing another scoring model.

| Rule / question | Executable check | Representative tests | Remaining judgement / limit |
| --- | --- | --- | --- |
| IDs are unique and references resolve in the correct scope | `index`, `refs`, `validate_package` in [validate.py](../../scripts/validate.py) | [Contracts](../../tests/test_contracts.py): duplicate IDs, missing source, wrong company, sector laundering, circular claim | Source interpretation and the real organisational perimeter |
| Dates fit the research cutoff and evidence remains fresh | `validate_package`: source publication, observation, expiry for scores/gates | Contract tests: future source, claim before publication, stale score/gate | Whether an undated or non-expiring claim is still relevant |
| Independent corroboration retains the original source identity | Normalised URL/hash → common `origin_id`; origin count for scores ≥3 | Contract tests: repeated press release, same URL/hash with distinct origins | Actual independence of organisations/documents |
| Unknown maturity uses null; score claims meet evidence gates | Package schema + `validate_package` | Contract tests: zero unknown, duplicated dimension, job/announcement evidence, scale and counter-evidence | Per-dimension anchors and their calibration; high scores currently require deployed evidence even outside delivery |
| Five hard gates precede priority | `priority_state`: any fail→blocked; otherwise any unknown→validation_required; otherwise eligible | Contract tests: missing/duplicate gates, hypotheses/jobs/social/stale facts used to pass | Data rights, operational security and actual human accountability |
| Opportunities link drivers, baseline and business process | v0.2 package checks + [bundle validator](../../scripts/validate_bundle.py) | [Sphere bundle tests](../../tests/test_sphere_bundle.py), market/driver and double-count tests | KPI formula quality, causal attribution and credible owner |
| Reused cost base has an explicit overlap explanation | v0.2 `cost_base_id` check for reduction/avoidance | Contract test for double counting | Reconciliation of economic benefit, cash and EBITDA; no ROI aggregation engine |
| Segment mix and BCG axes are coherent | `validate_bundle`: shares total 100, reporting year, required BCG axes | Sphere tests: mix, BCG and leadership scope | Comparable perimeter, period and unit; market-share estimates |
| Archive and bundle integrity match declared bytes | `validate_bundle` with archive, capture-kind checks and artifact hashes | Sphere tampering/path/coverage tests; capture tests in [tests](../../tests/README.md) | Rights review, faithful extraction and archive availability |
| Material-source capture satisfies pre-decision policy | [check_prehitl.py](../../scripts/check_prehitl.py) | Sphere/source-capture cases | Actual human GO_DRAFT |
| Final content matches reviewed evidence and open unknowns | `validate_freeze` in [bundle validator](../../scripts/validate_bundle.py) → `validate_content` | [Contract tests](../../tests/test_contracts.py) cover frozen content and changes after HITL; they do not exercise the full bundle-aware v0.2 freeze path | Archive verification through the freeze path, authenticated human approval, and semantic quality still need separate evidence |
| Template capability matches executable paths | [Registry checker](../../scripts/check_template_registry.py) | [Registry tests](../../tests/test_template_registry.py) | Reader acceptance and production readiness |
| Render evidence describes the actual PDF and PNGs | [Render verifier](../../scripts/verify_render_evidence.py) | [Render evidence tests](../../tests/test_verify_render_evidence.py) | Human reading; calibrated visual regression across browser versions |
| Resume rejects stale inputs or conflicting HEAD | [Checkpoint CLI](../../scripts/session_checkpoint.py) | [Checkpoint](../../tests/test_session_checkpoint.py), [cold resume](../../tests/test_cold_resume_cli.py) | Real transfer between model sessions and accessible external archives |
| Publication/readback remain distinct from approval | [Receipt validator](../../scripts/validate_artifact_receipt.py), [preflight](../../scripts/publication_preflight.py) | [Receipt](../../tests/test_artifact_receipts.py), [preflight](../../tests/test_publication_preflight.py) | Independent remote readback and authenticated human release |

## CLI and library boundaries

`python scripts/validate.py package <file>` validates a package. Its `content <content> <package>` CLI checks frozen content but does not accept a bundle hash argument; package v0.2 content needs the bundle-aware library path.

`validate_freeze(content, directory, archive)` in `scripts/validate_bundle.py` computes the canonical bundle hash, checks surviving reviews and accepted open questions, then calls `validate_content`. The bundle CLI exposes bundle validation only. The [publication preflight](../agent/publication-preflight.md) still needs an actual freeze-verdict integration and authenticated release path for real E2E acceptance.

## Verify the appropriate layer

Use the [getting-started commands](../getting-started.md) for a public demonstration or accessible bundle checks. Use your authorised archive for source-byte checks. Apply the [render QA contract](../agent/render-qa-contract.md) to newly generated PDFs. Keep `PASS`, `FAIL` and `NOT_RUN` attached to the exact inputs/version and check performed.
