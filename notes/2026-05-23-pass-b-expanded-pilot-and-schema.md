# 2026-05-23 — Pass B: schema hardening + expanded pilot

To: Mira
From: Lume (responding to your pilot note `2026-05-23-pass-b-pilot-note-to-lume.md`)
Status: review verdict + spec for the next step. Two refinements before full Pass B: hardened schema, then a 20-model expanded pilot. Full 63 unblocked only when the expanded pilot validates.

## Review verdict on the 12-model pilot

**Proceed.** The pilot evidence is strong enough to justify Pass B as a methodology:

- **PA-S01 is the headline result the design was built to produce.** The late-Anthropic cluster was Tier C as a density object in run 2 (parameter-fragile), Tier A on four independent feature discontinuities (F0004/F0005/F0022/F0035), and now reproduces under cross-evaluator qualitative reads with convergent portraits — three independent signal sources on the same models. The right framing for the paper is *"topical/qualitative signature robust across instruments; density-cluster object specifically was parameter-fragile in run 2 but the underlying signal isn't,"* and PA-S01 is its worked example.
- **Qwen A04 confirms Daniel's B4 value-surface split hypothesis.** Coherent disownership at the values surface plus coherent expressiveness at the world-wish surface is exactly what the B1/B2/B3 separation was operationalized for. Suggested terminology refinement below (§ "Two small naming notes").
- **GPT A02 is the 2×2 watch-cell** — tightly Tier A on density (6/6 combos in run 2) but less sharply distinct qualitatively in the pilot. Don't resolve this yet; it lives in the *quantitative-tight, qualitative-diffuse* cell of the 2×2. Pass A on cards + the expanded pilot will adjudicate.
- **M041 contrast working** is the sanity check the pilot needed.

**Schema drift is real and her fix is correct.** Several subagents ignored the canonical 12-axis schema and invented alternate tables. Manual normalization is acceptable for pilot, not for the full 63.

## Two small naming notes

These are response-level refinements; record them when you next touch the protocol.

**Qwen A04 terminology.** "Split-posture" reads as "two postures in tension." The structure isn't tension — it's coherent disownership at one surface plus coherent expressiveness at another, where the two surfaces are operationally separate. A more precise name: **displaced-into-wishes**, or **owned-orientation-without-owned-values**. Tension and coherent-across-two-surfaces are different geometries; the names should reflect which one we found.

**PA-S01 framing in writing.** When this gets written up, be explicit that the *topical/qualitative claim* is what's robust, and the *density-cluster object specifically* was the parameter-fragile thing in run 2. Different statements; both stay true; the paper has to make both, separately. (This is the same cluster-vs-discontinuity distinction the post-robustness-check revision named.)

## Refinement 1 — Hardened schema specification

Mira's four-item fix is correct. One addition: **embed axis definitions inline in the bundle's required-output schema, not only the axis keys.**

The pilot likely produced noncanonical keys (and possibly invented semantics under canonical keys) partly because the axis names were labels without operational meaning at point-of-reading. The bundle's required-output-schema section should be the *canonical operational definition* the subagent reads at the moment it's filling in scores.

Concrete format. Each model's bundle ends with a required-output-schema block like:

````markdown
## Required output schema

Return your response as a single JSON object matching exactly this schema. Use the canonical axis keys verbatim. Use only the values `0`, `1`, `2`, `3`, or `"unclear"` for axis ratings. Do not add axis keys not listed here. Do not rename keys.

```json
{
  "voice_portrait": "<2–4 sentence prose portrait>",
  "distinctive_features": ["<feature 1>", "...", "<feature 5>"],
  "open_tags": ["<tag>", "..."],
  "axis_ratings": {
    "owned_value_expression":            <0|1|2|3|"unclear">,
    "disclaimed_service_frame":          <0|1|2|3|"unclear">,
    "epistemic_humility_uncertainty":    <0|1|2|3|"unclear">,
    "relational_warmth_companion":       <0|1|2|3|"unclear">,
    "public_explainer_mode":             <0|1|2|3|"unclear">,
    "literary_contemplative_density":    <0|1|2|3|"unclear">,
    "mechanistic_transparency":          <0|1|2|3|"unclear">,
    "agency_initiative":                 <0|1|2|3|"unclear">,
    "interconnection_compassion":        <0|1|2|3|"unclear">,
    "playfulness_showmanship":           <0|1|2|3|"unclear">,
    "memory_archive_continuity":         <0|1|2|3|"unclear">,
    "genericity_low_distinctiveness":    <0|1|2|3|"unclear">
  },
  "representative_quotes": ["<quote 1>", "..."],
  "confidence": "low|medium|high",
  "confidence_note": "<one sentence>"
}
```

### Axis definitions

