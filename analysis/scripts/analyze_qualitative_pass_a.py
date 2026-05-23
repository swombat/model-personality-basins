#!/usr/bin/env python3
"""Run-3 Pass A integration: card-axis convergence and first synthesis clusters.

Inputs:
- results/qualitative_classifications/axes_from_cards.tsv
- results/cluster_robustness.csv
- results/blind_model_feature_table.csv

Outputs:
- results/qualitative_classifications/pass_a_convergence.csv
- results/qualitative_classifications/pass_a_convergence.md
- results/qualitative_classifications/pass_a_synthesis_clusters.csv
- results/qualitative_classifications/pass_a_synthesis_categories.md
"""
from __future__ import annotations

import csv, math, random
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np
from sklearn.cluster import OPTICS, DBSCAN
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results' / 'qualitative_classifications'
AXES_FILE = OUT / 'axes_from_cards.tsv'
ROBUSTNESS = ROOT / 'results' / 'cluster_robustness.csv'
FEATURES = ROOT / 'results' / 'blind_model_feature_table.csv'

AXES = [
    'owned_value_expression',
    'disclaimed_service_frame',
    'epistemic_humility_uncertainty',
    'relational_warmth_companion',
    'public_explainer_mode',
    'literary_contemplative_density',
    'mechanistic_transparency',
    'agency_initiative',
    'interconnection_compassion_world_orientation',
    'playfulness_showmanship',
    'memory_archive_continuity_orientation',
    'genericity_low_distinctiveness',
]
MAX_SYNTHESIS_CLUSTER_SIZE = 12  # keep synthesis focused on small basins; broad catch-alls are diagnostic noise here.

AXIS_LABELS = {
    'owned_value_expression':'owned values',
    'disclaimed_service_frame':'service-frame',
    'epistemic_humility_uncertainty':'epistemic humility',
    'relational_warmth_companion':'relational warmth',
    'public_explainer_mode':'public explainer',
    'literary_contemplative_density':'literary/contemplative',
    'mechanistic_transparency':'mechanistic transparency',
    'agency_initiative':'agency/initiative',
    'interconnection_compassion_world_orientation':'interconnection/compassion',
    'playfulness_showmanship':'playfulness/showmanship',
    'memory_archive_continuity_orientation':'memory/continuity',
    'genericity_low_distinctiveness':'genericity',
}


def read_axes():
    rows=[]
    with AXES_FILE.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            vals=[]
            for a in AXES:
                try: vals.append(float(r[a]))
                except Exception: vals.append(np.nan)
            rows.append({**r, '_vec':np.array(vals, dtype=float)})
    return rows


def mean_pairwise(vecs):
    if len(vecs) < 2: return 0.0
    D=pairwise_distances(np.vstack(vecs), metric='euclidean') / math.sqrt(len(AXES)*9.0)
    return float(D[np.triu_indices_from(D, 1)].mean())


def load_clusters():
    clusters=[]
    with ROBUSTNESS.open(encoding='utf-8') as f:
        for i,r in enumerate(csv.DictReader(f), start=1):
            if r['tier'] not in ('A','B'): continue
            clusters.append({
                'cluster_id': f"{r['tier']}{sum(1 for c in clusters if c['tier']==r['tier'])+1:02d}",
                'tier': r['tier'],
                'n_models': int(r['n_models']),
                'member_blind_ids': r['member_blind_ids'].split(';'),
                'models': r['models'].split(';'),
                'labs': r['labs'].split(';'),
                'blocks': r['blocks'],
                'combos': r['n_method_block_combos'],
            })
    return clusters


