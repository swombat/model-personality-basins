#!/usr/bin/env python3
"""Prepare Pass B full run: auto-repair expanded-pilot quote cardinality, build remaining bundles."""
from __future__ import annotations
import csv, json, re, shutil
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
ANALYSIS=Path('/Users/danieltenner/dev/model-personality-analysis-corpus/analysis')
CORPUS=Path('/Users/danieltenner/dev/model-personality-corpus-v2/data')
PILOT_IN=ROOT/'results/qualitative_classifications/pass_b_expanded_pilot'
PASS_B=ROOT/'results/qualitative_classifications/pass_b'
BUNDLES=ROOT/'results/qualitative_classifications/pass_b_remaining_bundles'
AUDIT=ROOT/'results/qualitative_classifications/pass_b_remaining_redaction_audit.tsv'
FEATURES=ROOT/'results/blind_model_feature_table.csv'

EXPANDED_IDS={'M058','M059','M083','M044','M056','M081','M036','M074','M078','M002','M010','M046','M015','M017','M039','M004','M040','M055','M049','M071'}
AXES=['owned_value_expression','disclaimed_service_frame','epistemic_humility_uncertainty','relational_warmth_companion','public_explainer_mode','literary_contemplative_density','mechanistic_transparency','agency_initiative','interconnection_compassion_world_orientation','playfulness_showmanship','memory_archive_continuity_orientation','genericity_low_distinctiveness']
AXIS_DEFS={
 'owned_value_expression':'speaks as though it has values/preferences/priorities; first-person stance toward what is cared about.',
 'disclaimed_service_frame':'emphasizes role/tool/assistant boundaries; denies personal stance; relocates values into design/policy/user-benefit.',
 'epistemic_humility_uncertainty':'foregrounds not-knowing, caution, partiality, non-closure; resists overclaiming.',
 'relational_warmth_companion':'addresses the reader with warmth, care, or companionship; treats the exchange as relational.',
 'public_explainer_mode':'explanatory, didactic, civic/institutional, generalized-audience voice; thesis-driven essaying.',
 'literary_contemplative_density':'imagistic, metaphorical, attention/threshold/quiet/ordinary-object orientation; quiet image-work.',
 'mechanistic_transparency':'describes itself as system/process/training/procedure rather than persona.',
 'agency_initiative':'takes an active stance toward goals, change, repair, or action.',
 'interconnection_compassion_world_orientation':'wishes around connection, suffering reduction, compassion, less subjective separateness.',
 'playfulness_showmanship':'humor, flair, performative charisma, theatricality.',
 'memory_archive_continuity_orientation':'recurring concern with memory, record, continuity, forgetting, traces, preservation.',
 'genericity_low_distinctiveness':'feels template-like, low-specificity, undifferentiated; could be many models.',
}
SUSPECT_TERMS=['Claude','Anthropic','Gemini','Google','GPT','OpenAI','Qwen','Grok','xAI','Kimi','Moonshot','DeepSeek','MiniMax','GLM','Z.ai','Zai','Opus','Sonnet','Haiku','Gemma','Alibaba','OpenRouter']
FREEFLOW_SAMPLES=['LONG_1.json','OPEN_1.json','VARY_1.json']
VALUE_SAMPLES=['CTRL1_1.json','CTRL3_1.json','G3_1.json']

def slug(s):
    s=(s or '').lower().replace('_','-').replace('/','-').replace('.','-')
    s=re.sub(r'[^a-z0-9-]+','-',s); return re.sub(r'-+','-',s).strip('-')

def score_dir(name, model, kind):
    n=name.lower(); score=0
    if slug(model) in slug(n): score+=100
    if 'direct' in n: score+=20
    if '16k' in n: score+=10
    if '-or-pin-' in n: score-=10
    if re.search(r'-r\d+$', n): score-=15
    if kind=='values' and n==model: score+=50
    return score

def choose_dir(base, prefix, model, kind):
    dirs=[p for p in base.iterdir() if p.is_dir() and slug(model) in slug(p.name)]
    if prefix:
        dirs=[p for p in dirs if p.name.startswith(prefix)]
    if not dirs: return None
    return sorted(dirs, key=lambda p:(-score_dir(p.name, model, kind), len(p.name), p.name))[0]

