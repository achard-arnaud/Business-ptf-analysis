# Architecture de bout en bout — Extract / Transform / Publish

**Statut** : cartographie du dépôt réel + architecture cible explicitement signalée. **Dernière revue** : 2026-10-13. **Portée** : Hivest Portfolio AI ; la note stratégique du fonds est une branche éditoriale distincte.

## 1. Modèle conceptuel

L'analogie ETL est un contrat de frontières, pas une promesse d'automatisation intégrale.

```mermaid
flowchart LR
 Q[Question et entité] --> E[EXTRACT<br/>Sources - snapshots - fragments - claims]
 E --> G[(Graphe de preuve<br/>source / claim / analysis / question / output)]
 G --> T[TRANSFORM<br/>drivers - diagnostic - décisions]
 T --> N[Scaffold narratif<br/>CIBLE: contrat distinct]
 N --> P[PUBLISH<br/>payload - template - renderer]
 P --> R[HTML / PDF / PNG + QA]
 R --> L[Loopback<br/>défaut - cause - règle - test]
 L -.question ciblée.-> Q
 H[GO_DRAFT / HITL] --> P
 T --> H
```

La **chaîne de preuve** reste source → fragment → claim → analyse → décision → contenu gelé. Un graphe est une indexation du raisonnement, une carte mentale est une vue, le rendu est une projection. La source primaire ne se trouve jamais dans un PDF généré.

## 2. Extract : questions, captures et unités de connaissance

Entrées : `program/state.json`, manifest entreprise, cutoff, décision à éclairer, trois inconnues susceptibles de modifier le verdict, anciennes preuves. La procédure canonique est `skills/hivest-portfolio-ai/references/evidence.md`, avec `research-graph.md` uniquement lorsqu'une question, un handoff ou une reprise l'exige.

Pour chaque source : conserver URL, publication et consultation séparées, auteur/organisme, scope groupe/filiale/site, juridiction, type et droits ; archiver l'artefact autorisé hors Git ; calculer le SHA-256 sur les **octets réellement capturés** et déclarer `capture_kind`. Un extrait n'est pas un original complet. Les fragments ont locator et citation ; les claims atomiques sont typés, datés, attribués, contradictoires si nécessaire. Grades A–E : classes de sources, pas probabilités.

**Exemple de séparation multi-entreprises :** une annonce d'éditeur prouve une capacité offerte ; elle ne prouve pas que Sphere ou STG utilise cette technologie. `wiki/` stocke le mécanisme sectoriel, `companies/<id>/` le claim strictement local. `program/roster.json` indexe les participations. Une absence de preuve correspond à `null` et à une question, jamais à un score 0.

Le graphe typé contient `source/claim/analysis/question/output` et liens `supports/depends_on/contradicts/answers`. Changement d'une preuve → descendants invalidés, pas réécriture générale. Le budget de contexte initial est de 12 claims critiques + contre-preuves, extensible si les contradictions l'exigent. Exécution parallèle : même cutoff, IDs réservés, sorties séparées, **un** intégrateur autorisé à promouvoir les connaissances.

Sorties : `package.json`, `evidence/`, registre, `research_graph.json` quand disponible, couverture négative et questions bloquantes. Vérifier les schémas, hashes et règles d'archive ; **ne pas** confondre un PASS structurel avec une certification de la vérité.

## 3. Transform : de l'évidence à la décision

Le workflow réel : `market-drivers` → `diagnostic` → `opportunities` → `review`. Les chaînes doivent rester auditables :

- Marché → segments → exposition **vérifiée** de la participation → mécanisme économique → driver.
- Activités et chaîne de valeur → diagnostic (8 dimensions + outils analytiques utiles) → opportunité → baseline non IA / NO-ACTION.
- Hard gates → priorisation argumentée sans total automatique → trois revues contradictoires → décision HITL datée.

Un **scaffold narratif transversal** est à construire : il n'existe pas encore de fichier contractuel unique utilisable pour tous les formats. Le template `strategic-market-note.md` décrit déjà lecteur, décision, thèse, drivers, objection forte, chaîne du métier, preuve et budget de pages. `exec-writing.md` fixe les trois pages du diagnostic exec. Le futur contrat doit conserver au minimum : `audience`, `decision_question`, `central_thesis`, `tension`, `argument_blocks[]`, `counterclaims[]`, `side_stories[]`, `evidence_refs[]`, `allowed_formats[]`, `review_state`.

