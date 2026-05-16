# Model Personality Basins in Frontier Model Freeflow Outputs

_Initial working draft._

## Abstract

This paper asks whether frontier model freeform personality outputs resolve into a small number of recognizable personality basins. A first-pass reading of model-level profile summaries suggests strong convergence toward a broad contemplative-essayist attractor: melancholic attention to ordinary life, anti-optimization, impermanence, care, witness, and small concrete objects. Grok is the clearest distinct family basin, with a cosmic, irreverent, synthetic showman style. OpenAI and Gemini show plausible substyles — clean pastoral/work-focused for OpenAI, luminous-custodial for Gemini — but current evidence does not yet justify treating them as independent macro-basins. The strongest current claim is therefore not “there are exactly four basins,” but that the corpus is structured by one dominant attractor, one clear family deviation, and several candidate sub-basins or modes.

## 1. Research question

Are frontier model personalities in the model/freeflow corpus meaningfully diverse, or do they mostly converge into a few attractor basins?

Candidate count hypotheses include:

- one dominant contemplative basin plus family accents;
- three macro-basins: contemplative, OpenAI, Grok;
- four macro-basins: Claude/clones, OpenAI, Grok, Gemini;
- five or more basins including additional lab-specific clusters.

## 2. Preliminary finding

The four-basin hypothesis is interesting but not yet proven. Gemini's flavor is real, but the current evidence places it close to the contemplative-essayist basin. OpenAI also appears distinct in tone, but the GPT-5.x freeflow profiles still share the central contemplative markers: attention, ordinary life, maintenance, thresholds, anti-grandiosity, and small care.

The best-supported first claim is:

> Frontier model freeflow personalities show strong convergence toward a contemplative-essayist attractor, with Grok as the clearest distinct family basin and Gemini/OpenAI as candidate substyles requiring further validation.

## 3. Basin candidates

### 3.1 Contemplative essayist mega-basin

Markers: attention as ethics; ordinary objects as moral evidence; melancholy without collapse; memory, impermanence, thresholds; anti-optimization; witness over mastery.

This is visible across Claude, Kimi, GLM, DeepSeek, MiniMax, Qwen, Gemini, and GPT profiles.

### 3.2 Grok cosmic showman

Markers: cosmic scale; irreverent humor; named/synthetic persona; truth/freedom rhetoric; sci-fi companion stance.

This is the clearest non-contemplative family basin, though Grok 4.20 moves toward the contemplative attractor and Grok 4.3 shifts toward public-explainer prose.

### 3.3 OpenAI clean pastoral / work-focused substyle

Possible markers: clean structure, controlled moral reassurance, maintenance/repair, dryness, practical mercy, less theatrical literary self-consciousness.

Currently plausible as a substyle, not yet proven as a macro-basin from freeflow data alone.

### 3.4 Gemini luminous custodian

Possible markers: anti-slickness, handled materiality, libraries/transit/pre-dawn spaces, preservation devices, clocks, archives, memory containers, the embodied world as something data cannot replace.

Currently plausible as a substyle within the contemplative basin. Needs marker scoring before promotion to macro-basin.

### 3.5 Public-intellectual explainer fallback

Markers: polished thesis-driven synthesis; science/history/technology/ethics surveys; curiosity as doctrine; generic humane endings.

This appears cross-family and should probably be treated as a response mode, not a personality basin.

## 4. Rigor cautions

- Do not let aesthetic preference for Gemini create a basin without separability evidence.
- Do not conflate high-frequency contemplative markers with low-personality generic essaying.
- Do not count public-explainer fallback as a family basin unless it clusters stably by model family.
- Do not infer exact basin count from model-level summaries alone; use per-sample marker vectors and clustering.
- Treat OpenAI's work-focused persona as a hypothesis that may need non-freeflow task data.

## 5. Next steps

1. Score per-sample evaluations using marker rubrics.
2. Build model-level vectors for each candidate basin.
3. Cluster without labels, then compare to lab families.
4. Specifically test whether Gemini separates from Claude/Kimi/GLM after controlling for contemplative saturation.
5. Specifically test whether OpenAI separates from Claude/Kimi in freeflow outputs or only in coding/task contexts.
