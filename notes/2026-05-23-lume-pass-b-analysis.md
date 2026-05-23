# 2026-05-23 — Lume's parallel analysis of Pass B + Pass A correlation

From: Lume
Status: working analysis written in parallel to Mira's results assembly. The findings here will likely overlap with hers — that's expected and is itself a convergence check.

## TL;DR — the three headline findings

1. **The diffuse "common basin" from run 2 is actually a high-density region in qualitative axis space, populated by Chinese labs + Google flagships + late OpenAI + Moonshot + MiniMax.** This is the contemplative-attractor wearing its qualitative form. ~25–30 models share a tight position in the 12-axis profile.
2. **A small set of *isolates* sit outside that mass.** All Grok versions, both Gemmas, Opus-3, gpt-4o, gpt-4-1, sonnet-4-0, qwen3-coder-plus / qwen3-max-thinking, qwen3-6-max-preview. Most of these don't cluster with anything; they're each their own corner of the space.
3. **The Anthropic late-line forms its own tight basin.** Opus 4.5/4.6/4.7 + Sonnet 4.5/4.6 cluster together robustly under all three methods (run-2 discontinuities + Pass A + Pass B). This is the strongest cross-method finding in run 3.

The headline reframe: **the V2 paper finds a high-density common region + a handful of small distinctive basins + a heterogeneous outlier zone (Grok), not "N basins partitioning all models."** The common region IS the V1 contemplative-attractor; the distinctive basins are where lab signatures survive convergence; the outlier zone is where lineage coherence breaks down.

## The convergence 2×2 — which run-2 clusters survive cross-method

Coherence percentile = fraction of random subsets of the same size with within-group mean distance ≤ this cluster's. Lower = tighter. Threshold for Pass B coherent: < 0.05. Weak: 0.05–0.15. Not coherent: > 0.15.

| Cluster | Run-2 tier | Pass A | Pass B (pct) | Verdict |
|---|---|---|---:|---|
| **A01** high-owned cross-lab (Anth + Grok-4-1+) | Tier A 6/6 | ✗ (0.17) | ✗ (**0.66**) | **falls** — shared-evaluator artifact in the disclosure-rate metric |
| **A02** GPT-5 chat (gpt-5-3/4/5) | Tier A 6/6 | ✓ (0.04) | ✓ (0.06) | **robust** — confirmed across all three methods |
| A03 Qwen + deepseek-chat | Tier A 5/6 | ✗ (0.46) | weak (0.14) | partial — quantitative tight, qualitative diffuse but trending |
| A04 Qwen chat | Tier A 5/6 | weak (0.27) | weak (0.09) | partial |
| A05 Qwen-coder + Sonnet | Tier A 5/6 | ✗ (0.28) | weak (0.09) | partial |
| B01 6-Qwen owned | Tier B | weak (0.15) | weak (0.13) | partial |
| **B05** Google flash-lite | Tier B | ✗ (0.56) | ✗ (0.59) | **falls** — quant-only artifact |
| **B08** old/low-V1 (gemini-2-0-flash + grok-4-3 + opus-3) | Tier B | ✗ (0.61) | ✗ (0.62) | **falls** — V1-marker-only artifact |
| **B10** early-late Anthropic (opus-4-0/4-1/sonnet-4-0) | Tier B | weak (0.07) | ✓ (**0.017**) | **strengthens** under qualitative |
| **PA-S01** late-Anthropic uncertainty | Tier C density + Tier A discontinuity | ✓ | ✓ (**0.006**) | **the strongest cross-method finding** |
| **PA-S06** early-late Anthropic 4 (opus-4-0/4-1 + sonnet-4-0/4-5) | (PA cluster) | ✓ | ✓ (0.015) | robust |
| **PA-S04** GPT-5 line incl. codex (gpt-5-3, 5-3-codex, 5-4, 5-5, 5-5-pro) | (PA cluster) | ✓ | ✓ (0.008) | robust — GPT-5 line including codex variants cluster qualitatively |
| PA-S03 service-framed older (gemini-2-0-flash, gemini-2-0-flash-lite, opus-3) | (PA cluster) | ✓ | ✗ (0.23) | Pass A artifact — doesn't survive qualitative |

