# Composition puis rendu — profils audit et exec

**Contrat local.** Entrée : dossier revu, décision, bundle/claims et profil audit ou exec. Sortie : payload/manifest traçables puis trois pages et QA visuelle selon les gates du profil ; aucune fixture ne vaut preuve. **Suite :** [learning.md](learning.md) après rendu revu, ou retour ciblé à [review.md](review.md) si fond modifié. Pour le profil exec, charger [exec-writing.md](exec-writing.md). Contrat complet : [workflow.md](workflow.md).

Choisir le profil avant de composer : `audit` suit `contracts/three-pager.schema.json` v0.1 et exige GO_DRAFT, gel, puis rendu final. `exec` suit `contracts/three-pager-exec.schema.json` v0.3, `references/exec-writing.md` et `templates/THREE_PAGER_EXEC_v0.3.md`. Une démonstration exec peut partir d'un bundle validé non gelé ; le manifeste porte le statut de preuve et les gates ouverts. Ne jamais inférer qu'un payload de démonstration valide le bundle.

Pour exec, rédiger figures canoniques → activité et Porter → cinq drivers → trois à cinq thèmes et transformation → renvois et quadrant → gouvernance et posture → thèse et conclusions. Contrôler la cohérence, le schéma, trois pages sans débordement, puis lire les trois PNG à 100 %. Aucune taille de police réduite pour absorber un débordement. Les pages exec n'affichent ni IDs internes ni statut de gate ; celui-ci reste dans le payload et le manifeste.

## Profil audit
Entrer seulement après GO_DRAFT sur le dossier hashé. Réutiliser fragments → claims graph light → rerank → scaffold → fill → sourcing → contre-perspective → reader QA. Une side story ne crée pas de claim. Ne pas charger le corpus complet.
Lire le contrat THREE_PAGER_PORTFOLIO_AI du dépôt et le schema. Une idée dominante par page, preuve et implication adjacentes, inconnues visibles. Les rubriques obligatoires restent présentes même non documentées. Mapper chaque élément matériel à ses claim_refs.
Valider puis figer payload_sha256 ; renderer prend uniquement le payload gelé. Garder versions et hash dans manifeste de rendu. Le renderer ne mène pas de recherche, ne modifie ni score ni recommandation. Toute lacune matérielle revient en REOPEN_TARGETED.
Produire HTML/PDF/PNG hors code. Exécuter les contrôles trois pages, tailles, overflow et inspection visuelle des trois pages. Si layout impose une modification de fond, revenir au contenu et renouveler le gate si matériel.
Template candidat jusqu'au loopback des deux pilotes. Ne jamais présenter des tests structurels comme une QA visuelle de rendu.

Appliquer le gate marché/drivers de `market-drivers.md` ; conserver la traçabilité source externe → exposition entreprise → driver → stratégie de valeur → opportunité → page.

