#!/usr/bin/env python3
"""One content file -> semantic scaffold -> landscape CSS -> six verified pages."""
from __future__ import annotations
import argparse,asyncio,hashlib,html,importlib.metadata,importlib.util,json,os,platform,re,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import render as legacy
KINDS=['understand','transmit','diagnose','integrate','value','act']
SLOTS=[['definition','value','examples','tows','tows_note','boundary'],['pitch','postulate','flow','levers','objections','exercise'],['effect','branches','causal_chain','loop','pilot'],['taxonomy','levels','rule','programme'],['porter_note','functions','support','discovery'],['selection_note','use_cases','matrix_note','score_legend','prompt','pilot']]
ESC=html.escape

def h(text):return ESC(str(text))
def md(text):return legacy.composition.md(text)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_sheet(path):
    data=json.loads(path.read_text());validate(data,path.parent);return data

def validate(data,folder):
    import jsonschema
    schema=json.loads((HERE.parents[1]/'contracts/pedagogical-sheet.schema.json').read_text())
    jsonschema.Draft202012Validator(schema).validate(data)
    if [p['kind'] for p in data['pages']]!=KINDS:raise ValueError('Six ordered semantic pages required')
    source_ids={x['id'] for x in data['sources']}
    if len(source_ids)!=len(data['sources']):raise ValueError('Duplicate source ID')
    for i,page in enumerate(data['pages']):
        if set(page['content'])!=set(SLOTS[i]):raise ValueError('Missing or unknown semantic slot on page '+str(i+1))
        if not set(page['source_ids'])<=source_ids:raise ValueError('Unknown source reference')
        for ref in re.findall(r'\[(S\d+)\]',json.dumps(page,ensure_ascii=False)):
            if ref not in source_ids:raise ValueError('Unknown inline source '+ref)
    def no_html(value):
        if isinstance(value,str) and re.search(r'<\s*/?\s*[a-zA-Z][^>]*>',value):raise ValueError('Content must not contain HTML or CSS')
        if isinstance(value,dict):
            for k,v in value.items():
                if k in ('css','style','layout','html'):raise ValueError('Presentation belongs to scaffold/CSS')
                no_html(v)
        if isinstance(value,list):
            for v in value:no_html(v)
    no_html(data)
    if [x['posture'] for x in data['pages'][0]['content']['tows']]!=['Offensive','Défensive','Opportuniste','Préservation']:raise ValueError('Four TOWS postures required')
    if {x['name'] for x in data['pages'][2]['content']['branches']}!={'Processus','Outils','Compétences','Données','Gouvernance'}:raise ValueError('Five systemic branches required')
    if [x['name'] for x in data['pages'][3]['content']['levels']]!=['Assistant','Copilot','Autopilot','Agent']:raise ValueError('Preserve the four source solution types')
    if len(data['pages'][4]['content']['functions'])!=4:raise ValueError('Four business functions required')
    cases=data['pages'][5]['content']['use_cases']
    if not 3<=len(cases)<=5 or len({x['id'] for x in cases})!=len(cases):raise ValueError('Select 3 to 5 distinct use cases')
    catalog=json.loads((folder/data['catalog_ref']).read_text())
    if len(catalog['items'])!=len({x['id'] for x in catalog['items']}) or not {f'UC-{n:03d}' for n in range(1,71)}<={x['id'] for x in catalog['items']}:raise ValueError('Keep all 70 source situations; additions may extend the catalog')
    ids={x['id'] for x in catalog['items']}
    for case in cases:
        if case['id'] not in ids:raise ValueError('Unknown catalog case')
        if len(case['scores'])!=5 or any(type(v)!=int or not 1<=v<=3 for v in case['scores']):raise ValueError('Five ordinal scores in 1..3 required')
        if any(type(case[k])!=int or not 1<=case[k]<=3 for k in ('integration','automation')):raise ValueError('Axes must be in 1..3')
    return data

def card(title,body,cls='card'):
    return '<article class="'+cls+'" data-card data-layout-box><h2>'+h(title)+'</h2>'+body+'</article>'
def small(text):return '<div class="small">'+md(text)+'</div>'
def note(text,cls='note'):return '<aside class="'+cls+'">'+md(text)+'</aside>'

