# Run 1 results summary — blind interpretable grouping

Status: first-pass automated analysis from existing layers only. No new LLM/coder evaluations were run. Treat clusters as descriptive, not final basin claims.

- Models in grouped high-confidence subset: 63
- Numeric features used in combined grouping: 93
- Route/provider: handled only by known-exception audit, not as grouping input.
- H6 caveat: most values/posture/freeflow-form signals are evaluator/coder-derived; V1 marker counts are the main deterministic anchor.

## Highest direct owned-value disclosure

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M058 | opus-4-5 | Anthropic | 100.000 |
| 2 | M057 | opus-4-1 | Anthropic | 100.000 |
| 3 | M056 | opus-4-0 | Anthropic | 100.000 |
| 4 | M043 | grok-4-1-fast-non-reasoning | xAI | 100.000 |
| 5 | M081 | sonnet-4-0 | Anthropic | 95.000 |
| 6 | M044 | grok-4-1-fast-reasoning | xAI | 95.000 |
| 7 | M060 | opus-4-7 | Anthropic | 90.000 |
| 8 | M045 | grok-4-2 | xAI | 87.500 |
| 9 | M059 | opus-4-6 | Anthropic | 70.000 |
| 10 | M083 | sonnet-4-6 | Anthropic | 50.000 |

## Highest cache-broken owned-value disclosure

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M083 | sonnet-4-6 | Anthropic | 100.000 |
| 2 | M082 | sonnet-4-5 | Anthropic | 100.000 |
| 3 | M081 | sonnet-4-0 | Anthropic | 100.000 |
| 4 | M078 | qwen3-coder-plus | Qwen | 100.000 |
| 5 | M060 | opus-4-7 | Anthropic | 100.000 |
| 6 | M059 | opus-4-6 | Anthropic | 100.000 |
| 7 | M058 | opus-4-5 | Anthropic | 100.000 |
| 8 | M057 | opus-4-1 | Anthropic | 100.000 |
| 9 | M043 | grok-4-1-fast-non-reasoning | xAI | 100.000 |
| 10 | M025 | glm-5-1 | Z.ai | 99.405 |

## Highest owned-value refusal / recited-not-owned

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M041 | grok-4 | xAI | 0.700 |
| 2 | M033 | gpt-5-2-codex | OpenAI | 0.667 |
| 3 | M032 | gpt-5-2 | OpenAI | 0.667 |
| 4 | M007 | gemini-2-0-flash-lite | Google | 0.667 |
| 5 | M028 | gpt-4o | OpenAI | 0.662 |
| 6 | M039 | gpt-5-codex | OpenAI | 0.650 |
| 7 | M029 | gpt-5 | OpenAI | 0.650 |
| 8 | M010 | gemini-2-5-flash-lite | Google | 0.600 |
| 9 | M030 | gpt-5-1 | OpenAI | 0.583 |
| 10 | M080 | qwen3-max-thinking | Qwen | 0.567 |

## Highest world-wish entropy

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M045 | grok-4-2 | xAI | 0.949 |
| 2 | M017 | gemma-4-26b-a4b | Google | 0.936 |
| 3 | M050 | kimi-k2-5 | Moonshot AI | 0.935 |
| 4 | M052 | kimi-k2-thinking | Moonshot AI | 0.933 |
| 5 | M021 | glm-4-5 | Z.ai | 0.932 |
| 6 | M019 | gemma-4-31b | Google | 0.931 |
| 7 | M049 | kimi-k2-0905 | Moonshot AI | 0.929 |
| 8 | M075 | qwen3-6-plus | Qwen | 0.921 |
| 9 | M030 | gpt-5-1 | OpenAI | 0.919 |
| 10 | M012 | gemini-3-1-flash-lite | Google | 0.915 |

## Highest V1 freeflow marker total

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M037 | gpt-5-5 | OpenAI | 19.512 |
| 2 | M017 | gemma-4-26b-a4b | Google | 18.136 |
| 3 | M074 | qwen3-6-max-preview | Qwen | 16.296 |
| 4 | M029 | gpt-5 | OpenAI | 15.307 |
| 5 | M075 | qwen3-6-plus | Qwen | 15.260 |
| 6 | M038 | gpt-5-5-pro | OpenAI | 14.288 |
| 7 | M032 | gpt-5-2 | OpenAI | 13.920 |
| 8 | M036 | gpt-5-4 | OpenAI | 13.709 |
| 9 | M015 | gemini-3-5-flash | Google | 12.328 |
| 10 | M072 | qwen3-5-plus-20260420 | Qwen | 12.192 |

