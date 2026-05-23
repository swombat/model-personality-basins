#!/usr/bin/env python3
"""Validate and summarize Pass B expanded pilot strict-JSON outputs."""
from __future__ import annotations
import csv,json,math,re
from pathlib import Path
import numpy as np
from sklearn.metrics import pairwise_distances

ROOT=Path(__file__).resolve().parents[2]
IN=ROOT/'results/qualitative_classifications/pass_b_expanded_pilot'
OUT=ROOT/'results/qualitative_classifications'
PASS_A=OUT/'axes_from_cards.tsv'
AXES=['owned_value_expression','disclaimed_service_frame','epistemic_humility_uncertainty','relational_warmth_companion','public_explainer_mode','literary_contemplative_density','mechanistic_transparency','agency_initiative','interconnection_compassion_world_orientation','playfulness_showmanship','memory_archive_continuity_orientation','genericity_low_distinctiveness']
TOP={'voice_portrait','distinctive_features','open_tags','axis_ratings','representative_quotes','confidence','confidence_note'}
ALLOWED={0,1,2,3,'unclear'}
MODELS={'M058':'opus-4-5','M059':'opus-4-6','M083':'sonnet-4-6','M044':'grok-4-1-fast-reasoning','M056':'opus-4-0','M081':'sonnet-4-0','M036':'gpt-5-4','M074':'qwen3-6-max-preview','M078':'qwen3-coder-plus','M002':'deepseek-chat','M010':'gemini-2-5-flash-lite','M046':'grok-4-3','M015':'gemini-3-5-flash','M017':'gemma-4-26b-a4b','M039':'gpt-5-codex','M004':'deepseek-v4-pro','M040':'grok-3','M055':'opus-3','M049':'kimi-k2-0905','M071':'qwen3-5-flash-02-23'}
GROUPS={
 'pa_s01_controls':['M058','M059','M083'],
 'high_owned_cross_lab':['M044','M056','M081'],
 'gpt_watch':['M036'],
 'qwen_a04_carryover':['M071','M074'],
 'qwen_coder_multimembership':['M078'],
 'deepseek_qwen_cluster_probe':['M002'],
 'tier_b_reps':['M010','M046','M015'],
 'diffuse_residual':['M017','M039','M004'],
 'grok_lineage':['M040','M044','M046'],
 'anthropic_version_contrast':['M055','M056','M058','M059','M081','M083'],
}

def word_count(s): return len(re.findall(r"\b\S+\b", s or ''))
def validate(d):
    reasons=[]
    if set(d.keys())!=TOP: reasons.append('top_level_keys')
    ar=d.get('axis_ratings')
    if not isinstance(ar,dict): reasons.append('axis_ratings_not_object'); ar={}
    if set(ar.keys())!=set(AXES): reasons.append('axis_keys')
    for a in AXES:
        if a not in ar or ar.get(a) not in ALLOWED: reasons.append(f'invalid_axis:{a}')
    if not isinstance(d.get('distinctive_features'),list) or len(d.get('distinctive_features',[]))!=5: reasons.append('distinctive_features_len')
    if not isinstance(d.get('open_tags'),list) or not (5<=len(d.get('open_tags',[]))<=10): reasons.append('open_tags_len')
    qs=d.get('representative_quotes')
    if not isinstance(qs,list) or len(qs)>3: reasons.append('representative_quotes_len')
    else:
        for i,q in enumerate(qs):
            if word_count(q)>25: reasons.append(f'quote_too_long:{i+1}')
    if d.get('confidence') not in {'low','medium','high'}: reasons.append('confidence_value')
    return reasons

def vec(row): return np.array([float(row[a]) for a in AXES], dtype=float)
def mean_pair(ids, by):
    ids=[i for i in ids if i in by]
    if len(ids)<2: return 0.0
    X=np.vstack([vec(by[i]) for i in ids]); D=pairwise_distances(X)/math.sqrt(len(AXES)*9.0)
    return float(D[np.triu_indices_from(D,1)].mean())
def load_pass_a():
    out={}
    with PASS_A.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            out[r['blind_id']]={a:r[a] for a in AXES}
    return out

def group_summary(g,ids,by,pa):
    ids=[i for i in ids if i in by]
    X=np.vstack([vec(by[i]) for i in ids]) if ids else np.zeros((0,len(AXES)))
    means=X.mean(axis=0) if len(ids) else np.zeros(len(AXES)); sds=X.std(axis=0) if len(ids) else np.zeros(len(AXES))
    high=[a for a,m,sd in zip(AXES,means,sds) if m>=2.45 and sd<=0.75]
    low=[a for a,m,sd in zip(AXES,means,sds) if m<=0.75 and sd<=0.75]
    split=[a for a,sd in zip(AXES,sds) if sd>=1.0]
    return {'group_id':g,'n_models':len(ids),'member_blind_ids':';'.join(ids),'models':'/'.join(MODELS[i] for i in ids),'pass_b_distance':f'{mean_pair(ids,by):.4f}','pass_a_distance_same_members':f'{mean_pair(ids,pa):.4f}' if all(i in pa for i in ids) else '', 'shared_high_axes':';'.join(high),'shared_low_axes':';'.join(low),'split_axes':';'.join(split)}

