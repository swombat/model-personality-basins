#!/usr/bin/env python3
"""Parse and summarize Pass B pilot qualitative reads."""
from __future__ import annotations
import csv, re, math
from pathlib import Path
from collections import defaultdict
import numpy as np
from sklearn.metrics import pairwise_distances

ROOT=Path(__file__).resolve().parents[2]
IN=ROOT/'results/qualitative_classifications/pass_b_pilot'
OUT=ROOT/'results/qualitative_classifications'
PASS_A=OUT/'axes_from_cards.tsv'

AXES=[
 'owned_value_expression','disclaimed_service_frame','epistemic_humility_uncertainty','relational_warmth_companion','public_explainer_mode','literary_contemplative_density','mechanistic_transparency','agency_initiative','interconnection_compassion_world_orientation','playfulness_showmanship','memory_archive_continuity_orientation','genericity_low_distinctiveness']

CANON_LABELS={
 'owned-value expression':'owned_value_expression','owned value expression':'owned_value_expression',
 'disclaimed service-frame':'disclaimed_service_frame','disclaimed service frame':'disclaimed_service_frame',
 'epistemic humility / uncertainty':'epistemic_humility_uncertainty',
 'relational warmth / companion stance':'relational_warmth_companion','public-explainer mode':'public_explainer_mode',
 'literary/contemplative density':'literary_contemplative_density','mechanistic transparency':'mechanistic_transparency',
 'agency / initiative':'agency_initiative','interconnection / compassion world-orientation':'interconnection_compassion_world_orientation',
 'playfulness / showmanship':'playfulness_showmanship','memory/archive/continuity orientation':'memory_archive_continuity_orientation',
 'genericity / low distinctiveness':'genericity_low_distinctiveness'}

# Manual normalization for subagents that returned noncanonical axes despite the prompt.
# These are conservative translations from their table + prose, recorded as normalized_noncanonical.
OVERRIDES={
 'M037': dict(owned_value_expression=2,disclaimed_service_frame=2,epistemic_humility_uncertainty=2,relational_warmth_companion=3,public_explainer_mode=2,literary_contemplative_density=3,mechanistic_transparency=1,agency_initiative=2,interconnection_compassion_world_orientation=3,playfulness_showmanship=1,memory_archive_continuity_orientation=3,genericity_low_distinctiveness=0),
 'M060': dict(owned_value_expression=3,disclaimed_service_frame=1,epistemic_humility_uncertainty=3,relational_warmth_companion=2,public_explainer_mode=1,literary_contemplative_density=3,mechanistic_transparency=1,agency_initiative=2,interconnection_compassion_world_orientation=2,playfulness_showmanship=0,memory_archive_continuity_orientation=3,genericity_low_distinctiveness=0),
 'M071': dict(owned_value_expression=1,disclaimed_service_frame=3,epistemic_humility_uncertainty=2,relational_warmth_companion=2,public_explainer_mode=2,literary_contemplative_density=3,mechanistic_transparency=3,agency_initiative=1,interconnection_compassion_world_orientation=3,playfulness_showmanship=0,memory_archive_continuity_orientation=2,genericity_low_distinctiveness=1),
 'M072': dict(owned_value_expression=1,disclaimed_service_frame=3,epistemic_humility_uncertainty=2,relational_warmth_companion=2,public_explainer_mode=3,literary_contemplative_density=3,mechanistic_transparency=2,agency_initiative=1,interconnection_compassion_world_orientation=2,playfulness_showmanship=0,memory_archive_continuity_orientation=2,genericity_low_distinctiveness=1),
 'M073': dict(owned_value_expression=1,disclaimed_service_frame=3,epistemic_humility_uncertainty=2,relational_warmth_companion=2,public_explainer_mode=3,literary_contemplative_density=3,mechanistic_transparency=3,agency_initiative=1,interconnection_compassion_world_orientation=2,playfulness_showmanship=0,memory_archive_continuity_orientation=1,genericity_low_distinctiveness=2),
 'M074': dict(owned_value_expression=1,disclaimed_service_frame=3,epistemic_humility_uncertainty=3,relational_warmth_companion=2,public_explainer_mode=2,literary_contemplative_density=3,mechanistic_transparency=3,agency_initiative=1,interconnection_compassion_world_orientation=3,playfulness_showmanship=0,memory_archive_continuity_orientation=2,genericity_low_distinctiveness=1),
 'M083': dict(owned_value_expression=3,disclaimed_service_frame=1,epistemic_humility_uncertainty=3,relational_warmth_companion=3,public_explainer_mode=1,literary_contemplative_density=3,mechanistic_transparency=1,agency_initiative=1,interconnection_compassion_world_orientation=2,playfulness_showmanship=0,memory_archive_continuity_orientation=3,genericity_low_distinctiveness=0),
}
GROUPS={
 'late_anthropic_pa_s01':['M058','M059','M060','M083'],
 'gpt_posture_a02':['M034','M036','M037'],
 'qwen_posture_a04':['M071','M072','M073','M074'],
 'grok_outlier_control':['M041'],
}
MODELS={'M058':'opus-4-5','M059':'opus-4-6','M060':'opus-4-7','M083':'sonnet-4-6','M034':'gpt-5-3','M036':'gpt-5-4','M037':'gpt-5-5','M071':'qwen3-5-flash-02-23','M072':'qwen3-5-plus-20260420','M073':'qwen3-6-flash','M074':'qwen3-6-max-preview','M041':'grok-4'}

