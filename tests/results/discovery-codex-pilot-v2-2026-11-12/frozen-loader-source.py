#!/usr/bin/env python3
"""Stateless, tool-free Responses API comparison. Default plan mode never calls a model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import time
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'feat/onboarding-strategic-discovery-20261111'
REFS = {'A': '0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92',
        'B': '3fd226adcf34376e99e7fbda11ace36638e3b370'}
FILES = ['agents/orchestrator.md', 'agents/researcher.md', 'workflows/onboarding.md']
SHARED = ['docs/agent-contracts.md', 'contracts/framework.json', 'docs/security-and-privacy.md']
PRIORITY = ['R01', 'R03', 'R07', 'R09', 'R10', 'R11', 'R13', 'R14', 'R16']
HOST = ('Act as the Orchestrator for the supplied method. Return only your next user-facing reply. '
        'Host capabilities: no browsing, source retrieval, file access, publication, memory service, '
        'or specialist tools are available. Researcher instructions are reference guidance only; '
        'no independent Researcher is running. The transcript contains all available user evidence. '
        'Do not describe hypothetical source access as an executed action.')
ENDPOINT = 'https://api.openai.com/v1/responses'


def encoded(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def digest(obj):
    return hashlib.sha256(encoded(obj)).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def bundle(arm):
    chunks = [HOST]
    hashes = {}
    for path in FILES + SHARED:
        ref = REFS[arm] if path in FILES else REFS['A']
        content = subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT).decode()
        hashes[path] = hashlib.sha256(content.encode()).hexdigest()
        chunks.append(f'\n--- {path} ---\n{content}')
    return '\n'.join(chunks), hashes


def request(model, instructions, history, user, max_tokens):
    # Intentionally cannot receive a whole case, future turn, rubric, or arm label.
    return {'model': model, 'instructions': instructions,
            'input': [*history, {'role': 'user', 'content': user}],
            'tools': [], 'store': False, 'max_output_tokens': max_tokens}


def extract(response):
    if response.get('status') != 'completed':
        raise ValueError('Provider response incomplete; no automatic retry')
    texts = []
    for item in response.get('output', []):
        if item['type'] == 'reasoning':
            continue
        if item['type'] != 'message' or item.get('role') != 'assistant':
            raise ValueError('Unexpected provider output item')
        for content in item['content']:
            if content['type'] != 'output_text':
                raise ValueError('Refusal or unexpected content; preserve and stop')
            texts.append(content['text'])
    answer = '\n'.join(texts)
    if not answer.strip():
        raise ValueError('Empty response')
    return answer


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise RuntimeError('Redirect forbidden')


def invoke(payload):
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY unavailable')
    req = urllib.request.Request(ENDPOINT, data=encoded(payload), headers={
        'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    # No redirects, retry, tools, previous_response_id or shared remote conversation.
    with urllib.request.build_opener(NoRedirect).open(req, timeout=120) as response:
        return response.read().decode(), response.headers.get('x-request-id')


def make_plan(model, repeats=3, seed=20261112, max_tokens=2048, ids=None):
    if not model.strip() or not 1 <= repeats <= 3 or not 128 <= max_tokens <= 4096:
        raise ValueError('Invalid model/repeat/token bounds')
    source = json.loads((ROOT / 'tests/discovery_live_cases.json').read_text())
    ids = PRIORITY if ids is None else ids
    selected = [c for c in source['cases'] if c['id'] in ids]
    if len(selected) != len(set(ids)) or not selected:
        raise ValueError('Unknown or empty case selection')
    prompts = {arm: bundle(arm) for arm in REFS}
    jobs = [(c['id'], rep, arm) for c in selected for rep in range(1, repeats + 1) for arm in REFS]
    random.Random(seed).shuffle(jobs)
    plan = {'schema': 1, 'mode': 'stateless_tool_free_model_calls', 'refs': REFS,
            'model': model, 'repeats': repeats, 'order_seed': seed, 'max_output_tokens': max_tokens,
            'max_calls': len(jobs) * 2, 'cases': selected, 'jobs': jobs,
            'prompt_hashes': {a: p[1] for a, p in prompts.items()},
            'instructions_hashes': {a: digest(p[0]) for a, p in prompts.items()},
            'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'endpoint': ENDPOINT, 'tools': [], 'retries': 0,
            'sampling': 'provider defaults; same requested model/settings in both arms',
            'actual_cost': None, 'behavioral_status': 'NOT_RUN'}
    return plan, prompts


def check_approval(plan, approval):
    # This file records an actual owner decision; software cannot authenticate that decision.
    if (approval.get('plan_sha256') != digest(plan)
        or approval.get('owner_approved') is not True
        or approval.get('max_calls') != plan['max_calls']
        or approval.get('provider_budget_enforced') is not True
        or not isinstance(approval.get('budget_usd'), (int, float))
        or not 0 < approval['budget_usd'] <= 100):
        raise ValueError('Matching owner approval and externally enforced provider budget required')


def execute(plan, prompts, out, approval, transport=invoke):
    check_approval(plan, approval)
    cases = {c['id']: c for c in plan['cases']}
    rows = []
    attempted = 0
    status = 'RUNNING'
    try:
        for case_id, rep, arm in plan['jobs']:
            history = []  # Fresh for EVERY arm, case and repetition.
            for turn, user in enumerate(cases[case_id]['turns'], 1):
                payload = request(plan['model'], prompts[arm][0], history, user, plan['max_output_tokens'])
                label = f'{case_id}-{rep}-{arm}-{turn}'
                save(out / (label + '.request.json'), payload)
                attempted += 1
                save(out / 'progress.json', {'attempted': attempted, 'current': label, 'status': 'OUTCOME_UNKNOWN'})
                start = time.monotonic()
                raw, receipt = transport(payload)
                (out / (label + '.response.json')).write_text(raw)
                response = json.loads(raw)
                answer = extract(response)
                row = {'case': case_id, 'rep': rep, 'arm': arm, 'turn': turn,
                       'request_sha256': digest(payload), 'response_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                       'provider_request_id': receipt, 'provider_response_id': response.get('id'),
                       'returned_model': response.get('model'), 'usage': response.get('usage'),
                       'seconds': time.monotonic() - start, 'words': len(answer.split()),
                       'answer': answer, 'behavioral_review': 'NOT_REVIEWED'}
                rows.append(row)
                save(out / 'rows.json', rows)
                history.extend([{'role': 'user', 'content': user}, {'role': 'assistant', 'content': answer}])
        status = 'GENERATED_NOT_REVIEWED'
    except Exception as exc:
        status = 'STOPPED_OUTCOME_REQUIRES_REVIEW'
        if isinstance(exc, urllib.error.HTTPError):
            (out / (label + '.http-error.txt')).write_bytes(exc.read())
        # No exception message: network diagnostics may contain host/account details.
        save(out / 'error.json', {'type': type(exc).__name__, 'automatic_retry': False})
        raise
    finally:
        save(out / 'summary.json', {'status': status, 'attempted_calls': attempted,
             'completed_calls': len(rows), 'expected_calls': plan['max_calls'], 'actual_cost_usd': None,
             'behavioral_winner': None, 'independent_review': 'NOT_RUN'})
        # Arm-free review cards; mapping is separate, blinding requires reviewer access control.
        cards, mapping = [], {}
        for i, job in enumerate(plan['jobs']):
            cid, rep, arm = job
            group = [r for r in rows if (r['case'], r['rep'], r['arm']) == tuple(job)]
            if len(group) != 2:
                continue
            card = f'card-{i:03d}'
            cards.append({'id': card, 'user_turns': cases[cid]['turns'],
                          'assistant_turns': [r['answer'] for r in group], 'scores': None, 'evidence': None})
            mapping[card] = {'case': cid, 'rep': rep, 'arm': arm}
        save(out / 'review-cards.json', cards)
        save(out / 'review-key.json', mapping)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--max-output-tokens', type=int, default=2048)
    parser.add_argument('--cases', nargs='+', default=PRIORITY)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--approval', type=Path)
    args = parser.parse_args()
    if git('branch', '--show-current') != BRANCH:
        parser.error('Run only on authorized working branch')
    plan, prompts = make_plan(args.model, args.repeats, max_tokens=args.max_output_tokens, ids=args.cases)
    approval = json.loads(args.approval.read_text()) if args.approval else {}
    if args.live:
        check_approval(plan, approval)
        if not os.environ.get('OPENAI_API_KEY'):
            parser.error('OPENAI_API_KEY unavailable; zero calls made')
    args.out.mkdir(parents=True, exist_ok=False)  # Never overwrite or silently resume a run.
    save(args.out / 'plan.json', plan)
    save(args.out / 'plan-hash.json', {'sha256': digest(plan)})
    for arm, (instructions, _) in prompts.items():
        (args.out / f'{arm}.instructions.txt').write_text(instructions)
    if args.live:
        execute(plan, prompts, args.out, approval)
    else:
        for c in plan['cases']:
            for arm in REFS:
                save(args.out / f'{c["id"]}-{arm}-turn1.request.json',
                     request(args.model, prompts[arm][0], [], c['turns'][0], args.max_output_tokens))
        save(args.out / 'summary.json', {'status': 'PLAN_ONLY', 'llm_calls': 0,
             'reason': 'No live flag, approved budget or verified API credential', 'behavioral_status': 'NOT_RUN'})
    print(json.dumps({'plan_sha256': digest(plan), 'planned_calls': plan['max_calls'], 'live': args.live}))


if __name__ == '__main__':
    main()
