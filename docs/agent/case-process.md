# Cas isolés et appels contrôlés

Pour une nouvelle instance, utiliser le moteur du projet :

```bash
python scripts/case_runtime.py check
python scripts/case_runtime.py init --case <case-id> --input intake.json
python scripts/case_runtime.py begin --case <case-id> --stage A0 --actor manual_agent
```

Le contrat d'intake est `contracts/case-artifacts.schema.json#/$defs/intake` : entity_id,
objective, constraints, cutoff, template_id, render_requested. Un template absent bloque.
Les cas RUN vont dans `data/cases/<case-id>/`, ignoré par Git ; les fixtures synthétiques
curatées vont dans `tests/`. Ne pas migrer les anciens dossiers par simple renommage.
La création exclusive refuse un identifiant existant et crée le graphe avant toute collecte.

`begin` émet un paquet de références avec les empreintes BUILD et celles des dépendances,
le contrat de sortie, le profil du template et le chemin exact du `result.json` attendu.
L'agent lit les sources et écrit cet artefact dans le dossier de la tentative ; le moteur
ne recherche pas le Web, ne sollicite aucun LLM et ne prétend pas observer les lectures
internes de l'hôte. `complete` contrôle les octets soumis, les schémas et les références.

| Étape | Entrée disponible | Artefact et contrôle |
| --- | --- | --- |
| A0 preuves | Intake | Captures locales, URL, date, locator, couverture de lecture |
| A1 modèle | A0 | Sources/fragments/claims en nodes ; edges typés et provenance |
| A2 structure | A0/A1 | Décision, objection, falsifier, sections et claim IDs |
| A3 rédaction | A1/A2 | Prose par section ; même mapping de claims que le scaffold |
| A4 revue | A0–A3 | Trois revues distinctes, et reçu PDF/QA si demandé |

```bash
python scripts/case_runtime.py complete --case <case-id> --stage A0
python scripts/case_runtime.py status --case <case-id>
python scripts/case_runtime.py invalidate --case <case-id> --stage A1 --reason "source corrigée"
```

Les anciennes tentatives restent présentes. L'invalidation suit le DAG du manifeste,
conserve les étapes amont et ne réépingle jamais silencieusement une nouvelle méthode.
Un changement de BUILD impose une nouvelle instance ou une migration explicitement
développée ; cette version n'offre pas de migration automatique de pins.

`state.json` est l'autorité de l'état et du journal `events` : séquence, date, étape,
tentative, acteur déclaré, résultat et empreintes. Écriture atomique et verrou local
évitent les mises à jour concurrentes perdues. Usage fournisseur et temps de lecture
restent inconnus si l'hôte ne les expose pas. Ce journal n'est pas une signature.

Le reçu A4 contrôle la présence et l'empreinte du PDF, ses pages physiques, `qa.json`
et les comptes QA. Il ne constitue ni une preuve de vérité des claims ni une
approbation métier. Les revues déclarées restent attribuées à leur auteur.

## Renforcement après incident

Utiliser `loopback --case <id> --proposal loopback/proposal.json` avec le contrat
`#/$defs/loopback`. Axes : architecture, bugfix, ci, runtime, skill. Le dispatch du
manifeste renvoie les questions et contrôles de l'axe. Relier l'observation à une preuve
locale hachée, à l'état exact, aux ADR concernés, à l'objectif/contraintes et à l'issue.
Choisir `no_change` ou une expérience avec hypothèse, falsifier, protocole, régression,
arrêt et rollback. Mesures : unité explicite, avant/après sourcés ou valeurs nulles.
Une estimation n'est pas une mesure observée.

Le validateur n'applique aucun correctif. Le BUILD autorisé corrige la première couche
fautive, exécute la régression et consigne les résultats dans l'issue et le reçu.
Revoir l'ADR si son hypothèse est invalidée ; renforcer l'implémentation si l'ADR reste
valide. La qualité d'une analyse n'est pas déduite d'une CI verte.

## Appel effectif du renderer

Quand render_requested=true, A3 doit fournir payload_ref vers un payload local à la
même tentative. Le profil impose son schéma et un adapter épinglé ; un profil sans
adapter bloque explicitement au lieu de produire un faux succès. Le profil exec
entreprise pointe le renderer Chromium canonique et ses dépendances locales.

Après begin A4, appeler `python scripts/case_runtime.py render --case <case-id>`.
Le moteur invoque le renderer par argv, conserve renderer.log, code de retour,
empreintes du payload/renderer et des fichiers, puis émet un reçu de rendu. Reporter
ce reçu exact dans le champ render du résultat A4, avec les trois notes de revue.
Une déclaration manuelle de render non produite par cet appel est refusée.
Le contrôle des pages physiques et de qa.json reste distinct de la lecture visuelle.
Le renderer n'est pas automatiquement disponible pour tous les templates de notes.
