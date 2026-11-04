# Contexte court, reprise et checkpoint

Cette procédure déporte les consignes de reprise de [`AGENTS.md`](../../AGENTS.md). Elle sert aussi de contrat entre deux étapes de la [skill unique](../../skills/hivest-portfolio-ai/SKILL.md).

1. Lire dans cet ordre : `program/state.json` → `companies/<id>/manifest.json` → `companies/<id>/INDEX.md` s'il existe → [workflow](../../skills/hivest-portfolio-ai/references/workflow.md). Si le manifest pointe vers `research_graph.json`, le lire seulement pour les questions actives. Vérifier la présence réelle des paths : certains dossiers sont encore en intake sans bundle.
2. Ouvrir la seule procédure de l'étape. Charger [research-graph.md](../../skills/hivest-portfolio-ai/references/research-graph.md) pour recherche en branches, dépendances, leadership/ML ou intégration ; charger les contrats JSON concernés, pas tous les schémas. Ne pas rouvrir `docs/ORIGINAL_HANDOFF.md`, tous les dossiers société ou toutes les fixtures pour une reprise ordinaire.
3. Conserver un paquet de contexte borné : entité et cutoff, état/gate, question et décision visées, chemins et hashes des entrées, top 12 claims décisifs avec contre-preuves (élargir si contradiction), trois inconnues qui inverseraient la décision, sorties attendues, owner et condition d'arrêt. Ne jamais tronquer silencieusement un claim critique au nom du budget.
4. Avant le relais, écrire dans l'index ou le dossier canonique un checkpoint court : étape achevée, artefacts sortants exacts, version/hash si disponible, validations exécutées et leurs limites, inconnues et contradictions ouvertes, gate/acteur requis, procédure suivante indiquée dans `workflow.md`. Mettre à jour le manifest seulement si le gate correspondant est effectivement passé.
5. À la reprise, comparer l'état et les hashes des entrées ; si une preuve ou une décision a changé, invalider les analyses dépendantes dans le graphe et rouvrir uniquement leur question. Une recherche parallèle éventuelle reçoit même cutoff, question/scope/ID réservés et fichiers distincts ; un intégrateur unique promeut sources, claims, index et état après déduplication.

L'index et le graph sont des cartes d'accès, non des preuves. La présence d'un `package_ref`, d'un `pre_hitl_dossier.md` ou d'un PDF ne ferme aucun gate. Pour les conditions de validation, lire [gates.md](gates.md).


## Reçu de session vérifiable (#39)

Le checkpoint portable candidat est décrit dans `contracts/session-checkpoint.schema.json` et vérifié par `scripts/session_checkpoint.py`. Il porte l'entité, le cutoff, le stage, le commit Git de base, le `run_context` exact, les `input_pins`, les `output_pins[].depends_on`, les claims décisifs/contradictoires, les validations `PASS|FAIL|NOT_RUN`, l'intégrateur, le gate et `next_action`.

La vérification exige **à la fois** le head Git attendu et les octets SHA-256 des entrées disponibles ; `CONFLICT`, `STALE` et `BLOCKED` ne constituent pas des réussites. Aucun write n'est réalisé par le validateur. Pour une source modifiée, invalider seulement ses descendants déclarés ; un changement non reconnu exige une recherche ciblée et non un effacement silencieux.

Ce reçu n'est **pas** une décision HITL : même un `human_decision_ref` syntaxiquement valide n'atteste pas que son auteur a approuvé. Le contrôle humain, le hash du bundle gelé et les gates documentés restent obligatoires. Les essais cross-model réels devront compléter les NRT synthétiques avant promotion d'un dispositif entièrement autonome.