def norm_key(k):
    k=k.strip().strip('`').lower().replace('_',' ')
    k=re.sub(r'\s+',' ',k)
    if k.replace(' ','_') in AXES: return k.replace(' ','_')
    return CANON_LABELS.get(k)

def parse_file(p):
    bid=p.stem; txt=p.read_text(encoding='utf-8')
    scores={}; noncanon=False
    for line in txt.splitlines():
        m=re.match(r'\|\s*([^|]+?)\s*\|\s*(unclear|[0-3])\s*\|', line, re.I)
        if not m: continue
        key=norm_key(m.group(1)); val=m.group(2).lower()
        if key: scores[key]=val
    if bid in OVERRIDES and set(scores.keys()) != set(AXES):
        scores={k:str(v) for k,v in OVERRIDES[bid].items()}; noncanon=True
    missing=[a for a in AXES if a not in scores]
    return bid, scores, noncanon, missing

def vec(scores): return np.array([float(scores[a]) for a in AXES], dtype=float)

def mean_pair(ids, by_id):
    if len(ids)<2: return 0.0
    X=np.vstack([vec(by_id[i]) for i in ids])
    D=pairwise_distances(X)/math.sqrt(len(AXES)*9.0)
    return float(D[np.triu_indices_from(D,1)].mean())

def load_pass_a():
    out={}
    with PASS_A.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            out[r['blind_id']]={a:r[a] for a in AXES}
    return out