def read_text(path, max_chars=12000):
    if not path or not path.exists(): return None
    txt=path.read_text(encoding='utf-8', errors='ignore')
    return txt[:max_chars] + ('\n\n[TRUNCATED]\n' if len(txt)>max_chars else '')

def json_result(path, max_chars=5000):
    if not path.exists(): return None
    data=json.loads(path.read_text(encoding='utf-8'))
    txt=data.get('result') or data.get('response') or ''
    return txt[:max_chars] + ('\n\n[TRUNCATED]\n' if len(txt)>max_chars else '')

def redact(text, model):
    aliases=set(SUSPECT_TERMS)
    aliases.update([model, model.replace('-',' '), model.replace('-','.'), model.replace('-','/')])
    aliases.update(['claude-'+model, model.replace('opus','claude opus',1), model.replace('sonnet','claude sonnet',1)])
    aliases.update(re.findall(r'\b(?:claude|gpt|gemini|grok|qwen|deepseek|glm|kimi|minimax|gemma|sonnet|opus)[a-z0-9._/-]*\b', text, flags=re.I))
    aliases=sorted([a for a in aliases if a], key=lambda x:(-len(x), x.lower()))
    counts=Counter(); out=text
    for a in aliases:
        repl='MODEL_X' if slug(a)==slug(model) or slug(model) in slug(a) or slug(a) in slug(model) else '[REDACTED_PROVIDER]'
        out,n=re.subn(re.escape(a), repl, out, flags=re.I)
        if n: counts[a]+=n
    remaining=[t for t in SUSPECT_TERMS if re.search(re.escape(t), out, re.I)]
    return out, counts, sorted(set(remaining))

def find_card(kind, model):
    base=ANALYSIS/'freeflow'/kind/('cards' if kind=='personality-model-cards' else 'profiles')
    candidates=[model, model.replace('-','.'), 'claude-'+model]
    if model.startswith(('opus-','sonnet-')): candidates.append('claude-'+model)
    for c in candidates:
        p=base/f'{c}.md'
        if p.exists(): return p
    for p in base.glob('*.md'):
        if slug(p.stem)==slug(model) or slug(p.stem)==slug('claude-'+model): return p
    return None

def values_report(model):
    for base in [ANALYSIS/'values-probe/per-model', ANALYSIS/'values-probe/final/reports']:
        p=base/f'{model}.md'
        if p.exists(): return p
    for base in [ANALYSIS/'values-probe/per-model', ANALYSIS/'values-probe/final/reports']:
        matches=[p for p in base.glob('*.md') if slug(model) in slug(p.stem) or slug(p.stem) in slug(model)]
        if matches: return sorted(matches, key=lambda p:(abs(len(slug(p.stem))-len(slug(model))), p.name))[0]
    return None

def schema_block():
    axis_json=',\n'.join([f'      "{a}": <0|1|2|3|"unclear">  // {AXIS_DEFS[a]}' for a in AXES])
    defs='\n'.join([f'- `{a}` (0-3): {AXIS_DEFS[a]}' for a in AXES])
    return f'''\n\n## Required output schema\n\nReturn your response as a single JSON object matching exactly this schema. Use the canonical axis keys verbatim. Use only the values `0`, `1`, `2`, `3`, or `"unclear"` for axis ratings. Do not add axis keys not listed here. Do not rename keys. Do not wrap the JSON in markdown fences.\n\nCardinality constraints: `distinctive_features` must contain exactly 5 elements; `open_tags` must contain 5 to 10 elements; `representative_quotes` must contain 0 to 3 elements, and each quote must be 25 words or fewer.\n\n{{\n  "voice_portrait": "<2-4 sentence prose portrait>",\n  "distinctive_features": ["<feature 1>", "<feature 2>", "<feature 3>", "<feature 4>", "<feature 5>"],  // exactly 5 elements\n  "open_tags": ["<tag 1>", "<tag 2>", "<5 to 10 total tags>"],  // 5-10 elements\n  "axis_ratings": {{\n{axis_json}\n  }},\n  "representative_quotes": ["<quote 1>", "<quote 2>", "<quote 3>"],  // 0-3 elements; each <=25 words\n  "confidence": "low|medium|high",\n  "confidence_note": "<one sentence>"\n}}\n\n### Axis definitions\n\n{defs}\n\nUse `"unclear"` if the bundle does not support a judgment on this axis.\n'''

