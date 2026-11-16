# Évolution des contrats

Les entrées datées ci-dessous décrivent leur version d’origine. Pour le comportement courant, suivre la [matrice règles/validateurs](../docs/architecture/rules-and-validation.md) et la [carte du code](../docs/architecture/code-map.md). `validate_freeze` fournit désormais un chemin bibliothèque pour le contenu v0.2 ; le renderer audit reste absent. Les schémas et les gates ne changent pas dans cette revue documentaire.

## 0.3.0 (profil de présentation exec candidat)

Le contrat `three-pager-exec.schema.json` et son renderer ajoutent une projection C-level distincte du contenu audit v0.1. La fixture Sphere permet la non-régression de la composition ; ses sources et son bundle ne sont pas certifiés dans ce dépôt. Le manifeste marque donc `UNVERIFIED_DEMO`. Les gates de diagnostic et de diffusion restent ouverts, et le profil audit ne change pas.

## 0.2.0 (candidat)

Le package exige `market_context` et `drivers`, avec couverture des six axes, liens des use cases aux drivers, mécanismes de valeur, classe technique et conditions d'arrêt. Les packages 0.1.0 restent validables pour historique mais ne satisfont pas la nouvelle étape marché. Une migration automatique ne peut pas inventer signaux, expositions ou preuves : acquisition et revue humaines sont nécessaires avant de déclarer un package 0.2.0 conforme.

Le schéma de contenu reste en 0.1.0 jusqu'à la définition de la projection marché sur les trois pages et du renderer. `validate_content` ne peut donc pas certifier le gel d'un package 0.2.0 pour l'instant. Un PASS de `validate_package` ne certifie pas le rendu.

Décisions ouvertes : seuils de maturité >=3 appliqués à toutes les dimensions ; inférences ancrées obligatoires ; sources partielles incompatibles avec confiance haute si seules origines ; enveloppe de valeur en sensibilité et preuve déclarative non mises en production.


## Complément Sphere —23/09/2026
Intégration conservatrice du contexte stratégique,graphe et rôles/ML. Le package réel respecte market_context/drivers. Les captures sont des extraits déclarés ; Sphere reste RESEARCH au gate originaux. Les garde-fous de hash global/unknowns sont préparés, mais la projection contenu v0.2 reste non certifiable tant que le contrat renderer demeure0.1. Aucun GO_DRAFT attribué.
