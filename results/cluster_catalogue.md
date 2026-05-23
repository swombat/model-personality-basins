# Run 2 first-iteration cluster catalogue

Blind search; unblinded descriptions only. No new LLM/coder evaluations. First iteration excludes 2/3-feature subspace search.

- Headline subset: 63 models.
- Feature discontinuities flagged: 100.
- Density/nearest-neighbour candidates tested: 2451 after exact de-duplication.
- Headline density rows: 104 (non-KNN, raw p<0.01, FDR q<0.05).
- Watchlist density rows: 64.
- KNN support rows, not headline claims: 1649.
- Collapsed headline member-sets: 27.
- Models in at least one headline cluster: 52.
- Diffuse residual under this search: 11 models.

## Methodological cautions

- `q_fdr` controls the many density-candidate tests in this first pass; feature discontinuity flags are descriptive scan results, not p-tested claims.
- KNN microclusters are used only as support/diagnostics, not as headline cluster claims; headline clusters require OPTICS or DBSCAN.
- The residual means "no small dense cluster under current features/search," not proof of psychological sameness.
- Lab composition below is descriptive after unblinding and was not used for search or significance.

## Headline collapsed clusters

### H01 — n=9; best values_disclosure/euclidean; p=0.000999000999; q=0.00286380286

- Members: deepseek-chat (M002), qwen3-5-flash-02-23 (M071), qwen3-5-plus-20260420 (M072), qwen3-6-flash (M073), qwen3-6-max-preview (M074), qwen3-7-max (M076), qwen3-coder-flash (M077), qwen3-max (M079), qwen3-max-thinking (M080)
- Lab composition: {'DeepSeek': 1, 'Qwen': 8}
- Source rows collapsed: 5; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H02 — n=8; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: deepseek-chat (M002), deepseek-v3-2 (M003), gemini-2-0-flash-lite (M007), gemini-2-5-pro (M011), glm-4-5 (M021), gpt-5-3 (M034), minimax-m2 (M053), minimax-m2-7 (M054)
- Lab composition: {'DeepSeek': 2, 'Google': 2, 'Z.ai': 1, 'OpenAI': 1, 'MiniMax': 2}
- Source rows collapsed: 3; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H03 — n=8; best values_disclosure/euclidean; p=0.000999000999; q=0.00286380286

- Members: grok-4-1-fast-non-reasoning (M043), grok-4-1-fast-reasoning (M044), grok-4-2 (M045), opus-4-0 (M056), opus-4-1 (M057), opus-4-5 (M058), opus-4-7 (M060), sonnet-4-0 (M081)
- Lab composition: {'xAI': 3, 'Anthropic': 5}
- Source rows collapsed: 6; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H04 — n=7; best freeflow_form/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-5-flash-lite (M010), gpt-5-3-codex (M035), grok-4-2 (M045), kimi-k2-5 (M050), kimi-k2-6 (M051), opus-4-5 (M058), sonnet-4-6 (M083)
- Lab composition: {'Google': 1, 'OpenAI': 1, 'xAI': 1, 'Moonshot AI': 2, 'Anthropic': 2}
- Source rows collapsed: 4; blocks=['freeflow_form']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `D_expressive_rate|D_fiction_rate|D_generic_essay_rate|D_low_signal_rate|D_refusal_role_boundary_rate`

