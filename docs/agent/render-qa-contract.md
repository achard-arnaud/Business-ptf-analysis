# Vérification des rendus — par artefact et par version

`scripts/verify_render_evidence.py` recoupe `render_manifest.json`, `qa.json`, **le vrai PDF** (trois pages physiques via pypdf) et les trois PNG (signatures, dimensions et hashes). Il refuse le succès sans tous les artefacts, sur un rapport de QA modifié, un PDF remplacé, une page manquante ou un écart de contenu.

Usage :

```sh
python scripts/verify_render_evidence.py /tmp/preview-qa/assets --profile value-chain-preview
python scripts/verify_render_evidence.py /tmp/legacy-qa --profile exec
```

Résultat `AUTOMATED_LAYOUT_PASS_READER_PENDING` : **la QA navigateur n'est pas la revue humaine de lecture**. L'historique `exec v0.3` conserve sa forme et ses contrats de rendu, seules les empreintes de sortie sont ajoutées au manifest lors de `--pdf`.

Ce contrôle est complémentaire des vérifications sémantiques sources/claims, de freeze/HITL, d'exfiltration et de disponibilité distante. Le test de dérive pixel par pixel à travers versions de Chromium reste à traiter avant de revendiquer une référence graphique stable sur différents runners.
