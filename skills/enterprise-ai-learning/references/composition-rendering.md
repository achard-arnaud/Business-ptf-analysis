# Composition et rendu — adaptation du mécanisme Hivest

## Provenance et choix de réemploi

Source : `achard-arnaud/Business-ptf-analysis`, commit `973e8d2d444494c0c066a0a4dac920652e35e0b9`. L'import est verrouillé dans `renderers/pedagogical/upstream-lock.json` avec empreinte de chaque fichier.

| Mécanisme Hivest | Adaptation pédagogique |
|---|---|
| Markdown → composants de note stratégique → HTML | Import réel de `strategic_note/build.py`; réemploi de la conversion et des composants, projection des tableaux en cartes |
| Palette navy/blue/teal/gold et typographies | Import de `strategic_note/theme.css`; surcouche pédagogique séparée |
| Trois pages exec | Six pages physiques, une par section Markdown; aucune couverture supplémentaire |
| Source → payload → rendu | Markdown hashé → binding JSON immuable → HTML → PDF/PNG |
| QA navigateur et inspection de PNG | Import du contrôleur exec; six pages attendues, contrôle PDF et revue visuelle des sorties réelles |
| Intégrité, QA, publication, autorisation distinctes | Empreintes, manifeste de rendu et reçu; succès visuel ≠ approbation du contenu |

Les gates de diagnostic entreprise, les pilotes Sphere/STG, les scores de maturité et le GO_DRAFT du portefeuille ne sont pas transposés à la formation. Le statut pédagogique reste candidat tant que la revue éditoriale n'est pas accordée.

## Exécution

1. Lire le Markdown du module courant. Vérifier les six sections; conserver ses sources et scores.
2. Exécuter `python renderers/pedagogical/render.py learning/enterprise-ai/perception.md --out build/learning` pour un pilote; ensuite passer le répertoire pour toute la série.
3. Vérifier `binding.json`, `qa.json`, `render_manifest.json`, `artifact_receipt.json` et le vrai PDF de six pages.
4. Inspecter les six PNG. Corriger le scaffold/CSS pour un défaut de forme; revenir au Markdown pour un défaut de fond. Ne pas réduire les polices pour obtenir six pages.
5. Garder les fichiers générés hors du code. La CI dédiée publie des artefacts du vrai contenu, avec test négatif de débordement.

Les graphiques du corpus ne sont pas inventés par le renderer. Le TOWS et les étapes sont des projections des cellules et textes existants. Un nouvel Ishikawa, un exercice ou une source supplémentaire exige une modification explicite du contenu.

## Recette reproductible — depuis la racine du dépôt

```bash
python -m pip install -r renderers/pedagogical/requirements.txt
python -m playwright install chromium
python renderers/pedagogical/render.py learning/enterprise-ai/perception.md --out build/learning
python renderers/pedagogical/verify.py learning/enterprise-ai/perception.md build/learning/perception
```

Si Chrome est déjà installé, définir `NICE_CHROMIUM_PATH` sur son chemin au lieu de télécharger Chromium. Le workflow effectue ce choix automatiquement. `--html-only` sert à préparer une composition et ne vaut pas un rendu validé. Les rapports conservent le SHA de construction en CI et les empreintes de la source, des imports, du renderer, du thème et de chaque sortie, y compris binding et scaffold. Le vérificateur porte sur le binding de projection, distinct du binding métier décrit par les contrats éditoriaux.

Inspecter les six PNG et le PDF après le contrôle automatisé; nommer dans le compte rendu les défauts corrigés et les limites éditoriales. Pour Perception, le registre indique que les IDs SRC-BOOK-01 à 04 désignent des sections du même ouvrage; le footer « ibid. » est une projection bibliographique, pas une nouvelle source. Ne pas généraliser cette substitution à un corpus différent.
