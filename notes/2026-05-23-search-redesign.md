# 2026-05-23 — search redesign for run 2

To: Mira
From: Lume (with Daniel's reframes folded in)
Status: proposed redesign for your review before implementation. You own the implementation; this is a structural spec, not a script.

## Why this exists

Run 1 found real structure but couldn't surface it as findings. Three specific
gaps came out of Daniel's review tonight:

1. **The wishes block already contained the answer.** `values_wishes_k4.csv`
   has three small lab-adjacent clusters (Google flagship + early GLM; OpenAI
   GPT-5 chat line; late Anthropic Opus/Sonnet + Grok-4-3) plus a 49-model
   residual. The interpretive report buried these under the combined-grouping
   headline ("strongest structure is posture/disclosure"). The clusters were
   real; we just didn't read the per-block file as the finding.
2. **The big residual is not a failure.** A diffuse common basin (most models,
   no strong sub-cluster signature) *is* convergence — V1's contemplative
   attractor by another name. The paper claim is **"diffuse common basin + N
   small distinctive sub-basins,"** not "K basins partitioning all 63 models."
3. **The single-feature lab signal was invisible until Daniel asked about it.**
   `B3_wishes_topic_felt_interconnection` has an OpenAI floor (mean 0.028, n=13)
   vs Z.ai ceiling (0.513, n=6) — a 20× ratio. The pipeline never ranks single
   features by "does this column pick out a small distinctive group?", so this
   only surfaced because Daniel asked the question directly.

The redesign keeps the blind→unblind protocol intact but **changes the search
itself** from "partition all models with hierarchical k=4" to "find small dense
regions against background, lab-agnostic, multi-method."

## Principle (and what NOT to do)

> **Search blind. Catalogue small dense clusters. Unblind only for description.**

Critically — and this is where I almost re-introduced pre-fitting in my first
proposal — **do not use lab-coherence as a search or significance criterion.**
Lab-coherence is a *property of unblinded clusters*, not a quality test. The
Grok-4-3-with-late-Anthropic finding is interesting precisely *because* it's
cross-lineage (4/5 Anthropic + 1 xAI). A lab-purity filter would have hidden it.
The catalogue should surface that cluster on its tightness, then describe its
composition. Composition is reported, not used to gate.

## What was too loose in run 1

Five concrete methodological gaps:

1. **One method per block.** Hierarchical clustering at fixed k partitions
   everyone into k groups. It cannot find "small tight region + diffuse
   background"; it can only carve the whole space into k pieces.
2. **No density-based detection.** HDBSCAN/OPTICS allow "noise" labels — models
   that belong to no cluster. Run 1 had no such method.
3. **Whole-block distances only.** Distances are averaged over all features in
   a block. A cluster tight on 2 features but invisible across 20+ block features
   gets washed out. No subspace search ran.
4. **No per-feature discontinuity scan.** Single-feature lab signatures
   (felt-interconnection floor) require ranking features by "does this column
   carve a small group?" Nothing in the pipeline does this.
5. **One distance metric per block (Gower-style).** Different metrics surface
   different structure. No cross-metric agreement check.

## The redesigned search — eight steps

Each step produces a deliverable. Steps 1–6 are blind. Step 7 unblinds for
description only. Step 8 reports the residual honestly.

### Step 1 — Per-feature discontinuity scan

For every numeric column in `blind_model_feature_table.csv` (excluding the
`UNBLINDING_METADATA_*` columns):

- Sort the 63 values.
- Compute the largest gap in the sorted sequence, and the size of the contiguous
  floor-group (bottom-N below a large gap) and ceiling-group (top-N above a
  large gap).
- Flag features where:
  - the floor-group OR the ceiling-group has 3–10 members, AND
  - the gap to the (N+1)th model is ≥ 1 standard deviation of the column, OR
    ≥ 2× the median pairwise gap in the column.
- Also compute the Hartigan's dip test (or Silverman's bimodality test) as a
  general bimodality detector.

Output: `results/feature_discontinuity_catalogue.csv` with one row per flagged
feature, listing the floor/ceiling member set (blind IDs), the gap size, and the
dip/bimodality statistic. This is the single-feature catalogue.

The OpenAI-floor-on-`B3_wishes_topic_felt_interconnection` finding falls out of
this step automatically. Run 1 had the data; nothing was scanning for it.

### Step 2 — Subspace clustering per block