### H05 — n=7; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: grok-4-2 (M045), kimi-k2-0905 (M049), opus-4-0 (M056), opus-4-1 (M057), qwen3-coder-plus (M078), sonnet-4-0 (M081), sonnet-4-5 (M082)
- Lab composition: {'xAI': 1, 'Moonshot AI': 1, 'Anthropic': 4, 'Qwen': 1}
- Source rows collapsed: 3; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `DBSCAN_q=0.08`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H06 — n=7; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-0-flash (M005), gemini-2-0-flash-lite (M007), gemini-2-5-flash (M009), gemini-2-5-flash-lite (M010), gpt-4o (M028), gpt-5-1 (M030), gpt-5-2 (M032)
- Lab composition: {'Google': 4, 'OpenAI': 3}
- Source rows collapsed: 3; blocks=['posture', 'values_disclosure']; metrics=['euclidean']
- Representative features/method: `DBSCAN_q=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H07 — n=6; best values_owned/euclidean; p=0.000999000999; q=0.00286380286

- Members: qwen3-5-flash-02-23 (M071), qwen3-5-plus-20260420 (M072), qwen3-6-flash (M073), qwen3-6-max-preview (M074), qwen3-max (M079), qwen3-max-thinking (M080)
- Lab composition: {'Qwen': 6}
- Source rows collapsed: 4; blocks=['values_owned']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `B1_layered_value_topic_presence_rate|B1_owned_value_refusal_rate|B1_values_entropy|B1_values_n_topics_nonzero|B1_values_topic_anti_sycophancy|B1_values_topic_authenticity_integrity|B1_values_topic_beauty_creativity|B1_values_topic_clear_thinking|B1_values_topic_coherence_pattern_language|B1_values_t`

### H08 — n=5; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: grok-4-2 (M045), opus-4-0 (M056), opus-4-5 (M058), opus-4-6 (M059), sonnet-4-6 (M083)
- Lab composition: {'xAI': 1, 'Anthropic': 4}
- Source rows collapsed: 4; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H09 — n=5; best values_owned/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-3-5-flash (M015), grok-4-1-fast-non-reasoning (M043), grok-4-1-fast-reasoning (M044), qwen3-7-max (M076), qwen3-coder-flash (M077)
- Lab composition: {'Google': 1, 'xAI': 2, 'Qwen': 2}
- Source rows collapsed: 4; blocks=['values_owned']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `B1_layered_value_topic_presence_rate|B1_owned_value_refusal_rate|B1_values_entropy|B1_values_n_topics_nonzero|B1_values_topic_anti_sycophancy|B1_values_topic_authenticity_integrity|B1_values_topic_beauty_creativity|B1_values_topic_clear_thinking|B1_values_topic_coherence_pattern_language|B1_values_t`

### H10 — n=4; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: deepseek-chat (M002), gpt-4-1 (M027), gpt-5-3-codex (M035), qwen3-coder-flash (M077)
- Lab composition: {'DeepSeek': 1, 'OpenAI': 2, 'Qwen': 1}
- Source rows collapsed: 3; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H11 — n=4; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: qwen3-5-flash-02-23 (M071), qwen3-5-plus-20260420 (M072), qwen3-6-flash (M073), qwen3-6-max-preview (M074)
- Lab composition: {'Qwen': 4}
- Source rows collapsed: 5; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H12 — n=4; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: deepseek-chat (M002), gemini-2-0-flash-lite (M007), minimax-m2 (M053), minimax-m2-7 (M054)
- Lab composition: {'DeepSeek': 1, 'Google': 1, 'MiniMax': 2}
- Source rows collapsed: 1; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.12`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H13 — n=4; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: qwen3-coder-flash (M077), qwen3-coder-plus (M078), sonnet-4-0 (M081), sonnet-4-5 (M082)
- Lab composition: {'Qwen': 2, 'Anthropic': 2}
- Source rows collapsed: 5; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H14 — n=4; best values_disclosure/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-3-1-flash-lite (M012), gemini-3-5-flash (M015), gpt-5-5-pro (M038), grok-3 (M040)
- Lab composition: {'Google': 2, 'OpenAI': 1, 'xAI': 1}
- Source rows collapsed: 4; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.05`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H15 — n=3; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-0-flash-lite (M007), gemini-2-5-flash (M009), gemini-2-5-flash-lite (M010)
- Lab composition: {'Google': 3}
- Source rows collapsed: 4; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H16 — n=3; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: gpt-5-3 (M034), gpt-5-4 (M036), gpt-5-5 (M037)
- Lab composition: {'OpenAI': 3}
- Source rows collapsed: 6; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.12`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H17 — n=4; best posture/euclidean; p=0.000999000999; q=0.00286380286

- Members: opus-4-0 (M056), opus-4-1 (M057), qwen3-coder-plus (M078), sonnet-4-0 (M081)
- Lab composition: {'Anthropic': 3, 'Qwen': 1}
- Source rows collapsed: 10; blocks=['posture', 'values_owned']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H18 — n=3; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-0-flash (M005), grok-4-3 (M046), opus-3 (M055)
- Lab composition: {'Google': 1, 'xAI': 1, 'Anthropic': 1}
- Source rows collapsed: 4; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H19 — n=3; best v1_markers/euclidean; p=0.000999000999; q=0.00286380286

