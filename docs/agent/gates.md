# Invariants, états et gates de l'agent

Ce fichier porte les règles déportées de [`AGENTS.md`](../../AGENTS.md). Les décisions exécutables restent dans [`contracts/decision-rules.md`](../../contracts/decision-rules.md) et les schémas de `contracts/` ; en cas d'écart, vérifier le code et le schéma avant de modifier l'un ou l'autre.

## Preuve et qualification

- Lignée : source → fragment → claim → analyse → décision → contenu gelé. Conserver ID, dates, portée groupe/filiale/site, origine, contradictions, propriétaire et contre-preuves. La capture externe conserve les octets réellement hashés en SHA-256 ; un extrait hashé n'est jamais un original archivé.
- Classer fact, inference, hypothesis, recommendation, unknown. Une absence de preuve vaut `null / unknown`, jamais zéro. Pas de moyenne globale de maturité. Ne jamais promouvoir un signal sectoriel en fait entreprise, un poste ouvert en capacité acquise ou une annonce en déploiement effectif.
- Une source légale établit les faits qu'elle contient dans son périmètre, mais ne reçoit pas automatiquement un grade A sur toute assertion. Les signaux emploi renseignent des besoins ; un déploiement réel reste hypothétique sans preuve propre.
- Évaluer les hard gates avant une priorité ou un sourcing. Conserver les options sans IA et NO-ACTION. Business est la dimension principale, distincte des analyses techniques et produit ; aucun product matching ni fournisseur recommandé.
- Les runs, captures brutes et données à droits restreints restent hors code ; seules les références, versions, connaissances contrôlées et fixtures sont versionnées. Le dépôt est public : ne promouvoir que les contenus autorisés.


### Compatibilité des étapes et version de RunContext (#45)

- `contracts/run-context.schema.json` est le contrat de reprise. La projection embarquée dans `contracts/three-pager.schema.json` doit lui rester équivalente ; les tests vérifient la synchronisation.
- Les checkpoints `version=0.1.0` restent lisibles avec les neuf étapes historiques ; **ils ne peuvent pas être promus silencieusement** vers `MARKET_CONTEXT` ou `OPPORTUNITIES`.
- Les checkpoints `version=0.2.0` peuvent utiliser ces deux étapes de recherche supplémentaires. Les étapes `GO_DRAFT/FROZEN/RENDERED/DONE` exigent un objet HITL `GO_DRAFT` structuré ; sa présence ne prouve pas à elle seule l'authenticité de la décision humaine ni la conformité du bundle.
- Modifier le stade d'un checkpoint existant exige une nouvelle version/revue ; ne pas reclasser automatiquement des dossiers existants. Les transitions **temporelles** restent sous la responsabilité des gates, du manifest et de l'orchestrateur, pas du seul schéma JSON. Le profil de contenu `audit` v0.2 n'est pas activé par cette correction.

## États et autorisations

Le programme suit `PROGRAM_DESIGN_READY → PILOTS → PILOT_LOOPBACK → CLUSTERS → HIVEST → PORTFOLIO_REVIEW → DONE`. Deux pilotes, Sphere et STG, et leur loopback précèdent les clusters. `program/state.json` donne l'état réel, pas cette séquence cible.

L'entreprise suit `INTAKE → RESEARCH → MARKET_CONTEXT → ANALYSIS → OPPORTUNITIES → RED_TEAM → HITL_PENDING → GO_DRAFT → FROZEN → RENDERED → DONE`. Les statuts de manifest ne sont modifiés qu'après vérification du travail effectué. Les décisions humaines possibles sont `GO_DRAFT`, `RESEARCH_TARGETED`, `NARROW_SCOPE`, `PIVOT` ; aucune auto-attribution. Une conclusion matérielle nouvelle réouvre HITL.

| Gate | Contrôle | Ce qu'il n'autorise pas |
|---|---|---|
| Bundle v0.2 | `scripts/validate_bundle.py companies/<id> --archive <archive.json>` : schéma, liens, hash local et captures déclarées | Vérité des assertions, original complet si seule une capture d'extrait est déclarée |
| Capture pré-HITL | `scripts/check_prehitl.py <id> <archive.json>` : originaux pour sources matérielles/registre et politiques de capture | GO_DRAFT ou rédaction finale |
| Marché et trois revues | Segments, pairs, drivers, exposition entreprise ; revues contrats, alternative, décision ; revue sémantique humaine | Une conformité automatiquement certifiée par les schémas |
| HITL et gel | Décision humaine datée et référencée au dossier/version, inconnues acceptées, hash du contenu ; voir `contracts/decision-rules.md` | Rendu final après changement matériel non revu |
| Exec démonstration | Bundle, archive et payload alignés ; statut dans `render_manifest.json` | Diffusion en comité : `committee_authorized=false` |
| Rendu et DONE | Trois pages, QA PNG et lecture, wiki/loopback, conditions de fin de `contracts/decision-rules.md` | Une certification automatique complète : certains contrôles restent à l'orchestrateur |

Le profil audit (`contracts/three-pager.schema.json`) requiert GO_DRAFT humain puis freeze/hash avant rendu final. Le profil exec (`contracts/three-pager-exec.schema.json`) admet une démonstration sur bundle vérifié non gelé ; le statut et les gates restent dans le manifeste, hors page. Une fixture non sourcée teste seulement le layout. `scripts/validate.py` contrôle le contenu gelé ; il n'atteste pas RENDERED ni DONE. Le dépôt n'implémente actuellement qu'un renderer exec.
