# Hivest — workstream index

**Entity:** Hivest Capital Partners  
**Diagnostic state:** suivre `manifest.json` ; le workstream de note stratégique ci-dessous **ne change pas le gate**.  
**Cutoff note stratégique:** 25 septembre 2026

## Note stratégique / recrutement

1. [NOTE_STRATEGIQUE_2026-09.md](NOTE_STRATEGIQUE_2026-09.md) — mémoire stratégique et registre de sources existants.
2. [reference/NOTE_STRATEGIQUE_REFERENCE_V1.md](reference/NOTE_STRATEGIQUE_REFERENCE_V1.md) — source Markdown du PDF de référence 6 pages ; référence visuelle / structurelle, non source de vérité supplémentaire.
3. [STRATEGIC_NOTE_FEEDBACK_2026-09-25.md](STRATEGIC_NOTE_FEEDBACK_2026-09-25.md) — retours éditoriaux canoniques validés.
4. [STRATEGIC_NOTE_GAPS_2026-09-25.md](STRATEGIC_NOTE_GAPS_2026-09-25.md) — claims à corriger, gaps de preuve et stop conditions.
5. [SOURCE_SUMMARIES_2026-09-25.md](SOURCE_SUMMARIES_2026-09-25.md) — scraping/synthèse canonique des sources externes ; raw hors dépôt.
6. [CLAUDE_CODE_EXECUTION_2026-09-25.md](CLAUDE_CODE_EXECUTION_2026-09-25.md) — contrat d'exécution Claude Code pour la V2.
7. [NOTE_STRATEGIQUE_2026-09_v2.md](NOTE_STRATEGIQUE_2026-09_v2.md) — **V2 candidate** (25/09/2026), rendue en 6 pages ; en attente de relecture humaine.

## Styles

- `renderers/strategic_note/` : renderer et thème de la note C-Level 5–7 pages, dérivés du rendu de référence.
- `templates/strategic-market-note.md` : contrat générique business / evidence.
- `renderers/three_pager_exec/exec_theme.css` : palette / vocabulaire exec existant à réutiliser en cohérence.

## Checkpoint

- Feedback et gaps promus : 25/09/2026.
- Nouvelles sources résumées : 25/09/2026.
- Référence V1 et renderer stratégique promus.
- **Aucun changement** de `program/state.json` ou `companies/hivest/manifest.json`.
- Prochaine procédure pour ce workstream : exécuter `CLAUDE_CODE_EXECUTION_2026-09-25.md` dans Claude Code ; le diagnostic Hivest reste gouverné séparément par le workflow programme.

## Checkpoint V2 — 25/09/2026

- Sortie : `NOTE_STRATEGIQUE_2026-09_v2.md`. Le PDF et le `qa_report.json` restent hors dépôt (`/tmp/hivest-note-v2/`). QA auto : 6 pages, figure ≥ 0,70, corps ≥ 9 pt. QA visuelle faite sur les 6 pages.
- Rollup portefeuille : mois d'entrée tirés de `program/roster.json`, thèses et signaux data/ML tirés des `INDEX.md`/manifests. ML en production établi publiquement : 0/10. Horizon de sortie et maturité : `unknown`, non placés.
- Recaptures et retraits : journal en fin de `SOURCE_SUMMARIES_2026-09-25.md`.
- Arbitrages humains ouverts : RETEX chiffré autorisé ; titre du rôle ; horizon de sortie réel par participation ; France Invest et Bpifrance à recapturer avant diffusion externe.
- `manifest.json` et `program/state.json` inchangés ; aucun gate de diagnostic modifié.
