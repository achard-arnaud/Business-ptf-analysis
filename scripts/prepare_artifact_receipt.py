"""Prepare an immutable, content-derived artifact receipt; no transport or approval."""
import argparse
import hashlib
import json
from pathlib import Path
from validate_artifact_receipt import validate_receipt


def prepare(artifact, *, entity_id, run_id, kind, producer, visibility="restricted",
            artifact_ref=None, qa_report=None, input_refs=None):
    artifact = Path(artifact)
    if not artifact.is_file():
        raise FileNotFoundError(artifact)
    data = artifact.read_bytes()
    qa = "NOT_RUN"
    if qa_report is not None:
        report = json.loads(Path(qa_report).read_text(encoding="utf-8"))
        if report.get("pass") is not True or report.get("page_count") != 3:
            raise ValueError("PDF browser QA has not passed exactly three pages")
        qa = "PASS"
    record = {
        "version": "0.1.0",
        "artifact_id": "sha256-" + hashlib.sha256(data).hexdigest()[:20],
        "entity_id": entity_id,
        "run_id": run_id,
        "kind": kind,
        "producer": producer,
        "artifact_ref": artifact_ref or str(artifact),
        "sha256": hashlib.sha256(data).hexdigest(),
        "visibility": visibility,
        "capture_kind": None,
        "hash_scope": None,
        "input_refs": list(input_refs or []),
        "publication_state": "prepared_not_published",
        "readback": None,
        "qa_state": qa,
        "authorization_state": "UNREVIEWED",
        "human_decision_ref": None,
    }
    validate_receipt(record)
    return record


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Create a prepared-only receipt for actual output bytes")
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--entity-id", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--kind", required=True, choices=("content_payload", "render_pdf", "render_png", "qa_report", "analysis_bundle"))
    ap.add_argument("--producer", required=True)
    ap.add_argument("--visibility", choices=("restricted", "public"), default="restricted")
    ap.add_argument("--qa-report", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    r = prepare(args.artifact, entity_id=args.entity_id, run_id=args.run_id, kind=args.kind,
                producer=args.producer, visibility=args.visibility, qa_report=args.qa_report)
    args.output.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PREPARED", "sha256": r["sha256"], "publication": r["publication_state"]}))
