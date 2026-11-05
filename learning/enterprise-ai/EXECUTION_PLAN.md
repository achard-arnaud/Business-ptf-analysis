# Plan d'industrialisation — fiches pédagogiques « Pour aller plus loin »

Version 0.1 — plan de reprise séquentielle, 5 novembre 2026  
Statut : cadrage en cours; aucune fusion vers dev/main avant fermeture des boucles et revue humaine.

## Objectif

Produire six fiches de six pages pour débutants et poissons pilotes : Prédiction, Perception, Création, Raisonnement (Thinking dans le livre), Agentique, puis Synthèse multicapacité. Le rendu final doit être réutilisable dans un programme de 17 piliers et prêt à recevoir un catalogue d'environ 70 cas d'usage.

## Frontières invariantes

1. **Binding de contenu** : variables, sources, claims, blocs rédigés et use cases.
2. **Scaffold HTML** : structure sémantique, ordre des six pages et références de blocs.
3. **Rendu** : CSS, pagination et export dans un renderer distinct; hors de cette livraison.
4. **Preuves** : séparer ce que dit le livre, l'inférence pédagogique, l'exemple hypothétique et la recommandation. Pas de promesse de ROI ni de reprise longue du texte source.
5. **Portefeuille Hivest** : parcours pédagogique isolé; ne modifie aucun gate ou état Hivest.
6. **Syllabus** : les liens aux 17 piliers restent provisoires tant que les IDs et objectifs exacts ne sont pas fournis.
7. **Backlog** : conserver IDs et catalogue complet; sélectionner seulement 3 à 5 cas pour chaque fiche.

## Boucle agentique séquentielle

Pour chaque unité, une même boucle est exécutée dans l'ordre. Les rôles sont des passes de revue, pas des agents parallèles obligatoires.

1. **Orchestrateur** — charge seulement l'objectif, le checkpoint, les contrats et le module courant; fixe la question de décision/apprentissage.
2. **Chercheur de sources** — relit les passages nécessaires, inscrit le locator, extrait des idées atomiques et note les lacunes.
3. **Concepteur pédagogique** — écrit les six pages et les transitions; vérifie le niveau débutant et le pitch Train-the-Trainer.
4. **Relecteur métier** — attaque les exemples, la TOWS, le mapping des fonctions, les contrôles, les scores et le prompt.
5. **Relecteur de contrat** — vérifie binding/scaffold, class, IDs, sources/claims, BAC et dimensions de notation.
6. **Correction unique** — répare les défauts matériels constatés, puis vérifie une fois; défaut persistant = réouverture ciblée.
7. **Checkpoint** — note les fichiers, versions, verdict, limites et prochaine unité. Seulement alors passer à l'étape suivante.

## Plan par portes

| Gate | Travail strictement séquentiel | Sortie / condition de passage |
|---|---|---|
| G0 — Architecture | Confirmer classes product/business/tech/pedagogique; séparer classe de template et dimension d'analyse; confirmer rôle du dépôt de transit | Taxonomie, manifest, skill et liens de contrats cohérents |
| G1 — Contrats | Revue du binding et du scaffold; exactitude des six pages, lineage claim/source, sélection des use cases, BAC, étoiles, backlog ref | Contrats couvrent un module réel sans style CSS ni champ orphelin |
| G2 — Prédiction | Fermer P1→P6, TOWS, pitch, Ishikawa, trajectoire, Porter/ICP, 3–5 cas, prompt | Revue pédagogique + métier + contrat, puis checkpoint |
| G3 — Perception | Même boucle, sans démarrer avant G2 validé | Checkpoint autonome et transition vers Création |
| G4 — Création | Même boucle; droit d'auteur, hallucinations, validation et responsabilité | Checkpoint autonome et transition vers Raisonnement |
| G5 — Raisonnement | Faire correspondre Thinking; expliquer retrieval/RAG sans surpromesse; vérifier les sources | Checkpoint autonome et transition vers Agentique |
| G6 — Agentique | Décrire permissions minimales, arrêt, journal, reprise et validation humaine | Checkpoint autonome et transition vers Synthèse |
| G7 — Synthèse multicapacité | Cas métier mobilisant au moins quatre capacités distinctes; tracer handoffs et humain | Minimum de quatre capacités, points d'arrêt et mesures de bout en bout |
| G8 — Catalogue backlog | Définir import, IDs stables, provenance, dédoublonnage, filtres et sélection top 3–5 | Modèle prêt à recevoir ~70 cas sans enfler les fiches |
| G9 — Scaffolding | Vérifier six pages semantic HTML, mapping de contenu et accessibilité des ancres | Scaffold prêt pour renderer externe; aucun CSS généré |
| G10 — Revue finale | Contrats/manifest/skill/fixtures; statut CI; limites; décision humaine | PR révisables, CI observée, aucune fusion implicite |

## Critères communs de revue par page

- Une question d'apprentissage, un message principal, un exemple professionnel et un takeaway.
- Page 1 : définition simple, trois exemples progressifs et quatre stratégies TOWS croisées.
- Page 2 : pitch réellement prononçable en 30 s, trois leviers d'adhésion et objections honnêtes.
- Page 3 : Processus, Outils, Compétences, Données, Gouvernance et une relation cause-effet.
- Page 4 : Assistant → Copilot → Autopilot/Agent, niveau d'automatisation et niveau d'intégration séparés.
- Page 5 : Logistique, Opérations, Marketing/Vente, Services; rôle ICP, besoin et enablers.
- Page 6 : 3–5 cas, matrice automatisation/intégration, BAC (Bénéfices, Avantages, Caractéristiques), légende des étoiles et prompt sans action réelle.
- La synthèse enchaîne au moins quatre capacités et garde la décision humaine visible.
- Toute inconnue de programme ou de source reste marquée, non comblée.

## État à la reprise

Les premiers drafts complets et les contrats sont déjà sur deux branches PR en mode draft. La CI a signalé puis corrigé un cas de schéma spécialisé; la PR de taxonomie a son contrôle validate vert. La CI de Business-ptf-analysis a validé contrats et tests existants; son contrôle de rendu historique est encore en cours au moment de la reprise. Ce plan remet le travail en séquence : la prochaine boucle porte sur G0–G1 et la fiche Prédiction, sans promouvoir les cinq autres tant que cette revue n'est pas close.
