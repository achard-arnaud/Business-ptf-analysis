#!/usr/bin/env python3
"""Candidate value-chain three-pager: data->3 landscape HTML pages->optional PDF/PNG QA.

No rewrite of exec v0.3; no bundle claim, GO_DRAFT or committee approval.
"""
import argparse
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_value_chain_view import check_view

STYLE = """
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; color:#202d38; background:#fff; font: 13px/1.3 Arial, Helvetica, sans-serif; }
.page { width:297mm; height:210mm; padding:11mm 13mm 10mm; overflow:hidden;
        page-break-after:always; break-after:page; display:flex; flex-direction:column;
        background:#fff; }
.header { display:flex; align-items:flex-end; justify-content:space-between;
          border-bottom:2px solid #253c4e; padding-bottom:12px; margin-bottom:16px; }
.eyebrow { text-transform:uppercase; font-size:12px; font-weight:bold; letter-spacing:.08em; color:#4a6576; }
h1 {font-size:26px; line-height:1.16; margin:5px 0 0; letter-spacing:-.02em;}
.headright {font-size:12px; text-align:right; color:#516779;}
.pagebody {flex:1; min-height:0; display:flex; flex-direction:column;}
.sectionname {font-size:16px; font-weight:bold; margin:0 0 10px; color:#223a4c;}
.hero {border:1px solid #bfd0d8; border-left:5px solid #2d6376;
       background:#f4f8fa; padding:16px; min-height:94px; margin-bottom:15px;}
.hero strong {font-size:18px;}
.hero p {margin:7px 0 0; color:#344d5f; }
.grid {display:grid; grid-template-columns:repeat(4,1fr); gap:10px;}
.drivers {grid-auto-rows:minmax(114px,auto);}
.card {border:1px solid #d8e1e6; border-radius:7px; padding:13px;
       overflow-wrap:anywhere; min-width:0; background:#fff;}
.card .id {color:#657986; font-size:12px; font-weight:bold;}
.card .name {font-size:15px; font-weight:bold; margin:6px 0 8px;}
.card .minor {color:#516774; font-size:12.5px;}
.card .kpi {font-size:12px; padding-top:6px; font-weight:bold;}
.notice {margin-top:15px; padding:13px 16px; font-size:13px;
         background:#f1f4f6; border-radius:5px; color:#3f5867;}
.activities {display:grid;grid-template-columns:repeat(3,1fr);
             grid-auto-rows:139px; gap:11px; align-content:start;}
.activity {border:1px solid #d8e1e6; padding:14px; border-radius:6px; min-width:0;
           overflow-wrap:anywhere;}
.role {font-size:12px; font-weight:bold; text-transform:uppercase; color:#2d6376;}
.activity .name {font-size:16px;font-weight:bold;margin:7px 0;}
.activity .minor {font-size:12.5px; color:#536979;}
.activity .refs {font-size:12px; margin-top:8px; color:#526b7a;}
.column-note {margin-top:12px; font-size:12.5px; color:#4b626f;}
.table {width:100%;border-collapse:collapse;table-layout:fixed;}
.table th {background:#e7eff2;color:#243b4a; padding:11px 10px;font-size:12px;
           text-transform:uppercase;text-align:left;}
.table td {padding:9px 10px; border-bottom:1px solid #d8e2e6;vertical-align:top;
           overflow-wrap:anywhere; font-size:12.5px;}
.table td strong {font-size:13px;}
.table tr:nth-child(even) {background:#f8fafb;}
.table td:first-child {font-weight:bold;color:#2d6376;}
.footer {border-top:1px solid #d8e2e6; display:flex; justify-content:space-between;
         color:#536a76;font-size:12px;padding-top:10px;margin-top:10px;}
b {font-weight:700;}
@media screen { .page {margin:8px auto;box-shadow:0 0 0 1px #e1e6e9;} }
"""

def esc(x):
    return html.escape(str(x), quote=True)

def header(data, page, title):
    return (f'<header class="header"><div><span class="eyebrow">Value-chain preview · '
            f'{esc(data["profile_id"].replace("_"," "))}</span><h1>{esc(title)}</h1></div>'
            f'<div class="headright"><b>{esc(data["entity_id"])}</b>'
            f'<div>Cutoff {esc(data["cutoff"])} · {page} / 3</div></div></header>')

def footer(page):
    return (f'<footer class="footer"><span>SYNTHETIC / CANDIDATE · Not investment or committee material</span>'
            f'<span>Evidence, ownership & HITL not verified · {page}/3</span></footer>')

def page(data, index, title, body):
    return ('<section class="page">'+header(data,index,title)
            +'<main class="pagebody">'+body+'</main>'+footer(index)+'</section>')

