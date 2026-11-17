# Agent router — choose the active company-analysis route

Select the workflow from the user's mandate before reading programme state.

1. **Hivest portfolio mandate:** read `program/state.json`, one company manifest/index and `skills/hivest-portfolio-ai/references/workflow.md`; apply Hivest gates.
2. **New independent company/use case:** use `skills/standalone-company-analysis/SKILL.md`. Initialize a distinct case through `scripts/case_runtime.py` before collecting sources; existing `companies/` folders are the historical route. Set `program_ref=null`; do not edit Hivest state, roster or roll-ups.
3. **Resume an independent instance:** follow its manifest, index and graph; preserve entity boundary and cutoff.
4. **Other request:** use `docs/agent/quickstart-map.md`.

The graph records dependencies, claims and questions. `scripts/research_graph.py` computes context and affected nodes; it does not collect web research, initialize graphs or author evidence. Do not claim unimplemented `Agent.py` capabilities. Keep facts, inferences, hypotheses, recommendations and unknowns distinct. Never translate lack of public evidence into a zero score.

Independent three-page output: page 1 company profile and thesis; page 2 Porter value chain; page 3 AI/Data maturity and prioritized workstreams.

The optional learning module remains separate from both company routes. See `docs/agent/quickstart-map.md`, `docs/architecture/code-map.md` and `docs/architecture/README.md`.


## Binding et revue avant PDF

Pour toute nouvelle instance indépendante, le graphe propre à l’entreprise est créé avant la collecte. Pour les restitutions en trois pages, utiliser le contrat `THREE_PAGER_PORTFOLIO_AI` et créer un payload et un manifeste de binding distincts à partir de cette instance. Rendre les trois pages depuis le payload avec le renderer du contrat ; ne pas reprendre les noms, conclusions ni exemples d’une autre instance. Avant dépôt, exécuter la validation du contrat et de cohérence, relire les trois pages rendues, puis consigner les revues preuves/contre-hypothèse/décision. Le statut reste brouillon tant qu’une approbation métier distincte n’a pas été donnée.


## New-case executable boundary
For new independent runs use `python scripts/case_runtime.py check`, then `init --case <id> --input intake.json`.
The active route is `workflow/case-process.json`; new RUN files live in ignored `data/cases/<id>/`.
Call begin/complete for A0 evidence, A1 typed graph, A2 scaffold, A3 composition, A4 review.
Each call consumes the emitted I/O/context packet; preserve pins, attempts and execution events.
Do not infer an old run completed these stages. Keep legacy programme gates and histories explicit.
For material incidents call loopback with the hashed proposal; diagnose architecture, bugfix, CI,
runtime or skill, then apply an authorized BUILD with regression proof and ADR disposition.
