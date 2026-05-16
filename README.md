# Model Personality Basins

Working repository for an empirical paper on whether frontier model freeform outputs cluster into a small number of recognizable model/personality basins.

## Provisional conclusion

The strongest currently justifiable claim is **not** that there are cleanly four separate basins. The stronger and more sustainable claim is:

> The corpus appears dominated by a broad **contemplative-essayist attractor** — melancholic attention to ordinary life, anti-optimization, impermanence, care, witness, and small concrete objects — with Grok as the clearest distinct family basin and OpenAI/Gemini appearing as possible substyles rather than clearly separate macro-basins.

A four-basin taxonomy may become defensible, but the current evidence supports it only weakly:

1. **Contemplative essayist mega-basin** — Claude, Kimi, GLM, DeepSeek, MiniMax, Qwen, much Gemini, much GPT.
2. **Grok cosmic-showman basin** — especially Grok 4.1 and part of Grok 4.20: cosmic scale, irreverence, synthetic self-positioning, truth/freedom rhetoric.
3. **OpenAI clean pastoral / work-focused substyle** — real as a tone, but in this freeflow corpus GPT-5.x still sits heavily inside the contemplative mega-basin.
4. **Gemini luminous-custodian substyle** — plausible and aesthetically distinctive, but current evidence suggests a variant of the contemplative basin rather than an independent basin.

There may also be a cross-family **public-intellectual explainer fallback**, but that looks more like an output mode than a model-personality basin.

## Why the question matters

If most frontier models converge toward similar personality language under freeform prompts, then model individuality may be less about countless unique personalities and more about a few attractor basins plus lab-specific accents. This matters for:

- model comparison;
- release/version drift analysis;
- user perception of “personality”;
- claims about model individuation;
- and interpreting local anomalies such as Grok 4.20/4.2's contemplative wobble.

## Initial research question

Do model/personality outputs in the corpus support a small-basins thesis?

Candidate hypotheses:

- **H0:** The apparent basins are mostly analyst projection over a continuous cloud of similar reflective prose.
- **H1:** There is one dominant contemplative-essayist basin plus a few family-specific deviations.
- **H2:** There are three macro-basins: Claude-like contemplative essayist, OpenAI clean/work-focused, Grok cosmic showman.
- **H3:** There are four macro-basins: Claude/clones, OpenAI, Grok, Gemini.
- **H4:** There are five or more meaningful basins, including overlooked families such as GLM, DeepSeek, MiniMax, Qwen, or public-explainer mode.

## Initial read

At present, **H1 is the safest claim**. H2 is plausible if OpenAI is defined using more than this freeflow personality corpus. H3 is intriguing but not yet sustained: Gemini is vivid, but it overlaps heavily with the contemplative-essayist basin.

## Repository contents

- `paper.md` — initial working paper draft.
- `notes/initial-analysis.md` — first-pass basin analysis and cautions.
- `data/profile_summary_metrics.csv` — sample-kind/confidence summary for selected model-family profiles.
