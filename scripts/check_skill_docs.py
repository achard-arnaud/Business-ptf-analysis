#!/usr/bin/env python3
"""Static navigation/discovery check for the single domain skill (#7).

This checks files and declared routes, not LLM behaviour or source truth.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = (
    "AGENTS.md",
    "skills/hivest-portfolio-ai/SKILL.md",
    "skills/hivest-portfolio-ai/references/workflow.md",
    "docs/agent/quickstart-map.md",
    "docs/agent/context-and-resume.md",
    "docs/architecture/code-map.md",
)
ROUTE_PROCEDURES = ("evidence", "market-drivers", "diagnostic", "opportunities",
                    "review", "composition", "learning")
LINK = re.compile(r"\]\(([^)]+)\)")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def check_document(path, root):
    text = path.read_text(encoding="utf-8")
    errors = []
    for match in LINK.finditer(text):
        target = match.group(1).split("#", 1)[0].strip().split(" ", 1)[0]
        if not target or target.startswith(("https:", "http:", "mailto:", "#")):
            continue
        target = unquote(target)
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"{path}: link escapes repository: {target}")
        elif not resolved.exists():
            errors.append(f"{path}: broken link: {target}")
    return errors


def check_frontmatter(path):
    data = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(data)
    if not match:
        return [f"{path}: missing skill frontmatter"]
    fields = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.MULTILINE))
    errors = [f"{path}: missing frontmatter {key}" for key in ("name", "description")
              if not fields.get(key, "").strip()]
    if fields.get("name", "").strip() != path.parent.name:
        errors.append(f"{path}: name differs from directory")
    return errors


def check(root=ROOT):
    root = Path(root)
    errors = []
    for relative in DOCS:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required route document: {relative}")
        else:
            errors.extend(check_document(path, root))
    skill = root / "skills/hivest-portfolio-ai/SKILL.md"
    if skill.is_file():
        errors.extend(check_frontmatter(skill))
    workflow = root / "skills/hivest-portfolio-ai/references/workflow.md"
    if workflow.is_file():
        body = workflow.read_text(encoding="utf-8")
        for procedure in ROUTE_PROCEDURES:
            if f"({procedure}.md)" not in body:
                errors.append(f"workflow missing procedure link: {procedure}")
    return errors


if __name__ == "__main__":
    found = check()
    for item in found:
        print(item)
    print("FAIL" if found else "PASS: route links and skill discovery metadata")
    sys.exit(bool(found))
