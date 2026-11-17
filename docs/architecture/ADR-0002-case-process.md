# ADR-0002 — Contrats exécutables de cas et frontière RUN/BUILD

- Date : 2026-11-17.
- Statut : décision de mise en œuvre autorisée par la demande de correction et de transfert de patterns de François dans cette session ; pas une approbation des analyses métier.
- Objectif : rendre une nouvelle instance isolée, reproductible et explicable.
- Contraintes : pas de Redis, pas de programme imposé, pas de migration silencieuse, recherche et jugement par l'agent, contrats vérifiés par Python.
- Issue : [#73](https://github.com/achard-arnaud/Business-ptf-analysis/issues/73). Épic contexte : #44.

## Constat et décision

Le code antérieur vérifie des packages, des contextes et un PDF final, mais AGENTS impose une initialisation manuelle. Un dossier et un manifeste déclaratif ne prouvent pas que les étapes ont eu lieu.

Adopter `workflow/case-process.json`, `contracts/case-artifacts.schema.json` et le consommateur `scripts/case_runtime.py`. Les nouvelles instances utilisent `data/cases/<case-id>/`, ignoré par Git. Le BUILD conserve méthodes, contrats, profils, tests, ADR et fixtures synthétiques. Les `companies/` historiques restent une route explicite ; ils n'acquièrent aucun reçu A0–A4 rétroactif. L'intake et le graphe vide sont créés avant la collecte.

| Frontière | Producteur | Contrat imposé au consommateur |
| --- | --- | --- |
| A0 acquisition | agent et outils de recherche | sources datées, capture locale, couverture lue/exclue/inconnue |
| A1 modélisation | agent | source → fragment → claim ; nodes/edges typés et provenance |
| A2 plan | agent | sections → claims, objection forte et falsifier |
| A3 écriture | agent | même jeu de sections et mapping de claims |
| A4 contrôle | agent, renderer et lecteur | trois revues distinctes ; PDF/QA hachés si demandés |

Le moteur initialise, commence, termine, inspecte et invalide une étape. Une dépendance non passée ou une empreinte périmée bloque. L'invalidation conserve les tentatives précédentes et affecte les descendants déclarés. Les paquets et le journal décrivent les appels reçus par le moteur ; ils ne prétendent pas observer la pensée du modèle ou toutes les lectures internes de l'hôte. Les instructions d'AGENTS et de la skill routent désormais vers ce consommateur.

## Options et objection

| Option | Coût et limite | Décision |
| --- | --- | --- |
| Renforcer seulement la prose | Peu de code, aucun refus déterministe des sauts ou données périmées | écartée |
| Ajouter un ordonnanceur autonome et une base distante | Exploitation et dépendances supplémentaires ; collecte encore spécifique | différée |
| Petit moteur local, contrats et profils | Maintenance de schémas et tests ; pas de vérification automatique du sens | retenue |

La meilleure objection est la duplication d'un moteur entre dépôts. Les copies sont une release identique hachée dans `workflow/engine-release.json` et contrôlée en CI, sans dépendance réseau en RUN. L'extraction en package se réexamine à la première divergence de comportement ou coût de maintenance observé.

## Prescriptions, falsification et limites

Bloquants : saut d'étape, capture modifiée, contexte altéré, référence hors cas/tentative, mauvais type de relation, fait sans fragment vérifié, mapping changé à l'écriture et reçu de rendu incohérent. Tests : `tests/test_case_runtime.py`. La CI doit exécuter `case_runtime.py check` et les tests, pas seulement valider le JSON.

Hypothèse falsifiable : un moteur de frontières manuelles suffit pour garantir la traçabilité technique des étapes. Réexaminer si un run contourne ces frontières, si une lecture nécessaire n'est pas dans le paquet ou si plusieurs écrivains perdent un état. Responsable : mainteneur du processus. Toute évolution des pins impose un nouveau cas ou une migration BUILD explicite ; aucun rebind automatique n'est livré.

Une CI verte ne prouve ni l'exactitude des claims, ni l'exécution de recherches non enregistrées, ni une approbation métier. Les compteurs de tokens fournisseur restent inconnus si non exposés.
