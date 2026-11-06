# Composition paysage — un contenu, trois couches

Le mécanisme Hivest fournit la conversion Markdown, le lancement navigateur et les contrôles géométriques verrouillés dans `renderers/pedagogical/upstream-lock.json`. Le profil paysage garde ces imports et remplace la projection portrait par six compositions pédagogiques. Aucune dépendance aux gates du portefeuille.

## Depuis la racine du dépôt

```bash
python -m pip install -r renderers/pedagogical/requirements.txt
python -m playwright install chromium
python renderers/pedagogical/landscape.py learning/enterprise-ai/perception.sheet.json --out build/perception
python renderers/pedagogical/landscape.py learning/enterprise-ai/perception.sheet.json --out build/perception --verify
```

Réutiliser un Chrome installé avec `NICE_CHROMIUM_PATH` si disponible; la CI le détecte. Le fichier canonique est `perception.sheet.json`; exporter son Markdown avec :

```bash
python renderers/pedagogical/landscape.py learning/enterprise-ai/perception.sheet.json --out build/perception --export-markdown learning/enterprise-ai/perception.md
```

## Sorties et preuve

- `binding.json` = copie fidèle du contenu canonique, pas un second modèle.
- `scaffold.html` = structure sémantique sans CSS; `fiche.html` = même structure avec `landscape.css` appliqué.
- `fiche.pdf` = six pages A4 paysage; `page-01.png` à `page-06.png` = pages à inspecter; `fiche.md` = projection lisible.
- `qa.json` = seul rapport de run : débordements, chevauchements, petites polices, padding, six pages physiques, orientation, empreintes, révision et versions des outils. Il conserve séparément les statuts visuel et éditorial.

Le vérificateur rejette source/catalogue périmés, sortie modifiée ou rendu invalide. Le test technique ne confirme pas la véracité du contenu. Ne pas réécrire un score, réduire les polices ou masquer un débordement pour obtenir un passage vert. Garder les sources primaires en liens dans la fiche et le registre complet dans le JSON/Markdown; les chiffres datés ne deviennent pas des garanties.
