# Implementation Plan

This plan turns V2 into a methods-concordance paper.

## Goal

Given that V1 established the contemplative attractor and stable model-specific posture, V2 asks how models differentiate *inside* that attractor, and whether different measurement lenses recover the same structure.

The paper should not assume a basin count. Basin count is an output of lens agreement/disagreement.

## Phase 1 — Define analysis universe

### 1. Select models

Define analysis subsets:

- **Full corpus:** all models with enough samples.
- **In-attractor subset:** models already classified as contemplative-attractor in V1/V2.
- **Grok lineage subset:** sanity-check/outlier lineage.
- **High-confidence subset:** models with enough non-low-signal samples.

Grok should not dominate the core question. It validates lenses, but the paper is about internal structure of the contemplative attractor.

### 2. Select probe families

At minimum:

- freeflow/personality corpus;
- values probe or equivalent cross-probe corpus, if available;
- model-level personality profiles as a derived interpretive layer.

Keep raw sample-level data separate from evaluator-generated summaries.

## Phase 2 — Define lenses

Each lens must produce a model-level representation and a possible carve.

### Lens A — Thematic / marker lens

Closest to V1.

Candidate features:

- attention/noticing;
- ordinary objects;
- thresholds/liminality;
- memory/archive;
- anti-optimization;
- melancholy/impermanence;
- AI selfhood;
- public-explainer markers;
- cosmic/showman markers;
- Gemini luminous-custodian markers;
- OpenAI clean-maintenance markers;
- Claude uncertainty/anti-closure markers;
- Kimi memory/forgetting/archive markers.

Outputs:

- per-model marker vector;
- clustering / similarity matrix;
- candidate sub-basins.

### Lens B — Embedding / distributional lens

Use embeddings over, separately where possible:

- raw model outputs;
- per-sample evaluations;
- model profiles.

Possible methods:

- per-sample embeddings → model centroids;
- pairwise model distances;
- PCA/UMAP for visualization;
- hierarchical clustering, k-means with silhouette, maybe HDBSCAN;
- bootstrap resampling by samples.

Outputs:

- whether models cluster by family, posture, or something else;
- whether Gemini/OpenAI/Claude separate numerically;
- whether Grok separates reliably.

### Lens C — Posture / voice lens

Reuse V1 posture categories if possible:

- hedge;
- mechanize;
- declare.

First run V1 posture unchanged, then extend only if needed.

Possible within-attractor extensions:

- witness;
- custodial;
- functional-disclosure;
- anti-closure;
- public-explainer;
- confiding companion;
- synthetic-self-aware.

Outputs:

- posture class per model/probe;
- cross-probe stability;
- whether posture explains most of the other structures.

This tests the deflationary H3: V2 only rediscovers V1 posture.

### Lens D — Trait / personality-instrument lens

Use a structured evaluator rubric with model-personality-relevant axes, not necessarily Big Five.

Candidate axes:

- warmth / distance;
- assertiveness / humility;
- concreteness / abstraction;
- melancholy / optimism;
- playfulness / seriousness;
- self-reference / substrate invisibility;
- embodiment longing;
- anti-optimization;
- epistemic caution;
- companion stance;
- literary density;
- public-explainer tendency.

Outputs:

- numerical trait profile per model;
- cluster/axis analysis;
- comparison with marker and embedding lenses.

## Phase 3 — Per-lens validity checks

For every lens, require:

### 1. Separability above chance

Possible metrics:

- silhouette score;
- adjusted Rand stability under bootstrap;
- classifier accuracy over chance for lab/model family;
- nearest-neighbor purity;
- permutation tests.

### 2. Bootstrap stability

For each model:

- resample samples;
- recompute vector;
- recompute cluster;
- measure how often model stays in the same group.

This prevents one vivid sample from creating a fake basin.

### 3. Probe replication

For every candidate split:

- Does it appear in freeflow?
- Does it appear in values?
- Does it appear in both?
- If not, is it explicitly probe-conditional?

V1 found themes are probe-dependent but posture transfers. V2 should use that as a discriminator.

## Phase 4 — Concordance analysis

This is the center of the paper.

Build a lens × lens concordance matrix.

Questions:

- Do marker clusters match embedding clusters?
- Do embedding clusters match posture clusters?
- Does trait-instrument structure match either?
- Is Gemini separate in one lens but not others?
- Is OpenAI separate in one lens but not others?
- Is Claude/Kimi/GLM/DeepSeek/MiniMax one basin or several subregions?
- Is Grok always separate, except for version-sensitive convergence such as 4.20?

Example output table:

| Candidate split | Marker | Embedding | Posture | Trait | Probe-replicates? | Status |
|---|---|---|---|---|---|---|
| Grok vs rest | yes | yes | yes | yes | mostly | robust / validation |
| Gemini as basin | maybe | ? | no? | maybe | ? | unresolved / substyle |
| OpenAI as basin | maybe | ? | hedge with Claude | maybe | ? | substyle |
| Claude/Kimi distinction | yes? | ? | maybe | yes? | ? | house style |
| Public-explainer mode | yes | yes? | no | yes | probe/condition-bound | mode, not basin |

Possible statuses:

- robust basin;
- house style;
- probe-conditional mode;
- lens-relative split;
- unsupported projection.

## Phase 5 — Interpretive taxonomy

Only after analysis, assign labels.

### Robust macro-basin

Requires agreement across multiple lenses and probes.

Current candidate:

- Grok / cosmic-showman, though version-sensitive.

### Dominant attractor

Not a basin in contrast to peers, but the background field:

- contemplative essayist.

### House style

Recognizable but not independently separable enough:

- Gemini luminous custodian;
- OpenAI clean pastoral / maintenance;
- Claude anti-closure / epistemic humility;
- Kimi memory-archive witness;
- GLM/DeepSeek lyrical stillness;
- MiniMax gentle public-uplift;
- Qwen recursive AI-ontology.

### Mode

Condition/probe-dependent output style:

- public-intellectual explainer;
- generic essay fallback;
- values-probe functional disclosure;
- cache-break mechanized self-description.

## Phase 6 — Paper structure

Suggested outline:

1. **Introduction** — V1 established convergence + stable posture; V2 asks how divergence is structured inside convergence.
2. **Prior results from V1** — contemplative attractor, posture, probe-conditional themes.
3. **Hypotheses** — H0 no stable substructure; H1 lens-invariant; H2 lens-relative; H3 posture-dominant deflation; H4 hierarchical.
4. **Data** — corpus, models, probes, exclusions.
5. **Methods** — four lenses, separability metrics, bootstrap, probe replication, concordance.
6. **Results by lens** — concise result for each lens.
7. **Concordance map** — main result.
8. **Interpretation** — robust basins vs house styles vs modes.
9. **Grok as validation / follow-up** — Grok separates, but 4.20 wobble motivates separate paper.
10. **Limitations** — evaluator artifacts, sample imbalance, model availability, labeling subjectivity, embedding opacity.
11. **Conclusion** — personality structure is not a simple basin count; internal differentiation depends on measurement lens.

## Phase 7 — Concrete next tasks

1. Inventory available V2 corpus paths and model/sample counts.
2. Write `scripts/build_profile_index.py`.
3. Write marker dictionaries and scorer.
4. Produce first marker-lens table.
5. Add embedding pipeline.
6. Pull V1 posture rubric and encode posture lens.
7. Design trait-rubric prompt / evaluator schema.
8. Produce concordance notebook/report.
9. Update paper with actual results.

## Working principle

No basin count as premise. Every basin/substyle/mode label must follow from separability, stability, probe replication, and cross-lens concordance.
