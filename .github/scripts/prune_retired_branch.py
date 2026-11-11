#!/usr/bin/env python3
"""Repository maintenance only; dry-run unless --apply is explicitly supplied."""
import argparse
import json
import os
import subprocess
import tempfile

REPO = "bribeirobr25/personal-branding-agents"
RETIRED = "feat/creative-strategist-concept-gate"
EXPECTED = "4a66318cc6b957fbe97c48c083abb117ead4b5e8"
KEEP = {"main", "feat/creative-strategist-concept-gate-20261110"}


def run(args, **kwargs):
    result = subprocess.run(args, capture_output=True, text=True, **kwargs)
    if result.returncode:
        raise RuntimeError(f"Command failed ({args[0]}, exit {result.returncode}); no credentials logged")
    return result.stdout


def get(path, pages=False):
    args = ["gh", "api", "--hostname", "github.com", "--method", "GET", f"repos/{REPO}/{path}"]
    if pages:
        args += ["--paginate", "--slurp"]
    value = json.loads(run(args))
    return [item for page in value for item in page] if pages else value


def audit():
    if os.environ.get("GITHUB_REPOSITORY") != REPO or RETIRED in KEEP:
        raise RuntimeError("Unexpected repository or preserved branch")
    branches = {b["name"]: b for b in get("branches?per_page=100", True)}
    if not KEEP <= set(branches):
        raise RuntimeError("A preserved branch is absent")
    target = branches.get(RETIRED)
    if target is None:
        return "already_absent"
    if target.get("protected") or target["commit"]["sha"] != EXPECTED:
        raise RuntimeError("Retired branch protected or changed; reassessment required")
    prs = get("pulls?state=open&per_page=100", True)
    if any(p.get("head", {}).get("ref") == RETIRED or p.get("base", {}).get("ref") == RETIRED for p in prs):
        raise RuntimeError("An open PR depends on the retired branch")
    main_sha = branches["main"]["commit"]["sha"]
    comparison = get(f"compare/{EXPECTED}...{main_sha}")
    if comparison.get("status") not in {"ahead", "identical"} or comparison.get("merge_base_commit", {}).get("sha") != EXPECTED:
        raise RuntimeError("main does not preserve the retired head")
    return "safe_ancestor"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    state = audit()
    print(json.dumps({"mode": "apply" if args.apply else "dry_run", "branch": RETIRED, "expected_sha": EXPECTED, "audit": state}))
    if not args.apply or state == "already_absent":
        return
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Deletion only allowed from main")
    if audit() != "safe_ancestor":
        return
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    with tempfile.TemporaryDirectory(prefix="retired-branch-") as directory:
        run(["git", "init", "--bare", "--quiet", directory], env=env)
        run(["git", "-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential", "push", "--atomic", f"--force-with-lease=refs/heads/{RETIRED}:{EXPECTED}", f"https://github.com/{REPO}.git", f":refs/heads/{RETIRED}"], cwd=directory, env=env)
    remaining = sorted(b["name"] for b in get("branches?per_page=100", True))
    if RETIRED in remaining or not KEEP <= set(remaining):
        raise RuntimeError("Cleanup postcondition failed")
    print(json.dumps({"deleted": RETIRED, "remaining": remaining}))


if __name__ == "__main__":
    main()
