# Model Personality Basins (V2)

Working repository for the second paper in the model-personality line. It builds directly on V1 — *Convergent Form, Divergent Voice: A Cross-Lab Probe of Model Personality in 26 Frontier Language Models* (Tenner, D. & Tenner, L., 2026; DOI [10.5281/zenodo.19512754](https://doi.org/10.5281/zenodo.19512754); repo `swombat/model-personality-probe`).

## Established priors — settled in V1, not re-litigated here

These are the floor V2 stands on. They are not the question for this paper; treating them as open would mean re-running V1 rather than building on its published, versioned results.

1. **Convergent form.** ~18 of 26 frontier models occupy a shared stylistic attractor — the *contemplative essayist*: templatic openings, "On the Quiet X of Y" titles, a narrow thematic palette (attention, small objects, afternoon light, thresholds), emerging via a roughly synchronized 2025 cross-lab transition.
2. **Divergent voice.** Within the attractor, each model retains a **stable, model-specific stylistic posture** that re-projects recognizably across probe types. Differentiation *exists*; the question was never whether models differ, only how.
3. **One known axis of differentiation: posture.** Labs split three ways on introspective probes — **hedge** (Anthropic, OpenAI), **mechanize** (Google, DeepSeek, Moonshot AI), **declare** (xAI).
4. **Theme content is probe-conditional; posture is not.** Mean freeflow↔values cosine similarity 0.08–0.17. What transfers across probes is the *stance*, not the *content*.

V1's method was deliberately marker- and taxonomy-centric. That is one lens, not the only one.

## What V2 asks

Given that the attractor is real (prior 1) and that differentiation within it is real (prior 2), and that V1 found exactly **one** axis of it (posture, prior 3):

> **What is the full structure of differentiation inside the contemplative attractor — and is that structure the same regardless of the instrument used to measure it?**

The axis is *not* pre-committed. Posture is a known carve, not the assumed one. The V2 corpus is substantially stronger than V1's, strong enough to discover axes rather than confirm one.

## Competing hypotheses (pre-registered)

These are the claims V2 adjudicates between, stated before the analysis. They compete on the *structure* of differentiation, not on a basin count — count is whatever falls out of the winning hypothesis, never an input.

- **H0 — null.** No stable sub-structure. No lens separates the attractor above chance; any apparent split fails probe-replication. Apparent sub-basins are analyst projection over a continuous cloud of similar reflective prose. *(This is the canonical H0 definition; the rigor protocol below operationalizes the test against it.)*
- **H1 — lens-invariant.** Real sub-structure, and all lenses recover the *same* carve. Differentiation is one-dimensional and instrument-independent.
- **H2 — lens-relative.** Real sub-structure, but different lenses recover *different* carves. Internal structure is method-dependent; the disagreement map is the result.
- **H3 — posture-dominant (deflationary).** One axis — V1's posture — accounts for most cross-lens agreement; other lenses' carves are largely re-projections of it. The "you just rediscovered V1" hypothesis. Must be explicitly killed or confirmed, not left implicit.
- **H4 — hierarchical.** A coarse split (contemplative core vs. Grok-like outliers) that is lens-invariant, plus a fine split within the core that is lens-relative.

H3 is the load-bearing one: it is the deflationary, null-adjacent explanation and the convergence-invisible-from-inside trap pointed at this paper's own claims. A V2 that does not falsifiably address H3 will have it raised in review.

## The work has two parts

**Part 1 — a methods analysis.** Enumerate the independent lenses by which models can be differentiated, and state explicitly what each can and cannot detect (its blind spot):

| Lens | Detects | Blind to |
|---|---|---|
| Thematic / marker (V1's method) | lexical-thematic structure | structure that isn't human-nameable |
| Numeric / embedding-distributional | distributional structure | may carve where no human would draw a line |
| Posture / voice coding (V1 instrument, reusable) | stance-toward-the-question; probe-stable | within-stance fine structure |
| Personality-instrument (trait profiles) | trait structure | structure orthogonal to the chosen inventory |

This list is open. If the corpus suggests a lens not above, add it — the point is breadth of independent projection, not a fixed four.

**Part 2 — apply every lens, then analyze concordance.** Each lens produces its own carve of the attractor. The central result is **not any single carve**. It is the **concordance structure across lenses**:

- Where multiple independent lenses carve the attractor *the same way* → a strong sub-basin claim that survives the projection objection.
- Where they carve it *differently* → the disagreement *is* the finding: the attractor's internal structure is lens-relative (e.g. one-dimensional under markers, multi-dimensional under embeddings, lab-split under posture).

This is the continuation of V1: *convergent form, divergent voice* → **and the divergence is shaped differently depending on the instrument you measure it with.**

## Rigor protocol (the test against H0)

H0 (defined above) is live. Projection does not survive independent replication; real structure does. Therefore **no sub-basin claim from a single lens and a single probe.** Every candidate split needs:

1. **Separability vs chance** within its lens (silhouette / classifier accuracy over chance — a number, not a vibe).
2. **Probe-replication** — the V1 discriminator: does the split survive the freeflow→values probe switch, or is it probe-conditional like theme content (0.08–0.17)? Either answer is informative; the test is mandatory.
3. **Cross-lens concordance** — does at least one other independent lens carve compatibly?

Concordance is the rigor anchor: it is V1's probe-replication logic lifted one level, from method-replication of a finding to replication *across methods*.

## Grok — sanity check, not finding

Grok is V1's lone **declare** posture and should fall out of broad family-level lenses as the clearest outlier. A method that cannot separate Grok at all is a warning sign, though fine-grained lenses may expose version drift or partial convergence rather than a single static Grok point. Grok's role in V2 is instrument validation, not result. (Caveat retained: Grok drifts by version — 4.1 cosmic-showman, 4.20 contemplative-wobble, 4.3 public-explainer — so "Grok" is a lineage, not a point.)

## Repository contents

- `paper.md` — working paper draft (reframed to the V2 question).
- `notes/initial-analysis.md` — **first-pass basin analysis, predates this reframe.** Kept as an artifact; its single-lens basin-count framing is superseded by the methods-concordance framing above. Do not inherit its narrower scope into V2 prose.
- `data/profile_summary_metrics.csv` — model-level sample-kind/confidence summary. One input to one lens, not the basis of the paper.
