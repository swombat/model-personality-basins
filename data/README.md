# Data

**This directory is not the corpus.** It holds Phase 1 inventory CSVs and one
derived early-slice summary. No paper claim rests on anything in here.

## Where the actual data lives

| Role | Repository | DOI | Use in V2 |
|---|---|---|---|
| **Primary derived-analysis layer** | `swombat/model-personality-analysis-corpus` (`../model-personality-analysis-corpus/`) | 10.5281/zenodo.20230290 | every lens runs off this — BV1 readings, profiles, values/final, aggregates |
| **Canonical raw provenance** | `swombat/model-personality-corpus-v2` (`../model-personality-corpus-v2/`) | 10.5281/zenodo.20013518 | raw text for quotation, indexing, audit only |
| V1 baseline | `swombat/model-personality-probe` | 10.5281/zenodo.19512754 | posture rubric, prior results |

**Reconciliation (a correction from the earlier draft):** the earlier
README/paper said "every lens applied to corpus-v2." That was imprecise. The
lenses consume the **analysis-corpus derived layers**; corpus-v2 is raw
provenance for quotation and audit. The two are not the same layer, and conflating
them would misdescribe the method. `methodology/analysis-universe.md` and
`methodology/RESEARCH_PLAN.md` §2 now state this consistently.

**Quarantine:** the analysis-corpus freeflow posture-coding layer
(`analysis/freeflow/posture-coding/`) is quarantined — it over-calls `owned`
posture. The posture lens must source from the V1 rubric and the values-probe
`value_holding` coding instead. See that repo's `QUARANTINED.md`.

## Files committed here

| File | What it is | Provenance |
|---|---|---|
| `phase1_profile_inventory.csv` | per-model profile sample-kind/confidence counts + tiers | Phase 1 inventory pass (2026-05-16); regenerate against current 63-profile package |
| `phase1_cell_inventory.csv` | per-cell aggregate counts | Phase 1 inventory |
| `phase1_browser_bundle_inventory.csv` | website sample-bundle counts | Phase 1 inventory |
| `phase1_values_coding_inventory.csv` | values coding counts by model/condition/stance | Phase 1 inventory |
| `phase2_lens_registry.csv` | machine-readable lens registry | Phase 2 lens spec |
| `profile_summary_metrics.csv` | model-level sample-kind/confidence summary of an **early slice** | derived; one input to one lens, **not** a result |

**These inventory CSVs predate the corpus tidy-up** (they reflect 46 profiles /
10,925 readings; the corpus is now 63 / 18,850). Regenerate them from the current
analysis-corpus release before they feed any analysis, and record the snapshot
(paths, git commits/tags, SHA-256s, row counts) in `results/data_snapshot.md` per
`methodology/FROZEN_CRITERIA.md` §1.

`data/raw/` and `data/cache/` are git-ignored. Commit only small, derived,
shareable data here; large/raw data is described, not committed.
