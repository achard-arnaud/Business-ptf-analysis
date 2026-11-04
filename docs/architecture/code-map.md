# Carte du code et autorité des contrats

Cette carte décrit les capacités réellement présentes. Le [workflow de la skill](../../skills/hivest-portfolio-ai/references/workflow.md) décrit la séquence métier et ses entrées/sorties ; [`AGENTS.md`](../../AGENTS.md) n'est que son routeur.

| Composant | Entrée → sortie | Limite |
|---|---|---|
| `program/state.json`, `companies/<id>/manifest.json`, `INDEX.md` | Programme et dossier → état et chemins pour la reprise | Les états ne sont pas calculés automatiquement depuis les fichiers |
| `contracts/company-package.schema.json`, `strategic-context.schema.json`, `run-context.schema.json` | Bundle v0.2, contexte et run → formes canoniques | Les schémas ne jugent pas la vérité |
| `scripts/validate.py` | Package JSON ou contenu FROZEN + package → PASS/FAIL | `content` exige GO_DRAFT et état FROZEN, pas DONE |
| `scripts/validate_bundle.py` | `package.json`, `strategic_context.json`, `research_graph.json`, artefacts hashés + archive facultative → diagnostic d'intégrité | Sans archive, snapshots externes non vérifiés ; avec archive, selon capture déclarée |
| `scripts/check_prehitl.py` | Entité + archive → PASS/FAIL de la politique de capture et présence du bundle | N'accorde pas GO_DRAFT |
| `scripts/research_graph.py`, `scripts/compose_dossier.py` | Graphe + cible → descendants/questions ; modules société → vue pré-HITL | La vue composée n'est pas une nouvelle preuve |
| `contracts/three-pager.schema.json`, `templates/THREE_PAGER_PORTFOLIO_AI.md` | Profil audit v0.1 → contenu à geler | Renderer audit absent de ce dépôt |
| `contracts/three-pager-exec.schema.json`, `templates/THREE_PAGER_EXEC_v0.3.md` | Profil exec v0.3 → payload et règles de narration | Une fixture est uniquement un test de présentation |
| `scripts/validate_exec.py`, `renderers/three_pager_exec/render_exec.py` | Payload exec + bundle/archive facultatifs → HTML, manifeste ; `--pdf` → PDF, PNG, QA | Démo vérifiée ≠ GO_DRAFT ; `--pdf` exige Playwright/Chromium ; revue PNG humaine |
| `.github/workflows/contracts.yml`, `tests/` | Push/PR → tests ; dispatch manuel → QA de layout de la fixture | CI n'a pas les archives externes ni la décision humaine |

`contracts/decision-rules.md` porte les règles de maturité, hard gates, sourcing et fin. Les JSON sont les formes vérifiées par le code ; les Markdown sont les consignes de jugement. Une modification de schéma implique validateurs et tests proches du contrat ; une modification éditoriale implique le profil de rendu concerné et ses trois PNG. Les documents historiques de `docs/` et les notes de `companies/` ne remplacent ni manifest ni bundle.

## Cartographie de responsabilité ETL (documentation, sans changement de runtime)

- **Extract** : `evidence.md`, `research-graph.md`, `package.json`, `research_graph.json`, archives externes et `scripts/validate_bundle.py`.
- **Transform** : `market-drivers.md`, `diagnostic.md`, `opportunities.md`, `review.md`, `strategic_context.json` ; `exec-writing.md` contribue à la construction narrative en composition.
- **Publish** : `composition.md`, profils et schémas associés, `renderers/three_pager_exec/` et `renderers/strategic_note/` (workstream fonds distinct), inspection PNG/PDF et manifests de QA.
- **Transversal** : `AGENTS.md` route, `program/state.json` et manifests fixent le gate, `context-and-resume.md` conserve les checkpoints ; `learning.md` boucle les défauts vers les contrats et les tests.

Le contrat de Narrative Scaffold commun, le graph de blocs narratifs et le moteur de publication multiformat restent des évolutions suivies dans [la roadmap](../roadmap/industrialization-backlog.md). Consulter [la vue E/T/P](end-to-end-etl.md) avant de proposer de nouvelles classes de code.
