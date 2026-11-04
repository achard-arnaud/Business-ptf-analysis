# Hivest — Portfolio Intelligence & Diagnostic OS

> **Guide d'entrée pour humains et agents — 13 octobre 2026.** Ce dépôt est un **système documentaire de recherche, de raisonnement, de décision et de publication fondé sur des preuves**. Il n'est ni un scraper autonome en continu, ni une usine de PDF sans contrôle, ni un système de recommandations fournisseurs.
>
> **Lire en premier :** [AGENTS.md](AGENTS.md) (routage) · [carte rapide](docs/agent/quickstart-map.md) (où aller) · [architecture E/T/P](docs/architecture/end-to-end-etl.md) (pourquoi et comment) · [workflow de la skill](skills/hivest-portfolio-ai/references/workflow.md) (contrat entrée/sortie et gates).

## 1. Modèle mental : Extract → Transform → Publish (ETL éditorial)

**EXTRACT — acquérir la connaissance.** Formuler les questions décisionnelles, chercher les sources, capturer les octets autorisés hors Git, référencer les locators, créer des fragments atomiques et des claims qualifiés, représenter leurs dépendances et leurs contradictions. La preuve suit : **source → fragment → claim**. Les sources communes vont dans un wiki sectoriel sourcé ; les observations locales restent dans chaque entreprise.

**TRANSFORM — raisonner et construire la narration.** Relier marché → exposition de l'entreprise → mécanisme de valeur ; reconstruire chaîne de valeur, drivers, maturité, opportunités et contre-analyses ; sélectionner une thèse et sa tension narrative, ses objections, les histoires latérales et la décision visée. La preuve suit : **claim → analyse → option/décision → scaffold narratif**. Le scaffold narratif inter-formats constitue une **cible d'évolution**, pas encore un schéma exécutable transversal.

**PUBLISH (LOAD) — distribuer une histoire validée.** Choisir profil, template et lecteur, composer le payload, valider les sources et les autorisations, rendre HTML/PDF/PNG et effectuer QA automatique + revue visuelle. La preuve suit : **contenu validé/gelé → payload → rendu et manifeste**. Le renderer **ne recherche, ne calcule une maturité, n'ajoute de faits ni ne change un arbitrage**.

Le mot ETL est une **analogie de responsabilité**, pas la description d'un batch entièrement automatisé. Le schéma du pipeline, les sorties réelles et les fonctions encore manuelles sont détaillés dans [l'architecture E/T/P](docs/architecture/end-to-end-etl.md).

## 2. Deux parcours complémentaires — ne pas confondre leurs gates

| Parcours | Lecteur/usage | Pilotage | Statut de preuve |
|---|---|---|---|
| **Diagnostic par participation (programme principal)** | Diagnostic IA, création de valeur et priorisation des opportunités par entreprise ; consolidation portefeuille | [skill unique](skills/hivest-portfolio-ai/SKILL.md) → [workflow](skills/hivest-portfolio-ai/references/workflow.md), 7 procédures | États et gates obligatoires : [program/state.json](program/state.json), manifest société, [gates](docs/agent/gates.md), GO_DRAFT humain et freeze pour sortie finale |
| **Note stratégique du fonds Hivest** | Note de discussion C-level de 5–7 pages et argumentation sur le CoE / investissement augmenté | [companies/hivest/INDEX.md](companies/hivest/INDEX.md), [contrat éditorial](templates/strategic-market-note.md), [renderer](renderers/strategic_note/README.md) | Workstream éditorial distinct ; la note V2 PR #4 est candidate ; sa production **ne ferme aucun gate** du diagnostic |

**État documenté du programme** : PILOTS, Sphere et STG ; `production_allowed=false` dans `program/state.json` au dernier état lu pour cette refonte. Toujours relire les JSON et les manifests ; ne jamais inférer un état de la présence d'un document, PDF, fixture ou ancienne note.

## 3. Route agent — les cinq lectures minimales

1. Lire [AGENTS.md](AGENTS.md), puis `program/state.json`.
2. Sélectionner **une** entité de [program/roster.json](program/roster.json) et lire `companies/<id>/manifest.json` puis `INDEX.md` si disponible.
3. Lire [workflow.md](skills/hivest-portfolio-ai/references/workflow.md) et ouvrir **une seule** procédure active parmi evidence, market-drivers, diagnostic, opportunities, review, composition, learning.
4. Charger [research-graph.md](skills/hivest-portfolio-ai/references/research-graph.md) seulement pour questions/reprise/intégration ; [exec-writing.md](skills/hivest-portfolio-ai/references/exec-writing.md) uniquement dans composition exec ; ouvrir les schémas ciblés, pas tous les dossiers.
5. Écrire un checkpoint borné : entité, cutoff, gate, entrée + hash, top claims et contre-preuves, inconnues critiques, sorties, validations/limites et prochaine question. Voir [contexte & reprise](docs/agent/context-and-resume.md).

Le contexte actif doit rester limité ; le dépôt ne transforme pas `AGENTS.md` en agent autonome. Le routeur peut déléguer un rôle de recherche, mais un agent unique peut exécuter successivement les procédures.

## 4. Pipeline opérationnel et handoffs

