# Schema field catalogue

Generated from the inspected company-package and strategic-context schemas on 2026-11-16. This lists declared property paths; consult the linked JSON for conditional requirements, exact enums, references and validation. Business semantics, origins, grain and calculations are in [DATA_DICTIONARY.md](DATA_DICTIONARY.md). Layout-only schemas have their own profile contracts.

## company-package

Source: [company-package.schema.json](../../contracts/company-package.schema.json); SHA-256 `7167234b2cd0edc1e6edfa48df326cb35a0d07eca6ee20717724f6a305f4bce5`.

| Property path | Declared shape |
| --- | --- |
| `/version` | enum |
| `/entity_id` | string |
| `/cutoff` | string |
| `/sources` | array |
| `/sources[]/id` | string |
| `/sources[]/url` | string |
| `/sources[]/scope` | enum |
| `/sources[]/entity_ids` | array |
| `/sources[]/published_at` | union |
| `/sources[]/accessed_at` | string |
| `/sources[]/grade` | enum |
| `/sources[]/origin_id` | string |
| `/sources[]/source_type` | enum |
| `/sources[]/access_status` | enum |
| `/sources[]/snapshot_uri` | string |
| `/sources[]/sha256` | string |
| `/sources[]/rights` | string |
| `/sources[]/capture_kind` | enum |
| `/sources[]/capture_policy` | enum |
| `/sources[]/hash_scope` | enum |
| `/fragments` | array |
| `/fragments[]/id` | string |
| `/fragments[]/source_id` | string |
| `/fragments[]/locator` | string |
| `/fragments[]/excerpt` | string |
| `/fragments[]/sha256` | string |
| `/claims` | array |
| `/claims[]/id` | string |
| `/claims[]/entity_id` | string |
| `/claims[]/scope` | enum |
| `/claims[]/statement` | string |
| `/claims[]/status` | enum |
| `/claims[]/confidence` | enum |
| `/claims[]/fragment_refs` | array |
| `/claims[]/basis_claim_refs` | array |
| `/claims[]/contradiction_refs` | array |
| `/claims[]/observed_at` | union |
| `/claims[]/valid_until` | union |
| `/claims[]/owner` | string |
| `/claims[]/validation_question` | string |
| `/claims[]/deployment_stage` | enum |
| `/maturity` | object |
| `/maturity/dimensions` | array |
| `/maturity/dimensions[]/id` | enum |
| `/maturity/dimensions[]/score` | enum |
| `/maturity/dimensions[]/status` | enum |
| `/maturity/dimensions[]/confidence` | enum |
| `/maturity/dimensions[]/claim_refs` | array |
| `/maturity/dimensions[]/counter_evidence` | array |
| `/maturity/dimensions[]/unknowns` | array |
| `/maturity/dimensions[]/rationale` | string |
| `/maturity/dimensions[]/scope` | string |
| `/maturity/summary` | string |
| `/maturity/bottlenecks` | array |
| `/maturity/applicable_domains` | array |
| `/maturity/excluded_domains_rationale` | array |
| `/value_chain` | array |
| `/value_chain[]/id` | string |
| `/value_chain[]/name` | string |
| `/value_chain[]/claim_refs` | array |
| `/value_chain[]/value_creation` | string |
| `/value_chain[]/friction` | string |
| `/value_chain[]/control_points` | array |
| `/value_chain[]/vrio` | string |
| `/value_chain[]/digitalisation` | string |
| `/value_chain[]/ai_opportunity_refs` | array |
| `/value_chain[]/constraints` | array |
| `/use_cases` | array |
| `/use_cases[]/id` | string |
| `/use_cases[]/title` | string |
| `/use_cases[]/vertical` | enum |
| `/use_cases[]/workflow` | string |
| `/use_cases[]/problem` | string |
| `/use_cases[]/value_mechanism` | string |
| `/use_cases[]/status` | enum |
| `/use_cases[]/company_claim_refs` | array |
| `/use_cases[]/sector_claim_refs` | array |
| `/use_cases[]/business_owner_hypothesis` | string |
| `/use_cases[]/data_dependencies` | array |
| `/use_cases[]/technology_dependencies` | array |
| `/use_cases[]/adoption_dependencies` | array |
| `/use_cases[]/gates` | array |
| `/use_cases[]/gates[]/name` | string |
| `/use_cases[]/gates[]/status` | enum |
| `/use_cases[]/gates[]/claim_refs` | array |
| `/use_cases[]/gates[]/reason` | string |
| `/use_cases[]/priority_state` | enum |
| `/use_cases[]/ratings` | object |
| `/use_cases[]/ratings/economic_value` | enum |
| `/use_cases[]/ratings/strategic_value` | enum |
| `/use_cases[]/ratings/feasibility` | enum |
| `/use_cases[]/ratings/time_to_value` | enum |
| `/use_cases[]/ratings/repeatability` | enum |
| `/use_cases[]/ratings/adoption` | enum |
| `/use_cases[]/ratings/risk` | enum |
| `/use_cases[]/ratings/portfolio_reuse` | enum |
| `/use_cases[]/family` | enum |
| `/use_cases[]/horizon` | enum |
| `/use_cases[]/sourcing_posture` | enum |
| `/use_cases[]/baseline_without_ai` | string |
| `/use_cases[]/reversibility` | string |
| `/use_cases[]/unknowns` | array |
| `/use_cases[]/validation_question` | string |
| `/use_cases[]/driver_refs` | array |
| `/use_cases[]/value_strategy` | enum |
| `/use_cases[]/technique_class` | enum |
| `/use_cases[]/kpi` | string |
| `/use_cases[]/stop_condition` | string |
| `/use_cases[]/cost_base_id` | union |
| `/use_cases[]/is_prerequisite` | boolean |
| `/use_cases[]/double_count_justification` | union |
| `/use_cases[]/new_demand_hypothesis` | union |
| `/use_cases[]/customer_test` | union |
| `/strategic_positions` | array |
| `/strategic_positions[]/activity_id` | string |
| `/strategic_positions[]/centrality` | enum |
| `/strategic_positions[]/differentiation` | enum |
| `/strategic_positions[]/claim_refs` | array |
| `/strategic_positions[]/rationale` | string |
| `/strategic_positions[]/sourcing_posture` | enum |
| `/strategic_positions[]/reversibility` | string |
| `/contradictions` | array |
| `/unknowns` | array |
| `/market_context` | object |
| `/market_context/arenas` | array |
| `/market_context/arenas[]/id` | string |
| `/market_context/arenas[]/name` | string |
| `/market_context/arenas[]/buyer_value` | string |
| `/market_context/arenas[]/claim_refs` | array |
| `/market_context/peers` | array |
| `/market_context/peers[]/name` | string |
| `/market_context/peers[]/signal` | string |
| `/market_context/peers[]/comparability_limit` | string |
| `/market_context/peers[]/claim_refs` | array |
| `/market_context/coverage` | object |
| `/market_context/coverage/demand_price` | object |
| `/market_context/coverage/demand_price/status` | enum |
| `/market_context/coverage/demand_price/gap_impact` | string |
| `/market_context/coverage/demand_price/next_research` | string |
| `/market_context/coverage/competition` | object |
| `/market_context/coverage/competition/status` | enum |
| `/market_context/coverage/competition/gap_impact` | string |
| `/market_context/coverage/competition/next_research` | string |
| `/market_context/coverage/materials_energy` | object |
| `/market_context/coverage/materials_energy/status` | enum |
| `/market_context/coverage/materials_energy/gap_impact` | string |
| `/market_context/coverage/materials_energy/next_research` | string |
| `/market_context/coverage/productivity_quality` | object |
| `/market_context/coverage/productivity_quality/status` | enum |
| `/market_context/coverage/productivity_quality/gap_impact` | string |
| `/market_context/coverage/productivity_quality/next_research` | string |
| `/market_context/coverage/regulation` | object |
| `/market_context/coverage/regulation/status` | enum |
| `/market_context/coverage/regulation/gap_impact` | string |
| `/market_context/coverage/regulation/next_research` | string |
| `/market_context/coverage/customers_upmarket` | object |
| `/market_context/coverage/customers_upmarket/status` | enum |
| `/market_context/coverage/customers_upmarket/gap_impact` | string |
| `/market_context/coverage/customers_upmarket/next_research` | string |
| `/drivers` | array |
| `/drivers[]/id` | string |
| `/drivers[]/rank` | integer |
| `/drivers[]/external_signal_claim_refs` | array |
| `/drivers[]/exposure_claim_refs` | array |
| `/drivers[]/exposure_hypothesis` | union |
| `/drivers[]/economic_mechanism` | string |
| `/drivers[]/value_strategies` | array |
| `/drivers[]/kpis` | array |
| `/drivers[]/baseline_status` | enum |
| `/drivers[]/counter_evidence_refs` | array |
| `/drivers[]/owner_hypothesis` | string |
| `/drivers[]/rank_inversion_condition` | string |
| `/strategic_context_ref` | string |

