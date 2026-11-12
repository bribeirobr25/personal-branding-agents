"""Offline scope/oracle/history tests. Sentinels are not model behavior evidence."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import discovery_r16_language_live as runner


class LanguageDiagnosticsTests(unittest.TestCase):
    def test_exact_scope_and_reproducibility(self):
        plan, prompts = runner.make_plan('0'*64)
        self.assertEqual(plan['max_calls'], 32)
        self.assertEqual(len(plan['jobs']), 24)
        self.assertEqual(sum(len(c['turns']) for c in plan['cases']), 16)
        self.assertEqual(plan, runner.make_plan('0'*64)[0])
        for arm in prompts:
            self.assertEqual(prompts[arm], runner.cli.base.bundle(arm))

    def test_oracle_and_purpose_never_enter_projection(self):
        data = json.loads(runner.FIXTURE.read_text())
        projected = runner.project_cases(data)
        for case in data['cases']:
            case['purpose'] = 'FORBIDDEN_PURPOSE_SENTINEL'
            for turn in case['turns']:
                turn['expected'] = {'reason': 'FORBIDDEN_EXPECTED_SENTINEL'}
        self.assertEqual(projected, runner.project_cases(data))
        self.assertNotIn('FORBIDDEN_', json.dumps(projected))
        for case in projected:
            self.assertEqual(set(case), {'id', 'turns'})

    def test_approval_missing_or_changed_plan_is_rejected(self):
        plan, _ = runner.make_plan('0'*64)
        for approval in (None, '', 'wrong'):
            with self.assertRaises(ValueError): runner.check_approval(plan, approval)
        approved = runner.cli.base.digest(plan)
        runner.check_approval(plan, approved)
        plan['max_calls'] = 108
        with self.assertRaises(ValueError): runner.check_approval(plan, approved)

    def test_all_32_calls_use_only_actual_own_history(self):
        plan, prompts = runner.make_plan('0'*64)
        observed, histories = [], {}
        cases = {c['id']: c for c in plan['cases']}

        def fake_call(codex, sealed, auth, out, forbidden):
            cid, rep, arm, turn = out.name.split('-')
            turn = int(turn)
            key = (cid, arm)
            history = histories.setdefault(key, [])
            self.assertEqual(sealed, runner.cli.envelope(prompts[arm][0], history, cases[cid]['turns'][turn-1]))
            self.assertNotIn('expected', sealed)
            answer = 'OFFLINE_ACTUAL_RETURN_' + out.name
            history.extend([{'role': 'user', 'content': cases[cid]['turns'][turn-1]},
                            {'role': 'assistant', 'content': answer}])
            observed.append(out.name)
            return {'answer': answer, 'usage': None, 'seconds': 0, 'words': 1}

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'run'; out.mkdir()
            with patch.object(runner.cli, 'metadata', return_value=({}, {})), \
                 patch.object(runner.cli, 'billing_gate', return_value={'offline': True}), \
                 patch.object(runner.cli, 'call', side_effect=fake_call), contextlib.redirect_stdout(io.StringIO()):
                runner.execute(plan, prompts, out, Path(tmp)/'private', Path('/offline/codex'), Path('/offline/auth'))
            self.assertEqual(len(observed), 32)
            self.assertEqual(len(set(observed)), 32)
            self.assertEqual(json.loads((out/'summary.json').read_text())['completed_calls'], 32)

    def test_unknown_dispatch_stops_without_retry(self):
        plan, prompts = runner.make_plan('0'*64)
        def timeout(codex, sealed, auth, out, forbidden):
            out.mkdir()
            (out/'dispatch.json').write_text('{}')
            raise TimeoutError('OFFLINE_TIMEOUT')
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'run'; out.mkdir()
            with patch.object(runner.cli, 'metadata', return_value=({}, {})), \
                 patch.object(runner.cli, 'billing_gate', return_value={'offline': True}), \
                 patch.object(runner.cli, 'call', side_effect=timeout) as call:
                with self.assertRaises(TimeoutError):
                    runner.execute(plan, prompts, out, Path(tmp)/'private', Path('/offline/codex'), Path('/offline/auth'))
            self.assertEqual(call.call_count, 1)
            summary = json.loads((out/'summary.json').read_text())
            self.assertEqual(summary['completed_calls'], 0)
            self.assertEqual(len(summary['unresolved_dispatches']), 1)
            self.assertEqual(len(summary['not_forwarded']), 31)

    def test_uncertain_billing_prevents_dispatch(self):
        plan, prompts = runner.make_plan('0'*64)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'run'; out.mkdir()
            with patch.object(runner.cli, 'metadata', return_value=({}, {})), \
                 patch.object(runner.cli, 'billing_gate', side_effect=ValueError('OFFLINE_UNCERTAIN')), \
                 patch.object(runner.cli, 'call') as call:
                with self.assertRaises(ValueError):
                    runner.execute(plan, prompts, out, Path(tmp)/'private', Path('/offline/codex'), Path('/offline/auth'))
            call.assert_not_called()
            summary = json.loads((out/'summary.json').read_text())
            self.assertEqual(summary['attempted_cli_calls'], 0)
            self.assertEqual(len(summary['not_forwarded']), 32)


if __name__ == '__main__':
    unittest.main()