| Phase ETL | Procédure canonique | Livrable central | Retour / gate |
|---|---|---|---|
| Extract | `evidence.md` + `research-graph.md` conditionnel | `package.json`, `evidence/`, sources/fragments/claims, questions | Capture et scope vérifiés ; preuve critique manquante → recherche ciblée |
| Transform | `market-drivers.md` | `market_context`, `drivers`, `strategic_context.json` | Secteur ≠ observation entreprise |
| Transform | `diagnostic.md` | Chaîne de valeur, 8 dimensions, SWOT/VRIO/7S | Inconnu `null`, pas de moyenne fictive |
| Transform | `opportunities.md` | Use cases, risques, alternatives sans IA, hard gates | Gates avant classement et sourcing |
| Transform | `review.md` | Trois revues, dossier pré-HITL, décision humaine | GO_DRAFT final uniquement après arbitrage |
| Transform → Publish | `composition.md` + `exec-writing.md` si exec | Payload sourcé, hashes, manifeste | Freeze selon profil, schema/claims alignés |
| Publish → boucle | `learning.md` | Rendu QA + défaut→cause→règle→test | Retour borné et promotion humaine |

**Chaîne invariant** : source → fragment → claim → analyse → décision → contenu gelé → projection rendue. Le renderer n'est **jamais** une source de preuve.

## 5. Dossiers, vérité et artefacts

| Chemin | Propriétaire de la vérité |
|---|---|
| `program/` | Roster, phase globale, séquence pilotes → clusters → fonds |
| `companies/<id>/` | Manifest, index, package v0.2, analyses et preuves **de cette entreprise** |
| `wiki/` | Patterns sectoriels sourcés, réutilisables mais non promus en fait entreprise |
| `contracts/` | Schémas de données et règles de décision ; source de vérité des invariants |
| `skills/hivest-portfolio-ai/` | **Une** skill programme avec références métier conditionnelles |
| `docs/agent/` | Gates, contexte et protocoles de reprise |
| `scripts/` + `tests/` | Validateurs, composition pré-HITL, analyse des dépendances et tests |
| `templates/` | Contrats narratifs et profils de sorties |
| `renderers/three_pager_exec/` | Renderer réellement codé du profil diagnostic exec |
| `renderers/strategic_note/` | Renderer distinct de note C-Level Hivest |
| `docs/architecture/` | Carte de code et architecture ETL explicative |

Les originaux, captures brutes, données sensibles et sessions d'exécution restent **hors du dépôt public**, avec références et empreintes des octets effectivement conservés. Le package, l'index ou une mind map ne sont pas des preuves originales.

## 6. Conditions à ne jamais contourner

- `unknown/null` ≠ zéro ou absent ; une communication sectorielle ne valide pas un déploiement local.
- Chaque claim matériel a provenance, périmètre, date, limite et contradictions ; les affirmations fournisseurs restent attribuées.
- Cinq hard gates obligatoires avant priorisation : `data_rights`, `security_ot`, `human_control`, `ownership`, `feasibility`.
- GO_DRAFT est une **décision humaine datée** ; hash/freeze et QA de sortie sont distincts. Changement matériel → réouverture du contrôle.
- Un PDF ou un `PASS` de schéma ne certifie pas la véracité, l'archivage intégral ni la diffusion en comité.
- Respecter la frontière de preuves et les règles complètes de [decision-rules.md](contracts/decision-rules.md) et [gates.md](docs/agent/gates.md).

## 7. Démarrer et tester

Python 3.11+ :

    python -m pip install -r requirements.txt
    python -m unittest discover -s tests -v
    python scripts/validate.py package companies/sphere/package.json
    python scripts/validate_bundle.py companies/sphere
    python scripts/check_prehitl.py sphere /chemin/externe/vers/archive.json

Le contrôle `validate_bundle.py` sans `--archive` vérifie essentiellement schéma, fichiers et liens locaux ; l'archive est nécessaire pour contrôler les captures externes déclarées. `check_prehitl.py` applique en plus les exigences de capture des originaux matériels. Aucun de ces scripts ne donne seul GO_DRAFT.

**Démo de rendu exec (fixture non vérifiée)** :

    python renderers/three_pager_exec/render_exec.py tests/fixtures/exec/sphere_unverified_v0.3.json /tmp/hivest-exec
    python renderers/three_pager_exec/render_exec.py tests/fixtures/exec/sphere_unverified_v0.3.json /tmp/hivest-exec --pdf

La fixture Sphere est `UNVERIFIED_DEMO`, pas une preuve. Sur un nouveau payload aligné, fournir ensemble `--bundle companies/<id> --archive /chemin/externe/vers/archive.json` ; le statut reste conditionnel au gate humain. Revoir les trois PNG. Voir [code-map.md](docs/architecture/code-map.md).

**Note stratégique C-Level** : voir [README du renderer](renderers/strategic_note/README.md), [template](templates/strategic-market-note.md) et [index du fonds](companies/hivest/INDEX.md). Ce renderer est distinct du profil diagnostic exec.

## 8. Statut réel, cible et backlog

- **Existant** : routeur, skill unique, workflow séquencé, schémas de preuve, research graph, validations, payload exec, rendus spécialisés et certains tests.
- **Manuel / partiel** : collecte et promotion de preuves, relecture sémantique, décision humaine, composition de certains artefacts et QA visuelle.
- **À construire** : contrat narratif inter-formats, lineage automatique du récit vers les claims, projections réutilisables, gestion structurée des side stories, contrats inter-agents inter-modèles, tests de mutation/regression E2E et industrialisation.
- **Backlog priorisé** : [sprints et gaps](docs/roadmap/industrialization-backlog.md), suivis dans GitHub Issues. Ne pas présumer qu'une issue créée est implémentée.

Le principe : **capturer une fois, qualifier et relier ; raisonner pour plusieurs décisions ; publier en plusieurs formats sans perdre la provenance.**
