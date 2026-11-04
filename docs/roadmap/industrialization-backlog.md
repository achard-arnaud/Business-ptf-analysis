# Backlog d'industrialisation — priorités et sprints

**Établi** : 2026-10-13. **Statut** : demandes d'évolution, **pas** fonctionnalités livrées. Les issues GitHub sont l'autorité opérationnelle ; ce fichier fournit l'ordre, les dépendances et les critères de sortie.

## Principes

1. Préserver les règles de diagnostic, le statut PILOTS et les approbations humaines ; refactorings sous tests avant extension fonctionnelle.
2. Livrer par tranches verticales : contrat → fixture → validateur → tests de mutation → migration pilote → doc.
3. Rendre chaque gap falsifiable avec propriétaire de la vérité, entrée/sortie, conditions négatives, seuil de QA et décision de promotion.
4. Distinguer absence de spécification, code manquant, automatisation partielle et défaut de documentation. Aucun ticket n'est clos par une simple reformulation du README.

## Sprint 0 — stabilisation et inventaire (P0)

- S0-01 : cartographie exhaustive des contrats exécutables, manifests et dépendances (drift audit).
- S0-02 : gold fixtures réelles et négatives Sphere/STG + provenance (sans données privées).
- S0-03 : intégrer l'architecture ETL et navigation agent à la CI de documentation.
- S0-04 : test de non-régression des gates et états/approbations.
- S0-05 : matrice de couverture des tests structure / sémantique / rendu.

**Exit** : tests existants inchangés ; contrats réconciliés et artefacts de preuve d'exemple explicites.

## Sprint 1 — fiabiliser EXTRACT (P0)

- S1-01 : schéma source/snapshot/capture_kind, empreinte, droits, stockage externe et replay.
- S1-02 : schéma fragment atomique, locator, source-scope et qualité de citation.
- S1-03 : registre de claims typés, contradictions, changement de source et fraîcheur.
- S1-04 : graphe incrémental et invalidation des descendants avec NRT.
- S1-05 : politique de provenance de sources communes vs entreprises, dédoublonnage par origine.
- S1-06 : jobs/reprise bornés, intégrateur unique et conflits de versions.
- S1-07 : évaluation extraction de transcriptions/vidéos comme leads, non faits sans corroboration.

**Exit** : chaîne source → fragment → claim vérifiable, rejouable à partir d'une archive autorisée ; changements matériels identifiés.

## Sprint 2 — industrialiser TRANSFORM (P0/P1)

- S2-01 : contrat de Narrative Scaffold indépendant des templates.
- S2-02 : relation `narrative_block → claim → fragment → source` et contrôle de couverture.
- S2-03 : moteur de tension narrative, objection forte, contre-thèse et issue décisionnelle (sans génération magique).
- S2-04 : side stories typées, lineage, return/payoff, cycle candidate/validated/promoted/retired.
- S2-05 : seuils de claims, sélection/reranking, contradicteurs et anti-invention.
- S2-06 : contrôle des baselines non IA et tests de sensibilité aux unknown.
- S2-07 : séparer scaffold fonds, participation et outputs diagnostics.
- S2-08 : migrer un scénario Sphere et une note Hivest vers le contrat candidat.

**Exit** : mêmes claims rendent deux narrations distinctes et traçables, sans mélange d'états ni invention de chiffres.

## Sprint 3 — PUBLISH multiformat et QA (P1)

- S3-01 : registre de templates/profils (capacité réelle, version, lifecycle).
- S3-02 : blocs de contenu agnostiques et interface figée vers renderers existants.
- S3-03 : spécification HTML pivot et adaptateurs PDF/PNG ; DOCX/slides seulement après test.
- S3-04 : QA visuelle et rapport machine-ingérable (overflow, figures, fonts, orphan).
- S3-05 : gate de sortie contrôlant freeze, hash, allowed_for_committee et non-régression narrative.
- S3-06 : renderer audit manquant : décision build ou retrait du catalogue.
- S3-07 : fixtures E2E et CI de rendu avec baseline visuelle.
- S3-08 : comparaison inter-formats de la rétention des claims et side stories obligatoires.

**Exit** : double projection contrôlée avec manifeste de preuve inchangé ; aucun renderer ne renforce une affirmation.

## Sprint 4 — opérations, boucle d'apprentissage et réutilisation (P1/P2)

- S4-01 : versionner les contrats de handoff GPT/Claude/Gemini, compatibilités et fallbacks.
- S4-02 : dossier de session/anti-compaction, ownership, version locks et reprise de l'intégrateur.
- S4-03 : portail de suivi des questions, gates, captures, coûts et prochain travail.
- S4-04 : runbook conformité/droits/PII et vérification d'exfiltration.
- S4-05 : normaliser feedback → diagnostic de défaut → ADR → contrat → NRT → promotion.
- S4-06 : rollup portefeuille avec lineage, couverture et comparabilité inter-sociétés.
- S4-07 : démo reproductible Sphere + STG + Hivest distincte des résultats de production.

**Exit** : reprise sans perte de contexte, boucle de changement testée et démonstration auditable.

## Priorisation

P0 = empêche une conclusion/provenance/gate défendable ; P1 = empêche la réutilisation industrielle ou le multiformat ; P2 = optimisation d'exploitation. Les tickets ne doivent pas faire entrer de nouveaux déploiements ni modifier les scores sans preuve. Chaque sprint dépend des contrats et fixtures de son prédécesseur. Avancement réel : voir Issues ; la présence de cette roadmap ne vaut ni validation ni clôture.

## Tickets créés (13 octobre 2026)

- [Sprint 0 — Issues #5–#9](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues?q=is%3Aissue+%5BS0%5D) : 5 tickets de stabilisation.
- [Sprint 1 — Issues #10–#16](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues?q=is%3Aissue+%5BS1%5D) : 7 tickets extraction/provenance.
- [Sprint 2 — Issues #17–#24](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues?q=is%3Aissue+%5BS2%5D) : 8 tickets reasoning/narration.
- [Sprint 3 — Issues #25–#32](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues?q=is%3Aissue+%5BS3%5D) : 8 tickets publication/QA.
- [Sprint 4 — Issues #33–#39](https://github.com/achard-arnaud/Hivest-ptf-analysis/issues?q=is%3Aissue+%5BS4%5D) : 7 tickets opérations, reprise et feedback.

**35 issues ouvertes**. Les numéros représentent des tâches, non des commits, livraisons ou bugs déjà reproduits. Dépendances inter-sprints à maintenir lors de la planification ; aucun gate métier n'est modifié par cette roadmap.
