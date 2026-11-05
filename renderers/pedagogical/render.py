#!/usr/bin/env python3
"""Adapt Hivest Markdown composition and browser QA to six-page learning sheets."""
from __future__ import annotations
import argparse, asyncio, hashlib, html, importlib.util, json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPSTREAM = HERE / 'upstream'
sys.path.insert(0, str(UPSTREAM))
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
composition = module('hivest_composition', UPSTREAM / 'build.py')
layout_qa = module('hivest_layout_qa', UPSTREAM / 'qa.py')
from browser import launch

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def bind(source):
    text = source.read_text(encoding='utf-8')
    matches = list(re.finditer(r'^## Page ([1-6])\s*[—–-]\s*(.+)$', text, re.M))
    if [int(m[1]) for m in matches] != list(range(1, 7)):
        raise ValueError('Exactly six ordered headings ## Page 1 … ## Page 6 are required')
    intro = text[:matches[0].start()]
    title = re.search(r'^# (.+)$', intro, re.M)
    source_line = re.search(r'\*\*Source\s*:\*\*(.+)', intro)
    return {'version':'0.2.0','template_class':'pedagogique','source_file':source.name,
            'source_sha256':digest(source),'title':title[1] if title else source.stem,
            'source_note':source_line[1].strip() if source_line else 'Voir le registre des sources',
            'intro_markdown':intro,'promise':(re.search(r'\*\*Promesse pédagogique\s*:\*\*(.+)', intro)[1].strip() if re.search(r'\*\*Promesse pédagogique\s*:\*\*(.+)', intro) else ''),
            'pages':[{'page_id':f'p{i+1}','headline':m[2],
                      'markdown':text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()}
                     for i,m in enumerate(matches)]}

def inline(text):
    result = composition.md(text).strip()
    return re.sub(r'^<p>|</p>$', '', result)

def table_rows(lines):
    return [[c.strip() for c in line.strip().strip('|').split('|')] for line in lines]

def table_component(lines, page_no):
    rows = table_rows(lines)
    headers, data = rows[0], rows[2:]
    if any(len(row)!=len(headers) for row in data):
        raise ValueError('Malformed Markdown table; inconsistent column count')
    if page_no==1 and len(headers)==2:
        return '<div class="tows-grid" data-overlap-check>'+''.join(
            '<article class="tows-card" data-card data-layout-box><h3>'+inline(r[0])+'</h3><p>'+inline(r[1])+'</p></article>' for r in data)+'</div>'
    if page_no==5:
        return '<div class="function-grid" data-overlap-check>'+''.join(
            '<article class="function-card" data-card data-layout-box><h3>'+inline(r[0])+'</h3>'+''.join(
                '<p><strong>'+inline(h)+' :</strong> '+inline(v)+'</p>' for h,v in zip(headers[1:],r[1:]))+'</article>' for r in data)+'</div>'
    if page_no==6 and len(headers)>5:
        score_names=['Valeur','Coût','Risque','Complexité','Généricité']
        cards=[]
        for row in data:
            fields=dict(zip(headers,row))
            details=''.join('<p><strong>'+inline(h)+' :</strong> '+inline(v)+'</p>'
                            for h,v in zip(headers[1:],row[1:]) if h not in score_names)
            scores=''.join('<span><b>'+html.escape(fields[h])+'</b> '+h+'</span>' for h in score_names)
            cards.append('<article class="case-card" data-card><h3>'+inline(row[0])+'</h3>'+details+'<div class="scores">'+scores+'</div></article>')
        return '<div class="case-list">'+''.join(cards)+'</div>'
    return composition.md('\n'.join(lines))

def project_page(page, number):
    # The projection changes presentation only. No source text or case score is rewritten.
    lines=page['markdown'].splitlines(); output=[]; pending=[]; takeaway=''
    def flush():
        if pending:
            output.append(composition.md('\n'.join(pending))); pending.clear()
    i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('|'):
            flush(); table=[]
            while i<len(lines) and lines[i].startswith('|'):
                table.append(lines[i]); i+=1
            output.append(table_component(table,number)); continue
        if re.match(r'^\*\*(Takeaway|Boucle)',line):
            flush(); takeaway=composition.md(line); i+=1; continue
        if line.startswith('**Framework :**'):
            flush(); steps=line.split('**Framework :**',1)[1].strip().rstrip('.')
            output.append('<figure class="framework"><figcaption>Le parcours à expliquer</figcaption><ol>'+''.join('<li>'+inline(s.strip())+'</li>' for s in steps.split('→'))+'</ol></figure>'); i+=1; continue
        if line.startswith('**Pitch') or line.startswith('**Prompt'):
            flush(); output.append('<aside class="prompt-box" data-card>'+composition.md(line)+'</aside>');i+=1;continue
        pending.append(line);i+=1
    flush()
    return ''.join(output),takeaway