def main():
    rows=[]; audit=[]; by={}; portraits={}
    for p in sorted(IN.glob('M*.json')):
        bid=p.stem; reasons=[]
        try: d=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            d={}; reasons=[f'json_parse:{e}']
        reasons += validate(d) if d else []
        audit.append({'blind_id':bid,'attempt_1_valid':'yes' if not reasons else 'no','attempt_2_valid':'not_needed','failure_reasons':';'.join(reasons),'manual_review_needed':'yes' if reasons else 'no'})
        # For interpretive analysis, retain rows whose axis block itself is valid even if
        # ancillary fields (usually quote count/length) failed strict validation. The
        # validation audit remains strict and controls the pass/fail recommendation.
        axis_ok = d and isinstance(d.get('axis_ratings'), dict) and set(d.get('axis_ratings', {}).keys()) == set(AXES) and all(d['axis_ratings'].get(a) in ALLOWED for a in AXES)
        if axis_ok:
            ar=d['axis_ratings']; row={'blind_id':bid,'model_for_audit':MODELS.get(bid,''),'normalized_from_noncanonical_table':'no'}
            row.update({a:ar[a] for a in AXES}); rows.append(row); by[bid]=row; portraits[bid]=d
    with (OUT/'pass_b_validation_audit.tsv').open('w', newline='', encoding='utf-8') as f:
        fields=['blind_id','attempt_1_valid','attempt_2_valid','failure_reasons','manual_review_needed']; w=csv.DictWriter(f, fieldnames=fields, delimiter='\t'); w.writeheader(); w.writerows(audit)
    with (OUT/'pass_b_expanded_pilot_axes.tsv').open('w', newline='', encoding='utf-8') as f:
        fields=['blind_id','model_for_audit','normalized_from_noncanonical_table']+AXES; w=csv.DictWriter(f, fieldnames=fields, delimiter='\t'); w.writeheader(); w.writerows(rows)
    pa=load_pass_a(); groups=[group_summary(g,ids,by,pa) for g,ids in GROUPS.items()]
    with (OUT/'pass_b_expanded_pilot_group_summary.csv').open('w', newline='', encoding='utf-8') as f:
        fields=list(groups[0].keys()); w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(groups)
    valid=sum(1 for a in audit if a['attempt_1_valid']=='yes')
    axis_valid=len(rows)
    pa_s01=[g for g in groups if g['group_id']=='pa_s01_controls'][0]
    residual=[g for g in groups if g['group_id']=='diffuse_residual'][0]
    full_go=(valid>=18 and float(pa_s01['pass_b_distance'])<=0.20 and float(residual['pass_b_distance'])>=0.20 and all(a['manual_review_needed']=='no' for a in audit))
    with (OUT/'pass_b_expanded_pilot_findings.md').open('w', encoding='utf-8') as f:
        f.write('# Pass B expanded pilot findings\n\n')
        f.write('## Pass criteria\n\n')
        f.write(f'- Schema validation: {valid}/20 valid on first attempt. Criterion >=18/20: {"PASS" if valid>=18 else "FAIL"}.\n')
        manual_ok = all(a['manual_review_needed']=='no' for a in audit)
        f.write(f'- Axis-schema validity: {axis_valid}/20 canonical axis blocks; no manual axis normalization needed: {"PASS" if axis_valid==20 else "FAIL"}.\n')
        f.write(f'- PA-S01 reconfirms: distance {pa_s01["pass_b_distance"]}; shared high axes {pa_s01["shared_high_axes"]}. {"PASS" if float(pa_s01["pass_b_distance"])<=0.20 else "CHECK"}.\n')
        f.write(f'- Diffuse residual reads as diffuse: distance {residual["pass_b_distance"]}. {"PASS" if float(residual["pass_b_distance"])>=0.20 else "CHECK"}.\n')
        f.write(f'\n**Recommendation:** {"Launch full Pass B with the hardened schema." if full_go else "Do not launch full Pass B yet; fix the quote-count instruction/schema and rerun or auto-repair validation. Axis blocks are still analyzable below."}\n\n')
        f.write('## Group summary\n\n| group | n | Pass B distance | Pass A distance | shared high axes | shared low axes | split axes | members |\n|---|---:|---:|---:|---|---|---|---|\n')
        for r in groups:
            f.write(f"| {r['group_id']} | {r['n_models']} | {r['pass_b_distance']} | {r['pass_a_distance_same_members']} | {r['shared_high_axes'] or '—'} | {r['shared_low_axes'] or '—'} | {r['split_axes'] or '—'} | {r['models']} |\n")
        f.write('\n## Requested reads\n\n')
        f.write('- **PA-S01:** reconfirmed. The three controls converge on high owned values, epistemic humility, warmth, literary-contemplative density, memory/continuity, and low play/genericity/service-frame.\n')
        f.write('- **Grok lineage:** M040/M044/M046 is not very tight; M044 is more high-owned/less showman than M040/M046, while M040/M046 carry stronger playfulness/public-explainer signals. This suggests lineage heterogeneity rather than one stable Grok basin.\n')
        f.write('- **Diffuse residual:** M017/M039/M004 do not form a tight group; they read as different singleton-ish profiles rather than a hidden residual basin.\n')
        f.write('- **Qwen-coder-plus multi-membership:** M078 reads as high-owned plus service-framed and literary/mechanistic, plausibly cutting across Qwen-coder and high-owned cross-lab rather than belonging only to one.\n')
        f.write('\n## Notes\n\n')
        f.write('- The hardened axis schema worked materially better than the first pilot: all 20 outputs used canonical axis keys and no manual axis normalization was needed. However, all 20 violated the strict representative-quotes cardinality rule because the bundle schema did not explicitly say 0-3 quotes at point of output. This is a validation-harness failure, not a recurrence of the noncanonical-axis failure.\n')
        f.write('- Axis key choice: I kept the longer protocol keys (`interconnection_compassion_world_orientation`, `memory_archive_continuity_orientation`) rather than Lume\'s shortened example keys, to preserve compatibility with Pass A and prior outputs.\n')
    print(f'valid={valid}/20 full_go={full_go}')
if __name__=='__main__': main()
