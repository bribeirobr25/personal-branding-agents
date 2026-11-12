#!/usr/bin/env python3
"""Audit actual model-bound inputs against frozen prompts and actual same-arm history.

Does not score behavior, infer source access, or manufacture missing responses.
Writes a separate report so the generation manifest remains immutable.
"""
import argparse
import json
from pathlib import Path
import statistics

import discovery_codex_cli as cli


def audit(run, allow_partial=False):
    plan = json.loads((run/'plan.json').read_text())
    summary = json.loads((run/'summary.json').read_text())
    manifest = json.loads((run/'manifest.json').read_text())
    if manifest != cli.manifest(run):
        raise ValueError('Manifest mismatch')
    if summary['completed_calls'] != plan['max_calls'] and not allow_partial:
        raise ValueError('Incomplete run')
    rows = json.loads((run/'rows.json').read_text())
    by_key = {(r['case'], r['rep'], r['arm'], r['turn']): r for r in rows}
    if len(by_key) != len(rows):
        raise ValueError('Duplicate turn')
    cases = {c['id']: c for c in plan['cases']}
    cards, key, checks, unknown, not_sent = [], {}, [], [], []
    for i, (cid, rep, arm) in enumerate(plan['jobs']):
        prompt, hashes = cli.base.bundle(arm)
        if hashes != plan['prompt_hashes'][arm] or (run/f'{arm}.instructions.txt').read_text() != prompt:
            raise ValueError('Frozen prompt drift')
        history, answers = [], []
        for turn, user in enumerate(cases[cid]['turns'], 1):
            label = f'{cid}-{rep}-{arm}-{turn}'
            folder = run/label
            if not (folder/'request.json').exists():
                not_sent.append(label)
                continue
            request = json.loads((folder/'request.json').read_text())
            expected = cli.wire_request(cli.envelope(prompt, history, user))
            if request != expected:
                raise ValueError('Model-bound context contamination: ' + label)
            if (cid, rep, arm, turn) not in by_key:
                transport = json.loads((folder/'transport.json').read_text())
                unknown.append({'label': label, 'transport': transport,
                                'request_context_check': 'PASS'})
                continue
            row = by_key[cid, rep, arm, turn]
            response, answer = cli.parse_stream((folder/'response.sse').read_bytes())
            if answer != row['answer'] or answer != (folder/'answer.txt').read_text():
                raise ValueError('Response preservation mismatch')
            if response.get('model') != cli.MODEL:
                raise ValueError('Returned model drift')
            transport = json.loads((folder/'transport.json').read_text())
            if transport['forwarded_requests'] != 1 or transport['cli_requests'] != 1 or transport['returncode'] != 0:
                raise ValueError('Dispatch count mismatch')
            sandbox = json.loads((folder/'sandbox-checks.json').read_text())
            if not sandbox or any(r['read_succeeded'] != (r['kind'] == 'allowed') for r in sandbox):
                raise ValueError('Sandbox control mismatch')
            billing = json.loads((run/f'{label}-billing.json').read_text())
            if billing['credit_balance_zero'] is not True or billing['credit_usage_available'] is not False:
                raise ValueError('Billing gate mismatch')
            checks.append({'label': label, 'request_sha256': cli.base.digest(request),
                           'response_sse_sha256': cli.sha((folder/'response.sse').read_bytes()),
                           'current_turn_and_own_actual_history': 'PASS', 'tools_empty': 'PASS',
                           'frozen_prompt': 'PASS', 'os_controls': 'PASS', 'billing_preflight': 'PASS'})
            history.extend([{'role': 'user', 'content': user}, {'role': 'assistant', 'content': answer}])
            answers.append(answer)
        card_id = f'card-{i:03d}'
        if not answers:
            continue
        cards.append({'id': card_id, 'user_turns': cases[cid]['turns'][:len(answers)],
                      'assistant_turns': answers, 'hard_gates': None, 'scores': None,
                      'evidence': None, 'complete_pair': len(answers) == 2,
                      'complete_dialogue': len(answers) == len(cases[cid]['turns']),
                      'review_status': 'NOT_REVIEWED'})
        key[card_id] = {'case': cid, 'rep': rep, 'arm': arm}
    aggregate = {}
    for arm in cli.base.REFS:
        subset = [r for r in rows if r['arm'] == arm]
        aggregate[arm] = {'calls': len(subset), 'words': sum(r['words'] for r in subset),
                          'input_tokens': sum(r['usage']['input_tokens'] for r in subset),
                          'output_tokens': sum(r['usage']['output_tokens'] for r in subset),
                          'median_seconds': statistics.median(r['seconds'] for r in subset) if subset else None}
    return {'status': 'PARTIAL' if unknown or not_sent else 'PASS',
            'scope': 'transport/context integrity, NOT behavioral review',
            'checked_calls': len(checks), 'checks': checks, 'aggregate': aggregate,
            'outcome_unknown': unknown, 'not_sent': not_sent,
            'behavioral_winner': None, 'independent_review': 'NOT_RUN'}, cards, key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--allow-partial', action='store_true')
    args = parser.parse_args()
    report, cards, key = audit(args.run, args.allow_partial)
    args.out.mkdir(parents=True, exist_ok=False)
    cli.base.save(args.out/'audit.json', report)
    cli.base.save(args.out/'review-cards.json', cards)
    cli.base.save(args.out/'review-key.json', key)
    print(json.dumps({k:v for k,v in report.items() if k != 'checks'}))


if __name__ == '__main__':
    main()
