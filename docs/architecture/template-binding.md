# Template binding: analytical meaning to output contract

Binding selects and maps prepared content to the fields and pages a particular renderer supports. The [registry](../../templates/registry.json) declares five capabilities. Its [checker](../../scripts/check_template_registry.py) verifies the referenced files; it does not perform automatic content adaptation.

## Responsibility boundaries

| Layer | Owns | Concrete example |
| --- | --- | --- |
| Analytical knowledge | Evidence, driver, activity, opportunity, baseline and decision | Company package and strategic context |
| Editorial selection | Audience, argument, relevant claims and page story | [Exec writing](../../skills/hivest-portfolio-ai/references/exec-writing.md), fund note Markdown |
| Profile payload / binding | Exact fields required for the selected output | Exec JSON, value-chain view or pedagogical sheet |
| Scaffold and layout | Structure, typography, component placement and dimensions | Pedagogical HTML scaffold + CSS; exec Python composition + CSS |
| Output evidence | Actual file hashes, physical pages, geometry and review states | Render manifest, QA report and artifact receipt |

Content changes return to the content authority. Layout changes remain in the renderer/template layer. A new material claim returns to research and the applicable review gate.

## Effective profiles

| Profile | Input contract and composition | Output / dependency | Capability |
| --- | --- | --- | --- |
| `exec` | [Schema](../../contracts/three-pager-exec.schema.json), [page contract](../../templates/THREE_PAGER_EXEC_v0.3.md), [render_exec.py](../../renderers/three_pager_exec/render_exec.py) | HTML + manifest; `--pdf` invokes browser export and QA for PDF/three PNGs | `demo_only`; fixed 4 support + 5 primary activities and 5 drivers |
| `audit` | [Content schema](../../contracts/three-pager.schema.json), [template](../../templates/THREE_PAGER_PORTFOLIO_AI.md) | Content/freeze checks available as specified in [rule matrix](rules-and-validation.md); renderer absent | `schema_only` |
| `fund-note` | [Markdown/directives contract](../../templates/strategic-market-note.md), [build.py](../../renderers/strategic_note/build.py) | HTML/PDF and figure QA; its separate [setup](../../renderers/strategic_note/README.md) includes Mermaid CLI | `preview`; editorial workstream independent of company gates |
| `value-chain-preview` | [Variable-activity schema](../../contracts/value-chain-view.schema.json), [render.py](../../renderers/value_chain_preview/render.py) | Three-page HTML; browser PDF/PNGs, manifest and local artifact receipt with `--pdf` | `preview`; manufacturing and infrastructure/asset-service fixtures |
| `pedagogical-six-page` | [Sheet schema](../../contracts/pedagogical-sheet.schema.json), [landscape.py](../../renderers/pedagogical/landscape.py) | `binding.json`, scaffold, styled HTML, six landscape PDF/PNGs, Markdown and QA hashes | `preview`; Perception is the canonical JSON pilot |

All registry entries have `committee_authorized=false`. The current [value-chain implementation](value-chain-profiles.md) already renders previews. Cross-sector real-case acceptance and common narrative adaptation remain separate work.

## Source pins and reuse

The pedagogical renderer imports a pinned snapshot of Markdown composition, browser and QA helpers through [upstream-lock.json](../../renderers/pedagogical/upstream-lock.json). Preserved reference copies use their original relative links; the [reference map](../../skills/enterprise-ai-learning/references/README.md) resolves them against active source files. Editing those copies requires an explicit version/pin update; ordinary navigation corrections belong in the map.

## Remaining common adapter work

A shared narrative block contract, block→claim lineage, reusable side stories and retention checks across all formats are still open. The profile-specific pedagogical scaffold demonstrates one implementation; it is not a general cross-format narrative engine. A new output needs a versioned input contract, mapping, executable renderer, negative tests and reader acceptance before its registry capability can advance.
