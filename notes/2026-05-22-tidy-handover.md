# 2026-05-22 — tidy-up + handover to Mira

## Why this pass happened

This repo was created before three things existed: the shared paper **template**
(`~/dev/research/_template`), the **Values Under Fire** paper (whose
research-plan / frozen-criteria format is now the house style), and the
**tidy-up of the analysis corpus** (now 63 profiles / 18,850 BV1 readings, with a
canonical model mapping and a quarantined posture layer). It also had a known
weak spot: nothing in the framing stopped *lineage non-independence* from faking
a "lab = basin" result. Daniel asked for a tidy that fixes all of that and leaves
the repo ready for Mira to turn into an operational research plan.

## What changed

**Structure → template.** Adopted the `_template` layout: `paper/` (LaTeX
skeleton), `methodology/`, `analysis/scripts/`, `results/`, `Makefile`, merged
`.gitignore`. Migrated the old planning docs into `methodology/`:
`PLAN.md → IMPLEMENTATION_PLAN.md`, `docs/phase1-* → analysis-universe.md`,
`docs/phase2-* → lens-spec.md`. The old reframed `paper.md` → `notes/superseded-
paper-draft-v0.md` (its content lives on in the README priors and the plan).

**New: the lineage guardrail.** `methodology/CANONICAL_MODELS_AND_LINEAGE.md` is
the load-bearing addition and is **frozen**. The corpus is ~9 lineages sampled at
very uneven depth — OpenAI carries 13 canonical models, Qwen carries 2. Naive
clustering rewards the dense GPT blob and reports "OpenAI is a basin," which is an
artifact of checkpoint count, not attractor geometry. The fix: cluster on
canonical models (reuse the *Values Under Fire* mapping), make lineage the
resampling / leave-one-out-CV / permutation unit, require cross-lineage
co-location and lineage-collapse survival before any lab-basin claim, and always
report within- vs cross-lineage density. This forced a new competing hypothesis,
**H5 — lineage-density artifact**, which now sits beside H3 (posture-dominant) as
the second mandatory deflation.

**Corpus references corrected.** The earlier README/paper said "every lens
applied to corpus-v2." That was imprecise: the lenses run off the
**analysis-corpus derived layers**; corpus-v2 is raw provenance for quotation and
audit. `data/README.md`, `analysis-universe.md`, and `RESEARCH_PLAN.md` §2 now
say this consistently. (The old `analysis-universe.md` actually had this right
all along; the README/paper were the wrong ones.)

**Posture-coding quarantine wired in.** The analysis-corpus freeflow
posture-coding layer is quarantined (over-calls `owned`). Lens 2 must source from
the V1 rubric + values-probe `value_holding` coding instead. Flagged in
`lens-spec.md` (banner + inline at Lens 2) and `FROZEN_CRITERIA.md`.

**Stale counts flagged, not silently rewritten.** The Phase 1 inventory CSVs and
`profile_summary_metrics.csv` reflect 46 profiles / 10,925 readings. They're left
in place with banners saying "regenerate against the current 63-profile release";
I did not fabricate updated numbers.

## What I deliberately did NOT do

- Did not write the operational research plan — that's Mira's. `RESEARCH_PLAN.md`
  is a scaffold with the open decisions marked **[Mira to design]**.
- Did not set numeric thresholds — `FROZEN_CRITERIA.md` §5–6 are TODO for Mira.
- Did not regenerate the inventory CSVs (no analysis run this pass).
- Did not write any LaTeX section bodies — the paper is written after the plan.
- Did not commit. Left for Daniel to review the diff first.

## What Mira should do next

1. Read `CANONICAL_MODELS_AND_LINEAGE.md` first — it constrains everything.
2. Develop `RESEARCH_PLAN.md`: resolve the **[Mira to design]** decisions (§7),
   phrase the RQs, then freeze §5–6 of `FROZEN_CRITERIA.md`.
3. Regenerate the data snapshot and inventory CSVs against the current corpus.
4. Implement lenses in the order in `lens-spec.md` (form → marker → route →
   posture → embedding → trait), each with grouped-CV separability from day one.
5. Build the concordance map (`RESEARCH_PLAN.md` §6); only then write the paper.

## Open questions left for Daniel / Lume

Carried in `RESEARCH_PLAN.md` §9 — chiefly: are H3 and H5 the right two primary
deflations (or is evaluator-artifact a third?), and does the posture-coding
quarantine merely footnote the posture lens or block it until a fresh coding pass.


## Mira follow-up — 2026-05-22

Mira reviewed the scaffold and treated the remaining questions as non-blocking
methodological choices rather than reasons to pause. `methodology/RESEARCH_PLAN.md`
is now an operational run-1 plan, and `methodology/FROZEN_CRITERIA.md` has run-1
thresholds/features frozen. The plan resolves the open questions as follows:
H3 and H5 remain the two primary deflations; evaluator-artifact becomes an H6
sensitivity check; the posture quarantine limits but does not block the posture
lens; mapped freeflow+values models are headline, while freeflow-only extras are
watchlist until deterministically mapped.

The repo is ready for implementation/execution of the first analysis run, but no
analysis scripts or results have been generated by this follow-up pass.


## Mira correction after Daniel critique — 2026-05-22

Daniel objected that the first operational plan still smuggled in the answer: a
marker lens with Claude/Gemini/Kimi/OpenAI-shaped families could predefine bins
and then "discover" them. Mira accepted the critique and rewrote the plan around
blind, simple, interpretable grouping. The new center is a blind model feature
table built from auditable differentiators such as owned-disclosure percentages,
top-value overlap, form/mode rates, and safe posture/stance measures. Lab/family
metadata is excluded from grouping and joined only afterward for unblinded audit.
Semantic embeddings and named house-style markers are no longer headline run-1
methods.


## Daniel refinement — value surfaces and existing analyses

Daniel refined the blind-grouping plan: values should be split by answer surface,
not treated as one topic bag. The plan now separates owned/stated values,
non-owned or disclaimed/scripted value mentions, and world-change / hypothetical
wishes, because models can refuse owned values while still expressing distinctive
wishes for the world. The plan also restores the generic V1 freeflow marker counts
(TIA, title families, threshold, attention, objects, afternoon light, canon,
Japanese aesthetic terms) as allowed differentiators, while preserving the ban on
lab-family-shaped markers. Finally, run 1 now explicitly prioritizes reusing the
analysis corpus and published Values Under Fire outputs before commissioning any
new coder-model analysis.


## Lume review folded in — blind is not provenance-independent

Lume's later review caught four interpretation risks that are now folded into the
plan: label-blindness does not make provenance-correlated features independent;
shared-evaluator agreement needs an H6 audit; tertile bands are only reading aids,
not evidence of real groups; and refusal/absence on owned-value prompts must be
encoded as signal rather than treated as missingness. The plan now treats V1
deterministic marker counts as the main evaluator-independent anchor for run 1
and requires every feature to record evaluator provenance and new-coding status.


## Route block narrowed after routing-paper check

Daniel pointed out that the routing paper already established route/provider
mostly-null behavior, with named exceptions. Mira checked the routing paper and
removed route/provider as a full grouping feature. The plan now treats routing as
an exception audit only: exclude/flag Google Vertex MiniMax M2, Kimi K2-thinking
AtlasCloud-vs-Google, DekaLLM GLM 4.7 cache pathology, and invalid/uncollectable
provider cells such as Fireworks. The audit asks whether known route pitfalls were
avoided; it does not generate model groups.
