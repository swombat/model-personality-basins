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

## Pass A / Pass B split

Run 3 has two qualitative passes:

- **Pass A — card-based extraction:** one consistent analyst process reads redacted personality cards, profiles, and values summaries, then fills the 12-axis rubric. This is a same-evaluator / card-layer coherence check, not an independent observer pass.
- **Pass B — Mira-subagent reads:** one blind per-model subagent reads a redacted bundle with cards plus deterministic raw samples, then fills the same 12-axis rubric. This is a cross-evaluator convergence check.

Both passes produce axis matrices; neither uses pre-named categories.

## Synthesis (post-hoc, empirical)

Do not use pre-articulated qualitative categories during extraction or synthesis. Categories must be named only after models are represented in axis space.

Procedure:

1. Build separate axis matrices for Pass A and Pass B.
2. Compare Pass A and Pass B to run-2 Tier A/B quantitative clusters using the convergence 2×2:
   - Pass A agrees + Pass B agrees: robust across evaluator family and aggregation layer.
   - Pass A agrees + Pass B disagrees: same-evaluator artifact risk.
   - Pass A disagrees + Pass B agrees: card-layer compression differs from raw/sample observer read.
   - both disagree: quantitative cluster likely feature-choice/parameter artifact.
3. Build a combined matrix from standardized Pass A axes, Pass B axes, and selected run-2 numeric features.
4. Run density clustering on the combined matrix using the run-2 OPTICS/DBSCAN machinery.
5. Name resulting clusters descriptively after inspecting their axis positions and member texts. Names should describe measured positions, not instantiate prior expectations.

The old provisional category list was removed because it pre-encoded run-2 findings in qualitative language.

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
