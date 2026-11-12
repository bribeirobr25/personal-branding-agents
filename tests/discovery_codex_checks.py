"""Record full offline check outputs. Never calls an inference provider."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('Do not overwrite prior evidence')
    commands = [[sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py', '-v'],
                [sys.executable, 'tools/check_documentation.py'],
                ['node', 'tests/discovery_turn_bounded_regression.js']]
    rows = []
    for command in commands:
        start = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        rows.append({'command': command, 'returncode': result.returncode,
                     'stdout': result.stdout, 'stderr': result.stderr, 'seconds': time.monotonic()-start})
    args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{'command': r['command'], 'returncode': r['returncode']} for r in rows]))
    raise SystemExit(int(any(r['returncode'] for r in rows)))


if __name__ == '__main__':
    main()
