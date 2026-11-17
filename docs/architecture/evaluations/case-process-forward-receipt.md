# Rejeu final — reçu indépendant

Release SHA-256 : `8613215d6500351a85efc77edc039bdc3d7b872fa4e665b15956d3179b1f8d0d`. Les cinq fichiers de release correspondent à leurs empreintes. Aucun changement d’implémentation.

| Contrôle | Résultat |
|---|---|
| Preflight initial/final | contracts_pass ; 10 templates |
| Artefact exact : citation C2 hors mapping Q2 | Rejet A3, exit 1 : Prose cites a claim outside its section mapping |
| Artefact exact : fragments issus de zones scoped non lues | Rejet, exit 1 : F1–F4 locator outside explicitly read scoped regions |
| Happy path après invalidation/correction | A0–A4 passed ; A3 attempt 2 ; autres attempt 1 |
| Mémo Trial exact, mesures unknown/null | decision_contract_valid ; guardrails_pass=false |

Les deux entrées négatives ont été recopiées octet pour octet. Leurs hashes sont conservés dans receipt.json :

- `probe-original-A3-mismatch.json` : `8c803798dd7b412a2f76c42954cb141dafc6a4cf76f18e4ba4eaae6d0770abdd` ; copie identique : True.

- `probe-scoped-unread-region.json` : `6eb420173b5ad1c62c2f6c764fae1ec432762d150187a0933e1d974b33eacded` ; copie identique : True.

Le contrat des mesures a changé ; le happy path a donc été rejoué. Le mémo Trial original reste accepté sans reading pour les valeurs unknown/null. Aucun nouveau test de mesure observed n’a été ajouté : seuls les deux cas négatifs demandés et ce happy path ont été exécutés.

Limites : le contrôle scoped rejette ici le payload de couverture historique en liste, qui ne fournit pas les read_locators explicitement attendus par la nouvelle implémentation. Ce rejeu exact prouve son rejet, pas à lui seul tous les cas de couverture valide. A4 réutilise les revues synthétiques historiques attribuées au même agent, avec adaptation des seuls chemins de tentative ; aucune nouvelle revue indépendante. Rendering=false ; aucune mesure de renderer, vérité technique ou approbation métier.

État, contextes, essais rejetés et finaux exportés dans results/case/. Runtime et empreintes Python/dépendances figurent dans receipt.json. Utilisation fournisseur inconnue. Commandes exactes et sorties : commands.json.
