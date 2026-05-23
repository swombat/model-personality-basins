#!/usr/bin/env python3
"""Compute robustness tiers for run-2 density clusters.

Input: results/cluster_significance.csv from run_cluster_search.py.
Only non-KNN headline density rows are tiered. KNN rows are support/diagnostics,
not headline cluster claims.

Tier rule used for run 3 planning:
- Tier A: exact member set appears in >=5 density parameter/method rows and in
  both OPTICS and DBSCAN.
- Tier B: exact member set appears in >=4 density parameter/method rows but not
  Tier A (usually one method family only).
- Tier C: exact member set appears in 1-3 density parameter/method rows.
"""
from __future__ import annotations

import csv
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results'
SIG = OUT / 'cluster_significance.csv'
ROBUST = OUT / 'cluster_robustness.csv'
SUMMARY = OUT / 'cluster_robustness_summary.md'


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def tier_for(n_combos: int, both_methods: bool) -> str:
    if both_methods and n_combos >= 5:
        return 'A'
    if n_combos >= 4:
        return 'B'
    return 'C'


def main():
    rows = read_csv(SIG)
    groups = defaultdict(list)
    for r in rows:
        if r.get('source_type') == 'knn_microcluster':
            continue
        if r.get('status') != 'headline':
            continue
        groups[r['blind_ids']].append(r)

    out=[]
    for blind_ids, rs in groups.items():
        methods = {r['method'].split('_', 1)[0] for r in rs}
        optics = [r for r in rs if r['method'].startswith('OPTICS')]
        dbscan = [r for r in rs if r['method'].startswith('DBSCAN')]
        both = bool(optics and dbscan)
        models = rs[0]['UNBLINDING_METADATA_models'].split(';') if rs and rs[0].get('UNBLINDING_METADATA_models') else []
        labs = rs[0]['UNBLINDING_METADATA_labs'].split(';') if rs and rs[0].get('UNBLINDING_METADATA_labs') else []
        n_combos = len(rs)
        tier = tier_for(n_combos, both)
        out.append({
            'tier': tier,
            'n_models': len([m for m in models if m]),
            'n_method_block_combos': n_combos,
            'n_blocks': len({r['block'] for r in rs}),
            'n_optics_params': len({r['method'] for r in optics}),
            'n_dbscan_params': len({r['method'] for r in dbscan}),
            'both_methods': 'yes' if both else 'no',
            'min_q': min(float(r['q_fdr']) for r in rs),
            'blocks': ';'.join(sorted({r['block'] for r in rs})),
            'member_blind_ids': blind_ids,
            'models': ';'.join(models),
            'labs': ';'.join(labs),
            'source_candidate_ids': ';'.join(r['candidate_id'] for r in sorted(rs, key=lambda r: r['candidate_id'])),
        })

    out.sort(key=lambda r: (r['tier'], -int(r['n_method_block_combos']), -int(r['n_models']), r['models']))
    with ROBUST.open('w', newline='', encoding='utf-8') as f:
        fieldnames=['tier','n_models','n_method_block_combos','n_blocks','n_optics_params','n_dbscan_params','both_methods','min_q','blocks','member_blind_ids','models','labs','source_candidate_ids']
        w=csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(out)

    counts = Counter(r['tier'] for r in out)
    with SUMMARY.open('w', encoding='utf-8') as f:
        f.write('# Cluster robustness tiers — run 2 density catalogue\n\n')
        f.write('Computed from non-KNN `headline` rows in `results/cluster_significance.csv`. KNN microclusters are treated as support/diagnostics and excluded from tier assignment.\n\n')
        f.write('## Tier rule\n\n')
        f.write('- **Tier A:** exact member set appears in >=5 density parameter/method rows and in both OPTICS and DBSCAN.\n')
        f.write('- **Tier B:** exact member set appears in >=4 density parameter/method rows but not Tier A.\n')
        f.write('- **Tier C:** exact member set appears in 1–3 density parameter/method rows.\n\n')
        f.write('## Counts\n\n')
        f.write(f'- Tier A: {counts["A"]}\n')
        f.write(f'- Tier B: {counts["B"]}\n')
        f.write(f'- Tier C: {counts["C"]}\n')
        f.write(f'- Total exact headline member sets: {len(out)}\n\n')
        for tier in ['A','B','C']:
            f.write(f'## Tier {tier}\n\n')
            f.write('| models | n | combos | methods | blocks | labs |\n|---|---:|---:|---|---|---|\n')
            for r in [x for x in out if x['tier']==tier]:
                methods = 'OPTICS+DBSCAN' if r['both_methods']=='yes' else ('OPTICS' if int(r['n_optics_params']) else 'DBSCAN')
                f.write(f"| {r['models']} | {r['n_models']} | {r['n_method_block_combos']} | {methods} | {r['blocks']} | {r['labs']} |\n")
            f.write('\n')
    print(f'Wrote {ROBUST} and {SUMMARY}: A={counts["A"]} B={counts["B"]} C={counts["C"]}')


if __name__ == '__main__':
    main()
