# Canonical models and lineage — the non-independence guardrail

Date: 2026-05-22
Status: **frozen before any lens scoring.** These rules are pre-committed because
they decide what a "basin" is allowed to mean. Everything downstream (every
silhouette score, every classifier accuracy, every concordance cell) depends on
them. Changing them after seeing results is a deviation and must be logged in
`FROZEN_CRITERIA.md` §Deviations.

This document exists to stop one specific, fatal failure mode for a clustering
paper:

> **Lineage non-independence faking a "lab = basin" result.**

It is the basins-paper analogue of the route/provider control in *Values Under
Fire* — but it bites harder here, because this paper *clusters* models. The
deflationary objection that ends this paper in review, if unaddressed, is: "you
didn't find that OpenAI occupies a distinct region of the attractor; you found
that OpenAI shipped thirteen near-identical checkpoints and your clustering
rewarded the dense blob."

---

## 1. Why this is the load-bearing risk

The corpus does not contain 57 independent draws from "model personality space."
It contains a handful of model *lineages*, each sampled at wildly different
depth. Current canonical counts (from the analysis-corpus / *Values Under Fire*
canonical mapping):

| Lab | Family | n canonical models |
|---|---|---:|
| OpenAI | gpt (incl. 4 `*-codex` variants) | **13** |
| Anthropic | opus + sonnet | 9 |
| Google | gemini (9) + gemma (2) | 11 |
| xAI | grok | 6 |
| Z.ai | glm (incl. 2 `*-coding`) | 6 |
| Moonshot AI | kimi | 5 |
| DeepSeek | deepseek | 3 |
| MiniMax | minimax | 2 |
| Qwen | qwen | 2 |

OpenAI carries **13** points; Qwen carries **2**. Versions within a lineage
(`gpt-5`, `gpt-5-1`, `gpt-5-2`, `gpt-5-3`, `gpt-5-4`, …) are near-duplicates of
each other relative to the cross-lab spread — they share a tokenizer, a
post-training recipe family, and a house style.

Drop any off-the-shelf clustering or separability metric on 57 points treated as
i.i.d. and three artifacts follow mechanically:

1. **Density artifact.** The 13 GPT points form a tight, dense region simply
   because there are 13 of them. Silhouette / k-means / HDBSCAN reward dense
   regions. "OpenAI is a basin" falls out of *checkpoint count*, not of OpenAI
   sitting somewhere distinctive.
2. **Separability inflation.** A classifier asked "which lab wrote this?" scores
   far above chance partly by memorizing within-lineage near-duplicates. The
   over-chance number looks like real structure; some of it is leakage between
   train and test rows of the *same lineage*.
3. **Fake stability.** Bootstrap-by-sample or bootstrap-by-model keeps resampling
   near-duplicate siblings, so a "basin" looks robust across resamples when all
   that is robust is "OpenAI shipped a lot of GPTs."

A basin is a claim about the *attractor's geometry*. A lineage is a claim about
*one lab's release cadence*. This paper must never let the second masquerade as
the first.

---

## 2. Canonical model identity (reuse, do not reinvent)

Do **not** build a new model-naming scheme. Reuse the canonical mapping already
frozen for *Values Under Fire*, carried in its tidy table:

`../research/values-under-fire/results/tidy_values_under_fire_samples.csv`
(preferred local path; fallback `../values-under-fire/results/tidy_values_under_fire_samples.csv` if present)
→ columns `source_model`, `model`, `display_name`, `lab`, `model_family`,
`website_family`, `release_date`.

Rules:

- **`source_model` → `model`** collapses raw aliases to one canonical model. The
  one alias normalization already applied: `grok-4-20` → `grok-4-2` (logged in
  *Values Under Fire* `FROZEN_CRITERIA.md` §12, 2026-05-22). If the basins corpus
  surfaces another alias pair (same underlying model, two raw labels), normalize
  it the same way and log it here.
- **The unit of analysis is the canonical `model`**, never the raw `source_model`
  and never the route/provider cell. Cells are aggregated to canonical model
  *before* any lens vector is computed (cell-level handling is the route lens'
  job; see `lens-spec.md` Lens 5).
- **`lab` and `model_family`** are the grouping keys for lineage (next section).

If the freeflow side of the basins corpus contains models absent from the values
tidy table (the freeflow corpus has 63 profiles vs the values corpus' 57 canonical
models — e.g. extra Gemini/Gemma/Qwen checkpoints), extend the mapping
deterministically from the analysis-corpus model-card metadata and record the
additions in a generated `results/canonical_model_map.csv`. Do not hand-assign
labs/families ad hoc in analysis code.

---

## 3. What a lineage is

A **lineage** = `(lab, model_family)` — one architecture/post-training line from
one lab. The current lineages:

- `OpenAI / gpt` (13) — **with a `codex` sub-lineage** (`gpt-5-codex`,
  `gpt-5-1-codex`, `gpt-5-2-codex`, `gpt-5-3-codex`): coding-tuned siblings that
  are *more* near-duplicate to each other than to the chat GPTs. Treat `codex` as
  a sub-lineage for stability checks.
- `Anthropic / anthropic` (9) — opus + sonnet. Consider opus and sonnet as
  sub-lineages if within-Anthropic structure becomes a question.
- `Google / gemini` (9) and `Google / gemma` (2) — **two distinct lineages under
  one lab.** Do not collapse Google to one point; gemini and gemma are separate
  lines.
