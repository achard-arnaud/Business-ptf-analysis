---
name: standalone-company-analysis
description: Independent company research and three-page analysis with a separate evidence graph created before research, outside Hivest.
---

# Independent company analysis

For every new company or use case outside Hivest:
1. Route by mandate. Hivest work stays in its own skill, state and gates; independent work never joins its roster or roll-ups.
2. Run `python scripts/case_runtime.py check`, then `init --case <case-id> --input intake.json` using template_id=three-pager-exec. The manifest creates isolated `data/cases/<case-id>/` state and graph before research. Begin/complete each A0–A4 stage with its emitted packet and I/O schema. Existing companies/ runs remain explicit historical instances; do not migrate or invent receipts.
3. Acquire dated primary sources; retain URL, date, scope, rights and locator. Keep short excerpts; connect claims to fragments; preserve contradictions. Distinguish facts, inferences, hypotheses, recommendations and unknowns.
4. Analyze business/economics → market/drivers → Porter chain → AI/Data maturity → backlog.
5. Compose page 1 profile/pitch, page 2 Porter, page 3 maturity/backlog. Keep evidence traceable. Never score internal maturity without internal evidence.
6. Update graph and manifest. Distinguish draft, structural check, human review and render. Never claim PDF/HITL/approval unless performed.

The repository graph script computes dependencies; it does not collect web research or initialize a graph. See `references/three-page-contract.md`.


## Binding, render et revue du PDF

Pour un pitch en trois pages d’une entreprise indépendante :
1. Après création du graphe et qualification des sources, créer un payload distinct au format `THREE_PAGER_PORTFOLIO_AI`, profil `exec`, rattaché à cette instance. Le payload est la source de vérité des libellés, des chiffres, des conclusions et des références.
2. Créer un manifeste de binding qui relie l’instance, le graphe, le payload, la version du contrat, le renderer, les sources par page et les livrables. Le binding doit être écrit avant le rendu.
3. Rendre avec le renderer HTML/Chromium canonique `renderers/three_pager_exec/render_exec.py`; les fallbacks historiques conservent leur provenance. Aucun nom d’entreprise, programme, conclusion ou exemple métier ne doit être injecté en dur dans le renderer ; toute variante de page est portée par le payload.
4. Vérifier le contrat JSON, la cohérence du récit entre pages, les renvois graphe→sources→claims→pages, le nombre de pages et les débordements. Lire visuellement chaque page exportée en image et consigner les constats.
5. Faire trois revues consignées : conformité au contrat et aux preuves ; hypothèse alternative la plus forte ; utilité décisionnelle et limites. Corriger puis relancer les contrôles si une revue échoue.
6. Marquer explicitement le statut comme brouillon public relu, sans approbation métier. Une revue de rendu ne vaut ni validation de la direction ni preuve de maturité interne. Garder les inconnues explicites.

Les profils de présentation plus génériques peuvent être utilisés seulement si leur contrat prend en charge le modèle d’activité. Ne pas employer un profil synthétique de démonstration pour publier l’analyse d’une entreprise réelle.


## Executable I/O authority
Read [case process](../../docs/agent/case-process.md) and `workflow/case-process.json`.
Stage contracts, context hashes and actual event logs are enforced by `scripts/case_runtime.py`.
Use the canonical HTML/Chromium renderer for new PDFs; historical fallback PDFs retain provenance.
For an incident, pass a state/evidence-pinned proposal to loopback. It checks the BUILD hypothesis,
ADR/objective/constraints and observed-vs-unknown measurements; it does not approve an analysis.
