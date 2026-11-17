# Revue du contrat du manifeste — 17 novembre 2026

## Objectif, contraintes et baselines

Garantir que les appels de l'agent consomment un manifeste valide et des dépendances sélectionnées avant de créer un run. Préserver les cas historiques, l'absence de fallback implicite, les bindings propres à chaque dépôt et la légèreté de la skill.

Versions relues : Business-ptf-analysis eeba98ddd00dca04306545d085fc821831672ac9 ; storytelling main 664391438be5c9d950dd33d3a9b6a19db35c775e. Le harvest Candidatures et ses sources restent dans harvest-contract-runtime-2026-11-17.md ; ils ne sont pas réexécutés ni dupliqués. Issues : Business #75 ; storytelling #340, suites bornées de #73/#338.

## Reproduction et disposition ADR

Dans une copie temporaire des fichiers BUILD référencés, remplacer renderer.args (liste) par la chaîne "--pdf". Le contrôle avant correction répond exactement contracts_pass, engine_version=1.0.0, templates=1. Aucun cas métier n'a été créé pour cette reproduction.

Constat : les schémas I/O d'artefacts existaient, mais le manifeste était analysé par quelques contrôles Python sans schéma global consommé. Les ADR-0002 et ADR-1008 restent cohérents ; leur prescription devait être appliquée aussi au manifeste et aux dépendances d'adapter. La correction porte sur cette première couche fautive.

## Prescription et vérification

- case-process.schema.json valide les types, étapes, profils, dépendances déclarées et cinq axes de loopback.
- renderer et payload_schema sont déclarés ensemble. L'argv est une liste de chaînes.
- Le moteur exige leurs chemins dans les refs du profil, puis valide le schéma de payload lui-même.
- Une demande de rendu sans adapter est refusée avant toute création de dossier/état.
- La release commune contient l'empreinte du nouveau schéma ; toutes les surfaces exécutent le même moteur.

Régressions : string argv ; schéma non épinglé ; schéma invalide ; axe inconnu ; rendu demandé sans adapter. Les scénarios valides de chaîne A0–A4, de mémo technique et de sous-processus renderer restent exécutés.

## Limites et falsifier

Un manifeste correctement typé ne prouve pas que l'adapter produira un bon document. Le renderer doit encore être exécuté, ses fichiers contrôlés et les pages relues. Les jugements, recherches et décisions métier restent attribués à l'agent/lecteur. Aucun coût ou gain fournisseur n'est mesuré ici.

Réexaminer si un manifeste invalide ou un adapter non sélectionné peut créer un cas ou être lancé. La fixture discriminante doit précéder toute nouvelle correction. Les anciennes traces de release restent historiques ; aucune étape ancienne n'est marquée accomplie rétroactivement.

## Source de patterns relue

Candidatures-nice main bda80b7ecd480fee295d211d9d80ae6abf8a1f69 : relecture ciblée de workflow/process-manifest.json, workflow/loopback-manifest.json et docs/ADR-007-RUN-BUILD.md. Les frontières observées confirment le harvest antérieur : contrat de processus référencé, instructions par phase, investigations chargées après signal, consommateur de loopback et reprise historique explicite. Aucun script ni aucune donnée de candidature n'a été exécuté ou transféré. Cette couverture ciblée ne constitue pas un audit de tous les changements du dépôt source.
