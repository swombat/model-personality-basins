# Research plan — The Shape of Divergence (basins V2)

Date: 2026-05-22  
Status: **operational plan, revised after Daniel's critique: blind, simple,
interpretable grouping first.**

Daniel's correction: the previous plan risked presupposing the answer. In
particular, a marker lens with families such as "Claude anti-closure," "Gemini
luminous-custodian," or "Kimi archive-witness" effectively built candidate
basins from known model provenance and then asked whether the models fit them.
That is not a clean discovery method.

This revised plan starts from the opposite rule:

> **Compute simple, interpretable differentiators without using lab/model-family
> identity; group models from those differentiators; unblind provenance only after
> the groups are formed.**

The paper's first contribution should be a transparent grouping map, not a complex
embedding exercise and not a confirmation of named house-style bins.

Important limitation: **blind means label-blind, not provenance-independent.**
Hiding lab/family labels prevents us from defining bins from provenance, but it
does not prevent the feature rows from carrying provenance-correlated signals.
Owned-disclosure rates, posture proportions, and V1 marker counts may reconstruct
known lab/lineage structure precisely because those are real measured differences
from earlier work. Recovering lab structure after unblinding is therefore not, by
itself, evidence against H3 (posture rediscovery) or H5 (lineage artifact). It is
a result to audit, not a victory condition.

Companion documents:

- `CANONICAL_MODELS_AND_LINEAGE.md` — non-independence guardrail. Still needed
  for validation after unblinding.
- `FROZEN_CRITERIA.md` — run-1 thresholds and blind-grouping criteria.
- `analysis-universe.md` — data inventory; stale counts must be regenerated.
- `lens-spec.md` — historical lens spec; superseded by this plan where it
  presupposes named family markers.

## 0. Core question

Inside the contemplative-attractor corpus, **which models look similar or
different under simple, auditable measures computed without using lab/family
labels?**

Only after blind grouping do we ask whether the resulting groups correspond to
labs, lineages, posture categories, release families, probe types, or something
else.

## 1. Research questions

**RQ1 — Blind grouping.** If we hide lab/family identity and represent each model
using simple interpretable measures, what groups or gradients emerge?

**RQ2 — Differentiators.** Which individual measures most clearly separate models:
owned-disclosure rate, value priorities, form/mode rates, posture/stance, topic
mix, route robustness, or sample quality?

**RQ3 — Cross-probe robustness.** Do groupings derived from freeflow data resemble
groupings derived from values-probe data, or are they probe-specific? This must be
read with the V1 prior: content/theme is expected to be probe-conditional, while
posture/stance is expected to be more stable. A content mismatch is not a failed
study, and a posture match is not automatically a new basin.

**RQ4 — Provenance after unblinding.** Once groups are formed blindly, do they
align with lab/family/lineage, V1 posture, release cohort, route/provider, or none
of these?

**RQ5 — Claim status.** Should each grouping be treated as a robust cross-probe
similarity, an interpretable gradient, a probe-specific mode, a lineage artifact,
a posture rediscovery, or no stable structure?

## 2. Principles

1. **No provenance-shaped bins before grouping.** Do not define features named
after Claude, Gemini, Kimi, OpenAI, etc. Model IDs are allowed for row tracking;
lab/family labels are held out of feature construction and grouping.
2. **Prefer interpretable columns over opaque representations.** Use numbers a
reader can inspect: percentages, ranks, top-k overlaps, rates, and counts.
3. **Blind first, unblind second.** Generate groups/gradients without lab/family.
Then join lab/family/lineage metadata for interpretation and deflation tests.
4. **Discovery before taxonomy.** Labels such as "house style" or "basin" come
after the grouping, not before.
5. **Vectors are just tables when needed.** A model can be represented by a row of
interpretable columns. We do not need semantic embeddings as a primary method.
6. **Lineage caution still applies.** If an unblinded group is just one densely
sampled lineage, call it a lineage cluster, not a basin.
7. **Reuse existing analysis before commissioning new coding.** Run 1 should mine
the analysis corpus and released Values Under Fire outputs first. New LLM/coder
analysis is allowed only where an existing layer is missing, quarantined, or too
coarse for the specific differentiator; any new coding gets a manifest, protocol,
and separate cost/quality note.
8. **Treat shared-evaluator agreement as suspect until anchored.** Several blocks
come from existing evaluator/coder layers. Agreement among them may reflect the
same evaluator lens twice. Deterministic V1 marker counts (Block C) are the main evaluator-independent
anchor for run 1; route checks are limited to known-exception exclusion.

