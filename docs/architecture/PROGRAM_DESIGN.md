# PROGRAM_DESIGN_READY — dossier de décision

## Résultat
Cristalliser un OS v0.1.0, puis éprouver Sphere et STG. Le template reste candidat jusqu'aux deux rendus pilotes. Aucun score, ROI ou verdict d'entreprise n'est produit dans cette phase.

## 1–2. Audit de réutilisation et capability map
Audit de fichiers réels aux commits figés dans `program/upstream-lock.json` ; aucun import global des dépôts.

| Capacité | Décision | Réutilisation / écart |
|---|---|---|
| AI strategy control tower | EXTEND | Reprendre cadrage, quatre passes corporate/organisation/hiring/newsflow et preuve de déploiement ; ajouter scope industriel et portefeuille. |
| Evidence V1 | EXTEND | Reprendre immutabilité, locator, excerpt borné, hash, entités ; séparer dates publication/observation/consultation, scope et indépendance des sources. |
| Claim contract | EXTEND | Préserver ownership/contradictions ; ajouter recommendation et scope sector/company/portfolio. P1/P2/U1/W1/N0 ne sont pas synonymes automatiques de A–E. |
| Enterprise use-case intelligence | EXTEND | Product-blind déjà présent. Le contrat amont 0.6 accepte observed/inferred/validated ; ajouter une couche hypothèses non promues et les horizons/sourcing. |
| Enterprise value-chain causal analysis | EXTEND | Le skill exige un UC canonique ; créer ici la chaîne corporate d'abord, puis conserver son analyse locale sans extrapoler un UC à toute l'entreprise. |
| Storytelling / claims graph / RunContext | EXISTING | Réutiliser séparation recherche/fragments/claims/scaffold/rendu, trois revues et boucle bornée. |
| Maturité 8 dimensions | NEW | Rubrique propre au programme, score nul si inconnu, couverture séparée de capacité. |
| Strategic Centrality × Differentiation | NEW | 3×3 interne, argument de sourcing et garde-fous ; pas une BCG. |
| THREE_PAGER_PORTFOLIO_AI | NEW | Le catalogue storytelling inspecté ne contient pas ce template. Contrat créé, validation graphique différée aux pilotes. |
| Product fit, nudging commercial, reach | REJECT | Hors finalité ; aucun catalogue fournisseur n'alimente le diagnostic. |
| Runtime applicatif CRM complet | REJECT | Aucun besoin de cloner base, UI ou dépendances CRM pour un OS documentaire. |

Le code amont n'est pas déclaré exécuté ou intégré : cette livraison réutilise les contrats et procédures après lecture. Les fichiers lus, leurs SHA et décisions sont consignés.

## 3. Architecture
Router court → manifest → procédure → preuves pertinentes → checkpoint. Un seul nouveau skill programme avec six modules en lecture conditionnelle couvre les écarts ; les dix rôles du handoff ne deviennent pas dix skills redondantes.
`raw external immutable → evidence → claims → wiki → analysis → frozen content → artifacts`.
Les pages wiki et analyses promues sont durables ; debug et runs restent externes. Les snapshots ne sont jamais remplacés : correction = nouveau hash + supersedes.

## 4. Contrats
`company-package.schema.json` : sources, fragments, claims, maturité, chaîne, use cases et 9-box ; `run-context.schema.json` : reprise et HITL ; `three-pager.schema.json` : contenu prêt à geler. Les JSON sont aussi du YAML valide ; une seule source canonique évite deux schemas divergents.
Le validateur sémantique vérifie références, portée, dates, corroboration, hard gates et contenu gelé. La qualification de la force probante reste une revue analytique.

## 5. Trois pages
Contrat détaillé : `templates/THREE_PAGER_PORTFOLIO_AI.md`. Maintenir toutes les rubriques avec « non établi » si nécessaire. Si les 7 axes 7S ne sont pas tous documentés, afficher une grille de couverture, pas un radar fermé trompeur. Six opportunités suffisamment décrites suffisent ; dix est un maximum. Pas de réduction de police pour absorber une recherche trop longue.