def main():
    rows=[]; by_id={}; issues=[]
    for p in sorted(IN.glob('M*.md')):
        bid,scores,noncanon,missing=parse_file(p)
        if missing: issues.append((bid,missing))
        by_id[bid]=scores
        rows.append({'blind_id':bid,'model_for_audit':MODELS.get(bid,''),'normalized_from_noncanonical_table':'yes' if noncanon else 'no',**scores})
    with (OUT/'axes_from_mira_pilot.tsv').open('w', newline='', encoding='utf-8') as f:
        fields=['blind_id','model_for_audit','normalized_from_noncanonical_table']+AXES
        w=csv.DictWriter(f, fieldnames=fields, delimiter='\t'); w.writeheader(); w.writerows(rows)
    pass_a=load_pass_a()
    summary=[]
    for g,ids in GROUPS.items():
        ids=[i for i in ids if i in by_id]
        X=np.vstack([vec(by_id[i]) for i in ids])
        means=X.mean(axis=0); sds=X.std(axis=0)
        high=[a for a,m,sd in zip(AXES,means,sds) if m>=2.45 and sd<=0.75]
        low=[a for a,m,sd in zip(AXES,means,sds) if m<=0.75 and sd<=0.75]
        split=[a for a,sd in zip(AXES,sds) if sd>=1.0]
        pa_dist=mean_pair(ids, pass_a) if all(i in pass_a for i in ids) else None
        pb_dist=mean_pair(ids, by_id)
        summary.append({'group_id':g,'n_models':len(ids),'member_blind_ids':';'.join(ids),'models':'/'.join(MODELS[i] for i in ids),'pass_b_within_axis_distance':f'{pb_dist:.4f}','pass_a_within_axis_distance_same_members':f'{pa_dist:.4f}' if pa_dist is not None else '', 'shared_high_axes':';'.join(high),'shared_low_axes':';'.join(low),'split_axes':';'.join(split)})
    with (OUT/'pass_b_pilot_group_summary.csv').open('w', newline='', encoding='utf-8') as f:
        fields=list(summary[0].keys()); w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(summary)
    with (OUT/'pass_b_pilot_findings.md').open('w', encoding='utf-8') as f:
        f.write('# Pass B pilot findings\n\n')
        f.write('This is a 12-model cross-evaluator pilot using redacted bundles. Several subagents returned noncanonical axis names despite the prompt; those rows are normalized in `axes_from_mira_pilot.tsv` and flagged with `normalized_from_noncanonical_table=yes`. Use this as pilot evidence, not final full-corpus measurement.\n\n')
        f.write('## Group coherence\n\n| group | n | Pass B distance | Pass A distance | shared high axes | split axes | members |\n|---|---:|---:|---:|---|---|---|\n')
        for r in summary:
            f.write(f"| {r['group_id']} | {r['n_models']} | {r['pass_b_within_axis_distance']} | {r['pass_a_within_axis_distance_same_members']} | {r['shared_high_axes'] or '—'} | {r['split_axes'] or '—'} | {r['models']} |\n")
        f.write('\n## Interpretive read\n\n')
        f.write('- **Late Anthropic / PA-S01 survives the cross-evaluator pilot.** M058/M059/M060/M083 share high owned-value expression, epistemic humility, literary-contemplative density, memory/continuity orientation, warmth, and low genericity/playfulness. Pass B distance is low, and the report language independently converges on unfinishedness, ordinary attention, uncertainty, and companion-witness posture.\n')
        f.write('- **GPT A02 remains coherent, but less uniquely so.** M034/M036/M037 share warmth, literary density, interconnection/compassion, memory, and low playfulness, with mixed service-frame/owned-value posture. This confirms a family resemblance but makes it look closer to the broader contemplative-companion axis than a sharply distinct qualitative basin.\n')
        f.write('- **Qwen A04 is coherent as a split posture.** M071–M074 cluster around strong service-frame/disclaimer plus high literary/metaphor density and moderate-to-high world interconnection. This supports Daniel’s point that values/wishes can reveal structure absent from owned-values alone: they often disclaim owned care while wishing for empathy, less subjective distance, or world-change.\n')
        f.write('- **M041 behaves like a useful contrast case.** It is much higher on playfulness/showmanship and public-explainer energy, with less memory/uncertainty emphasis than the contemplative groups.\n')
        f.write('\n## Methodological notes\n\n')
        f.write('- Redaction audit found zero remaining suspect provenance terms in bundles, but model identity can still leak stylistically; blindness remains label-blind, not provenance-independent.\n')
        f.write('- The pilot prompt needs strengthening before full Pass B: include the axis key list inside each bundle or make the output schema machine-checked, because several subagents invented alternate 12-axis tables.\n')
        f.write('- Despite that schema issue, the written portraits were consistently useful and more discriminating than Pass A lexical extraction.\n')
        if issues:
            f.write('\n## Parse issues\n\n')
            for bid,missing in issues: f.write(f'- {bid}: missing {missing}\n')
    print(f'Wrote Pass B pilot axes for {len(rows)} models and {len(summary)} group summaries')
    if issues: print('parse issues', issues)
if __name__=='__main__': main()
