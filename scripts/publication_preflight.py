"""Fail-closed publication preflight; never mints a human/committee approval (#29).

Mechanical integrity is necessary but not sufficient for publication.
"""
import argparse
import hashlib
import json
from pathlib import Path

from validate_artifact_receipt import validate_receipt


def check_release(manifest, receipt, pdf_bytes, *, independent_readback=None,
                  freeze_verdict=None, reader_verdict=None):
    reasons=[]
    if manifest.get("render_profile") != "exec":
        reasons.append("unsupported_render_profile")
    if manifest.get("visual_qa") not in ("LAYOUT_PASS_MANUAL_PENDING","READER_APPROVED"):
        reasons.append("layout_qa_not_passed")
    if receipt.get("kind") != "render_pdf":
        reasons.append("not_a_pdf_receipt")
    digest=hashlib.sha256(pdf_bytes).hexdigest()
    if receipt.get("sha256") != digest:
        reasons.append("render_bytes_changed")
    if receipt.get("qa_state") != "PASS":
        reasons.append("artifact_qa_not_passed")
    if receipt.get("publication_state") != "published_verified":
        reasons.append("artifact_not_durably_published")
    try:
        validate_receipt(receipt, remote_readback_bytes=independent_readback)
    except Exception:
        reasons.append("invalid_publication_receipt")
    if not isinstance(freeze_verdict,dict) or freeze_verdict.get("status") != "VERIFIED_FROZEN_BUNDLE":
        reasons.append("frozen_bundle_and_hitl_not_verified")
    else:
        if not freeze_verdict.get("bundle_sha256") or manifest.get("bundle_sha256") != freeze_verdict["bundle_sha256"]:
            reasons.append("bundle_hash_mismatch")
        if not freeze_verdict.get("payload_sha256") or manifest.get("payload_sha256") != freeze_verdict["payload_sha256"]:
            reasons.append("payload_hash_mismatch")
    if not isinstance(reader_verdict,dict) or reader_verdict.get("status") != "READER_REVIEWED":
        reasons.append("human_reader_qa_missing")
    else:
        if reader_verdict.get("pdf_sha256") != digest:
            reasons.append("human_reader_review_stale")
    if receipt.get("authorization_state") != "HITL_REFERENCED":
        reasons.append("no_hitl_reference")
    # Even complete metadata does not authenticate who recorded HITL or reader review.
    return {"status": "BLOCKED" if reasons else "AWAIT_AUTHENTICATED_HUMAN_RELEASE",
            "blockers": sorted(set(reasons)),
            "committee_authorized": False,
            "human_authenticity_verified": False,
            "artifact_sha256": digest}


def inspect_files(manifest_path, receipt_path, pdf_path, readback_file=None,
                  freeze_verdict_path=None, reader_verdict_path=None):
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8")) if path else None
    return check_release(read(manifest_path),read(receipt_path),Path(pdf_path).read_bytes(),
                         independent_readback=Path(readback_file).read_bytes() if readback_file else None,
                         freeze_verdict=read(freeze_verdict_path),
                         reader_verdict=read(reader_verdict_path))


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("manifest",type=Path)
    ap.add_argument("receipt",type=Path)
    ap.add_argument("pdf",type=Path)
    ap.add_argument("--readback-file",type=Path)
    ap.add_argument("--freeze-verdict",type=Path)
    ap.add_argument("--reader-verdict",type=Path)
    args=ap.parse_args()
    result=inspect_files(args.manifest,args.receipt,args.pdf,args.readback_file,args.freeze_verdict,args.reader_verdict)
    print(json.dumps(result,ensure_ascii=False))
    if result["status"]=="BLOCKED":
        raise SystemExit(2)
