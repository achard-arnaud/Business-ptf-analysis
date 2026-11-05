# Fiche 2 — Perception

**Promesse pédagogique :** transformer des images, documents, sons ou vidéos en éléments que l'équipe peut contrôler et exploiter.  
**Source :** SRC-BOOK-01, chap. 2, « Perception », pp. 26–28; SRC-BOOK-02, chap. 5; SRC-BOOK-03, chap. 6.

## Page 1 — Comprendre : rendre lisible un monde non structuré
La perception permet à une IA de lire, voir, entendre ou extraire des éléments de formats habituellement interprétés par des personnes. Elle transforme un document ou un signal en texte, champs ou catégories. Une extraction plausible reste à vérifier, surtout si l'original est flou ou ambigu.

**Exemples progressifs :** transcrire une note vocale; lire les champs d'une facture; repérer un équipement endommagé dans une photo.

| TOWS | Posture appliquée |
|---|---|
| Offensive — forces × opportunités | Exploiter un grand volume documentaire déjà autorisé pour accélérer un service. |
| Défensive — forces × menaces | Repérer des anomalies d'image ou de document avec contrôle d'un expert. |
| Opportuniste — faiblesses × opportunités | Tester une extraction sur un petit lot homogène, sans écriture automatique dans le système. |
| Préservation — faiblesses × menaces | Différer si qualité d'image, droits, langues ou conséquences ne sont pas maîtrisés. |

**Takeaway → p. 2 :** l'IA peut lire un format, mais l'équipe doit définir ce que signifie « juste ».

## Page 2 — Transmettre : libérer du temps de lecture
**Pitch (30 s).** « Une partie de notre travail consiste à ouvrir, lire et recopier des informations dispersées. La perception peut préremplir ou signaler les éléments importants. Nous gardons le document d'origine, indiquons ce qui reste incertain et demandons une vérification là où une erreur aurait un effet réel. »

**Framework :** Document / image / audio → Extraction → Vérification des champs → Saisie métier → Correction.

- **Urgence :** le volume augmente plus vite que le temps de lecture disponible.
- **Douleur :** réduire la ressaisie, si l'extraction est contrôlée.
- **Simplicité :** commencer par trois champs d'un type de document fréquent.
- **Objections :** « Elle lit mal » — afficher source et niveau de confiance. « Les documents sont sensibles » — vérifier droits et environnement avant l'essai. « Elle remplacera le contrôle » — définir les champs qui exigent une validation.

**Takeaway → p. 3 :** l'adoption se joue dans le traitement des erreurs et des cas illisibles.

## Page 3 — Diagnostiquer : préserver l'original et la correction

| Branche | À vérifier |
|---|---|
| Processus | Quand un humain vérifie-t-il et que devient une extraction incertaine ? |
| Outils | Peut-on afficher côte à côte source et champ extrait ? |
| Compétences | Les opérateurs savent-ils détecter omis, inversés, ambigus ? |
| Données | Variété de formats, langue, qualité, autorisations et conservation ? |
| Gouvernance | Traçabilité du document, accès, durée de rétention, arrêt ? |

**Carte causale :** document dégradé → champ mal lu → erreur transmise → décision erronée. Le système doit permettre de revenir à la source, corriger le champ et mesurer le taux d'erreur par type de document.

**Takeaway → p. 4 :** débutez par une extraction assistée, sans automatiser la saisie finale.

## Page 4 — Se projeter : passer de l'extraction à l'action
**Assistant :** lit un fichier sur demande et liste les champs. **Copilot :** propose les valeurs dans l'écran métier avec liens vers la preuve. **Autopilot/Agent :** classe ou route un dossier dans les cas simples; les exceptions attendent une personne.

- **Low-hanging fruit :** extraire nom de document et date.
- **Quick win :** préremplir quelques champs avec validation.
- **Big bet :** orchestration documentaire de bout en bout multi-format.

**Lien niveau 2 :** à confirmer; piste de progression proposée entre qualité documentaire, contrôle des extractions et intégration au processus.

**Takeaway → p. 5 :** le bon format et les conséquences varient selon la fonction.

## Page 5 — Relier à la valeur : traiter les bons flux
| Fonction | Douleur / décision | Porteur métier | Enablers |
|---|---|---|---|
| Logistique | Lire bons, preuves de livraison, étiquettes | Responsable entrepôt | Scan, référentiel, contrôle des codes |
| Opérations | Lire formulaires ou images de contrôle qualité | Responsable qualité | Images annotées, critères d'inspection |
| Marketing/Vente | Extraire demandes entrantes et pièces commerciales | Responsable avant-vente | CRM, règles de consentement, modèle de champs |
| Services | Lire factures, formulaires ou comptes rendus | Responsable de service | Gestion documentaire, conservation et droits |

**Takeaway → p. 6 :** choisir un lot où la comparaison à la source reste facile.

## Page 6 — Agir : tester extraction et contrôle
| Cas | Automatisation × Intégration | BAC (B / A / C) | Valeur | Coût | Risque | Complexité | Généricité |
|---|---|---|---:|---:|---:|---:|---:|
| Extraction de champs de facture | moyenne × moyenne | B : réduire la ressaisie; A : préremplir avant contrôle; C : champs extraits et reliés à la pièce | 3 | 2 | 2 | 2 | 3 |
| Transcription de demandes vocales | faible × faible | B : rendre l'audio consultable; A : retrouver un passage; C : transcription horodatée | 2 | 1 | 2 | 1 | 3 |
| Repérage visuel de défauts | moyenne × forte | B : repérer plus tôt; A : concentrer l'inspection; C : alerte visuelle localisée | 3 | 3 | 3 | 3 | 2 |

Matrice : la paire indique d'abord l'automatisation, puis l'intégration; chacune va de faible à forte. Étoiles 1 faible à 3 élevé; valeur et généricité élevées aident, coût/risque/complexité élevés demandent plus de prudence.

**Prompt d'essai :** « À partir de ces trois factures fictives, relève fournisseur, date, montant et devise. Pour chaque champ, cite la zone du document, indique “illisible” si besoin, n'invente rien et laisse toute saisie dans l'ERP à un humain. »

**Boucle :** comparer champs lus, corrections, temps et exceptions avant l'intégration.
