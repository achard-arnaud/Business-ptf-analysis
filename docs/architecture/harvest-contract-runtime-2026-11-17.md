# Harvest et écarts : contrats, runtime et renforcement — 17 novembre 2026

Format : repo-harvest/v1. Mandat : comparer Candidatures-nice, Business-ptf-analysis et storytelling ; implémenter les écarts qui empêchent un réemploi propre. Profil : François-Pro. Autorisation : diagnostic, issues et corrections demandés dans cette session.

## Baselines et couverture

| Source | Version examinée | Parcours et fichiers discriminants |
| --- | --- | --- |
| Candidatures-nice | bd58411e6187012695d05a573ea8d919d22c0579 | docs/ADR-007-RUN-BUILD.md ; workflow/process.json et process-manifest.json ; loopback-manifest.json ; scripts/run_context.py, process_loopback.py, loopback_journal.py, run_lifecycle_plan.py ; run-loopback/SKILL.md |
| Business-ptf-analysis | 86ca3dce840497233c20688b8d0bfbbfeb6f1c99 | AGENTS ; standalone skill ; run-context schema ; research_graph ; session_checkpoint ; render_independent_company_runs ; CI et suite tests |
| storytelling main | 41fa280db407f2311e9f62f5b191fd39fa94062a | AGENTS ; SKILL ; manifest modes/templates ; ADR-1004/1005 ; src et scripts ; schémas claims |
| storytelling dev | d490ddf (SHA complet conservé dans Git local) | delta main…dev : 25 commits ; fonctions de business brief, route réglementaire et contrat éditorial. Le runtime root installé reste absent également de dev. |
| skill installée | empreintes de release dans workflow/engine-release.json | SKILL, runtime et profils quatre couches, src/runtime.py, note_runtime.py, schémas et tests ; changements validés dans son checkout personnel |

Lecture statique ciblée des sources Candidatures : aucun script métier exécuté, aucune donnée de candidature transférée. Inventaires GitHub non tronqués. Échantillon : ces parcours, pas l'ensemble du dépôt. Transfert d'invariants et de mécanismes abstraits ; pas de reprise de code Candidatures. Les sources primaires sont les fichiers aux SHAs ci-dessus.

## Hypothèses concurrentes et lectures discriminantes

| Question | Alternatives | Preuve | Résultat / limite |
| --- | --- | --- | --- |
| L'init indépendante existe-t-elle ? | initializer actif / instruction seulement | scripts, AGENTS et skill | à la baseline Business, instruction manuelle ; research_graph ne crée aucun cas |
| Les étapes sont-elles exécutables ? | machine d'états complète / validateurs indépendants | scripts, I/O et tests | packages/contextes/rendu contrôlés ; aucun consommateur ne lie la nouvelle instance à A0–A4 |
| L'absence de loopback est-elle totale ? | aucun / documents et backlog / moteur | #36, docs et scripts | principe présent et backlog ouvert ; pas de reçu de proposition exécuté pour le cycle courant |
| La divergence storytelling vient-elle de dev ? | runtime en dev / seulement installé | ls-tree main/dev, fichiers installés | runtime root et profils installés absents des deux branches ; dev porte d'autres travaux à préserver |
| Une inconnue peut-elle rester sans preuve ? | statut fidèle / schéma force un fragment | claim.schema fragment_ids.minItems | minItems=1 pour tout statut ; corrigé conditionnellement, sans fabriquer une source |

## Écarts et livraison

| Gap | Impact et contrainte | ADR / issue | Réponse vérifiable |
| --- | --- | --- | --- |
| Nouvelle instance déclarative | mélange de contextes, dépendances invisibles ; cas isolés exigés | Business ADR-0002 / #73 ; storytelling ADR-1008 / #338 | init exclusif, graphe avant collecte, data/cases ignoré, pins, tentatives, refus des sauts |
| Frontières preuve/claims/prose | provenance et mapping non contrôlés au fil du run | mêmes ADR ; #12/#18 restent portées métier plus larges | schémas par étape, nodes/edges typés, provenance et mapping conservés ; citations explicites hors mapping rejetées |
| Logs / dépendances | on confond acte déclaré et appel observé | ADR-0002 / #73 | état atomique verrouillé, events horodatés, paquets, hashes ; Python/jsonschema/pypdf observés ; tokens inconnus |
| Renforcement confondu avec conformité | bug réparé sans diagnostic mesurable réutilisable | Business ADR-0003 / #74, parent #36 | loopback cinq axes, hypothèse/falsifier/ADR/issue, preuve hachée, lectures JSON avant/après ; aucune mutation automatique |
| Drift source/installation | exécution non reproductible selon la surface | storytelling ADR-1008 / #338 | même release d'engine et contrats ; helper evidence runtime rapatrié ; templates source conservés ; wrappers/alias explicités |
| Persona technique = liste de formats | absence de décision et de criticité dans l'I/O | storytelling ADR-1008 / #339 | 4 piliers, 7 profils de décision, un moteur ; sections par type, mesures observées/estimées/inconnues, Adopt conditionnel |
| Tests insuffisants | tests de happy path et conformité locale | mêmes issues, CI | CLI réelle + cas négatifs : sources non lues, contexte/capture modifiés, chaîne affaiblie, références étrangères, compte rendu de mesure faux |

