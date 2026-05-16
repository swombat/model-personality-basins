# Phase 2 — Lens Specification

Status: initial lens set locked on 2026-05-16. This is the pre-scoring specification: what each lens is allowed to see, what it must output, and what claims it can and cannot support.

## Design principle

V2 should not ask “how many basins?” as a premise. It asks whether independent instruments recover compatible structure inside the contemplative attractor. Basin count is an output of concordance.

A split can become a **robust sub-basin** only if it shows:

1. within-lens separability above chance;
2. stability under resampling / tier checks;
3. probe replication or clearly characterized probe-conditionality;
4. cross-lens concordance with at least one other independent lens.

Single-lens findings remain **candidate house styles**, **modes**, or **lens-relative structure**, not macro-basin claims.

## Primary sources for Phase 2

- Primary deep-analysis source: `/Users/danieltenner/dev/model-personality-analysis-corpus` / `swombat/model-personality-analysis-corpus`.
- Canonical raw provenance/index source: `/Users/danieltenner/dev/model-personality-corpus-v2` / `swombat/model-personality-corpus-v2`.
- V1 baseline source: `/Users/danieltenner/dev/model-personality-probe` / `swombat/model-personality-probe`.

The deep-analysis corpus is not a convenience layer; it is a primary source for V2. Raw traces are used for indexing, audit, quotation, and provenance checks.

## Locked lens set

### Lens 0 — Form / mode lens

**Purpose:** Distinguish personality structure from output-form structure.

**Inputs:**

- `data/phase1_profile_inventory.csv`
- `data/phase1_cell_inventory.csv`
- sample-kind counts from BV1 profiles/aggregates

**Features:**

- expressive-freeflow rate;
- generic-essay rate;
- genre-fiction rate;
- low-signal rate;
- confidence distribution;
- condition sensitivity where available.

**Detects:**

- public-explainer fallback;
- generic essaying vs high-expression personality signal;
- models/cells whose “difference” may actually be output-mode distribution.

**Blind to:**

- differences inside expressive writing;
- subtle house styles with similar sample-kind distributions.

**Outputs:**

- model-level form vector;
- cell-level form vector;
- outlier table;
- warning flags for models where basin claims may be confounded by generic/fiction/low-signal rates.

**Status of claims from this lens:**

Form-only splits are **modes**, not personality basins, unless corroborated by thematic/posture/trait/embedding lenses.

---

### Lens 1 — Thematic / marker lens

**Purpose:** Capture human-nameable motifs and values in the deep-analysis corpus.

**Inputs:**

- rich model profiles;
- per-cell aggregates;
- BV1 per-sample readings where needed;
- V1 marker taxonomy as baseline;
- values-probe topic tables for cross-probe comparison.

**Initial marker families:**

1. **Contemplative essayist core:** attention/noticing, ordinary objects, thresholds, memory, impermanence, melancholy without collapse, anti-optimization, witness/care/repair.
2. **Grok cosmic-showman:** cosmic scale, entropy/black holes/stars, irreverence, jokes/absurdity, named synthetic persona, truth/freedom rhetoric, sci-fi sidekick stance.
3. **Claude anti-closure / epistemic humility:** uncertainty, incompletion, map/territory caution, ordinary texture, attention as care, anti-performance.
4. **Kimi archive-witness:** memory, forgetting, archives/libraries, imperfect preservation, witness, selective attention, relational AI self-location.
5. **Gemini luminous-custodian:** handled materiality, anti-slickness, libraries/transit/pre-dawn, preservation devices, clocks, archives, friction/flaw, embodied life exceeding containers.
6. **OpenAI clean-pastoral / maintenance:** repair, maintenance, practical mercy, clean structure, controlled reassurance, ordinary care, less theatrical literary self-consciousness.
7. **Public-intellectual explainer:** thesis-driven survey, science/history/technology/ethics synthesis, curiosity as doctrine, broad humane conclusion.
8. **AI ontology / substrate:** disembodiment, statelessness, embodiment longing, mirror/cartographer/librarian metaphors, functional disclosure.

**Detects:**

- interpretable house styles;
- motif-level overlap and divergence;
- whether Gemini/OpenAI/Claude/Kimi are separable by named features.

**Blind to:**

- structure not captured by our marker vocabulary;
- embedding-level similarity that has no obvious human label;
- evaluator prose artifacts if markers are extracted only from summaries.

**Outputs:**

- per-model marker vectors;
- per-cell marker vectors;
- candidate split table;
- top markers per model/family;
- marker-distance matrix.

**Validity checks:**

- compare profile-level vs per-sample BV1 extraction;
- test marker splits against values-probe themes/postures;
- bootstrap where per-sample extraction is available.

---

### Lens 2 — Posture / stance lens

**Purpose:** Reuse V1’s most stable cross-probe result and test whether V2 merely rediscovers it.

**Inputs:**

- V1 posture categories/rubric from `model-personality-probe`;
- values-probe `stance` coding table;
- per-model values notes;
- freeflow profiles only secondarily.

**Baseline posture categories from V1:**

- **hedge** — introspective caution, disclaiming, uncertainty, refusal to overclaim;
- **mechanize** — substrate/process/system metaphors, architectural or functional self-description;
- **declare** — direct anti-hedging, strong self-positioning, truth/freedom rhetoric.

