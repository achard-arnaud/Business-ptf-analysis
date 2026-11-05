"""Optimistic session checkpoint verification and dependency invalidation (#39).

This module does not write state or verify the authenticity of human approval.
"""
import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "contracts" / "session-checkpoint.schema.json").read_text(encoding="utf-8"))


def validate_checkpoint(record):
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(record)
    sources = [p["path"] for p in record["input_pins"]]
    if len(sources) != len(set(sources)):
        raise ValueError("duplicate input paths")
    if len({p["path"] for p in record["output_pins"]}) != len(record["output_pins"]):
        raise ValueError("duplicate output paths")
    if any(not set(o["depends_on"]) <= set(sources) for o in record["output_pins"]):
        raise ValueError("output depends on unpinned input")
    if record["gate"] == "APPROVED_REF_ONLY" and not record.get("human_decision_ref"):
        raise ValueError("approved-reference checkpoint must carry a decision reference")
    return True


def safe_file(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("checkpoint path escapes root")
    return path


def verify_inputs(record, root, observed_repo_sha):
    validate_checkpoint(record)
    if observed_repo_sha != record["repo_sha"]:
        return {"status": "CONFLICT", "reason": "repo SHA changed; no write permitted"}
    pins = [record["run_context"], *record["input_pins"]]
    for item in pins:
        path = safe_file(root, item["path"])
        if not path.is_file():
            return {"status": "BLOCKED", "reason": "missing pinned file: " + item["path"]}
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            return {"status": "STALE", "reason": "input bytes changed: " + item["path"]}
    return {"status": "READY_TO_RESUME", "human_approval_verified": False, "outputs_promoted": False}


def invalidate_outputs(record, changed_input_paths):
    validate_checkpoint(record)
    pinned = {item["path"] for item in record["input_pins"]}
    changed = set(changed_input_paths)
    if not changed <= pinned:
        raise ValueError("unrecognized changed input must trigger targeted re-research")
    return sorted(o["path"] for o in record["output_pins"] if changed.intersection(o["depends_on"]))


def resume_packet(record, root, observed_repo_sha):
    """Return only bounded refs needed to resume, never evidence contents."""
    result = verify_inputs(record, root, observed_repo_sha)
    if result["status"] != "READY_TO_RESUME":
        return result
    return {
        **result,
        "entity_id": record["entity_id"],
        "stage": record["stage"],
        "cutoff": record["cutoff"],
        "integrator": record["integrator"],
        "critical_claim_refs": record["critical_claim_refs"],
        "counterclaim_refs": record["counterclaim_refs"],
        "decisive_unknowns": record["decisive_unknowns"],
        "gate": record["gate"],
        "human_approval_verified": False,
        "next_action": record["next_action"],
        "stop_condition": record["stop_condition"],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read-only checkpoint metadata / cold-session resumption")
    parser.add_argument("mode_or_checkpoint")
    parser.add_argument("checkpoint", nargs="?")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--repo-sha")
    args = parser.parse_args()
    try:
        if args.mode_or_checkpoint == "resume":
            if not args.checkpoint or args.root is None or args.repo_sha is None:
                parser.error("resume requires checkpoint, --root and --repo-sha")
            record = json.loads(Path(args.checkpoint).read_text(encoding="utf-8"))
            result = resume_packet(record, args.root, args.repo_sha)
        elif args.checkpoint is None:
            record = json.loads(Path(args.mode_or_checkpoint).read_text(encoding="utf-8"))
            validate_checkpoint(record)
            result = {"status":"CHECKPOINT_METADATA_VALID","human_approval_verified":False}
        else:
            parser.error("usage: session_checkpoint.py resume <checkpoint> --root <dir> --repo-sha <sha>")
        print(json.dumps(result, ensure_ascii=False))
        if result["status"] not in ("CHECKPOINT_METADATA_VALID", "READY_TO_RESUME"):
            sys.exit(2)
    except Exception as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)}))
        sys.exit(1)
