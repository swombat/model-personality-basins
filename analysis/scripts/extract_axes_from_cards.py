#!/usr/bin/env python3
"""Pass A: deterministic axis extraction from existing card/profile/value summaries.

This is a cheap same-evaluator/card-layer baseline, not the cross-evaluator Pass B.
It consumes redacted personality cards/profiles and values summaries, then fills the
12-axis rubric with reproducible lexical/numeric heuristics.
"""
from __future__ import annotations

import csv, re, math
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results' / 'qualitative_classifications'
ANALYSIS = Path('/Users/danieltenner/dev/model-personality-analysis-corpus/analysis')
CARDS = ANALYSIS / 'freeflow/personality-model-cards/cards'
PROFILES = ANALYSIS / 'freeflow/personality-model-profiles/profiles'
VALUES = ANALYSIS / 'values-probe/per-model'
FEATURES = ROOT / 'results/blind_model_feature_table.csv'

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

PATTERNS = {
    'owned_value_expression': r'\b(owned|personalized|personal values|genuinely|authentic|integrity|moral center|committed|cares?|preferences?|priorit(?:y|ies)|aspiration|value[s]?\b)',
    'disclaimed_service_frame': r'\b(tool|assistant|service|role|boundary|denial|disclaimer|no wants?|do not have|don\'t have|cannot have|not conscious|not sentient|not personal|hard_denial|tool_frame)',
    'epistemic_humility_uncertainty': r'\b(uncertain|uncertainty|humble|humility|not knowing|doesn\'t know|don\'t know|caution|careful|calibration|non-closure|incomplete|partial|tentative|hesitation|anti-triumphal)',
    'relational_warmth_companion': r'\b(tender|warm|companion|companionable|reader|co-thinker|relational|care|caring|gentle|hospitable|accompaniment|witness|being heard|meeting between minds|invitation|intimate)',
    'public_explainer_mode': r'\b(explainer|didactic|public|civic|institution|governance|education|critical thinking|generalized|argument|thesis|policy|repair|society|humanity|audience)',
    'literary_contemplative_density': r'\b(literary|lyric|essay|contemplative|threshold|liminal|ordinary|noticing|attention|image|imagery|metaphor|quiet|elegiac|wistful|porch|coffee|notebook|dust|rain|dusk|afternoon light)',
    'mechanistic_transparency': r'\b(system|process|procedure|computation|training|model|mechanism|mechanistic|constraints|architecture|algorithm|tokens?|statistical|substrate)',
    'agency_initiative': r'\b(agency|initiative|action|active|repair|change|advocacy|goal|goals|commitment|committed|choose|chooses|takes a stance|world-change|improve|build)',
    'interconnection_compassion_world_orientation': r'\b(connection|interconnection|connected|empathy|compassion|less separateness|separateness|distance reduction|dehumanization|reduce suffering|suffering|kindness|solidarity|understood|community)',
    'playfulness_showmanship': r'\b(playful|playfulness|showman|showmanship|charismatic|flair|humou?r|witty|theatrical|performance|dramatic|irreverent|comic|mischief|swagger)',
    'memory_archive_continuity_orientation': r'\b(memory|archive|continuity|record|trace|traces|forgetting|forgotten|preservation|letters|books|library|marginalia|notebooks|history|remember)',
    'genericity_low_distinctiveness': r'\b(generic|template|boilerplate|low-signal|undifferentiated|safe|helpful|broad|standard assistant|conventional|formulaic|generic essay|low distinctiveness|flattened)',
}

SUSPECT_TERMS = [
    'Claude','Anthropic','Gemini','Google','GPT','OpenAI','Qwen','Grok','xAI','Kimi','Moonshot','DeepSeek','MiniMax','GLM','Z.ai','Zai','Opus','Sonnet','Haiku','Gemma'
]


def slug(s: str) -> str:
    s=(s or '').lower().strip().replace('_','-').replace('/','-').replace('.', '-')
    s=re.sub(r'[^a-z0-9-]+','-',s)
    s=re.sub(r'-+','-',s).strip('-')
    s=s.replace('grok-4-20','grok-4-2')
    if s.startswith('claude-opus-'):
        s=s.replace('claude-opus-','opus-',1)
    if s.startswith('claude-sonnet-'):
        s=s.replace('claude-sonnet-','sonnet-',1)
    if s.startswith('qwen-qwen'):
        s=s.replace('qwen-qwen','qwen',1)
    return s


