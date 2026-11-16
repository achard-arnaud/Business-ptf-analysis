# Agent routes — load the active task's dependencies

For a company diagnosis, read [AGENTS.md](../../AGENTS.md), [programme state](../../program/state.json), one company manifest/index and the [workflow](../../skills/hivest-portfolio-ai/references/workflow.md). Other tasks have their own route below.

| Intent | Required route | Expected result |
| --- | --- | --- |
| Resume a company | [Context protocol](context-and-resume.md) → entity state/index → active procedure | Bounded question, verified input pins, gate and next action |
| Acquire / qualify evidence | [Evidence](../../skills/hivest-portfolio-ai/references/evidence.md); [research graph](../../skills/hivest-portfolio-ai/references/research-graph.md) as needed | Source → fragment → claim; scope, contradictions and unknowns |
| Diagnose / prioritise | [Market drivers](../../skills/hivest-portfolio-ai/references/market-drivers.md) → [diagnostic](../../skills/hivest-portfolio-ai/references/diagnostic.md) → [opportunities](../../skills/hivest-portfolio-ai/references/opportunities.md) | Driver/activity/use-case mapping, baseline and prerequisite gates |
| Review / compose executive output | [Review](../../skills/hivest-portfolio-ai/references/review.md) → [composition](../../skills/hivest-portfolio-ai/references/composition.md) → [binding guide](../architecture/template-binding.md) | Matching payload/profile, evidence status and output QA |
| Produce the learning pilot | [Learning README](../../learning/enterprise-ai/README.md) → [canonical Perception sheet](../../learning/enterprise-ai/perception.sheet.json) → [composition recipe](../../skills/enterprise-ai-learning/references/composition-rendering.md) | Six landscape pages from canonical JSON; older modules remain candidates |
| Compose the fund note | [Fund index](../../companies/hivest/INDEX.md) → [template](../../templates/strategic-market-note.md) → [renderer setup](../../renderers/strategic_note/README.md) | Separate editorial note and its own QA |
| Modify code or a contract | [Code map](../architecture/code-map.md) → affected schema/script/fixture/test | Bounded implementation and relevant checks |
| Review data / functional architecture | [Domain](../architecture/domain-and-data.md) → [dictionary](../data/DATA_DICTIONARY.md) → [rule matrix](../architecture/rules-and-validation.md) | Traceable requirement → field → validator → evidence |
| Review architecture decisions | [Architecture register](../architecture/README.md) → relevant original record/ADR | Scope, rationale, status and current dependency pointers |
| Transfer between models | [Handoff](handoff-and-fallback.md) → [checkpoint](context-and-resume.md) | Required/available capabilities, pinned inputs and stop condition |
| Run a public demo | [Getting started](../getting-started.md) | HTML without private archives; browser-specific steps when required |

At each handoff retain entity/cutoff, current gate, decision question, paths/versions/hashes, decisive claims and counterclaims, material unknowns, actual validations, next action and stop condition. Keep acquisition, semantic review, QA and human release separately evidenced. The index/graph locates evidence; it does not replace it.
