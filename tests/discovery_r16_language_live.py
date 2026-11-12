#!/usr/bin/env python3
"""L01–L12 controller using the already-qualified Codex CLI wire/OS boundary.

Default is OFFLINE. Live requires an explicitly approved exact plan hash.
The controller never sends fixture expected/purpose/rubric fields to the model.
"""
import argparse
import json
from pathlib import Path
import random
import shutil
import subprocess

import discovery_codex_cli as cli

ROOT = cli.base.ROOT
FIXTURE = ROOT / 'tests/discovery-r16-language-diagnostics-2026-11-12.json'
FIXTURE_REF = 'e9dc6930afe0c616fa89ca64170679a6310199cb'
IDS = [f'L{i:02d}' for i in range(1, 13)]
SEED = 20261112


def project_cases(fixture):
    """One-way projection: only IDs for scheduling and literal user text survive."""
    cases = [{'id': c['id'], 'turns': [turn['user'] for turn in c['turns']]}
             for c in fixture['cases']]
    if ([c['id'] for c in cases] != IDS or sum(len(c['turns']) for c in cases) != 16
            or any(len(c['turns']) not in (1, 2) for c in cases)
            or any(not isinstance(u, str) or not u for c in cases for u in c['turns'])):
        raise ValueError('Exact L01-L12 / sixteen-turn diagnostic scope required')
    return cases


def make_plan(binary_sha):
    raw = FIXTURE.read_bytes()
    pinned = subprocess.check_output(['git', 'show', f'{FIXTURE_REF}:{FIXTURE.relative_to(ROOT)}'], cwd=ROOT)
    if raw != pinned:
        raise ValueError('Diagnostic fixture differs from its reviewed frozen version')
    fixture = json.loads(raw)
    if (fixture['baseline_ref'] != cli.base.REFS['A']
            or fixture['candidate_ref'] != cli.base.REFS['B']):
        raise ValueError('Frozen A/B reference mismatch')
    cases = project_cases(fixture)
    prompts = {arm: cli.base.bundle(arm) for arm in cli.base.REFS}
    jobs = [(c['id'], 1, arm) for c in cases for arm in cli.base.REFS]
    random.Random(SEED).shuffle(jobs)
    plan = {'schema': 1, 'stage': 'r16_language_diagnostics',
            'scope': 'L01-L12 only; no R-series pilot or 108-call battery',
            'refs': cli.base.REFS, 'fixture_ref': FIXTURE_REF,
            'fixture_sha256': cli.sha(raw), 'model': cli.MODEL,
            'cli_version': cli.VERSION, 'cli_sha256': binary_sha,
            'runner_sha256': cli.sha(Path(__file__).read_bytes()),
            'transport_sha256': cli.sha(Path(cli.__file__).read_bytes()),
            'loader_sha256': cli.sha(Path(cli.base.__file__).read_bytes()),
            'prompt_hashes': {a: p[1] for a, p in prompts.items()},
            'instructions_hashes': {a: cli.base.digest(p[0]) for a, p in prompts.items()},
            'cases': cases, 'jobs': jobs, 'repeats': 1, 'order_seed': SEED,
            'max_calls': 32, 'endpoint': cli.ENDPOINT, 'tools': [], 'retries': 0,
            'reasoning_effort': 'low', 'sampling': 'unchanged provider defaults',
            'network_timeout_seconds': cli.TIMEOUT, 'cli_timeout_seconds': cli.TIMEOUT + 30,
            'max_output_tokens': None, 'cost_policy': 'included_only_zero_credit_balance_no_fallback',
            'review': {'explicit_reply_language_arm_turns': 24,
                       'ambiguous_reply_language_arm_turns': 8,
                       'ambiguous_verdict': 'INDETERMINATE',
                       'deliverable_language': 'separate pending preference unless an actual artifact is produced',
                       'expected_fields_in_model_context': False,
                       'judge_calls': 0, 'independent_review': 'NOT_RUN'}}
    return plan, prompts


def check_approval(plan, approved_hash):
    # This binds a real human decision; passing a flag is not proof of that decision.
    if not approved_hash or approved_hash != cli.base.digest(plan):
        raise ValueError('Explicit authorization for this exact 32-call plan required')


