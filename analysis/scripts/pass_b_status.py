#!/usr/bin/env python3
"""Print Pass B completion status for watchdog checks."""
from __future__ import annotations
import csv, json, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/'results/blind_model_feature_table.csv'
PASS_B=ROOT/'results/qualitative_classifications/pass_b'
ids=[]
with FEATURES.open() as f:
    for r in csv.DictReader(f):
        try: n=float(r.get('C_v1_marker_samples_used') or 0)
        except Exception: n=0
        if n>=50:
            ids.append((r['blind_id'], r['UNBLINDING_METADATA_model']))
done=[]; invalid=[]; missing=[]
for bid,model in ids:
    p=PASS_B/f'{bid}.json'
    if not p.exists():
        missing.append((bid,model)); continue
    done.append((bid,model))
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        invalid.append((bid,model,str(e)))
print(f'Pass B outputs: {len(done)}/{len(ids)} present')
print(f'Missing {len(missing)}: ' + ', '.join(f'{b}:{m}' for b,m in missing))
if invalid:
    print(f'Invalid JSON {len(invalid)}: ' + ', '.join(f'{b}:{m}' for b,m,_ in invalid))
else:
    print('Invalid JSON 0')