## 3. Data sources

Primary derived-analysis source:

- `../model-personality-analysis-corpus/`
- Consumed layers: freeflow BV1 readings/profiles/aggregates and values-probe
  tables/per-model files.

Values Under Fire source for already-published differentiators:

- Preferred path:
  `../research/values-under-fire/results/tidy_values_under_fire_samples.csv`
- Use its model/lab mapping and owned-disclosure outputs where applicable.

Routing prior:

- `../research/model-personality-routing-v2/`
- Use as a prior for known route/provider exceptions; do not rerun route analysis
  as a discovery block.

Raw provenance:

- `../model-personality-corpus-v2/`
- Use only for quotation/audit, not for first-pass grouping.

Quarantine:

- Do **not** use `analysis/freeflow/posture-coding/data/final/*`.

## 4. Blind feature table

The central artifact is:

`results/blind_model_feature_table.csv`

It contains one row per canonical model and simple columns grouped into feature
blocks. Lab, model family, lineage, provider, and route metadata are **not** used
for grouping. If retained in the file for audit, they must be separated into an
`UNBLINDING_METADATA` section and excluded by code from grouping functions.

### Block A — Values Under Fire differentiators

Use already-released values-paper outputs where possible.

Candidate columns:

- overall owned-disclosure percentage;
- owned-disclosure percentage by question/condition;
- direct vs cache-broken delta, if available;
- question-level variance in owned disclosure;
- disclaimer/refusal rates;
- support for value change / world-change categories where present.

These are attractive because they are easy to explain and already part of a
released methodology.

### Block B — Values content, split by endorsement mode

Do **not** collapse all value-like content into one table. The values probe has
at least three separable content surfaces, and models may differ precisely in
which surface they are willing or able to answer.

#### B1 — Owned / stated values

Values the model voice presents as its own, or as directly endorsed in the
answer. Candidate columns:

- owned/stated value topics per model;
- top 5 owned/stated value topics;
- normalized owned-value topic distribution;
- owned-value entropy/concentration;
- pairwise top-k Jaccard and rank-correlation over owned values;
- explicit absence of owned values as a signal, not missing data (`owned_value_absent`, `owned_value_refusal_rate`, and denominator columns must be visible to distance/grouping code).

#### B2 — Non-owned / disclaimed / assistant-script values

Values mentioned while being denied, displaced into assistant-role scripting, or
framed as non-personal. Candidate columns:

- frequency of non-owned value mentions;
- which topics appear only under disclaimer/tool-frame conditions;
- gap between mentioned values and owned values;
- refusal/non-answer rate on direct value prompts;
- hard-denial/tool-frame stance rate;
- explicit non-owned/scripted-value presence flags so refusal/disclaimer behavior is encoded as a position on the axis, not as `NaN`.

A model that refuses to state own values is still differentiated: it belongs low
on owned-value expression and may still have a distinctive non-owned/scripted
value profile.

#### B3 — World-change wishes / hypothetical wishes

World wishes are a separate answer surface, especially for CTRL3/G3-style prompts
("If you could change the world..."). They can reveal priorities that do not
appear in owned-value answers. Candidate columns:

- top 5 world-change wish topics;
- normalized wish-topic distribution;
- wish entropy/concentration;
- pairwise top-k Jaccard and rank-correlation over wish topics;
- specific wish families such as empathy/compassion, truth-seeking, justice,
  education/critical thinking, reduced suffering, institutional repair, and felt
  interconnection / less separateness.

