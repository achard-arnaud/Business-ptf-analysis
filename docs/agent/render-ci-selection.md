# CI de rendu — sélecteur par delta et trois profils (#31)

`scripts/ci_render_selector.py` retourne `true/false` d'après les chemins réellement modifiés, y compris suppression/renommage ; jamais sur la base de labels GitHub ou d'un commentaire d'agent. Changements de renderer/CSS, manifests/templates, contrats et fixtures de rendu → Chromium. Docs purement descriptives → unitaires & lints, pas de browser.

Le workflow `.github/workflows/contracts.yml` conserve les NRT structurelles en `validate`. En cas de sélection, `render-qa` attend la validation puis génère :
- le template exec v0.3 avec une fixture démonstrative **non approuvée** ;
- le profil manufacturier candidat ;
- le profil infrastructure/asset-service candidat.

Chaque rendu livre **PDF + 3 PNG + report navigateur + manifest**, puis passe `verify_render_evidence.py` : nombre physique des pages, hashes, défauts CSS, statut QA et statut de publication. Le test négatif produit un overflow volontaire et exige que le navigateur le rejette. Artifacts Actions conservés séparément de l'archive des preuves d'entreprises ; aucune nouvelle permission de déploiement.

**Limites :** la comparaison pixel-à-pixel historique n'est pas encore activée ; elle requiert une baseline stabilisée par version Chromium et une inspection humaine. CI verte ne signifie pas GO_DRAFT, preuve économique, autorisation comité ou diffusion.
