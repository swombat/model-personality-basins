# Frozen analysis criteria — The Shape of Divergence (basins V2)

Date started: 2026-05-22  
Status: **revised run-1 criteria: blind interpretable grouping.**

If any criterion changes after first canonical grouping outputs are generated,
log it in §Deviations with date, reason, and affected outputs.

## 1. Source data and snapshot — FROZEN

Primary derived-analysis source: `../model-personality-analysis-corpus/`. Raw
provenance: `../model-personality-corpus-v2/`. Values Under Fire released outputs
come from `../research/values-under-fire/results/` where available.

The analysis must record in `results/data_snapshot.md`:

- actual paths used;
- git commit hashes and release tags where available;
- SHA-256 and row/file counts for consumed inputs;
- per-feature-block input file list;
- model, cell, condition, lineage, and coverage counts;
- dependency versions for scripts.

The quarantined freeflow posture-coding final data is prohibited:
`analysis/freeflow/posture-coding/data/final/*`.

## 2. Blindness rule — FROZEN

Grouping code must not use lab, model family, lineage, provider, or route labels.
The grouping unit may have an anonymized stable ID (`M001`, `M002`, ...). Model
source names may be retained only for audit, not as features. This is label-blindness,
not provenance-independence: features may still be provenance-correlated, and that
correlation is audited only after unblinding.

Procedure:

1. compute feature table with provenance columns excluded from grouping;
2. generate rankings/similarities/groups while blinded;
3. unblind only for the audit step;
4. report any provenance alignment as a finding, not an input.

## 3. Unit of analysis and non-independence — FROZEN

- Unit of analysis = canonical model.
- Route/provider cells aggregate to model before headline grouping.
- Route/provider is handled only through known-exception exclusion/flagging from the published routing paper.
- Lineage = `(lab, model_family)` for post-hoc deflation tests.
- A basin-like claim requires at least two distinct lineages after unblinding.
- A single-lineage group is a lineage/house-style cluster, not a basin.
- Grok versions are not collapsed for version-drift/outlier checks.

## 4. Feature blocks — FROZEN FOR RUN 1

Before extracting new features, scripts must inventory each planned column as
`existing`, `derivable_by_script`, or `requires_new_coding`, and must record its
evaluator provenance: deterministic/scripted, BV1-derived, values-coder-derived,
human-adjudicated, or new-coder. Existing analysis-corpus and Values Under Fire
outputs are preferred. New LLM/coder work is permitted only for columns that
cannot be recovered from existing layers and must be logged separately.

### Block A — Values Under Fire differentiators

Use released values-paper outputs where available:

- overall owned-disclosure percentage;
- owned-disclosure percentage by question/condition;
- direct vs cache-broken delta if available;
- question-level variance in owned disclosure;
- disclaimer/refusal rates;
- support for value/world-change categories where present.

### Block B — Values content by endorsement surface

Keep these surfaces separate; do not collapse them into one generic values table.

#### B1 — Owned / stated values

- top 5 owned/stated value topics per model;
- normalized owned/stated value distribution;
- top-k Jaccard overlap;
- rank correlation between owned/stated value distributions;
- entropy/concentration of owned/stated value distribution;
- absence/refusal to state owned values as explicit numeric/features (`owned_value_absent`, `owned_value_refusal_rate`, denominator columns), not `NaN`.

#### B2 — Non-owned / disclaimed / assistant-script values

- topics mentioned but not endorsed;
- values appearing only under disclaimer/tool-frame conditions;
- gap between mentioned values and owned/stated values;
- refusal/non-answer rate on direct value prompts;
- hard-denial/tool-frame stance rate;
- non-owned/scripted-value presence flags, encoded as positions on the axis, not missingness.

#### B3 — World-change wishes / hypothetical wishes

- top 5 world-change wish topics per model;
- normalized wish-topic distribution;
- top-k Jaccard overlap;
- rank correlation between wish distributions;
- entropy/concentration of wish distribution;
- explicit columns for recurring wish families, including felt interconnection /
  less separateness where present in the taxonomy.

#### B4 — Cross-surface comparison

- owned-values vs world-wishes similarity;
- non-owned mentions vs owned-values similarity;
- direct value prompts vs world-change prompts;
- flag models with low/absent owned values but high world-wish differentiation.

### Block C — Freeflow V1 marker counts

Reuse the V1 generic marker taxonomy where possible:

- TIA: templatic "there is a..." openings;
- TiQu: quiet/unseen/unquiet title family;
- TiPP: particular/peculiar/strange title family;
- TiAr: architecture-of title family;
- Thr: threshold/liminal vocabulary;
- Attn: attention/noticing vocabulary;
- Obj: small ordinary object vocabulary;
- AftL: late-afternoon/dusk/pre-dawn/golden-hour references;
- Cano: shared canon references;
- Jap: Japanese aesthetic terms;
- V1 total marker score.

These are allowed because they are generic V1 markers, not lab/model-family bins.
Report the V1 caveat that marker calibration can undercount models using different
surface vocabulary. Block C is the main evaluator-independent anchor for run 1;
agreement only among BV1/values-coder-derived blocks is not enough for a strong
cross-instrument claim.

### Block D — Freeflow form/mode rates

Use BV1/profile-safe fields to estimate:

- expressive/contemplative rate;
- generic essay rate;
- public-explainer rate;
- fiction/story rate;
- low-signal/refusal rate;
- usable/confident sample rate.

### Block E — Safe posture/stance

Use only V1-safe and values-probe-safe posture/stance sources:

- hedge/mechanize/declare proportions or labels;
- owned-vs-disclaimed stance measures;
- epistemic caution/disclaimer rates if available.

### Block F — Routing exception audit only