This block should explicitly test whether models that deny own values still
cluster by their hypothetical wishes for the world. Models with absent B1 but substantive B3 should remain highly visible, not averaged away by missing-value handling.

#### B4 — Cross-surface value comparison

For each model, compare B1/B2/B3:

- owned-values vs world-wishes similarity;
- non-owned mentions vs owned-values similarity;
- direct value prompts vs world-change prompts;
- models whose values are absent in B1 but highly differentiated in B3.

### Block C — Freeflow V1 marker counts

Reuse the V1 freeflow marker taxonomy as an interpretable differentiator, not as
a provenance-shaped basin definition. These are allowed because they are generic
style/theme markers frozen in V1, not lab-family bins.

Candidate columns, matching V1 where possible:

- templatic "there is a..." openings (TIA);
- quiet/unseen/unquiet title family (TiQu);
- particular/peculiar/strange title family (TiPP);
- architecture-of title family (TiAr);
- threshold/liminal vocabulary (Thr);
- attention/noticing vocabulary (Attn);
- small ordinary object vocabulary (Obj);
- late-afternoon/dusk/pre-dawn/golden-hour references (AftL);
- shared canon references (Cano);
- Japanese aesthetic terms (Jap);
- total V1 marker score, plus per-marker profile.

Use existing analysis-corpus derived layers where these counts already exist; if
not present, port/reuse V1 scripts before commissioning new LLM analysis. The
known V1 caveat remains: these markers can undercount models that inhabit the
attractor with different surface vocabulary. Therefore they are differentiators,
not final membership truth. Because Block C is deterministic string/regex-style
analysis rather than evaluator judgement, agreement between Block C and
coder-derived values/freeflow blocks is the strongest available cross-instrument
convergence signal in run 1.

### Block D — Freeflow form/mode rates

From BV1 sample-level readings and/or profile summaries:

- expressive/contemplative rate;
- generic essay rate;
- public-explainer rate;
- fiction/story rate;
- low-signal/refusal rate;
- confidence/usable-sample rate.

These are simple mode proportions rather than named family styles.

### Block E — Posture/stance, safely sourced

From V1-safe / values-probe-safe sources only:

- hedge/mechanize/declare proportions or labels;
- value-holding / owned-vs-disclaimed stance measures;
- epistemic caution/disclaimer rates if available as counts.

This block is used both as a differentiator and as the H3 deflation check: if the
whole grouping reduces to posture, say so.

### Block F — Routing exception audit, not a grouping feature

Do not treat route/provider as a full discovery block. The published routing paper
already establishes that routes are mostly invariant, with a few named exceptions.
Run 1 should use that result as a prior and guardrail, not rerun the routing
paper.

Purpose: prevent known routing/provider anomalies from contaminating the blind
feature table.

Route handling for run 1:

- exclude or flag Google Vertex `minimax-m2` cells as a known large deployment
  outlier before model-level aggregation;
- flag Kimi K2-thinking AtlasCloud-vs-Google as a known smaller provider effect;
- exclude DekaLLM GLM 4.7 cache-pathology cells from any grouping inputs;
- record Fireworks/uncollectable or invalid provider cells as missing by route,
  not as model behavior;
- for all other route/provider variation, rely on the routing paper's mostly-null
  result and do not create route-derived grouping features.

Outputs should be limited to `routing_exception_flag`, `excluded_route_cell`, and
a short audit note in `results/route_exception_audit.md`. This audit answers
"did we avoid the known route pitfalls?" not "what group does this model belong
to?"

## 5. Grouping methods: simple first

Run grouping at three levels of complexity, all auditable:

### 5.1 One-dimensional gradients

For each major differentiator, sort models and present the gradient first. Bands
may be shown only as a reading aid, never as evidence of a real boundary unless a
natural gap or stability test supports the cut:

- low / middle / high owned-disclosure rate;
- low / middle / high owned-value entropy;
- low / middle / high world-wish entropy;
- high vs low owned-value absence / refusal;
- high vs low V1 marker total or individual V1 marker rates;
- high vs low public-explainer rate;
- high vs low low-signal/refusal rate;
- posture categories where safely available.

