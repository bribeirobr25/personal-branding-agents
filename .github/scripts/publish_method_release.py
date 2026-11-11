#!/usr/bin/env python3
"""Publish the reviewed prompt-first release; never move or replace an existing tag."""
import json
import os
import re
import subprocess
from pathlib import Path

REPO = "bribeirobr25/personal-branding-agents"
TAG = "v0.2.0"


def command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Release command failed ({args[0]}, exit {result.returncode}); credentials suppressed")
    return result.stdout


def get_refs():
    return json.loads(command(["gh", "api", "--method", "GET", f"repos/{REPO}/git/matching-refs/tags/{TAG}"]))


def main():
    if os.environ.get("GITHUB_REPOSITORY") != REPO or os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Release only allowed from the designated main")
    sha = os.environ.get("GITHUB_SHA", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError("Missing exact merged SHA")
    manifest = json.loads(Path("framework-manifest.json").read_text())
    if manifest.get("method_version") != "0.2.0" or manifest.get("implementation_level") != "prompt-first":
        raise RuntimeError("Manifest scope/version does not match this release")
    existing = [r for r in get_refs() if r["ref"] == f"refs/tags/{TAG}"]
    if existing:
        if len(existing) != 1 or existing[0]["object"]["type"] != "commit" or existing[0]["object"]["sha"] != sha:
            raise RuntimeError("Existing tag points elsewhere; never retag automatically")
    else:
        command(["gh", "api", "--method", "POST", f"repos/{REPO}/git/refs", "-f", f"ref=refs/tags/{TAG}", "-f", f"sha={sha}"])
    exact = [r for r in get_refs() if r["ref"] == f"refs/tags/{TAG}"]
    if len(exact) != 1 or exact[0]["object"]["sha"] != sha or exact[0]["object"]["type"] != "commit":
        raise RuntimeError("Tag verification failed")
    releases = json.loads(command(["gh", "api", "--method", "GET", f"repos/{REPO}/releases?per_page=100"]))
    matching = [r for r in releases if r["tag_name"] == TAG]
    if matching:
        if any(r["draft"] for r in matching):
            raise RuntimeError("Existing release is draft; requires explicit reconciliation")
    else:
        command(["gh", "release", "create", TAG, "--repo", REPO, "--verify-tag", "--title", "Method 0.2.0: evidence-led prompt-first framework", "--notes-file", "docs/releases/v0.2.0.md"])
    release = json.loads(command(["gh", "api", "--method", "GET", f"repos/{REPO}/releases/tags/{TAG}"]))
    if release["draft"] or release["tag_name"] != TAG:
        raise RuntimeError("Published release not confirmed")
    print(json.dumps({"tag": TAG, "resolved_commit": sha, "release_url": release["html_url"], "tag_was_not_moved": True}))


if __name__ == "__main__":
    main()
