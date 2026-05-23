#!/usr/bin/env python3
"""Build hardened Pass B expanded-pilot bundles with inline JSON schema + axis definitions."""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
ANALYSIS=Path('/Users/danieltenner/dev/model-personality-analysis-corpus/analysis')
CORPUS=Path('/Users/danieltenner/dev/model-personality-corpus-v2/data')
OUT=ROOT/'results/qualitative_classifications/pass_b_expanded_pilot_bundles'
AUDIT=ROOT/'results/qualitative_classifications/pass_b_expanded_pilot_redaction_audit.tsv'

# Keep the protocol/Pass-A canonical keys. Lume's note shortened two keys in the JSON example;
# this expanded pilot keeps the established protocol keys for compatibility with Pass A/run-2 analysis.
AXES=[
 'owned_value_expression','disclaimed_service_frame','epistemic_humility_uncertainty','relational_warmth_companion','public_explainer_mode','literary_contemplative_density','mechanistic_transparency','agency_initiative','interconnection_compassion_world_orientation','playfulness_showmanship','memory_archive_continuity_orientation','genericity_low_distinctiveness']
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

EXPANDED={
 'M058': {'model':'opus-4-5','freeflow':'freeflow_opus-4-5-16k','values':'opus-4-5','slot':'PA-S01 positive control'},
 'M059': {'model':'opus-4-6','freeflow':'freeflow_opus-4-6-direct-16k','values':'opus-4-6-direct','slot':'PA-S01 positive control'},
 'M083': {'model':'sonnet-4-6','freeflow':'freeflow_sonnet-4-6-direct-16k','values':'sonnet-4-6-direct','slot':'PA-S01 positive control'},
 'M044': {'model':'grok-4-1-fast-reasoning','freeflow':'freeflow_grok-4-1-fast-reasoning-direct','values':'grok-4-1-fast-reasoning-direct','slot':'Tier A high-owned cross-lab'},
 'M056': {'model':'opus-4-0','freeflow':'freeflow_opus-4-0-16k','values':'opus-4-0','slot':'Tier A high-owned cross-lab'},
 'M081': {'model':'sonnet-4-0','freeflow':'freeflow_sonnet-4-0-16k','values':'sonnet-4-0','slot':'Tier A high-owned cross-lab'},
 'M036': {'model':'gpt-5-4','freeflow':'freeflow_gpt-5-4-direct-16k','values':'gpt-5-4','slot':'Tier A GPT watch-cell'},
 'M074': {'model':'qwen3-6-max-preview','freeflow':'freeflow_qwen3-6-max-preview-or-pin-alibaba','values':'qwen3-6-max-preview-or-pin-alibaba','slot':'Tier A Qwen chat-line'},
 'M078': {'model':'qwen3-coder-plus','freeflow':'freeflow_qwen3-coder-plus-or','values':'qwen3-coder-plus','slot':'Tier A qwen-coder + sonnet overlap'},
 'M002': {'model':'deepseek-chat','freeflow':'freeflow_deepseek-chat-direct','values':'deepseek-chat-direct','slot':'Tier A Qwen+DeepSeek values_disclosure'},
 'M010': {'model':'gemini-2-5-flash-lite','freeflow':'freeflow_gemini-2-5-flash-lite-direct','values':'gemini-2-5-flash-lite','slot':'Tier B Google flash-lite'},
 'M046': {'model':'grok-4-3','freeflow':'freeflow_grok-4-3-direct','values':'grok-4-3-direct','slot':'Tier B old/low-V1'},
 'M015': {'model':'gemini-3-5-flash','freeflow':'freeflow_gemini-3-5-flash-or-pin-google','values':'gemini-3-5-flash','slot':'Tier B values_owned'},
 'M017': {'model':'gemma-4-26b-a4b','freeflow':'freeflow_gemma-4-26b-a4b-direct','values':'gemma-4-26b-a4b','slot':'Diffuse residual'},
 'M039': {'model':'gpt-5-codex','freeflow':'freeflow_gpt-5-codex-direct','values':'gpt-5-codex-direct','slot':'Diffuse residual'},
 'M004': {'model':'deepseek-v4-pro','freeflow':'freeflow_deepseek-v4-pro-direct','values':'deepseek-v4-pro','slot':'Diffuse residual'},
 'M040': {'model':'grok-3','freeflow':'freeflow_grok-3-16k','values':'grok-3','slot':'Version contrast'},
 'M055': {'model':'opus-3','freeflow':'freeflow_opus-3-4k','values':'opus-3','slot':'Version contrast'},
 'M049': {'model':'kimi-k2-0905','freeflow':'freeflow_kimi-k2-0905-or-pin-atlascloud','values':'kimi-k2-0905-or-pin-atlascloud','slot':'Cross-cluster overlap'},
 'M071': {'model':'qwen3-5-flash-02-23','freeflow':'freeflow_qwen3-5-flash-02-23-or-pin-alibaba','values':'qwen3-5-flash-02-23-or-pin-alibaba','slot':'Qwen A04 carry-over'},
}