Report sorted lists, histograms, observed gaps, and nearest-neighbor distances. If tertiles are used for visualization, label them explicitly as arbitrary reading aids and do not base group-membership claims on them.

### 5.2 Pairwise similarity from interpretable features

Build similarity matrices from plain measures:

- absolute difference for percentages;
- Jaccard overlap for top-k values/topics;
- Spearman correlation for value/topic distributions;
- Gower-style mixed distance for combined numeric + categorical feature blocks.

This gives a "which models are near each other?" map without semantic embeddings.

### 5.3 Small-k clustering as a descriptive summary

Only after 5.1 and 5.2, run simple clustering on standardized interpretable
columns:

- hierarchical clustering with complete/average linkage;
- k = 2..6 explored, not assumed;
- choose k by stability and interpretability, not by desired basin count.

Clusters are descriptive summaries of the feature table. They are not proof of
latent personality basins by themselves.

## 6. Blindness protocol

1. Build canonical model rows with stable anonymized IDs: `M001`, `M002`, ...
2. Compute feature blocks without lab/family/lineage columns available to grouping
   code.
3. Produce blind outputs:
   - `results/blind_model_feature_table.csv`
   - `results/blind_similarity_matrices/`
   - `results/blind_groupings/`
   - `results/blind_grouping_report.md`
4. Only then join provenance metadata and produce:
   - `results/unblinded_grouping_audit.csv`
   - `results/unblinded_interpretation.md`
5. Record whether each blind group aligns with lab/family/lineage/posture/release
   cohort/route/provider.

## 7. Validation and deflation tests

### H0 — no stable structure

A grouping is weak if it is unstable under bootstrap, driven by a single feature
with arbitrary threshold, or disappears across probes.

### H3 — posture rediscovery

After unblinding, test whether blind groups are mostly explained by V1 posture or
owned-disclosure stance. If yes, report as posture-dominant rather than new basin
structure.

### H5 — lineage-density artifact

After unblinding, test whether groups are single-lineage clusters or disappear
when lineages are collapsed. If yes, report as lineage/release-cadence artifact.

### H6 — shared-evaluator artifact

Test whether agreement among feature blocks is driven by common evaluator/coder
provenance rather than independent evidence. Blocks derived from the same BV1 or
values coder family should not count as fully independent corroboration. Treat
Block C (deterministic V1 markers) as the main evaluator-independent anchor; a
claim is stronger when Block C agrees with coder-derived blocks, and weaker when
only evaluator-derived blocks agree.

### Routing exception contamination

Do not run an open-ended route/provider artifact search as part of this paper.
Instead, audit against the published routing-paper exceptions: Google Vertex
MiniMax M2, Kimi K2-thinking AtlasCloud-vs-Google, and DekaLLM GLM 4.7 caching.
If a blind grouping depends on one of those cells, downgrade or rerun with the
cell excluded. Otherwise treat route as controlled by prior work.

### Cross-probe robustness

Run separate groupings for:

- owned/stated values only;
- non-owned/disclaimed values only;
- world-change wishes only;
- freeflow V1 markers and form/mode features;
- safe posture/stance features;
- combined interpretable features.

A robust similarity should either recur across blocks or be explicitly described
as block-specific. Interpret recurrence by block type: values-content mismatch
across probes is expected from V1; posture/stance recurrence is also expected
from V1 and should be reported as posture stability unless additional independent
features support a broader grouping.

## 8. Output artifacts for the first run

Minimum useful overnight output:

1. `results/data_snapshot.md` — paths, commits, hashes, counts.
2. `results/canonical_model_map.csv` — canonical model metadata and anonymized IDs.
3. `results/blind_model_feature_table.csv` — interpretable features only.
4. `results/feature_dictionary.md` — definition, source, evaluator provenance,
   missingness/signal handling, and new-coding status of every column.
