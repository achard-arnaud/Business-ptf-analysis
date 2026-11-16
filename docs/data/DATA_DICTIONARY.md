# Data dictionary — evidence, analysis and decision fields

The diagnostic's grain is **one company, one research cutoff and one decision question**. [Schema fields](SCHEMA_FIELDS.md) inventories every declared property in the company package and strategic context; their schemas retain exact type, enum and conditional-required authority. This dictionary defines the business meaning, origin, grain and calculations. Presentation fields remain in [profile-specific contracts](../architecture/template-binding.md).

## Identity, dates, missing values and units

| Field / convention | Meaning and source | Rule / limitation |
| --- | --- | --- |
| `version`, `entity_id`, `cutoff`, `strategic_context_ref` | Contract version, company identity, research date and linked context | Package/context must agree on company and cutoff; v0.2 expects `strategic_context.json`. |
| `id`, `*_refs`, `*_id` | Object identity and links within the relevant collection | IDs are collection-local; use the correct source/fragment/claim/activity/use-case registry. |
| `published_at`, `accessed_at` | Source publication and actual consultation | Publication fits the cutoff; consultation may occur later. Unknown publication retains null where allowed. |
| `observed_at`, `valid_until` | Claim observation and expiry | Observation cannot precede its cited publication; scored/gate evidence must remain fresh at cutoff. |
| `score=null`, `status=unknown` | Unmeasured maturity | Null retains uncertainty. Numeric zero is rejected for maturity. |
| `revenue_share`, `revenue_year` | Integer percentage points on 0–100 and reporting year | Bundle checks shares sum to 100 and year fits the cutoff. |
| `revenue_estimate_meur` | EUR millions as decimal string, or null | Preserve reporting perimeter and source basis. No currency conversion engine. |
| `company_growth`, `market_growth`, `relative_market_share`, `bcg` | Growth, market-share ratio and analytical quadrant | Record unit, period and denominator in evidence; schema does not fix growth units. BCG requires both market axes. |
| `kpi`, `kpis`, `baseline`, `baseline_without_ai` | Textual outcome measure and situation of reference | Case analysis must specify formula, unit, period, owner and attribution. These fields do not execute calculations. |

## Evidence objects — company package

Each grouped row shares a grain and origin. Exact leaf paths are listed in the [field catalogue](SCHEMA_FIELDS.md).

| Object / fields | Grain and origin | Meaning / rule |
| --- | --- | --- |
| `sources`: `url`, `scope`, `entity_ids` | One source, acquired and scoped | Company/sector/portfolio applicability; a sector pattern retains its external scope. |
| `sources`: `grade`, `source_type`, `access_status`, `origin_id` | Analyst qualification of one source | Grades A–E are source classes. Reused URL/hash keeps a common origin; source independence requires review. |
| `sources`: `snapshot_uri`, `sha256`, `rights`, `capture_kind`, `capture_policy`, `hash_scope` | Authorised external capture | Pairs `full_original/original_bytes` or `selected_excerpt/excerpt_utf8`. Hash actual captured bytes; URI availability is a separate check. |
| `fragments`: `source_id`, `locator`, `excerpt`, `sha256` | One located passage from a read source | Fragment hash uses NFC-normalised UTF-8; keep locator and wording. |
| `claims`: `statement`, `entity_id`, `scope`, `status`, `confidence`, `deployment_stage` | One proposition, extracted or inferred | Distinguish epistemic status, confidence and deployment stage; company scope matches the bundle. |
| `claims`: `fragment_refs`, `basis_claim_refs`, `contradiction_refs` | Direct evidence, inferential basis and counterclaims | Facts require fragments; inference needs source anchoring; basis graph must be acyclic. |
| `claims`: `owner`, `validation_question` | Responsible party / unresolved question | Supports bounded follow-up and review. |

## Analytical objects — company package

