# Renderer — strategic-market-note, profil `exec`

Markdown + directives légères → HTML → PDF A4 portrait, rendu « cabinet de conseil » pour un lectorat C-Level (5 à 7 pages).

```bash
pip install markdown "playwright==1.56.0" pillow  # version alignée sur chromium-1194 préinstallé
npm i -g @mermaid-js/mermaid-cli@11             # mmdc 12 ne connaît plus l'option -w utilisée par build.py
python renderers/strategic_note/build.py renderers/strategic_note/sample_note.md --out /tmp/snote --pages 1-3
```

| Élément | Syntaxe |
|---|---|
| Couverture | front matter : `kicker`, `title`, `subtitle`, `author`, `date`, `horizon`, `audience`, `footer`, `sources_title`, `sources_intro` |
| En bref | `::: tldr [Label]` + liste numérotée |
| KPI | `::: kpis` + lignes `- VALEUR \| libellé[^src]` (4 conseillées) |
| Encadrés | `::: callout`, `::: callout-gold`, `::: story` (+ label optionnel) |
| Deux colonnes | `::: cols` … `+++` … `:::` |
| Section numérotée | `## 1 — Titre` ; accroche : paragraphe suivi de `{: .lede}` |
| Figure | bloc ```` ```mermaid ```` avec `%% caption:`, `%% maxh:` (mm), `%% width:` (px, gantt) |
| Saut de page | `\newpage` |
| Sources | notes `[^id]` — renumérotées dans l'ordre de première citation |

**QA (`qa_report.json`, code retour 2 si échec)** : nombre de pages dans `--pages`, échelle de chaque figure ≥ 0,70 (sinon transposition LR↔TB automatique, source Mermaid conservée à côté du PNG), corps ≥ 9 pt, texte secondaire ≥ 8 pt. La relecture visuelle page par page reste obligatoire.

Palette et typographie : navy/blue/teal/gold hérités de `Hivest-ptf-analysis/renderers/three_pager_exec/exec_theme.css` ; titres Source Serif 4, texte Inter (repli Carlito / Liberation).

## Frontière avec la recherche et la narration

Ce README décrit **uniquement le renderer de la note stratégique C-Level**, pas une skill de recherche. Les sources, leurs fragments, claims, limitations et feedback sont organisés dans `companies/hivest/INDEX.md` et le contrat `templates/strategic-market-note.md` ; le parcours de diagnostic par participation suit `skills/hivest-portfolio-ai/SKILL.md` et ses propres gates. Le renderer prend le Markdown structuré comme **entrée**, sans ajouter de faits ni accorder GO_DRAFT. Voir [architecture ETL](../../docs/architecture/end-to-end-etl.md).
