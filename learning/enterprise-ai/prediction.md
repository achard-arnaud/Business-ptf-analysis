# Fiche 1 — Prédiction

**Promesse pédagogique :** passer d'un historique à une décision mieux préparée, sans présenter une estimation comme une certitude.  
**Source :** SRC-BOOK-01, chap. 2, « Prediction », pp. 23–26; SRC-BOOK-02, chap. 5; SRC-BOOK-03, chap. 6.

## Page 1 — Comprendre : un signal sur ce qui pourrait arriver
La prédiction utilise des observations passées pour estimer une valeur, une catégorie ou une probabilité future. Elle répond à « que risque-t-il de se passer ? » et aide un professionnel à préparer une réponse. Elle n'explique pas toujours pourquoi et n'annonce pas le futur avec certitude.

**Exemples progressifs :** estimer le nombre de demandes la semaine prochaine; classer les alertes à examiner; anticiper les pannes probables afin de planifier une maintenance.

| TOWS | Posture appliquée |
|---|---|
| Offensive — forces × opportunités | Capitaliser sur un historique fiable pour anticiper une demande encore peu servie. |
| Défensive — forces × menaces | Utiliser une détection éprouvée pour repérer une dérive, avec revue humaine et plan de repli. |
| Opportuniste — faiblesses × opportunités | Commencer sur une source déjà disponible et un cas de faible conséquence, puis apprendre. |
| Préservation — faiblesses × menaces | Reporter si données biaisées, contexte changeant ou faux négatifs trop coûteux. |

**Takeaway → p. 2 :** choisir la décision à préparer avant de choisir le modèle.

## Page 2 — Transmettre : faire parler l'historique
**Pitch (30 s).** « Nous prenons déjà des décisions à partir d'indices et d'historiques. La prédiction peut faire ressortir plus tôt les cas qui méritent notre attention. Elle donne un signal à vérifier, pas un ordre. Testons-le sur une tâche répétitive et gardons la décision à l'équipe. »

**Framework :** Historique → Estimation → Vérification → Décision métier → Mesure.

- **Urgence :** les volumes et anomalies deviennent parfois visibles trop tard.
- **Douleur :** le signal aide à trier les cas, sous réserve d'une comparaison avec la pratique actuelle.
- **Simplicité :** une liste de 20 alertes revue une fois par semaine suffit pour apprendre.
- **Objections :** « Le modèle peut se tromper » — définissons les seuils et l'escalade. « Nos données ne sont pas parfaites » — vérifions leur couverture d'abord. « Cela remplace l'équipe » — le premier essai mesure une décision assistée.

**Takeaway → p. 3 :** un bon test dépend autant de l'organisation que de l'algorithme.

## Page 3 — Diagnostiquer : préparer une boucle de correction

| Branche | À vérifier |
|---|---|
| Processus | Quelle action change si le signal dépasse le seuil ? Qui traite les exceptions ? |
| Outils | Où voir score, date, incertitude et moyen de corriger ? |
| Compétences | Les utilisateurs distinguent-ils une alerte utile d'une certitude ? |
| Données | Historique représentatif, droits d'usage, champs manquants, périodes atypiques ? |
| Gouvernance | Propriétaire, seuil d'arrêt, suivi des erreurs et biais, recours ? |

**Carte causale :** données incomplètes → estimation instable → alertes mal priorisées → perte de confiance → contournement. Une boucle de retour utilisateur et une revue régulière permettent de repérer ce glissement.

**Takeaway → p. 4 :** le premier niveau utile peut rester une simple aide à la décision.

## Page 4 — Se projeter : augmenter l'intégration par étapes
**Assistant :** explique une estimation déjà produite. **Copilot :** affiche le signal dans l'outil métier et permet de le corriger. **Autopilot/Agent :** peut déclencher une action bornée après validation des règles, seuils et exceptions.

- **Low-hanging fruit :** tableau de prévisions avec incertitudes visibles.
- **Quick win :** alerte hebdomadaire de charge, revue par le responsable.
- **Big bet :** ajustement coordonné de capacité sur plusieurs équipes.

**Lien au programme :** niveau 2 proposé — relier le signal à une décision et mesurer sa qualité; pilier exact à confirmer avec le syllabus des 17 piliers.

**Takeaway → p. 5 :** la valeur apparaît dans une fonction et un flux de travail précis.

## Page 5 — Relier à la valeur : quatre portes d'entrée
| Fonction | Douleur / décision | Porteur métier | Enablers |
|---|---|---|---|
| Logistique | Anticiper stock et réapprovisionnement | Responsable supply | Historique de commandes et délais |
| Opérations | Prévoir charge, maintenance ou défauts | Responsable opérations | Séries temporelles fiables, capteur si utile |
| Marketing/Vente | Prioriser prospects ou demandes | Responsable CRM / ventes | Historique de conversion, contrôle des biais |
| Services | Prévoir flux de tickets et capacité | Responsable de service | Motifs, volumes, saisonnalité |

Dans la chaîne de valeur, le point d'entrée n'est pas « faire de l'IA » mais réduire l'incertitude d'une décision répétée.

**Takeaway → p. 6 :** choisir une décision mesurable et un premier cas réversible.

## Page 6 — Agir : sélectionner un premier essai
**Matrice automatisation × intégration :** prévision de charge — faible automatisation / faible intégration; tri d'anomalies — automatisation faible à moyenne / intégration moyenne; réapprovisionnement automatique — automatisation forte / intégration forte, donc contrôle et exception renforcés.

| Cas | Bénéfice | Avantage | Caractéristique | Valeur | Coût | Risque | Complexité | Généricité |
|---|---|---|---|---:|---:|---:|---:|---:|
| Prévision de charge | Anticiper | Ajuster les équipes plus tôt | Fourchette + intervalle | 3 | 1 | 1 | 1 | 3 |
| Détection d'anomalies | Repérer tôt | Réduire le tri manuel | Alerte + cause candidate | 2 | 2 | 2 | 2 | 3 |
| Score de priorité | Concentrer l'attention | Classer les cas à revoir | Score avec critères | 2 | 2 | 3 | 2 | 2 |

**Lecture des étoiles :** 1 faible, 2 moyenne, 3 élevée. Valeur et généricité élevées sont favorables; coût, risque et complexité élevés demandent davantage de prudence. Notes pédagogiques, pas un business case.

**Prompt d'essai :** « Avec ce jeu fictif de volumes hebdomadaires, estime les quatre semaines suivantes. Présente les hypothèses, les limites et les anomalies; distingue données observées et estimation; propose les contrôles qu'un responsable doit faire avant d'ajuster un planning. N'invente aucune donnée et ne déclenche aucune action. »

**Boucle :** comparer erreur et décision à une base de référence avant toute extension.
