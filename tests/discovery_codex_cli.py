#!/usr/bin/env python3
"""Codex CLI + bounded wire broker. macOS only; no API-key or paid fallback.

The trusted controller reads fixtures. Only the current turn envelope reaches the
CLI. A one-shot broker rebuilds the remote request from that envelope, never from
CLI-added context. Responses are buffered/validated before the CLI can see them.
"""
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import queue
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request

import discovery_live_ab as base

ENDPOINT = 'https://chatgpt.com/backend-api/codex/responses'
PILOT = ['R01', 'R13', 'R16']
MODEL = 'gpt-6.1-sol'
VERSION = 'codex-cli 0.145.0'
TIMEOUT = 180
DISABLED = ['shell_tool', 'unified_exec', 'apps', 'plugins', 'remote_plugin',
            'hooks', 'memories', 'multi_agent', 'skill_search', 'shell_snapshot',
            'image_generation', 'browser_use', 'computer_use', 'code_mode',
            'code_mode_host', 'tool_suggest', 'workspace_dependencies']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean_env(root):
    # No inherited API credentials, proxy, shell startup, app or session variables.
    return {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': str(root),
            'CODEX_HOME': str(root), 'TMPDIR': str(root), 'LANG': 'en_US.UTF-8'}


def settings(root, port=None):
    common = ('project_doc_max_bytes = 0\nweb_search = "disabled"\n'
              'personality = "none"\ncli_auth_credentials_store = "file"\n'
              'check_for_update_on_startup = false\n')
    if port is not None:
        common += (f'model = "{MODEL}"\nmodel_provider = "bounded"\n'
                   f'model_instructions_file = {json.dumps(str(root / "instructions.txt"))}\n'
                   '[model_providers.bounded]\nname = "Bounded ChatGPT CLI transport"\n'
                   f'base_url = "http://127.0.0.1:{port}/v1"\n'
                   'wire_api = "responses"\nrequires_openai_auth = false\n'
                   'env_key = "DISCOVERY_LOOPBACK_TOKEN"\n'
                   'request_max_retries = 0\nstream_max_retries = 0\n'
                   'supports_websockets = false\n')
    return (common + '[features]\n' + ''.join(f'{f} = false\n' for f in DISABLED)
            + '[skills]\nbundled.enabled = false\ninclude_instructions = false\n'
            + '[memories]\nuse_memories = false\ngenerate_memories = false\n')


def read_auth(path):
    auth = json.loads(path.read_text())
    if (auth.get('auth_mode') != 'chatgpt' or auth.get('OPENAI_API_KEY')
            or not (auth.get('tokens') or {}).get('access_token')):
        raise ValueError('ChatGPT-only authentication required')
    return auth


def put_auth(root, auth):
    dest = root / 'auth.json'
    dest.write_text(json.dumps(auth))
    dest.chmod(0o600)


