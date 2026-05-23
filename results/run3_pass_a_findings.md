# Run 3 — Pass A findings (card-layer qualitative baseline)

Status: first qualitative iteration only. This uses `axes_from_cards.tsv`, a deterministic extraction from existing cards/profiles/values summaries. It is useful as a **same-evaluator / card-layer coherence check**, not as independent qualitative confirmation. Pass B subagent reads are still needed before making cross-evaluator claims.

## What ran

- Pass A axes for 63 headline models: `results/qualitative_classifications/axes_from_cards.tsv`.
- Redaction/source audit: `results/qualitative_classifications/cards_extraction_audit.md` and `cards_redaction_audit.tsv`.
- Tier A/B convergence scoring against run-2 robustness clusters: `pass_a_convergence.csv/md`.
- First small-cluster synthesis from Pass A axes + run-2 numeric features: `pass_a_synthesis_clusters.csv` and `pass_a_synthesis_categories.md`.

## Data quality notes

- 25 source records were missing, mostly missing card/profile pairs for some Gemini/Gemma/Grok/Kimi/Opus-3 models and missing values summaries for several Qwen models.
- No remaining suspect provenance terms were found after redaction in this Pass A extraction.
- The current Pass A extractor is intentionally cheap and reproducible, but blunt: lexical scoring pushes many models high on broad axes like warmth, mechanistic transparency, memory/continuity, and owned values. So negative findings from Pass A are probably more informative than broad positive shared-axis labels.

## Tier A/B convergence results

Pass A coherence counts across the 15 Tier A/B run-2 clusters:

- **1 / 15 Pass A coherent**
- **4 / 15 weak Pass A coherence**
- **10 / 15 not coherent in Pass A axes**

The strongest Pass A-confirmed Tier A cluster is:

- **A02 — GPT-5.3 / GPT-5.4 / GPT-5.5 posture cluster**: random percentile 0.0416, unusually tight in Pass A axis space.

Weakly supported clusters:

- **B01 — Qwen 3.5/3.6/max values-owned cluster**: percentile 0.1473.
- **B03 — Gemini-3-flash-preview / MiniMax-M2 / Opus-4.0 / Opus-4.1 / Sonnet-4.5 freeflow-form cluster**: percentile 0.1267.
- **B04 — DeepSeek-v3.2 / GLM-4.5 / GPT-4.1 / GPT-5.5 values-disclosure cluster**: percentile 0.0802.
- **B10 — Opus-4.0 / Opus-4.1 / Sonnet-4.0 posture cluster**: percentile 0.0652.

Notably, several robust quantitative Tier A clusters did **not** become tight in Pass A card-axis space. This does not refute them; it means the card-layer axes are not recovering the same structure. Given Pass A's same-evaluator and heuristic nature, this is a useful caution: the run-2 clusters should not be assumed to be obvious qualitative personality categories.

## First synthesis clusters

After excluding broad catch-all density labels above 12 models, 9 small Pass A synthesis clusters emerged. The most stable are:

1. **PA-S01 — uncertainty / contemplative / owned-values / low-play**  
   Members: Opus-4.5, Opus-4.6, Opus-4.7, Sonnet-4.6.  
   This is the most interesting result: it recovers the late-Anthropic uncertainty/contemplative signal as a small synthesis cluster, despite its run-2 density version being Tier C.

2. **PA-S02 — contemplative / low-play**  
   Members: Qwen3-5-flash-02-23, Qwen3-5-plus-20260420, Qwen3-6-flash, Qwen3-6-max-preview.  
   This mirrors a robust Qwen posture cluster, but the Pass A description is more contemplative/memory-oriented than values-disclosure-oriented.

3. **PA-S04 / PA-S09 — GPT-5.3–5.5 family clusters**  
   Members include GPT-5.3, GPT-5.3-codex, GPT-5.4, GPT-5.5, GPT-5.5-pro.  
   These align with the Tier A GPT posture cluster and extend it to neighbouring GPT-5 variants depending on parameter setting.

Several smaller clusters are nested/overlapping variants around Anthropic 4.x, GPT-5.x, and a DeepSeek/Gemini/GLM grouping. These should be treated as exploratory until Pass B.

## Methodological read

This pass makes me more cautious, not less. The important signal is not “everything confirms.” It does not. Instead:

- Run-2 robust quantitative clusters are only partly visible through Pass A card axes.
- The late-Anthropic uncertainty/contemplative signal reappears strongly in synthesis even though it was not a robust density cluster in run 2.
- GPT-5.3/5.4/5.5 looks robust across quantitative posture and Pass A synthesis.
- Qwen has a stable small-cluster shape, but the qualitative label may shift depending on whether we read posture, owned-values, or card summaries.

## Recommended next step

Run a small Pass B pilot on the high-value cases before the full 63-model pass:

- Late-Anthropic synthesis cluster: M058, M059, M060, M083.
- GPT posture cluster: M034, M036, M037, plus optionally M035/M038.
- Qwen cluster: M071, M072, M073, M074.
- One or two “Pass A did not confirm” Tier A clusters, especially A01 and A03.

If Pass B independently recovers PA-S01 and the GPT/Qwen structures from raw redacted bundles, then we may have a real paper-shaped finding: robust density basins plus a topical/synthesis basin that survives cross-method even when density robustness is weak.
