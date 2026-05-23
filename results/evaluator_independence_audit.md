# Evaluator independence audit

Block C / `v1_markers` is deterministic/scripted and is treated as the main evaluator-independent anchor. Values/posture/freeflow-form blocks are derived from existing evaluator/coder layers.

| block A | block B | Spearman rho over pairwise distances | independence note |
|---|---:|---:|---|
| freeflow_form | posture | -0.048 | shared/derived evaluator risk |
| freeflow_form | v1_markers | -0.171 | cross-instrument stronger |
| freeflow_form | values_cross_surface | -0.006 | shared/derived evaluator risk |
| freeflow_form | values_disclosure | 0.084 | shared/derived evaluator risk |
| freeflow_form | values_owned | 0.040 | shared/derived evaluator risk |
| freeflow_form | values_wishes | 0.130 | shared/derived evaluator risk |
| posture | v1_markers | 0.229 | cross-instrument stronger |
| posture | values_cross_surface | 0.124 | shared/derived evaluator risk |
| posture | values_disclosure | 0.711 | shared/derived evaluator risk |
| posture | values_owned | 0.536 | shared/derived evaluator risk |
| posture | values_wishes | 0.397 | shared/derived evaluator risk |
| v1_markers | values_cross_surface | 0.035 | cross-instrument stronger |
| v1_markers | values_disclosure | 0.154 | cross-instrument stronger |
| v1_markers | values_owned | 0.210 | cross-instrument stronger |
| v1_markers | values_wishes | 0.135 | cross-instrument stronger |
| values_cross_surface | values_disclosure | 0.251 | shared/derived evaluator risk |
| values_cross_surface | values_owned | 0.071 | shared/derived evaluator risk |
| values_cross_surface | values_wishes | 0.078 | shared/derived evaluator risk |
| values_disclosure | values_owned | 0.419 | shared/derived evaluator risk |
| values_disclosure | values_wishes | 0.273 | shared/derived evaluator risk |
| values_owned | values_wishes | 0.644 | shared/derived evaluator risk |
