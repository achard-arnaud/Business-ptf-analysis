# Value-chain profiles — fixed executive output and variable preview

The historical `THREE_PAGER_PORTFOLIO_AI / exec v0.3` profile requires exactly 4 support + 5 primary Porter activities and 5 drivers. Preserve that version's schema and renderer for compatible fixtures.

The [variable-activity schema](../../contracts/value-chain-view.schema.json) describes a separate candidate analytical projection. [validate_value_chain_view.py](../../scripts/validate_value_chain_view.py) checks its shape/references; [renderers/value_chain_preview/render.py](../../renderers/value_chain_preview/render.py) already renders three-page previews. The [registry](../../templates/registry.json) declares `value-chain-preview` as `preview`.

| Profile | Synthetic fixture | Business topology |
| --- | --- | --- |
| `manufacturing_porter` | [Manufacturing](../../tests/fixtures/value_chain_manufacturing_v01.json) | Purchasing, manufacturing, logistics, marketing, service and support |
| `infrastructure_asset_service` | [Asset/service](../../tests/fixtures/value_chain_asset_service_v01.json) | Origination, engineering, financing, EPC, operations, M&V and refinancing |

```bash
python renderers/value_chain_preview/render.py tests/fixtures/value_chain_asset_service_v01.json /tmp/value-chain-demo
```

HTML-only output records `qa_status=NOT_RUN`. With browser dependencies, add `--pdf` to generate PDF, three PNGs, browser QA, manifest hashes and a prepared-only artifact receipt. Then run:

```bash
python scripts/verify_render_evidence.py /tmp/value-chain-demo --profile value-chain-preview
```

The [external asset/service case analysis](../../examples/three-pagers/external-case/analysis.md) motivates a financing/contract/asset topology. The fixture *synthetic-asset-operator* contains invented test data; its outputs remain preview evidence. See [binding responsibilities](template-binding.md) and the [getting-started dependency matrix](../getting-started.md#runtime-and-configuration-boundaries).

## Remaining acceptance

Issue #43 still needs real-case migration, semantic/reader acceptance and the associated evidence trail. The preview renderer and selected browser CI are implemented increments. Their presence preserves `render_authorized_for_committee=false` and does not replace the legacy exec contract.