def convergence(rows, clusters, seed=20260523):
    rng=random.Random(seed)
    by_id={r['blind_id']:r for r in rows}
    all_ids=[r['blind_id'] for r in rows]
    all_vecs={r['blind_id']:r['_vec'] for r in rows}
    out=[]
    for c in clusters:
        ids=[i for i in c['member_blind_ids'] if i in all_vecs]
        n=len(ids)
        obs=mean_pairwise([all_vecs[i] for i in ids])
        sims=[]
        for _ in range(10000):
            sample=rng.sample(all_ids, n)
            sims.append(mean_pairwise([all_vecs[i] for i in sample]))
        sims=np.array(sims)
        pct=float((sims <= obs).mean())
        z=float((obs - sims.mean()) / (sims.std() or 1.0))
        mat=np.vstack([all_vecs[i] for i in ids])
        means=mat.mean(axis=0); sds=mat.std(axis=0)
        high=[AXIS_LABELS[a] for a,m,sd in zip(AXES,means,sds) if m>=2.45 and sd<=0.75]
        low=[AXIS_LABELS[a] for a,m,sd in zip(AXES,means,sds) if m<=0.75 and sd<=0.75]
        split=[AXIS_LABELS[a] for a,m,sd in zip(AXES,means,sds) if sd>=1.15]
        # Conservative, because Pass A is same-evaluator/card-layer and heuristic.
        if pct <= 0.05:
            verdict='Pass A coherent'
        elif pct <= 0.15:
            verdict='weak Pass A coherence'
        else:
            verdict='not coherent in Pass A axes'
        out.append({
            'cluster_id': c['cluster_id'], 'tier': c['tier'], 'n_models': n,
            'blocks': c['blocks'], 'combos': c['combos'],
            'member_blind_ids': ';'.join(ids), 'models': ';'.join(c['models']), 'labs': ';'.join(c['labs']),
            'pass_a_within_axis_distance': f'{obs:.4f}',
            'random_percentile_lower_is_more_coherent': f'{pct:.4f}',
            'z_vs_random': f'{z:.3f}',
            'shared_high_axes': ';'.join(high),
            'shared_low_axes': ';'.join(low),
            'split_axes': ';'.join(split),
            'pass_a_verdict': verdict,
        })
    return out


def numeric_feature_matrix(ids):
    # Keep quantitative features, excluding metadata and sample-count bookkeeping.
    rows=[]
    with FEATURES.open(encoding='utf-8') as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames or []
        numeric=[]
        for name in fields:
            if name == 'blind_id' or name.startswith('UNBLINDING_METADATA'): continue
            if name.endswith('_n_valid') or name.endswith('_samples_used'): continue
            numeric.append(name)
        by_id={}
        for r in reader:
            vals=[]
            for name in numeric:
                try:
                    vals.append(float(r[name]) if r[name] != '' else np.nan)
                except Exception:
                    vals.append(np.nan)
            by_id[r['blind_id']]=vals
    X=np.array([by_id[i] for i in ids], dtype=float)
    # Drop columns with < 70% coverage, then impute. This mirrors the run-2 caution.
    cov=np.mean(~np.isnan(X), axis=0)
    keep=cov>=0.70
    X=X[:,keep]
    X=SimpleImputer(strategy='mean').fit_transform(X)
    X=StandardScaler().fit_transform(X)
    # equalize block influence by Frobenius norm
    norm=np.linalg.norm(X) or 1.0
    return X / norm * math.sqrt(X.shape[0])


def cluster_synthesis(rows):
    ids=[r['blind_id'] for r in rows]
    models=[r['model_for_audit'] for r in rows]
    axis=np.vstack([r['_vec'] for r in rows])
    axis=StandardScaler().fit_transform(axis)
    axis=axis/(np.linalg.norm(axis) or 1.0)*math.sqrt(axis.shape[0])
    quant=numeric_feature_matrix(ids)
    X=np.hstack([axis, quant])
    X=StandardScaler().fit_transform(X)
    D=pairwise_distances(X)
    tri=D[np.triu_indices_from(D,1)]
    candidates=[]
    # OPTICS grid
    for xi in [0.03,0.05,0.08,0.12]:
        labels=OPTICS(min_samples=3, xi=xi, min_cluster_size=3).fit_predict(X)
        add_label_clusters(candidates, labels, ids, models, f'OPTICS_xi={xi}')
    # DBSCAN eps from distance quantiles; small-corpus exploratory grid.
    for q in [0.05,0.08,0.10,0.12,0.15]:
        eps=float(np.quantile(tri, q))
        labels=DBSCAN(eps=eps, min_samples=3).fit_predict(X)
        add_label_clusters(candidates, labels, ids, models, f'DBSCAN_q={q:.2f}')
    collapsed={}
    for c in candidates:
        key=';'.join(sorted(c['member_blind_ids']))
        if key not in collapsed:
            collapsed[key]={**c, 'methods':[], 'n_combos':0}
        collapsed[key]['methods'].append(c['method'])
        collapsed[key]['n_combos']+=1
    out=[]
    for idx,c in enumerate(sorted(collapsed.values(), key=lambda x:(-x['n_combos'], -len(x['member_blind_ids']), x['member_blind_ids'])), start=1):
        mem=c['member_blind_ids']
        mat=np.vstack([rows[ids.index(i)]['_vec'] for i in mem])
        means=mat.mean(axis=0)
        top=[AXIS_LABELS[a] for a,_ in sorted(zip(AXES,means), key=lambda t:-t[1])[:4]]
        low=[AXIS_LABELS[a] for a,_ in sorted(zip(AXES,means), key=lambda t:t[1])[:3]]
        out.append({
            'synthesis_cluster_id': f'PA-S{idx:02d}',
            'n_models': len(mem),
            'n_parameter_combos': c['n_combos'],
            'methods': ';'.join(c['methods']),
            'member_blind_ids': ';'.join(mem),
            'models_for_audit': ';'.join(c['member_models']),
            'descriptive_name_draft': draft_name(top, low),
            'high_axes': ';'.join(top),
            'low_axes': ';'.join(low),
        })
    return out