def render_html(data):
    check_view(data)
    drivers=data["drivers"]; acts=data["activities"]; opp=data["opportunities"]
    dmap={x["id"]:x for x in drivers}
    amap={x["id"]:x for x in acts}
    cards="".join(
        f'<article class="card" data-no-overflow><div class="id">{esc(d["id"])}</div>'
        f'<div class="name">{esc(d["label"])}</div>'
        f'<div class="minor">{esc(d["economic_mechanism"])}</div>'
        f'<div class="kpi">KPI · {esc(d["kpi"])}</div></article>'
        for d in drivers)
    first=(
        '<div class="hero"><strong>Economic mechanisms, not an AI catalogue</strong>'
        '<p>This profile is a structural demonstration. No source archive, business ROI or '
        'investment decision has been verified. Compare each idea against the no-AI baseline.</p></div>'
        '<h2 class="sectionname">Value drivers and measurement anchors</h2>'
        f'<div class="grid drivers">{cards}</div>'
        '<div class="notice">Driver count is profile-dependent; it is not the fixed five-driver '
        'constraint of the historical executive template. Any factual claim requires source lineage.</div>')
    actcards="".join(
        f'<article class="activity" data-no-overflow><span class="role">{esc(a["role"])} · {esc(a["id"])}</span>'
        f'<div class="name">{esc(a["label"])}</div><div class="minor">{esc(a["value_mechanism"])}</div>'
        f'<div class="refs">Drivers: {esc(", ".join(dmap[x]["label"] for x in a["driver_refs"]))}'
        f' · {esc(a["epistemic_status"])}</div></article>'
        for a in acts)
    second=(
        '<h2 class="sectionname">Activities and contribution to value</h2>'
        f'<div class="activities">{actcards}</div>'
        '<div class="column-note">Topology follows the business model; activities do not inherit '
        'the fixed Porter manufacturing layout. Evidence status remains explicitly scoped.</div>')
    rows="".join(
        f'<tr><td>{esc(u["id"])}</td>'
        f'<td><strong>{esc(amap[u["activity_id"]]["label"])}</strong>'
        f'<div>{esc(", ".join(dmap[x]["label"] for x in u["driver_refs"]))}</div></td>'
        f'<td>{esc(u["baseline_no_ai"])}</td>'
        f'<td>{esc(u["kpi"])}</td>'
        f'<td>{esc(u["stop_condition"])}</td></tr>'
        for u in opp)
    third=(
        '<h2 class="sectionname">Candidate opportunities — baseline and stop rule</h2>'
        '<table class="table"><colgroup><col style="width:8%"><col style="width:26%">'
        '<col style="width:25%"><col style="width:16%"><col style="width:25%"></colgroup>'
        '<thead><tr><th>ID</th><th>Activity / driver</th><th>Without AI</th><th>Measure</th>'
        '<th>Stop / challenge</th></tr></thead><tbody>'+rows+'</tbody></table>'
        '<div class="notice">Before prioritisation: verify data rights, OT/security, human control, '
        'value owner and feasibility. The review must separate economic priority from delivery sequence.</div>')
    doc='<!doctype html><html lang="en"><head><meta charset="utf-8">'
    doc+='<meta name="viewport" content="width=device-width, initial-scale=1">'
    doc+='<title>Value-chain preview</title><style>'+STYLE+'</style></head><body>'
    doc+=page(data,1,"Business model and value",first)
    doc+=page(data,2,"Value chain and drivers",second)
    doc+=page(data,3,"Opportunities and hard gates",third)
    return doc+'</body></html>'

def render(source, out, pdf=False):
    data=json.loads(Path(source).read_text(encoding="utf-8"))
    markup=render_html(data)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    stem="value_chain_"+data["profile_id"]
    html_path=out/(stem+".html")
    html_path.write_text(markup,encoding="utf-8")
    manifest={"profile":"value_chain_preview","source_profile":data["profile_id"],"version":"0.1.0",
              "source_sha256":hashlib.sha256(Path(source).read_bytes()).hexdigest(),
              "html_sha256":hashlib.sha256(markup.encode("utf-8")).hexdigest(),
              "page_count_intended":3,"evidence_verified":False,
              "render_authorized_for_committee":False,"qa_status":"NOT_RUN"}
    if pdf:
        rdir=ROOT/"renderers"/"three_pager_exec"
        subprocess.run([sys.executable,str(rdir/"render2.py"),str(html_path),str(out),stem],check=True)
        subprocess.run([sys.executable,str(rdir/"qa.py"),str(html_path),
                        "--report",str(out/"qa.json"),"--screenshots",str(out/"qa")],check=True)
        manifest["qa_status"]="LAYOUT_PASS_READER_PENDING"
        manifest["pdf_sha256"]=hashlib.sha256((out/(stem+".pdf")).read_bytes()).hexdigest()
    (out/"render_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    if pdf:
        from prepare_artifact_receipt import prepare
        receipt = prepare(out/(stem+".pdf"), entity_id=data["entity_id"],
                          run_id="preview-"+data["profile_id"], kind="render_pdf",
                          producer="renderers/value_chain_preview/render.py",
                          visibility="public", qa_report=out/"qa.json",
                          input_refs=[str(source),str(out/"render_manifest.json")])
        (out/"artifact_receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    return manifest

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("view",type=Path)
    ap.add_argument("out",type=Path)
    ap.add_argument("--pdf",action="store_true")
    args=ap.parse_args()
    print(json.dumps(render(args.view,args.out,pdf=args.pdf),ensure_ascii=False))