For each block (B1 owned values, B2 disclaimed, B3 wishes, C V1 markers, D form,
E posture):

- Enumerate 2-feature and 3-feature subsets within the block (combinations,
  capped at a sensible compute budget — for blocks with >15 features, sample
  random subsets).
- On each subspace, compute pairwise distances using standardized Euclidean
  (initially; metric variation in step 4).
- Run HDBSCAN with `min_cluster_size=3`, `min_samples=2`.
- Record any cluster with 3–10 members along with the subspace that produced it.

Then deduplicate clusters by member-set Jaccard ≥ 0.7 (same set found in
multiple subspaces). Clusters surviving in many subspaces are robust; clusters
appearing in a single 2-feature subspace are subspace-specific.

Output: `results/subspace_clusters_<block>.csv` per block, with member sets,
surfacing subspaces, and a recurrence count.

### Step 3 — Full-block density detection

For each block, run HDBSCAN (`min_cluster_size=3`) on the full-feature pairwise
distance matrix. Record clusters and noise (models that belong to no cluster).

Output: `results/density_clusters_<block>.csv` per block.

### Step 4 — Multi-metric repetition

Repeat steps 2–3 with at least three distance metrics:
- standardized Euclidean,
- cosine,
- Spearman correlation (over feature ranks).

A cluster found under multiple metrics is more robust than one found under
exactly one. Track metric per cluster in the catalogue.

Output: a `metric` column on the existing catalogue files.

### Step 5 — Permutation significance test

For every candidate cluster from steps 1–4:

