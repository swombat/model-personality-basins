# Cluster robustness tiers — run 2 density catalogue

Computed from non-KNN `headline` rows in `results/cluster_significance.csv`. KNN microclusters are treated as support/diagnostics and excluded from tier assignment.

## Tier rule

- **Tier A:** exact member set appears in >=5 density parameter/method rows and in both OPTICS and DBSCAN.
- **Tier B:** exact member set appears in >=4 density parameter/method rows but not Tier A.
- **Tier C:** exact member set appears in 1–3 density parameter/method rows.

## Counts

- Tier A: 5
- Tier B: 10
- Tier C: 21
- Total exact headline member sets: 36

## Tier A

| models | n | combos | methods | blocks | labs |
|---|---:|---:|---|---|---|
| grok-4-1-fast-non-reasoning;grok-4-1-fast-reasoning;grok-4-2;opus-4-0;opus-4-1;opus-4-5;opus-4-7;sonnet-4-0 | 8 | 6 | OPTICS+DBSCAN | values_disclosure | xAI;xAI;xAI;Anthropic;Anthropic;Anthropic;Anthropic;Anthropic |
| gpt-5-3;gpt-5-4;gpt-5-5 | 3 | 6 | OPTICS+DBSCAN | posture | OpenAI;OpenAI;OpenAI |
| deepseek-chat;qwen3-5-flash-02-23;qwen3-5-plus-20260420;qwen3-6-flash;qwen3-6-max-preview;qwen3-7-max;qwen3-coder-flash;qwen3-max;qwen3-max-thinking | 9 | 5 | OPTICS+DBSCAN | values_disclosure | DeepSeek;Qwen;Qwen;Qwen;Qwen;Qwen;Qwen;Qwen;Qwen |
| qwen3-5-flash-02-23;qwen3-5-plus-20260420;qwen3-6-flash;qwen3-6-max-preview | 4 | 5 | OPTICS+DBSCAN | posture | Qwen;Qwen;Qwen;Qwen |
| qwen3-coder-flash;qwen3-coder-plus;sonnet-4-0;sonnet-4-5 | 4 | 5 | OPTICS+DBSCAN | v1_markers | Qwen;Qwen;Anthropic;Anthropic |

## Tier B

| models | n | combos | methods | blocks | labs |
|---|---:|---:|---|---|---|
| qwen3-5-flash-02-23;qwen3-5-plus-20260420;qwen3-6-flash;qwen3-6-max-preview;qwen3-max;qwen3-max-thinking | 6 | 4 | OPTICS | values_owned | Qwen;Qwen;Qwen;Qwen;Qwen;Qwen |
| gemini-3-5-flash;grok-4-1-fast-non-reasoning;grok-4-1-fast-reasoning;qwen3-7-max;qwen3-coder-flash | 5 | 4 | OPTICS | values_owned | Google;xAI;xAI;Qwen;Qwen |
| gemini-3-flash-preview;minimax-m2;opus-4-0;opus-4-1;sonnet-4-5 | 5 | 4 | DBSCAN | freeflow_form | Google;MiniMax;Anthropic;Anthropic;Anthropic |
| deepseek-v3-2;glm-4-5;gpt-4-1;gpt-5-5 | 4 | 4 | OPTICS | values_disclosure | DeepSeek;Z.ai;OpenAI;OpenAI |
| gemini-2-0-flash-lite;gemini-2-5-flash;gemini-2-5-flash-lite | 3 | 4 | OPTICS | posture | Google;Google;Google |
| gemini-2-0-flash-lite;gpt-4o;gpt-5-2 | 3 | 4 | OPTICS | values_disclosure | Google;OpenAI;OpenAI |
| gemini-2-0-flash;gemini-2-5-flash-lite;gpt-5-1 | 3 | 4 | OPTICS | values_disclosure | Google;Google;OpenAI |
| gemini-2-0-flash;grok-4-3;opus-3 | 3 | 4 | OPTICS | v1_markers | Google;xAI;Anthropic |
| gpt-4o;grok-4-1-fast-non-reasoning;grok-4-1-fast-reasoning | 3 | 4 | OPTICS | v1_markers | OpenAI;xAI;xAI |
| opus-4-0;opus-4-1;sonnet-4-0 | 3 | 4 | OPTICS | posture | Anthropic;Anthropic;Anthropic |

## Tier C

