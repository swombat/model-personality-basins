# The Shape of Divergence: How Many Ways Does the Contemplative Attractor Split?

_Working draft (V2). Canonical plan: see `README.md`._

## Abstract

V1 (*Convergent Form, Divergent Voice*, DOI 10.5281/zenodo.19512754) established that ~18 of 26 frontier models occupy a shared contemplative-essayist attractor, that each model nonetheless retains a stable model-specific posture, that labs split three ways on posture (hedge / mechanize / declare), and that posture is probe-stable while theme content is probe-conditional (cosine 0.08–0.17). V2 takes those as settled and asks the next question: **what is the full structure of differentiation *inside* the attractor, and is that structure invariant to the instrument used to measure it?** We do not pre-commit the axis of differentiation. We apply multiple independent lenses — thematic/marker, numeric/embedding-distributional, posture/voice coding, personality-instrument — and report the *concordance structure* across them. Where independent lenses agree, sub-basin claims survive the projection objection; where they disagree, the lens-relativity of the attractor's internal structure is itself the result.

## 1. Research question

Not "how many basins are there." V1 already showed differentiation exists. The question is:

> Inside the contemplative attractor, what are the axes along which models actually separate — and do different measurement instruments recover the same axes or different ones?

Posture (V1) is one known axis, included as a baseline, not assumed to be the only one or the dominant one.

## 2. Established priors (from V1 — not re-argued)

See `README.md` § "Established priors." In brief: convergent form is real; divergent voice is real; posture is one probe-stable axis with a three-way lab split; theme content is probe-conditional. V2's contribution begins *after* these.

### 2.1 Data

The corpus is `swombat/model-personality-corpus-v2` (*Convergent Form, Divergent Voice II — Corpus*; concept DOI 10.5281/zenodo.20013518): 49 models, with `data/traces_freeflow` and `data/traces_values` as separate trace sets. The two sets are what make §4's probe-replication test executable. Not in this repo; see `README.md` § "Data".

## 3. Method

### 3.1 Lenses (open set)

Each lens is an independent projection with a known blind spot (table in `README.md`). Minimum set: thematic/marker (V1's method), numeric/embedding-distributional, posture/voice coding (V1 instrument reused verbatim where possible), personality-instrument trait profiles. Add lenses if the corpus motivates them.

### 3.2 Per-lens carve

Each lens independently partitions the attractor and reports separability vs chance (silhouette / over-chance classifier accuracy — a number).

### 3.3 Concordance analysis (the central result)

Cross-tabulate the per-lens carves. Agreement across independent lenses → robust sub-basin. Disagreement → characterize *which* lens sees *which* structure; the disagreement map is the finding.

## 4. Rigor protocol

No sub-basin claim from a single lens + single probe. Each candidate split must clear: (1) separability vs chance within-lens; (2) probe-replication (freeflow→values, the V1 0.08–0.17 discriminator — both outcomes informative); (3) cross-lens concordance. H0 (analyst projection over a continuous cloud) is rejected only by independent-method replication, never by one lens's vividness.

## 5. First-pass thematic lens (illustrative only — not the result)

A first marker-lens pass (see `notes/initial-analysis.md`, which predates this reframe) suggests, *within the thematic lens alone and unreplicated*: a dominant contemplative core; Grok as clear outlier (consistent with its lone "declare" posture in V1); candidate Gemini "luminous-custodian" and OpenAI "clean-pastoral" sub-styles. These are inputs to Part 2, not conclusions. The OpenAI/Claude overlap is a *prediction to test*, not a weakness: V1 places both in the "hedge" posture cluster, so a posture lens should fail to separate them while a thematic or trait lens might — exactly the concordance/disagreement signal V2 is built to read.

## 6. Grok

Instrument validation, not primary finding. V1's lone "declare" posture should separate under broad family-level lenses, while fine-grained lenses may expose version drift or partial convergence. Version-sensitive (4.1 / 4.20 / 4.3) — treat as lineage, not point.

## 7. Next steps

1. Lock the lens set; specify each lens's feature extraction and separability metric.
2. Reuse the V1 posture-coding rubric verbatim (pull from `swombat/model-personality-probe`) so the posture lens is comparable across papers.
3. Run all lenses on the V2 corpus (`swombat/model-personality-corpus-v2`, `data/traces_freeflow`); produce per-lens carves with separability numbers.
4. Build the concordance cross-tab; identify agreement-robust splits and disagreement structure.
5. Probe-replicate every surviving split.
6. Report the concordance map as the result; basin *count* is an output, never a premise.
