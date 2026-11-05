# Carte de navigation pour agents — Hivest

**Règle** : partir de `AGENTS.md` et `program/state.json`. Ne jamais charger le repo entier. Séparer diagnostic des participations et note stratégique du fonds.

## J'ai besoin de…

| Intention | Lire | Sortie attendue | Interdit |
|---|---|---|---|
| Reprendre une entreprise | `program/state.json` → `companies/<id>/manifest.json` → `INDEX.md` → `references/workflow.md` | Étape active, question critique, checkpoint | Inférer gate de la présence d'un rapport |
| Rechercher une preuve | `references/evidence.md` ; `research-graph.md` si reprise/questions | source → fragment → claim, couverture/inconnues | Déduire une installation locale d'une annonce éditeur |
| Faire un benchmark sectoriel | `market-drivers.md`, `wiki/`, claims locaux | driver + exposition datée + mécanisme | Promouvoir automatiquement un pattern sectoriel |
| Diagnostiquer | `diagnostic.md`, schémas concernés | chaîne, huit dimensions, analyses et `null` | Moyenner des inconnues |
| Prioriser | `opportunities.md`, `contracts/decision-rules.md` | use cases, gates, baseline non IA | Scorer avant hard gates |
| Relire et arbitrer | `review.md`, `docs/agent/gates.md` | trois revues et décision HITL | Auto-approbation |
| Rédiger 3 pages exec | `composition.md` puis `exec-writing.md` | payload sourcé, QA, PNG | Faire rechercher le renderer |
| Produire les fiches pédagogiques IA | `learning/enterprise-ai/README.md` → `manifest.json` → `sources.md` → skill locale | six fiches candidat, binding/scaffold distincts, correspondance au syllabus à confirmer | modifier les gates Hivest ou prétendre qu'un renderer existe |
| Rédiger note fonds 5–7 pages | `companies/hivest/INDEX.md` → `templates/strategic-market-note.md` → `renderers/strategic_note/README.md` | note candidate et QA, hors programme | Changer `program/state.json` ou le manifest |
| Modifier le code | `docs/architecture/code-map.md`, schéma/validateur/fixture/test concernés | PR avec tests et non-régression | Promettre une feature sur seule base du README |
| Transférer vers un autre modèle | `docs/agent/handoff-and-fallback.md` et `contracts/research-handoff.schema.json` | Paquet de relais borné, capacité/fallback et reçu | Déduire un accès ou un GO_DRAFT de la seule validation JSON |
| Préparer la prochaine étape | `docs/agent/context-and-resume.md` | checkpoint court, hashes, next, stop | Écraser archives ou états concurrents |

## Contrat de relais minimal

- Entité, cutoff, audience/decision_question et gate courant ;
- chemins + versions/hashes entrants ;
- 12 claims prioritaires et contre-preuves (étendre si conflit) ;
- trois inconnues pouvant changer la décision ;
- artefacts et validations effectivement réalisés + limites ;
- décision humaine requise, procédure suivante et condition d'arrêt.

**Note** : `research-graph.md` est un module conditionnel de la skill unique ; il ne transforme pas l'index en preuve. Les source captures raw restent hors Git.
