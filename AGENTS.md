# Agent router — choose the active company-analysis route

Select the workflow from the user's mandate before reading programme state.

1. **Hivest portfolio mandate:** read `program/state.json`, one company manifest/index and `skills/hivest-portfolio-ai/references/workflow.md`; apply Hivest gates.
2. **New independent company/use case:** use `skills/standalone-company-analysis/SKILL.md`. Create a distinct `companies/<entity-id>/` folder and a new research graph before collecting sources. Set `program_ref=null`; do not edit Hivest state, roster or roll-ups.
3. **Resume an independent instance:** follow its manifest, index and graph; preserve entity boundary and cutoff.
4. **Other request:** use `docs/agent/quickstart-map.md`.

The graph records dependencies, claims and questions. `scripts/research_graph.py` computes context and affected nodes; it does not collect web research, initialize graphs or author evidence. Do not claim unimplemented `Agent.py` capabilities. Keep facts, inferences, hypotheses, recommendations and unknowns distinct. Never translate lack of public evidence into a zero score.

Independent three-page output: page 1 company profile and thesis; page 2 Porter value chain; page 3 AI/Data maturity and prioritized workstreams. Do not introduce recruitment or candidate positioning unless explicitly requested.

The optional learning module remains separate from both company routes. See `docs/agent/quickstart-map.md`, `docs/architecture/code-map.md` and `docs/architecture/README.md`.
