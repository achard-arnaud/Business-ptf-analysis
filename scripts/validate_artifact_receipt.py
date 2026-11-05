"""Independent artifact receipt checks (#47); no transport or approval implied."""
import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "contracts/artifact-receipt.schema.json").read_text(encoding="utf-8"))


def validate_receipt(receipt, *, remote_readback_bytes=None):
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(receipt)
    if receipt["kind"] == "source_capture":
        pair = (receipt["capture_kind"], receipt["hash_scope"])
        if pair not in (("selected_excerpt", "excerpt_utf8"), ("full_original", "original_bytes")):
            raise ValueError("source capture must declare actual snapshot bytes scope")
    elif receipt["capture_kind"] is not None or receipt["hash_scope"] is not None:
        raise ValueError("non-source artifact cannot advertise source-capture semantics")
    if receipt["authorization_state"] == "HITL_REFERENCED" and not receipt.get("human_decision_ref"):
        raise ValueError("HITL reference without decision reference")
    state = receipt["publication_state"]
    if state == "published_verified":
        evidence = receipt["readback"]
        if evidence is None or evidence["sha256"] != receipt["sha256"]:
            raise ValueError("published receipt missing matching readback metadata")
        if remote_readback_bytes is None:
            raise ValueError("published_verified requires independently re-read bytes")
        actual = hashlib.sha256(remote_readback_bytes).hexdigest()
        if actual != receipt["sha256"]:
            raise ValueError("remote readback content does not match published artifact")
    elif receipt["readback"] is not None:
        raise ValueError("non-verified publication may not claim a verified readback")
    return {"status": "RECEIPT_CHECKED", "publication_state": state,
            "qa_state": receipt["qa_state"], "authorization_state": receipt["authorization_state"],
            "human_decision_authenticity_verified": False}


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("receipt", type=Path)
    p.add_argument("--readback-file", type=Path)
    args = p.parse_args()
    try:
        record = json.loads(args.receipt.read_text(encoding="utf-8"))
        supplied = args.readback_file.read_bytes() if args.readback_file is not None else None
        print(json.dumps(validate_receipt(record, remote_readback_bytes=supplied)))
    except Exception as exc:
        print(json.dumps({"status":"FAIL", "reason":str(exc)}))
        sys.exit(1)
