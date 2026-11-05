---
name: enterprise-ai-learning
description: Produce six-page beginner-friendly enterprise AI “Pour aller plus loin” sheets and Train-the-Trainer kits from a supplied course corpus, maintaining separate evidence, content binding, semantic HTML scaffold and visual rendering.
template_class: pedagogique
template_type: ai-enterprise-learning-six-page
---

# Skill locale — programme IA en entreprise

## Rôle et frontière du programme

Cette skill spécialisée produit les modules de [learning/enterprise-ai](../../learning/enterprise-ai/README.md). Elle complète la skill générique de six pages du dépôt [skills-notes-and-storytelling](https://github.com/achard-arnaud/skills-notes-and-storytelling/tree/8565f785e5a47076a56a5b65fc140d1fbf6168f0/skills/pedagogical-ai-learning), sans modifier les gates du diagnostic de portefeuille Hivest.

Lire le manifest et le registre de sources, puis travailler strictement dans cet ordre : Prédiction, Perception, Création, Raisonnement, Agentique, Synthèse. Terminer une fiche avant d'entamer la suivante. Le binding, le scaffold HTML et le rendu CSS restent trois artefacts distincts.

## Contrat des six pages

1. **Comprendre** — définition sans jargon, pourquoi, trois exemples progressifs, matrice TOWS : offensive (forces × opportunités), défensive (forces × menaces), opportuniste (faiblesses × opportunités), préservation (faiblesses × menaces).
2. **Transmettre** — pitch d'environ 30 secondes, postulat, diagramme, conviction par l'urgence, le soulagement d'une douleur et la facilité d'un premier essai; objections sans promesse excessive.
3. **Diagnostiquer** — Ishikawa/mindmap : Processus, Outils, Compétences, Données et Gouvernance; expliciter leurs relations.
4. **Se projeter** — Assistant → Copilot → Autopilot/Agent; séparer petit fruit accessible, gain rapide et pari majeur; lien niveau 2 / 17 piliers seulement si l'ID de syllabus est connu.
5. **Relier à la valeur** — logistique, opérations, marketing/vente et services; relier douleur, rôle porteur, tâche et enablers à la chaîne de valeur. Ne pas inventer une particularité sectorielle.
6. **Agir** — 3 à 5 cas, positionnés sur automatisation × intégration, avec BAC, étoiles et prompt concret. Conserver les IDs du backlog élargi non retenus dans le manifeste du catalogue, pas dans le texte de la fiche.

## Cadre de preuve et sécurité

- Utiliser SRC-BOOK-01 à 04 avec un locator exact. « Thinking » est le libellé source associé à « Raisonnement » dans cette série.
- Étiqueter faits du corpus, inférences pédagogiques, hypothèses et recommandations; ne jamais attribuer au livre les cadres conçus pour ce programme.
- Les notes sont ordinales : 1 faible, 2 moyenne, 3 élevée. Valeur et généricité élevées sont favorables; coût, risque et complexité élevés appellent davantage de prudence. Les hard gates passent avant toute notation.
- Les prompts de démonstration utilisent des données fictives ou anonymisées et n'autorisent ni décision sensible ni action réelle.
- Rattacher chaque page à un objectif d'apprentissage et à un takeaway qui prépare la page suivante.
- Aucun CSS, token de marque, règle de pagination ou choix de renderer dans le binding ou dans cette skill.

## Contrôles avant transmission

Valider six pages exactement, présence de chaque bloc attendu, cohérence des IDs entre binding et scaffold, traçabilité source, légende des étoiles, BAC développé, au moins trois cas distincts et un prompt testable. Faire une contre-lecture apprenant : « une personne débutante peut-elle expliquer l'idée, donner un exemple, nommer une limite et proposer une première mesure ? »

La revue visuelle est une étape externe et séparée après gel du contenu.
