import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import discovery_live_ab as runner


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.plan, self.prompts = runner.make_plan('MODEL_PENDING_OWNER_SELECTION', repeats=1, ids=['R01', 'R16'])
        self.approval = {'plan_sha256': runner.digest(self.plan), 'owner_approved': True,
                         'max_calls': 8, 'provider_budget_enforced': True, 'budget_usd': 1}

    def test_exact_original_fixtures(self):
        text = (runner.ROOT / 'tests/results/discovery-behavior-ab-round4-dialogues-2026-11-12.md').read_text()
        cases = json.loads((runner.ROOT / 'tests/discovery_live_cases.json').read_text())['cases']
        self.assertEqual(len(cases), 16)
        for case in cases:
            block = text.split('## ' + case['id'] + ':')[1].split('\n## ')[0]
            for i, turn in enumerate(case['turns'], 1):
                self.assertIn(f'**User {i}, identical for A/B:** {turn}', block)

    def test_no_future_or_other_arm_in_requests(self):
        calls = []
        def fake(payload):
            calls.append(payload)
            return json.dumps({'status': 'completed', 'model': 'TEST_DOUBLE_NOT_LLM',
                'output': [{'type': 'message', 'role': 'assistant', 'content': [
                    {'type': 'output_text', 'text': 'TRANSPORT_SENTINEL_' + str(len(calls))}]}]}), 'fake-receipt'
        with tempfile.TemporaryDirectory() as d:
            runner.execute(self.plan, self.prompts, Path(d), self.approval, fake)
            for n in range(0, len(calls), 2):
                first, second = calls[n:n+2]
                self.assertEqual(len(first['input']), 1)
                self.assertEqual(len(second['input']), 3)
                self.assertEqual(second['input'][1]['content'], 'TRANSPORT_SENTINEL_' + str(n+1))
                self.assertNotIn('Actually call me Sol', json.dumps(first))
                self.assertNotIn('The team used the handoff checklist', json.dumps(first))
                self.assertEqual(first['tools'], [])
                self.assertFalse(first['store'])
                self.assertNotIn('previous_response_id', first)
            self.assertEqual(len(json.loads((Path(d) / 'review-cards.json').read_text())), 4)

    def test_missing_and_tampered_approval_make_zero_calls(self):
        for approval in [{}, dict(self.approval, plan_sha256='wrong'),
                         dict(self.approval, provider_budget_enforced=False),
                         dict(self.approval, max_calls=1000)]:
            with tempfile.TemporaryDirectory() as d, patch.object(runner, 'invoke') as mock:
                with self.assertRaises(ValueError):
                    runner.execute(self.plan, self.prompts, Path(d), approval, mock)
                mock.assert_not_called()

    def test_timeout_stops_without_retry(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(runner, 'invoke', side_effect=TimeoutError) as mock:
                with self.assertRaises(TimeoutError):
                    runner.execute(self.plan, self.prompts, Path(d), self.approval, mock)
                self.assertEqual(mock.call_count, 1)
            summary = json.loads((Path(d) / 'summary.json').read_text())
            self.assertEqual(summary['attempted_calls'], 1)
            self.assertEqual(summary['completed_calls'], 0)
            self.assertIsNone(summary['behavioral_winner'])

    def test_incomplete_response_preserved_and_stops(self):
        raw = json.dumps({'status': 'incomplete', 'output': []})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                runner.execute(self.plan, self.prompts, Path(d), self.approval, lambda _: (raw, 'fake'))
            self.assertEqual(len(list(Path(d).glob('*.response.json'))), 1)
            self.assertEqual(json.loads((Path(d) / 'review-cards.json').read_text()), [])

    def test_prompt_snapshots_and_shared_contracts(self):
        self.assertNotEqual(self.prompts['A'][0], self.prompts['B'][0])
        for path in runner.SHARED:
            self.assertEqual(self.prompts['A'][1][path], self.prompts['B'][1][path])
        self.assertEqual(runner.make_plan('x')[0]['max_calls'], 108)
        self.assertEqual(runner.make_plan('x', ids=['R%02d' % i for i in range(1, 17)])[0]['max_calls'], 192)

    def test_schedule_and_plan_are_reproducible(self):
        again, _ = runner.make_plan('MODEL_PENDING_OWNER_SELECTION', repeats=1, ids=['R01', 'R16'])
        self.assertEqual(runner.digest(again), runner.digest(self.plan))
        self.assertNotEqual(runner.digest(dict(again, model='other')), runner.digest(self.plan))

    def test_bad_selection_and_limits_rejected(self):
        for kwargs in [{'ids': ['R99']}, {'ids': []}, {'repeats': 0}, {'max_tokens': 10000}]:
            with self.assertRaises(ValueError):
                runner.make_plan('x', **kwargs)

    def test_refusals_and_unexpected_tools_rejected(self):
        for item in [{'type': 'function_call'}, {'type': 'message', 'role': 'assistant',
                       'content': [{'type': 'refusal', 'refusal': 'no'}]}]:
            with self.assertRaises(ValueError):
                runner.extract({'status': 'completed', 'output': [item]})


if __name__ == '__main__':
    unittest.main()