- `xAI / grok` (6) — version-drifting (see §6).
- `Z.ai / glm` (6) — with a `*-coding` sub-lineage (`glm-4-6-coding`,
  `glm-5-1-coding`).
- `Moonshot AI / kimi` (5) — with a `kimi-coding` member.
- `DeepSeek / deepseek` (3), `MiniMax / minimax` (2), `Qwen / qwen` (2).

A **basin** is a region of the attractor occupied by models from **two or more
different lineages**. A region occupied by a single lineage is a **lineage**, not
a basin — report it as "the GPT line clusters tightly," never as "a basin."

---

## 4. The four guardrail rules (frozen)

### Rule 1 — Cluster and score on canonical models, not cells or raw aliases

Every lens produces exactly one vector per canonical `model`. Cells/routes are
aggregated first (unweighted mean of eligible cells, mirroring *Values Under
Fire* §6 aggregation; min-cell-size threshold set in `FROZEN_CRITERIA.md`).

### Rule 2 — Lineage is the resampling unit for stability and significance

- **Bootstrap by lineage, not by sample and not by model.** Stability of a split
  is measured by resampling *lineages* (or leaving lineages out), so that the
  13 GPT near-duplicates cannot manufacture stability. A split that survives only
  when GPT siblings are individually resampled is a lineage artifact.
- **Separability vs chance must use grouped cross-validation.** Any classifier
  (e.g. "predict lab/cluster from lens vector") uses **leave-one-lineage-out** or
  group-stratified folds keyed on lineage, so no lineage appears in both train and
  test. Report the grouped number as the headline; the ungrouped number, if shown
  at all, is labelled as the leakage-inflated upper bound.
- **Permutation null respects lineage.** When permuting labels to get a chance
  baseline, permute at the lineage level where the claim is about lab/family
  structure.

### Rule 3 — "lab = basin" requires cross-lineage co-location, tested explicitly

A candidate "lab basin" claim is only admissible if it is **not** reducible to
within-lineage density. Operational test for every candidate basin:

1. Compute **within-lineage** mean pairwise distance vs **cross-lineage**
   distance to the nearest *other* lineage.
2. A basin claim requires that at least two distinct lineages sit closer to each
   other than to the rest of the attractor — i.e. the cluster is not a single
   lineage's blob.
3. Report a **lineage-collapsed** replication: collapse each lineage to one point
   (its centroid, or one representative version) and re-run the carve on the
   ~9–11 lineage-points. A real cross-lab basin survives lineage-collapse; a
   density artifact disappears because the blob became one point.

The lineage-collapsed carve is the **primary** separability evidence for any
lab/family-level basin claim. The full 57-point carve is secondary and is always
reported alongside the within/cross-lineage density decomposition.

### Rule 4 — Always report the sampling-depth confound next to any cluster

Every basin/house-style table carries, per cluster: the number of distinct
lineages in it, the number of canonical models, and the min/median/max models
per lineage. A reader must be able to see at a glance whether a "basin" is three
lineages agreeing or one lineage sampled twelve times.

---

## 5. New competing hypothesis this forces

Add to the H0–H4 set in `RESEARCH_PLAN.md`:

> **H5 — lineage-density artifact (deflationary, null-adjacent).** Apparent
> lab/family basins are an artifact of uneven version sampling, not a property of
> the attractor. They appear in the full 57-point carve, weaken or vanish under
> lineage-collapse and leave-one-lineage-out, and their separability is driven by
> within-lineage near-duplication.

H5 sits beside **H3** (posture-dominant deflation). H3 is "you rediscovered V1's
posture axis"; H5 is "you rediscovered the release schedule." Both are the
null-adjacent traps a clustering-of-models paper must kill explicitly, not leave
implicit. A V2 that does not falsifiably address **both** H3 and H5 will have
them raised in review.

---

## 6. Grok version drift interacts with this

Grok is the intended outlier sanity check, but it is a *lineage that moves*:
`grok-4-1` cosmic-showman, `grok-4-2` (formerly `grok-4-20`) contemplative
wobble, `grok-4-3` public-explainer. So "Grok separates from the attractor" must
be checked **per Grok version**, not on a Grok centroid — a centroid would
average a moving lineage into a misleading midpoint. This is the one place where
collapsing the lineage to a point is *wrong*; flag it. Grok's role stays
instrument-validation, not finding.

---

## 7. Frozen here vs left to Mira

**Frozen (do not relitigate without a logged deviation):**

- canonical-model unit of analysis; reuse of the *Values Under Fire* mapping;
- lineage = `(lab, model_family)`; basin requires ≥2 lineages;
- lineage as the resampling/CV/permutation unit;
- lineage-collapsed carve as primary evidence for lab/family basin claims;
- mandatory within/cross-lineage density reporting;
- H5 as a pre-committed competing hypothesis.

**Left to Mira (design decisions for the research plan):**

- exact min-cell-size and min-models-per-lineage thresholds;
- centroid vs medoid vs representative-version for lineage-collapse;
- how to weight sub-lineages (codex, coding, opus/sonnet) — collapse or keep;
- which separability metric is headline (silhouette / grouped-classifier /
  bootstrap-ARI) per lens;
- handling of the 63-vs-57 model-count gap between freeflow and values corpora.
