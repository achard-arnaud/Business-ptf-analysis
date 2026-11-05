# Fiche 4 — Raisonnement (Thinking)

**Promesse pédagogique :** relier plusieurs éléments d'information pour éclairer une question complexe, en rendant visibles les sources, les incertitudes et les étapes de vérification.  
**Source :** SRC-BOOK-01, chap. 2, « Thinking mode », pp. 30–34; chap. 6, « Use case fact sheets »; chap. 10.

## Page 1 — Comprendre : relier sans masquer les lacunes
Dans cette série, « Raisonnement » correspond au libellé « Thinking » du livre. Il couvre l'analyse, la synthèse, la comparaison, l'interprétation et la personnalisation selon le contexte ou les informations mémorisées. Il ne garantit ni une démonstration logique ni une réponse vraie : le système peut omettre ou relier à tort des éléments.

Le RAG (recherche augmentée) signifie que le système retrouve d'abord des sources autorisées puis prépare sa réponse à partir de celles-ci; il doit rendre ces sources vérifiables.

**Exemples progressifs :** résumer un dossier; comparer deux procédures; préparer une recommandation avec preuves et inconnues.

| TOWS | Posture appliquée |
|---|---|
| Offensive — forces × opportunités | Relier une base de connaissances fiable à des décisions transverses. |
| Défensive — forces × menaces | Exiger citations, contradiction et revue avant une décision sensible. |
| Opportuniste — faiblesses × opportunités | Tester la recherche sur un corpus restreint et accessible. |
| Préservation — faiblesses × menaces | Éviter les conclusions si les sources sont absentes, périmées ou conflictuelles. |

**Takeaway → p. 2 :** toute synthèse doit montrer sur quoi elle repose.

## Page 2 — Transmettre : passer du volume à la compréhension
**Pitch (30 s).** « Nous avons souvent assez d'informations, mais elles sont dispersées. Le raisonnement peut rassembler les éléments, les comparer et proposer une synthèse pour nous aider à décider. Nous lui demandons aussi de montrer les sources, les désaccords et ce qu'il ne sait pas. »

**Framework :** Question → Recherche de sources → Mise en relation → Synthèse + preuves → Revue humaine → Décision.

- **Urgence :** documents et règles se multiplient.
- **Douleur :** synthèse manuelle longue et difficile à partager.
- **Simplicité :** commencer par une seule question récurrente et un corpus validé.
- **Objections :** « La citation peut être fausse » — ouvrir la source. « Le modèle a lu tout le Web » — limiter au corpus autorisé. « Il va décider » — séparer synthèse et décision.

**Takeaway → p. 3 :** une réponse utile exige un corpus, des droits et une responsabilité.

## Page 3 — Diagnostiquer : bâtir la chaîne de confiance
| Branche | À vérifier |
|---|---|
| Processus | Quelles questions peuvent être aidées et quand une expertise est obligatoire ? |
| Outils | Recherche, liens vers extraits, gestion des versions et signalement ? |
| Compétences | Les lecteurs savent-ils vérifier la preuve et repérer l'absence ? |
| Données | Sources complètes, à jour, autorisées et accessibles ? |
| Gouvernance | Propriétaire du corpus, périmètre des réponses, journal et révision ? |

**Chaîne Ishikawa :** source obsolète → recherche inadéquate → synthèse crédible mais fausse → décision fragilisée. Tester des questions auxquelles la réponse est connue et d'autres où le corpus ne contient pas la réponse.

**Takeaway → p. 4 :** connecter les bonnes sources est un passage de maturité.

## Page 4 — Se projeter : une réponse sourcée avant une action
**Assistant :** répond à une question sur des sources fournies. **Copilot :** recherche dans le contexte du travail et prépare une synthèse dans le flux. **Agent :** peut assembler un dossier ou router une demande; la conclusion reste validée par un humain.

- **Low-hanging fruit :** résumé avec citations sur un document.
- **Quick win :** recherche dans une base de procédures avec renvoi direct aux passages.
- **Big bet :** assistant métier qui combine plusieurs corpus et workflows, avec surveillance.

**Lien niveau 2 :** compétence proposée — poser des questions vérifiables, reconnaître les lacunes et mesurer la couverture; pilier exact à confirmer.

**Takeaway → p. 5 :** choisir le métier où l'information dispersée crée un coût concret.

## Page 5 — Relier à la valeur : synthétiser au bon endroit
| Fonction | Besoin | Porteur métier | Enablers |
|---|---|---|---|
| Logistique | Comprendre retards et contraintes de transport | Responsable supply | Suivi des commandes, contrats, événements |
| Opérations | Comparer incidents et procédures | Responsable de production | Journal d'incidents, base de consignes |
| Marketing/Vente | Préparer un compte rendu de marché ou client | Responsable commercial | Sources datées, CRM autorisé |
| Services | Répondre à une question en citant la procédure | Responsable support | Base documentaire, accès et mise à jour |

**Takeaway → p. 6 :** choisir un cas où la preuve peut être contrôlée rapidement.

## Page 6 — Agir : un cas de recherche sourcée
| Cas | Automatisation × Intégration | BAC (B / A / C) | Valeur | Coût | Risque | Complexité | Généricité |
|---|---|---|---:|---:|---:|---:|---:|
| Q/R sur procédures internes | moyenne × faible | B : réduire le temps de recherche; A : rendre la règle consultable; C : réponse avec source | 3 | 2 | 2 | 2 | 3 |
| Comparaison de dossiers | faible × faible | B : accélérer la revue; A : repérer les écarts; C : tableau comparatif sourcé | 2 | 1 | 2 | 2 | 2 |
| Synthèse de veille | moyenne × moyenne | B : synthétiser plus vite; A : dégager les thèmes; C : note datée et sourcée | 2 | 2 | 3 | 2 | 2 |

Matrice : chaque paire indique automatisation puis intégration, chacune de faible à forte. Étoiles : 1 faible, 2 moyen, 3 élevé. Risque/coût/complexité élevés demandent des contrôles et ressources supérieurs.

**Prompt d'essai :** « Réponds à la question à partir des extraits fournis seulement. Pour chaque affirmation importante, cite la source et le passage. Sépare faits, interprétations et inconnues; si le corpus ne permet pas de répondre, dis-le. Donne les éléments contradictoires et une question de vérification pour le métier. »

**Boucle :** vérifier chaque citation puis comparer temps, complétude et erreurs à la recherche actuelle.
