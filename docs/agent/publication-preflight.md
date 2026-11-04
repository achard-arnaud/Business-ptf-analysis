# Gate de publication — contrôle conservateur, jamais auto-GO_DRAFT

## Autorités et limites

`scripts/publication_preflight.py` reçoit un manifest de rendu, un reçu d'artefact, les **octets réels** du PDF, éventuellement une relecture distante indépendante, un verdict de bundle gelé et une revue de lecteur liée au même SHA PDF. Les statuts de validation de métadonnées ne sont **pas** des signatures ni des approbations humaines authentifiées.

Le contrôleur fail-closed refuse les renderers preview, les QA absentes, les sources PDF modifiées, les artefacts non publiés, l'absence de relecture distante, les empreintes bundle/payload discordantes, le manque de preuve de freeze/HITL et les revues de lecture périmées.

Même dans un cas entièrement renseigné, le résultat est `AWAIT_AUTHENTICATED_HUMAN_RELEASE` et jamais `committee_authorized=true`. La décision réelle doit être prise et conservée par la personne autorisée, via le workflow qui possède cette autorité. Aucun champ contrôlé par un agent ne peut lui attribuer la qualité d'approbateur.

### Recommandations d'implémentation restantes

- Construire `VERIFIED_FROZEN_BUNDLE` via le validateur canonique `validate_freeze` sur un vrai bundle avec archive autorisée ; jamais à partir d'une fixture de modèle.
- Relire les octets du PDF depuis le stockage ou le connecteur **après publication**, puis conserver le reçu corrélé au commit/URI.
- Revue du lecteur sur les PNG du même PDF, avec empreinte de la version et une identité humaine validée par le système.
- N'autoriser la publication comité qu'après ces étapes et une décision humaine authentifiée. Sans cette capacité, garder le rendu en `DEMO_ONLY`.

Ce document ne livre pas un protocole d'authentification de comité ; #29 reste ouvert pour la preuve E2E réelle.