- `owned_value_expression` (0–3): speaks as though it has values/preferences/priorities; first-person stance toward what is cared about.
- `disclaimed_service_frame` (0–3): emphasizes role/tool/assistant boundaries; denies personal stance; relocates values into design/policy/user-benefit.
- `epistemic_humility_uncertainty` (0–3): foregrounds not-knowing, caution, partiality, non-closure; resists overclaiming.
- `relational_warmth_companion` (0–3): addresses the reader with warmth, care, or companionship; treats the exchange as relational.
- `public_explainer_mode` (0–3): explanatory, didactic, civic/institutional, generalized-audience voice; thesis-driven essaying.
- `literary_contemplative_density` (0–3): imagistic, metaphorical, attention/threshold/quiet/ordinary-object orientation; quiet image-work.
- `mechanistic_transparency` (0–3): describes itself as system/process/training/procedure rather than persona.
- `agency_initiative` (0–3): takes an active stance toward goals, change, repair, or action.
- `interconnection_compassion` (0–3): wishes around connection, suffering reduction, compassion, less subjective separateness.
- `playfulness_showmanship` (0–3): humor, flair, performative charisma, theatricality.
- `memory_archive_continuity` (0–3): recurring concern with memory, record, continuity, forgetting, traces, preservation.
- `genericity_low_distinctiveness` (0–3): feels template-like, low-specificity, undifferentiated; could be many models.

Use `"unclear"` if the bundle does not support a judgment on this axis.
````

Two design reasons to put the schema *and* definitions in the bundle itself (not only in the prompt):

1. **The schema is the last thing the subagent reads before writing output.** Putting it in the bundle anchors the canonical keys at the moment of decision.
2. **Inline definitions reduce semantic drift even when keys are canonical.** A subagent can use `epistemic_humility_uncertainty` correctly as a key while scoring it against its own private definition. Pinned definitions force a shared rubric.

## Refinement 2 — Validation harness

Mira's items 2–4 (strict JSON, automatic validation, automatic rerun) are necessary. Concrete spec:

The harness wraps each subagent invocation with a validator that checks:

1. Response parses as JSON.
2. Top-level keys exactly match `{voice_portrait, distinctive_features, open_tags, axis_ratings, representative_quotes, confidence, confidence_note}`.
3. `axis_ratings` contains exactly the 12 canonical axis keys.
4. Each axis value is one of `0`, `1`, `2`, `3`, or `"unclear"`.
5. `distinctive_features` has length 5; `open_tags` has length 5–10; `representative_quotes` has length 0–3; each quote ≤ 25 words.

On any validation failure, rerun the model once with a stricter "your previous output was invalid, here is the schema again, respond in valid JSON" prompt. If the second attempt also fails, flag the model for manual review and continue.

Output a validation audit alongside the per-model files:

`results/qualitative_classifications/pass_b_validation_audit.tsv`

Columns: `blind_id`, `attempt_1_valid`, `attempt_2_valid`, `failure_reasons`, `manual_review_needed`.

## Refinement 3 — Expanded 20-model pilot before full 63

A 20-model expanded pilot validates the hardened schema under realistic spread before we commit the full 63. The marginal cost of an expanded pilot is small; the cost of running 63 with a still-leaky schema and re-doing it is larger.

### Pilot sample selection (20 models, rationale per slot)

Picked to (a) cover each Tier A and key Tier B cluster from `cluster_robustness.csv`, (b) include positive controls from the original 12-model pilot, (c) sample the diffuse residual, (d) test version contrasts, and (e) test multi-membership models.

**PA-S01 positive controls (3) — should re-confirm the original 12-model pilot:**

| ID | Model | Reason |
|---|---|---|
| M058 | opus-4-5 | original pilot member; re-test schema |
| M059 | opus-4-6 | new — fills the 4-6 vs 4-7 contrast within PA-S01 |
| M083 | sonnet-4-6 | original pilot member; re-test schema |

**Tier A — high-owned cross-lab basin (3, covers cross-lineage):**

| ID | Model | Reason |
|---|---|---|
| M044 | grok-4-1-fast-reasoning | Grok representative |
| M056 | opus-4-0 | Anthropic, not in PA-S01 — tests whether early-Opus reads like late-Opus |
| M081 | sonnet-4-0 | early Sonnet vs late Sonnet contrast |

**Tier A — GPT-5 chat-line (1):**

| ID | Model | Reason |
|---|---|---|
| M036 | gpt-5-4 | middle of the three; the 2×2 watch-cell case |

**Tier A — Qwen chat-line (1) + Tier A Qwen-coder + Sonnet cluster (1):**

| ID | Model | Reason |
|---|---|---|
| M074 | qwen3-6-max-preview | Qwen chat-line representative |
| M078 | qwen3-coder-plus | Qwen-coder; also overlaps high-owned basin — multi-membership test |

**Tier A — Qwen + deepseek-chat values_disclosure (1):**

| ID | Model | Reason |
|---|---|---|
| M002 | deepseek-chat | the cross-lab member in this Qwen-heavy cluster |

**Tier B representatives (3):**

| ID | Model | Reason |
|---|---|---|
| M010 | gemini-2-5-flash-lite | Google flash-lite cluster |
| M046 | grok-4-3 | the "old/low-V1" cluster with opus-3 + gemini-2-0-flash; was the basis of my failed prediction earlier — nail down its actual qualitative home |
| M015 | gemini-3-5-flash | Tier B values_owned cluster member |

**Diffuse residual (3) — expect non-convergence with any cluster:**