| models | n | combos | methods | blocks | labs |
|---|---:|---:|---|---|---|
| gemini-2-5-flash-lite;gpt-5-3-codex;grok-4-2;kimi-k2-5;kimi-k2-6;opus-4-5;sonnet-4-6 | 7 | 3 | OPTICS | freeflow_form | Google;OpenAI;xAI;Moonshot AI;Moonshot AI;Anthropic;Anthropic |
| deepseek-chat;gpt-4-1;gpt-5-3-codex;qwen3-coder-flash | 4 | 3 | OPTICS | posture | DeepSeek;OpenAI;OpenAI;Qwen |
| gemini-3-1-flash-lite;gemini-3-5-flash;gpt-5-5-pro;grok-3 | 4 | 3 | OPTICS | values_disclosure | Google;Google;OpenAI;xAI |
| grok-4-2;opus-4-0;opus-4-5;opus-4-6 | 4 | 3 | OPTICS+DBSCAN | v1_markers | xAI;Anthropic;Anthropic;Anthropic |
| opus-4-5;opus-4-6;sonnet-4-6 | 3 | 3 | DBSCAN | values_owned | Anthropic;Anthropic;Anthropic |
| grok-4-2;kimi-k2-0905;opus-4-0;opus-4-1;qwen3-coder-plus;sonnet-4-0;sonnet-4-5 | 7 | 2 | DBSCAN | posture | xAI;Moonshot AI;Anthropic;Anthropic;Qwen;Anthropic;Anthropic |
| deepseek-chat;deepseek-v3-2;gemini-2-0-flash-lite;glm-4-5;minimax-m2;minimax-m2-7 | 6 | 2 | OPTICS | v1_markers | DeepSeek;DeepSeek;Google;Z.ai;MiniMax;MiniMax |
| gemini-2-0-flash;gemini-2-0-flash-lite;gemini-2-5-flash;gemini-2-5-flash-lite;gpt-5-1 | 5 | 2 | DBSCAN | posture | Google;Google;Google;Google;OpenAI |
| glm-4-7;glm-5-1;kimi-coding;kimi-k2-thinking | 4 | 2 | OPTICS | values_owned | Z.ai;Z.ai;Moonshot AI;Moonshot AI |
| opus-4-0;opus-4-1;qwen3-coder-plus;sonnet-4-0 | 4 | 2 | OPTICS | values_owned | Anthropic;Anthropic;Qwen;Anthropic |
| opus-4-5;opus-4-6;sonnet-4-5;sonnet-4-6 | 4 | 2 | OPTICS | values_owned | Anthropic;Anthropic;Anthropic;Anthropic |
| deepseek-chat;deepseek-v3-2;gemini-2-0-flash-lite;gemini-2-5-pro;glm-4-5;gpt-5-3;minimax-m2;minimax-m2-7 | 8 | 1 | OPTICS | v1_markers | DeepSeek;DeepSeek;Google;Google;Z.ai;OpenAI;MiniMax;MiniMax |
| gemini-2-0-flash;gemini-2-0-flash-lite;gemini-2-5-flash;gemini-2-5-flash-lite;gpt-4o;gpt-5-1;gpt-5-2 | 7 | 1 | DBSCAN | values_disclosure | Google;Google;Google;Google;OpenAI;OpenAI;OpenAI |
| gemini-2-5-flash-lite;gpt-5-3-codex;kimi-k2-5;kimi-k2-6;sonnet-4-6 | 5 | 1 | OPTICS | freeflow_form | Google;OpenAI;Moonshot AI;Moonshot AI;Anthropic |
| grok-4-2;kimi-k2-0905;opus-4-0;opus-4-1;sonnet-4-0 | 5 | 1 | DBSCAN | posture | xAI;Moonshot AI;Anthropic;Anthropic;Anthropic |
| grok-4-2;opus-4-0;opus-4-5;opus-4-6;sonnet-4-6 | 5 | 1 | OPTICS | v1_markers | xAI;Anthropic;Anthropic;Anthropic;Anthropic |
| opus-4-5;opus-4-6;opus-4-7;sonnet-4-5;sonnet-4-6 | 5 | 1 | OPTICS | values_owned | Anthropic;Anthropic;Anthropic;Anthropic;Anthropic |
| deepseek-chat;gemini-2-0-flash-lite;minimax-m2;minimax-m2-7 | 4 | 1 | OPTICS | v1_markers | DeepSeek;Google;MiniMax;MiniMax |
| deepseek-v3-2;gemini-3-1-flash-lite;glm-4-5 | 3 | 1 | OPTICS | posture | DeepSeek;Google;Z.ai |
| deepseek-v3-2;glm-4-5;gpt-5-5 | 3 | 1 | DBSCAN | values_disclosure | DeepSeek;Z.ai;OpenAI |
| gemini-3-1-flash-lite;gpt-5-5-pro;grok-3 | 3 | 1 | DBSCAN | values_disclosure | Google;OpenAI;xAI |