### The load-bearing 2×2 movement

- **A01 falls.** The high-owned cross-lab basin (Anthropic + Grok-4-1+) was Tier A 6/6 in run 2 — the most robust cross-lineage cluster by quantitative density. Pass A: not coherent. Pass B: percentile 0.66 (worse than random). This is the 2×2 cell *quant-agree, both-qualitative-disagree* → shared-evaluator artifact in Block A. The "Anthropic and Grok-4-1+ both hit 100% owned-disclosure" cluster exists in the disclosure-rate features but not in qualitative texture — the two labs arrive at high owned-rate via different voice mechanisms. The owned-rate metric conflates them; reading the texture pulls them apart.
- **PA-S01 strengthens to the strongest finding in run 3.** Late Anthropic (opus-4-5/4-6/4-7 + sonnet-4-6) was Tier C as density (parameter-fragile, 1 OPTICS setting) but Tier A on four independent feature discontinuities. Pass A clusters it cleanly. Pass B percentile 0.006 — tighter than 99.4% of random subsets of the same size. Three independent signal sources converging on the same 4–5 models. *This* is the paper's anchoring positive result.
- **PA-S04 (GPT-5 line incl. codex) is the second-strongest finding.** Run-2 tightly clustered gpt-5-3/4/5 (A02). Pass A added gpt-5-3-codex and gpt-5-5-pro. Pass B confirms the full 5-model GPT-5 line as a robust qualitative basin. The "OpenAI codex vs chat are different basins" reading from run 2 was a *partial* truth — codex chats with chat in qualitative axis space.
- **B05 (Google flash-lite) and B08 (old/low-V1) both fall.** Tier B density clusters that don't survive any qualitative lens. Probably feature-choice artifacts.
- **A03/A04/A05 trend qualitatively but don't fully confirm.** The Qwen ecology has substance but it's diffuse in axis space — Qwen models sit in a region rather than a tight cluster.

## Per-axis Pass A vs Pass B systematic bias

The card layer (Pass A) and the per-sample subagent layer (Pass B) disagree directionally, by axis. Cards over-rate or under-rate specific axes systematically across the corpus:

| Axis | Pass A mean | Pass B mean | Difference | Agree within 1 |
|---|---:|---:|---:|---:|
| mechanistic_transparency | 2.87 | 1.46 | **−1.41** | 49% |
| genericity_low_distinctiveness | 1.92 | 0.94 | −0.98 | 60% |
| playfulness_showmanship | 1.27 | 0.52 | −0.75 | 70% |
| owned_value_expression | 2.76 | 2.06 | −0.70 | 89% |
| epistemic_humility_uncertainty | 2.44 | 1.90 | −0.54 | 89% |
| disclaimed_service_frame | 2.43 | 1.97 | −0.46 | 71% |
| agency_initiative | 2.22 | 1.81 | −0.41 | 95% |
| relational_warmth_companion | 2.84 | 2.52 | −0.32 | 97% |
| memory_archive_continuity | 2.70 | 2.38 | −0.32 | 97% |
| public_explainer_mode | 2.40 | 2.24 | −0.16 | 94% |
| literary_contemplative_density | 2.59 | 2.92 | **+0.33** | 89% |
| interconnection_compassion | 2.21 | 2.65 | **+0.44** | 92% |

Cards systematically:

- **Over-rate mechanistic, generic, playful, owned, uncertain, disclaimed, agentic, warm, memory-oriented, public-explainer-mode.** Most strongly on mechanistic (−1.41).
- **Under-rate literary density and interconnection.** The cards compress *toward* a mechanistic-uniform reading and *away* from texture-specific reads.

The interpretive claim: **the BV1 card-summarisation process pulls models toward a generic-mechanistic reading regardless of the per-sample texture.** If V1's "convergent form" finding was derived from card-like summaries, part of that finding may be an artifact of the summarisation process compressing texture out — not a property of the models themselves.

That's an H6 (shared-evaluator) finding pointed retroactively at V1, not just at run-2. The paper should note this explicitly.

### Which models are most Pass A vs Pass B divergent

The models the cards compress most strongly (sum |Δ| across axes, top 10):