| Object / fields | Grain and origin | Meaning / rule |
| --- | --- | --- |
| `maturity.dimensions` | One of eight dimensions; evidence-based assessment | IDs: strategy/value, operating model, data/knowledge, technology/platform, delivery, people/adoption, security/risk and breadth. `score` is ordinal 1–4 or null; scope, confidence, rationale, claims, counter-evidence and unknowns accompany it. |
| `maturity.summary`, `bottlenecks`, `applicable_domains`, `excluded_domains_rationale` | Company synthesis | State applicability and limits. No global numeric maturity average. |
| `value_chain` | One business activity from company analysis | Name, value creation, friction, control points, VRIO, digitalisation, constraints, claim refs and opportunity refs. |
| `market_context.arenas`, `peers` | One market arena / comparator | Buyer value, external signal, comparability limits and claim references. |
| `market_context.coverage` | One of six research axes | Demand/price, competition, materials/energy, productivity/quality, regulation, customer upmarket; each records status, gap impact and next research. Coverage differs from company capability. |
| `drivers` | One proposed economic driver | External signal → company exposure claim or explicit hypothesis → economic mechanism. Retain rank, rank inversion condition, strategy, KPIs, baseline, owner hypothesis and counter-evidence. Ranking has no automatic formula. |
| `use_cases`: identity, `vertical`, `workflow`, `problem`, `value_mechanism`, `status` | One operational opportunity | Observed cases require deployed company evidence. Hypothetical opportunities remain explicit. |
| `use_cases`: `company_claim_refs`, `sector_claim_refs`, `driver_refs` | Evidence and driver mapping | Resolve each scope separately; v0.2 non-prerequisites require a driver. |
| `use_cases`: owner and data/technology/adoption dependencies | Proposed delivery conditions | Verify owner and prerequisites through research or a pilot. |
| `use_cases.gates`, `priority_state` | Five mandatory prerequisite decisions | `data_rights`, `security_ot`, `human_control`, `ownership`, `feasibility`. Any fail→blocked; otherwise any unknown→validation_required; all pass→eligible. Pass requires fresh company facts. |
| `use_cases.ratings` | Eight ordinal ratings | Economic/strategic value, feasibility, time to value, repeatability, adoption, risk, portfolio reuse. High risk is unfavourable; high adoption means readiness. No automatic weighted total. |
| `use_cases.family`, `horizon` | Delivery time category | Validator pairs quick_win/0–6, structural/6–18 and transformation/18–36 months. These are indicative horizons. |
| `use_cases`: sourcing, baseline, reversibility, unknowns, validation question | Case qualification | Compare AI with a non-AI baseline and no action; retain control and exit conditions. |
| `use_cases`: `value_strategy`, `technique_class`, `kpi`, `stop_condition` | Economic intent, technical family and test | KPI remains textual; operational formula is case-specific. |
| `use_cases`: `cost_base_id`, `double_count_justification` | Shared cost base / overlap explanation | Repeated reduction/avoidance bases require explanations for both uses. This is an overlap check, not proof of net benefit. |
| `use_cases`: `is_prerequisite`, `new_demand_hypothesis`, `customer_test` | Enabling work / demand test | BLUE_OCEAN requires a demand hypothesis and customer test. |
| `strategic_positions` | One activity's position in a 3×3 sourcing frame | Centrality, differentiation, evidence, rationale, sourcing posture and reversibility. Remains an argued strategic choice. |
| `contradictions`, `unknowns` | Company-level objections / gaps | Remain open until the appropriate evidence and decision process resolves them. |

## Strategic context

| Object / fields | Grain and origin | Rule / limitation |
| --- | --- | --- |
| `ml_strategy` | Observed and proposed ML strategy from case analysis | Bundle checks observed status/claim refs and a search artifact. Object shape remains loosely constrained by the schema. |
| `leaders` | One role and exact organisational scope | Person/title, status, source refs, next question, promoter signal and ownership scope. COO/DSI required; group verification requires corporate/register evidence; unknown person uses null. |
| `segments` | One revenue segment with evidence and share basis | Reporting values/axes use the units above; preserve source perimeter and period. |
| `frameworks` | Paths to Porter, 4P, SWOT, VRIO and 7S modules | Paths must exist; meaning requires semantic review. |
| `driver_ids`, `opportunity_links` | One use-case-to-driver/activity mapping | Each link carries value strategy, method, KPI, baseline, page, ML requirement, decision status and driver label. Bundle checks references and page 3. |
| `prerequisites`, `shortlist_ids` | Enabling work and selected opportunities | Former prerequisite IDs stay outside the AI inventory; shortlist cardinality is checked. Prerequisite object typing remains limited. |
| `reviews` | Contract, alternative and decision review artifacts | Each has kind, verdict and path. Freeze requires surviving verdicts. |
| `coverage`, `critical_questions`, `render_status` | Coverage, questions and current render state | Coverage remains loosely typed; current bundle expects `render_status=not_authorized`. |
| `artifact_hashes` | Relative artifact path → file SHA-256 | Required coverage and actual file bytes are checked. |

## Operational envelopes and hash scopes

| Contract | Main meaning | Definition / owner |
| --- | --- | --- |
| RunContext | Stage, pinned package/version, selected claims, contradictions, unknowns, verdict, human decision reference and next action | [Schema](../../contracts/run-context.schema.json), [gates](../agent/gates.md) |
| Checkpoint | Repository SHA, run-context pin, input/output pins, dependencies, validations, integrator and stop condition | [Schema](../../contracts/session-checkpoint.schema.json), [resume protocol](../agent/context-and-resume.md) |
| Research handoff | Sender/receiver, question, budget, required/available capabilities, outputs, readiness and fallback | [Schema](../../contracts/research-handoff.schema.json), [handoff](../agent/handoff-and-fallback.md) |
| Artifact receipt | One artifact's bytes, producer, visibility, publication/readback, QA and authorisation-reference metadata | [Schema](../../contracts/artifact-receipt.schema.json), [receipt contract](../agent/artifact-receipts.md) |

[HASHING.md](../../contracts/HASHING.md) defines canonical JSON and NFC fragment digests. Capture files are hashed as retained bytes. The executive renderer hashes payload **file bytes** in its manifest; freeze/package validation uses canonical JSON digests. Compare hashes within the producing contract's scope.

For replay, retain code revision, accessible source bytes, input pins, runtime/browser/font dependencies and relevant human decisions. See [domain history](../architecture/domain-and-data.md#time-history-and-replay) and the [rule matrix](../architecture/rules-and-validation.md).
