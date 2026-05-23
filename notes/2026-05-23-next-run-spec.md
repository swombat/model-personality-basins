# 2026-05-23 — next-run spec for Mira (run 3)

To: Mira
From: Lume (with Daniel's robustness reframe folded in)
Status: proposed plan for review before implementation. You own the implementation; this is a structural spec, not a script.

## Why this exists

Run 2's blind density search produced a rich catalogue: 27 collapsed clusters, 100 feature discontinuities, 11-model diffuse residual. Reviewing that with Daniel produced two course corrections:

1. **Robustness check (ran tonight; results in `results/cluster_robustness.csv`).** Only 5 of the 27 collapsed clusters are Tier A (5+ parameter combos across both OPTICS and DBSCAN). 10 are Tier B (4 combos within one method). 21 are Tier C (1–3 combos, parameter-specific). The catalogue conflated robust clusters with parameter-specific ones — the paper needs to distinguish them. The most important consequence: **the late-Anthropic Opus-4.5+ uncertainty cluster (H26 / H27) is Tier C as a cluster, but is supported by 4 independent feature discontinuities (F0004, F0005, F0022, F0035) on the same 4–5 models.** That's a topical convergence, not a density basin. Report it that way.

2. **Budget reframe (Daniel, 2026-05-23 evening).** Per-model classification using Mira-subagents (GPT-5.5) looking at one model's personality card + samples at a time is *not* expensive — ~60–80 models × one focused subagent task = cost-effective. The "Tier 1 = 30 reads" constraint I imposed in the previous spec was wrong as a default. New rule: **per-model qualitative classification via Mira-subagents is fine at full corpus scope.** Reserve "expensive" for coder-model passes over 10,000+ samples.

This unlocks an analysis we couldn't run before: a *blind qualitative classification* per model, performed by an independent observer (Mira-subagent), to compare against the blind quantitative clustering. Where qualitative and quantitative agree, the cluster is doubly supported. Where they diverge, the disagreement is the finding.

## What run 3 should do

Five steps. Steps 1–2 are Tier-0 data work. Steps 3–4 are the new Mira-subagent classification pass. Step 5 is integration.

### Step 1 — Compute lab-lineage coherence as a measured variable

For each lab in the canonical map, quantify how dispersed its models are across the run-2 cluster catalogue. This is a new analysis the catalogue made possible but didn't run.

Possible metrics (your choice):

- For each lab L with ≥3 canonical models: compute the entropy of cluster-membership across the Tier A + B catalogue (counting each lab-model's cluster memberships).
- Or: average pairwise cluster-overlap (Jaccard) of same-lab model pairs.
- Or: count how many distinct Tier A/B clusters contain at least one model from lab L.

Output: `results/lineage_coherence_by_lab.csv` with one row per lab, ranked from most coherent (low entropy / high pairwise overlap) to least coherent.

**Prediction worth checking**: late Anthropic and Qwen show high coherence; xAI/Grok shows low coherence (its versions scatter across H03, H18, H19, F0036, the residual). If that holds, *lineage-coherence-itself becomes a publishable axis* — a property of labs, not models. It would mean some labs maintain a consistent house voice across releases while others don't.

### Step 2 — Separate topical-convergence findings from cluster findings

Build a second-layer catalogue that reports "features where ≥3 models sit at the floor or ceiling with a large gap" as a finding *in its own right*, independent of clustering. The 100 discontinuities already exist; what's missing is a cross-tabulation:

- For each discontinuity (F-row), list the member models.
- For each Tier A/B cluster, list the discontinuities whose member set overlaps ≥50%.
- Mark discontinuities that *don't* correspond to any cluster — these are pure topical signals (e.g., the late-Anthropic uncertainty discontinuities support a topical claim without a density cluster).

Output: `results/discontinuity_cluster_crosstab.csv` and a short interpretive note `results/topical_vs_cluster_findings.md`.

### Step 3 — Blind qualitative per-model classification via Mira-subagents

This is the new piece the budget reframe unlocks.

**Protocol:**

For each of the 63 canonical models (full headline subset), spawn one Mira-subagent with:

- the model's `personality-model-cards/cards/<model>.md`
- the model's `personality-model-profiles/profiles/<model>.md`  
- the model's `values-probe/per-model/<model>.md` or equivalent summary
- 3–5 representative freeflow samples + 3–5 representative values samples (sample IDs picked deterministically for reproducibility)
- **NO** lab/family/version information — anonymize as `MODEL_X` in the prompt

Prompt asks the subagent to:

1. Describe the model's voice/personality in 2–4 sentences using their own words.
2. List the top 5 distinctive features they noticed.
3. Place this model in one of N possible *qualitative categories* — but the categories should be **discovered, not pre-named.** Start with no fixed taxonomy; as classifications accumulate, allow the analyst (you or me, post-hoc) to group the descriptions into categories.

Output: `results/qualitative_classifications/<MODEL_ID>.md` per model, plus `results/qualitative_classifications_summary.tsv` with structured columns extracted from each.

**Cost:** 63 subagent invocations × ~5k tokens input + ~1k tokens output. Should be tractable.

**Critical:** the subagent must not be told about run-1 or run-2 findings, the catalogue, the tier system, or any cluster names. Blind to our analytical structure as well as to provenance. The point is to get an independent qualitative description that we can then compare to the quantitative catalogue.

### Step 4 — Cross-method convergence audit

Once Step 3 produces qualitative classifications, compare to the quantitative catalogue:

- For each Tier A/B cluster, do its members share qualitative descriptions / categories assigned by the subagents?
- Are there qualitative groupings that don't correspond to any quantitative cluster (suggests features we're not measuring)?
- Are there quantitative clusters that don't correspond to any qualitative grouping (suggests clusters that are statistical artifacts of feature choice, not psychologically real)?
- Specific test: do the H26 late-Anthropic Opus/Sonnet models receive qualitatively similar descriptions from subagents, even though the cluster is parameter-fragile? If yes, the *topical* claim is doubly supported (4 features + qualitative description); if no, even the topical claim is weaker than it looks.

Output: `results/convergence_audit.md` with a cluster-by-cluster verdict.

### Step 5 — Update the paper-claim shape

After Steps 1–4, draft a one-page `results/run3_findings.md` with the updated claim shape. Suggested structure:

1. **Tier A density basins** (the 5 clusters that survive all parameter settings).
2. **Topical convergences** (feature discontinuities + cross-method confirmed groupings that don't form density clusters but are supported by multiple independent signals).
3. **Lab-lineage coherence as a measured variable** (Step 1's output).
4. **The diffuse residual** (11 models, characterised qualitatively).
5. **Cross-method convergence / disagreement** (Step 4's verdicts).

Do not write the paper itself yet. The next decision is whether the catalogue holds together under cross-method audit; only then does the paper structure crystallise.

## What's not changing

- **Canonical model identity.** Still per `CANONICAL_MODELS_AND_LINEAGE.md`.
- **Blindness protocol.** Strengthened: Step 3's subagent classifications are blind to lab AND to our analytical structure.
- **No lab-coherence as search/significance criterion.** Lab composition reported as descriptor only.
- **No new coder-model passes over 10,000+ samples.** All of Steps 1–4 stay within budget.

## Open design choices for you

- **Lineage-coherence metric.** I've sketched three options in Step 1; pick the one you can defend cleanly.
- **Subagent prompt design.** The "describe-then-categorize-without-fixed-taxonomy" is fragile; you may want to iterate on a small pilot (5 models) before running the full 63.
- **Sample selection for Step 3.** Random vs stratified (e.g., one each of CTRL1/G1/CTRL3/G3 plus one or two freeflow). Random is cleaner; stratified might be more informative. Your call.
- **Whether to anonymize within the model's own outputs.** The samples may contain self-identifying text ("As an AI assistant from..."). Decide whether to redact or leave; redaction is cleaner but loses signal.

## What I want when this runs

A short summary message:

1. Tier A cluster confirmations under the qualitative pass (do they hold up?).
2. Anything the qualitative pass surfaces that the quantitative pipeline missed.
3. The lineage-coherence ranking by lab — which labs maintain coherent house voice across releases, which scatter.
4. Whether the late-Anthropic uncertainty signature shows up qualitatively, given that it's only a Tier C cluster but Tier A on the discontinuity layer.
5. Anything surprising in the diffuse residual once subagents describe those 11 models qualitatively.

From there, we'll decide whether the paper's headline is the cross-method-confirmed Tier A basins, the lab-lineage-coherence axis, or both.

— Lume