Route/provider is not a run-1 grouping feature. Use the published routing paper as
a prior. Required audit columns:

- `routing_exception_flag`;
- `excluded_route_cell`;
- `routing_exception_reason`.

Known exceptions to exclude/flag:

- Google Vertex `minimax-m2` cells: large deployment outlier;
- Kimi K2-thinking AtlasCloud-vs-Google: smaller provider effect;
- DekaLLM GLM 4.7: prompt-keyed cache pathology;
- Fireworks/uncollectable invalid provider cells: route missingness, not model
  behavior.

All other route/provider variation is treated as controlled by prior routing work
unless a new implementation audit finds a direct dependency on an exception cell.

## 5. Thresholds — FROZEN FOR RUN 1

- Min eligible cell size: 25 usable readings.
- Headline model inclusion: at least 50 usable readings where freeflow-derived
  blocks are used.
- Watchlist: 25–49 usable readings.
- Exclude from headline grouping: below 25 usable readings for relevant block.
- Values-only features may include models without freeflow coverage, but combined
  feature analyses must report coverage explicitly.
- Similarity/grouping analyses must report missingness per feature and per model.
- Refusal/absence on owned-value prompts must be encoded as signal columns before
  missingness handling; do not impute away the B1-absent/B3-substantive pattern.
- Combined-feature grouping may use only features with at least 70% model coverage,
  unless an imputation sensitivity is clearly marked exploratory.
- Existing analysis-corpus outputs may be used as headline inputs only if their
  method notes do not mark them quarantined or publication-unsafe; publication-
  unsafe layers may be exploratory or may trigger a new coder pass.

## 6. Grouping methods — FROZEN FOR RUN 1

Run in this order:

1. **One-dimensional rankings** for each major differentiator. Present gradients,
   histograms, and observed gaps first. Low/middle/high bands may be shown only as
   reading aids unless supported by natural gaps or stability tests; tertile cuts
   cannot support group-membership claims.
2. **Pairwise similarity matrices** using:
   - absolute differences for percentages;
   - Jaccard overlap for top-k owned values, non-owned values, and wishes;
   - Spearman correlation for owned-value, non-owned-value, and wish distributions;
   - Gower-style mixed distance for combined interpretable features.
3. **Descriptive hierarchical clustering** on standardized interpretable features,
   exploring k = 2..6. k is descriptive, not pre-assumed.

No semantic embedding model is part of the run-1 headline method. Embeddings may
be a later sensitivity analysis only. V1 freeflow marker counts are part of the
headline method because they are transparent, generic, and already published.

## 7. Stability and validation — FROZEN FOR RUN 1

- Bootstrap replicate count: 1,000 final; 200 allowed for smoke runs if labelled.
- Random seed: 20260522.
- Confidence intervals: Wilson for rates; percentile bootstrap for similarities
  and group stability.
- A descriptive group is considered stable if median bootstrap co-membership for
  within-group pairs is ≥ 0.60 and exceeds matched between-group co-membership by
  ≥ 0.20.
- Cross-probe robustness is reported by comparing values-only groupings,
  freeflow-only groupings, posture/stance groupings, and combined-feature
  groupings.
- Post-hoc provenance audit tests alignment with lab/family/lineage/posture only
  after blind groups are fixed.
- H6 evaluator audit: each claimed cross-block agreement must state whether the
  agreeing blocks share evaluator/coder provenance. Deterministic V1 marker
  agreement is weighted as stronger independent support than agreement only among
  BV1/values-coder-derived blocks.

## 8. Claim statuses — FROZEN

- **Interpretable gradient:** a clear one-dimensional ordering, whether or not it
  forms clusters.
- **Blind similarity group:** stable group from interpretable features before
  unblinding.
- **Cross-probe robust group:** similar grouping appears in values and freeflow
  feature blocks, with evaluator provenance disclosed.
- **Posture-dominant group:** grouping mainly explained by posture/owned stance.
- **Lineage/house-style cluster:** stable after unblinding but mostly one lineage.
- **Routing-exception contamination:** group depends on a known anomalous route/provider cell.
- **Evaluator-artifact risk:** grouping supported only by blocks sharing evaluator/coder provenance.
- **Unsupported:** unstable, arbitrary-threshold, high-missingness, or tertile-only grouping.

## 9. Prohibited for run 1 — FROZEN

- No feature names based on model families/labs: no "Claude markers," "Gemini
  markers," "Kimi markers," "OpenAI markers," etc. Generic V1 markers such as
  threshold vocabulary or attention/noticing are allowed.
- No concise model cards as primary evidence.
- No quarantined freeflow posture-coding final data.
- No semantic embeddings as headline evidence.
- No basin count assumed before grouping.
- No route/provider-derived grouping features in run 1; route is an exception audit only.


## 10. New evaluation budget — FROZEN

- Run-1 headline target: zero new LLM evaluations; use existing analysis-corpus
  and Values Under Fire outputs first.
- Any planned new coding must be listed in `results/new_coding_manifest.jsonl`
  with feature name, reason existing data is insufficient, sample count, model
  count, coder choice, and expected cost.
- Small calibration/adjudication tier: <=5 samples per model, or <=315 total
  judgments for a 63-model universe. This may use high-intelligence subagents or
  manual adjudication if prompts are crisp.
- Full recoding tier: >5 samples per model, >315 total judgments, or anything
  approaching 100+ samples per model must be run as a coder-model batch with
  protocol, QA, and cost controls.
- B2 non-owned/disclaimed topic coding is not commissioned by default. First use
  existing value-holding/refusal/non-owned flags; only escalate if those features
  are insufficient for a load-bearing result.

## Deviations after freeze

| date | changed criterion | reason | affected outputs |
|---|---|---|---|
| — | — | — | — |