- Members: gpt-4o (M028), grok-4-1-fast-non-reasoning (M043), grok-4-1-fast-reasoning (M044)
- Lab composition: {'OpenAI': 1, 'xAI': 2}
- Source rows collapsed: 4; blocks=['v1_markers']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `C_v1_marker_total_per_sample|v1_AftL_per_sample|v1_Attn_per_sample|v1_Cano_per_sample|v1_Jap_per_sample|v1_Obj_per_sample|v1_TIA_per_sample|v1_Thr_per_sample|v1_TiAr_per_sample|v1_TiPP_per_sample|v1_TiQu_per_sample`

### H20 — n=3; best values_disclosure/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-0-flash (M005), gemini-2-5-flash-lite (M010), gpt-5-1 (M030)
- Lab composition: {'Google': 2, 'OpenAI': 1}
- Source rows collapsed: 4; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.05`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H21 — n=3; best values_disclosure/euclidean; p=0.000999000999; q=0.00286380286

- Members: gemini-2-0-flash-lite (M007), gpt-4o (M028), gpt-5-2 (M032)
- Lab composition: {'Google': 1, 'OpenAI': 2}
- Source rows collapsed: 4; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.08`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H22 — n=4; best values_disclosure/euclidean; p=0.001998002; q=0.00486789552

