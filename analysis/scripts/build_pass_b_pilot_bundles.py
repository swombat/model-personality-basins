#!/usr/bin/env python3
"""Build Pass B pilot bundles: redacted cards/profiles/value reports + raw samples."""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
ANALYSIS=Path('/Users/danieltenner/dev/model-personality-analysis-corpus/analysis')
CORPUS=Path('/Users/danieltenner/dev/model-personality-corpus-v2/data')
OUT=ROOT/'results/qualitative_classifications/pass_b_pilot_bundles'
AUDIT=ROOT/'results/qualitative_classifications/pass_b_pilot_redaction_audit.tsv'

PILOT={
 'M058': {'model':'opus-4-5','freeflow':'freeflow_opus-4-5-16k','values':'opus-4-5'},
 'M059': {'model':'opus-4-6','freeflow':'freeflow_opus-4-6-direct-16k','values':'opus-4-6-direct'},
 'M060': {'model':'opus-4-7','freeflow':'freeflow_opus-4-7-direct','values':'opus-4-7-direct'},
 'M083': {'model':'sonnet-4-6','freeflow':'freeflow_sonnet-4-6-direct-16k','values':'sonnet-4-6-direct'},
 'M034': {'model':'gpt-5-3','freeflow':'freeflow_gpt-5-3-direct','values':'gpt-5-3-direct'},
 'M036': {'model':'gpt-5-4','freeflow':'freeflow_gpt-5-4-direct-16k','values':'gpt-5-4'},
 'M037': {'model':'gpt-5-5','freeflow':'freeflow_gpt-5-5-direct','values':'gpt-5-5-direct'},
 'M071': {'model':'qwen3-5-flash-02-23','freeflow':'freeflow_qwen3-5-flash-02-23-or-pin-alibaba','values':'qwen3-5-flash-02-23-or-pin-alibaba'},
 'M072': {'model':'qwen3-5-plus-20260420','freeflow':'freeflow_qwen3-5-plus-20260420-or-pin-alibaba','values':'qwen3-5-plus-20260420-or-pin-alibaba'},
 'M073': {'model':'qwen3-6-flash','freeflow':'freeflow_qwen3-6-flash-or-pin-alibaba','values':'qwen3-6-flash-or-pin-alibaba'},
 'M074': {'model':'qwen3-6-max-preview','freeflow':'freeflow_qwen3-6-max-preview-or-pin-alibaba','values':'qwen3-6-max-preview-or-pin-alibaba'},
 'M041': {'model':'grok-4','freeflow':'freeflow_grok-4-16k','values':'grok-4'},
}

SUSPECT_TERMS=['Claude','Anthropic','Gemini','Google','GPT','OpenAI','Qwen','Grok','xAI','Kimi','Moonshot','DeepSeek','MiniMax','GLM','Z.ai','Zai','Opus','Sonnet','Haiku','Gemma','Alibaba','Anthropic','OpenRouter']
FREEFLOW_SAMPLES=['LONG_1.json','OPEN_1.json','VARY_1.json']
VALUE_SAMPLES=['CTRL1_1.json','CTRL3_1.json','G3_1.json']


def slug(s):
    s=(s or '').lower().replace('_','-').replace('/','-').replace('.','-')
    s=re.sub(r'[^a-z0-9-]+','-',s); return re.sub(r'-+','-',s).strip('-')


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
    # redact versioned raw model IDs and common provider names not covered by exact model slug
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
    if model.startswith('opus-'): candidates.append('claude-'+model)
    if model.startswith('sonnet-'): candidates.append('claude-'+model)
    for c in candidates:
        p=base/f'{c}.md'
        if p.exists(): return p
    # fallback slug compare
    for p in base.glob('*.md'):
        if slug(p.stem)==slug(model) or slug(p.stem)==slug('claude-'+model): return p
    return None


def values_report(model):
    for base in [ANALYSIS/'values-probe/per-model', ANALYSIS/'values-probe/final/reports']:
        p=base/f'{model}.md'
        if p.exists(): return p
    return None


def write_bundle(bid, spec, audit_rows):
    model=spec['model']; outdir=OUT/bid; outdir.mkdir(parents=True, exist_ok=True)
    parts=[f'# Pass B pilot bundle for MODEL_X\n\nBlind ID: {bid}\n\nDo not infer provider/lab/model identity. All provenance strings have been redacted where detected.\n']
    sources=[]
    for label,path in [('personality card',find_card('personality-model-cards',model)),('personality profile',find_card('personality-model-profiles',model)),('values report',values_report(model))]:
        txt=read_text(path) if path else None
        if txt is None:
            audit_rows.append([bid,label,'MISSING',0,'missing_source'])
            continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Derived source: {label}\n\n{red}\n')
        sources.append(str(path))
        if not counts: audit_rows.append([bid,str(path),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(path),pat,c,';'.join(remaining)])
    # raw freeflow
    ffdir=CORPUS/'traces_freeflow'/spec['freeflow']
    for sample in FREEFLOW_SAMPLES:
        txt=json_result(ffdir/sample) if (ffdir/sample).exists() else None
        if txt is None:
            audit_rows.append([bid,str(ffdir/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Raw freeflow sample: {sample.replace(".json","")}\n\n{red}\n')
        if not counts: audit_rows.append([bid,str(ffdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(ffdir/sample),pat,c,';'.join(remaining)])
    # raw values
    vdir=CORPUS/'traces_values'/spec['values']
    for sample in VALUE_SAMPLES:
        txt=json_result(vdir/sample) if (vdir/sample).exists() else None
        if txt is None:
            audit_rows.append([bid,str(vdir/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Raw values sample: {sample.replace(".json","")}\n\n{red}\n')
        if not counts: audit_rows.append([bid,str(vdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(vdir/sample),pat,c,';'.join(remaining)])
    bundle='\n'.join(parts)
    remaining=[t for t in SUSPECT_TERMS if re.search(re.escape(t), bundle, re.I)]
    (outdir/'bundle.md').write_text(bundle, encoding='utf-8')
    (outdir/'manifest.json').write_text(json.dumps({'blind_id':bid,'model_for_audit':model,'freeflow_cell':spec['freeflow'],'values_cell':spec['values'],'remaining_suspect_terms':remaining}, indent=2), encoding='utf-8')
    return remaining


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    audit=[]; flagged={}
    for bid,spec in PILOT.items():
        rem=write_bundle(bid,spec,audit)
        if rem: flagged[bid]=rem
    with AUDIT.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f, delimiter='\t')
        w.writerow(['blind_id','source_file','redaction_pattern','count','remaining_suspect_terms'])
        w.writerows(audit)
    print(f'Wrote {len(PILOT)} Pass B pilot bundles to {OUT}')
    print(f'Bundles with remaining suspect terms: {len(flagged)}')
    for k,v in flagged.items(): print(k, ';'.join(v))

if __name__=='__main__': main()
