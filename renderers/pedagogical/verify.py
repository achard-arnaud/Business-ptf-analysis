#!/usr/bin/env python3
"""Verify source, runtime, output integrity and physical PDF against one real run."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render as renderer

REQUIRED={'binding.json','scaffold.html','fiche.html','fiche.pdf','qa.json','artifact_receipt.json',*[f'page-{n:02d}.png' for n in range(1,7)]}

def verify_hashes(source, out, manifest):
    if manifest['source_sha256'] != renderer.digest(source):
        raise ValueError('Source changed after rendering')
    entries=manifest['outputs']
    names=[item['path'] for item in entries]
    if len(names)!=len(set(names)) or not REQUIRED.issubset(names):
        raise ValueError('Missing or duplicate artifact')
    for item in entries:
        name=item['path']
        if Path(name).name!=name or renderer.digest(out/name)!=item['sha256']:
            raise ValueError('Artifact integrity mismatch: '+name)

def verify(source, out):
    from pypdf import PdfReader
    renderer.verify_upstream()
    manifest=json.loads((out/'render_manifest.json').read_text())
    verify_hashes(source,out,manifest)
    for field,path in [('renderer_sha256','render.py'),('theme_sha256','theme.css'),('upstream_lock_sha256','upstream-lock.json')]:
        if manifest[field]!=renderer.digest(renderer.HERE/path):
            raise ValueError('Runtime changed after rendering: '+path)
    binding=json.loads((out/'binding.json').read_text())
    if binding!=renderer.bind(source): raise ValueError('Binding does not match source')
    if (out/'scaffold.html').read_text()!=renderer.compose(binding,include_styles=False):
        raise ValueError('Scaffold does not match binding')
    if (out/'fiche.html').read_text()!=renderer.compose(binding):
        raise ValueError('HTML does not match binding and theme')
    qa=json.loads((out/'qa.json').read_text())
    if not manifest['qa_pass'] or not qa['pass'] or qa['page_count']!=6 or qa['physical_pdf_pages']!=6 or not qa['nonempty_pdf_pages'] or any(qa['summary'].values()):
        raise ValueError('Layout QA failed')
    pdf=PdfReader(out/'fiche.pdf')
    if len(pdf.pages)!=6 or any(len(p.extract_text().strip())<=50 for p in pdf.pages):
        raise ValueError('Physical PDF failed')
    receipt=json.loads((out/'artifact_receipt.json').read_text())
    if receipt['sha256']!=renderer.digest(out/'fiche.pdf') or receipt['qa_state']!='PASS':
        raise ValueError('PDF receipt mismatch')
    return {'pass':True,'module':source.stem,'physical_pages':6,'build_revision':manifest.get('build_revision'),'reader_review':qa['reader_review']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    print(json.dumps(verify(a.source,a.output),ensure_ascii=False,indent=2))