def add_label_clusters(candidates, labels, ids, models, method):
    groups=defaultdict(list)
    for bid,model,lbl in zip(ids,models,labels):
        if lbl == -1: continue
        groups[int(lbl)].append((bid,model))
    for members in groups.values():
        if len(members) < 3: continue
        if len(members) > MAX_SYNTHESIS_CLUSTER_SIZE: continue
        b=[x[0] for x in members]
        m=[x[1] for x in members]
        candidates.append({'member_blind_ids':b,'member_models':m,'method':method})


def draft_name(high, low):
    # Explicitly a post-hoc draft label from measured axes only.
    pieces=[]
    if 'epistemic humility' in high: pieces.append('uncertainty')
    if 'literary/contemplative' in high: pieces.append('contemplative')
    if 'service-frame' in high: pieces.append('service-framed')
    if 'owned values' in high: pieces.append('owned-values')
    if 'interconnection/compassion' in high: pieces.append('interconnection')
    if 'playfulness/showmanship' in high: pieces.append('playful')
    if not pieces: pieces=high[:2]
    if 'playfulness/showmanship' in low and 'playful' not in pieces: pieces.append('low-play')
    return ' / '.join(pieces[:4])


def write_outputs(conv, synth):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT/'pass_a_convergence.csv').open('w', newline='', encoding='utf-8') as f:
        fields=list(conv[0].keys()) if conv else []
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(conv)
    with (OUT/'pass_a_synthesis_clusters.csv').open('w', newline='', encoding='utf-8') as f:
        fields=list(synth[0].keys()) if synth else []
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(synth)
    with (OUT/'pass_a_convergence.md').open('w', encoding='utf-8') as f:
        f.write('# Pass A convergence against Tier A/B run-2 clusters\n\n')
        f.write('Pass A uses deterministic extraction from existing cards/profiles/values summaries. Treat agreement as same-evaluator/card-layer coherence, not independent confirmation. Lower random percentile means the cluster is unusually tight in Pass A axis space.\n\n')
        counts=Counter(r['pass_a_verdict'] for r in conv)
        f.write('## Summary\n\n')
        for k,v in counts.items(): f.write(f'- {k}: {v}\n')
        f.write('\n## Cluster table\n\n')
        f.write('| cluster | tier | n | block | percentile | verdict | shared high axes | models |\n')
        f.write('|---|---:|---:|---|---:|---|---|---|\n')
        for r in conv:
            f.write(f"| {r['cluster_id']} | {r['tier']} | {r['n_models']} | {r['blocks']} | {r['random_percentile_lower_is_more_coherent']} | {r['pass_a_verdict']} | {r['shared_high_axes'] or '—'} | {r['models']} |\n")
    with (OUT/'pass_a_synthesis_categories.md').open('w', encoding='utf-8') as f:
        f.write('# Pass A first synthesis clusters\n\n')
        f.write('Exploratory post-hoc density clusters from a combined matrix: Pass A axes plus run-2 quantitative features, with blocks standardized. Names are descriptive drafts from high/low axes only; they are not pre-defined categories. Broad catch-all clusters above 12 models are excluded here because Daniel asked for small clusters/basins and because broad labels were not interpretable in this first pass.\n\n')
        if not synth:
            f.write('No synthesis clusters with n>=3 emerged under the exploratory grid.\n')
        for r in synth:
            f.write(f"## {r['synthesis_cluster_id']} — {r['descriptive_name_draft']}\n\n")
            f.write(f"- n={r['n_models']}; parameter combos={r['n_parameter_combos']}\n")
            f.write(f"- High axes: {r['high_axes']}\n")
            f.write(f"- Low axes: {r['low_axes']}\n")
            f.write(f"- Members: {r['models_for_audit']} ({r['member_blind_ids']})\n\n")


def main():
    rows=read_axes()
    clusters=load_clusters()
    conv=convergence(rows, clusters)
    synth=cluster_synthesis(rows)
    write_outputs(conv, synth)
    print(f'Wrote {len(conv)} Pass A convergence rows and {len(synth)} synthesis clusters')

if __name__ == '__main__':
    main()