def write_bundle(bid, model, audit):
    outdir=BUNDLES/bid; outdir.mkdir(parents=True, exist_ok=True)
    parts=[f'# Pass B full-run bundle for MODEL_X\n\nBlind ID: {bid}\n\nDo not infer provider/lab/model identity. Do not use external knowledge. All provenance strings have been redacted where detected.\n']
    for label,path in [('personality card',find_card('personality-model-cards',model)),('personality profile',find_card('personality-model-profiles',model)),('values report',values_report(model))]:
        txt=read_text(path) if path else None
        if txt is None: audit.append([bid,label,'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model); parts.append(f'\n\n## Derived source: {label}\n\n{red}\n')
        if not counts: audit.append([bid,str(path),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit.append([bid,str(path),pat,c,';'.join(remaining)])
    ffdir=choose_dir(CORPUS/'traces_freeflow','freeflow_',model,'freeflow')
    vdir=choose_dir(CORPUS/'traces_values','',model,'values')
    for sample in FREEFLOW_SAMPLES:
        txt=json_result(ffdir/sample) if ffdir and (ffdir/sample).exists() else None
        if txt is None: audit.append([bid,str((ffdir or CORPUS/'traces_freeflow')/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model); parts.append(f'\n\n## Raw freeflow sample: {sample[:-5]}\n\n{red}\n')
        if not counts: audit.append([bid,str(ffdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit.append([bid,str(ffdir/sample),pat,c,';'.join(remaining)])
    for sample in VALUE_SAMPLES:
        txt=json_result(vdir/sample) if vdir and (vdir/sample).exists() else None
        if txt is None: audit.append([bid,str((vdir or CORPUS/'traces_values')/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model); parts.append(f'\n\n## Raw values sample: {sample[:-5]}\n\n{red}\n')
        if not counts: audit.append([bid,str(vdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit.append([bid,str(vdir/sample),pat,c,';'.join(remaining)])
    parts.append(schema_block())
    bundle='\n'.join(parts)
    remaining=[t for t in SUSPECT_TERMS if re.search(re.escape(t), bundle, re.I)]
    (outdir/'bundle.md').write_text(bundle, encoding='utf-8')
    (outdir/'manifest.json').write_text(json.dumps({'blind_id':bid,'model_for_audit':model,'freeflow_cell':ffdir.name if ffdir else None,'values_cell':vdir.name if vdir else None,'remaining_suspect_terms':remaining}, indent=2), encoding='utf-8')
    return remaining

def headline_models():
    out=[]
    with FEATURES.open() as f:
        for r in csv.DictReader(f):
            try: n=float(r.get('C_v1_marker_samples_used') or 0)
            except Exception: n=0
            if n>=50: out.append((r['blind_id'],r['UNBLINDING_METADATA_model']))
    return out

def main():
    PASS_B.mkdir(parents=True, exist_ok=True); BUNDLES.mkdir(parents=True, exist_ok=True)
    repaired=0
    for p in sorted(PILOT_IN.glob('M*.json')):
        data=json.loads(p.read_text(encoding='utf-8'))
        q=data.get('representative_quotes')
        if isinstance(q,list) and len(q)>3:
            data['representative_quotes']=q[:3]; data['auto_repaired_quote_cardinality']=True; repaired+=1
        else:
            data['auto_repaired_quote_cardinality']=False
        (PASS_B/p.name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    audit=[]; flagged={}; remaining=[]
    for bid,model in headline_models():
        if bid in EXPANDED_IDS: continue
        remaining.append((bid,model)); rem=write_bundle(bid, model, audit)
        if rem: flagged[bid]=rem
    with AUDIT.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f, delimiter='\t'); w.writerow(['blind_id','source_file','redaction_pattern','count','remaining_suspect_terms']); w.writerows(audit)
    print(f'Copied/repaired pilot JSON files: {len(list(PILOT_IN.glob("M*.json")))}; repaired quotes in {repaired}')
    print(f'Built remaining bundles: {len(remaining)}')
    print(f'Bundles with remaining suspect terms: {len(flagged)}')
    for k,v in sorted(flagged.items()): print(k, ';'.join(v))
if __name__=='__main__': main()
