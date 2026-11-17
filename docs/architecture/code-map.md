# Code map — execution boundaries

Use the Hivest workflow for programme sequencing and `skills/standalone-company-analysis/SKILL.md` for independent instances.

| Component | Capability | Boundary |
|---|---|---|
| Manifest and programme state | Scope, stage and next work | Independent runs use `program_ref=null`, outside Hivest roll-ups |
| Company package | Source, fragment and claim lineage | Public research may remain a draft |
| `research_graph.py` | Dependency context and affected nodes | No web research, graph initialization or automatic rewrite |
| Standalone analysis skill | Route a new case, create its own graph, compose three pages | Procedure only; no `Agent.py` orchestrator exists |
| Validators/renderers | Structural or render checks | No implied human approval |
