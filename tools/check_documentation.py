#!/usr/bin/env python3
"""Offline structural checks, not LLM evaluation or a security certification."""
from __future__ import annotations
import argparse
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

VERSION = "0.2.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_contract(contract: dict) -> None:
    require(contract.get("contract_version") == VERSION, "Contract version mismatch")
    require(contract.get("enforced_runtime") is False, "Do not claim an enforced runtime")
    expected = {
        "task_status": {"completed", "partial", "blocked", "failed", "not_started"},
        "access_status": {"accessed", "partial", "blocked", "not_supported", "not_attempted"},
        "evidence_status": {"verified", "user_reported", "unverified", "contradictory", "outdated"},
        "concept_decision": {"SELECT", "REVISE", "BLOCK"},
        "final_gate_result": {"PASS", "REVISE", "BLOCK"},
    }
    for key, values in expected.items():
        require(set(contract.get(key, [])) == values, f"Incorrect vocabulary: {key}")
    require(len(contract.get("final_gates", [])) == 5, "Exactly five final gates required")
    transitions = {tuple(item) for item in contract.get("core_transitions", [])}
    require(("approved", "scheduled") in transitions and ("scheduled", "published") in transitions,
            "Scheduling must remain distinct from publication")
    require(("reviewed", "published") not in transitions, "Approval cannot be bypassed")
    require("artifact_hash" in contract.get("approval_required", []), "Approval needs artifact hash")
    require(contract.get("legacy_aliases", {}).get("pre_draft_gate.PASS") == "SELECT",
            "Legacy creative PASS is selection only")


def run(root: Path, inventory: Path | None) -> dict:
    local = {p.relative_to(root).as_posix(): p for p in root.rglob("*")
             if p.is_file() and not any(part.startswith(".") for part in p.relative_to(root).parts)
             and "__pycache__" not in p.parts}
    known = set(local)
    extra = set()
    if inventory:
        raw = json.loads(inventory.read_text(encoding="utf-8"))
        require(isinstance(raw, list) and all(isinstance(p, str) for p in raw), "Inventory must be a path list")
        extra = set(raw) - known
        known.update(raw)
    require("framework-manifest.json" in local, "Missing local manifest")
    json_count = 0
    for name, path in local.items():
        if name.endswith(".json"):
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    manifest = json.loads(local["framework-manifest.json"].read_text(encoding="utf-8"))
    contract = json.loads(local["contracts/framework.json"].read_text(encoding="utf-8"))
    require(manifest.get("method_version") == VERSION, "Method version mismatch")
    require(manifest.get("contract_version") == VERSION, "Manifest contract mismatch")
    require(manifest.get("implementation_level") == "prompt-first", "Unsupported implementation claim")
    validate_contract(contract)
    for path in manifest.get("templates", []):
        require(path in known, f"Missing template: {path}")
    approval = json.loads(local["templates/approval-record.json"].read_text(encoding="utf-8"))
    require(approval.get("status") == "not_approved", "Blank template cannot be approved")
    for key in contract["approval_required"]:
        require(key in approval and approval[key] is None, f"Blank approval must not invent {key}")
    links = 0
    for name, path in local.items():
        if not name.endswith(".md"):
            continue
        text = path.read_text(encoding="utf-8")
        require(text.count("```") % 2 == 0, f"Unclosed code fence: {name}")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target_path = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path)))
            require(not target_path.startswith("../"), f"Link escapes repository: {name}")
            exists = target_path in known or any(p.startswith(target_path.rstrip("/") + "/") for p in known)
            require(exists, f"Missing local link target: {name} -> {target_path}")
            links += 1
    # Negative controls check that the checker itself rejects structural regressions.
    negative = []
    broken = json.loads(json.dumps(contract)); broken["concept_decision"].append("APPROVED")
    negative.append(broken)
    broken = json.loads(json.dumps(contract)); broken["core_transitions"].append(["reviewed", "published"])
    negative.append(broken)
    broken = json.loads(json.dumps(contract)); broken["evidence_status"].append("blocked")
    negative.append(broken)
    for broken in negative:
        rejected = False
        try:
            validate_contract(broken)
        except ValueError:
            rejected = True
        require(rejected, "Negative control unexpectedly accepted")
    return {
        "structural_result": "PASS", "local_files_checked": len(local),
        "inventory_only_paths": len(extra), "json_files_parsed": json_count,
        "local_link_targets_checked": links,
        "behavioral_cases_executed_by_this_check": 0,
        "negative_controls_rejected": len(negative),
        "limitations": ["No external link or fragment validation", "No LLM/runtime execution",
                        "No independent review or legal/security certification",
                        "Inventory-only file contents are not inspected"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--inventory", type=Path, help="Optional audited path list for staged-only validation")
    args = parser.parse_args()
    try:
        result = run(args.root.resolve(), args.inventory)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"structural_result": "FAIL", "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
