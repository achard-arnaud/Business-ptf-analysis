# Fiche 6 — Synthèse multicapacité

**Promesse pédagogique :** montrer comment plusieurs capacités se complètent dans un même parcours, et où l'humain garde la décision.  
**Source :** SRC-BOOK-01, chap. 2, pp. 23–36 (modes combinables); SRC-BOOK-02, chap. 5; SRC-BOOK-03, chap. 6.

## Page 1 — Comprendre : une chaîne de capacités plutôt qu'un modèle unique
Cas illustratif : réception et traitement d'une demande de remboursement fictive ou anonymisée. La **Perception** lit formulaire et pièces; le **Raisonnement** vérifie cohérence et règles sourcées; la **Prédiction** signale un niveau de priorité ou une anomalie; la **Création** prépare une réponse; l'**Agentique** peut router le dossier après accord. Cinq capacités sont présentes; aucune n'est nécessairement requise dans chaque entreprise.

| TOWS | Posture appliquée |
|---|---|
| Offensive — forces × opportunités | Combiner sources autorisées et flux bien définis pour améliorer le délai de traitement. |
| Défensive — forces × menaces | Placer validation humaine aux décisions d'éligibilité, de paiement et de communication. |
| Opportuniste — faiblesses × opportunités | Prototyper la lecture + vérification sur données synthétiques. |
| Préservation — faiblesses × menaces | Garder un traitement manuel si qualité, droits ou responsabilité ne sont pas clairs. |

**Takeaway → p. 2 :** raconter la chaîne et ses points de contrôle plutôt que promettre un agent magique.

## Page 2 — Transmettre : expliquer le parcours
**Pitch (30 s).** « Une demande arrive sous plusieurs formats. L'IA peut lire les pièces, comparer les informations à une règle, signaler ce qui mérite attention et préparer une réponse. La décision reste à la personne autorisée; une automatisation éventuelle ne vient qu'après un test et une validation du processus. »

**Framework :** Entrée → Perception → Raisonnement sourcé → Prédiction de priorité → Création d'un brouillon → décision humaine → routage contrôlé.

Urgence : la coordination prend du temps; douleur : les mêmes vérifications sont répétées; simplicité : commencer par le dossier et les règles sans envoyer ni décider. Objections : erreur de chaîne, fuite de données, score injuste, responsabilité, intégration — traiter chacune comme un risque à tester.

**Takeaway → p. 3 :** le système est fiable seulement si tous les handoffs le sont.

## Page 3 — Diagnostiquer : examiner les cinq branches

| Branche | Question systémique |
|---|---|
| Processus | Quelle étape est assistée, qui tranche et comment une exception revient-elle ? |
| Outils | Formulaire, gestion documentaire, règles, CRM/case management reliés comment ? |
| Compétences | Qui vérifie extraction, règle, score et réponse ? |
| Données | Formats et règles autorisés, versions, historique représentatif ? |
| Gouvernance | Accès minimaux, journal bout en bout, responsables et arrêt d'urgence ? |

**Chemin d'échec :** pièce mal lue → comparaison incomplète → score trompeur → réponse erronée → routage incorrect. Les contrôles doivent suivre la donnée et conserver le lien à la pièce d'origine.

**Takeaway → p. 4 :** établir d'abord une version « lecture seule » avant toute action.

## Page 4 — Se projeter : intégrer après validation de chaque maillon
Assistant : lecture/synthèse sur demande. Copilot : vérification et brouillon intégrés au poste du gestionnaire. Agent : rassemble les pièces et route les cas conformes; cas ambigus ou décision financière restent en validation humaine.

- **Low-hanging fruit :** extraction et checklist sur dossier synthétique.
- **Quick win :** assistant de complétude avec citations des règles.
- **Big bet :** parcours orchestré multi-système, contrôles et reprise d'incident.

Le lien au niveau 2 est proposé autour du mapping de processus, du choix d'un cas et de sa mesure; numérotation exacte à confirmer avec le syllabus des 17 piliers.

**Takeaway → p. 5 :** le processus choisi doit combiner volume, douleur et contrôle faisable.

## Page 5 — Relier à la valeur : où la chaîne se répète
| Fonction | Parcours candidat | Porteur métier | Enablers |
|---|---|---|---|
| Logistique | Documents → conformité de livraison → priorité → dossier | Responsable supply | Documents, commandes, règles et file |
| Opérations | Signal/capteur → interprétation → alerte → intervention | Responsable opérations | Capteurs, historiques, système de maintenance |
| Marketing/Vente | Demande → profil → priorité → proposition | Responsable ventes | CRM autorisé, catalogue, contrôle des engagements |
| Services | Pièces → règle → priorité → réponse → routage | Responsable service | Base de règles, gestion de cas, approbation |

Les fonctions auxiliaires (IT, sécurité, juridique, RH) rendent possible le flux par les accès, contrôles et compétences; elles ne sont pas de simples fournisseurs de validation en fin de projet.

**Takeaway → p. 6 :** démarrer par la partie qui apporte une mesure utile avec le moins de dépendances.

## Page 6 — Agir : un premier parcours de demande
| Cas | Automatisation × Intégration | BAC résumé | Valeur | Coût | Risque | Complexité | Généricité |
|---|---|---|---:|---:|---:|---:|---:|
| Extraction + checklist | faible × faible | Réduire ressaisie; repérer les manques; champs liés aux pièces | 3 | 1 | 1 | 1 | 3 |
| Priorité avec contrôle | moyenne × moyenne | Traiter plus vite; ordonner revue; score + motif | 2 | 2 | 3 | 2 | 2 |
| Routage agentique de cas simples | forte × forte | Réduire délai; éviter les relances; routage + journal + arrêt | 3 | 3 | 3 | 3 | 2 |

BAC signifie ici Bénéfices, Avantages, Caractéristiques. Étoiles 1 faible à 3 élevé; un score élevé de risque, coût ou complexité est défavorable.

**Prompt d'essai :** « Sur ce dossier fictif, extrais les champs demandés avec renvoi aux passages source; compare-les à la règle jointe; liste les pièces manquantes et contradictions; propose une priorité et un brouillon de réponse. Sépare constat, hypothèse et recommandation. N'approuve aucun remboursement, n'envoie rien et n'écris dans aucun système. »

**Boucle :** tester chaque capacité seule et en chaîne, mesurer erreurs de bout en bout et revoir les points d'arrêt.