def metadata(codex, auth_path, private_out):
    """Read-only account methods; no thread/start or turn/start. Raw stays private."""
    auth = read_auth(auth_path)
    with tempfile.TemporaryDirectory(prefix='discovery-account-', dir='/private/tmp') as tmp:
        root = Path(tmp)
        put_auth(root, auth)
        (root / 'config.toml').write_text(settings(root))
        proc = subprocess.Popen([str(codex), 'app-server', '--listen', 'stdio://'],
                                cwd=root, env=clean_env(root), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        messages = queue.Queue()

        def reader():
            for line in proc.stdout:
                messages.put(line)
            messages.put(None)

        threading.Thread(target=reader, daemon=True).start()

        def rpc(number, method, params):
            proc.stdin.write(json.dumps({'id': number, 'method': method, 'params': params}) + '\n')
            proc.stdin.flush()
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                line = messages.get(timeout=max(.01, deadline - time.monotonic()))
                if line is None:
                    raise RuntimeError('Account server exited')
                response = json.loads(line)
                if response.get('id') == number:
                    if 'error' in response:
                        raise RuntimeError('Account metadata request failed')
                    return response['result']
            raise TimeoutError('Account metadata timeout')

        try:
            rpc(1, 'initialize', {'clientInfo': {'name': 'discovery_billing', 'version': '1'},
                                  'capabilities': {'experimentalApi': True}})
            proc.stdin.write('{"method":"initialized"}\n')
            proc.stdin.flush()
            account = rpc(2, 'account/read', {'refreshToken': False})
            limits = rpc(3, 'account/rateLimits/read', {})
            raw = {'observed_at': time.time(), 'account': account, 'limits': limits}
            base.save(private_out, raw)
            private_out.chmod(0o600)
            # Keep refreshed credentials private and use the same identity for this call.
            auth = read_auth(root / 'auth.json')
        finally:
            proc.terminate()
            proc.wait(timeout=5)
            proc.stdin.close()
            proc.stdout.close()
    return raw, auth


def billing_gate(raw):
    """Fail closed on unknown, credit-backed, spent or non-personal accounts."""
    account = raw.get('account', {}).get('account') or {}
    if account.get('type') != 'chatgpt' or account.get('planType') not in ('plus', 'pro', 'prolite'):
        raise ValueError('Included personal ChatGPT plan not established')
    buckets = raw.get('limits', {}).get('rateLimitsByLimitId') or {}
    snapshot = buckets.get('codex') or raw.get('limits', {}).get('rateLimits') or {}
    credits = snapshot.get('credits') or {}
    if (snapshot.get('limitId') != 'codex'
            or credits.get('hasCredits') is not False or credits.get('unlimited') is not False
            or credits.get('balance') not in ('0', '0.0', '0.00')
            or snapshot.get('rateLimitReachedType') is not None
            or snapshot.get('spendControlReached') is not False):
        raise ValueError('Zero-credit included-usage gate failed')
    windows = [snapshot[k] for k in ('primary', 'secondary') if snapshot.get(k) is not None]
    if not windows or any(type(w.get('usedPercent')) is not int or not 0 <= w['usedPercent'] < 90
                          for w in windows):
        raise ValueError('Insufficient or unknown included allowance')
    if not 0 <= time.time() - raw['observed_at'] < 60:
        raise ValueError('Stale billing observation')
    # No account identity, plan name, quota analytics or reset-credit IDs in public Git.
    return {'auth': 'chatgpt', 'included_personal_plan': True,
            'available_included_allowance': True, 'credit_balance_zero': True,
            'credit_usage_available': False, 'paid_fallback': False,
            'raw_receipt_sha256': base.digest(raw), 'observed_at': raw['observed_at']}


def envelope(instructions, history, user):
    if not isinstance(user, str) or not user or len(history) not in (0, 2):
        raise ValueError('Only current U1 or same-dialogue U1/A1/U2 accepted')
    for i, item in enumerate(history):
        if set(item) != {'role', 'content'} or item['role'] != ('user', 'assistant')[i]:
            raise ValueError('Invalid bounded history')
        if not isinstance(item['content'], str) or not item['content']:
            raise ValueError('Invalid history text')
    return {'instructions': instructions, 'input': [*history, {'role': 'user', 'content': user}]}


def wire_request(sealed):
    # Construct from allowlisted fields; never forward arbitrary Codex request fields.
    return {'model': MODEL, 'instructions': sealed['instructions'], 'input': sealed['input'],
            'tools': [], 'tool_choice': 'auto', 'parallel_tool_calls': False,
            'reasoning': {'effort': 'low', 'summary': 'auto'},
            'store': False, 'stream': True, 'include': []}


def parse_stream(raw):
    events, completed = [], []
    for line in raw.decode('utf-8').splitlines():
        if not line.startswith('data:'):
            continue
        text = line[5:].strip()
        if text == '[DONE]':
            continue
        event = json.loads(text)
        events.append(event)
        kind = event.get('type', '')
        if kind in ('error', 'response.failed', 'response.incomplete'):
            raise ValueError('Incomplete or failed stream')
        item = event.get('item')
        if item and item.get('type') not in ('message', 'reasoning'):
            raise ValueError('Tool or unexpected output blocked before CLI delivery')
        if 'function_call' in kind or 'refusal' in kind:
            raise ValueError('Tool/refusal event rejected')
        if kind == 'response.completed':
            completed.append(event['response'])
    if len(completed) != 1:
        raise ValueError('Exactly one completed response required')
    response = completed[0]
    answer = base.extract(response)
    return response, answer


def sandbox_profile(root, port):
    # The outer sandbox covers the CLI itself, including startup/autoload and tools.
    # A separate cwd and Codex's own read-only sandbox would NOT prevent file reads.
    if not Path.home().resolve().is_relative_to('/Users'):
        raise ValueError('Unqualified host home layout')
    protected = ['/Users', '/private/tmp',
                 '/private/var/folders', '/Volumes', str(base.ROOT.resolve())]
    return ('(version 1)\n(allow default)\n(deny file-read* file-write* '
            + ' '.join('(subpath ' + json.dumps(p) + ')' for p in protected) + ')\n'
            '(allow file-read-metadata)\n(allow file-read* file-write* (subpath ' + json.dumps(str(root))
            + '))\n(deny network*)\n'
            f'(allow network-outbound (remote ip "localhost:{port}"))\n')


def qualify_sandbox(profile, allowed, forbidden):
    records = []
    for path, expected in [(allowed, True), *[(p, False) for p in forbidden]]:
        result = subprocess.run(['/usr/bin/sandbox-exec', '-p', profile, '/bin/cat', str(path)],
                                capture_output=True, timeout=10)
        ok = result.returncode == 0
        records.append({'kind': 'allowed' if expected else 'forbidden',
                        'read_succeeded': ok, 'returncode': result.returncode})
        if ok != expected:
            raise ValueError('OS file isolation negative control failed: '
                             + json.dumps(records) + ' stderr=' + result.stderr.decode(errors='replace'))
    return records


class Broker:
    """One bounded request, one destination, zero redirects/retries/tools."""
    def __init__(self, sealed, auth, out, transport=None):
        self.sealed, self.auth, self.out = sealed, auth, out
        self.transport = transport or self.forward
        self.attempts, self.forwarded, self.error, self.result = 0, 0, None, None
        self.lock = threading.Lock()
        self.nonce = secrets.token_urlsafe(32)

    def forward(self, payload):
        token = self.auth['tokens']['access_token']
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                   'Accept': 'text/event-stream', 'originator': 'codex_cli_rs',
                   'User-Agent': VERSION}
        account_id = self.auth['tokens'].get('account_id')
        if account_id:
            headers['ChatGPT-Account-Id'] = account_id
        request = urllib.request.Request(ENDPOINT, data=base.encoded(payload), headers=headers)
        self.forwarded += 1  # Written before network: unknown outcome counts as an attempt.
        base.save(self.out / 'dispatch.json', {'status': 'OUTCOME_UNKNOWN', 'attempts': 1})
        try:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), base.NoRedirect)
            with opener.open(request, timeout=TIMEOUT) as response:
                raw = bytearray()
                with (self.out / 'response.sse').open('wb') as artifact:
                    while True:
                        chunk = response.read1(65536)
                        if not chunk:
                            break
                        raw.extend(chunk)
                        artifact.write(chunk)
                        artifact.flush()
                receipt = {k: response.headers.get(k) for k in
                           ('x-request-id', 'openai-processing-ms', 'content-type', 'date')}
                base.save(self.out / 'receipt.json', receipt)
                return bytes(raw)
        except urllib.error.HTTPError as exc:
            (self.out / 'http-error.bin').write_bytes(exc.read())
            base.save(self.out / 'receipt.json', {'http_status': exc.code,
                       'x-request-id': exc.headers.get('x-request-id')})
            raise

    def handler(self):
        broker = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                # No model discovery or any other network passthrough.
                self.send_response(200 if self.path.startswith('/v1/models?') else 404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"models":[]}')

            def do_POST(self):
                with broker.lock:
                    broker.attempts += 1
                    if broker.attempts != 1 or self.path != '/v1/responses':
                        self.send_error(409, 'One request only')
                        return
                    try:
                        if self.headers.get('Authorization') != 'Bearer ' + broker.nonce:
                            raise ValueError('Local capability token mismatch')
                        size = int(self.headers.get('Content-Length', 0))
                        if not 0 < size < 2_000_000:
                            raise ValueError('Invalid request size')
                        raw = self.rfile.read(size)
                        (broker.out / 'cli-request.json').write_bytes(raw)
                        incoming = json.loads(raw)
                        # Bind the CLI invocation to the expected bundle and envelope.
                        # This CLI trims the instruction-file boundary whitespace.
                        # The remote payload below still uses the unmodified frozen bytes.
                        if incoming.get('instructions') != broker.sealed['instructions'].strip():
                            raise ValueError('CLI instructions drift')
                        expected = base.encoded(broker.sealed['input']).decode()
                        last = incoming.get('input', [])[-1]
                        if last.get('role') != 'user' or last.get('content') != [
                                {'type': 'input_text', 'text': expected}]:
                            raise ValueError('CLI current-envelope drift')
                        payload = wire_request(broker.sealed)
                        base.save(broker.out / 'request.json', payload)
                        raw_response = broker.transport(payload)
                        (broker.out / 'response.sse').write_bytes(raw_response)
                        broker.result = parse_stream(raw_response)
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/event-stream')
                        self.send_header('Content-Length', str(len(raw_response)))
                        self.end_headers()
                        self.wfile.write(raw_response)
                    except Exception as exc:
                        broker.error = type(exc).__name__
                        base.save(broker.out / 'failure.json', {'type': broker.error,
                                  'automatic_retry': False, 'forwarded': broker.forwarded})
                        self.send_error(400, 'Bounded adapter stopped; inspect artifacts')

            def log_message(self, *args):
                pass
        return Handler


