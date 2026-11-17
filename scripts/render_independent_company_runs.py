"""Render bound independent-company exec payloads for CI and verify their bytes."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import digest  # noqa: E402


def bound_runs(root=ROOT):
    runs = []
    for manifest_path in sorted((root / "companies").glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("instance_kind") != "independent_company_analysis" or not manifest.get("pdf_ref"):
            continue
        entity_dir = manifest_path.parent
        required = ("payload_ref", "binding_ref", "render_manifest_ref", "review_refs")
        missing = [key for key in required if not manifest.get(key)]
        if missing:
            raise ValueError(f"{manifest_path}: bound PDF run missing {', '.join(missing)}")
        payload_path = root / manifest["payload_ref"]
        binding_path = root / manifest["binding_ref"]
        render_manifest_path = root / manifest["render_manifest_ref"]
        pdf_path = root / manifest["pdf_ref"]
        graph_path = root / manifest["graph_ref"]
        if not all(path.is_file() for path in (payload_path, binding_path, render_manifest_path, pdf_path, graph_path)):
            raise ValueError(f"{manifest_path}: payload/binding/render manifest path is broken")
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
        render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        package_path = root / manifest["package_ref"]
        context_path = root / manifest["strategic_context_ref"]
        package = json.loads(package_path.read_text(encoding="utf-8"))
        context = json.loads(context_path.read_text(encoding="utf-8"))
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        if payload.get("entity_id") != manifest.get("entity_id") or binding.get("entity_id") != manifest.get("entity_id"):
            raise ValueError(f"{manifest_path}: entity binding does not match payload")
        if payload.get("cutoff") != package.get("cutoff") or package.get("entity_id") != context.get("entity_id"):
            raise ValueError(f"{manifest_path}: source package/context does not match the run")
        bundle_sha256 = digest({"package": package, "context": context, "graph": graph})
        if payload.get("lineage", {}).get("bundle_sha256") != bundle_sha256:
            raise ValueError(f"{payload_path}: stale evidence bundle hash")
        if manifest.get("evidence_bundle_sha256") != bundle_sha256:
            raise ValueError(f"{manifest_path}: stale evidence bundle hash")
        if binding.get("evidence_snapshot_sha256") != bundle_sha256:
            raise ValueError(f"{binding_path}: stale evidence snapshot hash")
        if binding.get("graph") != manifest.get("graph_ref") or binding.get("payload") != manifest.get("payload_ref"):
            raise ValueError(f"{manifest_path}: graph/payload binding does not match run manifest")
        file_sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        if render_manifest.get("payload_sha256") != file_sha(payload_path):
            raise ValueError(f"{render_manifest_path}: stale payload hash")
        if render_manifest.get("pdf_sha256") != file_sha(pdf_path):
            raise ValueError(f"{render_manifest_path}: stale PDF hash")
        if render_manifest.get("graph_sha256") != file_sha(graph_path):
            raise ValueError(f"{render_manifest_path}: stale graph hash")
        if render_manifest.get("bundle_sha256") != bundle_sha256:
            raise ValueError(f"{render_manifest_path}: stale evidence bundle hash")
        if render_manifest.get("package_sha256") != file_sha(package_path) or render_manifest.get("context_sha256") != file_sha(context_path):
            raise ValueError(f"{render_manifest_path}: stale source package/context hash")
        for review_ref in manifest["review_refs"]:
            if not (root / review_ref).is_file():
                raise ValueError(f"{manifest_path}: review path is broken: {review_ref}")
        if payload.get("render_profile") != "exec":
            raise ValueError(f"{payload_path}: unsupported render profile {payload.get('render_profile')!r}")
        if render_manifest.get("entity") != payload.get("entity") or render_manifest.get("render_profile") != "exec":
            raise ValueError(f"{render_manifest_path}: render profile/entity does not match run")
        runs.append((manifest["entity_id"], payload_path, binding_path, render_manifest_path))
    return runs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true", help="validate bindings and hashes without starting Chromium")
    args = parser.parse_args()
    renderer = ROOT / "renderers" / "three_pager_exec" / "render_exec.py"
    verifier = ROOT / "scripts" / "verify_render_evidence.py"
    runs = bound_runs(ROOT)
    if args.check_only:
        print(json.dumps({"bound_independent_company_runs": len(runs), "entity_ids": [r[0] for r in runs]}))
        return
    for entity_id, payload, _binding, _render_manifest in runs:
        out = args.out / entity_id
        subprocess.run([sys.executable, str(renderer), str(payload), str(out), "--pdf"], check=True)
        subprocess.run([sys.executable, str(verifier), str(out), "--profile", "exec"], check=True)
    print(json.dumps({"independent_company_runs_rendered": len(runs), "entity_ids": [r[0] for r in runs]}))


if __name__ == "__main__":
    main()
