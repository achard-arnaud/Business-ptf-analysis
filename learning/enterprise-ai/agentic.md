# Fiche 5 — Agentique

**Promesse pédagogique :** faire passer un système de la réponse à l'exécution contrôlée d'étapes, seulement lorsque les autorisations et les points d'arrêt sont définis.  
**Source :** SRC-BOOK-01, chap. 2, « Agentic mode », pp. 34–36; SRC-BOOK-03, chap. 6; SRC-BOOK-04, chap. 10.

## Page 1 — Comprendre : de l'assistant à l'action
Une solution agentique peut planifier une séquence, utiliser des outils et accomplir certaines tâches avec moins de relances. Elle peut aussi se tromper plus loin et plus vite. « Autonome » décrit la délégation, pas la qualité. Une tâche doit avoir un résultat clair, des limites, des journaux et un moyen d'interrompre.

**Exemples progressifs :** lister les étapes d'un dossier; préparer un brouillon et demander approbation; classer automatiquement les cas simples et escalader les exceptions.

| TOWS | Posture appliquée |
|---|---|
| Offensive — forces × opportunités | Déléguer des tâches nombreuses et répétables dans un workflow maîtrisé. |
| Défensive — forces × menaces | Garder approbation et journal sur les décisions ou écritures sensibles. |
| Opportuniste — faiblesses × opportunités | Automatiser une étape limitée avec données fictives puis pilote restreint. |
| Préservation — faiblesses × menaces | Pas d'action autonome si identité, droits, exceptions ou retour arrière sont incertains. |

**Takeaway → p. 2 :** parler de tâche et d'autorisation, pas de « collègue IA ».

## Page 2 — Transmettre : déléguer avec des garde-fous
**Pitch (30 s).** « Un agent peut enchaîner plusieurs étapes qui nous demandent aujourd'hui des relances et des copiés-collés. Nous définissons précisément ce qu'il peut faire, où il s'arrête et qui valide. Nous commençons par un flux non sensible, avec journal et bouton d'arrêt. »

**Framework :** Objectif → Plan → Outils autorisés → Contrôles → Approbation / arrêt → Journal.

- **Urgence :** les files d'attente et relances pèsent sur le délai.
- **Douleur :** l'agent peut prendre en charge les étapes prévisibles.
- **Simplicité :** un workflow sandboxé et un résultat vérifiable.
- **Objections :** « Il peut agir à tort » — droits minimaux, limites et annulation. « Je ne peux pas le surveiller » — notification et journal. « Un agent fait tout » — chaque outil et étape doit être autorisé.

**Takeaway → p. 3 :** déléguer exige plus de gouvernance que rédiger un brouillon.

## Page 3 — Diagnostiquer : cartographier pouvoir et arrêt
| Branche | À vérifier |
|---|---|
| Processus | Actions autorisées, exceptions, approbation, retour arrière ? |
| Outils | Comptes de service, permissions minimales, environnement de test ? |
| Compétences | Qui surveille, reprend et explique une exécution ? |
| Données | Exactitude, droits, limites d'accès et mise à jour ? |
| Gouvernance | Responsable, traces, seuil d'arrêt, incident, recours ? |

**Carte causale :** objectif vague → mauvaise action choisie → outil trop permissif → effet réel → correction coûteuse. Réduire le périmètre avant d'augmenter l'autonomie.

**Takeaway → p. 4 :** le plus sûr est de monter en autonomie par incréments.

## Page 4 — Se projeter : action graduée
**Assistant :** propose la prochaine étape. **Copilot :** exécute une action à chaque validation. **Autopilot/Agent :** enchaîne les étapes bornées et s'arrête sur exceptions. Commencer par l'assistant, puis l'action supervisée; ne déléguer un workflow complet qu'après preuve de stabilité.

- **Low-hanging fruit :** préparer une checklist de suivi.
- **Quick win :** router un dossier test vers une file simulée.
- **Big bet :** orchestration multi-systèmes, droits et continuité renforcés.

**Lien niveau 2 :** proposition — décrire workflow, permissions et supervision; mapping des 17 piliers à confirmer.

**Takeaway → p. 5 :** les métiers diffèrent par le coût d'une action erronée.

## Page 5 — Relier à la valeur : automatiser le flux, pas le jugement
| Fonction | Besoin | Porteur métier | Enablers |
|---|---|---|---|
| Logistique | Créer ou suivre une demande d'expédition | Responsable transport | API, règles, preuve de livraison |
| Opérations | Alerter et ouvrir une tâche après incident | Responsable d'exploitation | Seuils, CMMS, procédure d'escalade |
| Marketing/Vente | Préparer le suivi d'une demande entrante | Responsable commercial | CRM, consentement, approbation |
| Services | Catégoriser et router demandes simples | Responsable support | Base de réponse, file, transfert humain |

**Takeaway → p. 6 :** évaluer le contrôle et les conséquences avant le nombre d'étapes automatisées.

## Page 6 — Agir : un workflow borné
| Cas | Automatisation × Intégration | BAC (B / A / C) | Valeur | Coût | Risque | Complexité | Généricité |
|---|---|---|---:|---:|---:|---:|---:|
| Routage de demandes simples | forte × moyenne | B : réduire le délai de tri; A : orienter vers la bonne file; C : catégorie et règle visibles | 3 | 2 | 2 | 2 | 3 |
| Préparation de dossier | moyenne × faible | B : réduire les relances; A : rendre le dossier complet; C : checklist de pièces et étapes | 2 | 1 | 1 | 1 | 3 |
| Enchaînement multi-outils | forte × forte | B : réduire les délais; A : coordonner les étapes; C : agent avec journal et arrêt | 3 | 3 | 3 | 3 | 2 |

Matrice : chaque paire indique automatisation puis intégration, chacune de faible à forte. Étoiles mesurent l'ampleur (1–3), pas la désirabilité : coût, risque et complexité élevés dégradent le cas. Droits, sécurité, contrôle humain et faisabilité sont des gates avant classement.

**Prompt d'essai :** « Dans cet environnement fictif, prépare le routage de ces trois demandes. Pour chacune, donne la catégorie, la règle utilisée, l'action proposée et les incertitudes. N'envoie aucun message, ne modifie aucun système et arrête-toi si une demande sort des critères. »

**Boucle :** compter exceptions, actions reprises et erreurs avant toute permission d'écriture.