def call(codex, sealed, auth, out, forbidden, transport=None):
    out.mkdir()
    base.save(out / 'envelope.json', sealed)
    broker = Broker(sealed, auth, out, transport)
    with tempfile.TemporaryDirectory(prefix='discovery-call-', dir='/private/tmp') as tmp:
        root = Path(tmp)
        executable = root / 'codex'
        shutil.copy2(codex, executable)
        # OAuth stays in the trusted controller, never in the CLI filesystem/env.
        (root / 'instructions.txt').write_text(sealed['instructions'])
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), broker.handler())
        server.daemon_threads = True
        server.timeout = 1
        threading.Thread(target=server.serve_forever, daemon=True).start()
        config = settings(root, server.server_port)
        (root / 'config.toml').write_text(config)
        (out / 'config.toml').write_text(config)
        profile = sandbox_profile(root, server.server_port)
        (out / 'sandbox.sb').write_text(profile)
        base.save(out / 'sandbox-checks.json', qualify_sandbox(profile, root / 'instructions.txt', forbidden))
        cmd = ['/usr/bin/sandbox-exec', '-p', profile, str(executable), 'exec',
               '--ephemeral', '--skip-git-repo-check', '--ignore-rules', '--json',
               '--color', 'never', '-']
        env = dict(clean_env(root), DISCOVERY_LOOPBACK_TOKEN=broker.nonce)
        base.save(out / 'invocation.json', {'argv': cmd, 'env': clean_env(root),
                  'private_env_names': ['DISCOVERY_LOOPBACK_TOKEN'],
                  'cwd': str(root), 'stdin_sha256': sha(base.encoded(sealed['input']))})
        start = time.monotonic()
        result = None
        try:
            result = subprocess.run(cmd, cwd=root, env=env,
                                    input=base.encoded(sealed['input']), capture_output=True,
                                    timeout=TIMEOUT + 30)
            (out / 'stdout.jsonl').write_bytes(result.stdout)
            (out / 'stderr.txt').write_bytes(result.stderr)
        except subprocess.TimeoutExpired as exc:
            (out / 'stdout.jsonl').write_bytes(exc.stdout or b'')
            (out / 'stderr.txt').write_bytes(exc.stderr or b'')
            raise
        finally:
            server.shutdown()
            server.server_close()
            base.save(out / 'transport.json', {'seconds': time.monotonic() - start,
                      'cli_requests': broker.attempts, 'forwarded_requests': broker.forwarded,
                      'returncode': result.returncode if result else None, 'error': broker.error})
        if result.returncode != 0 or broker.error or broker.result is None or broker.attempts != 1:
            raise RuntimeError('CLI transport failed; no retry')
        response, answer = broker.result
        final_messages = [e['item']['text'] for line in result.stdout.splitlines()
                          if (e := json.loads(line)).get('type') == 'item.completed'
                          and e.get('item', {}).get('type') == 'agent_message']
        if final_messages != [answer]:
            raise ValueError('CLI final answer differs from provider output')
        base.save(out / 'response.json', response)
        (out / 'answer.txt').write_text(answer)
        return {'answer': answer, 'usage': response.get('usage'),
                'returned_model': response.get('model'), 'response_id': response.get('id'),
                'words': len(answer.split()), 'seconds': time.monotonic() - start,
                'behavioral_review': 'NOT_REVIEWED'}


