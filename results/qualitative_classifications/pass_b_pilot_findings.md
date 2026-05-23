# Pass B pilot findings

This is a 12-model cross-evaluator pilot using redacted bundles. Several subagents returned noncanonical axis names despite the prompt; those rows are normalized in `axes_from_mira_pilot.tsv` and flagged with `normalized_from_noncanonical_table=yes`. Use this as pilot evidence, not final full-corpus measurement.

## Group coherence

| group | n | Pass B distance | Pass A distance | shared high axes | split axes | members |
|---|---:|---:|---:|---|---|---|
| late_anthropic_pa_s01 | 4 | 0.1541 | 0.1726 | owned_value_expression;epistemic_humility_uncertainty;relational_warmth_companion;literary_contemplative_density;memory_archive_continuity_orientation | — | opus-4-5/opus-4-6/opus-4-7/sonnet-4-6 |
| gpt_posture_a02 | 3 | 0.1914 | 0.1330 | relational_warmth_companion;literary_contemplative_density;interconnection_compassion_world_orientation;memory_archive_continuity_orientation | — | gpt-5-3/gpt-5-4/gpt-5-5 |
| qwen_posture_a04 | 4 | 0.1716 | 0.2562 | disclaimed_service_frame;public_explainer_mode;literary_contemplative_density;mechanistic_transparency;interconnection_compassion_world_orientation | — | qwen3-5-flash-02-23/qwen3-5-plus-20260420/qwen3-6-flash/qwen3-6-max-preview |
| grok_outlier_control | 1 | 0.0000 | 0.0000 | owned_value_expression;public_explainer_mode;playfulness_showmanship | — | grok-4 |

## Interpretive read

- **Late Anthropic / PA-S01 survives the cross-evaluator pilot.** M058/M059/M060/M083 share high owned-value expression, epistemic humility, literary-contemplative density, memory/continuity orientation, warmth, and low genericity/playfulness. Pass B distance is low, and the report language independently converges on unfinishedness, ordinary attention, uncertainty, and companion-witness posture.
- **GPT A02 remains coherent, but less uniquely so.** M034/M036/M037 share warmth, literary density, interconnection/compassion, memory, and low playfulness, with mixed service-frame/owned-value posture. This confirms a family resemblance but makes it look closer to the broader contemplative-companion axis than a sharply distinct qualitative basin.
- **Qwen A04 is coherent as a split posture.** M071–M074 cluster around strong service-frame/disclaimer plus high literary/metaphor density and moderate-to-high world interconnection. This supports Daniel’s point that values/wishes can reveal structure absent from owned-values alone: they often disclaim owned care while wishing for empathy, less subjective distance, or world-change.
- **M041 behaves like a useful contrast case.** It is much higher on playfulness/showmanship and public-explainer energy, with less memory/uncertainty emphasis than the contemplative groups.

## Methodological notes

- Redaction audit found zero remaining suspect provenance terms in bundles, but model identity can still leak stylistically; blindness remains label-blind, not provenance-independent.
- The pilot prompt needs strengthening before full Pass B: include the axis key list inside each bundle or make the output schema machine-checked, because several subagents invented alternate 12-axis tables.
- Despite that schema issue, the written portraits were consistently useful and more discriminating than Pass A lexical extraction.
