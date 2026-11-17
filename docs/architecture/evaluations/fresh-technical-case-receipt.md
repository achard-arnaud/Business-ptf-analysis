# Fresh synthetic technical forward evaluation

Result: A0–A4 all passed on attempt 1, revision 11. Trial proposed, reversible criticality; keeping current compared against Trial. No benchmark, latency/cost all null/unknown. `guardrails_pass=false`, `technical_truth_verified=false`, `decision_approved=false`, `business_approval=false`. No external writes, no real service calls. One-page text scope, not a rendered/physically checked page.

Fresh directory: `/workspace/scratch/c0515666b3f3/forward-technical-fresh`. Fresh skill copy from installed package; no implementation modifications. All 15 pinned BUILD files byte-identical to installed package. No prior run outputs read. Context packets and exact output paths are preserved at `skill/data/cases/forward-search/stages/A0..A4/attempt-1/context.json`.

Commands (cwd `forward-technical-fresh/skill`; all exit 0 unless noted):

```text
python scripts/case_runtime.py check
python scripts/note_runtime.py profile one-pager
python scripts/technical_decision.py profile poc-verdict
python scripts/case_runtime.py init --case forward-search --input ../intake.json
python scripts/case_runtime.py begin --case forward-search --stage A0 --actor manual_agent
python ../build_artifacts.py                 # exit 1; local helper attempted A1 output before begin; FileNotFoundError, no engine rejection
# Corrected helper to write only requested stage; implementation untouched.
python ../build_artifacts.py A0
python scripts/case_runtime.py complete --case forward-search --stage A0
python scripts/case_runtime.py begin --case forward-search --stage A1 --actor manual_agent
python ../build_artifacts.py A1
python scripts/case_runtime.py complete --case forward-search --stage A1
python scripts/case_runtime.py begin --case forward-search --stage A2 --actor manual_agent
python ../build_artifacts.py A2
python scripts/technical_decision.py validate data/cases/forward-search/stages/A2/attempt-1/memo.json --case forward-search
python scripts/case_runtime.py complete --case forward-search --stage A2
python scripts/case_runtime.py begin --case forward-search --stage A3 --actor manual_agent
python ../build_artifacts.py A3
python scripts/case_runtime.py complete --case forward-search --stage A3
python scripts/case_runtime.py begin --case forward-search --stage A4 --actor manual_agent
python ../build_artifacts.py A4
python scripts/case_runtime.py complete --case forward-search --stage A4
python scripts/case_runtime.py status --case forward-search
python scripts/case_runtime.py check
sha256sum workflow/engine-release.json workflow/case-process.json data/cases/forward-search/state.json ../note-technique.md
```

Blockers remaining: none for text-only execution. Real trial remains unexecuted and conditional on need, isolation, rollback, protocol and thresholds. Reviews are three separately documented lenses from the same evaluator, not independent approval. Mock `https://example.org/search` is only a synthetic source label; `fetched_at` explicitly means local intake timestamp.

SHA-256:

| Artifact | Hash |
|---|---|
| engine release | `d556dfae61d422347abd6fd7eec9dda8268ae95665021851f3248ef2667831a7` |
| workflow manifest | `686645486e084d5d3343719f855b2d88d5e638095b0f7adf784afa533aa27630` |
| final state | `254ae0b9f2b841b1c4329c2b6801cc99551998857ece73be5c4ed2bf041f7856` |
| note-technique.md | `a633a1a071e7a320820ea21fd6c40bd9caa9fda660cc32972ab639b244be4c16` |
| case_runtime.py | `5aff2d7fce757379e7225c5d1748a03daf8ed001cf0f18b5560fb44e0a427294` |
| technical_decision.py | `8a01014dcbab5e31f14da4c2bf5dec22d0a1b0ecd7fc149eedbaef35bb7bbab3` |

Full build hashes and stage output hashes are in state.json; release inventory in workflow/engine-release.json. Text length: 260 whitespace-delimited words.