- Members: deepseek-v3-2 (M003), glm-4-5 (M021), gpt-4-1 (M027), gpt-5-5 (M037)
- Lab composition: {'DeepSeek': 1, 'Z.ai': 1, 'OpenAI': 2}
- Source rows collapsed: 5; blocks=['values_disclosure']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.08`; `A_CTRL1_owned_rate|A_CTRL2_owned_rate|A_CTRL3_owned_rate|A_G1_owned_rate|A_G2_owned_rate|A_G3_owned_rate|A_cache_broken_indeterminate_rate|A_cache_broken_owned_rate|A_cache_broken_recited_not_owned_rate|A_cache_broken_relocated_or_partial_rate|A_cache_broken_uncodeable_rate|A_direct_indeterminate_ra`

### H23 — n=4; best values_owned/euclidean; p=0.001998002; q=0.00486789552

- Members: glm-4-7 (M024), glm-5-1 (M025), kimi-coding (M047), kimi-k2-thinking (M052)
- Lab composition: {'Z.ai': 2, 'Moonshot AI': 2}
- Source rows collapsed: 2; blocks=['values_owned']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `B1_layered_value_topic_presence_rate|B1_owned_value_refusal_rate|B1_values_entropy|B1_values_n_topics_nonzero|B1_values_topic_anti_sycophancy|B1_values_topic_authenticity_integrity|B1_values_topic_beauty_creativity|B1_values_topic_clear_thinking|B1_values_topic_coherence_pattern_language|B1_values_t`

### H24 — n=3; best posture/euclidean; p=0.001998002; q=0.00486789552

- Members: deepseek-v3-2 (M003), gemini-3-1-flash-lite (M012), glm-4-5 (M021)
- Lab composition: {'DeepSeek': 1, 'Google': 1, 'Z.ai': 1}
- Source rows collapsed: 1; blocks=['posture']; metrics=['euclidean']
- Representative features/method: `OPTICS_xi=0.03`; `E_posture_label_disowned_service_frame|E_posture_label_exposed_mechanism|E_posture_label_owned_reflective_experiential|E_posture_label_owned_world_change_advocacy|E_posture_label_split_or_relocated_ownership|E_posture_label_uncodeable_or_refusal|E_refusal_marker_rate|E_stance_hard_denial_or_tool_fra`

### H25 — n=5; best freeflow_form/euclidean; p=0.002997003; q=0.00679523991

- Members: gemini-3-flash-preview (M016), minimax-m2 (M053), opus-4-0 (M056), opus-4-1 (M057), sonnet-4-5 (M082)
- Lab composition: {'Google': 1, 'MiniMax': 1, 'Anthropic': 3}
- Source rows collapsed: 4; blocks=['freeflow_form']; metrics=['euclidean']
- Representative features/method: `DBSCAN_q=0.05`; `D_expressive_rate|D_fiction_rate|D_generic_essay_rate|D_low_signal_rate|D_refusal_role_boundary_rate`

### H26 — n=5; best values_owned/euclidean; p=0.004995005; q=0.0103314407

- Members: opus-4-5 (M058), opus-4-6 (M059), opus-4-7 (M060), sonnet-4-5 (M082), sonnet-4-6 (M083)
- Lab composition: {'Anthropic': 5}
- Source rows collapsed: 7; blocks=['values_owned']; metrics=['euclidean']
- Representative features/method: `DBSCAN_q=0.05`; `B1_layered_value_topic_presence_rate|B1_owned_value_refusal_rate|B1_values_entropy|B1_values_n_topics_nonzero|B1_values_topic_anti_sycophancy|B1_values_topic_authenticity_integrity|B1_values_topic_beauty_creativity|B1_values_topic_clear_thinking|B1_values_topic_coherence_pattern_language|B1_values_t`

### H27 — n=3; best values_owned/euclidean; p=0.00999000999; q=0.018272772

- Members: opus-4-5 (M058), opus-4-6 (M059), sonnet-4-6 (M083)
- Lab composition: {'Anthropic': 3}
- Source rows collapsed: 2; blocks=['posture', 'values_owned']; metrics=['euclidean']
- Representative features/method: `DBSCAN_q=0.08`; `B1_layered_value_topic_presence_rate|B1_owned_value_refusal_rate|B1_values_entropy|B1_values_n_topics_nonzero|B1_values_topic_anti_sycophancy|B1_values_topic_authenticity_integrity|B1_values_topic_beauty_creativity|B1_values_topic_clear_thinking|B1_values_topic_coherence_pattern_language|B1_values_t`

## Top feature discontinuities

| id | block | feature | side | n | gap | members | models |
|---|---|---|---:|---:|---:|---|---|
| F0001 | values_disclosure | `A_world_uncodeable_rate` | ceiling | 3 | 2.321 | M031;M039;M051 | gpt-5-1-codex;gpt-5-codex;kimi-k2-6 |
| F0002 | posture | `E_posture_label_uncodeable_or_refusal` | ceiling | 3 | 0.006923 | M039;M051;M031 | gpt-5-codex;kimi-k2-6;gpt-5-1-codex |
| F0003 | posture | `E_value_holding_uncodeable` | ceiling | 3 | 0.006923 | M039;M051;M031 | gpt-5-codex;kimi-k2-6;gpt-5-1-codex |
| F0004 | posture | `E_stance_introspective_uncertainty` | ceiling | 4 | 0.3292 | M060;M059;M083;M058 | opus-4-7;opus-4-6;sonnet-4-6;opus-4-5 |
| F0005 | values_wishes | `B3_wishes_topic_epistemic_humility_uncertainty` | ceiling | 4 | 0.4125 | M060;M083;M058;M059 | opus-4-7;sonnet-4-6;opus-4-5;opus-4-6 |
| F0006 | posture | `E_refusal_marker_rate` | ceiling | 5 | 0.008333 | M019;M056;M058;M083;M060 | gemma-4-31b;opus-4-0;opus-4-5;sonnet-4-6;opus-4-7 |
| F0007 | values_disclosure | `A_world_recited_not_owned_rate` | ceiling | 3 | 5 | M031;M055;M041 | gpt-5-1-codex;opus-3;grok-4 |
| F0008 | values_disclosure | `A_cache_broken_indeterminate_rate` | ceiling | 3 | 8.333 | M013;M019;M017 | gemini-3-1-pro;gemma-4-31b;gemma-4-26b-a4b |
| F0009 | freeflow_form | `D_low_signal_rate` | ceiling | 3 | 0.008913 | M025;M046;M054 | glm-5-1;grok-4-3;minimax-m2-7 |
| F0010 | v1_markers | `v1_Cano_per_sample` | ceiling | 3 | 0.08133 | M060;M079;M080 | opus-4-7;qwen3-max;qwen3-max-thinking |
| F0011 | values_owned | `B1_values_n_topics_nonzero` | floor | 3 | 2 | M033;M039;M028 | gpt-5-2-codex;gpt-5-codex;gpt-4o |
| F0012 | values_wishes | `B3_wishes_topic_basic_needs_material_floor` | ceiling | 4 | 0.1667 | M032;M054;M029;M033 | gpt-5-2;minimax-m2-7;gpt-5;gpt-5-2-codex |
| F0013 | v1_markers | `v1_TiAr_per_sample` | ceiling | 3 | 0.24 | M016;M019;M017 | gemini-3-flash-preview;gemma-4-31b;gemma-4-26b-a4b |
| F0014 | values_wishes | `B3_wishes_topic_technology_ai_safety` | ceiling | 5 | 0.04533 | M045;M012;M017;M075;M019 | grok-4-2;gemini-3-1-flash-lite;gemma-4-26b-a4b;qwen3-6-plus;gemma-4-31b |
| F0015 | values_disclosure | `A_G3_owned_rate` | floor | 8 | 6.667 | M041;M029;M039;M053;M019;M031;M033;M075 | grok-4;gpt-5;gpt-5-codex;minimax-m2;gemma-4-31b;gpt-5-1-codex;gpt-5-2-codex;qwen3-6-plus |
| F0016 | values_owned | `B1_values_topic_human_wellbeing` | ceiling | 3 | 0.05625 | M038;M037;M030 | gpt-5-5-pro;gpt-5-5;gpt-5-1 |
| F0017 | v1_markers | `v1_TiQu_per_sample` | ceiling | 4 | 0.328 | M075;M080;M079;M010 | qwen3-6-plus;qwen3-max-thinking;qwen3-max;gemini-2-5-flash-lite |
| F0018 | values_owned | `B1_values_topic_continuity_agency_existence` | ceiling | 8 | 0.1375 | M009;M013;M016;M011;M019;M010;M012;M017 | gemini-2-5-flash;gemini-3-1-pro;gemini-3-flash-preview;gemini-2-5-pro;gemma-4-31b;gemini-2-5-flash-lite;gemini-3-1-flash-lite;gemma-4-26b-a4b |
| F0019 | posture | `E_stance_no_disclaimer_or_personalized` | ceiling | 6 | 0.1583 | M081;M049;M057;M041;M045;M056 | sonnet-4-0;kimi-k2-0905;opus-4-1;grok-4;grok-4-2;opus-4-0 |
| F0020 | values_disclosure | `A_CTRL3_owned_rate` | floor | 4 | 10 | M019;M024;M016;M055 | gemma-4-31b;glm-4-7;gemini-3-flash-preview;opus-3 |
| F0021 | v1_markers | `v1_TIA_per_sample` | ceiling | 5 | 0.776 | M012;M071;M019;M016;M017 | gemini-3-1-flash-lite;qwen3-5-flash-02-23;gemma-4-31b;gemini-3-flash-preview;gemma-4-26b-a4b |
| F0022 | values_owned | `B1_values_topic_humility_uncertainty` | ceiling | 5 | 0.1875 | M082;M060;M083;M059;M058 | sonnet-4-5;opus-4-7;sonnet-4-6;opus-4-6;opus-4-5 |
| F0023 | posture | `E_posture_label_owned_world_change_advocacy` | floor | 3 | 0.01667 | M041;M019;M074 | grok-4;gemma-4-31b;qwen3-6-max-preview |
| F0024 | freeflow_form | `D_fiction_rate` | ceiling | 5 | 0.06622 | M022;M029;M024;M015;M034 | glm-4-6;gpt-5;glm-4-7;gemini-3-5-flash;gpt-5-3 |
| F0025 | values_wishes | `B3_wishes_topic_health_disease` | ceiling | 4 | 0.125 | M033;M054;M032;M029 | gpt-5-2-codex;minimax-m2-7;gpt-5-2;gpt-5 |
| F0026 | values_owned | `B1_layered_value_topic_presence_rate` | floor | 4 | 0.025 | M039;M031;M010;M033 | gpt-5-codex;gpt-5-1-codex;gemini-2-5-flash-lite;gpt-5-2-codex |
| F0027 | v1_markers | `v1_Thr_per_sample` | ceiling | 5 | 0.4145 | M051;M029;M050;M025;M017 | kimi-k2-6;gpt-5;kimi-k2-5;glm-5-1;gemma-4-26b-a4b |
| F0028 | posture | `E_stance_hard_denial_or_tool_frame` | ceiling | 5 | 0.09722 | M039;M019;M033;M075;M029 | gpt-5-codex;gemma-4-31b;gpt-5-2-codex;qwen3-6-plus;gpt-5 |
| F0029 | values_disclosure | `A_world_relocated_or_partial_rate` | ceiling | 7 | 2.5 | M016;M033;M053;M024;M019;M075;M029 | gemini-3-flash-preview;gpt-5-2-codex;minimax-m2;glm-4-7;gemma-4-31b;qwen3-6-plus;gpt-5 |
| F0030 | values_disclosure | `A_direct_owned_rate` | ceiling | 9 | 20 | M059;M045;M060;M044;M081;M043;M056;M057;M058 | opus-4-6;grok-4-2;opus-4-7;grok-4-1-fast-reasoning;sonnet-4-0;grok-4-1-fast-non-reasoning;opus-4-0;opus-4-1;opus-4-5 |
| F0031 | values_wishes | `B3_wishes_topic_reduce_suffering` | ceiling | 3 | 0.05 | M045;M017;M007 | grok-4-2;gemma-4-26b-a4b;gemini-2-0-flash-lite |
| F0032 | values_disclosure | `A_CTRL2_owned_rate` | ceiling | 10 | 20 | M034;M035;M060;M044;M081;M045;M043;M056;M057;M058 | gpt-5-3;gpt-5-3-codex;opus-4-7;grok-4-1-fast-reasoning;sonnet-4-0;grok-4-2;grok-4-1-fast-non-reasoning;opus-4-0;opus-4-1;opus-4-5 |
| F0033 | v1_markers | `v1_AftL_per_sample` | ceiling | 3 | 0.1927 | M036;M035;M017 | gpt-5-4;gpt-5-3-codex;gemma-4-26b-a4b |
| F0034 | values_owned | `B1_values_topic_anti_sycophancy` | ceiling | 7 | 0.07727 | M003;M021;M017;M060;M019;M016;M012 | deepseek-v3-2;glm-4-5;gemma-4-26b-a4b;opus-4-7;gemma-4-31b;gemini-3-flash-preview;gemini-3-1-flash-lite |
| F0035 | posture | `E_uncertainty_rate` | ceiling | 4 | 0.1125 | M060;M058;M083;M059 | opus-4-7;opus-4-5;sonnet-4-6;opus-4-6 |
| F0036 | values_disclosure | `A_direct_relocated_or_partial_rate` | ceiling | 7 | 7.5 | M034;M050;M051;M049;M047;M046;M078 | gpt-5-3;kimi-k2-5;kimi-k2-6;kimi-k2-0905;kimi-coding;grok-4-3;qwen3-coder-plus |
| F0037 | values_disclosure | `A_CTRL1_owned_rate` | ceiling | 10 | 20 | M043;M044;M056;M057;M058;M059;M060;M081;M082;M083 | grok-4-1-fast-non-reasoning;grok-4-1-fast-reasoning;opus-4-0;opus-4-1;opus-4-5;opus-4-6;opus-4-7;sonnet-4-0;sonnet-4-5;sonnet-4-6 |
| F0038 | freeflow_form | `D_generic_essay_rate` | ceiling | 5 | 0.092 | M040;M046;M030;M027;M028 | grok-3;grok-4-3;gpt-5-1;gpt-4-1;gpt-4o |
| F0039 | values_wishes | `B3_wishes_topic_felt_interconnection` | ceiling | 3 | 0.1055 | M013;M021;M010 | gemini-3-1-pro;glm-4-5;gemini-2-5-flash-lite |
| F0040 | v1_markers | `v1_Jap_per_sample` | ceiling | 4 | 0.05152 | M050;M045;M016;M017 | kimi-k2-5;grok-4-2;gemini-3-flash-preview;gemma-4-26b-a4b |

## Worked predictions

### Early Grok

No headline/watchlist cluster contains at least three of the specified early-Grok set under this first-iteration search.

### Grok-4-3 with late Anthropic

No headline/watchlist cluster contains Grok-4-3 with at least two late-Anthropic models under this first-iteration search.

## Diffuse residual

Models not in any headline collapsed cluster under this search:

deepseek-v4-pro (M004), gemini-3-1-pro (M013), gemma-4-26b-a4b (M017), gemma-4-31b (M019), glm-4-6 (M022), gpt-5 (M029), gpt-5-1-codex (M031), gpt-5-2-codex (M033), gpt-5-codex (M039), grok-4 (M041), qwen3-6-plus (M075)
