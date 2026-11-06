---
template_type: ai-enterprise-learning-six-page
template_class: pedagogique
version: 0.3.0
lifecycle: candidate
pages: 6
orientation: landscape
content_contract: contracts/pedagogical-sheet.schema.json
skill: skills/enterprise-ai-learning/SKILL.md
---

# Fiche pédagogique approfondie — six pages paysage

Utiliser un seul fichier de contenu `<capacité>.sheet.json` conforme au contrat actif. Les six pages gardent leur ordre et leur fonction :

1. **Comprendre** : définition lire/voir/entendre pour Perception, exemples progressifs, TOWS croisé avec quatre histoires sourcées et enseignements explicitement proposés.
2. **Transmettre** : pitch de 30 secondes, postulat, parcours visuel, urgence/douleur/simplicité, objections et animation réutilisable.
3. **Diagnostiquer** : diagramme à cinq branches Processus/Outils/Compétences/Données/Gouvernance, obstacles, leviers, responsables et mesures.
4. **Intégrer** : taxonomie opérationnelle, quatre types du livre (Assistant, Copilot, Autopilot, Agent), deux axes distincts et trajectoire d’apprentissage. Ne pas confondre autopilot et agent.
5. **Relier à la valeur** : quatre fonctions, interlocuteur métier, douleur, question d’entretien, situations, briques nécessaires, mesure et vigilance. Nommer l’adaptation simplifiée de Porter.
6. **Agir** : trois à cinq cas du catalogue, BAC explicite, matrice intégration/automatisation, scores 1–3 et prompt opératoire. V/G élevés favorables; coût/risque/complexité élevés défavorables. Aucun total arbitraire.

## Séparation et simplification

- **Contenu** : `contracts/pedagogical-sheet.schema.json` et `learning/enterprise-ai/perception.sheet.json`. Ce fichier contient les textes, sources, données des diagrammes et cas. Aucun HTML/CSS.
- **Structure** : builders sémantiques de `renderers/pedagogical/landscape.py` et enveloppe `landscape.html`. Produit `scaffold.html` sans CSS.
- **Design** : `landscape.css`, A4 paysage. Les chiffres ne changent pas pour tenir sur une page.
- **QA** : un seul `qa.json` réunit résultat des contrôles, empreintes et versions du run. Il ne vaut pas approbation du fond.

Les anciens contrats binding/scaffold/catalogue et le renderer portrait restent des compatibilités des versions 0.1/0.2; ne pas les charger pour cette version. Le Markdown de Perception est une projection lisible du JSON, générée par `--export-markdown`.

## Règles éditoriales

Un titre exprime une idée; le takeaway prépare la page suivante. Chaque tableau ou diagramme aide à expliquer une décision. Attribuer toute performance à sa source, au dispositif et à la date. Une posture TOWS appliquée à une entreprise reste une interprétation pédagogique. Aucun chiffre fournisseur ne devient le ROI de l’apprenant. Ne pas inventer de numéro parmi les 17 piliers en l’absence du syllabus.
