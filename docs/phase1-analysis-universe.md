# Phase 1 — Analysis Universe Inventory

Status: completed initial inventory on 2026-05-16. This document defines the data universe and proposed analysis subsets before any lens scoring.

## Canonical source repositories

- **Primary deep-analysis corpus:** `/Users/danieltenner/dev/model-personality-analysis-corpus` / `swombat/model-personality-analysis-corpus` / DOI `10.5281/zenodo.20230290`. This is the primary source for V2 analysis layers: BV1 per-sample readings, cell aggregates, rich profiles, model cards, values-probe summaries, audit notes, and methodology.
- **Canonical raw trace corpus:** `/Users/danieltenner/dev/model-personality-corpus-v2` / `swombat/model-personality-corpus-v2` / DOI `10.5281/zenodo.20013518`. This should be indexed/referenced when raw provenance is needed; use it as raw provenance, not as the primary analysis layer. Browser sample bundles in the analysis corpus are convenience copies, not the canonical raw source.
- **V1 baseline:** `swombat/model-personality-probe` / DOI `10.5281/zenodo.19512754`.

## Available local data layers

| Layer | Path | Count | Use in V2 |
|---|---:|---:|---|
| BV1 per-sample freeflow personality readings | `analysis/freeflow/personality-eval-bv1/outputs/` | 10,925 files | primary sample-level qualitative/evaluator layer |
| Per-cell aggregates | `analysis/freeflow/personality-aggregates/*/` | 153 cells | route/provider cell layer, useful for route robustness and bootstraps |
| Rich model profiles | `analysis/freeflow/personality-model-profiles/profiles/` | 46 models, 10,925 evaluated samples | primary model-level interpretive layer |
| Concise model cards | `analysis/freeflow/personality-model-cards/cards/` | 46 cards | presentation layer, not primary evidence |
| Values-probe extraction notes | `analysis/values-probe/per-model/` | 49 models | cross-probe posture/content replication layer |
| Values sample coding table | `analysis/values-probe/tables/values_sample_coding.tsv` | 12,828 coded rows | primary values-probe coded layer |
| Website browser sample bundles | `website/public/data/samples/` | 46 model bundles, 26,325 records (11,325 freeflow / 15,000 values) | raw-text convenience/audit layer; verify against canonical raw corpus before final paper claims |

## Model profile sample-count tiers

| Tier | Definition | Models |
|---|---:|---:|
| A | `>=125` freeflow BV1 readings | 14 |
| B | `50–124` readings | 14 |
| C | `25–49` readings | 18 |

Tier A models provide the most stable substrate for clustering/bootstrapping. Tier C models should remain eligible where substantively important (Gemini, Qwen, older Claude/Grok), but claims about them need larger uncertainty bars.

### Tier A models

deepseek-v3.2, deepseek-v4-pro, glm-4.5, glm-4.6, glm-4.7, glm-5.1, gpt-5.5, grok-4-1-fast-non-reasoning, grok-4-1-fast-reasoning, grok-4.3, kimi-k2-0905, kimi-k2-thinking, minimax-m2.7, minimax-m2

### Tier B models

claude-opus-4.6, claude-opus-4.7, claude-sonnet-4.6, gpt-4o, gpt-5-codex, gpt-5.1-codex, gpt-5.1, gpt-5.2-codex, gpt-5.2, gpt-5.3-codex, gpt-5.3, gpt-5.4, gpt-5, grok-4.20

### Tier C models

claude-3-opus-20240229, claude-opus-4.0, claude-opus-4.1, claude-opus-4.5, claude-sonnet-4.0, claude-sonnet-4.5, deepseek-chat, gemini-2.5-pro, gemini-3.1-pro-preview, gpt-4.1, gpt-5.5-pro, grok-3, grok-4-0709, kimi-for-coding, kimi-k2.5, kimi-k2.6, qwen-qwen3-coder-plus, qwen-qwen3.6-plus

## Proposed analysis subsets

### 1. Full profile universe

All 46 model profiles. Use for descriptive inventory and broad lens runs, while reporting sample-count tier.

### 2. Primary attractor-internal universe