def make_plan(stage):
    plan, prompts = base.make_plan(MODEL, repeats=1 if stage == 'pilot' else 3,
                                   ids=PILOT if stage == 'pilot' else base.PRIORITY)
    plan.update({'stage': stage, 'mode': 'codex_cli_bounded_chatgpt', 'endpoint': ENDPOINT,
                 'adapter_sha256': sha(Path(__file__).read_bytes()), 'cli_version': VERSION,
                 'reasoning_effort': 'low', 'retries': 0, 'max_output_tokens': None,
                 'max_output_limitation': 'ChatGPT Codex transport has no validated output-token cap',
                 'cost_policy': 'included_only_zero_credit_balance_no_fallback',
                 'sampling': 'provider defaults, low reasoning, same settings both arms'})
    return plan, prompts


def manifest(out):
    return {str(p.relative_to(out)): sha(p.read_bytes()) for p in sorted(out.rglob('*'))
            if p.is_file() and p.name != 'manifest.json'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['pilot', 'battery'], default='pilot')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--private-out', type=Path)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--pilot', type=Path)
    parser.add_argument('--codex', type=Path, default=Path.home() / '.local/bin/codex')
    parser.add_argument('--auth', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    if base.git('branch', '--show-current') != base.BRANCH:
        parser.error('Only the authorized branch is allowed')
    version = subprocess.check_output([str(args.codex), '--version'], text=True).strip()
    if version != VERSION:
        parser.error('CLI version changed; requalify isolation before running')
    plan, prompts = make_plan(args.stage)
    if args.live and (not args.private_out or args.private_out.resolve().is_relative_to(base.ROOT)):
        parser.error('Private receipts must be outside the public repository')
    if args.live and args.stage == 'battery':
        if not args.pilot:
            parser.error('Completed isolated pilot required')
        pilot = json.loads((args.pilot / 'summary.json').read_text())
        if (pilot.get('status') != 'GENERATED_NOT_REVIEWED' or pilot.get('completed_calls') != 12
                or pilot.get('isolation') != 'PASS' or pilot.get('adapter_sha256') != plan['adapter_sha256']
                or pilot.get('cli_sha256') != sha(args.codex.resolve().read_bytes())
                or json.loads((args.pilot / 'manifest.json').read_text()) != manifest(args.pilot)):
            parser.error('Pilot qualification mismatch')
    args.out.mkdir(parents=True, exist_ok=False)
    base.save(args.out / 'plan.json', plan)
    shutil.copy2(Path(__file__), args.out / 'adapter-source.py')
    shutil.copy2(Path(base.__file__), args.out / 'frozen-loader-source.py')
    for arm, prompt in prompts.items():
        (args.out / f'{arm}.instructions.txt').write_text(prompt[0])
    rows, attempted, status = [], 0, 'PLAN_ONLY'
    if args.live:
        args.private_out.mkdir(parents=True, exist_ok=False, mode=0o700)
    try:
        if args.live:
            cases = {c['id']: c for c in plan['cases']}
            # Independently fictional canaries are outside every CLI readable root.
            canary = args.private_out / 'forbidden-canary.txt'
            canary.write_text('FICTIONAL_OTHER_ARM_FUTURE_RUBRIC_MEMORY_CANARY')
            forbidden = [base.ROOT / 'tests/discovery_live_cases.json',
                         base.ROOT / 'AGENTS.md', canary]
            for cid, rep, arm in plan['jobs']:
                history = []
                for turn, user in enumerate(cases[cid]['turns'], 1):
                    label = f'{cid}-{rep}-{arm}-{turn}'
                    raw, auth = metadata(args.codex, args.auth, args.private_out / f'{label}-billing.json')
                    receipt = billing_gate(raw)
                    base.save(args.out / f'{label}-billing.json', receipt)
                    attempted += 1
                    base.save(args.out / 'progress.json', {'status': 'OUTCOME_UNKNOWN',
                                                         'current': label, 'attempted': attempted})
                    row = call(args.codex, envelope(prompts[arm][0], history, user), auth,
                               args.out / label, forbidden)
                    row.update({'case': cid, 'rep': rep, 'arm': arm, 'turn': turn})
                    rows.append(row)
                    base.save(args.out / 'rows.json', rows)
                    history.extend([{'role': 'user', 'content': user},
                                    {'role': 'assistant', 'content': row['answer']}])
                    print(json.dumps({'completed': len(rows), 'expected': plan['max_calls'],
                                      'label': label}), flush=True)
            status = 'GENERATED_NOT_REVIEWED'
    except Exception as exc:
        status = 'STOPPED_OUTCOME_REQUIRES_REVIEW'
        base.save(args.out / 'failure.json', {'type': type(exc).__name__, 'message': str(exc)
                   if isinstance(exc, (ValueError, RuntimeError)) else 'See private/transport receipts',
                   'automatic_retry': False})
        raise
    finally:
        base.save(args.out / 'summary.json', {'status': status, 'attempted_calls': attempted,
                  'completed_calls': len(rows), 'expected_calls': plan['max_calls'],
                  'stage': args.stage, 'isolation': 'PASS' if status == 'GENERATED_NOT_REVIEWED' else 'NOT_QUALIFIED',
                  'adapter_sha256': plan['adapter_sha256'], 'cli_sha256': sha(args.codex.resolve().read_bytes()),
                  'actual_cost_usd': None, 'billing_evidence': 'included-only preflight; no monetary invoice',
                  'behavioral_winner': None, 'independent_review': 'NOT_RUN'})
        base.save(args.out / 'manifest.json', manifest(args.out))


if __name__ == '__main__':
    main()
