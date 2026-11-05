"""Authoritative inventory of three-pager and strategic-note renderer capability (#25)."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def check_registry(registry, root=ROOT):
    root = Path(root)
    schema = json.loads((root / "contracts/template-registry.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(registry)
    keys = [(x["template_id"], x["profile"]) for x in registry["templates"]]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate template profile")
    for item in registry["templates"]:
        for field in ("template_ref", "schema_ref", "renderer_ref"):
            path = item[field]
            if path is None:
                continue
            target = (root / path).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise ValueError(f"template file missing or outside repository: {field} {path}")
        cap, renderer = item["capability"], item["renderer_ref"]
        if cap == "schema_only" and (renderer is not None or item["formats"]):
            raise ValueError("schema_only cannot advertise renderer or output formats")
        if cap in ("preview", "demo_only", "ready") and renderer is None:
            raise ValueError("rendering capability cannot be claimed without renderer")
        if cap in ("demo_only", "ready") and item["schema_ref"] is None:
            raise ValueError("validated rendering route must have schema")
        if item["committee_authorized"]:
            raise ValueError("template registry never grants committee authorization")
    return {"status":"REGISTRY_VALID","profiles":len(keys),"committee_authorized":False}


if __name__ == "__main__":
    try:
        registry = json.loads((ROOT / "templates/registry.json").read_text(encoding="utf-8"))
        print(json.dumps(check_registry(registry), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)}, ensure_ascii=False))
        sys.exit(1)
