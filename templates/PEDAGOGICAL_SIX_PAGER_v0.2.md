# Fiche pédagogique six pages — projection Hivest v0.2

Classe : pedagogique. Profil candidat, six pages physiques A4 portrait.

Entrée : un Markdown existant avec six titres ordonnés `## Page 1 — …` à `## Page 6 — …`. Le texte et les notes restent ceux du Markdown; le renderer ne produit ni recherche ni score.

1. Comprendre : bandeau, définition et exemples, TOWS en quatre cartes.
2. Transmettre : pitch dans une carte, framework en étapes, arguments et objections.
3. Diagnostiquer : les cinq branches systémiques et leur relation causale.
4. Se projeter : trajectoire d'intégration, horizons, rattachement au programme.
5. Relier à la valeur : quatre cartes métier issues du tableau Porter/ICP.
6. Agir : chaque use case possède sa carte BAC et ses cinq notes; le prompt clôt la page.

Le HTML sémantique possède six sections `.page`. La palette et les composants viennent du rendu Hivest importé; les adaptations CSS restent dans `renderers/pedagogical/theme.css`. Aucun style dans `binding.json`.

La QA reprend le contrôle navigateur Hivest, remplace le nombre attendu de trois par six et recoupe le nombre de pages physiques du PDF. Aucun dépassement n'est absorbé en réduisant les polices; un dépassement fait échouer le rendu. Le rapport et le manifeste sont liés aux empreintes réelles des entrées et sorties. Le reçu garde distincts intégrité, QA, publication et autorisation.
