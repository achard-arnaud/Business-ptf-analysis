# Value-chain profiles (candidate) — separates economic reasoning from layout

The production-like `THREE_PAGER_PORTFOLIO_AI / exec v0.3` requires exactly 4 support + 5 primary Porter activities and 5 drivers. **Do not change this historical schema or renderer in place.** Its valid fixtures remain authoritative for this legacy profile.

A *candidate and non-renderable* cross-sector view is defined in `contracts/value-chain-view.schema.json`; `scripts/validate_value_chain_view.py` only checks structure and references. This is the intermediate analytical projection of `company-package.value_chain`, not a second memory, claim store or template registry entry.

| Profile | Synthetic fixture | Useful topology |
|---|---|---|
| `manufacturing_porter` | `tests/fixtures/value_chain_manufacturing_v01.json` | Purchasing, manufacturing, logistics, marketing, service and supports |
| `infrastructure_asset_service` | `tests/fixtures/value_chain_asset_service_v01.json` | Origination → engineering → financing → EPC → operations → M&V → refinancing |

The external [GreenYellow analysis](../../examples/three-pagers/greenyellow/analysis.md) shows why a financing-and-contract asset model should not be forced into a manufacturing grid. The fixture named *synthetic-asset-operator* is **invented test data**, not an observed GreenYellow rollout, a case with GO_DRAFT, or a verified business claim.

**Next before #43 can close:** define a new versioned render profile/adapter mapping `activities` (variable count) and `drivers` to three landscape pages; preserve evidence lineage and ≥9pt; render two actual PDFs; run visual QA per page, positive/negative NRT and human reader acceptance. Until then `render_authorized=false` and the template registry must not claim this candidate as ready.
