"""Validate inter-model handoff metadata without claiming tool access or HITL (#33)."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "contracts" / "research-handoff.schema.json").read_text(encoding="utf-8"))


def validate_handoff(record):
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(record)
    required = record["required_capabilities"]
    caps = record["capabilities"]
    if any(name not in caps for name in required):
        raise ValueError("required capability missing from capability report")
    unavailable = [name for name in required if caps[name] != "available"]
    if record["readiness"] == "READY" and unavailable:
        raise ValueError("READY cannot rely on deferred/unavailable capabilities")
    if record["readiness"] == "READY" and record["fallback"]["mode"] != "none":
        raise ValueError("READY should not advertise active fallback")
    if record["readiness"] == "RECOVERABLE":
        if not unavailable or record["fallback"]["mode"] not in ("verified_snapshot", "defer"):
            raise ValueError("RECOVERABLE needs unavailable capability and a bounded fallback")
    if record["readiness"] == "BLOCKED" and record["fallback"]["mode"] not in ("stop", "defer"):
        raise ValueError("BLOCKED must stop or defer")
    if record["fallback"]["mode"] == "verified_snapshot" and not record["fallback"].get("snapshot"):
        raise ValueError("snapshot fallback needs an exact pinned snapshot reference")
    if len(set(x["path"] for x in record["inputs"])) != len(record["inputs"]):
        raise ValueError("duplicate input paths")
    return {"status": "METADATA_VALID", "readiness": record["readiness"],
            "verified_external_access": False, "human_approval": False}


if __name__ == "__main__":
    try:
        document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(validate_handoff(document)))
    except (ValueError, OSError, KeyError, IndexError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        sys.exit(1)