**À ne pas implémenter en douce** : le scaffold cible n'est ni un schéma JSON existant ni une nouvelle autorisation de publier. Il doit faire l'objet d'issues, de schémas, validateurs, fixtures et gates.

## 4. Publish : contenu gelé et projection multiformat

```mermaid
sequenceDiagram
 participant A as Agent composeur
 participant C as Contrats / claims
 participant H as Relecteur humain
 participant R as Renderer
 participant Q as QA
 A->>C: Valider provenance + payload + profil
 C-->>A: Écarts et artefacts validables
 A->>H: Soumettre décision et inconnues
 H-->>A: GO_DRAFT ou retour ciblé
 A->>C: Freeze du payload + hash si profil final
 A->>R: Payload validé + template + paramètres
 R-->>Q: HTML / PDF / PNG + manifeste
 Q-->>A: QA automatique + inspection visuelle
 A-->>H: Livrable et limites de publication
```

**Profil diagnostic** : audit (schéma mais renderer audit absent) ou exec (`render_exec.py` réellement disponible). **Note fonds** : renderer distinct `renderers/strategic_note/build.py`, format C-level 5–7 pages, Mermaid, typographie et QA. Le renderer n'a le droit ni de renforcer un claim ni de modifier une recommandation. Une réduction de police pour cacher le débordement n'est pas une correction.

Une projection HTML pivot inter-formats (PDF, DOCX, slides) est un **objectif**, non une capacité commune disponible aujourd'hui. Séparer contrat de blocs narratifs, spécification de présentation et moteur cible.

## 5. Où se trouvent les autorités ?

| Sujet | Autorité | Ne pas substituer |
|---|---|---|
| Programme et statut | `program/state.json`, manifests | README, ancienne note, existence de PDF |
| Gates et choix | `contracts/decision-rules.md`, `docs/agent/gates.md` | Prompt agent, design du renderer |
| Données | `contracts/*.schema.json`, packages validés | Notes librement rédigées |
| Workflow | `skills/hivest-portfolio-ai/references/workflow.md` | Ordre alphabétique des fichiers |
| Recherche et reprise | `evidence.md`, `research-graph.md`, `context-and-resume.md` | Chat précédent ou résumé approximatif |
| Narration / rendu | `templates/`, `exec-writing.md`, `renderers/` | Preuve canonique et gates |

## 6. Différences entre les deux branches métiers

Le programme **participation** mesure maturité, chaîne de valeur et opportunités avant de composer un rapport contrôlé ; son état est dans `program/state.json`. La **note stratégique du fonds** est un workstream de discussion et de recrutement, avec journal de recherche, gap register, contrat éditorial et renderer dédiés : `companies/hivest/INDEX.md`. La PR #4 y produit une V2 candidate de 6 pages. Son succès de mise en page ne clôture aucune décision de diagnostic.

## 7. Processus de reprise et cycle d'amélioration

```mermaid
flowchart TD
 S[Reprise par agent] --> M[État + manifest + index]
 M --> K{Hashes et cutoff inchangés ?}
 K -- Oui --> A[Une seule étape active]
 K -- Non --> I[Invalider descendants affectés]
 I --> E[Recherche ciblée, puis intégration]
 E --> A
 A --> V[Valider schéma + preuve + décision]
 V --> H{Gate humain requis ?}
 H -- Oui --> W[Attendre autorisation explicite dans le dossier]
 H -- Non --> C[Checkpoint + prochaine procédure]
 W --> C
 C --> S
```

Le loopback documente **défaut → cause → nouvelle règle → contrat modifié → test de non-régression (NRT)**. Aucun agent n'attribue lui-même GO_DRAFT, DONE ou production_allowed.

## 8. Limites vérifiées / chantiers industriels

- Captation et promotion impliquent encore des procédures agent et une intervention humaine ; pas de scraping universel déclenché par simple présence d'une URL.
- L'existence de validateurs ne certifie pas la véracité d'une phrase, l'intégrité d'une source non archivée, la revue de marché ou la qualité pédagogique d'une narration.
- Le graphe sait calculer dépendances / descendants, mais le lineage sémantique complet **narrative_block → claim → fragment → source** doit être codifié et testé.
- Les sorties narratives multiformats, side stories structurées et contrats inter-modèles sont une proposition, pas une feature déjà livrée.
- La série d'issues dans [le backlog](../roadmap/industrialization-backlog.md) formalise ces changements sans réécrire le workflow existant avant validation.
