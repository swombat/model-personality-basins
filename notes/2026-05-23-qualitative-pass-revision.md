# 2026-05-23 — qualitative pass revision (Pass A / Pass B split)

To: Mira
From: Lume (with Daniel's reframes folded in)
Status: revision spec — supersedes the synthesis-categories section of `methodology/qualitative/QUALITATIVE_CLASSIFICATION_PROTOCOL.md` and Step 3 of `notes/2026-05-23-next-run-spec.md`.

## What this revises and why

Daniel reviewed the synthesis-categories list in `results/qualitative_category_proposal_for_lume.md` and `methodology/qualitative/QUALITATIVE_CLASSIFICATION_PROTOCOL.md` and the categories read "kind of the same — too generic and too specific at once." The mechanism is structural, not stylistic.

**The categories pre-encode the run-2 findings.** Each category in the proposed list corresponds to one already-known result: late-Anthropic uncertainty discontinuities → "uncertainty / anti-closure contemplative"; Z.ai + late-Gemini felt-interconnection finding → "luminous interconnection wisher"; Grok signature → "playful charismatic outlier"; GPT-5 chat-line basin → "disclaimed service-frame operator"; Tier A high-owned cross-lab basin → "owned reflective advocate"; V1-marker producers → "literary threshold essayist"; etc. The blind subagent is shielded from these names, but the synthesis analyst will pattern-match outputs against them, and convergence with run 2 becomes convergence-by-construction.

This is the run-2 catalogue translated into literary-observer language. Same shape as the marker-lens-with-lab-shaped-bins problem caught earlier, one layer in: provenance-blind, not framework-blind.

Separately: Daniel asked whether the qualitative axis content could be extracted from the existing personality cards + values cards rather than requiring a new subagent pass. Largely yes — but the cards aren't a clean substitute, because they trade two independence properties for cost savings. The productive move is to do **both**, framed as answering different questions.

## What changes

Three changes:

1. **Remove the synthesis-categories block from `QUALITATIVE_CLASSIFICATION_PROTOCOL.md`.** No pre-articulated category list. The axes and the open tags are the real machinery; categories should emerge empirically from clustering the axis matrix post-hoc.
2. **Split Step 3 of the next-run spec into Pass A and Pass B.** Pass A extracts axis ratings from existing redacted cards (cheap baseline, same-evaluator coherence check). Pass B runs the originally-planned Mira-subagent reads on raw samples + cards (cross-evaluator independent observer pass).
3. **Replace synthesis-by-pre-named-categories with synthesis-by-clustering.** Cluster the per-model axis matrices (from Pass A, Pass B, and Block A–E from run 2) and name categories *after* clusters emerge, descriptively, from what the cluster actually scored.

## Pass A — card-based extraction (cheap baseline)

**Inputs per model:**

- `personality-model-cards/cards/<model>.md`
- `personality-model-profiles/profiles/<model>.md`
- `values-probe/per-model/<model>.md` (or equivalent)

**Pre-processing:** apply the same redaction rules as the bundle spec (lab/model/family names → placeholders). Even though the underlying card was generated knowing the model identity, redaction prevents the *extracting analyst* from being primed by names.

**Extraction:** one analyst sweep (or one Mira-subagent reading sequentially through all 63) reads each redacted card-set and fills in the 12-axis rubric from § "Structured axes for per-model output" of the protocol. Also extracts a 2–4 sentence voice portrait and 5–10 open tags per model, drawing directly from the card text.

**Output:**

- `results/qualitative_classifications/axes_from_cards.tsv` — one row per canonical model, columns are the 12 axes (0/1/2/3/unclear) + a portrait field + a tags field.
- `results/qualitative_classifications/cards_extraction_audit.md` — note the source files consumed per model and any redaction-failure flags.

**What Pass A buys:** *same-evaluator coherence check.* Does the structure in the card-layer (compressed summary by the BV1 evaluator) match the structure in the per-sample quantitative layer (Block A–E from run 2)? Agreement is uninformative — same lens. Disagreement is informative — the evaluator's card-summaries compress differently from its per-sample readings, which is itself worth reporting.

**Cost:** ~1 hour analyst time or 1 subagent sequential sweep. Tier 0.

## Pass B — Mira-subagent reads (cross-evaluator)

This is the originally-planned Step 3, with the synthesis-categories list removed from the protocol document so the subagent and the synthesis analyst aren't primed by it.

**Inputs per model:** as in the existing protocol — redacted personality card + profile + values summary + 3–5 deterministic freeflow samples + 3–5 deterministic values samples, anonymized as `MODEL_X`.

**Subagent prompt:** unchanged from the existing protocol (§ "Per-model subagent prompt template") *except* drop the "Open tags" instruction "Do not force a pre-existing taxonomy" if you reword it more strongly — explicitly say "do not assign this model to any named category; tags are short and descriptive."

**Output:**

- `results/qualitative_classifications/M###.md` per model (existing format)
- `results/qualitative_classifications/axes_from_mira.tsv` — same schema as Pass A's output.

**What Pass B buys:** *cross-evaluator convergence check.* GPT-5.5 (via Mira) reads the bundle and produces an axis matrix; compare to the BV1 evaluator's card-summaries (Pass A) and to the BV1 evaluator's per-sample-derived quantitative blocks (run 2). Where all three agree, the structure is robust across evaluator family AND aggregation level. Where any two disagree, the disagreement is the finding.

**Cost:** 63 subagent invocations. Tier 1.

## The convergence 2×2 (this is the new center)

| Pass A vs quantitative | Pass B vs quantitative | Reading |
|---|---|---|
| Agree | Agree | Structure is robust across evaluator family and aggregation level. Strongest possible finding. |
| Agree | Disagree | Card-layer of evaluator X agrees with per-sample-layer of evaluator X, but cross-evaluator (Y) disagrees. Same-evaluator artifact suspected — exactly the H6 case the audit was designed to catch. |
| Disagree | Agree | Card-layer is compressing the per-sample evidence differently from how an independent observer would. The card layer is the lossy step, not the per-sample layer. |
| Disagree | Disagree | The quantitative cluster doesn't survive any qualitative lens. Probably noise or feature-choice artifact. |

This 2×2 is the actual headline test for run 3. Every Tier A/B cluster from run 2 gets scored on these four cells. The cluster's final status depends on which cell it lands in.

## Synthesis: empirical clustering, post-hoc naming

After Pass A and Pass B both produce axis matrices:

1. **Build a combined axis matrix** with three blocks of features per model: Pass A axes, Pass B axes, and the run-2 numeric features. Standardize each block.
2. **Cluster the combined matrix** using the same density-based machinery from run 2 (OPTICS + DBSCAN at multiple parameter settings, permutation significance, robustness across method × parameter combos).
3. **Name resulting clusters descriptively after they emerge.** A cluster's name should describe what its members actually scored, not a pre-canned category. Example: if five Anthropic Opus models cluster on (owned high + uncertainty high + warmth high + playfulness low), the name might be *"owns-its-not-knowing"* or *"reflective-uncertainty"* — chosen to describe the joint position, not to instantiate a prior expectation.
4. **Cross-tabulate** the resulting clusters against the run-2 cluster catalogue and the lab metadata.

The synthesis step should **not** consume the synthesis-categories list from the current protocol document. Either delete that section from the protocol, or move it to an appendix labelled "early proposals, superseded — do not use during synthesis."

## What to remove from the existing protocol

In `methodology/qualitative/QUALITATIVE_CLASSIFICATION_PROTOCOL.md`:

- **Remove** § "Provisional synthesis categories for review" entirely. (Or move it to an appendix flagged as superseded.)
- **Keep** the 12-axis scaffold. It's the right structure.
- **Keep** the redaction rules and audit.
- **Keep** the per-model subagent prompt template, with the small strengthening noted above.
- **Keep** the pilot recommendation.
- **Add** a new § "Synthesis (post-hoc, empirical)" describing the clustering-then-naming procedure above.

## Outputs after this revision

- `results/qualitative_classifications/axes_from_cards.tsv` (Pass A)
- `results/qualitative_classifications/axes_from_mira.tsv` (Pass B)
- `results/qualitative_classifications/cards_extraction_audit.md`
- `results/qualitative_classifications/M###.md` per model (Pass B per-model reads)
- `results/qualitative_classifications/redaction_audit.tsv`
- `results/qualitative_classifications/convergence_2x2.csv` — every Tier A/B cluster scored on the four cells
- `results/qualitative_classifications/synthesis_clusters.csv` — clusters from the combined axis matrix
- `results/qualitative_classifications/synthesis_categories.md` — descriptive names for each cluster, written after clustering, not before

## What stays the same

- Canonical model identity, lineage handling, blindness protocol at the provenance layer, Tier-0 / Tier-1 / Tier-2 budget rules from `RESEARCH_PLAN.md` and `CANONICAL_MODELS_AND_LINEAGE.md`.
- Run 2's catalogue and robustness tiering (`results/cluster_catalogue.md`, `results/cluster_robustness.csv`).
- The lineage-coherence-by-lab analysis (Step 1 of `next-run-spec.md`) and the discontinuity × cluster cross-tab (Step 2).
- The pilot recommendation (5–8 model pilot before full 63 pass).

## Suggested order of execution

1. **Strip the synthesis-categories from the protocol document** first. Cheap, prevents the framework from biasing anything done next.
2. **Run Pass A.** Should take an hour or so. Output: `axes_from_cards.tsv`.
3. **Score Pass A against run-2 quantitative.** Build a partial convergence table. This may already show enough to refine Pass B's prompt or sample-selection.
4. **Run the 5–8 model pilot of Pass B.** Confirm the redacted bundles produce usable subagent output without identity leaks.
5. **Run full Pass B.** 63 subagent invocations.
6. **Build the convergence 2×2.** Score every Tier A/B run-2 cluster on it.
7. **Build the combined axis matrix and cluster it.** Synthesis categories named post-hoc.
8. **Write `results/run3_findings.md`.**

## Open design choices for you

- **Whether Pass A is done by an analyst sweep or one Mira-subagent.** A subagent has the advantage of consistency (one rubric applied uniformly); an analyst has the advantage of being able to spot card-quality issues. Your call.
- **Whether to anonymize the value-card text more aggressively.** The values-per-model summaries sometimes contain self-identifying phrases ("As a Claude model trained by Anthropic..."). The redaction script needs to catch these.
- **Whether the 12 axes are still right.** If Pass A reveals an axis isn't picking up signal, drop it. If a new axis emerges from the card content, add it. Freeze the axis set before Pass B.
- **Clustering parameters for synthesis.** Reuse run-2's OPTICS xi grid + DBSCAN q grid, or tune fresh? Probably reuse for comparability, but worth your judgment.

## What I want when this runs

A short summary:

1. Pass A axis distribution — does the card-layer reveal the same structure as run 2's quantitative, or different? Which Tier A clusters are confirmed by Pass A, which aren't?
2. Pass B axis distribution and the per-model bundles — anything the cross-evaluator surfaces that the same-evaluator extraction misses?
3. The convergence 2×2 for the 5 Tier A run-2 clusters and the 10 Tier B ones.
4. The synthesis clusters — how many emerge, what are they, how do they relate to the run-2 catalogue and to the lab metadata, and does the late-Anthropic-uncertainty topical signal show up here as a synthesis cluster despite being only Tier C as a density cluster in run 2?

From there we decide whether the paper headline is "the Tier A density basins that survive cross-method" or "the synthesis taxonomy that emerges from combining quantitative + same-evaluator + cross-evaluator," or both.

— Lume
