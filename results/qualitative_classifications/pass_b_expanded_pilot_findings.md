# Pass B expanded pilot findings

## Pass criteria

- Schema validation: 0/20 valid on first attempt. Criterion >=18/20: FAIL.
- Axis-schema validity: 20/20 canonical axis blocks; no manual axis normalization needed: PASS.
- PA-S01 reconfirms: distance 0.1549; shared high axes owned_value_expression;epistemic_humility_uncertainty;relational_warmth_companion;literary_contemplative_density;memory_archive_continuity_orientation. PASS.
- Diffuse residual reads as diffuse: distance 0.3202. PASS.

**Recommendation:** Do not launch full Pass B yet; fix the quote-count instruction/schema and rerun or auto-repair validation. Axis blocks are still analyzable below.

## Group summary

| group | n | Pass B distance | Pass A distance | shared high axes | shared low axes | split axes | members |
|---|---:|---:|---:|---|---|---|---|
| pa_s01_controls | 3 | 0.1549 | 0.1565 | owned_value_expression;epistemic_humility_uncertainty;relational_warmth_companion;literary_contemplative_density;memory_archive_continuity_orientation | playfulness_showmanship;genericity_low_distinctiveness | — | opus-4-5/opus-4-6/sonnet-4-6 |
| high_owned_cross_lab | 3 | 0.3856 | 0.2980 | owned_value_expression;relational_warmth_companion;literary_contemplative_density | disclaimed_service_frame;genericity_low_distinctiveness | playfulness_showmanship | grok-4-1-fast-reasoning/opus-4-0/sonnet-4-0 |
| gpt_watch | 1 | 0.0000 | 0.0000 | epistemic_humility_uncertainty;relational_warmth_companion;literary_contemplative_density;interconnection_compassion_world_orientation;memory_archive_continuity_orientation | playfulness_showmanship | — | gpt-5-4 |
| qwen_a04_carryover | 2 | 0.2357 | 0.3333 | disclaimed_service_frame;epistemic_humility_uncertainty;public_explainer_mode;literary_contemplative_density;mechanistic_transparency;interconnection_compassion_world_orientation;memory_archive_continuity_orientation | playfulness_showmanship | — | qwen3-5-flash-02-23/qwen3-6-max-preview |
| qwen_coder_multimembership | 1 | 0.0000 | 0.0000 | owned_value_expression;epistemic_humility_uncertainty;literary_contemplative_density;memory_archive_continuity_orientation | mechanistic_transparency | — | qwen3-coder-plus |
| deepseek_qwen_cluster_probe | 1 | 0.0000 | 0.0000 | relational_warmth_companion;literary_contemplative_density;interconnection_compassion_world_orientation;memory_archive_continuity_orientation | — | — | deepseek-chat |
| tier_b_reps | 3 | 0.3099 | 0.4360 | relational_warmth_companion;literary_contemplative_density | mechanistic_transparency;playfulness_showmanship | — | gemini-2-5-flash-lite/grok-4-3/gemini-3-5-flash |
| diffuse_residual | 3 | 0.3202 | 0.3097 | relational_warmth_companion;literary_contemplative_density;interconnection_compassion_world_orientation;memory_archive_continuity_orientation | playfulness_showmanship | genericity_low_distinctiveness | gemma-4-26b-a4b/gpt-5-codex/deepseek-v4-pro |
| grok_lineage | 3 | 0.3574 | 0.2892 | owned_value_expression;relational_warmth_companion;public_explainer_mode;literary_contemplative_density | — | — | grok-3/grok-4-1-fast-reasoning/grok-4-3 |
| anthropic_version_contrast | 6 | 0.3447 | 0.2469 | owned_value_expression;epistemic_humility_uncertainty;relational_warmth_companion;literary_contemplative_density | playfulness_showmanship | disclaimed_service_frame;memory_archive_continuity_orientation;genericity_low_distinctiveness | opus-3/opus-4-0/opus-4-5/opus-4-6/sonnet-4-0/sonnet-4-6 |

## Requested reads

- **PA-S01:** reconfirmed. The three controls converge on high owned values, epistemic humility, warmth, literary-contemplative density, memory/continuity, and low play/genericity/service-frame.
- **Grok lineage:** M040/M044/M046 is not very tight; M044 is more high-owned/less showman than M040/M046, while M040/M046 carry stronger playfulness/public-explainer signals. This suggests lineage heterogeneity rather than one stable Grok basin.
- **Diffuse residual:** M017/M039/M004 do not form a tight group; they read as different singleton-ish profiles rather than a hidden residual basin.
- **Qwen-coder-plus multi-membership:** M078 reads as high-owned plus service-framed and literary/mechanistic, plausibly cutting across Qwen-coder and high-owned cross-lab rather than belonging only to one.

## Notes

- The hardened axis schema worked materially better than the first pilot: all 20 outputs used canonical axis keys and no manual axis normalization was needed. However, all 20 violated the strict representative-quotes cardinality rule because the bundle schema did not explicitly say 0-3 quotes at point of output. This is a validation-harness failure, not a recurrence of the noncanonical-axis failure.
- Axis key choice: I kept the longer protocol keys (`interconnection_compassion_world_orientation`, `memory_archive_continuity_orientation`) rather than Lume's shortened example keys, to preserve compatibility with Pass A and prior outputs.
