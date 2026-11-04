# Contrat de handoff intermodèles — recherche et étape

**S'applique seulement** lorsqu'un travail est transféré entre modèles/sessions. La skill métier et les gates restent dans `skills/hivest-portfolio-ai/` et `docs/agent/gates.md`.

## Format et responsabilités
- Producteur : question bornée, `entity_id`, `cutoff`, stage, `run_context` pinned, `inputs` pinned, sortie attendue, budget et stop condition.
- Consommateur : annonce capacités **réellement disponibles** dans la session (`available|deferred|unavailable`), vérifie les octets accessibles et les références avant d'affirmer une preuve.
- Intégrateur unique : déduplique et promeut les claims après vérification de leurs sources ; aucune sous-session ne promeut un statut ni n'approuve un GO_DRAFT.
- `READY` = capacités requises présentes **selon le reçu déclaratif** ; `RECOVERABLE` = snapshot exact référencé ou différé ; `BLOCKED` = arrêt traçable. **Une validation JSON n'atteste pas l'accès externe.**

## Bootstrap / fallback frugal
1. Charger `program/state.json`, le manifest et l'index de l'entité, puis le contrat de l'étape active.
2. Charger le `research-handoff` (schéma `contracts/research-handoff.schema.json`) et uniquement les artefacts d'entrée déclarés.
3. Tester capacités utiles (GitHub read/write, Python, navigateur, archive) séparément. Ne pas confondre clone Git local et API connecteur.
4. Si une capacité est absente, appliquer un snapshot **déjà vérifié et épinglé**, ou reporter le travail. Pas de téléchargement inventé ni d'accès déclaré par déduction.
5. Le retour est source→fragment→claim avec contradictions et preuves de lecture ; l'intégrateur réconcilie versions et hashes avant de mettre à jour les connaissances.

Le champ `budget` borne recherches et sources ; aucune économie de tokens n'est revendiquée sans mesure du runtime. Pas d'agents secondaires obligatoires, et aucun changement des gates métier.

Exécuter : `python scripts/validate_handoff.py tests/fixtures/research_handoff_v01.json` ; contrôles négatifs : `python -m unittest tests.test_research_handoff -v` (ou discovery). Statut renvoyé `METADATA_VALID` : aucun droit, aucun HITL, aucune vérité des sources certifiés.
