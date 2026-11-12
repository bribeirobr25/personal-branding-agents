"""Offline CLI wire inspection. No external inference endpoint is used."""
import http.server
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading


def main():
    with tempfile.TemporaryDirectory(prefix='discovery-wire-probe-') as tmp:
        root = Path(tmp)
        (root / 'instructions.txt').write_text('FROZEN_METHOD_SENTINEL')
        captured = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                captured.append({'path': self.path, 'body': raw.decode(errors='replace')})
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":{"message":"OFFLINE_CAPTURE_ONLY"}}')

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        config = f'''model_provider = "capture"
model = "gpt-6.1-sol"
model_instructions_file = "{root / 'instructions.txt'}"
project_doc_max_bytes = 0
web_search = "disabled"
personality = "none"
[model_providers.capture]
name = "Offline capture"
base_url = "http://127.0.0.1:{server.server_port}/v1"
wire_api = "responses"
requires_openai_auth = false
request_max_retries = 0
stream_max_retries = 0
supports_websockets = false
[features]
shell_tool = false
unified_exec = false
apps = false
plugins = false
remote_plugin = false
hooks = false
memories = false
multi_agent = false
skill_search = false
shell_snapshot = false
image_generation = false
browser_use = false
computer_use = false
code_mode = false
code_mode_host = false
tool_suggest = false
[skills]
bundled.enabled = false
include_instructions = false
[memories]
use_memories = false
generate_memories = false
'''
        (root / 'config.toml').write_text(config)
        env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': tmp,
               'CODEX_HOME': tmp, 'TMPDIR': tmp}
        result = subprocess.run([str(Path.home() / '.local/bin/codex'), 'exec',
                                 '--skip-git-repo-check', '--ephemeral', '--ignore-rules',
                                 '--json', '--color', 'never', '-'],
                                input='CURRENT_USER_SENTINEL', text=True, env=env,
                                cwd=tmp, capture_output=True, timeout=45)
        server.shutdown()
        print(json.dumps({'config': config, 'requests': captured,
                          'returncode': result.returncode, 'stdout': result.stdout,
                          'stderr': result.stderr}, indent=2))


if __name__ == '__main__':
    main()
