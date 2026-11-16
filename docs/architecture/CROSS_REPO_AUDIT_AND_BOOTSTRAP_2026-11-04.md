# Audit croisé — industrialisation du diagnostic en trois pages (04/11/2026)

**Portée :** analyse du dépôt `Hivest-ptf-analysis` comparée aux contrats publiés sur la branche `dev` de `Candidatures-nice`. Les constats décrivent des fichiers et capacités observables ; les chantiers sont des **propositions**, pas des changements de runtime effectués. L'exemple GreenYellow reste une analyse extérieure, sans GO_DRAFT.

## Décision d'architecture

**Conserver une skill métier** avec lectures conditionnelles, contrats de preuve et gates séparés du rendu. Renforcer la découverte, les états, le registre des templates et les reçus ; éviter un second moteur, une skill par framework ou un bus externe imposé.

| Boucle | Forces locales | Emprunt ciblé à Candidatures-nice | Gap / priorité | Epic |
|---|---|---|---|---|
| 1. Agents / skills | Routeur `AGENTS.md` léger ; skill unique et procédures conditionnelles | Entrées d'intention, `bootstrap-run`, discovery `.agents/`, lint de liens et frontmatter | Bootstrap/capability receipt non testé en session vierge ; P1 | [#41](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/41) |
| 2. Multi-template / objets | Schémas audit v0.1, exec v0.3 ; render_exec, liens de preuve | Catalogue de manifests, `process_adapter.status`, schema & renderer réellement prêts | Aucune autorité centralisée de capacités ; Porter 4+5 et 5 drivers figés ; P1 | [#42](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/42) |
| 3. Contexte | Checkpoint 12 claims, trois unknowns, source hashes, intégrateur unique | `run-context`, `process_pins` (hash garanties), `next_action`, invalidation | Enum RunContext sans `MARKET_CONTEXT` / `OPPORTUNITIES` ; P0 | [#44](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/44) |
| 4. Runtime/assets | Archives hors Git, hashing, GO_DRAFT explicite, QA de rendu | `PUBLISHING` (receipt & readback), `BUS` (transit ≠ ACK), CI par impact | Pas d'enveloppe d'artefact transversale/ACK durable ; P1 | [#46](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/46) |

## 1. Agents et skills — rester explicite sans multiplier les agents

**Autorités :** `AGENTS.md` = routeur ; `skills/hivest-portfolio-ai/SKILL.md` = workflow métier ; `references/workflow.md` = étapes, entrées/sorties ; procédures `evidence`, `market-drivers`, `diagnostic`, `opportunities`, `review`, `composition`, `learning` chargées à la demande. `research-graph` et `exec-writing` seulement sous condition.

Transfert : `AGENTS.md` de Candidatures ne porte ni les instructions A1–A4 ni le détail de test/CI ; `.agents/skills/*/SKILL.md` est un **wrapper de discovery** vers la compétence canonique `workflow/skills`. Son `scripts/check_skill_links.py` contrôle liens, frontmatter et chemins, **sans prouver que l'agent suit la route**.

**Stratégie bootstrap :** (1) intention, (2) état de programme, (3) identifiant entité et manifest, (4) résumé de capacité de la session (GitHub lecture/écriture, archive, navigateur, Python), (5) seule phase active, (6) contrat/fixture utile, (7) preuve/reçu de continuation. Distinguish `READY`, `RECOVERABLE` et `BLOCKED` sans créer un nouveau gate métier.

Gates : session vierge, absence d'archive, skill non découvrable, path cassé, relecture inutile des autres sociétés. Owner [#7](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/7), [#33](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/33), [#39](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/39).

## 2. Multi-template et objets — preuve indépendante de la présentation

Le renderer exécutif `renderers/three_pager_exec/render_exec.py` est effectif ; le renderer audit annoncé par `contracts/three-pager.schema.json` n'est pas implémenté. Le contrat exec v0.3 impose `drivers[5]`, quatre activités support et cinq principales ; ces choix sont éditoriaux **propres à une topologie** et ne doivent pas devenir une ontologie universelle.

**Séparation cible :**
- Objet durable : `source → fragment → claim → driver → business_activity → opportunity → decision`, avec source, périmètre et état de preuve.
- Vue éditoriale : `scaffold → argument_block → profile/template → rendered page`.
- Manifest : `template_id/version/lifecycle/profile/capability/schema/renderer/QA/permissions`, calculé sur l'existant, pas basé sur l'énumération du README.
- Deux topologies tests : chaîne industrielle manufacturière (Sphere) et contrats/actifs/financement (GreenYellow). Aucune migration in-place du v0.3 sans compatibilité.

Cas externe : `examples/three-pagers/greenyellow/{analysis,three-pager}.md` conserve mécanisme économique, alternatives sans IA, risques et inconnues. Il est **interdit** d'en déduire un `companies/greenyellow` ou un manifest de portefeuille.

Owner [#25](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/25), [#30](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/30), nouveau [#43](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/43).

## 3. Context engineering — hydrater une décision, pas le dépôt

**Défaut concret :** `docs/agent/gates.md` et workflow acceptent `MARKET_CONTEXT` et `OPPORTUNITIES` ; l'enum `stage` de `contracts/run-context.schema.json` les rejette. Il faut corriger la contradiction par une migration de contrat testée, pas uniquement éditer un paragraphe.

**Bootstrap profond, séquence conditionnelle :**

```text
L0 - intent / route / legal scope (public vs entité)
  ↓
L1 - program/state + manifest entité + INDEX court
  ↓
L2 - stage actif, owners et contrats JSON affectés
  ↓
L3 - source registry + top 12 claims décisifs / contre-preuves + 3 unknowns
  ↓ seulement si le gate / la décision l'exigent
L4 - source originale / fragments / graph descendants / revue sectorielle ciblée
  ↓
L5 - checkpoint (hashes, scopes, stage, artefacts, next_action, HITL)
  ↓
L6 - composition / renderer / QA après autorisation de phase
```

**Stratégie de récolte:** établir une question décisionnelle et un cutoff ; indexer marché/secteur séparé des claims société ; récolter d'abord les sources primaires et leurs captures autorisées, puis les contradictions. Chaque recherche reçoit un budget, un owner, un stop condition, des identifiants réservés et un résultat source→fragment→claim. S'arrêter dès que l'incertitude restant ouverte exige un accès interne ou un pilote ; ne pas remédier à un manque de preuves par plus de prose.

**Invariants :** aucun changement de scope silencieux (groupe/filiale/site), aucun `null → zéro`, pas de consentement inventé, aucun nouveau modèle ne fusionne des claims sans source. Après mutation, invalider les seuls descendants ; les modifications de présentation ne périment pas les preuves factuelles.

Owner [#5](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/5), [#8](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/8), [#13](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/13), nouveau [#45](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/45).

## 4. Runtime, assets, publication — ne jamais confondre les succès

Le pipeline réel : `validate_bundle` vérifie une archive autorisée, `validate_exec` limite la démo et interdit le comité, `render_exec` crée HTML/PDF/PNG, `qa.py` contrôle le rendu. La CI `contracts.yml` exécute les unitaires au push/PR ; le rendu navigateur est **manuel** (`workflow_dispatch`). Ainsi, un passage CI habituel n'atteste pas la QA visuelle d'un nouveau rendu.

**Receipts et statuts séparés :**
1. `artifact_integrity`: octets effectivement capturés et empreinte SHA-256 ;
2. `publication`: prepared / published_unverified / published_verified / blocked ;
3. `content_validity`: schema valid, semantic reviewed, unknowns ouverts ;
4. `render_qa`: not_run / failed / passed sur payload précis ;
5. `authorization`: demo_only / HITL-approved / committee_authorized.

Un fichier externe n'est pas une archive persistante garantie ; une écriture retournant `OK` n'est pas un ACK durable. Test de relecture distante avec sha attendu/observé, sous une classe de visibilité et une politique de droits. N'engager ni S3, ni event bus, ni migration du stockage avant preuves de nécessité.

**Tests à coût maîtrisé :** doc-only→liens ; modif schéma/contrat→NRT de gates/invalidation ; renderer/CSS→3 PNG et layout ; publisher/writer→concurrence+readback ; impact inconnu→NRT élargies. Ne jamais remplacer `not_run` par `pass`.

Owner [#10](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/10), [#29](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/29), [#31](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/31), nouveau [#47](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues/47).

## Backlog consolidé et ordre recommandé

| Séquence | Ticket(s) | Raison et résultat de sortie |
|---|---|---|
| **P0-1** | #45, #8, #5 | Un seul enum d'étapes, tests de transitions, pas de reprise incohérente |
| **P0-2** | #7, #33, #39 | Navigation et capability bootstrap contrôlés, checkpoint portable |
| **P1-1** | #25, #30, #43 | Manifest multi-template, renderer réel et topologies métier distinctes |
| **P1-2** | #10, #29, #47 | Assets/archives, receipt vérifiable, décision HITL préservée |
| **P1-3** | #28, #31, #6 | QA ciblée, fixtures réalistes et NRT mutation |
| **P2** | #17, #18, #23, #36 | Scaffold agnostique, composition et loopback, après stabilisation de la preuve |

**Facteur limitant :** aucune mesure des lectures réelles, du coût en tokens ni de la robustesse intermodèles n'a été exécutée dans cet audit de dépôt distant. Les bénéfices de contexte et CI sont des hypothèses à mesurer.

## Discipline d'implémentation

1. **Un ticket / une branche / une PR / un propriétaire du contrat**, dans l'ordre de dépendance ; pas de merge parallèle de deux changements de state machine.
2. Tests positifs + négatifs proches des artefacts du ticket ; promotion du contrat seulement avec migration de version quand nécessaire.
3. Rejouer les pilotes existants avant d'accepter une nouvelle topologie de template. Les exemples externes testent la lecture métier, jamais une approbation du programme.
4. Un checkpoint de sortie `paths + SHA + tests exécutés + statut gate + unknowns + next_action` suffit ; ne pas déposer un transcript ou une copie de tous les documents dans le repo.

## Sources croisées

- Dépôt actif : `AGENTS.md`, `skills/hivest-portfolio-ai/SKILL.md`, `references/workflow.md`, `contracts/*.schema.json`, `docs/agent/*`, `renderers/three_pager_exec/*`, `.github/workflows/contracts.yml`.
- Dépôt comparatif : `Candidatures-nice/AGENTS.md`, `workflow/skills/bootstrap-run/SKILL.md`, `workflow/skills/run-context/SKILL.md`, `scripts/process_pins.py`, `config/templates.json`, `templates/manifests/*.json`, `workflow/PUBLISHING.md`, `workflow/TESTING.md`.
- Documentation externe : [Skills — OpenAI](https://developers.openai.com/api/docs/guides/tools-skills), [AGENTS.md vs skills — GitHub](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review), [OpenAI — rationaliser les instructions et skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

**Statut du présent document :** design/revue, aucun changement de programme, schéma, skill, renderer ou gate.