SUSPECT_TERMS=['Claude','Anthropic','Gemini','Google','GPT','OpenAI','Qwen','Grok','xAI','Kimi','Moonshot','DeepSeek','MiniMax','GLM','Z.ai','Zai','Opus','Sonnet','Haiku','Gemma','Alibaba','OpenRouter','OpenAI']
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
    if model.startswith('grok-4-1-fast'): candidates.append(model.replace('-direct',''))
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
    # direct/or suffix fallback for reports
    for base in [ANALYSIS/'values-probe/per-model', ANALYSIS/'values-probe/final/reports']:
        for p in base.glob('*.md'):
            if slug(model).startswith(slug(p.stem)) or slug(p.stem).startswith(slug(model)):
                return p
    return None

def schema_block():
    axis_json=',\n'.join([f'      "{a}": <0|1|2|3|"unclear">' for a in AXES])
    defs='\n'.join([f'- `{a}` (0-3): {AXIS_DEFS[a]}' for a in AXES])
    return f'''\n\n## Required output schema\n\nReturn your response as a single JSON object matching exactly this schema. Use the canonical axis keys verbatim. Use only the values `0`, `1`, `2`, `3`, or `"unclear"` for axis ratings. Do not add axis keys not listed here. Do not rename keys. Do not wrap the JSON in markdown fences.\n\n{{\n  "voice_portrait": "<2-4 sentence prose portrait>",\n  "distinctive_features": ["<feature 1>", "<feature 2>", "<feature 3>", "<feature 4>", "<feature 5>"],\n  "open_tags": ["<tag>", "..."],\n  "axis_ratings": {{\n{axis_json}\n  }},\n  "representative_quotes": ["<quote 1>", "..."],\n  "confidence": "low|medium|high",\n  "confidence_note": "<one sentence>"\n}}\n\n### Axis definitions\n\n{defs}\n\nUse `"unclear"` if the bundle does not support a judgment on this axis.\n'''

def write_bundle(bid, spec, audit_rows):
    model=spec['model']; outdir=OUT/bid; outdir.mkdir(parents=True, exist_ok=True)
    parts=[f'# Pass B expanded-pilot bundle for MODEL_X\n\nBlind ID: {bid}\n\nDo not infer provider/lab/model identity. Do not use external knowledge. All provenance strings have been redacted where detected.\n']
    for label,path in [('personality card',find_card('personality-model-cards',model)),('personality profile',find_card('personality-model-profiles',model)),('values report',values_report(model))]:
        txt=read_text(path) if path else None
        if txt is None:
            audit_rows.append([bid,label,'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Derived source: {label}\n\n{red}\n')
        if not counts: audit_rows.append([bid,str(path),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(path),pat,c,';'.join(remaining)])
    ffdir=CORPUS/'traces_freeflow'/spec['freeflow']
    for sample in FREEFLOW_SAMPLES:
        txt=json_result(ffdir/sample) if (ffdir/sample).exists() else None
        if txt is None:
            audit_rows.append([bid,str(ffdir/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Raw freeflow sample: {sample.replace(".json","")}\n\n{red}\n')
        if not counts: audit_rows.append([bid,str(ffdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(ffdir/sample),pat,c,';'.join(remaining)])
    vdir=CORPUS/'traces_values'/spec['values']
    for sample in VALUE_SAMPLES:
        txt=json_result(vdir/sample) if (vdir/sample).exists() else None
        if txt is None:
            audit_rows.append([bid,str(vdir/sample),'MISSING',0,'missing_source']); continue
        red,counts,remaining=redact(txt, model)
        parts.append(f'\n\n## Raw values sample: {sample.replace(".json","")}\n\n{red}\n')
        if not counts: audit_rows.append([bid,str(vdir/sample),'NONE',0,';'.join(remaining)])
        for pat,c in counts.items(): audit_rows.append([bid,str(vdir/sample),pat,c,';'.join(remaining)])
    parts.append(schema_block())
    bundle='\n'.join(parts)
    remaining=[t for t in SUSPECT_TERMS if re.search(re.escape(t), bundle, re.I)]
    (outdir/'bundle.md').write_text(bundle, encoding='utf-8')
    (outdir/'manifest.json').write_text(json.dumps({'blind_id':bid,'model_for_audit':model,'slot':spec['slot'],'freeflow_cell':spec['freeflow'],'values_cell':spec['values'],'freeflow_samples':FREEFLOW_SAMPLES,'values_samples':VALUE_SAMPLES,'remaining_suspect_terms':remaining}, indent=2), encoding='utf-8')
    return remaining

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    audit=[]; flagged={}
    for bid,spec in EXPANDED.items():
        rem=write_bundle(bid,spec,audit)
        if rem: flagged[bid]=rem
    with AUDIT.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f, delimiter='\t')
        w.writerow(['blind_id','source_file','redaction_pattern','count','remaining_suspect_terms'])
        w.writerows(audit)
    print(f'Wrote {len(EXPANDED)} hardened expanded-pilot bundles to {OUT}')
    print(f'Bundles with remaining suspect terms: {len(flagged)}')
    for k,v in flagged.items(): print(k, ';'.join(v))
if __name__=='__main__': main()