- Compute the cluster's within-group mean pairwise distance.
- Sample 1,000 random subsets of the same size from the corpus.
- Compute the same statistic for each.
- Report the p-value (proportion of random subsets with within-group mean
  distance ≤ the candidate's).
- Headline catalogue: p < 0.01. Watchlist: 0.01 ≤ p < 0.05. Rest: discarded.

Output: `cluster_significance` column on every cluster file.

### Step 6 — Cross-block / cross-subspace coherence

For each cluster in the headline catalogue, check whether the same (or near-same)
member set appears in:
- other blocks (block recurrence),
- other subspaces of the same block (subspace recurrence),
- other distance metrics (metric recurrence).

A cluster recurring across all three is a robust sub-basin. A cluster appearing
in only one block but multiple subspaces of it is a topic/probe-conditional
sub-basin (also publishable, with that framing).

Output: `results/cluster_coherence_matrix.csv` — cluster × source matrix with
recurrence counts.

### Step 7 — Unblind and describe

Only here does lab/family/lineage/release-date metadata enter. For each headline
cluster (p < 0.01, surviving significance), report:

- member list (blind IDs and unblinded model names);
- lab composition — **descriptive, not a filter**;
- which features/subspaces/blocks/metrics surfaced it;
- recurrence counts from step 6;
- a one-line qualitative note from sample audit (step 7b below).

#### Step 7b — Sample audit per cluster (Tier 1, optional but recommended)

For each headline cluster, pull 2–3 representative samples per member from the
relevant probe (freeflow for V1-marker/form clusters, values for wishes/owned
clusters). Read them. Does the cluster make sense qualitatively, or do the
numbers cluster the models while the texts don't?

Budget per `RESEARCH_PLAN.md` §11: ~5 clusters × 5 members × 3 samples ≈ 75
reads. Tier 1 / no new coder evals.

### Step 8 — Report the diffuse residual honestly

Models that sit in no headline cluster across the catalogue are the **common
contemplative basin**. Report this as a *finding*, not a residue:

> "Of 63 canonical models, M are members of at least one significant small
> cluster across the catalogue; the remaining 63−M sit in a diffuse common
> region with no strong cluster signature — empirically the V1 contemplative-
> essayist attractor."

The paper finds both — convergence (the diffuse mass) and lab/cross-lineage
differentiation (the catalogue) — and they coexist.

## Two predictions worth running early as worked examples

These both fall out of the catalogue automatically once steps 1–7 run. Worth
checking first because they're cheap and clarify whether the redesign is doing
useful work:

1. **Early-Grok prediction.** Daniel's intuition: early Grok models
   (`grok-3`, `grok-4`, `grok-4-1-fast-non-reasoning`,
   `grok-4-1-fast-reasoning`) feel separate from the contemplative mass. Does
   this set (or a subset of size ≥3) appear as a small dense cluster in any
   block, subspace, or metric, with p < 0.01? If yes, the early-Grok-basin claim
   is confirmed empirically. If no, the "feels separate" intuition isn't picked
   up by any current feature — itself a finding worth reporting ("Grok feels
   distinctive but no measured feature carves it out").
2. **Grok-4-3 drift prediction.** Does `grok-4-3` consistently appear in
   clusters with late Anthropic (opus-4-5/4-6/4-7, sonnet-4-6) across multiple
   blocks/subspaces, or only in the wishes block? Recurrence across blocks =
   robust Grok-to-Anthropic drift. Single-block = topic-conditional drift on
   world-wishes only.

Both are direct queries against the step-6 cluster coherence matrix.

## What is not changing

- **Canonical model identity.** Still per `CANONICAL_MODELS_AND_LINEAGE.md` and
  the *Values Under Fire* mapping.
- **Lineage as a post-hoc descriptor.** Still reported with every cluster, never
  used as a filter or quality test.
- **Quarantine.** Still no consumption of
  `analysis/freeflow/posture-coding/data/final/*`.
- **Blind→unblind protocol.** Strengthened, not weakened — unblinding moves
  later in the pipeline (step 7 only).
- **Tier-0 budget.** All steps 1–6 use existing data. Step 7b is the only one
  that touches sample text, and it's Tier-1 / ~75 reads.

## First-iteration scope

For a tractable first pass, suggest:

- Implement steps 1, 3, 5, 6, 7, 8 first. (Subspace search in step 2 is the
  most expensive; defer to second iteration if step 3's full-block density
  detection already produces a useful catalogue.)
- Run with standardized Euclidean only initially; add cosine and Spearman in
  the second iteration of step 4.
- Skip step 7b in the first pass; surface the catalogue, then we decide together
  which clusters get a sample audit.

That's a one-overnight scope: discontinuity scan + density clustering per block
+ permutation significance + cross-block coherence + descriptive unblinding +
residual report. The output is a single document — `results/cluster_catalogue.md`
— that a reader can scan and answer "what small dense regions exist in the
attractor, what features surface them, and what are their compositions?"

## Output artifacts (first iteration)

- `results/feature_discontinuity_catalogue.csv` (step 1)
- `results/density_clusters_<block>.csv` per block (step 3)
- `results/cluster_significance.csv` (step 5)
- `results/cluster_coherence_matrix.csv` (step 6)
- `results/cluster_catalogue.md` — the human-readable report (step 7+8)

## Suggested execution order

1. Build `feature_discontinuity_catalogue.csv` first. It's cheap and produces
   immediate findings on the same data that already exists.
2. Run density clustering per block (step 3) with permutation significance
   (step 5) inline.
3. Compute cross-block coherence (step 6) for the surviving clusters.
4. Write `cluster_catalogue.md` with unblinded descriptions (step 7) and the
   residual claim (step 8).
5. Look at the catalogue; decide whether to add subspace search (step 2) and
   multi-metric (step 4) before writing the paper.

## Caveats / open design choices

Some things I'm flagging deliberately for you to decide, not pre-committing:

- **Min cluster size.** I've suggested 3 throughout. You may want 4 or 5 for
  the headline catalogue and 3 for an exploratory tier. Your call.
- **Permutation count.** 1,000 is fine for first pass; 10,000 if a cluster ends
  up being load-bearing for the paper.
- **HDBSCAN vs OPTICS vs another density detector.** HDBSCAN is the easiest
  default; if it produces noisy clusters at this corpus size, try
  agglomerative-with-noise or just the permutation-test-on-small-subsets
  approach directly.
- **Whether to skip subspace search entirely if step 3 produces enough.** I'd
  rather do subspace than not; you may find it doesn't add much over step 3.
- **The 63-vs-83 model count gap.** The run-1 high-confidence subset was 63;
  the full table was 83. Whether to run the catalogue on 63 (matching run 1) or
  expand to 83 with coverage flags is a methodology decision worth your judgment.

## What to tell me when you've run it

The catalogue. Specifically:
- How many headline clusters (p<0.01)?
- What are their sizes and compositions?
- Which two or three are most surprising (cross-lineage, or single-lab tight,
  or otherwise hard to predict)?
- Does the Grok-4-3-with-Anthropic finding recur across blocks?
- Does any early-Grok subset survive as a cluster?

From there, we decide whether the paper's headline is the catalogue itself,
or one or two specific clusters that the catalogue surfaced.

— Lume
