"""Offline tests of repository administration; no GitHub requests or deletions."""
import copy
import importlib.util
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

cleanup = load("cleanup_public", ".github/scripts/prune_retired_branch.py")
release = load("release_public", ".github/scripts/publish_method_release.py")

class MaintenanceTests(unittest.TestCase):
    def branches(self):
        return [{"name": "main", "commit": {"sha": cleanup.EXPECTED}},
                {"name": "feat/creative-strategist-concept-gate-20261110", "commit": {"sha": "candidate"}},
                {"name": cleanup.RETIRED, "protected": False, "commit": {"sha": cleanup.EXPECTED}}]
    def audit(self, branches=None, prs=None, compare=None):
        rows = self.branches() if branches is None else branches
        def fake_get(path, pages=False):
            if path.startswith("branches?"): return rows
            if path.startswith("pulls?"): return [] if prs is None else prs
            if path.startswith("compare/"):
                return {"status":"identical", "merge_base_commit":{"sha":cleanup.EXPECTED}} if compare is None else compare
            raise AssertionError("Unexpected API request")
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": cleanup.REPO}), patch.object(cleanup, "get", side_effect=fake_get):
            return cleanup.audit()
    def test_safe_ancestor(self):
        self.assertEqual(self.audit(), "safe_ancestor")
    def test_already_absent(self):
        self.assertEqual(self.audit(branches=self.branches()[:2]), "already_absent")
    def test_changed_head(self):
        rows=self.branches();rows[2]["commit"]["sha"]="changed"
        with self.assertRaises(RuntimeError): self.audit(branches=rows)
    def test_protected(self):
        rows=self.branches();rows[2]["protected"]=True
        with self.assertRaises(RuntimeError): self.audit(branches=rows)
    def test_dependent_head_pr(self):
        with self.assertRaises(RuntimeError): self.audit(prs=[{"head":{"ref":cleanup.RETIRED}}])
    def test_dependent_base_pr(self):
        with self.assertRaises(RuntimeError): self.audit(prs=[{"base":{"ref":cleanup.RETIRED}}])
    def test_unpreserved_head(self):
        with self.assertRaises(RuntimeError): self.audit(compare={"status":"diverged","merge_base_commit":{"sha":"other"}})
    def test_missing_active(self):
        with self.assertRaises(RuntimeError): self.audit(branches=[self.branches()[0],self.branches()[2]])
    def test_wrong_repository(self):
        with patch.dict(os.environ, {"GITHUB_REPOSITORY":"example/other"}), self.assertRaises(RuntimeError): cleanup.audit()
    def test_existing_release_tag_is_not_moved(self):
        env={"GITHUB_REPOSITORY":release.REPO,"GITHUB_REF":"refs/heads/main","GITHUB_SHA":"a"*40}
        existing=[{"ref":"refs/tags/v0.2.0","object":{"type":"commit","sha":"b"*40}}]
        with patch.dict(os.environ,env), patch.object(release,"get_refs",return_value=existing), patch.object(release,"command") as write:
            with self.assertRaises(RuntimeError): release.main()
            write.assert_not_called()
    def test_release_not_from_working_branch(self):
        with patch.dict(os.environ,{"GITHUB_REPOSITORY":release.REPO,"GITHUB_REF":"refs/heads/working"}), patch.object(release,"command") as write:
            with self.assertRaises(RuntimeError): release.main()
            write.assert_not_called()
    def test_owner_authority_is_required_and_blank(self):
        contract=json.loads((ROOT/"contracts/framework.json").read_text())
        blank=json.loads((ROOT/"templates/approval-record.json").read_text())
        self.assertTrue({"actor_role","authority_ref"} <= set(contract["approval_required"]))
        self.assertIn("owner_authority_must_be_verified", contract["rules"])
        self.assertIsNone(blank["actor_role"]);self.assertIsNone(blank["authority_ref"])
        self.assertEqual(blank["status"],"not_approved")
    def test_hidden_python_syntax(self):
        for filename in (ROOT/".github/scripts").glob("*.py"):
            compile(filename.read_text(),str(filename),"exec")

if __name__=="__main__": unittest.main()