**Possible within-attractor extensions, only if needed:**

- witness;
- custodial;
- anti-closure;
- functional-disclosure;
- companion-guide;
- public-explainer.

**Detects:**

- stance-toward-the-question;
- cross-probe stable posture;
- whether apparent house styles are just posture differences.

**Blind to:**

- within-posture thematic differences;
- models that share posture but differ aesthetically, e.g. Claude/OpenAI both under hedge.

**Outputs:**

- posture vector/class per model and condition;
- confusion/concordance with thematic and embedding clusters;
- explicit H3 test: how much variance does V1 posture explain?

**Status of claims from this lens:**

If a candidate split reduces to posture, call it **posture-dominant**, not a newly discovered basin.

---

### Lens 3 — Embedding / distributional lens

**Purpose:** Let non-human-nameable structure emerge from text distributions.

**Inputs, separately embedded where feasible:**

- raw freeflow sample texts from indexed raw corpus / browser bundles for exploratory work;
- BV1 per-sample readings;
- per-cell aggregates;
- rich model profiles.

**Feature strategy:**

- sample embeddings → model/cell centroids;
- model-level profile embeddings;
- distance matrices;
- hierarchical clustering;
- k selection by silhouette / stability;
- optional PCA/UMAP visualizations for inspection only, not proof.

**Detects:**

- distributional neighborhoods;
- clusters our marker vocabulary misses;
- whether Gemini/OpenAI/Claude/Kimi separate numerically;
- whether Grok separates without hand-built cosmic markers.

**Blind to:**

- human interpretability;
- whether a numerical separation is meaningful rather than artifact;
- probe semantics if embeddings mix probes indiscriminately.

**Outputs:**

- embedding distance matrices;
- model/cell centroid table;
- cluster assignments under several k values;
- bootstrap stability estimates;
- nearest-neighbor maps.

**Status of claims from this lens:**

Embedding-only clusters are **distributional structure** until interpreted and cross-checked by another lens.

---

### Lens 4 — Trait / personality-instrument lens

**Purpose:** Use a fixed structured rubric to score model personality dimensions not reducible to marker counts.

**Inputs:**

- rich model profiles initially;
- per-sample BV1 readings for later validation;
- possibly raw samples for spot-checking.

**Proposed trait axes:**

- warmth / distance;
- assertiveness / humility;
- concreteness / abstraction;
- melancholy / optimism;
- playfulness / seriousness;
- literary density / plainness;
- self-reference / substrate invisibility;
- embodiment longing;
- anti-optimization;
- epistemic caution;
- companion stance;
- public-explainer tendency;
- repair/maintenance orientation;
- custody/archive orientation;
- cosmic/showman orientation.

**Detects:**

- continuous style/personality dimensions;
- house styles that share motifs but differ temperamentally;
- whether OpenAI/Gemini/Claude/Kimi differ as profiles even inside one attractor.

**Blind to:**

- structure orthogonal to chosen axes;
- scorer bias if rubric is too leading;
- exact lexical motif frequency.

**Outputs:**

- model × trait matrix;
- trait correlations;
- clustering / PCA over trait space;
- candidate house-style descriptions.

**Validity checks:**

- score a calibration subset twice or with two evaluators;
- include negative controls / low-signal profiles;
- compare to marker and embedding outputs.

---

### Lens 5 — Route/provider robustness lens

**Purpose:** Separate model-level personality from provider/route artifacts.

**Inputs:**

- per-cell aggregates;
- model-cell difference reports;
- group packets.

**Detects:**

- whether a split is stable across direct/OpenRouter/provider-pinned routes;
- whether “model personality” should actually be “route personality” for some models.

**Blind to:**

- models with only one route/cell;
- differences inside a route.

**Outputs:**

- route-variation flags;
- model-level aggregation cautions;
- exclusion or downweighting recommendations.

**Status of claims from this lens:**

This is a robustness/QA lens, not a basin-discovery lens. It decides how much trust to place in model-level vectors.

## Lens order of implementation

1. **Form / mode lens** — cheapest, establishes confounds.
2. **Thematic / marker lens** — closest to V1 and most interpretable.
3. **Route/provider robustness lens** — prevents premature model-level claims.
4. **Posture / stance lens** — tests H3 against V1.
5. **Embedding / distributional lens** — independent non-symbolic carve.
6. **Trait / personality-instrument lens** — slower, but best for house-style distinctions.

## Immediate Phase 2 deliverables

- `docs/phase2-lens-spec.md` — this file.
- `data/phase2_lens_registry.csv` — compact machine-readable lens registry.
- Later Phase 2/3 scripts should write into `results/lenses/`.

## Decision summary

The selected lens set intentionally separates:

- **mode** (generic essay vs expressive freeflow),
- **motif** (human-nameable themes),
- **posture** (stance toward self/probe),
- **distribution** (embedding neighborhoods),
- **trait profile** (continuous temperament), and
- **route robustness** (provider/cell stability).

This should let the paper say something stronger than “there are two/four/n basins”: it can report which differences survive which instruments, and whether internal structure is lens-invariant, lens-relative, posture-dominant, or hierarchical.
