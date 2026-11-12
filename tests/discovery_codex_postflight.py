"""Read-only subscription receipt after a stopped/completed run; no inference."""
import argparse
from pathlib import Path

import discovery_codex_cli as cli


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--private-out', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists() or args.private_out.exists():
        parser.error('Do not overwrite receipts')
    if args.private_out.resolve().is_relative_to(cli.base.ROOT):
        parser.error('Private receipt cannot be inside Git')
    raw, _ = cli.metadata(Path.home()/'.local/bin/codex', Path.home()/'.codex/auth.json', args.private_out)
    receipt = cli.billing_gate(raw)
    cli.base.save(args.out, receipt)
    print('Read-only postflight: included allowance available, credits unavailable, balance zero.')


if __name__ == '__main__':
    main()
