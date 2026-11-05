# Checkpoint 07 — Revue finale G10

Date : 5 novembre 2026  
État : prêt pour revue humaine; les PR restent en draft, aucun merge vers dev ou main.

## GitHub

| Dépôt | PR | Head | État |
|---|---|---|---|
| skills-notes-and-storytelling | #172 | 8565f785e5a47076a56a5b65fc140d1fbf6168f0 | draft, mergeable, validate success |
| Business-ptf-analysis | #62 | 0b630cf2fc6828b5e6954f90e638555216055e19 | draft, mergeable, validate success, select-render success, render-qa success |

La branche du programme conserve son isolation du workflow Hivest. Le dernier contrôle visuel déclenché vérifie des rendus historiques du dépôt; il ne crée pas de PDF des nouvelles fiches.

## Contrats et contenu

- Taxonomie product / business / tech / pedagogique déclarée dans le manifest générique.
- Cinq fiches de capacité et une synthèse; six pages par module; six boucles et checkpoints.
- Binding et scaffold utilisent 24 IDs de blocs, projetés en 28 slots de page; aucune déclaration de CSS.
- Schéma séparé pour le catalogue élargi, liens de sources et règles de dédoublonnage.
- BAC, étoiles, matrice automatisation/intégration et prompts de prototypage présents.
- Source map liée au livre; les textes sont reformulés.
- 17 piliers : contenu et niveau 2 raccordés de façon provisoire, faute d'IDs syllabus.

## Ce qui reste humain

Relire les fiches, confirmer les liens exacts aux 17 piliers, choisir le renderer et effectuer la QA visuelle; ensuite décider si les PR peuvent sortir de draft et être intégrées. La présence d'une CI verte ne remplace aucune de ces décisions.
