---
name: enterprise-ai-learning
description: Concevoir des fiches pédagogiques approfondies « Pour aller plus loin » sur les cinq capacités IA en entreprise et leur combinaison, puis les rendre en six pages paysage. Utiliser pour les kits ambassadeurs Train the Trainer, l’exploitation d’un catalogue de cas et les approfondissements du programme de 17 piliers; travailler avec un seul contrat de contenu, un scaffold sémantique et un CSS séparé.
---

# Fiches IA — comprendre, transmettre, intégrer

## Lire juste ce qu’il faut

Lire le brief courant, le registre de sources et le catalogue fourni. Pour une fiche existante, lire son `<capacité>.sheet.json`; pour Perception, partir de `learning/enterprise-ai/perception.sheet.json`. Lire uniquement le [contrat actif](../../contracts/pedagogical-sheet.schema.json), le [template de six pages](../../templates/PEDAGOGICAL_SIX_PAGER_v0.3.md) et, au moment du rendu, la [recette de composition](references/composition-rendering.md).

Le JSON est le seul contenu canonique. Le Markdown est sa projection de lecture. Ne pas refaire trois bindings, un manifeste de scaffold et plusieurs reçus. Les anciens contrats des versions portrait restent des archives de compatibilité. Garder HTML dans le scaffold et CSS dans le design; ne pas enfouir un choix de mise en page dans les données.

## Boucle 1 — lire et répartir le corpus

Dédupliquer les pièces jointes par empreinte; conserver tous les numéros, situations et nuances. Attribuer une dominante selon le résultat attendu, puis garder les capacités complémentaires avec leurs conditions. Distinguer la lecture d’une entrée, son interprétation, la rédaction d’une sortie et l’action. Ne pas forcer une solution classique dans l’IA; une règle fixe ou un connecteur ne prouve pas l’agentique.

Lire les passages utiles du livre et noter chapitre/pages réellement lus. Ne pas republier le livre ni son extraction dans le dépôt. Pour les histoires d’entreprise, vérifier les sources primaires, dater les faits et signaler les résultats déclarés par un fournisseur ou le client. Ne pas inventer de gain pour remplir un quadrant.

## Boucle 2 — écrire une capacité, une page à la fois

Écrire et relire les six pages avant d’en commencer une autre. Garder les titres et transitions comme un récit :

1. **Comprendre** : définir sans jargon, aller de l’exemple simple au flux réel. Construire chaque posture TOWS à partir d’un facteur interne et d’un facteur externe. Séparer fait de l’histoire, lecture stratégique proposée et limite de preuve.
2. **Transmettre** : écrire un pitch oral de 30 secondes, un postulat, le parcours visuel, trois leviers honnêtes et des réponses aux objections. Donner une courte animation et un critère de compréhension.
3. **Diagnostiquer** : faire apparaître les cinq branches, leurs effets et dépendances. Associer obstacle, levier d’adoption, responsable et mesure; ne pas remplacer le schéma par cinq mots isolés.
4. **Intégrer** : préciser les sous-tâches, les entrées/sorties et frontières de capacité. Préserver Assistant/Copilot/Autopilot/Agent et les deux axes du livre. L’autonomie n’est ni une obligation ni une preuve de valeur. Si le syllabus manque, écrire un ancrage proposé sans numéro inventé.
5. **Relier à la valeur** : pour Logistique, Opérations, Marketing/Vente et Services, nommer l’interlocuteur qui porte le problème, la douleur, la question à poser, les cas, les briques et le résultat à mesurer. Expliciter la simplification de Porter et le rôle des fonctions support.
6. **Agir** : retenir 3–5 IDs stables du catalogue; relier Bénéfice, Avantage et Caractéristique. Donner une mesure, un contrôle, un positionnement intégration/automatisation et un prompt testable. Préserver le sens des scores : 1 faible, 2 moyen, 3 élevé; V/G favorables, C/R/X défavorables. Ne pas les additionner.

Pour la synthèse future, choisir au moins quatre contributions distinctes dans une chaîne réellement décrite. UC-069 est un candidat du corpus fourni. Ne pas inventer un mode manquant pour satisfaire le compte.

## Boucle 3 — composer, rendre, relire

Exécuter le renderer sur le fichier canonique et vérifier le vrai PDF paysage de six pages. Inspecter chaque page; corriger la structure ou le CSS pour un défaut visuel et revenir au JSON pour un défaut de fond. Garder une typographie lisible, remplir utilement la page et donner la priorité aux schémas qui expliquent. Ne pas étirer six paragraphes en six pages vides.

Ne pas inventer de visuel factuel ni de preuve. Un diagramme opérationnel est une construction pédagogique fondée sur les données de la fiche; les scores restent des hypothèses d’atelier. Distinguer contrôle automatique, revue visuelle et validation éditoriale. Livrer le PDF, un aperçu et le Markdown utile; conserver le catalogue complet hors du backlog resserré.

## Fermer la boucle

Vérifier : un débutant explique-t-il l’idée, une erreur plausible, un exemple métier et le prochain essai ? Le formateur peut-il reprendre l’animation ? Les quatre histoires ont-elles leurs sources et les cas leurs IDs ? Le rendu est-il paysage et dense sans réduire les polices ? Consigner seulement les améliorations réutilisables avant le tour suivant.

## Frontière du dépôt portefeuille

Travailler seulement dans le workstream pédagogique. Ne pas modifier `program/state.json`, les manifests d’entreprise ni leurs gates. La skill générique de référence est versionnée dans `achard-arnaud/skills-notes-and-storytelling`; le pilote conserve ses propres sources et sorties.
