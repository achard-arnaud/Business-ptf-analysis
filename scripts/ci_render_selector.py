"""Choose browser layout QA based on real changed paths, not labels (#31)."""
import argparse
import re
import subprocess
from pathlib import PurePosixPath


def should_render(paths):
    paths=set(paths)
    if not paths:
        return False
    for path in paths:
        p=path.replace("\\","/")
        if p.startswith(".github/workflows/"):
            return True
        if p.startswith("renderers/") and not p.endswith((".md",".txt")):
            return True
        if p.startswith("templates/") and (p.endswith(".md") or p.endswith(".json")):
            return True
        if p.startswith("contracts/") and p.endswith(".schema.json"):
            return True
        if p.startswith("tests/fixtures/") and ("/exec/" in p or PurePosixPath(p).name.startswith("value_chain_")):
            return True
        if p in ("scripts/verify_render_evidence.py", "scripts/prepare_artifact_receipt.py",
                 "scripts/validate_value_chain_view.py", "scripts/ci_render_selector.py"):
            return True
        if p.startswith(("scripts/","tests/")) and p.endswith(".py") and any(t in p for t in ("render","layout","template","pdf","qa_")):
            return True
    return False


def changed_files(base, head):
    valid=lambda v: bool(v and re.fullmatch("[0-9a-fA-F]{40}",v) and v!="0"*40)
    if not valid(head):
        raise ValueError("invalid head commit SHA")
    if not valid(base):
        base=subprocess.check_output(["git","rev-parse",head+"^"],text=True).strip()
    raw=subprocess.check_output(["git","diff","--name-only","-z","--find-renames",base,head])
    return [x.decode("utf-8") for x in raw.split(b"\0") if x]


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--base",required=True)
    parser.add_argument("--head",required=True)
    args=parser.parse_args()
    print("true" if should_render(changed_files(args.base,args.head)) else "false")