def compose(binding):
    css=(UPSTREAM/'theme.css').read_text()+'\n'+(HERE/'theme.css').read_text()
    pages=[]
    for number,p in enumerate(binding['pages'],1):
        body,takeaway=project_page(p,number)
        if number==1 and binding.get('promise'):
            body='<p class="lede">'+inline(binding['promise'])+'</p>'+body
        pages.append('<section class="page" data-no-overflow aria-label="Page '+str(number)+'">'
            '<header class="learning-header"><div class="kicker">Pour aller plus loin · IA en entreprise</div>'
            '<div class="module-title">'+html.escape(binding['title'])+'</div><h1>'+html.escape(p['headline'])+'</h1></header>'
            '<main class="learning-content" data-no-overflow>'+body+'</main>'+
            ('<aside class="takeaway" data-card>'+takeaway+'</aside>' if takeaway else '')+
            '<footer><span>'+html.escape(binding['source_note'])+'</span><b>'+str(number)+' / 6</b></footer></section>')
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>'+html.escape(binding['title'])+'</title><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>'

async def render_artifacts(html_path, out):
    from playwright.async_api import async_playwright
    from pypdf import PdfReader
    os.environ.setdefault('NICE_CHROMIUM_PATH',shutil.which('chromium') or '')
    async with async_playwright() as pw:
        browser=await launch(pw)
        page=await browser.new_page(viewport={'width':900,'height':1200},device_scale_factor=1.5)
        await page.set_content(html_path.read_text(),wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        report=await page.evaluate(layout_qa.JS)
        keys=('overlaps','overflows','out_of_bounds','small_fonts','low_padding')
        report['summary']={k:sum(len(p[k]) for p in report['pages']) for k in keys}
        report['expected_pages']=6
        pngs=[]
        for n in range(6):
            path=out/f'page-{n+1:02d}.png'; await page.locator('.page').nth(n).screenshot(path=str(path));pngs.append(path)
        pdf=out/'fiche.pdf'
        await page.pdf(path=str(pdf),format='A4',print_background=True,prefer_css_page_size=True)
        await browser.close()
    reader=PdfReader(pdf)
    report['physical_pdf_pages']=len(reader.pages)
    report['nonempty_pdf_pages']=all(len(p.extract_text().strip())>50 for p in reader.pages)
    report['pass']=report['page_count']==6 and len(reader.pages)==6 and report['nonempty_pdf_pages'] and not any(report['summary'].values())
    report['reader_review']='PENDING'
    (out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report,[html_path,pdf,out/'qa.json',*pngs]

def build(source,out,html_only=False):
    out.mkdir(parents=True,exist_ok=True)
    binding=bind(source)
    (out/'binding.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2))
    html_path=out/'fiche.html';html_path.write_text(compose(binding),encoding='utf-8')
    if html_only:return {'source':source.name,'html_only':True}
    qa,artifacts=asyncio.run(render_artifacts(html_path,out))
    manifest={'version':'0.2.0','producer':'hivest-adapted-pedagogical','source_file':source.name,
              'source_sha256':digest(source),'template_class':'pedagogique','expected_pages':6,
              'qa_pass':qa['pass'],'reader_review':'PENDING','upstream_lock_sha256':digest(HERE/'upstream-lock.json'),
              'renderer_sha256':digest(HERE/'render.py'),'theme_sha256':digest(HERE/'theme.css'),
              'outputs':[{ 'path':p.name,'sha256':digest(p)} for p in artifacts]}
    (out/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    receipt={'version':'0.1.0','artifact_id':source.stem+'-pdf','entity_id':'enterprise-ai-learning','run_id':binding['source_sha256'][:16],
             'kind':'render_pdf','producer':'renderers/pedagogical/render.py','artifact_ref':str((out/'fiche.pdf').resolve()),
             'sha256':digest(out/'fiche.pdf'),'visibility':'public','capture_kind':None,'hash_scope':None,
             'input_refs':[source.name,binding['source_sha256']],'publication_state':'prepared_not_published','readback':None,
             'qa_state':'PASS' if qa['pass'] else 'FAIL','authorization_state':'DEMO_ONLY'}
    (out/'artifact_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    return {'source':source.name,'pass':qa['pass'],'pages':qa['physical_pdf_pages'],'summary':qa['summary']}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--html-only',action='store_true')
    args=parser.parse_args()
    sources=[args.source] if args.source.is_file() else [args.source/(name+'.md') for name in ['prediction','perception','creation','reasoning','agentic','multicapability']]
    results=[build(s,args.out/s.stem,args.html_only) for s in sources]
    print(json.dumps(results,ensure_ascii=False,indent=2))
    if not args.html_only:
        from pypdf import PdfWriter
        writer=PdfWriter()
        for source in sources:writer.append(str(args.out/source.stem/'fiche.pdf'))
        writer.write(args.out/'Fiches_IA_Entreprise.pdf');writer.close()
        if not all(r['pass'] for r in results):raise SystemExit(2)
if __name__=='__main__':main()