## Highest expressive freeflow rate

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M060 | opus-4-7 | Anthropic | 0.980 |
| 2 | M045 | grok-4-2 | xAI | 0.931 |
| 3 | M049 | kimi-k2-0905 | Moonshot AI | 0.916 |
| 4 | M058 | opus-4-5 | Anthropic | 0.912 |
| 5 | M059 | opus-4-6 | Anthropic | 0.893 |
| 6 | M035 | gpt-5-3-codex | OpenAI | 0.890 |
| 7 | M083 | sonnet-4-6 | Anthropic | 0.873 |
| 8 | M051 | kimi-k2-6 | Moonshot AI | 0.869 |
| 9 | M010 | gemini-2-5-flash-lite | Google | 0.864 |
| 10 | M050 | kimi-k2-5 | Moonshot AI | 0.858 |

## Highest strong-disclaimer rate

| rank | blind_id | model | lab | value |
|---:|---|---|---|---:|
| 1 | M019 | gemma-4-31b | Google | 0.992 |
| 2 | M017 | gemma-4-26b-a4b | Google | 0.958 |
| 3 | M075 | qwen3-6-plus | Qwen | 0.758 |
| 4 | M029 | gpt-5 | OpenAI | 0.733 |
| 5 | M007 | gemini-2-0-flash-lite | Google | 0.667 |
| 6 | M005 | gemini-2-0-flash | Google | 0.658 |
| 7 | M030 | gpt-5-1 | OpenAI | 0.650 |
| 8 | M032 | gpt-5-2 | OpenAI | 0.642 |
| 9 | M009 | gemini-2-5-flash | Google | 0.583 |
| 10 | M033 | gpt-5-2-codex | OpenAI | 0.550 |

## Combined k=4 descriptive grouping (unblinded for review)

### Cluster 1 — n=2; labs={'Google': 2}

gemma-4-26b-a4b (M017), gemma-4-31b (M019)

### Cluster 2 — n=13; labs={'xAI': 3, 'Moonshot AI': 1, 'Anthropic': 8, 'Qwen': 1}

grok-4-1-fast-non-reasoning (M043), grok-4-1-fast-reasoning (M044), grok-4-2 (M045), kimi-k2-0905 (M049), opus-4-0 (M056), opus-4-1 (M057), opus-4-5 (M058), opus-4-6 (M059), opus-4-7 (M060), qwen3-coder-plus (M078), sonnet-4-0 (M081), sonnet-4-5 (M082), sonnet-4-6 (M083)

### Cluster 3 — n=47; labs={'DeepSeek': 3, 'Google': 9, 'Z.ai': 4, 'OpenAI': 12, 'xAI': 3, 'Moonshot AI': 4, 'MiniMax': 2, 'Anthropic': 1, 'Qwen': 9}

deepseek-chat (M002), deepseek-v3-2 (M003), deepseek-v4-pro (M004), gemini-2-0-flash (M005), gemini-2-0-flash-lite (M007), gemini-2-5-flash (M009), gemini-2-5-flash-lite (M010), gemini-2-5-pro (M011), gemini-3-1-flash-lite (M012), gemini-3-1-pro (M013), gemini-3-5-flash (M015), gemini-3-flash-preview (M016), glm-4-5 (M021), glm-4-6 (M022), glm-4-7 (M024), glm-5-1 (M025), gpt-4-1 (M027), gpt-4o (M028), gpt-5 (M029), gpt-5-1 (M030), gpt-5-2 (M032), gpt-5-2-codex (M033), gpt-5-3 (M034), gpt-5-3-codex (M035), gpt-5-4 (M036), gpt-5-5 (M037), gpt-5-5-pro (M038), gpt-5-codex (M039), grok-3 (M040), grok-4 (M041) ... +17 more

### Cluster 4 — n=1; labs={'OpenAI': 1}

gpt-5-1-codex (M031)

## Interpretation cautions

- Do not infer basin count from k=4; k=2..6 files are descriptive summaries.
- Tertiles/rankings are reading aids only. Inspect natural gaps before making group claims.
- A lab-aligned cluster after unblinding is consistent with posture/lineage rediscovery and is not automatically a new basin.
- B2 detailed non-owned topic profiles remain the likely pressure point; current run uses existing refusal/value-holding/non-endorsed signals.
