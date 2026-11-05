# Checkpoint 06 — Backlog et scaffold sémantique

Date : 5 novembre 2026  
État : G8 et G9 clos au niveau contrat candidat; non fusionné.

## G8 — Catalogue d'environ 70 cas

- Catalogue distinct du binding de fiche; extensible jusqu'à 500 entrées.
- ID stable, clé de dédoublonnage, champ duplicate_of, statut, sources/locators et liens vers piliers.
- Les entrées partielles restent importables; inconnus non inventés.
- La sélection dans une fiche reste bornée à 3–5 cas.
- Le schéma ne peut pas imposer l'unicité d'un champ ID sur des objets dans JSON Schema standard; le contrôle des collisions et doublons sémantiques est exigé à l'ingestion et documenté.

## G9 — Scaffold

- Six pages sémantiques avec rôles orientation, teach-back, carte système, trajectoire, chaîne de valeur et backlog.
- Slots d'ancrage stables définis par page; binding et scaffold emploient le même registre de block IDs.
- Structure HTML décrite, aucun CSS, token graphique, règle de pagination ou rendu ajouté.
- Les fiches restent du contenu indépendant du scaffold.

**Verdict :** architecture des contrats prête à recevoir le catalogue et le renderer. La revue finale doit encore vérifier les liens inter-dépôts, le statut CI sur les HEAD courants et le caractère candidat des six modules.

**Prochaine porte :** G10 — revue finale.
