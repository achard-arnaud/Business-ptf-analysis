# Value chain preview — three-page landscape candidate v0.1

## Scope

Data comes from `contracts/value-chain-view.schema.json`, **not** the historical `three-pager-exec.schema.json`. The renderer is intentionally separate from the immutable exec v0.3 contract and layout. Profiles supported: `manufacturing_porter` and `infrastructure_asset_service`.

Pages: (1) business model / drivers, (2) activities and value contribution, (3) candidate opportunities and baseline without AI. Each page carries an explicit synthetic/unapproved footer.

## Run

```sh
python renderers/value_chain_preview/render.py tests/fixtures/value_chain_asset_service_v01.json /tmp/asset-preview --pdf
python renderers/value_chain_preview/render.py tests/fixtures/value_chain_manufacturing_v01.json /tmp/manufacturing-preview --pdf
```

`--pdf` requires the Playwright/Chromium renderer already used in `three_pager_exec`. It creates HTML, PDF, three page PNGs, `qa.json`, and `render_manifest.json`. No `--pdf`: the manifest states `qa_status=NOT_RUN`, never a false PASS.

**Never promote this template into committee output.** The fixtures have no evidence archive, human approval, source-grade verification, or business owner. An actual company bundle must pass lineage / rights / gate checks via the canonical pipeline before its claims can enter an approved publication. A machine layout PASS still requires reader review.
