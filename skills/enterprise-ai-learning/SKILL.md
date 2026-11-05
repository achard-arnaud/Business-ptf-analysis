---
name: enterprise-ai-learning
description: Produce and render six-page enterprise AI learning sheets from existing Markdown using the imported Hivest composition, theme, browser QA and artifact-manifest mechanism. Use for pedagogical adaptation, Train-the-Trainer kits and Markdown-to-PDF/PNG generation while preserving sources and content.
---

# Skill locale — programme IA en entreprise

## Rôle et frontière du programme

Cette skill spécialisée produit les modules de [learning/enterprise-ai](../../learning/enterprise-ai/README.md). Elle complète la skill générique de six pages du dépôt [skills-notes-and-storytelling](https://github.com/achard-arnaud/skills-notes-and-storytelling/tree/eecfb6f690b2ce60f39193a376f625c71d8eb0a1/skills/pedagogical-ai-learning), sans modifier les gates du diagnostic de portefeuille Hivest.

Lire le manifest et le registre de sources, puis travailler strictement dans cet ordre : Prédiction, Perception, Création, Raisonnement, Agentique, Synthèse. Terminer une fiche avant d'entamer la suivante. Le binding, le scaffold HTML et le rendu CSS restent trois artefacts distincts. Pour appliquer le rendu Hivest aux Markdown, suivre [composition-rendering.md](references/composition-rendering.md) : import de conversion et de thème, projection en six pages, PDF/PNG et QA liés aux vraies sorties.

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

La revue visuelle suit le rendu des vrais Markdown; elle reste distincte du contrôle du fond.


## Rendu appliqué aux Markdown

Lire la procédure [composition-rendering.md](references/composition-rendering.md), adaptée des procédures Hivest importées. Lancer le renderer sur un module, contrôler ses six pages physiques, lire ses PNG puis appliquer aux suivants. Le moteur CSS vit dans renderers/pedagogical, hors du binding. Une QA verte ne valide pas le contenu.

## Cycle repris et adapté de la skill Hivest

L'original importé est conservé dans [upstream-hivest-skill.md](references/upstream-hivest-skill.md). Le mécanisme opératoire adapté suit : Markdown revu → binding et empreinte → scaffold → HTML → PDF et PNG → QA automatisée → inspection visuelle → retour ciblé.

Le renderer consomme les Markdown actuels. Un défaut de mise en page retourne à la composition; un changement de fond retourne à la revue du Markdown, puis renouvelle l'empreinte du binding. Lire un seul module à la fois, fermer sa boucle de rendu, puis passer au suivant. Le statut de sortie est preview tant que le contenu pédagogique n'a pas été validé.

## Second tour : produire et prouver

Partir de la racine du dépôt contenant la skill et les Markdown. Pour un module existant, suivre le parcours de projection décrit dans la référence de composition : conserver les sources, les scores et les inconnues; ne pas prétendre reconstruire le binding éditorial ni sa chaîne de claims. Produire séparément `binding.json` (projection), `scaffold.html` (sans CSS), puis `fiche.html` (CSS appliqué), PDF et six PNG.

Exécuter le vérificateur sur la source et le dossier de sortie. Il doit rejeter un fichier modifié après rendu, une source périmée, un import altéré ou une QA en échec. Inspecter ensuite les six pages; conserver `reader_review=PENDING` dans le rapport automatisé et consigner la lecture humaine séparément. Une réussite technique ne transforme ni les liens provisoires au syllabus ni le contenu candidat en contenu approuvé.

Utiliser une seule convention de score : 1 faible, 2 moyen, 3 élevé; valeur/généricité élevées favorables, coût/risque/complexité élevés défavorables. Refuser notes hors 1–3, page vide et backlog hors 3–5 cas. Corriger le Markdown pour un défaut de fond, le scaffold/CSS pour un défaut visuel; ne pas réduire la typographie pour masquer un débordement.