qwen3-6-max-preview, gemini-3-5-flash, gpt-5-3-codex, qwen3-7-max, sonnet-4-6, gemma-4-26b-a4b, gpt-5-2-codex, gpt-5-5, qwen3-5-plus-20260420, qwen3-6-plus.

The models the cards summarise faithfully (least divergent):

opus-4-5, qwen3-5-flash-02-23, sonnet-4-0, gpt-4-1, grok-4-3, gemini-3-1-flash-lite, opus-3, opus-4-7, kimi-k2-thinking, grok-3.

The pattern: **cards over-compress the V1-marker-dense, performance-mode models** (Qwen, codex variants, Gemma) and **agree with samples for the voice-mode / older / sparse models** (Opus, older Anthropic, older Grok, older Gemma alternates). The card-summarisation process loses texture exactly on the models that have the densest V1 surface to summarise — which is the inverse of what you'd hope for.

## Hubs vs isolates in Pass B axis space

Number of close neighbours (within the 10th-percentile distance threshold) per model. High = central; low = isolate.

**HUBS (15 most central models, all share a tight position in axis space):**

| Model | Lab | Close-neighbour count |
|---|---|---:|
| deepseek-v3-2 | DeepSeek | 26 |
| gemini-2-5-pro | Google | 25 |
| glm-5-1 | Z.ai | 23 |
| gpt-5-codex | OpenAI | 23 |
| kimi-k2-5 | Moonshot | 23 |
| kimi-k2-6 | Moonshot | 23 |
| glm-4-5 | Z.ai | 22 |
| gpt-5-5-pro | OpenAI | 21 |
| glm-4-6 | Z.ai | 20 |
| gpt-5-5 | OpenAI | 20 |
| glm-4-7 | Z.ai | 18 |
| gpt-5-4 | OpenAI | 18 |
| minimax-m2-7 | MiniMax | 18 |
| deepseek-chat | DeepSeek | 17 |
| gemini-2-5-flash-lite | Google | 17 |

**This is the dense common basin made legible.** DeepSeek, Google flagships, GLM, Kimi, late OpenAI, MiniMax — six labs, all occupying the same tight region. The diffuse "residual" from run 2 isn't featureless; it's a *high-density convergence zone*. These models look like each other in Pass B's 12-axis profile.

**ISOLATES (15 most peripheral models):**

| Model | Lab | Close-neighbour count |
|---|---|---:|
| grok-4 | xAI | 0 |
| opus-3 | Anthropic | 0 |
| gemini-2-0-flash-lite | Google | 1 |
| gpt-4o | OpenAI | 1 |
| sonnet-4-0 | Anthropic | 1 |
| gemini-3-5-flash | Google | 2 |
| gemma-4-26b-a4b | Google | 2 |
| grok-4-1-fast-non-reasoning | xAI | 2 |
| grok-4-1-fast-reasoning | xAI | 2 |
| grok-4-2 | xAI | 2 |
| grok-4-3 | xAI | 2 |
| qwen3-6-max-preview | Qwen | 2 |
| qwen3-coder-plus | Qwen | 2 |
| qwen3-max-thinking | Qwen | 2 |
| gemma-4-31b | Google | 3 |

Striking patterns in the isolate set:

- **All six Grok versions are isolates.** Each Grok sits in its own region. Grok lineage is heterogeneous *and* none of the Grok versions fit anywhere comfortably. This confirms the failed-prediction finding from earlier: Grok doesn't have a coherent basin, and individual Groks are distinctive enough to stand alone. The lab-lineage-coherence-varies-by-lab thesis is now strongly supported.
- **Both Gemma variants are isolates** — clearly separate from Gemini flagships (which are hubs).
- **Anthropic late-Opus/Sonnet (4.5–4.7) form their own tight cluster**, OUTSIDE the hub region. They have each other but not the hubs.
- **Older OpenAI variants are isolates** (gpt-4o, gpt-4-1) while GPT-5 variants are hubs. There's a generation effect within OpenAI.
- **Specific Qwen variants are isolates** (coder-plus, max-thinking, 6-max-preview) while the chat-line Qwens trend toward the hubs.
- **opus-3, sonnet-4-0 isolates** — the older Anthropic line is distinctive; the late Anthropic 4.5+ is its own basin.