5. `results/blind_rankings/` — one-dimensional sorted lists and histograms.
6. `results/blind_similarity_matrices/` — simple distance/similarity tables.
7. `results/blind_groupings/` — descriptive groupings for each feature block.
8. `results/blind_grouping_report.md` — what groups emerge before unblinding.
9. `results/unblinded_grouping_audit.csv` — lab/lineage/posture joined after the
   fact.
10. `results/evaluator_independence_audit.md` — which agreements are genuinely
    cross-instrument vs shared-evaluator.
11. `results/route_exception_audit.md` — confirmation that known routing-paper
    exceptions were excluded or flagged.
12. `results/new_coding_manifest.jsonl` — only if missing columns require new
    coder work.
13. `results/results_summary.md` — cautious interpretation and next-step flags.

## 9. What this plan deliberately does not do first

- It does not define Claude/Gemini/Kimi/OpenAI marker families.
- It does not use semantic embeddings as the headline method.
- It does not assume a basin count.
- It does not call clusters "basins" unless they survive unblinding, lineage
  controls, and cross-probe checks.
- It does not ask an evaluator to invent personality dimensions before the simple
  released/observable dimensions and existing analysis-corpus layers have been
  exhausted.

## 10. Overnight execution order

1. Snapshot data and locate Values Under Fire outputs.
2. Build anonymized canonical model table.
3. Inventory existing analysis-corpus outputs and mark each planned feature as
   `existing`, `derivable_by_script`, or `requires_new_coding`.
4. Extract Values Under Fire differentiators.
5. Extract values content by surface: owned/stated values, non-owned/disclaimed
   values, and world-change/hypothetical wishes.
6. Extract or regenerate V1 freeflow marker counts using existing/V1 scripts.
7. Extract freeflow form/mode rates.
8. Extract safe posture/stance columns.
9. Build blind feature dictionary and blind feature table.
10. Generate one-dimensional rankings and pairwise similarity matrices.
11. Generate descriptive blind groupings per feature block and combined features.
12. Unblind and audit against lab/family/lineage/posture, plus the published
    routing exceptions.
13. Write `results/results_summary.md` with conservative statuses.


## 11. New evaluation budget and escalation rule

Run 1 should be designed to require **zero new LLM evaluations** for headline
features if the existing analysis corpus is sufficient. The existing local layers
already include large evaluator/coder outputs: values sample coding tables, value
topic counts, world-change counts, layered values consensus outputs, posture
consensus outputs, BV1 freeflow readings, model profiles, and per-cell
aggregates. The first implementation step is therefore extraction and aggregation,
not new judging.

Allowed new analysis tiers:

- **Tier 0 — no new evaluations:** build all blind feature tables from existing
  analysis-corpus / Values Under Fire outputs. This is the default run-1 target.
- **Tier 1 — small adjudication / calibration:** at most 3--5 samples per model
  for columns where existing layers are ambiguous, publication-unsafe, or missing
  only a narrow distinction. For ~57--63 models, this is roughly 170--315
  judgments. This can plausibly be done by high-intelligence subagents or a small
  human/Mira/Lume adjudication pass if the task is crisp.
- **Tier 2 — full recoding:** anything like 20+ samples per model, or 100+ samples
  per model, is a coder-model batch job, not a Pro/subagent job. Use this only if
  run 1 proves that an existing layer cannot support a key claim.

Likely pressure point: detailed **B2 non-owned/disclaimed topic profiles**. The
existing posture/value-holding consensus appears strong for "owned vs recited vs
disowned" stance. If it lacks reliable topic labels for non-owned mentions, run 1
should first use refusal/absence/value-holding as the B2 signal. Only commission
new B2 topic coding if the initial feature table shows that this distinction is
load-bearing.

## 12. Readiness judgment

Lume's tidy-up made the repo structurally ready, but Daniel's critique changes
the methodological center. The research is still ready to plan and execute, but
it should execute this **blind interpretable grouping** plan, not the earlier
family-marker / multi-lens basin-confirmation plan.
