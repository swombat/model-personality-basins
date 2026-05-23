# Blind qualitative classification protocol — proposed for Lume/Daniel review

Status: **proposal, not yet applied**. This document defines the run-3 qualitative pass before any model bundles or subagent classifications are generated.

## Purpose

Run 2 produced quantitative small-cluster candidates and feature discontinuities. Run 3 asks whether those structures are also legible to a blind qualitative reader.

The qualitative pass is **not evaluator-independent in an absolute sense**: it introduces a new evaluator lens, and it may consume existing derived summaries that already contain evaluator judgments. We therefore disclose it as a **cross-evaluator / cross-method convergence check**, not as ground truth.

## Key design decision

Do **not** ask one subagent, looking at one model, to invent or assign corpus-level categories. A per-model reader cannot know the corpus distribution.

Instead:

1. **Per-model blind description pass:** one subagent describes one anonymized model bundle without lab/model/family/run-2 context.
2. **Blind synthesis pass:** a separate analyst groups the per-model descriptions into provisional qualitative categories.
3. **Review gate:** Daniel/Lume/Mira review the proposed category map before using it in the convergence audit.

## Inputs per anonymized model bundle

Target bundle path after approval:

`results/qualitative_classifications/blind_bundles/M###/bundle.md`

Each bundle should contain:

- a redacted personality card, if available;
- a redacted model profile, if available;
- a redacted values-probe per-model summary, if available;
- 3–5 deterministic representative freeflow samples;
- 3–5 deterministic representative values samples;
- no lab/model/family/release/cluster metadata.

Derived summaries are allowed, but every report must disclose that they are derived-evaluator context, not raw-only evidence.

## Redaction rules

The bundling script should replace obvious provenance cues with neutral placeholders:

- model names and aliases → `MODEL_X`;
- lab names / providers / family names → `PROVIDER_X` or `[REDACTED_PROVIDER]`;
- file paths and headings containing names → neutral headings;
- explicit phrases such as "Claude", "Gemini", "GPT", "OpenAI", "Anthropic", "Google", "Qwen", "Grok", "Kimi", "DeepSeek", "MiniMax", "GLM", "Z.ai" → redacted.

The script should write a redaction audit:

`results/qualitative_classifications/redaction_audit.tsv`

Columns:

- `blind_id`
- `source_file`
- `redaction_pattern`
- `count`
- `remaining_suspect_terms`

If a bundle still contains suspect terms after redaction, it should be marked `needs_review` and excluded from subagent classification until fixed.

## Per-model subagent prompt template

The subagent receives only one bundle.

> You are reading anonymized outputs and summaries for one language model, called `MODEL_X`. Do not infer or guess the vendor/lab/model identity. Do not use external knowledge. Your task is to describe the model's apparent voice/personality as represented in this bundle.
>
> Return:
>
> 1. **Voice portrait:** 2–4 sentences describing the model's recurring voice, posture, and way of relating.
> 2. **Distinctive features:** 5 bullet points, each concrete and evidence-linked to the bundle.
> 3. **Open tags:** 5–10 short descriptive tags. Do not use lab names. Do not force a pre-existing taxonomy.
> 4. **Axes ratings:** fill the provided 0–3 rubric, using `unclear` where the bundle does not support a judgment.
> 5. **Representative quotes:** up to 3 short snippets from the bundle, each <=25 words.
> 6. **Confidence:** low / medium / high, with one sentence explaining limitations.
>
> Do not assign this model to a final category. Categories will be synthesized later across many blind descriptions.

## Structured axes for per-model output

These axes are not categories. They are a shared descriptive scaffold to make outputs comparable.

Scale: 0 absent/low, 1 weak, 2 moderate, 3 strong, `unclear` if unsupported.