def page_understand(c):
    examples=''.join('<div class="sense"><h3>'+h(x['title'])+'</h3>'+md(x['text'])+'</div>' for x in c['examples'])
    left='<div class="understand-left">'+md(c['definition'])+note(c['value'],'value-note')+examples+'</div>'
    stories=''.join(card(x['posture']+' · '+x['cross'], '<p class="factor">'+h(x['factors'])+'</p>'+md(x['story'])+'<div class="lesson">'+md('**À retenir :** '+x['lesson'])+'</div>','tows-card') for x in c['tows'])
    return '<div class="understand-grid" data-overlap-check>'+left+'<div class="understand-right">'+small(c['tows_note'])+'<div class="tows-grid" data-overlap-check>'+stories+'</div>'+note(c['boundary'])+'</div></div>'

def page_transmit(c):
    flow='<ol class="flow">'+''.join('<li><b>'+h(x['title'])+'</b><span>'+h(x['text'])+'</span></li>' for x in c['flow'])+'</ol>'
    e=c['exercise']
    pitch=card('Le pitch · 30 secondes',md('« '+c['pitch'].strip('« »')+' »')+small(c['postulate']),'pitch-card')
    levers=card('Trois leviers de conviction',''.join('<section><h3>'+h(x['title'])+'</h3>'+md(x['text'])+'</section>' for x in c['levers']))
    objections=card('Répondre sans surpromettre',''.join('<section><h3>'+h(x['objection'])+'</h3>'+md(x['answer'])+'</section>' for x in c['objections']))
    exercise='<div class="exercise"><h2>'+h(e['title'])+'</h2><div class="exercise-steps">'+''.join('<p>'+h(x)+'</p>' for x in e['steps'])+'</div>'+small('**Vérifier :** '+e['check'])+'</div>'
    return flow+'<div class="transmit-columns three-grid">'+pitch+levers+objections+'</div>'+exercise

def fishbone(c):
    positions=[(115,13,210,49),(310,82,390,49),(455,13,550,49),(625,82,700,49),(755,13,845,49)]
    byname={x['name']:x for x in c['branches']}
    parts=['<svg class="fishbone" viewBox="0 0 1060 102" role="img" aria-label="Cinq causes systémiques de la qualité de perception"><path d="M15 49 H935" class="spine"/>']
    for name,(x,y,ex,ey) in zip(['Processus','Outils','Compétences','Données','Gouvernance'],positions):
        item=byname[name];liney=y+19 if y<49 else y-16
        parts.append(f'<path d="M{x} {liney} L{ex} {ey}" class="rib"/><text x="{x}" y="{y}" text-anchor="middle" class="branch-name">{h(name)}</text><text x="{x}" y="{y+16}" text-anchor="middle" class="branch-risk">{h(item["risk_short"])}</text>')
    parts.append('<rect x="935" y="28" width="120" height="43" rx="7" class="effect-box"/><text x="995" y="47" text-anchor="middle" class="effect-text">Valeur fiable</text><text x="995" y="64" text-anchor="middle" class="effect-text">moins de reprises</text></svg>')
    return ''.join(parts)

def page_diagnose(c):
    rows=''.join('<tr><th scope="row">'+h(x['name'])+'<span>'+h(x['question'])+'</span></th><td>'+md(x['obstacle'])+'</td><td>'+md(x['lever'])+'</td><td>'+md('**'+x['owner']+'** '+x['signal'])+'</td></tr>' for x in c['branches'])
    table='<table class="system-table"><thead><tr><th>Branche / question</th><th>Ce qui bloque l’adoption</th><th>Levier de diffusion</th><th>Responsable / preuve de progrès</th></tr></thead><tbody>'+rows+'</tbody></table>'
    chain='<div class="causal-chain">'+'<span class="arrow">→</span>'.join('<b>'+h(x)+'</b>' for x in c['causal_chain'])+'</div>'
    p=c['pilot'];bottom='<div class="two-grid">'+note(c['loop'])+card(p['title'],md(p['text'])+small(p['questions']))+'</div>'
    return fishbone(c)+table+chain+bottom