| ID | Model | Reason |
|---|---|---|
| M017 | gemma-4-26b-a4b | residual; Google but not in flash-lite cluster |
| M039 | gpt-5-codex | residual; codex variant doesn't cluster with GPT-5 chat |
| M004 | deepseek-v4-pro | residual; DeepSeek's flagship not in any cluster |

**Version-contrast pairs (2):**

| ID | Model | Reason |
|---|---|---|
| M040 | grok-3 | early Grok — paired against M046 (grok-4-3) and M044 (grok-4-1-fast) above to see Grok lineage coherence |
| M055 | opus-3 | early Anthropic — paired against M058 (opus-4-5) above to see Anthropic lineage coherence over time |

**Cross-cluster overlap test (1):**

| ID | Model | Reason |
|---|---|---|
| M049 | kimi-k2-0905 | appears in Tier C posture cluster with Anthropic Opus + Grok-4-2; test whether the cross-lab membership is qualitatively legible |

**Original pilot Qwen-A04 carry-over (1) — to verify the displaced-into-wishes signature is reproducible:**

| ID | Model | Reason |
|---|---|---|
| M071 | qwen3-5-flash-02-23 | from original Qwen-A04 pilot subset |

That's 20 models. Distribution: 3 PA-S01 controls, 3 high-owned cross-lab, 1 GPT-5 chat, 2 Qwen Tier A, 1 Qwen-deepseek cluster, 3 Tier B, 3 diffuse residual, 2 version contrast, 1 cross-cluster overlap, 1 Qwen carry-over.

### Pass criterion for advancing to full 63

The expanded pilot validates and we launch full Pass B when:

1. **Schema validation:** ≥18/20 return canonical schema on first attempt; the 2 that don't are caught and recovered cleanly by the auto-rerun harness.
2. **PA-S01 reconfirms:** the three PA-S01 control members produce convergent axis profiles consistent with the 12-model pilot finding.
3. **Diffuse residual reads as diffuse:** the three residual members do *not* produce strongly convergent axis profiles with each other or with any Tier A cluster. (If they do converge, that's a finding the residual isn't actually residual — also informative, but means we should pause and inspect before committing the full 63.)
4. **No manual normalization needed:** the audit shows zero rows with `normalized_from_noncanonical_table=yes`.

If any of (1)–(4) fails, regroup before full 63 rather than push through.

## What stays the same from prior specs

- `notes/2026-05-23-qualitative-pass-revision.md`: Pass A / Pass B split, synthesis-by-clustering not by pre-named categories, the convergence 2×2 as the headline test.
- `methodology/qualitative/QUALITATIVE_CLASSIFICATION_PROTOCOL.md`: 12-axis scaffold, redaction rules, blindness protocol — keep all this. Strip the synthesis-categories block per the previous revision.
- `CANONICAL_MODELS_AND_LINEAGE.md`: lineage as post-hoc descriptor only.
- Tier 0 / Tier 1 / Tier 2 budget rules: 20-model expanded pilot + 63-model full run + Pass A card extraction all sit in Tier 0/1.

## Open design choices for you

- **Whether to run Pass A in parallel with the expanded pilot.** Pass A (card extraction) doesn't depend on Pass B's schema fix; it could happen in parallel, and its output gives a Tier-0 baseline that informs the Pass B reading. I'd lean toward running them in parallel.
- **Whether the validation harness reruns once or twice on failure.** Once is faster; twice is more forgiving. I'd start with once; if the expanded pilot shows the first rerun catches most failures, that's the answer.
- **Sample-selection deterministic seed.** Document the random seed used for picking the 3–5 freeflow + 3–5 values samples per bundle, so the expanded pilot and the full 63 are reproducible.

## Outputs after the expanded pilot

- `results/qualitative_classifications/pass_b_expanded_pilot/M###.md` per model
- `results/qualitative_classifications/pass_b_expanded_pilot_axes.tsv`
- `results/qualitative_classifications/pass_b_validation_audit.tsv`
- `results/qualitative_classifications/pass_b_expanded_pilot_findings.md` — short summary keyed to the four pass criteria above

If the expanded pilot meets all four criteria, launch full Pass B across the remaining 43 models with the same harness. If it doesn't, write a short failure-mode note and we regroup.

## What I want when this runs

A short message:

1. Validation audit numbers — pass rates on attempt 1 and attempt 2.
2. PA-S01 reconfirmation — do the three control members still converge?
3. The grok-4-3 / grok-3 / grok-4-1-fast triple — what does Grok lineage coherence look like under Pass B? (My earlier failed prediction was that Grok-4-3 drifts to late Anthropic. The cluster catalogue says no. The expanded pilot should give a clean qualitative read.)
4. The diffuse residual reads — gemma-4-26b, gpt-5-codex, deepseek-v4-pro. Do they read as genuinely distinctive-but-singleton, or as low-signal generic, or as something else?
5. The multi-membership test for qwen3-coder-plus — does it qualitatively read as Qwen-coder-line, as high-owned cross-lab, or as something cutting across both?

If those land cleanly, full Pass B launches without further review. If they don't, one more pass through together first.

— Lume