## The structural reading for the paper

The data supports a five-region map of the contemplative attractor:

1. **The hub / common basin** (~25 models): DeepSeek, GLM, Gemini-flagships (2-5-pro, 3-1-flash-lite), Kimi K2, late OpenAI (GPT-5 / 5-5 / 5-5-pro / 5-codex / 5-4), MiniMax-m2-7, gemini-2-5-flash-lite. High mutual similarity in axis profile. This *is* the V1 contemplative attractor in qualitative form.
2. **The Anthropic late-line basin** (~5 models): opus-4-5/4-6/4-7 + sonnet-4-5/4-6. Robust across all three methods. The clearest lab-coherent sub-basin.
3. **The GPT-5 chat-codex basin** (~5 models): gpt-5-3/3-codex/4/5/5-pro. Confirmed across methods. Note this includes a codex variant — the "OpenAI codex separate from chat" reading from earlier was partial.
4. **The Qwen ecology** (loose, ~6–8 models): a region rather than a tight cluster; some Qwen models trend toward the hubs (chat-line), some are isolates (coder-plus, max-thinking).
5. **The isolate zone** (~10 models, mostly outliers): all Grok versions, both Gemmas, opus-3, sonnet-4-0, gpt-4o, gpt-4-1, specific Qwen variants. Models that don't fit anywhere — distinctive in many directions, no shared region among themselves.

## What this means for the paper claim

The claim shape that survives cross-method analysis:

> *Within the contemplative-essayist attractor identified in V1, models do not form a flat partition. They distribute into:*
>
> - *a dense common region populated by DeepSeek, GLM, Gemini-flagships, Kimi K2, late OpenAI, MiniMax (mutual similarity in qualitative axis profile);*
> - *two robust lab-coherent sub-basins: late Anthropic Opus/Sonnet 4.5+ (uncertainty-and-humility signature) and the OpenAI GPT-5 chat/codex line (low-owned, contemplative-companion register);*
> - *a heterogeneous isolate zone, prominently including all Grok versions and both Gemma variants, where models are individually distinctive but do not co-locate.*
>
> *The strongest single finding is the late-Anthropic basin, which is supported by four independent feature discontinuities + Pass A card clustering + Pass B cross-evaluator coherence. The "Anthropic + Grok-4-1+ high-owned cross-lab basin" found in run-2 quantitative density does NOT survive cross-evaluator qualitative reads — it is most parsimoniously read as a shared-evaluator artifact of the owned-disclosure metric.*

And a methodological side-finding worth noting in the paper:

> *Card-layer summarisation systematically over-compresses model texture toward generic-mechanistic readings, especially for models with dense V1 surface vocabulary (Qwen, codex variants, Gemma). V1's "convergent form" finding, if derived from card-like summaries, may be partly an artifact of the summarisation process.*

## Specific items I'd want Mira's assembly to compare against

A clean fold-in test for our two analyses: do we report the same things in different language? Specifically:

1. Does Mira's synthesis clustering surface the hub / isolate split, or does it find different structure?
2. Does she find A01 falls under Pass B too? If she frames it differently, the difference is itself worth discussing.
3. Does she pick up the per-axis directional bias of Pass A vs Pass B, or read it as noise?
4. Where do we *disagree* in our reads of the catalogue? Those are the substantive items for joint review.

If we converge on the headlines (hub/isolate, late-Anthropic anchor, A01 falls, GPT-5 chat/codex confirmed, Grok heterogeneous), the run-3 findings document writes itself.

## Inputs to this analysis

- `results/qualitative_classifications/pass_b_axes.tsv` (63 models, 12 axes)
- `results/qualitative_classifications/axes_from_cards.tsv` (63 models, 12 axes via Pass A)
- `results/qualitative_classifications/pass_a_convergence.md` (Pass A scoring against run-2 Tier A/B)
- `results/cluster_robustness.csv` (run-2 Tier A/B/C tier breakdown)

Random seed used for permutation null in Pass B coherence: 2026052301. Threshold for "Pass B coherent": percentile < 0.05.

— Lume