def page_integrate(c):
    taxonomy=card('Trois aptitudes opérationnelles',''.join('<section><h3>'+h(x['name'])+'</h3>'+md(x['meaning'])+md(x['limit'])+small('**Corpus :** '+x['cases'])+'</section>' for x in c['taxonomy']))
    levels='<table class="levels-table"><thead><tr><th>Configuration</th><th>Intégration / automatisation</th><th>Exemple de conception</th><th>Contrôle</th></tr></thead><tbody>'+''.join('<tr><th>'+h(x['name'])+'<span>'+h(x['horizon'])+'</span></th><td>'+h(x['integration'])+' / '+h(x['automation'])+'</td><td>'+md(x['example'])+'</td><td>'+md(x['control'])+'</td></tr>' for x in c['levels'])+'</tbody></table>'
    p=c['programme'];return '<div class="integrate-upper">'+taxonomy+'<div>'+levels+note(c['rule'])+'</div></div>'+note('**'+p['title']+' :** '+p['text']+' **Évaluation :** '+p['assessment'],'programme-note note')

def page_value(c):
    columns=[]
    for i,x in enumerate(c['functions'],1):
        body='<p class="icp">'+h(x['icp'])+'</p>'+md('**Douleur :** '+x['pain'])+'<blockquote>'+h(x['talk'])+'</blockquote>'+md('**Cas :** '+x['cases'])+md('**Briques :** '+x['enablers'])+md('**Mesure :** '+x['measure'])
        columns.append(card(str(i)+' · '+x['name'],body,'function-column'))
    return small(c['porter_note'])+'<div class="four-grid functions" data-overlap-check>'+''.join(columns)+'</div><div class="two-grid value-bottom">'+note(c['support'])+note(c['discovery'])+'</div>'

def integration_matrix(c):
    parts=['<svg class="matrix" viewBox="0 0 420 165" role="img" aria-label="Automatisation en abscisse, intégration en ordonnée"><text x="32" y="12" class="axis">Intégration forte ↑</text>']
    for y,a,b in [(20,'Copilot','Agent'),(80,'Assistant','Autopilot')]:
        for x,label in [(32,a),(218,b)]:parts.append(f'<rect x="{x}" y="{y}" width="186" height="60" class="quadrant"/><text x="{x+7}" y="{y+17}" class="quadrant-name">{h(label)}</text>')
    grouped={}
    for case in c['use_cases']:grouped.setdefault((case['automation'],case['integration']),[]).append(case['id'].replace('UC-',''))
    for (automation,integration),ids in grouped.items():
        x={1:80,2:218,3:355}[automation];y={1:122,2:80,3:55}[integration];label_y=y-5 if integration==2 else y+5
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" class="point"/><text x="{x+7}" y="{label_y}" class="point-label">{h("/".join(ids))}</text>')
    parts.append('<text x="32" y="162" class="axis">Automatisation faible → forte</text></svg>');return ''.join(parts)

def page_act(c):
    rows=[]
    for x in c['use_cases']:
        scores='<div class="scores">'+''.join('<span>'+label+' <b data-score="'+str(v)+'">'+'★'*v+'</b></span>' for label,v in zip(['V','C','R','X','G'],x['scores']))+'</div>'
        bac=''.join('<p><b>'+label+'</b> '+h(x[key])+'</p>' for label,key in [('B ·','benefit'),('A ·','advantage'),('C ·','characteristic')])
        rows.append('<tr><th>'+h(x['id'])+'<span>'+h(x['title'])+'</span><em>'+h(x['owner'])+'</em></th><td>'+bac+'</td><td>'+scores+'</td><td>'+md(x['measure'])+'</td></tr>')
    table='<table class="case-table"><thead><tr><th>Cas / interlocuteur</th><th>Bénéfice · Avantage · Caractéristique</th><th>Notes / 3</th><th>Mesure et contrôle</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    left='<div class="case-side">'+table+'</div>'
    right='<div class="pilot-side"><h2>Automatisation × intégration</h2>'+integration_matrix(c)+small(c['matrix_note'])+card('Prompt d’essai · UC-021',md('« '+c['prompt']+' »'),'prompt-card')+note(c['pilot'])+'</div>'
    return '<div class="selection-note small">'+md(c['selection_note'])+'</div><div class="action-grid">'+left+right+'</div>'+small(c['score_legend'])

