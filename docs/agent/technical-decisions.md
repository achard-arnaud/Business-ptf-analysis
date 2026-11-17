# Sharp CTO : type de décision et criticité

Le format, la décision et la criticité sont indépendants. Une décision peut devenir
une note d'architecture, un benchmark ou un mémo bref. Choisir le type dans
`config/technical-decisions.json`, puis le template. Réutiliser le même graphe et
le même processus A0–A4 ; ne pas créer de skill par mémo.

| Pilier | Type | Ce qui doit être examiné |
| --- | --- | --- |
| Choix et risques | rupture-adr | Frontière, alternatives, hypothèses falsifiables, sortie |
| Choix et risques | debt-risk | Dette, SPOF, estimation de remédiation et risque accepté |
| Économie | migration-tco | Inaction, bascule, horizon TCO, retour et sensibilité |
| Économie | ecosystem-impact | Contextes bornés, dépendances produits, duplication, propagation |
| Industrialisation | bootstrap-dx | CI bloquante, ownership des contrats, données/secrets, limites |
| Industrialisation | run-readiness | Objectifs de service, observabilité, dégradation, reprise |
| R&D | poc-verdict | Protocole, performance/DX, limites, verdict Adopt/Trial/Hold/Kill |

```bash
python scripts/technical_decision.py profile migration-tco
python scripts/technical_decision.py validate memo.json --case <case-id>
```

Le mémo suit `contracts/technical-decision.schema.json`. Une section porte des preuves
ou des inconnues explicites. Les options sont comparées sur le même objectif et les
mêmes contraintes. Les hypothèses ont un falsifier et un protocole de vérification.
Un chiffre est observé, estimé ou inconnu ; une estimation garde son unité, ses
hypothèses et sa provenance. Ne jamais inventer des jours de dette ou un ROI.

Les mesures du contrat acceptent une unité et une valeur nulle pour une inconnue.
Exemples de mesures utiles : jours-personnes de remédiation, coût par période, temps
de bascule, délai de récupération, coût/requête et temps de tâche. Déclarer l'horizon
et le périmètre dans la section concernée ; une comparaison de chiffres de périmètres
différents ne prouve aucun gain. Les guardrails portent un seuil et un comparateur.
`Adopt` exige que tous les seuils explicités passent sur mesures observées. `Trial`
peut être retenu avec des inconnues, assorti du prochain test et de son arrêt.

Criticité : reversible, material ou structural. Une décision structurelle requiert
une preuve ADR ; ce contrôle impose la trace, pas l'acceptation de l'ADR. Le contrat
vérifie identité, références, empreintes et logique des seuils. Le CTO juge la causalité,
la pertinence des seuils et le risque résiduel. La revue métier reste distincte.

Une mesure observed inclut reading={evidence_id, pointer} vers une valeur numérique dans une preuve JSON hachée ; le validateur compare effectivement cette valeur. Les estimations sont sourcées et restent distinctes.