## 6. Tests
Unitaires : hash, références, dates, scopes et hard gates. Schema : types, cardinalités, enums. NRT adversariales : sector laundering, annonce→production, job→capacité, unknown→0, manque de contre-preuve, freeze sans HITL. Rendu : trois pages exactes, overflow, police ≥9 pt, sources lisibles et inconnues visibles ; exécution sur les deux vrais pilotes avant promotion du template. Reader/decision : thèse, falsificateur et prochaine décision repérables sans lire les annexes.

## 7. Pilotes retenus
Sphere : industriel multi-sites et packaging ; teste granularité groupe/site, qualité, rendement, énergie, supply chain et différenciation process.
STG : logistique sous température dirigée ; teste flux, réseau, planning, service client, dispatch et frontière optimisation/IA. L'absence de manufacturing ne doit pas dégrader son score breadth.
Ce choix est une recommandation de design, pas un classement économique. Le statut actif et le type d'activité sont vérifiés sur https://hivestcapital.com/portefeuille/ le 23/09/2026. La richesse des sources IA n'est pas encore établie. Remplaçant industriel : CCE Group ; remplaçant service : Novasol. Remplacer uniquement après journal d'échec d'accès/couverture.

## 8. Ordre proposé
Sphere → STG → loopback obligatoire → CCE Group → Aurightec → VMI-Jokon → Agora Makers → Marie-Laure PLV → NV Labs → Novasol Chemicals → Reunimer → Hivest.
Logique : apprendre manufacturing et services, réutiliser engineering, puis process régulés/distribution et chaîne agro ; traiter Hivest à partir des constats des participations. Réviser à chaque cluster selon sources et réutilisabilité ; ne pas inventer de sequencing score numérique tant que ces critères ne sont pas observés.

## 9. Risques et limites
- Publicité faible ≠ maturité faible : afficher couverture et capacité séparément.
- Groupe ≠ filiale ≠ usine : scope de chaque claim obligatoire ; pas d'extrapolation silencieuse.
- Même communiqué repris par cinq sites = une seule origine de preuve.
- ROI brut ≠ valeur equity : baseline, coûts d'intégration/adoption/supervision et horizon requis ; ne pas additionner bénéfices qui se chevauchent.
- Breadth : dénominateur des domaines applicables documenté ; pas de pénalité sectorielle automatique.
- 7S et SWOT sont des synthèses analytiques ; interdire les scores de décoration.
- Sources LinkedIn éventuellement inaccessibles : consigner l'accès, ne pas fabriquer de profil.
- Trois pages denses : contrat candidat, test visuel réel encore à faire.
- Attribution « Karpathy LLM-Wiki » fournie par le handoff sans URL précise : architecture adoptée comme choix interne, attribution bibliographique non vérifiée.
- Données privées : dépôt public ; ne promouvoir que contenu public autorisé. Les notes d'entretien éventuelles restent externes.

## 10. Exécution du premier pilote
1. Sphere, cutoff 23/09/2026 : résoudre groupe/filiales/acquisitions et périmètre financier ; conserver annonce et closing distincts.
2. Récolter sites officiels, Hivest, comptes disponibles, usines, produits, recrutements et cas clients/fournisseurs. Journaliser recherches négatives et dates.
3. Trois inconnues prioritaires : hétérogénéité ERP/MES et données qualité ; coût réel des pertes/arrêts/énergie ; autorité groupe vs usines pour financer et déployer.
4. Reconstruire chaîne matériaux → formulation/production → qualité → distribution ; qualifier handoffs et contrôles avant toute solution IA.
5. Alimenter wiki packaging/industrial AI avec preuve de possibilités et limites de transfert ; chercher optimisation et vision autant que GenAI.
6. Produire les huit dimensions et un inventaire hypothétique explicite. Shortlist 6–10, baseline sans IA, gates OT/data, mécanisme économique et question de validation.
7. Red-team conformance, contre-perspective, décision ; une réparation puis une vérification. Si échec majeur : REOPEN_TARGETED.
8. Présenter le dossier pré-HITL à François ; seulement après GO_DRAFT, geler le contenu, rendre les trois pages et vérifier visuellement.
9. Répéter STG, comparer les échecs du template et proposer le loopback avant industrialisation.