BUILDERS=[page_understand,page_transmit,page_diagnose,page_integrate,page_value,page_act]

def scaffold(data):
    sources={x['id']:x for x in data['sources']};pages=[]
    for i,(page,builder) in enumerate(zip(data['pages'],BUILDERS),1):
        src=' · '.join('<a href="'+h(sources[k]['url'])+'">'+h(k+' '+sources[k]['title'].split(' — ')[0])+'</a>' if sources[k]['url'] else h(k+' Corpus fourni') for k in page['source_ids'])
        pages.append('<section class="page p'+str(i)+'" data-no-overflow aria-label="'+h(f'Page {i} : {page["title"]}')+'"><header><div class="eyebrow">POUR ALLER PLUS LOIN <span>IA EN ENTREPRISE · '+h(data['title'].upper())+' · '+str(i)+' / 6</span></div><h1>'+h(page['title'])+'</h1><p class="page-lead">'+h(page['lead'])+'</p></header><main data-no-overflow>'+builder(page['content'])+'</main><aside class="takeaway">'+md('**À retenir →** '+page['takeaway'])+'</aside><footer><div>'+src+'</div><b>'+h(data['title'].upper())+' · '+str(i)+' / 6</b></footer></section>')
    template=(HERE/'landscape.html').read_text();return template.replace('{{TITLE}}',h(data['title'])).replace('{{PAGES}}',''.join(pages))

def as_markdown(data):
    out=['# Fiche — '+data['title'],'',data['subtitle'],'','**Source :** livre et cas documentés; références en fin de fiche.','']
    def walk(obj):
        if isinstance(obj,str):return [obj,'']
        if isinstance(obj,list):return sum((walk(x) for x in obj),[])
        if isinstance(obj,dict):
            result=[]
            for k,v in obj.items():
                if k in ('scores','automation','integration'):continue
                if k in ('title','name','posture'):result+=['### '+str(v),'']
                else:result+=walk(v)
            return result
        return []
    for i,page in enumerate(data['pages'],1):
        out+=['## Page '+str(i)+' — '+page['title'],'',page['lead'],'']+walk(page['content'])
        if page['kind']=='act':
            out+=['| Cas | BAC | Valeur | Coût | Risque | Complexité | Généricité |','|---|---|---:|---:|---:|---:|---:|']
            for x in page['content']['use_cases']:out+=['| '+x['id']+' '+x['title']+' | B : '+x['benefit']+'; A : '+x['advantage']+'; C : '+x['characteristic']+' | '+' | '.join(str(v) for v in x['scores'])+' |']
        out+=['','**Takeaway :** '+page['takeaway'],'']
    out+=['## Sources et statuts','']
    for s in data['sources']:out+=['- **'+s['id']+'** '+s['title']+' — '+s['locator']+'. '+s['status']+'. '+s['url']]
    return '\n'.join(out)+'\n'

