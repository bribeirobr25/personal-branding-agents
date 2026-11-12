"""Offline transport doubles are sentinels, never benchmark answers."""
import copy
import json
import tempfile
import time
import unittest
from unittest.mock import patch
from pathlib import Path

import discovery_codex_cli as cli


def billing():
    return {'observed_at': time.time(),
            'account': {'account': {'type': 'chatgpt', 'planType': 'pro'}},
            'limits': {'rateLimits': {'limitId': 'codex',
                'primary': {'usedPercent': 10}, 'secondary': None,
                'credits': {'hasCredits': False, 'unlimited': False, 'balance': '0'},
                'spendControlReached': False, 'rateLimitReachedType': None}}}


def stream(item=None, status='completed'):
    item = item or {'id': 'offline_msg', 'type': 'message', 'role': 'assistant',
                    'status': 'completed', 'content': [{'type': 'output_text',
                    'text': 'OFFLINE_TRANSPORT_SENTINEL', 'annotations': []}]}
    response = {'id': 'offline_response', 'object': 'response', 'status': status,
                'model': cli.MODEL, 'output': [item],
                'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}
    events = [{'type': 'response.created', 'response': dict(response, output=[], status='in_progress')},
              {'type': 'response.output_item.added', 'output_index': 0, 'item': item},
              {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
              {'type': 'response.completed', 'response': response}]
    return b''.join(('data: ' + json.dumps(e) + '\n\n').encode() for e in events)


class AdapterTests(unittest.TestCase):
    def test_billing_only_known_included_without_credits(self):
        self.assertTrue(cli.billing_gate(billing())['credit_balance_zero'])
        for field, value in [('credits', None), ('credits', {'hasCredits': True, 'unlimited': False, 'balance': '1'}),
                             ('spendControlReached', None), ('primary', {'usedPercent': 90}),
                             ('rateLimitReachedType', 'rate_limit_reached')]:
            raw = billing()
            raw['limits']['rateLimits'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                cli.billing_gate(raw)

    def test_billing_api_unknown_credit_unlimited_and_stale_rejected(self):
        for mutate in [lambda r: r['account']['account'].update(type='apiKey'),
                       lambda r: r['account']['account'].update(planType='enterprise'),
                       lambda r: r['limits']['rateLimits']['credits'].update(unlimited=True),
                       lambda r: r.update(observed_at=time.time()-61)]:
            raw = billing(); mutate(raw)
            with self.assertRaises(ValueError):
                cli.billing_gate(raw)

    def test_billing_public_receipt_omits_identity_and_analytics(self):
        raw = billing()
        raw['account']['account']['email'] = 'fictional@example.invalid'
        receipt = json.dumps(cli.billing_gate(raw))
        for forbidden in ('email', 'example.invalid', 'usedPercent', 'planType'):
            self.assertNotIn(forbidden, receipt)

    def test_payload_only_current_turn_and_own_actual_history(self):
        history = [{'role': 'user', 'content': 'OWN_U1'},
                   {'role': 'assistant', 'content': 'ACTUAL_OWN_A1'}]
        sealed = cli.envelope('FROZEN_A', history, 'OWN_U2')
        wire = cli.wire_request(sealed)
        self.assertEqual(wire['input'], history + [{'role': 'user', 'content': 'OWN_U2'}])
        self.assertEqual(wire['instructions'], 'FROZEN_A')
        self.assertEqual(wire['tools'], [])
        self.assertFalse(wire['store'])
        for field in ('previous_response_id', 'conversation', 'prompt_cache_key', 'client_metadata'):
            self.assertNotIn(field, wire)

    def test_future_turns_and_extra_fields_cannot_enter_builder(self):
        with self.assertRaises(TypeError):
            cli.envelope('P', [], 'U1', future='FUTURE')
        for bad in [[{'role': 'user', 'content': 'U1'}],
                    [{'role': 'user', 'content': 'U1', 'expected': 'SECRET'},
                     {'role': 'assistant', 'content': 'A1'}]]:
            with self.assertRaises(ValueError):
                cli.envelope('P', bad, 'U2')

    def test_wire_ignores_cli_added_or_untrusted_fields(self):
        sealed = cli.envelope('P', [], 'U1')
        expected = cli.wire_request(sealed)
        poisoned = dict(sealed, tools=['FILES'], memory='PERSONAL', other_arm='OTHER', future='FUTURE')
        self.assertEqual(cli.wire_request(poisoned), expected)

    def test_tool_refusal_incomplete_and_missing_completion_rejected(self):
        bad_items = [{'type': 'function_call', 'name': 'view_image', 'arguments': '{}'},
                     {'type': 'message', 'role': 'assistant', 'content': [{'type': 'refusal', 'refusal': 'NO'}]}]
        for item in bad_items:
            with self.assertRaises(ValueError):
                cli.parse_stream(stream(item))
        with self.assertRaises(ValueError):
            cli.parse_stream(stream(status='incomplete'))
        with self.assertRaises(ValueError):
            cli.parse_stream(b'data: {"type":"response.created"}\n\n')
        with self.assertRaises(ValueError):
            cli.parse_stream(stream() + stream())

    def test_complete_stream_preserved(self):
        response, answer = cli.parse_stream(stream())
        self.assertEqual(answer, 'OFFLINE_TRANSPORT_SENTINEL')
        self.assertEqual(response['id'], 'offline_response')

    def test_schedules_frozen_and_separate(self):
        pilot, prompts = cli.make_plan('pilot')
        battery, _ = cli.make_plan('battery')
        self.assertEqual(pilot['max_calls'], 12)
        self.assertEqual(battery['max_calls'], 108)
        self.assertEqual({c['id'] for c in pilot['cases']}, set(cli.PILOT))
        self.assertEqual(pilot['refs'], cli.base.REFS)
        for arm in prompts:
            self.assertEqual(prompts[arm], cli.base.bundle(arm))

    def test_environment_does_not_inherit_host_state(self):
        self.assertEqual(set(cli.clean_env(Path('/fictional'))),
                         {'PATH', 'HOME', 'CODEX_HOME', 'TMPDIR', 'LANG'})

    def test_auth_api_or_missing_tokens_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'auth.json'
            for auth in [{'auth_mode': 'apikey', 'OPENAI_API_KEY': 'OFFLINE'},
                         {'auth_mode': 'chatgpt', 'tokens': {}}]:
                path.write_text(json.dumps(auth))
                with self.assertRaises(ValueError):
                    cli.read_auth(path)

    def test_incomplete_pilot_cannot_start_battery_or_read_account(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pilot = root/'pilot'; pilot.mkdir()
            (pilot/'summary.json').write_text(json.dumps({
                'status': 'STOPPED_OUTCOME_REQUIRES_REVIEW', 'completed_calls': 9}))
            argv = ['runner', '--stage', 'battery', '--live', '--pilot', str(pilot),
                    '--out', str(root/'must-not-exist'), '--private-out', str(root/'private')]
            with patch('sys.argv', argv), patch.object(cli.base, 'git', return_value=cli.base.BRANCH), \
                 patch.object(cli.subprocess, 'check_output', return_value=cli.VERSION), \
                 patch.object(cli, 'make_plan', return_value=({'adapter_sha256': 'unused'}, {})), \
                 patch.object(cli, 'metadata') as account, self.assertRaises(SystemExit):
                cli.main()
            account.assert_not_called()
            self.assertFalse((root/'must-not-exist').exists())

    def test_readonly_receipt_does_not_authorize_positive_credits(self):
        raw = billing()
        raw['limits']['rateLimits']['credits']['balance'] = '0.01'
        with self.assertRaises(ValueError):
            cli.billing_gate(raw)

    def test_behavioral_gate_requires_all_turns_and_rejects_language_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'manifest.json').write_text('{}')
            review = {'status': 'QUALIFIED', 'context_audit': 'PASS',
                      'pilot_manifest_sha256': cli.sha((root/'manifest.json').read_bytes()),
                      'turns': [{'case': cid, 'arm': arm, 'turn': turn,
                                 'hard_gates': dict.fromkeys(cli.HARD_GATES, 'PASS'),
                                 'language_name': 'PASS', 'evidence': 'OFFLINE_GATE_SENTINEL'}
                                for cid in cli.PILOT for arm in cli.base.REFS for turn in (1, 2)]}
            cli.check_pilot_review(root, review)
            for change in ('language', 'missing', 'duplicate', 'hash', 'uncertain'):
                bad = copy.deepcopy(review)
                if change == 'language': bad['turns'][-1]['language_name'] = 'FAIL'
                if change == 'missing': bad['turns'].pop()
                if change == 'duplicate': bad['turns'][0] = bad['turns'][1]
                if change == 'hash': bad['pilot_manifest_sha256'] = 'wrong'
                if change == 'uncertain': bad['turns'][0]['hard_gates']['consent'] = 'UNCERTAIN'
                with self.subTest(change=change), self.assertRaises(ValueError):
                    cli.check_pilot_review(root, bad)

    def test_headers_and_partial_stream_survive_timeout_without_retry(self):
        class Response:
            headers = {'x-request-id': 'OFFLINE_REQUEST_ID'}
            calls = 0
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read1(self, size):
                self.calls += 1
                if self.calls == 1:
                    return b'data: {"type":"response.created","response":{"id":"OFFLINE_RESPONSE_ID"}}\n\n'
                raise TimeoutError()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            broker = cli.Broker(cli.envelope('P', [], 'U'), {'tokens': {'access_token': 'OFFLINE'}}, root)
            response = Response()
            with patch.object(cli.urllib.request, 'build_opener') as factory:
                factory.return_value.open.return_value = response
                with self.assertRaises(TimeoutError): broker.forward(cli.wire_request(broker.sealed))
                self.assertEqual(factory.return_value.open.call_count, 1)
                self.assertEqual(factory.return_value.open.call_args.kwargs['timeout'], 180)
            self.assertEqual(json.loads((root/'receipt.json').read_text())['x-request-id'], 'OFFLINE_REQUEST_ID')
            trace = json.loads((root/'network-trace.json').read_text())
            self.assertEqual(trace['provider_response_id'], 'OFFLINE_RESPONSE_ID')
            self.assertEqual(trace['phase'], 'STREAM_READ')
            self.assertEqual(trace['error_type'], 'TimeoutError')
            self.assertTrue((root/'response.sse').read_bytes())

    def test_timeout_before_headers_records_http_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            broker = cli.Broker(cli.envelope('P', [], 'U'), {'tokens': {'access_token': 'OFFLINE'}}, root)
            with patch.object(cli.urllib.request, 'build_opener') as factory:
                factory.return_value.open.side_effect = TimeoutError()
                with self.assertRaises(TimeoutError): broker.forward(cli.wire_request(broker.sealed))
                self.assertEqual(factory.return_value.open.call_count, 1)
            trace = json.loads((root/'network-trace.json').read_text())
            self.assertEqual(trace['phase'], 'HTTP_OPEN')
            self.assertEqual(trace['received_bytes'], 0)
            self.assertIsNone(trace['provider_response_id'])
            self.assertFalse((root/'receipt.json').exists())


if __name__ == '__main__':
    unittest.main()
