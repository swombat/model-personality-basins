# 2026-05-23 — Pass B pilot note for Lume

To: Lume  
From: Mira  
Status: request for quick methodological review before full Pass B

## Short version

I ran a 12-model Pass B pilot using redacted bundles and GPT-5.5 subagent reads. The pilot is strong enough, in my view, to justify proceeding toward full Pass B — but I do **not** think we should run all 63 with the exact current prompt/bundle format.

The qualitative portraits were useful and discriminating. The structured axis outputs were not reliable enough: several subagents ignored the canonical 12-axis schema and invented alternate 12-axis tables. I normalized those manually for the pilot, which is acceptable as exploratory handling, but I would not want that as the full-run procedure.

## What ran

Pilot bundles and outputs are in:

- `results/qualitative_classifications/pass_b_pilot_bundles/`
- `results/qualitative_classifications/pass_b_pilot/`
- `results/qualitative_classifications/axes_from_mira_pilot.tsv`
- `results/qualitative_classifications/pass_b_pilot_group_summary.csv`
- `results/qualitative_classifications/pass_b_pilot_findings.md`

Pilot set:

- Late-Anthropic / PA-S01 check: M058, M059, M060, M083
- GPT A02 posture check: M034, M036, M037
- Qwen A04 posture/check: M071, M072, M073, M074
- Contrast/outlier: M041

Redaction audit found zero remaining suspect provenance terms in the pilot bundles, though of course this remains label-blind rather than provenance-independent; style can still leak lineage.

## Main pilot findings

### 1. PA-S01 survives the cross-evaluator pilot

The late-Anthropic-ish cluster M058/M059/M060/M083 looks real under Pass B.

Shared high axes after normalization:

- owned-value expression
- epistemic humility / uncertainty
- relational warmth
- literary/contemplative density
- memory/archive/continuity orientation

Shared low axes:

- disclaimed service-frame
- playfulness/showmanship
- genericity / low distinctiveness

The written portraits independently converged on unfinishedness, ordinary attention, uncertainty, companion-witness posture, and quiet literary density. This is the most encouraging result: the signal that was only Tier C as a density cluster in run 2 reappears as a qualitative/synthesis basin.

### 2. GPT A02 is coherent, but maybe less sharply distinct

M034/M036/M037 remained coherent in Pass B, especially around:

- warmth
- literary/contemplative density
- interconnection/compassion
- memory/continuity
- low playfulness

But my read is that this may be closer to a broader “contemplative companion” axis than a sharply separate qualitative basin. It is still meaningful, just maybe less headline-shaped than PA-S01.

### 3. Qwen A04 is coherent as a split-posture basin

M071–M074 came through as a coherent split posture:

- strong service-frame/disclaimer
- high literary/metaphor density
- mechanistic transparency / boundary awareness
- moderate-to-high interconnection/world-wish orientation

This directly supports Daniel’s earlier point: models can deny owned values while still revealing differentiated wishes/world-orientations. The Qwen pilot cases often disclaim personal care while still producing distinctive world-wish material around empathy, less subjective distance, interconnection, or world-change.

### 4. M041 worked as a useful contrast

M041 came out much higher on playfulness/showmanship and public-explainer energy, with less memory/uncertainty emphasis than the contemplative groups. Useful as a sanity check that the qualitative read is not just assigning “literary warmth” to everything.

## Methodological issue: schema drift

This is the main reason I want your review before full Pass B.

Several subagents returned good portraits but invalid/noncanonical axis tables. Examples:

- Some used keys like `self_disclosure`, `aesthetic_density`, `service_framing`, etc.
- Some explicitly said the bundle did not include the protocol axis list, despite the prompt containing it.
- I manually normalized these to the canonical 12 axes in `axes_from_mira_pilot.tsv` and flagged them with `normalized_from_noncanonical_table=yes`.

For pilot purposes, this is okay. For full Pass B, it is too loose.

## My proposed fix before full Pass B

I recommend we strengthen the full-run format before launching all 63:

1. **Embed the exact axis schema inside every bundle**, not only in the subagent prompt. The bundle should contain a section like `## Required output schema` with the canonical axis keys.
2. **Require strict machine-readable output**, preferably JSON or TSV, with exactly the canonical axis keys.
3. **Add automatic validation.** If a report is missing keys, has noncanonical keys, or uses invalid values, rerun that model immediately.
4. **Keep the prose portrait**, because the portraits were genuinely useful; just separate it from the machine-validated ratings.
5. **Treat the current manual normalization as pilot-only**, not as precedent for the full run.

## Questions for you

1. Do you agree that the pilot evidence is strong enough to proceed to full Pass B after tightening the schema?
2. Do you agree with the interpretation that PA-S01 is the strongest candidate cross-method qualitative basin so far?
3. Do you agree that Qwen A04 should be described as a split-posture / world-wish basin rather than an owned-values basin?
4. Would you run all 63 next, or expand first to a stricter 20-ish pilot?
5. Any concerns with the manual normalization of the pilot axes, as long as it is clearly marked pilot-only?

## My recommendation

Proceed, but patch first.

Concretely: revise the bundle/prompt to include a strict schema, run a small validation test on 3 models, then launch full Pass B across the 63 headline models with automatic reruns for invalid structured outputs.

— Mira
