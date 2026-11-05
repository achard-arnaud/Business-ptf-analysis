"""Correlate actual 3-page PDF, screenshots, browser report and render manifest.

Mechanical QA is not reader QA, business evidence or committee permission.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from pypdf import PdfReader

ISSUE_KEYS=("overlaps","overflows","out_of_bounds","small_fonts","low_padding")
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify(folder, *, profile):
    folder=Path(folder)
    manifest=json.loads((folder/"render_manifest.json").read_text(encoding="utf-8"))
    report_path=folder/"qa.json"
    report=json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("page_count")!=3 or report.get("pass") is not True:
        raise ValueError("browser report does not pass exactly three pages")
    summary=report.get("summary",{})
    if any(summary.get(key,1)!=0 for key in ISSUE_KEYS):
        raise ValueError("browser report contains layout defects or missing category")
    if manifest.get("qa_sha256") != sha(report_path):
        raise ValueError("QA report changed since manifest")
    pdfs=list(folder.glob("*.pdf"))
    if len(pdfs)!=1:
        raise ValueError("expected exactly one PDF")
    pdf=pdfs[0]
    if len(PdfReader(str(pdf)).pages)!=3:
        raise ValueError("PDF physical page count != 3")
    if manifest.get("pdf_sha256")!=sha(pdf):
        raise ValueError("PDF changed since manifest")
    pngs=sorted(folder.glob("*_page[1-3].png"))
    if len(pngs)!=3:
        raise ValueError("missing page PNG screenshots")
    for png in pngs:
        raw=png.read_bytes()
        if len(raw)<40 or raw[:8]!=b"\x89PNG\r\n\x1a\n":
            raise ValueError("invalid page PNG signature")
        width,height=struct.unpack(">II",raw[16:24])
        if width<800 or height<500:
            raise ValueError("page PNG dimensions too small")
    observed=[sha(p) for p in pngs]
    if manifest.get("png_sha256")!=observed:
        raise ValueError("PNG changed since render manifest")
    if profile=="value-chain-preview":
        receipt=json.loads((folder/"artifact_receipt.json").read_text(encoding="utf-8"))
        if receipt.get("sha256")!=sha(pdf) or receipt.get("publication_state")!="prepared_not_published":
            raise ValueError("preview receipt does not match exact PDF or falsely claims publication")
        if receipt.get("authorization_state")!="UNREVIEWED" or receipt.get("qa_state")!="PASS":
            raise ValueError("preview receipt must be mechanically QAed and not human approved")
    elif profile=="exec":
        if manifest.get("render_profile")!="exec" or manifest.get("visual_qa")!="LAYOUT_PASS_MANUAL_PENDING":
            raise ValueError("exec not in manual-review-pending layout-pass state")
    else:
        raise ValueError("unknown rendering profile")
    return {"status":"AUTOMATED_LAYOUT_PASS_READER_PENDING","profile":profile,
            "physical_pages":3,"pngs":3,"pdf_sha256":sha(pdf),"committee_authorized":False}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("folder",type=Path)
    p.add_argument("--profile",choices=("exec","value-chain-preview"),required=True)
    a=p.parse_args()
    print(json.dumps(verify(a.folder,profile=a.profile),ensure_ascii=False))