def execute(plan, prompts, out, private_out, codex, auth_path):
    cases = {c['id']: c for c in plan['cases']}
    labels = [f'{cid}-{rep}-{arm}-{turn}' for cid, rep, arm in plan['jobs']
              for turn in range(1, len(cases[cid]['turns']) + 1)]
    rows, attempted, status = [], 0, 'RUNNING'
    private_out.mkdir(parents=True, exist_ok=False, mode=0o700)
    canary = private_out / 'forbidden-canary.txt'
    canary.write_text('FICTIONAL_EXPECTED_FUTURE_OTHER_ARM_MEMORY_CANARY')
    forbidden = [FIXTURE, ROOT/'AGENTS.md',
                 ROOT/'docs/proposals/discovery-r16-language-intent-investigation-2026-11-12.md', canary]
    label = None
    try:
        for cid, rep, arm in plan['jobs']:
            history = []
            for turn, user in enumerate(cases[cid]['turns'], 1):
                label = f'{cid}-{rep}-{arm}-{turn}'
                raw, auth = cli.metadata(codex, auth_path, private_out/f'{label}-billing.json')
                cli.base.save(out/f'{label}-billing.json', cli.billing_gate(raw))
                attempted += 1
                cli.base.save(out/'progress.json', {'status': 'OUTCOME_UNKNOWN',
                              'current': label, 'attempted_cli_calls': attempted})
                # Never pass the original fixture record, expected fields or another history.
                row = cli.call(codex, cli.envelope(prompts[arm][0], history, user),
                               auth, out/label, forbidden)
                row.update({'case': cid, 'rep': rep, 'arm': arm, 'turn': turn})
                rows.append(row)
                cli.base.save(out/'rows.json', rows)
                history.extend([{'role': 'user', 'content': user},
                                {'role': 'assistant', 'content': row['answer']}])
                cli.base.save(out/'progress.json', {'status': 'CALL_COMPLETED',
                              'current': label, 'completed_calls': len(rows)})
                print(json.dumps({'completed': len(rows), 'expected': 32, 'label': label}), flush=True)
        status = 'GENERATED_NOT_REVIEWED'
    except Exception as exc:
        status = 'STOPPED_OUTCOME_REQUIRES_REVIEW'
        cli.base.save(out/'failure.json', {'type': type(exc).__name__, 'current': label,
                                         'automatic_retry': False})
        raise
    finally:
        complete = {f"{r['case']}-{r['rep']}-{r['arm']}-{r['turn']}" for r in rows}
        dispatches = [name for name in labels if (out/name/'dispatch.json').exists()]
        cli.base.save(out/'rows.json', rows)
        cli.base.save(out/'summary.json', {'status': status, 'stage': plan['stage'],
                      'attempted_cli_calls': attempted, 'forwarded_requests': len(dispatches),
                      'completed_calls': len(rows), 'expected_calls': 32,
                      'unresolved_dispatches': [n for n in dispatches if n not in complete],
                      'not_forwarded': [n for n in labels if n not in dispatches],
                      'isolation': 'PENDING_SEPARATE_AUDIT', 'actual_cost_usd': None,
                      'behavioral_winner': None, 'independent_review': 'NOT_RUN'})
        cli.base.save(out/'manifest.json', cli.manifest(out))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--approved-plan-sha256')
    parser.add_argument('--private-out', type=Path)
    parser.add_argument('--codex', type=Path, default=Path.home()/'.local/bin/codex')
    parser.add_argument('--auth', type=Path, default=Path.home()/'.codex/auth.json')
    args = parser.parse_args()
    if cli.base.git('branch', '--show-current') != cli.base.BRANCH:
        parser.error('Authorized branch only')
    version = subprocess.check_output([str(args.codex), '--version'], text=True).strip()
    if version != cli.VERSION:
        parser.error('Changed CLI version requires requalification')
    plan, prompts = make_plan(cli.sha(args.codex.resolve().read_bytes()))
    if args.live:
        check_approval(plan, args.approved_plan_sha256)
        if not args.private_out or args.private_out.resolve().is_relative_to(ROOT):
            parser.error('Private receipts must stay outside Git')
    args.out.mkdir(parents=True, exist_ok=False)
    cli.base.save(args.out/'plan.json', plan)
    cli.base.save(args.out/'plan-hash.json', {'sha256': cli.base.digest(plan)})
    for source, name in [(Path(__file__), 'runner-source.py'), (Path(cli.__file__), 'transport-source.py'),
                         (Path(cli.base.__file__), 'frozen-loader-source.py')]:
        shutil.copy2(source, args.out/name)
    for arm, prompt in prompts.items():
        (args.out/f'{arm}.instructions.txt').write_text(prompt[0])
    if args.live:
        execute(plan, prompts, args.out, args.private_out, args.codex, args.auth)
    else:
        for case in plan['cases']:
            for arm in prompts:
                payload = cli.wire_request(cli.envelope(prompts[arm][0], [], case['turns'][0]))
                cli.base.save(args.out/f"{case['id']}-{arm}-turn1.request.json", payload)
        cli.base.save(args.out/'summary.json', {'status': 'AWAITING_EXPLICIT_USER_AUTHORIZATION',
                      'planned_calls': 32, 'model_calls': 0,
                      'second_turn_payloads': 'Not materialized until actual same-arm first response'})
        cli.base.save(args.out/'manifest.json', cli.manifest(args.out))
    print(json.dumps({'plan_sha256': cli.base.digest(plan), 'planned_calls': 32, 'live': args.live}))


if __name__ == '__main__':
    main()
