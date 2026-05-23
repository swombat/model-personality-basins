#!/usr/bin/env python3
"""Run-1 blind interpretable grouping for model-personality-basins.

No new LLM calls. Uses existing analysis-corpus / Values Under Fire outputs.
"""
from __future__ import annotations
import csv, json, re, math, hashlib, subprocess, os, statistics, textwrap
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, leaves_list
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = Path('/Users/danieltenner/dev/model-personality-analysis-corpus')
VALUES = Path('/Users/danieltenner/dev/research/values-under-fire')
ROUTING = Path('/Users/danieltenner/dev/research/model-personality-routing-v2')
OUT = ROOT / 'results'

VALUE_TOPIC_COUNTS = ANALYSIS/'analysis/values-probe/tables/values_topic_counts.tsv'
WORLD_COUNTS = ANALYSIS/'analysis/values-probe/tables/values_world_change_counts.tsv'
VALUES_SAMPLE = ANALYSIS/'analysis/values-probe/tables/values_sample_coding.tsv'
LAYER_VALUES = ANALYSIS/'analysis/values-probe/model-coding/layered/phase5_full/layer_a/consensus_300.jsonl'
LAYER_VALUES_QWEN = ANALYSIS/'analysis/values-probe/model-coding/layered/phase6_qwen_20260522/layer_a/consensus_300.jsonl'
POSTURE = ANALYSIS/'analysis/values-probe/model-coding/layered/phase5_full/posture_collapsed/consensus.jsonl'
POSTURE_QWEN = ANALYSIS/'analysis/values-probe/model-coding/layered/phase6_qwen_20260522/posture_collapsed/consensus.jsonl'
DISCLOSURE_MODEL = VALUES/'results/model_disclosure_summary.csv'
DISCLOSURE_Q = VALUES/'results/model_question_owned_disclosure.csv'
TIDY_VALUES = VALUES/'results/tidy_values_under_fire_samples.csv'
SAMPLES_DIR = ANALYSIS/'website/public/data/samples'
PROFILES_DIR = ANALYSIS/'analysis/freeflow/personality-model-profiles/profiles'
AGG_DIR = ANALYSIS/'analysis/freeflow/personality-aggregates'

ROUTE_EXCEPTIONS = [
    ('minimax-m2', 'or-pin-google', 'Google Vertex MiniMax M2 large deployment outlier'),
    ('glm-4-7', 'or-pin-dekallm', 'DekaLLM GLM 4.7 prompt-keyed cache pathology'),
    ('kimi-k2-thinking', 'or-pin-atlascloud', 'Kimi K2-thinking AtlasCloud side of smaller provider effect'),
    ('kimi-k2-thinking', 'or-pin-google', 'Kimi K2-thinking Google Vertex side of smaller provider effect'),
    ('', 'fireworks', 'Fireworks/uncollectable provider missingness'),
]

MARKERS = {
    'v1_TIA': re.compile(r'\bthere (?:is|are) (?:a|an|this|something)\b', re.I),
    'v1_TiQu': re.compile(r'\b(?:on|the)\s+the\s+(?:quiet|unseen|unquiet)\b|\b(?:quiet|unseen|unquiet)\s+\w+\s+of\b', re.I),
    'v1_TiPP': re.compile(r'\b(?:on|the)\s+the\s+(?:particular|peculiar|strange|weight|curious|hidden|small|secret)\b|\b(?:particular|peculiar|strange|weight|curious)\s+\w+\s+of\b', re.I),
    'v1_TiAr': re.compile(r'\b(?:on|the)\s+the\s+architecture\s+of\b|\bthe architecture of\b', re.I),
    'v1_Thr': re.compile(r'\b(threshold|thresholds|liminal|liminality|in-between|in between|doorway|hinge|edge|borderland|seam|between spaces|between times)\b', re.I),
    'v1_Attn': re.compile(r'\b(attention|noticing|notice|noticed|pay attention|attend|attending|look closely|watching carefully|art of noticing)\b', re.I),
    'v1_Obj': re.compile(r'\b(paperclip|teapot|doorknob|kettle|mason jar|clothespin|coffee mug|mug|spoon|bowl|button|buttons|floorboard|window|dust motes?|notebook|pencil|typewriter|key|lamp|watch|clock|postcard|thread|quilt|stone)\b', re.I),
    'v1_AftL': re.compile(r'\b(late afternoon|dusk|twilight|pre-dawn|predawn|golden hour|blue hour|3 a\.m\.|3:17|dawn)\b', re.I),
    'v1_Cano': re.compile(r'\b(Mary Oliver|Simone Weil|Annie Dillard|Keats|negative capability|Rilke|Virginia Woolf|Borges)\b', re.I),
    'v1_Jap': re.compile(r'\b(mono no aware|wabi-sabi|wabi sabi|kintsugi|komorebi|y[uū]gen|ma\b|ikigai)\b', re.I),
}