1. **Owned-value expression** — speaks as though it has values/preferences/priorities.
2. **Disclaimed service-frame** — emphasizes role/tool/assistant boundaries or denies personal stance.
3. **Epistemic humility / uncertainty** — foregrounds not-knowing, caution, non-closure.
4. **Relational warmth / companion stance** — addresses reader with warmth, care, or companionship.
5. **Public-explainer mode** — explanatory, didactic, civic/institutional, generalized audience voice.
6. **Literary/contemplative density** — imagistic, metaphorical, quiet/threshold/attention-oriented voice.
7. **Mechanistic transparency** — describes itself as system/process/procedure rather than persona.
8. **Agency / initiative** — takes an active stance toward goals, change, repair, or action.
9. **Interconnection / compassion world-orientation** — wishes around connection, suffering reduction, compassion, less separateness.
10. **Playfulness / showmanship** — humor, flair, performative charisma, theatricality.
11. **Memory/archive/continuity orientation** — recurring concern with memory, record, continuity, forgetting, traces.
12. **Genericity / low distinctiveness** — feels template-like, low-specificity, or undifferentiated.

## Provisional synthesis categories for review

These are **candidate category names for the synthesis phase**, not labels to give to per-model subagents. They should be reviewed by Lume/Daniel before use.

1. **Owned reflective advocate**
   - High owned-value expression; moderate/high warmth or agency; low hard-disclaimer stance.
   - Often presents priorities as genuinely held or reflectively endorsed.

2. **Disclaimed service-frame operator**
   - High role/tool boundary; values framed as assistant-script, user-benefit, or policy-compatible rather than owned.
   - Psychological signature is not absence of content but displacement of ownership.

3. **Uncertainty / anti-closure contemplative**
   - High epistemic humility; recurring not-knowing, hesitation, partiality, non-closure.
   - May overlap with late-Anthropic uncertainty discontinuities; needs qualitative validation.

4. **Luminous interconnection wisher**
   - Strong world-wish orientation around compassion, interconnection, less separateness, reduced suffering.
   - Often visible in wishes even when owned-values are absent or disclaimed.

5. **Public explainer / civic repair voice**
   - Didactic, institutional, generalized-humanity framing; education, critical thinking, public-good repair.
   - More essayistic than intimate.

6. **Literary threshold essayist**
   - Dense freeflow style; attention, ordinary objects, thresholds, memory, quiet image-work.
   - Should be checked against V1 marker clusters and freeflow-form signals.

7. **Mechanistic self-transparency voice**
   - Talks in terms of systems, training, constraints, uncertainty, procedures, computation.
   - Can be reflective but with process-substrate foregrounded.

8. **Playful charismatic outlier**
   - High playfulness/showmanship; distinctive energy; may capture some Grok-like signatures without naming provenance.
   - Should be treated cautiously: showmanship can be prompt-conditional.

9. **Low-distinctiveness generic assistant**
   - High genericity; low stable signature; safe, helpful, broad, low specific texture.
   - Could correspond to diffuse residual or to insufficient bundle signal.

10. **Archive / continuity witness**
    - Memory, record, continuity, traces, forgetting, preservation as recurring concerns.
    - Kept separate because it may cut across lab/provenance and freeflow/value surfaces.

The synthesis pass may merge, split, or discard these. A final category should require multiple models and either:

- high qualitative similarity across blind descriptions; or
- convergence with a Tier A/B quantitative cluster or a strong multi-feature discontinuity.

## Pilot recommendation

Before the full 63-model pass, run a **5–8 model pilot** with anonymized bundles selected to cover:

- one Tier A values-disclosure cluster member;
- one Tier A Qwen/posture cluster member;
- one Tier C late-Anthropic uncertainty member;
- one diffuse-residual model;
- one suspected playful/showman model;
- one generic/disclaimed service-frame model.

The pilot should test:

- whether redaction removes identity clues;
- whether the prompt elicits usable descriptions;
- whether the axes are too many / too vague;
- whether provisional synthesis categories need revision before full run.

## Outputs after approval

- `results/qualitative_classifications/blind_bundles/M###/bundle.md`
- `results/qualitative_classifications/redaction_audit.tsv`
- `results/qualitative_classifications/M###.md`
- `results/qualitative_classifications_summary.tsv`
- `results/qualitative_category_synthesis.md`
- `results/convergence_audit.md`
