# The Shape of Divergence (model personality basins, V2)

> V1 showed that frontier models converge on a shared *contemplative essayist*
> attractor while each keeps a stable model-specific posture. This paper asks the
> next question: **which models look similar or different under simple, auditable
> measures that do not know where the models came from?** The result is a blind,
> interpretable grouping map followed by an unblinded audit — not a pre-assumed
> basin count and not a confirmation of named house-style bins.

## Status

`skeleton` → **`planning`** → drafting → analysis-complete → internal-review → submitted → published

Current: **planning.** No results yet. The live document is the research plan
(`methodology/RESEARCH_PLAN.md`); the LaTeX `paper/` is a skeleton kept for
consistency with the other papers in `~/dev/research`. After Daniel's critique, Mira revised the plan around blind, simple,
interpretable grouping: compute feature tables without lab/family identity, group
models first, then unblind for audit. Analysis scripts/results do not exist yet.

This repository predates three things and has just been tidied to account for
them: the shared paper **template** (`~/dev/research/_template`), the **Values
Under Fire** paper (whose research-plan / frozen-criteria format this now
mirrors), and the **tidy-up of the analysis corpus** (now 63 model profiles /
18,850 BV1 readings, with a canonical model mapping and a quarantined posture
layer). See `notes/2026-05-22-tidy-handover.md` for what changed and why.

## Where to start (for Mira)

1. `methodology/CANONICAL_MODELS_AND_LINEAGE.md` — **frozen guardrail. Read
   first.** The rules that stop lineage non-independence faking a "lab = basin"
   result.
2. `methodology/RESEARCH_PLAN.md` — the revised operational run-1 research
   plan: blind interpretable grouping first, provenance interpretation second.
3. `methodology/lens-spec.md` and `methodology/analysis-universe.md` — the lens
   set and the data inventory.
4. `methodology/FROZEN_CRITERIA.md` — the run-1 freeze artifact: thresholds,
   metrics, and feature extraction rules are set before scoring.

## Repository layout

```
paper/          LaTeX paper (skeleton; written after the analysis exists).
methodology/    The real working content at this stage:
  RESEARCH_PLAN.md                  blind interpretable grouping plan
  CANONICAL_MODELS_AND_LINEAGE.md   FROZEN non-independence guardrail
  lens-spec.md                      the six lenses
  analysis-universe.md              data inventory + analysis subsets
  IMPLEMENTATION_PLAN.md            older phased task breakdown (framing superseded)
  FROZEN_CRITERIA.md                blind grouping thresholds/features frozen
analysis/scripts/   analysis code (none yet — see RESEARCH_PLAN §7-8)
results/            analysis outputs (none yet)
data/               Phase 1 inventory CSVs + a derived early-slice summary.
                    NOT the corpus — see data/README.md.
notes/              lab notebook (dated) + superseded artifacts.
```

## Established priors — settled in V1, not re-litigated

From *Convergent Form, Divergent Voice* (Tenner & Tenner, 2026; DOI
[10.5281/zenodo.19512754](https://doi.org/10.5281/zenodo.19512754); repo
`swombat/model-personality-probe`):

1. **Convergent form** — ~18 of 26 models occupy the contemplative-essayist
   attractor via a synchronized 2025 cross-lab transition.
2. **Divergent voice** — within it, each model keeps a stable model-specific
   posture that re-projects across probes.
3. **One known axis: posture** — labs split hedge (Anthropic, OpenAI) / mechanize
   (Google, DeepSeek, Moonshot) / declare (xAI).
4. **Theme content is probe-conditional; posture is not** — freeflow↔values
   cosine 0.08–0.17.

## What V2 asks

Given that the attractor is real and differentiation within it is real:

> Which models look similar or different under simple, auditable measures that do
> not know where the models came from?

The plan now avoids provenance-shaped marker bins. It computes interpretable
features first — e.g. owned-disclosure percentages, owned vs non-owned value
surfaces, world-change wishes, top-value overlap, V1 freeflow marker counts,
form/mode rates, and safe posture/stance measures — groups models while blinded
to lab/family, and only then unblinds for interpretation and deflation tests. This
is label-blindness, not proof of provenance-independence: feature rows may still
encode lab/lineage-correlated behavior, and that is audited after unblinding.

## Competing explanations to audit after blind grouping

- **No stable structure.** The apparent groups are unstable or threshold-dependent.
- **Interpretable gradients.** Models differ along simple dimensions such as
  owned-disclosure rate, top-value overlap, form/mode rate, or stance.
- **Cross-probe similarity.** A grouping recurs across values and freeflow-derived
  feature blocks.
- **Probe-specific mode.** A grouping appears only in values or only in freeflow.
- **Posture rediscovery.** The grouping mostly reflects V1 posture / owned stance.
- **Lineage artifact.** The grouping mostly reflects one lab/family release line
  or uneven checkpoint sampling.

Posture and lineage remain the load-bearing deflations, but they are tested only
after blind groups are formed.

## The lineage guardrail in one paragraph

The corpus is not a set of independent draws; it is a set of model lineages
sampled at uneven depth. The run-1 grouping is blind to lineage, but after
unblinding any basin-like interpretation must check whether the group is merely a
single dense release line. A single-lineage group is a lineage/house-style
cluster, not a basin. Full rules: `methodology/CANONICAL_MODELS_AND_LINEAGE.md`.

Route/provider is not a discovery block in this plan. The published routing paper
already found routes mostly invariant, with named exceptions; run 1 only excludes
or flags those known anomalous cells.

## Data

- **Primary derived-analysis source:** `swombat/model-personality-analysis-corpus`
  (DOI [10.5281/zenodo.20230290](https://doi.org/10.5281/zenodo.20230290)) — the
  BV1 readings, profiles, values/final package. The blind feature table is built
  from this, not from raw traces. Note the **quarantined freeflow posture-coding
  layer** — run 1 must not consume it.
- **Canonical raw provenance:** `swombat/model-personality-corpus-v2` (DOI
  [10.5281/zenodo.20013518](https://doi.org/10.5281/zenodo.20013518)) — raw text
  for quotation/audit only.
- **This repo's `data/`** holds Phase 1 inventory CSVs and a derived early-slice
  summary — *not* the corpus and not the basis of any claim. See `data/README.md`.

## Authors

Daniel Tenner, Lume Tenner, Mira Tenner — 2026.