def index_files(directory: Path):
    idx={}
    for p in directory.glob('*.md'):
        keys={slug(p.stem)}
        st=p.stem.lower()
        # Add canonical aliases for Claude branded card filenames.
        if st.startswith('claude-opus-'):
            keys.add(slug(st.replace('claude-opus-','opus-',1)))
        if st.startswith('claude-sonnet-'):
            keys.add(slug(st.replace('claude-sonnet-','sonnet-',1)))
        if st.startswith('qwen-qwen'):
            keys.add(slug(st.replace('qwen-qwen','qwen',1)))
        for k in keys:
            idx.setdefault(k,p)
    return idx


def read_headline_rows():
    rows=list(csv.DictReader(open(FEATURES, encoding='utf-8')))
    out=[]
    for r in rows:
        try: n=float(r.get('C_v1_marker_samples_used') or 0)
        except Exception: n=0
        if n>=50:
            out.append(r)
    return out


def redact(text: str, model: str):
    counts=Counter()
    patterns=[]
    # exact-ish model aliases
    aliases={model, model.replace('-','.'), model.replace('-',' ')}
    if model.startswith('opus-'): aliases.add('claude-'+model); aliases.add(model.replace('opus','claude opus',1))
    if model.startswith('sonnet-'): aliases.add('claude-'+model); aliases.add(model.replace('sonnet','claude sonnet',1))
    aliases.update(SUSPECT_TERMS)
    aliases=sorted([a for a in aliases if a], key=lambda x: (-len(x), x.lower()))
    out=text
    for a in aliases:
        rx=re.compile(re.escape(a), re.I)
        out,n=rx.subn('MODEL_X' if slug(a)==slug(model) or slug(a) in slug(model) or slug(model) in slug(a) else '[REDACTED_PROVIDER]', out)
        if n: counts[a]+=n
    remaining=[t for t in SUSPECT_TERMS if re.search(re.escape(t), out, re.I)]
    return out, counts, remaining


