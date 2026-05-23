# Run 1 interpretive report — blind interpretable basins analysis

Generated: 2026-05-23.

## What ran

Run 1 used **existing analysis only**: no new LLM/coder evaluations were commissioned. The full blind feature table contains 83 canonical model rows after alias normalization (`claude-opus-*` → `opus-*`, `claude-sonnet-*` → `sonnet-*`). The headline grouping subset contains 63 models with enough freeflow-derived coverage for cross-block comparison.

Route/provider was **not** used as a grouping feature. It is only an exception audit, following the routing-paper prior.

## Important implementation note

During execution I found a mechanical bug in the first script version: feature columns were being duplicated when written to CSV, which made the 70% coverage rule appear satisfied artificially. I fixed this by de-duplicating feature names and by making the combined grouping use the high-confidence 63-model subset rather than the full 83-row inventory. After the fix, combined grouping uses 93 numeric features, and block-level distance matrices are emitted separately.

## Main readout

The run does **not** yet support a clean claim like "there are N personality basins." It supports a more cautious first result:

1. **There are strong interpretable gradients**: owned-value disclosure, owned-value refusal/recitation, world-wish entropy, V1 marker density, expressive/freeflow rate, and strong-disclaimer rate all separate models in reader-checkable ways.
2. **The combined k=4 grouping is descriptive, not taxonomic.** It finds:
   - a small Gemma/generic-disclaimer outlier group (`gemma-4-26b-a4b`, `gemma-4-31b`);
   - a high-owned/high-expressive Anthropic–Grok-adjacent group containing Opus/Sonnet, Grok 4.1/4.2, `kimi-k2-0905`, and `qwen3-coder-plus`;
   - one large mixed central mass;
   - a singleton `gpt-5-1-codex` outlier.
3. **The strongest apparent structure is posture/value-disclosure structure, not independent basin structure.** The posture distance matrix correlates strongly with values-disclosure distance (Spearman rho 0.711) and moderately with owned-values distance (0.536). That is exactly where H6/shared-evaluator and H3/posture-rediscovery cautions matter.
4. **The deterministic V1 marker anchor only weakly agrees with the values/posture blocks.** V1 marker distance correlations are low: posture 0.229, values-owned 0.210, values-disclosure 0.154, values-wishes 0.135, freeflow-form -0.171. This is evidence against treating the combined grouping as a robust cross-instrument basin map yet.
5. **World-wish content has its own signal.** The world-wishes block surfaces the Daniel-noted pattern: high wish entropy among Kimi, Gemma/Gemini/GLM, Grok 4.2, and some Qwen/OpenAI models. But its agreement with deterministic V1 markers is weak (rho 0.135), so it is better framed as a values-surface gradient or probe-conditional grouping until checked more directly.

## Route exception handling

The routing-paper prior was applied as an audit/exclusion layer, not a discovery lens.

Flagged/excluded cases:

- `minimax-m2`: Google Vertex MiniMax M2 large deployment outlier; 250 freeflow samples excluded.
- `glm-4-7`: DekaLLM prompt-keyed cache pathology; 125 freeflow samples excluded.
- `kimi-k2-thinking`: smaller AtlasCloud/Google provider-effect flag retained, not excluded.
- `minimax-m2-7`: Fireworks/uncollectable missingness flag.

So the analysis should not be discovering a route basin. If any later claim depends on these rows, inspect `results/route_exception_audit.md` first.

## Files to review first

- `results/results_summary.md` — concise rankings and combined k=4 group summary.
- `results/evaluator_independence_audit.md` — cross-block distance correlations and H6 risk notes.
- `results/route_exception_audit.md` — route/provider contamination check.
- `results/blind_model_feature_table.csv` — full feature table with unblinding metadata segregated.
- `results/blind_groupings/*.csv` — k=2..6 combined groups and per-block k=4 groups.
- `results/blind_similarity_matrices/*.csv` — combined and per-block distance matrices.

## Recommended next step

Do **not** write the paper as "basin count discovered" yet. Write Run 1 as:

> Blind interpretable measures recover several readable model gradients and a few descriptive clusters, but cross-instrument convergence is limited. The strongest combined structure is largely posture/value-disclosure aligned, while world-wish content and V1 freeflow markers provide partially independent, weaker, probe-conditional structure.

The most valuable next analysis would be a small targeted adjudication pass, not a 100+ per-model recode: inspect exemplars for the world-wish/interconnection family and the high-owned/high-expressive Anthropic–Grok-adjacent group to determine whether those are content basins, posture rediscoveries, or evaluator artifacts.
