# Contrat d'injection du backlog — environ 70 cas

Le backlog complet vit dans un catalogue séparé; une fiche ne charge que 3 à 5 cas. Le schéma canonique est lié dans le manifest de programme et versionné dans le dépôt de transit.

## Règles d'ingestion

- Préserver un ID stable par cas; ne jamais réutiliser un ID pour un autre processus.
- Capturer provenance et locator sans recopier les documents sources; les données brutes restent dans leur espace autorisé.
- Définir une clé de dédoublonnage (fonction + processus + douleur + résultat attendu); détecter les collisions d'ID et les doublons sémantiques avant sélection.
- Pour un doublon retenu, conserver l'ID canonique et renseigner l'ID redirigé dans duplicate_of; ne pas effacer l'historique.
- Autoriser les champs métier inconnus à rester null, absents ou « unknown » selon le schéma. Ne pas compléter par intuition.
- Garder séparés les liens vers les 17 piliers; les rattachements restent proposés jusqu'à réception du syllabus exact.
- Le catalogue accepte jusqu'à 500 cas pour absorber plusieurs lots; la capacité initiale planifiée est d'environ 70.
- Le classement n'est pas une validation. Hard gates et revue métier précèdent score, sélection et pilote.

## Projection dans une fiche

Le binding reçoit une référence au catalogue et les 3 à 5 IDs retenus. Pour chaque cas sélectionné, il transporte problème, processus, ICP métier, entrée/sortie, automation, intégration, BAC, notation, contrôle humain, mesure et sources. La fiche ne duplique pas le catalogue complet.