## strategic-context

Source: [strategic-context.schema.json](../../contracts/strategic-context.schema.json); SHA-256 `4b9348712b91ac4945fab192561294b952dbc0e68fc0b382c474793760020cfa`.

| Property path | Declared shape |
| --- | --- |
| `/entity_id` | string |
| `/cutoff` | string |
| `/ml_strategy` | object |
| `/leaders` | array |
| `/leaders[]/role` | string |
| `/leaders[]/person` | string / null |
| `/leaders[]/exact_title` | string / null |
| `/leaders[]/scope` | enum |
| `/leaders[]/status` | enum |
| `/leaders[]/source_refs` | array |
| `/leaders[]/next_question` | string |
| `/leaders[]/promoter_signal` | string / null |
| `/leaders[]/ownership_scope` | string / null |
| `/segments` | array |
| `/segments[]/id` | string |
| `/segments[]/name` | string |
| `/segments[]/revenue_share` | integer |
| `/segments[]/revenue_year` | integer |
| `/segments[]/revenue_estimate_meur` | string / null |
| `/segments[]/share_basis` | string |
| `/segments[]/company_growth` | number / null |
| `/segments[]/market_growth` | number / null |
| `/segments[]/relative_market_share` | number / null |
| `/segments[]/bcg` | string / null |
| `/segments[]/claim_refs` | array |
| `/frameworks` | object |
| `/driver_ids` | array |
| `/opportunity_links` | array |
| `/opportunity_links[]/use_case_id` | string |
| `/opportunity_links[]/driver_id` | string |
| `/opportunity_links[]/value_strategy` | string |
| `/opportunity_links[]/method` | string |
| `/opportunity_links[]/kpi` | string |
| `/opportunity_links[]/baseline` | string |
| `/opportunity_links[]/activity_id` | string |
| `/opportunity_links[]/page` | object/conditional |
| `/opportunity_links[]/ml_required` | boolean |
| `/opportunity_links[]/decision_status` | enum |
| `/opportunity_links[]/driver_label` | string |
| `/prerequisites` | array |
| `/shortlist_ids` | array |
| `/reviews` | array |
| `/reviews[]/kind` | enum |
| `/reviews[]/verdict` | enum |
| `/reviews[]/path` | string |
| `/coverage` | object |
| `/critical_questions` | array |
| `/render_status` | string |
| `/artifact_hashes` | object |
| `/version` | object/conditional |
