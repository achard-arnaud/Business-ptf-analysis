# Validation scope and reproducible checks

Run commands from the repository root after installing [core requirements](../requirements.txt):

```bash
python scripts/check_skill_docs.py
python scripts/check_template_registry.py
python -m unittest discover -s tests -v
```

The [getting-started guide](../docs/getting-started.md) separates HTML/core checks, browser setup and authorised archive inputs. The [business rule matrix](../docs/architecture/rules-and-validation.md) maps individual business invariants to code and representative tests.

## Coverage by boundary

| Boundary | Test modules | Evidence established |
| --- | --- | --- |
| Package/evidence/maturity/gates/frozen content | `test_contracts.py`, `test_sphere_bundle.py` | Types, references, dates, source scope, non-compensable gates, known negative cases and accessible bundle integrity |
| RunContext and handoff | `test_run_context_stages.py`, `test_research_handoff.py` | Versioned stage compatibility and handoff metadata |
| Session resumption | `test_session_checkpoint.py`, `test_cold_resume_cli.py` | Pinned input bytes, conflicting revision, stale/missing file and bounded subprocess resume |
| Skill discovery and registry | `test_skill_docs.py`, `test_template_registry.py` | Fixed navigation set/frontmatter, declared template paths and capabilities |
| Executive / value-chain output | `test_three_pager_exec.py`, `test_value_chain_views.py`, `test_value_chain_preview.py` | Profile-specific composition, synthetic sector topologies and negative cases |
| Artifact/QA/publication | `test_artifact_receipts.py`, `test_prepare_artifact_receipt.py`, `test_verify_render_evidence.py`, `test_publication_preflight.py` | Actual-byte integrity rules, render metadata/evidence checks and conservative release prerequisites |
| Renderer CI selection | `test_ci_render_selector.py` | Changed-path selection, including relevant removals/renames |
| Learning pilot | `test_pedagogical_renderer.py`, `test_pedagogical_landscape.py` | Binding/content fidelity, locked imports and learning-specific rendering contracts |

Some tests use synthetic fixtures; `test_sphere_bundle.py` also checks the committed Sphere dossier and targeted mutations. These have different evidence scopes. Neither creates new company facts or approves an investment decision.

## Browser and archive acceptance

[Contract CI](../.github/workflows/contracts.yml) selects browser checks by actual path changes or manual dispatch. Selected runs render the executive fixture and two value-chain profiles, verify actual PDFs/PNGs/QA hashes and reject a deliberate overflow. [Pedagogical CI](../.github/workflows/pedagogical-render.yml) separately sets `PEDAGOGICAL_BROWSER_TEST=1` and renders the six-page Perception sheet. Core local discovery may skip browser-dependent tests; report that scope explicitly.

External capture archives are not part of public CI. `validate_bundle.py --archive` adds the available declared-capture checks; `check_prehitl.py` adds material-original policy. Live transfer between model sessions, original-source truth, causal ROI and authenticated human release require their own evidence.

Pilot acceptance still requires source review, three review lenses, actual human HITL, the applicable frozen-content check, physical PDF generation, reader inspection and cross-pilot loopback. A passing structural or layout test covers its stated boundary.

## Documentation dependency coverage

The built-in route checker inspects a fixed navigation list rather than every Markdown file or transitive dependency. The [reference guide](../skills/enterprise-ai-learning/references/README.md) maps original-relative links in pinned source copies. Extending repository-wide documentation-link coverage in CI remains a separate implementation choice.
