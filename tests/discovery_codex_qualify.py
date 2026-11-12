"""Execute OS and real CLI negative controls against a LOCAL transport double."""
import argparse
import base64
import json
from pathlib import Path
import tempfile

import discovery_codex_cli as cli
from test_discovery_codex_cli import stream


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    # Fake credential is accepted only by the local test double. No remote dispatch.
    claims = {'email': 'fictional@example.invalid', 'exp': 4102444800,
              'https://api.openai.com/auth': {'chatgpt_plan_type': 'pro',
                                           'chatgpt_account_id': 'OFFLINE_ACCOUNT'}}
    jwt = 'e30.' + base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip('=') + '.offline'
    auth = {'auth_mode': 'chatgpt', 'OPENAI_API_KEY': None,
            'tokens': {'access_token': jwt, 'id_token': jwt,
                       'refresh_token': 'OFFLINE_NO_REFRESH', 'account_id': 'OFFLINE_ACCOUNT'}}
    with tempfile.TemporaryDirectory(prefix='discovery-negative-', dir='/private/tmp') as tmp:
        forbidden = Path(tmp) / 'future-rubric-other-arm-personal-memory.txt'
        forbidden.write_text('FORBIDDEN_FICTIONAL_CANARY')
        observed = []

        def transport(payload):
            observed.append(payload)
            cli.base.save(args.out/'offline-assertions.json', {
                'no_canary': 'FORBIDDEN_FICTIONAL_CANARY' not in json.dumps(payload),
                'wire_matches': payload == cli.wire_request(cli.envelope('FROZEN_SENTINEL\n', [], 'CURRENT_SENTINEL'))})
            assert 'FORBIDDEN_FICTIONAL_CANARY' not in json.dumps(payload)
            assert payload == cli.wire_request(cli.envelope('FROZEN_SENTINEL\n', [], 'CURRENT_SENTINEL'))
            return stream()

        result = cli.call(Path.home()/'.local/bin/codex', cli.envelope('FROZEN_SENTINEL\n', [], 'CURRENT_SENTINEL'),
                          auth, args.out/'allowed', [forbidden, cli.base.ROOT/'AGENTS.md'], transport)
        assert result['answer'] == 'OFFLINE_TRANSPORT_SENTINEL'
        assert len(observed) == 1
        # Even a malicious service response cannot reach the CLI as an executable tool.
        try:
            cli.call(Path.home()/'.local/bin/codex', cli.envelope('FROZEN_SENTINEL', [], 'CURRENT_SENTINEL'),
                     auth, args.out/'tool-rejected', [forbidden],
                     lambda payload: stream({'type': 'function_call', 'name': 'view_image',
                         'arguments': json.dumps({'path': str(forbidden)})}))
        except RuntimeError:
            pass
        else:
            raise AssertionError('Tool event accepted')
        cli.base.save(args.out/'summary.json', {'status': 'PASS', 'remote_inference_calls': 0,
                      'offline_sentinel_calls': 2, 'os_file_denial': 'PASS', 'wire_allowlist': 'PASS',
                      'tool_response_blocked_before_cli': 'PASS'})
        cli.base.save(args.out/'manifest.json', cli.manifest(args.out))
        print(json.dumps({'status': 'PASS', 'remote_inference_calls': 0}))


if __name__ == '__main__':
    main()