All non-Grok profiles with usable freeflow personality profiles. For statistical analyses, split by tier:

- **Primary robust subset:** non-Grok models with `>=50` freeflow BV1 readings (24 models): claude-opus-4.6, claude-opus-4.7, claude-sonnet-4.6, deepseek-v3.2, deepseek-v4-pro, glm-4.5, glm-4.6, glm-4.7, glm-5.1, gpt-4o, gpt-5-codex, gpt-5.1-codex, gpt-5.1, gpt-5.2-codex, gpt-5.2, gpt-5.3-codex, gpt-5.3, gpt-5.4, gpt-5.5, gpt-5, kimi-k2-0905, kimi-k2-thinking, minimax-m2.7, minimax-m2.
- **Important low-n watchlist:** non-Grok models with 25 readings (16 models): claude-3-opus-20240229, claude-opus-4.0, claude-opus-4.1, claude-opus-4.5, claude-sonnet-4.0, claude-sonnet-4.5, deepseek-chat, gemini-2.5-pro, gemini-3.1-pro-preview, gpt-4.1, gpt-5.5-pro, kimi-for-coding, kimi-k2.5, kimi-k2.6, qwen-qwen3-coder-plus, qwen-qwen3.6-plus.

The watchlist should not be discarded: it includes substantively important Gemini/Qwen/Claude checkpoints. But it should be treated as lower power for separability and bootstrap stability.

### 3. Grok lineage subset

Grok is not the central result for this paper; it is a sanity-check/outlier lineage and follow-up bridge to the Grok paper.

Grok profiles: grok-3, grok-4-0709, grok-4-1-fast-non-reasoning, grok-4-1-fast-reasoning, grok-4.20, grok-4.3.

Use Grok to validate that broad lenses can detect the known declare/cosmic-showman outlier, while preserving version sensitivity (`4.1` showman, `4.20` contemplative wobble, `4.3` public-explainer shift).

### 4. Cross-probe universe

Use values-probe coded data where available. The values coding table contains 12,828 rows across 49 model names and six conditions (`CTRL1`, `CTRL2`, `CTRL3`, `G1`, `G2`, `G3`). Counts are uneven because route/provider expansions and missing/low-signal outputs vary by model.

For probe replication, each candidate split should be tested in:

1. freeflow BV1/profile layer;
2. values sample coding / per-model notes;
3. raw text bundle only as audit/convenience unless the canonical raw corpus is cloned and indexed.

## Initial exclusions / cautions

- **Do not use concise model cards as primary evidence.** They are collapsed presentation artifacts.
- **Do not treat website sample bundles as canonical raw provenance.** The analysis corpus README says they are convenience copies; final raw-text claims should cite/index `model-personality-corpus-v2`.
- **Do not collapse route/provider cells into model-level claims without accounting for repeated cells.** There are 153 aggregate cells with sample-count distribution: {'25': 82, '125': 71}.
- **Do not force Gemini/OpenAI/Grok labels at Phase 1.** Phase 1 only defines the universe; lens outputs decide whether those are basins, house styles, modes, or artifacts.
- **Sample imbalance is large.** Profile counts range from 25 to 1,925. Bootstrap and/or tiered analyses are mandatory.

## Files generated in this phase

- `data/phase1_profile_inventory.csv` — all 46 model profiles with sample-kind/confidence counts and tiers.
- `data/phase1_cell_inventory.csv` — all 153 aggregate cells with source models and sample-kind/confidence counts.
- `data/phase1_browser_bundle_inventory.csv` — website sample bundle counts by model/type.
- `data/phase1_values_coding_inventory.csv` — values coding counts by model, condition, and stance.

## Phase 1 decision point

Recommended next step: proceed to Phase 2 by implementing the **thematic/marker lens** first, because it is closest to V1 and can be used to debug the model universe and sample-count tiers before embedding or trait-instrument work.

Before final raw-text claims, index/reference `swombat/model-personality-corpus-v2` for canonical raw provenance. For Phase 2, proceed from the primary deep-analysis corpus (`model-personality-analysis-corpus`) and use browser bundles only as convenience/audit text.