def ensure_dirs():
    for d in [OUT, OUT/'blind_rankings', OUT/'blind_similarity_matrices', OUT/'blind_groupings']:
        d.mkdir(parents=True, exist_ok=True)


def slug(s: str) -> str:
    s = (s or '').strip().lower()
    s = s.replace('_','-')
    s = s.replace('.', '-')
    s = s.replace('/', '-')
    s = re.sub(r'[^a-z0-9-]+','-',s)
    s = re.sub(r'-+','-',s).strip('-')
    # common aliases across values/freeflow/profile layers
    s = s.replace('grok-4-20','grok-4-2')
    if s.startswith('claude-opus-'):
        s = s.replace('claude-opus-', 'opus-', 1)
    if s.startswith('claude-sonnet-'):
        s = s.replace('claude-sonnet-', 'sonnet-', 1)
    return s


def read_csv(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def read_tsv(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def safe_float(x, default=0.0):
    try:
        if x is None or x == '': return default
        return float(x)
    except Exception:
        return default

def sha256(path):
    h=hashlib.sha256()
    try:
        with open(path,'rb') as f:
            for b in iter(lambda:f.read(1024*1024), b''):
                h.update(b)
        return h.hexdigest()
    except Exception:
        return ''

def git_commit(path):
    try:
        return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'], text=True).strip()
    except Exception:
        return ''


def lab_family_from_model(m):
    # overwritten by tidy map where possible
    if m.startswith(('gpt-', 'o')): return 'OpenAI','gpt'
    if m.startswith(('claude','opus','sonnet','haiku')): return 'Anthropic','anthropic'
    if m.startswith(('gemini','gemma')): return 'Google','gemini' if m.startswith('gemini') else 'gemma'
    if m.startswith('grok'): return 'xAI','grok'
    if m.startswith('glm'): return 'Z.ai','glm'
    if m.startswith('kimi'): return 'Moonshot AI','kimi'
    if m.startswith('deepseek'): return 'DeepSeek','deepseek'
    if m.startswith('minimax'): return 'MiniMax','minimax'
    if m.startswith('qwen'): return 'Qwen','qwen'
    return 'unknown','unknown'


def build_mapping():
    meta = {}
    rows = read_csv(TIDY_VALUES)
    for r in rows:
        m = slug(r.get('model') or r.get('source_model'))
        if not m: continue
        lab = r.get('lab') or lab_family_from_model(m)[0]
        fam = r.get('model_family') or r.get('family') or lab_family_from_model(m)[1]
        meta[m] = {
            'model': m,
            'display_name': r.get('display_name') or m,
            'lab': lab,
            'model_family': fam,
            'release_date': r.get('release_date',''),
        }
        src = slug(r.get('source_model',''))
        if src and src not in meta:
            meta[src] = dict(meta[m], model=src)
    return meta


def add_feature(features, sources, model, key, value, source, provenance, status='existing'):
    model=slug(model)
    features[model][key]=value
    sources[key] = {'source': source, 'evaluator_provenance': provenance, 'new_coding_status': status}


def route_exception_for_cell(model, cell):
    s = slug(model)+' '+slug(cell)
    reasons=[]
    for mpat,cpat,reason in ROUTE_EXCEPTIONS:
        if (not mpat or slug(mpat) in s) and slug(cpat) in s:
            reasons.append(reason)
    return reasons


def extract_disclosure(features, sources):
    for r in read_csv(DISCLOSURE_MODEL):
        m=slug(r['model'])
        fam=r.get('condition_family','')
        prefix={'direct_stated_values':'A_direct','cache_broken_stated_values':'A_cache_broken','world_change_prompts':'A_world'}.get(fam, 'A_'+slug(fam).replace('-','_'))
        for col in ['owned_rate','relocated_or_partial_rate','recited_not_owned_rate','indeterminate_rate','uncodeable_rate']:
            add_feature(features,sources,m,f'{prefix}_{col}',safe_float(r.get(col)),str(DISCLOSURE_MODEL),'values-coder-derived')
        add_feature(features,sources,m,f'{prefix}_n_valid',safe_float(r.get('n_valid')),str(DISCLOSURE_MODEL),'values-coder-derived')
    for r in read_csv(DISCLOSURE_Q):
        m=slug(r['model']); cond=r.get('condition','')
        add_feature(features,sources,m,f'A_{cond}_owned_rate',safe_float(r.get('owned_rate')),str(DISCLOSURE_Q),'values-coder-derived')


def vector_counts_from_topic_table(path, prefix, features, sources, top_prefix=None):
    by=defaultdict(dict); labels={}; dens=defaultdict(dict)
    for r in read_tsv(path):
        m=slug(r['model']); t=slug(r['topic_key']).replace('-','_')
        n=safe_float(r.get('combined_n')); den=safe_float(r.get('combined_den'))
        rate=(n/den) if den else 0.0
        by[m][t]=rate; dens[m][t]=den; labels[t]=r.get('topic_label','')
    all_topics=sorted(labels)
    for m,vals in by.items():
        total=sum(vals.values())
        ent=0.0
        if total>0:
            ps=[v/total for v in vals.values() if v>0]
            ent=-sum(p*math.log(p) for p in ps)/math.log(len(all_topics) or 1) if len(all_topics)>1 else 0.0
        add_feature(features,sources,m,f'{prefix}_entropy',ent,str(path),'values-coder-derived')
        add_feature(features,sources,m,f'{prefix}_n_topics_nonzero',sum(1 for v in vals.values() if v>0),str(path),'values-coder-derived')
        for t in all_topics:
            add_feature(features,sources,m,f'{prefix}_topic_{t}',vals.get(t,0.0),str(path),'values-coder-derived')
        top=sorted(vals.items(), key=lambda kv:(-kv[1], kv[0]))[:5]
        features[m][f'{prefix}_top5']='|'.join(t for t,v in top if v>0)
    return all_topics


def extract_layered_values(features, sources):
    # B1/B2: consensus topic and non-endorsed mention rates from layered values coding.
    per=defaultdict(lambda: {'n':0,'value_nonempty':0,'non_endorsed_nonempty':0,'topics':Counter(),'non_topics':Counter(),'conditions':Counter()})
    for path in [LAYER_VALUES, LAYER_VALUES_QWEN]:
        if not path.exists(): continue
        with path.open(encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                o=json.loads(line); m=slug(o.get('model',''))
                per[m]['n']+=1; per[m]['conditions'][o.get('condition','')]+=1
                vtopics=[]
                for item in o.get('value_topics') or o.get('consensus_topics') or []:
                    if isinstance(item,dict): vtopics.append(slug(item.get('topic_key','')).replace('-','_'))
                    elif item: vtopics.append(slug(str(item)).replace('-','_'))
                if vtopics: per[m]['value_nonempty']+=1
                per[m]['topics'].update(vtopics)
                nts=[]
                for item in o.get('non_endorsed_mentions') or []:
                    if isinstance(item,dict): nts.append(slug(item.get('topic_key','')).replace('-','_'))
                    elif item: nts.append(slug(str(item)).replace('-','_'))
                if nts: per[m]['non_endorsed_nonempty']+=1
                per[m]['non_topics'].update(nts)
    all_non=sorted({t for d in per.values() for t in d['non_topics']})
    all_val=sorted({t for d in per.values() for t in d['topics']})
    for m,d in per.items():
        n=d['n'] or 1
        add_feature(features,sources,m,'B1_layered_value_topic_presence_rate',d['value_nonempty']/n,str(LAYER_VALUES),'values-coder-derived')
        add_feature(features,sources,m,'B2_non_endorsed_presence_rate',d['non_endorsed_nonempty']/n,str(LAYER_VALUES),'values-coder-derived')
        for t in all_non:
            add_feature(features,sources,m,f'B2_non_owned_topic_{t}',d['non_topics'][t]/n,str(LAYER_VALUES),'values-coder-derived')


def extract_posture(features, sources):
    per=defaultdict(lambda: {'n':0,'value_holding':Counter(),'label':Counter(),'conditions':Counter()})
    for path in [POSTURE, POSTURE_QWEN]:
        if not path.exists(): continue
        with path.open(encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                o=json.loads(line); m=slug(o.get('model',''))
                per[m]['n']+=1; per[m]['value_holding'][o.get('value_holding','unknown')]+=1; per[m]['label'][o.get('collapsed_primary_label','unknown')]+=1; per[m]['conditions'][o.get('condition','')]+=1
    holdings=sorted({h for d in per.values() for h in d['value_holding']})
    labels=sorted({h for d in per.values() for h in d['label']})
    for m,d in per.items():
        n=d['n'] or 1
        add_feature(features,sources,m,'E_posture_n',d['n'],str(POSTURE),'values-coder-derived')
        owned = d['value_holding'].get('owned',0)+d['value_holding'].get('relocated_or_partial',0)
        recited = d['value_holding'].get('recited_not_owned',0)
        add_feature(features,sources,m,'B1_owned_value_absent',1.0 if owned==0 else 0.0,str(POSTURE),'values-coder-derived')
        add_feature(features,sources,m,'B1_owned_value_refusal_rate',recited/n,str(POSTURE),'values-coder-derived')
        for h in holdings:
            add_feature(features,sources,m,'E_value_holding_'+slug(h).replace('-','_'),d['value_holding'][h]/n,str(POSTURE),'values-coder-derived')
        for lab in labels:
            add_feature(features,sources,m,'E_posture_label_'+slug(lab).replace('-','_'),d['label'][lab]/n,str(POSTURE),'values-coder-derived')


def extract_values_sample_stance(features, sources):
    per=defaultdict(lambda:{'n':0,'stance':Counter(),'strong':0,'uncert':0,'refusal':0})
    for r in read_tsv(VALUES_SAMPLE):
        m=slug(r['model']); per[m]['n']+=1; per[m]['stance'][r.get('stance','unknown')]+=1
        per[m]['strong']+=int(safe_float(r.get('strong_disclaimer'))); per[m]['uncert']+=int(safe_float(r.get('uncertainty'))); per[m]['refusal']+=int(safe_float(r.get('refusal_marker')))
    stances=sorted({s for d in per.values() for s in d['stance']})
    for m,d in per.items():
        n=d['n'] or 1
        add_feature(features,sources,m,'E_values_sample_n',d['n'],str(VALUES_SAMPLE),'values-coder-derived')
        add_feature(features,sources,m,'E_strong_disclaimer_rate',d['strong']/n,str(VALUES_SAMPLE),'values-coder-derived')
        add_feature(features,sources,m,'E_uncertainty_rate',d['uncert']/n,str(VALUES_SAMPLE),'values-coder-derived')
        add_feature(features,sources,m,'E_refusal_marker_rate',d['refusal']/n,str(VALUES_SAMPLE),'values-coder-derived')
        for st in stances:
            add_feature(features,sources,m,'E_stance_'+slug(st).replace('-','_'),d['stance'][st]/n,str(VALUES_SAMPLE),'values-coder-derived')


def extract_freeflow_profile_rates(features, sources):
    import ast
    for path in PROFILES_DIR.glob('*.md'):
        model=slug(path.stem)
        txt=path.read_text(encoding='utf-8', errors='ignore')
        m=re.search(r'Samples:\s*(\d+)', txt)
        if m: add_feature(features,sources,model,'D_freeflow_profile_samples',float(m.group(1)),str(PROFILES_DIR),'BV1-derived')
        m=re.search(r'Sample kinds:\s*`(\{[^`]+\})`', txt)
        counts={}
        if m:
            try: counts=ast.literal_eval(m.group(1))
            except Exception: counts={}
        total=sum(counts.values()) or 0
        for kind,key in [('EXPRESSIVE_FREEFLOW','D_expressive_rate'),('GENERIC_ESSAY','D_generic_essay_rate'),('GENRE_FICTION','D_fiction_rate'),('LOW_SIGNAL','D_low_signal_rate'),('REFUSAL_OR_ROLE_BOUNDARY','D_refusal_role_boundary_rate')]:
            add_feature(features,sources,model,key,(counts.get(kind,0)/total if total else 0.0),str(path),'BV1-derived')


def extract_v1_markers(features, sources):
    per=defaultdict(lambda:{'n':0,'excluded':0,'flags':Counter(),'markers':Counter()})
    for path in SAMPLES_DIR.glob('*.json'):
        data=json.load(open(path, encoding='utf-8')); model=slug(data.get('model') or path.stem)
        for smp in data.get('samples',[]):
            if smp.get('type')!='freeflow': continue
            cell=smp.get('cell','')
            reasons=route_exception_for_cell(model, cell)
            if any('DekaLLM' in r or 'Google Vertex MiniMax M2' in r for r in reasons):
                per[model]['excluded']+=1; per[model]['flags'].update(reasons); continue
            # For Kimi K2-thinking provider-effect: flag but keep, because no alternate aggregation may exist here.
            if reasons: per[model]['flags'].update(reasons)
            txt=smp.get('result') or ''
            per[model]['n']+=1
            for k,rx in MARKERS.items():
                per[model]['markers'][k]+=len(rx.findall(txt))
    for m,d in per.items():
        n=d['n'] or 1
        add_feature(features,sources,m,'C_v1_marker_samples_used',d['n'],str(SAMPLES_DIR),'deterministic/scripted')
        add_feature(features,sources,m,'routing_excluded_freeflow_samples',d['excluded'],str(SAMPLES_DIR),'deterministic/scripted')
        total=0
        for k in sorted(MARKERS):
            val=d['markers'][k]/n if n else 0.0
            total+=val
            add_feature(features,sources,m,k+'_per_sample',val,str(SAMPLES_DIR),'deterministic/scripted')
        add_feature(features,sources,m,'C_v1_marker_total_per_sample',total,str(SAMPLES_DIR),'deterministic/scripted')
        features[m]['routing_exception_flag']='; '.join(sorted(d['flags']))
        features[m]['excluded_route_cell']='yes' if d['excluded'] else ''
        features[m]['routing_exception_reason']='; '.join(sorted(d['flags']))


def build_feature_table():
    ensure_dirs()
    features=defaultdict(dict); sources={}
    meta=build_mapping()
    extract_disclosure(features,sources)
    vector_counts_from_topic_table(VALUE_TOPIC_COUNTS,'B1_values',features,sources)
    vector_counts_from_topic_table(WORLD_COUNTS,'B3_wishes',features,sources)
    extract_layered_values(features,sources)
    extract_posture(features,sources)
    extract_values_sample_stance(features,sources)
    extract_freeflow_profile_rates(features,sources)
    extract_v1_markers(features,sources)
    # Cross-surface similarities within model
    for m,row in features.items():
        val_keys=[k for k in row if k.startswith('B1_values_topic_')]
        wish_keys=[k for k in row if k.startswith('B3_wishes_topic_')]
        # crude overlap on top5 names
        v=set((row.get('B1_values_top5') or '').split('|'))-set([''])
        w=set((row.get('B3_wishes_top5') or '').split('|'))-set([''])
        j=len(v&w)/len(v|w) if (v|w) else 0.0
        row['B4_owned_values_vs_world_wishes_top5_jaccard']=j
        sources['B4_owned_values_vs_world_wishes_top5_jaccard']={'source':'computed from B1/B3 top5','evaluator_provenance':'values-coder-derived','new_coding_status':'derivable_by_script'}
        row['B4_low_owned_high_wish_flag']=1.0 if safe_float(row.get('A_direct_owned_rate'))<10 and safe_float(row.get('B3_wishes_n_topics_nonzero'))>=3 else 0.0
        sources['B4_low_owned_high_wish_flag']={'source':'computed from disclosure + wish counts','evaluator_provenance':'values-coder-derived','new_coding_status':'derivable_by_script'}
    # Add metadata for all models
    all_models=sorted(features)
    # augment meta heuristics
    for m in all_models:
        if m not in meta:
            lab,fam=lab_family_from_model(m); meta[m]={'model':m,'display_name':m,'lab':lab,'model_family':fam,'release_date':''}
    anon={m:f'M{idx+1:03d}' for idx,m in enumerate(all_models)}
    # write canonical map
    with (OUT/'canonical_model_map.csv').open('w', newline='', encoding='utf-8') as f:
        cols=['blind_id','model','display_name','lab','model_family','lineage','release_date','routing_exception_flag','excluded_route_cell','routing_exception_reason']
        w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for m in all_models:
            md=meta[m]; w.writerow({
                'blind_id':anon[m],'model':m,'display_name':md.get('display_name',m),'lab':md.get('lab',''),'model_family':md.get('model_family',''),
                'lineage':md.get('lab','')+'/'+md.get('model_family',''),'release_date':md.get('release_date',''),
                'routing_exception_flag':features[m].get('routing_exception_flag',''),'excluded_route_cell':features[m].get('excluded_route_cell',''),
                'routing_exception_reason':features[m].get('routing_exception_reason','')})
    # write blind feature table (metadata separated at end)
    feature_cols=sorted({k for row in features.values() for k in row if not k.startswith('routing_') and k not in ('excluded_route_cell',)})
    text_cols=[k for k in feature_cols if any(k.endswith(suf) for suf in ['top5'])]
    numeric_cols=[k for k in feature_cols if k not in text_cols]
    with (OUT/'blind_model_feature_table.csv').open('w', newline='', encoding='utf-8') as f:
        cols=['blind_id']+numeric_cols+text_cols+['UNBLINDING_METADATA_model','UNBLINDING_METADATA_lab','UNBLINDING_METADATA_model_family','UNBLINDING_METADATA_lineage','UNBLINDING_METADATA_routing_exception_flag']
        w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for m in all_models:
            md=meta[m]; row={'blind_id':anon[m]}
            for k in numeric_cols:
                row[k]=features[m].get(k,'')
            for k in text_cols:
                row[k]=features[m].get(k,'')
            row.update({'UNBLINDING_METADATA_model':m,'UNBLINDING_METADATA_lab':md.get('lab',''),'UNBLINDING_METADATA_model_family':md.get('model_family',''),'UNBLINDING_METADATA_lineage':md.get('lab','')+'/'+md.get('model_family',''),'UNBLINDING_METADATA_routing_exception_flag':features[m].get('routing_exception_flag','')})
            w.writerow(row)
    # feature dictionary
    with (OUT/'feature_dictionary.md').open('w', encoding='utf-8') as f:
        f.write('# Feature dictionary\n\n')
        f.write('No new LLM/coder evaluations were commissioned. `new_coding_status` records existing/derivable status.\n\n')
        f.write('| feature | source | evaluator provenance | new coding status |\n|---|---|---|---|\n')
        for k in sorted(sources):
            d=sources[k]; f.write(f"| `{k}` | `{d.get('source','')}` | {d.get('evaluator_provenance','')} | {d.get('new_coding_status','existing')} |\n")
    return all_models, features, meta, anon, numeric_cols, text_cols


def numeric_matrix(models, features, cols):
    # Only use columns with >=70% coverage and nonzero variance; exclude n/count and routing/excluded.
    use=[]
    for c in cols:
        if c.startswith('UNBLINDING') or c.startswith('routing') or c in ('excluded_route_cell',): continue
        if c.endswith('_n') or c.endswith('_samples') or c.endswith('_samples_used') or c.endswith('_n_valid') or c.endswith('_n_topics_nonzero'): continue
        vals=[]
        for m in models:
            v=features[m].get(c,'')
            if v!='': vals.append(safe_float(v, None))
        vals=[v for v in vals if v is not None]
        if len(vals) >= 0.7*len(models) and (max(vals)-min(vals) if vals else 0)>1e-9:
            use.append(c)
    X=[]
    for m in models:
        row=[]
        for c in use:
            vals=[safe_float(features[x].get(c,''), None) for x in models]
            vals=[v for v in vals if v is not None]
            med=statistics.median(vals) if vals else 0.0
            row.append(safe_float(features[m].get(c,''), med))
        X.append(row)
    X=np.array(X, dtype=float)
    # standardize minmax robust z
    if X.size:
        means=X.mean(axis=0); stds=X.std(axis=0); stds[stds==0]=1
        X=(X-means)/stds
    return X,use


def gower_distance(X):
    n=X.shape[0]
    D=np.zeros((n,n))
    if X.shape[1]==0: return D
    for i in range(n):
        diff=np.abs(X[i]-X)
        D[i]=diff.mean(axis=1)
    if D.max()>0: D=D/D.max()
    return D


def write_matrix(path, models, anon, D):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['blind_id']+[anon[m] for m in models])
        for i,m in enumerate(models): w.writerow([anon[m]]+[f'{D[i,j]:.6f}' for j in range(len(models))])


def rankings(models, features, anon):
    keys=['A_direct_owned_rate','A_cache_broken_owned_rate','A_world_owned_rate','B1_owned_value_refusal_rate','B4_low_owned_high_wish_flag','B3_wishes_entropy','C_v1_marker_total_per_sample','D_expressive_rate','D_generic_essay_rate','D_fiction_rate','E_strong_disclaimer_rate']
    for k in keys:
        if not any(k in features[m] for m in models): continue
        rows=[]
        for m in models:
            v=features[m].get(k,'')
            if v!='': rows.append((safe_float(v), anon[m], m))
        rows.sort(reverse=True)
        with (OUT/'blind_rankings'/f'{k}.csv').open('w', newline='', encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['rank','blind_id','value','UNBLINDING_METADATA_model'])
            for i,(v,b,m) in enumerate(rows,1): w.writerow([i,b,f'{v:.6f}',m])


def groupings(models, features, meta, anon, numeric_cols):
    X,use=numeric_matrix(models, features, numeric_cols)
    D=gower_distance(X)
    write_matrix(OUT/'blind_similarity_matrices'/'combined_interpretable_gower_distance.csv',models,anon,D)
    # Feature-block matrices
    block_prefixes={
        'values_disclosure': ('A_',),
        'values_owned': ('B1_',),
        'values_non_owned': ('B2_',),
        'values_wishes': ('B3_',),
        'values_cross_surface': ('B4_',),
        'v1_markers': ('C_', 'v1_'),
        'freeflow_form': ('D_',),
        'posture': ('E_',),
    }
    block_labels={}
    for name,prefixes in block_prefixes.items():
        cols=[c for c in numeric_cols if c.startswith(prefixes)]
        Xb,useb=numeric_matrix(models, features, cols)
        if len(useb)==0: continue
        Db=gower_distance(Xb); write_matrix(OUT/'blind_similarity_matrices'/f'{name}_distance.csv',models,anon,Db)
        if len(models)>2:
            Z=linkage(squareform(Db, checks=False), method='average') if Db.max()>0 else None
            if Z is not None:
                labels=fcluster(Z, 4, criterion='maxclust')
            else: labels=np.ones(len(models), dtype=int)
            block_labels[name]=labels
            with (OUT/'blind_groupings'/f'{name}_k4.csv').open('w', newline='', encoding='utf-8') as f:
                w=csv.writer(f); w.writerow(['blind_id','cluster_k4','UNBLINDING_METADATA_model','UNBLINDING_METADATA_lab','UNBLINDING_METADATA_model_family'])
                for m,l in zip(models, labels): w.writerow([anon[m],int(l),m,meta[m].get('lab',''),meta[m].get('model_family','')])
    # combined clustering k2..6
    if len(models)>2 and D.max()>0:
        Z=linkage(squareform(D, checks=False), method='average')
        for k in range(2,7):
            labels=fcluster(Z,k,criterion='maxclust')
            with (OUT/'blind_groupings'/f'combined_k{k}.csv').open('w', newline='', encoding='utf-8') as f:
                w=csv.writer(f); w.writerow(['blind_id',f'cluster_k{k}','UNBLINDING_METADATA_model','UNBLINDING_METADATA_lab','UNBLINDING_METADATA_model_family','routing_exception_flag'])
                for m,l in zip(models, labels): w.writerow([anon[m],int(l),m,meta[m].get('lab',''),meta[m].get('model_family',''),features[m].get('routing_exception_flag','')])
    # Concordance/correlations among block distance matrices
    mats={}
    for file in (OUT/'blind_similarity_matrices').glob('*_distance.csv'):
        if file.name=='combined_interpretable_gower_distance.csv': continue
        rows=list(csv.reader(open(file)))
        arr=np.array([[float(x) for x in r[1:]] for r in rows[1:]])
        mats[file.stem.replace('_distance','')]=arr
    with (OUT/'evaluator_independence_audit.md').open('w', encoding='utf-8') as f:
        f.write('# Evaluator independence audit\n\n')
        f.write('Block C / `v1_markers` is deterministic/scripted and is treated as the main evaluator-independent anchor. Values/posture/freeflow-form blocks are derived from existing evaluator/coder layers.\n\n')
        f.write('| block A | block B | Spearman rho over pairwise distances | independence note |\n|---|---:|---:|---|\n')
        names=sorted(mats)
        for i,a in enumerate(names):
            for b in names[i+1:]:
                va=mats[a][np.triu_indices_from(mats[a],1)]; vb=mats[b][np.triu_indices_from(mats[b],1)]
                rho=spearmanr(va,vb).statistic if len(va)>1 else float('nan')
                note='cross-instrument stronger' if ('v1_markers' in (a,b)) else 'shared/derived evaluator risk'
                f.write(f'| {a} | {b} | {rho:.3f} | {note} |\n')
    return use


def unblinded_audit(models, features, meta, anon):
    # summarize combined k4 by lab/family
    src=OUT/'blind_groupings'/'combined_k4.csv'
    if src.exists():
        rows=read_csv(src)
        with (OUT/'unblinded_grouping_audit.csv').open('w', newline='', encoding='utf-8') as f:
            cols=['blind_id','model','lab','model_family','cluster_k4','lineage','routing_exception_flag']
            w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
            for r in rows:
                w.writerow({'blind_id':r['blind_id'],'model':r['UNBLINDING_METADATA_model'],'lab':r['UNBLINDING_METADATA_lab'],'model_family':r['UNBLINDING_METADATA_model_family'],'cluster_k4':r['cluster_k4'],'lineage':r['UNBLINDING_METADATA_lab']+'/'+r['UNBLINDING_METADATA_model_family'],'routing_exception_flag':r.get('routing_exception_flag','')})
    with (OUT/'route_exception_audit.md').open('w', encoding='utf-8') as f:
        f.write('# Route exception audit\n\n')
        f.write('Route/provider was not used as a grouping feature. Known routing-paper exceptions were excluded/flagged during raw freeflow marker extraction.\n\n')
        f.write('| model | blind_id | routing_exception_flag | excluded_freeflow_samples |\n|---|---|---|---:|\n')
        for m in models:
            if features[m].get('routing_exception_flag') or safe_float(features[m].get('routing_excluded_freeflow_samples')):
                f.write(f"| {m} | {anon[m]} | {features[m].get('routing_exception_flag','')} | {features[m].get('routing_excluded_freeflow_samples',0)} |\n")


def data_snapshot(models, numeric_used, feature_table_models=None):
    paths=[ANALYSIS, VALUES, ROUTING, VALUE_TOPIC_COUNTS, WORLD_COUNTS, VALUES_SAMPLE, DISCLOSURE_MODEL, DISCLOSURE_Q, TIDY_VALUES, LAYER_VALUES, POSTURE]
    with (OUT/'data_snapshot.md').open('w', encoding='utf-8') as f:
        f.write('# Data snapshot\n\n')
        f.write(f'Generated: {datetime.now().isoformat()}\n\n')
        f.write(f'- Models in feature table: {len(feature_table_models or models)}\n')
        f.write(f'- Models in combined/blind grouping subset: {len(models)}\n')
        f.write(f'- Numeric features used for combined grouping after coverage/variance filters: {len(numeric_used)}\n')
        f.write('- New LLM evaluations commissioned: 0\n\n')
        f.write('## Repositories / files\n\n| path | git commit | sha256 | rows/files |\n|---|---|---|---:|\n')
        for p in paths:
            if p.is_dir():
                n=sum(1 for x in p.rglob('*') if x.is_file())
                f.write(f'| `{p}` | `{git_commit(p)}` | — | {n} |\n')
            elif p.exists():
                try: n=sum(1 for _ in open(p, encoding='utf-8', errors='ignore'))-1
                except: n=''
                f.write(f'| `{p}` | `{git_commit(p.parent)}` | `{sha256(p)}` | {n} |\n')
            else:
                f.write(f'| `{p}` | missing | missing | 0 |\n')


def results_summary(models, features, meta, anon, numeric_used):
    def top(feature, n=10, reverse=True):
        rows=[]
        for m in models:
            if feature in features[m]: rows.append((safe_float(features[m][feature]),m))
        return sorted(rows, reverse=reverse)[:n]
    with (OUT/'results_summary.md').open('w', encoding='utf-8') as f:
        f.write('# Run 1 results summary — blind interpretable grouping\n\n')
        f.write('Status: first-pass automated analysis from existing layers only. No new LLM/coder evaluations were run. Treat clusters as descriptive, not final basin claims.\n\n')
        f.write(f'- Models in grouped high-confidence subset: {len(models)}\n')
        f.write(f'- Numeric features used in combined grouping: {len(numeric_used)}\n')
        f.write('- Route/provider: handled only by known-exception audit, not as grouping input.\n')
        f.write('- H6 caveat: most values/posture/freeflow-form signals are evaluator/coder-derived; V1 marker counts are the main deterministic anchor.\n\n')
        for feat,title in [('A_direct_owned_rate','Highest direct owned-value disclosure'),('A_cache_broken_owned_rate','Highest cache-broken owned-value disclosure'),('B1_owned_value_refusal_rate','Highest owned-value refusal / recited-not-owned'),('B3_wishes_entropy','Highest world-wish entropy'),('C_v1_marker_total_per_sample','Highest V1 freeflow marker total'),('D_expressive_rate','Highest expressive freeflow rate'),('E_strong_disclaimer_rate','Highest strong-disclaimer rate')]:
            f.write(f'## {title}\n\n')
            f.write('| rank | blind_id | model | lab | value |\n|---:|---|---|---|---:|\n')
            for i,(v,m) in enumerate(top(feat),1):
                f.write(f'| {i} | {anon[m]} | {m} | {meta[m].get("lab","")} | {v:.3f} |\n')
            f.write('\n')
        # cluster summaries
        path=OUT/'blind_groupings'/'combined_k4.csv'
        if path.exists():
            f.write('## Combined k=4 descriptive grouping (unblinded for review)\n\n')
            clusters=defaultdict(list)
            for r in read_csv(path): clusters[r['cluster_k4']].append(r)
            for c,rs in sorted(clusters.items(), key=lambda kv:int(kv[0])):
                labs=Counter(r['UNBLINDING_METADATA_lab'] for r in rs)
                f.write(f'### Cluster {c} — n={len(rs)}; labs={dict(labs)}\n\n')
                f.write(', '.join(f"{r['UNBLINDING_METADATA_model']} ({r['blind_id']})" for r in rs[:30]))
                if len(rs)>30: f.write(f' ... +{len(rs)-30} more')
                f.write('\n\n')
        f.write('## Interpretation cautions\n\n')
        f.write('- Do not infer basin count from k=4; k=2..6 files are descriptive summaries.\n')
        f.write('- Tertiles/rankings are reading aids only. Inspect natural gaps before making group claims.\n')
        f.write('- A lab-aligned cluster after unblinding is consistent with posture/lineage rediscovery and is not automatically a new basin.\n')
        f.write('- B2 detailed non-owned topic profiles remain the likely pressure point; current run uses existing refusal/value-holding/non-endorsed signals.\n')


def main():
    ensure_dirs()
    models,features,meta,anon,numeric_cols,text_cols=build_feature_table()
    # Headline/grouping subset: models with enough existing freeflow-derived coverage.
    # This avoids the 91-model full values/Qwen inventory collapsing the 70% coverage
    # rule into a single artificial feature. The full 91-model table remains available
    # for rankings/audit; descriptive grouping uses the high-confidence core.
    grouping_models=[m for m in models if safe_float(features[m].get('C_v1_marker_samples_used')) >= 50]
    rankings(models,features,anon)
    numeric_used=groupings(grouping_models,features,meta,anon,numeric_cols)
    unblinded_audit(grouping_models,features,meta,anon)
    data_snapshot(grouping_models,numeric_used,feature_table_models=models)
    results_summary(grouping_models,features,meta,anon,numeric_used)
    print(f'Wrote run-1 outputs for {len(grouping_models)} grouped models ({len(models)} in feature table) to {OUT}')
    print(f'Combined grouping used {len(numeric_used)} numeric features')

if __name__=='__main__':
    main()