## Architecture retenue et limites

Les ADR deviennent prescriptifs sur des refus testables. Un seul engine partage les mécanismes ; chaque dépôt garde ses bindings de template. La copie de release est hachée et vérifiée avant une nouvelle instance et en CI. Un package externe n'est pas introduit : coût d'exploitation non justifié à ce stade. Le déclencheur d'extraction est une divergence répétée ou un coût de maintenance mesuré.

Le chemin exécuté est intake → A0 source/capture → A1 fragment/claim/edges → A2 scaffold → A3 écriture → A4 revues et reçu PDF si requis. L'agent effectue recherche, raisonnement, écriture et lecture visuelle. Le moteur contrôle la soumission et ses dépendances ; ce n'est pas un agent autonome et il ne prouve pas toutes les lectures de l'hôte. Aucun statut métier historique n'est promu.

Le run et le BUILD partagent un dépôt mais pas leurs répertoires ni leurs mutations : nouvelles données dans data/cases, méthodes/contracts/tests versionnés. Le journal conserve chaque tentative et rejet. L'invalidation conserve les octets historiques et remet les descendants à pending. Une évolution de méthode ne rebinde pas silencieusement un run épinglé ; la migration automatique reste absente.

La QA de graphe ne prouve pas la vérité des faits ; un fragment marqué verified reste une déclaration attribuée à l'agent. Le contrôle de citation explicite vérifie les IDs, pas les paraphrases implicites. La preuve d'une lecture scoped exige des locators explicites dans le helper de bundle. Une critique sémantique continue de relever des trois revues.

La CI bloque les ruptures structurelles, pas les mauvaises décisions. Un verdict technique reste proposé. Aucun budget en jours-personnes, TCO, ROI ou token fournisseur n'est inventé ; les mesures absentes restent nulles. Les autres épics historiques ne sont pas clos par cette livraison bornée.

## Prochaine décision

Après preuve de transfert et CI verte, fermer uniquement les quatre tickets au périmètre livré. Garder #36 comme parent de promotion/calibration plus large, et #44 pour les migrations/contextes métier encore ouverts. Ne pas annoncer l'exécution A0–A4 rétroactive de Square : son incident sert de preuve d'investigation, son PDF et ses revues restent ceux du run historique.


## Couverture complémentaire et évaluation

Storytelling `dev` d490ddf97f76e0c4d94af8ea72b3dbfc70494ab8 a aussi été comparé à main : 25 commits d’avance, sans src/runtime.py ni scripts/note_runtime.py. Ses ajouts réglementaires et contrats éditoriaux sont des travaux distincts à conserver dans leur branche. La convergence ne suppose pas leur promotion implicite.

L’évaluation indépendante du processus est consignée dans [le reçu](evaluations/case-process-forward-receipt.md) et [ses hashes](evaluations/case-process-forward-receipt.json). Le scénario ne rend aucun PDF ; il vérifie A0–A4 avec refus/reprise et un mémo Trial à mesures inconnues. Les régressions unitaires supplémentaires contrôlent une région scoped valide et les mesures observées hachées.

## Précisions de version et de rendu

Le dev storytelling observé au SHA d490ddf97f76e0c4d94af8ea72b3dbfc70494ab8 est 25 commits devant main ; il contient une extension réglementaire et un handoff business-brief. Ces changements ne sont pas imputés à cette livraison. Ils restent conservés dans la validation d’intégration. Les I/O du moteur et leurs cinq hashes sont identiques entre les deux dépôts et la skill installée ; chaque surface garde ses wrappers et bindings de templates.

Le nouveau chemin entreprise possède un appel render réel : payload A3 validé et épinglé → adapter canonique invoqué → logs et reçu → contrôle A4. Les profils de notes sans adapter déclaré refusent le rendu au lieu de prétendre l’exécuter. Les renderers externes et la migration des anciens cas demeurent hors de cette livraison.