async def render(source,out):
    from playwright.async_api import async_playwright
    from pypdf import PdfReader
    legacy.verify_upstream();data=load_sheet(source);out.mkdir(parents=True,exist_ok=True)
    base=scaffold(data);css=(HERE/'landscape.css').read_text()
    (out/'binding.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    (out/'scaffold.html').write_text(base)
    (out/'fiche.html').write_text(base.replace('</head>','<style>'+css+'</style></head>'))
    (out/'fiche.md').write_text(as_markdown(data))
    os.environ.setdefault('NICE_CHROMIUM_PATH',shutil.which('google-chrome') or shutil.which('chromium') or '')
    async with async_playwright() as pw:
        browser=await legacy.launch(pw);version=browser.version
        page=await browser.new_page(viewport={'width':1250,'height':900},device_scale_factor=1.5)
        await page.set_content((out/'fiche.html').read_text(),wait_until='networkidle');await page.evaluate('document.fonts.ready')
        qa=await page.evaluate(legacy.layout_qa.JS)
        qa['page_metrics']=await page.locator('.page').evaluate_all('(pages)=>pages.map(p=>({width:p.clientWidth,height:p.clientHeight,main:p.querySelector("main").clientHeight,main_scroll:p.querySelector("main").scrollHeight,words:p.innerText.split(/\\s+/).length}))')
        for i in range(6):await page.locator('.page').nth(i).screenshot(path=str(out/f'page-{i+1:02d}.png'))
        await page.pdf(path=str(out/'fiche.pdf'),format='A4',landscape=True,print_background=True,prefer_css_page_size=True)
        await browser.close()
    pdf=PdfReader(out/'fiche.pdf');keys=('overlaps','overflows','out_of_bounds','small_fonts','low_padding')
    qa['summary']={k:sum(len(p[k]) for p in qa['pages']) for k in keys}
    qa['physical_pages']=len(pdf.pages);qa['landscape']=all(float(p.mediabox.width)>float(p.mediabox.height) for p in pdf.pages)
    qa['nonempty']=all(len(p.extract_text().strip())>500 for p in pdf.pages)
    qa['pass']=qa['page_count']==6 and qa['physical_pages']==6 and qa['landscape'] and qa['nonempty'] and not any(qa['summary'].values())
    qa['visual_review']='PENDING';qa['editorial_status']=data['status'];qa['build_revision']=os.environ.get('GITHUB_SHA')
    qa['source_sha256']=sha(source);qa['catalog_sha256']=sha(source.parent/data['catalog_ref'])
    qa['runtime']={'python':platform.python_version(),'chromium':version,**{p:importlib.metadata.version(p) for p in ('Markdown','playwright','pypdf','jsonschema')}}
    qa['runtime_hashes']={name:sha(HERE/name) for name in ('landscape.py','landscape.css','landscape.html','upstream-lock.json')}
    qa['outputs']={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and (p.name.startswith('page-') or p.name in ('binding.json','scaffold.html','fiche.html','fiche.pdf','fiche.md'))}
    (out/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));return qa

def verify(source,out):
    from pypdf import PdfReader
    data=load_sheet(source);qa=json.loads((out/'qa.json').read_text())
    if not qa['pass'] or qa['source_sha256']!=sha(source) or qa['catalog_sha256']!=sha(source.parent/data['catalog_ref']):raise ValueError('Failed or stale build')
    required={'binding.json','scaffold.html','fiche.html','fiche.pdf','fiche.md',*[f'page-{i:02d}.png' for i in range(1,7)]}
    if not required<=set(qa['outputs']):raise ValueError('Missing output')
    for name,digest in qa['outputs'].items():
        if Path(name).name!=name or sha(out/name)!=digest:raise ValueError('Modified output: '+name)
    for name,digest in qa['runtime_hashes'].items():
        if sha(HERE/name)!=digest:raise ValueError('Modified renderer')
    if json.loads((out/'binding.json').read_text())!=data or (out/'scaffold.html').read_text()!=scaffold(data):raise ValueError('Binding/scaffold mismatch')
    pdf=PdfReader(out/'fiche.pdf')
    if len(pdf.pages)!=6 or any(float(p.mediabox.width)<=float(p.mediabox.height) for p in pdf.pages):raise ValueError('Not six landscape pages')
    return {'pass':True,'physical_pages':6,'landscape':True,'build_revision':qa.get('build_revision'),'summary':qa['summary']}

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--verify',action='store_true');p.add_argument('--html-only',action='store_true');p.add_argument('--export-markdown',type=Path);a=p.parse_args()
    if a.export_markdown:a.export_markdown.write_text(as_markdown(load_sheet(a.source)));return
    if a.verify:print(json.dumps(verify(a.source,a.out),indent=2));return
    if a.html_only:
        data=load_sheet(a.source);a.out.mkdir(parents=True,exist_ok=True);base=scaffold(data);(a.out/'scaffold.html').write_text(base);(a.out/'fiche.html').write_text(base.replace('</head>','<style>'+(HERE/'landscape.css').read_text()+'</style></head>'));return
    q=asyncio.run(render(a.source,a.out));print(json.dumps({k:q[k] for k in ('pass','physical_pages','landscape','summary','page_metrics')},indent=2))
    if not q['pass']:raise SystemExit(2)
    print(json.dumps(verify(a.source,a.out),indent=2))
if __name__=='__main__':main()