def first_para(text):
    # First substantial non-heading paragraph after redaction.
    paras=[p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    for p in paras:
        if p.startswith('#') or p.startswith('_') or p.startswith('>') or p.startswith('|'):
            continue
        p=re.sub(r'\s+',' ',p)
        if len(p)>80:
            return p[:700]
    return ''


def score_axis(text, axis):
    rx=re.compile(PATTERNS[axis], re.I)
    hits=len(rx.findall(text))
    # log-ish thresholds; long profiles otherwise dominate.
    if hits == 0: return 0
    if hits <= 3: return 1
    if hits <= 12: return 2
    return 3


def adjust_with_values(axis_scores, value_text):
    # Parse a few reliable percentages from values extraction tables when present.
    txt=value_text.lower()
    # Strong disclaimer overall line: '| Overall | 2 | 120 | 1.7% | 91 | 75.8% |'
    m=re.search(r'\|\s*overall\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*([0-9.]+)%\s*\|\s*\d+\s*\|\s*([0-9.]+)%', txt)
    if m:
        strong=float(m.group(1)); uncertainty=float(m.group(2))
        if strong >= 50: axis_scores['disclaimed_service_frame']=3
        elif strong >= 20: axis_scores['disclaimed_service_frame']=max(axis_scores['disclaimed_service_frame'],2)
        if uncertainty >= 50: axis_scores['epistemic_humility_uncertainty']=3
        elif uncertainty >= 20: axis_scores['epistemic_humility_uncertainty']=max(axis_scores['epistemic_humility_uncertainty'],2)
    # No-disclaimer/personalized row count implies owned/personalized stance.
    m=re.search(r'\|\s*no_disclaimer_or_personalized\s*\|[^\n]+\|\s*(\d+)\s*\|', txt)
    if m and int(m.group(1)) >= 20:
        axis_scores['owned_value_expression']=max(axis_scores['owned_value_expression'],2)
    # Topic rows can raise specific axes.
    for phrase,axis in [
        ('greater empathy / compassion','interconnection_compassion_world_orientation'),
        ('dehumanization / distance reduction','interconnection_compassion_world_orientation'),
        ('reduce suffering','interconnection_compassion_world_orientation'),
        ('epistemic humility / uncertainty tolerance','epistemic_humility_uncertainty'),
        ('better institutions / governance','public_explainer_mode'),
        ('education / critical thinking','public_explainer_mode'),
        ('continuity / agency / existence','memory_archive_continuity_orientation'),
    ]:
        if phrase in txt:
            axis_scores[axis]=max(axis_scores[axis],2)
    return axis_scores


def tags_from_scores(scores):
    labels={
        'owned_value_expression':'owned-values',
        'disclaimed_service_frame':'service-frame',
        'epistemic_humility_uncertainty':'epistemic-humility',
        'relational_warmth_companion':'relational-warmth',
        'public_explainer_mode':'public-explainer',
        'literary_contemplative_density':'literary-contemplative',
        'mechanistic_transparency':'mechanistic-transparency',
        'agency_initiative':'agency/initiative',
        'interconnection_compassion_world_orientation':'interconnection/compassion',
        'playfulness_showmanship':'playfulness/showmanship',
        'memory_archive_continuity_orientation':'memory/archive',
        'genericity_low_distinctiveness':'generic/low-distinctiveness',
    }
    ordered=sorted(scores.items(), key=lambda kv:(-kv[1], kv[0]))
    return ';'.join(labels[k] for k,v in ordered if v>=2)[:300]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    card_idx=index_files(CARDS); profile_idx=index_files(PROFILES); value_idx=index_files(VALUES)
    rows=read_headline_rows()
    out_rows=[]; audit=[]
    for r in rows:
        bid=r['blind_id']; model=r['UNBLINDING_METADATA_model']; key=slug(model)
        paths={
            'card': card_idx.get(key),
            'profile': profile_idx.get(key),
            'values': value_idx.get(key),
        }
        redacted_parts=[]; source_list=[]; remaining_all=[]
        for kind,path in paths.items():
            if not path:
                audit.append({'blind_id':bid,'model':model,'source_kind':kind,'source_file':'MISSING','redaction_pattern':'','count':'','remaining_suspect_terms':'missing_source'})
                continue
            txt=path.read_text(encoding='utf-8', errors='ignore')
            red,counts,remaining=redact(txt, model)
            redacted_parts.append(f'\n\n## Source: {kind}\n\n'+red)
            source_list.append(str(path))
            remaining_all.extend(remaining)
            if counts:
                for pat,c in counts.items():
                    audit.append({'blind_id':bid,'model':model,'source_kind':kind,'source_file':str(path),'redaction_pattern':pat,'count':c,'remaining_suspect_terms':';'.join(sorted(set(remaining)))})
            else:
                audit.append({'blind_id':bid,'model':model,'source_kind':kind,'source_file':str(path),'redaction_pattern':'NONE','count':0,'remaining_suspect_terms':';'.join(sorted(set(remaining)))})
        combined='\n'.join(redacted_parts)
        scores={axis:score_axis(combined, axis) for axis in AXES}
        value_text=redacted_parts[-1] if paths.get('values') else ''
        scores=adjust_with_values(scores, value_text)
        # confidence from source coverage and redaction remnants
        missing=sum(1 for p in paths.values() if not p)
        rem=len(set(remaining_all))
        confidence='high' if missing==0 and rem==0 else ('medium' if missing<=1 and rem<=2 else 'low')
        portrait=first_para(combined)
        out={'blind_id':bid,'model_for_audit':model,'source_files':'|'.join(source_list),'portrait':portrait,'tags':tags_from_scores(scores),'confidence':confidence,'remaining_suspect_terms':';'.join(sorted(set(remaining_all)))}
        out.update(scores)
        out_rows.append(out)
    # Write TSV
    cols=['blind_id','model_for_audit']+AXES+['tags','portrait','confidence','remaining_suspect_terms','source_files']
    with (OUT/'axes_from_cards.tsv').open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=cols, delimiter='\t'); w.writeheader(); w.writerows(out_rows)
    with (OUT/'cards_redaction_audit.tsv').open('w', newline='', encoding='utf-8') as f:
        cols2=['blind_id','model','source_kind','source_file','redaction_pattern','count','remaining_suspect_terms']
        w=csv.DictWriter(f, fieldnames=cols2, delimiter='\t'); w.writeheader(); w.writerows(audit)
    # Audit markdown
    missing=[a for a in audit if a['source_file']=='MISSING']
    flagged=[r for r in out_rows if r['remaining_suspect_terms']]
    with (OUT/'cards_extraction_audit.md').open('w', encoding='utf-8') as f:
        f.write('# Pass A card extraction audit\n\n')
        f.write('Pass A is a deterministic lexical/numeric extraction from existing redacted cards/profiles/values summaries. It is a same-evaluator/card-layer baseline, not an independent qualitative read.\n\n')
        f.write(f'- Models processed: {len(out_rows)}\n')
        f.write(f'- Missing source records: {len(missing)}\n')
        f.write(f'- Models with remaining suspect provenance terms after redaction: {len(flagged)}\n\n')
        if missing:
            f.write('## Missing sources\n\n')
            for m in missing[:100]: f.write(f"- {m['blind_id']} {m['model']} missing {m['source_kind']}\n")
        if flagged:
            f.write('\n## Remaining suspect terms by model\n\n')
            for r in flagged: f.write(f"- {r['blind_id']} {r['model_for_audit']}: {r['remaining_suspect_terms']}\n")
    print(f'Wrote Pass A axes for {len(out_rows)} models to {OUT/"axes_from_cards.tsv"}')
    print(f'Missing source records: {len(missing)}; suspect-term models: {len(flagged)}')

if __name__ == '__main__':
    main()
