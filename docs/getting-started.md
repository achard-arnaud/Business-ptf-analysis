# Getting started

### 1. Install the core dependencies

Use Python 3.11+ from the repository root. Core validation and the HTML demo do not require an LLM API key or private source archive.

```bash
git clone https://github.com/achard-arnaud/Business-ptf-analysis.git
cd Business-ptf-analysis
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_skill_docs.py
python scripts/check_template_registry.py
```

On Windows, activate with `.venv\Scripts\activate`.

### 2. Generate an executive HTML demo

```bash
python renderers/three_pager_exec/render_exec.py \
  tests/fixtures/exec/sphere_unverified_v0.3.json \
  /tmp/business-ptf-demo
```

Open the generated `.html` file. The same directory contains `render_manifest.json`; the fixture is explicitly **`UNVERIFIED_DEMO`**. This command exercises payload validation and composition, not real-world evidence verification.

For PDF and PNG output, install the browser dependencies and repeat with `--pdf`:

```bash
python -m pip install playwright
python -m playwright install chromium
python renderers/three_pager_exec/render_exec.py \
  tests/fixtures/exec/sphere_unverified_v0.3.json \
  /tmp/business-ptf-demo --pdf
python scripts/verify_render_evidence.py /tmp/business-ptf-demo --profile exec
```

Linux environments may also require Playwright system dependencies (`python -m playwright install --with-deps chromium`). Inspect all three PNGs; automatic layout success does not replace reader review. Use a writable local path instead of `/tmp/...` on Windows.

### 3. Inspect or resume an existing Hivest diagnostic

Read [AGENTS.md](../AGENTS.md), [programme state](../program/state.json), then **one** company’s manifest and index, followed by the active procedure in the [workflow](../skills/hivest-portfolio-ai/references/workflow.md). [Sphere](../companies/sphere/INDEX.md) is the most complete reference bundle; other companies may still be at intake.

```bash
python scripts/validate.py package companies/sphere/package.json
python scripts/validate_bundle.py companies/sphere
```

These commands check the accessible package/bundle; without an archive they do not establish that original sources were captured. With your own authorised external archive:

```bash
python scripts/validate_bundle.py companies/sphere --archive /path/to/archive.json
python scripts/check_prehitl.py sphere /path/to/archive.json
```

For an evidence-aligned executive render, supply **both** `--bundle companies/<id>` and `--archive /path/to/archive.json` with the matching payload. No validation command grants `GO_DRAFT`.

For a session that already has a checkpoint, follow the [cold-resume instructions](../docs/agent/context-and-resume.md#reprise-à-froid-par-commande-itération-39); the CLI checks the independently observed repository SHA and accessible pinned input bytes before returning `READY_TO_RESUME`.

### 4. Run the checks

```bash
python -m unittest discover -s tests -v
```

[Contract CI](../.github/workflows/contracts.yml) runs navigation, registry and unit checks. Its path selector invokes browser QA for affected rendering components, with a manual-dispatch option. [Pedagogical CI](../.github/workflows/pedagogical-render.yml) has its own path-filtered browser checks. Private archive capture, authenticated human decisions and actual cross-model transfer are outside those CI proofs.


## Runtime and configuration boundaries

| Task | Dependencies / inputs | Configuration surface |
| --- | --- | --- |
| Package/bundle checks, unit tests and HTML demo | [Core requirements](../requirements.txt), Python 3.11+ | CLI input/output paths; run from repository root. |
| Exec / value-chain PDF and layout QA | Playwright + installed Chromium + pypdf | `NICE_CHROMIUM_PATH` optionally selects an installed executable; otherwise the shared launcher uses Playwright's managed Chromium. |
| Strategic-note figures and PDF | Separate [renderer setup](../renderers/strategic_note/README.md); Markdown, Playwright, Pillow and Mermaid CLI for diagrams | `CHROME_PATH` selects the executable used for Mermaid figures. Its current default is an environment-specific `/opt/pw-browsers/...` path. `mmdc` must be on PATH; PDF export uses Playwright's browser. |
| Pedagogical pilot | [Renderer requirements](../renderers/pedagogical/requirements.txt), canonical sheet and catalogue | CLI paths, browser selection and [upstream lock](../renderers/pedagogical/upstream-lock.json). |
| Evidence-aligned diagnostic | Accessible company bundle and authorised external capture archive | Explicit archive path; no credentials or private archives belong in public Git. |

Dependency files currently specify version ranges. The strategic-note guide contains an environment-specific tested version example; a shared complete dependency/browser/font lock remains open work. Record your runtime and input hashes for a reproducible run. A clone alone does not provision an external archive or a usable browser.

## Adapt to another company or client

Choose the route from the mandate before opening or updating any programme files.

| Mandate | Starting point |
| --- | --- |
| **New independent company or use case** | Follow the [standalone analysis skill](../skills/standalone-company-analysis/SKILL.md) and [case process](agent/case-process.md). Run `python scripts/case_runtime.py check`, then `python scripts/case_runtime.py init --case <case-id> --input intake.json` with an intake conforming to the [case intake schema](../contracts/case-artifacts.schema.json). This creates the case and its graph under `data/cases/<case-id>/` before collection. Omit `program_ref` from the intake JSON; the runtime rejects undeclared fields. Do not register the case in Hivest. |
| **Hivest portfolio mandate** | Use the [Hivest workflow](../skills/hivest-portfolio-ai/references/workflow.md), programme state and company gates. Programme registration belongs only to this route. |
| **Resume an existing case** | For an isolated case, use `case_runtime.py status --case <case-id>` and its saved state. For an existing historical `companies/` bundle, use its manifest and index; do not re-initialise it or infer A0–A4 receipts from older artefacts. |

On the selected route:

1. Define the decision, entity, cutoff and rights boundary before collecting sources.
2. Build evidence and analytical objects against the [data dictionary](data/DATA_DICTIONARY.md) and current schemas. Keep shared sector observations distinct from company facts.
3. Select a [binding/profile](architecture/template-binding.md) whose model fits the business. The exec profile keeps its fixed Porter topology; the variable-activity profile remains a preview.
4. Validate the accessible files and required external captures, then obtain the applicable human review. Company registration and capability promotion are deliberate state changes.

There is no single client configuration file, general source connector framework, Docker service or one-command deployed application. The current runnable units are Python CLIs and agent-guided procedures. Client parameterisation, source credentials and a packaged replay environment require their own contracts and implementation.

## Reading failures and outputs

Validation tools generally emit JSON verdicts; rendering scripts may also emit subprocess/browser diagnostics. Capture stdout/stderr and retain the exact command, input version and environment when investigating a failure. This is a collection of CLIs rather than a central run/logging service.

| Symptom | First action |
| --- | --- |
| Python import missing | Activate the intended environment and install the requirements for that profile. |
| Browser launch fails | Check executable availability, browser installation and host capability; keep HTML-only validation separate. |
| `snapshot_integrity=not_checked_external_archive_required` | Supply the authorised capture archive for source-byte validation. |
| Resume returns `STALE`, `CONFLICT` or `BLOCKED` | Re-read independent HEAD and accessible pinned inputs; use [resume protocol](agent/context-and-resume.md). |
| Layout passes but no release authority | Complete the distinct reader, freeze and authenticated human release requirements in [publication preflight](agent/publication-preflight.md). |
