# ADR-0003 — Loopback fondé sur traces et expériences bornées

- Date : 2026-11-17.
- Statut : mise en œuvre autorisée dans cette session, sans délégation d'approbation métier.
- Objectif : corriger architecture, bugs, CI, runtime et contrats de skills à partir des incidents.
- Contraintes : ne pas transformer une observation en cause démontrée ; ne pas inventer de gains ; conserver les preuves et l'état du run.
- Issue : [#74](https://github.com/achard-arnaud/Business-ptf-analysis/issues/74), livraison bornée de la boucle #36.

## Décision

Le loopback reçoit un cas/version, un état haché, des preuves locales hachées, l'objectif/contraintes, les ADR concernés, leur disposition (cohérent, à challenger ou inconnu) et l'issue. Il route vers cinq axes d'investigation : architecture, bugfix, ci, runtime, skill. Ce sont des questions de diagnostic distinctes de la conformité du livrable.

Le résultat est `no_change` ou une proposition d'expérience : hypothèse, falsifier, protocole, régression, arrêt et rollback. Les mesures avant/après portent une unité. Les mesures observées doivent correspondre à des valeurs lues dans des preuves JSON hachées ; les inconnues sont nulles. Le validateur ne déduit pas la causalité de ces valeurs.

Le BUILD autorisé applique la correction à la première couche fautive, exécute le cas de rupture et le cas de transfert, puis relie résultat et commit à l'issue. Un ADR cohérent conduit à corriger son implémentation ; une hypothèse invalidée conduit à proposer sa révision avec alternatives. La procédure ne mute ni le run, ni les skills, ni GitHub automatiquement.

## Alternatives et critères

Une liste libre de leçons ne permet pas le contrôle des références et de la mesure. Une réparation automatique des méthodes depuis chaque incident généralise trop vite. Le reçu de proposition validé est retenu : faible dépendance technique, diagnostic attribué et promotion séparée. Coût : conserver des traces courtes, les tests et la relation ADR/issue.

## Hypothèse falsifiable et vérification

Hypothèse : les incidents significatifs fournissent assez de traces pour distinguer hypothèse et correction vérifiée. Si la preuve de run ou de dépendance manque, la conclusion reste inconnue et l'expérience doit d'abord instrumenter. Si deux cas indépendants contredisent la correction proposée, rouvrir l'ADR et la régression de transfert.

Contrôles exécutables : schéma loopback, `case_runtime.py loopback`, tests de preuve périmée, mesure inventée et absence de mutation. Les contrôles ne prouvent pas le sens du diagnostic ; une cause demeure déclarée et sourcée. La livraison ne remplace pas toute la portée de #36 (promotion méthodologique et calibration restent supervisées).
