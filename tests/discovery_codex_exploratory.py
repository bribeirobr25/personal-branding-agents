"""Owner-authorized exploratory battery using the frozen Codex transport."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

import discovery_codex_cli as cli

ROOT = cli.base.ROOT
VERSIONED_PROTOCOL = ROOT / 'tests/discovery-codex-exploratory-protocol-2026-11-12.md'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--private-out', type=Path)
    parser.add_argument('--authorized-plan')
    args = parser.parse_args()
    codex = Path.home() / '.local/bin/codex'
    assert cli.base.git('branch', '--show-current') == cli.base.BRANCH
    assert subprocess.check_output([codex, '--version'], text=True).strip() == cli.VERSION
    plan, prompts = cli.make_plan('battery')
    assert plan['max_calls'] == 108
    plan.update(cli_sha256=cli.sha(codex.resolve().read_bytes()),
                exploratory_runner_sha256=cli.sha(Path(__file__).read_bytes()),
                loader_sha256=cli.sha(Path(cli.base.__file__).read_bytes()),
                protocol_sha256=cli.sha(VERSIONED_PROTOCOL.read_bytes()),
                network_timeout_seconds=cli.TIMEOUT, cli_timeout_seconds=cli.TIMEOUT+30)
    digest = cli.base.digest(plan)
    live = args.authorized_plan is not None
    if live and (args.authorized_plan != digest or not args.private_out
                 or args.private_out.resolve().is_relative_to(ROOT)):
        parser.error('Exact authorized plan and private receipt directory required')
    out = args.out
    out.mkdir(parents=True, exist_ok=False)
    cli.base.save(out/'plan.json', plan)
    cli.base.save(out/'plan-hash.json', {'sha256': digest})
    for src in [__file__, cli.__file__, cli.base.__file__]:
        shutil.copy2(src, out/Path(src).name)
    shutil.copy2(VERSIONED_PROTOCOL, out/'protocol-source.txt')
    for arm, prompt in prompts.items():
        (out/f'{arm}.instructions.txt').write_text(prompt[0])
    rows, dispatched, status = [], [], 'PLAN_ONLY'
    cases = {c['id']: c['turns'] for c in plan['cases']}
    labels = [f'{cid}-{rep}-{arm}-{turn}' for cid, rep, arm in plan['jobs'] for turn in (1, 2)]
    current = None
    try:
        if live:
            args.private_out.mkdir(mode=0o700, parents=True, exist_ok=False)
            canary = args.private_out/'canary.txt'
            canary.write_text('FICTIONAL_FORBIDDEN_CONTEXT')
            forbidden = [ROOT/'AGENTS.md', ROOT/'tests/discovery_live_cases.json', canary]
            ids = set()
            for cid, rep, arm in plan['jobs']:
                history = []
                for turn, user in enumerate(cases[cid], 1):
                    current = f'{cid}-{rep}-{arm}-{turn}'
                    raw, auth = cli.metadata(codex, Path.home()/'.codex/auth.json',
                                             args.private_out/f'{current}-billing.json')
                    cli.base.save(out/f'{current}-billing.json', cli.billing_gate(raw))
                    cli.base.save(out/'progress.json', {'current': current, 'status': 'OUTCOME_UNKNOWN'})
                    folder = out/current
                    row = cli.call(codex, cli.envelope(prompts[arm][0], history, user), auth, folder, forbidden)
                    trace = json.loads((folder/'network-trace.json').read_text())
                    rid = row['response_id']
                    if (not rid or rid in ids or trace['provider_response_id'] != rid
                            or trace['phase'] != 'STREAM_EOF' or row['returned_model'] != cli.MODEL):
                        raise ValueError('Provider response identity or model mismatch')
                    ids.add(rid)
                    row.update(case=cid, rep=rep, arm=arm, turn=turn)
                    rows.append(row)
                    cli.base.save(out/'rows.json', rows)
                    history.extend([{'role':'user','content':user}, {'role':'assistant','content':row['answer']}])
                    print(f'{len(rows)}/108 {current}', flush=True)
            status = 'GENERATED_NOT_REVIEWED'
    except (Exception, KeyboardInterrupt) as exc:
        status = 'STOPPED'
        cli.base.save(out/'failure.json', {'type': type(exc).__name__, 'current': current, 'retry': False})
        raise
    finally:
        dispatched = [label for label in labels if (out/label/'dispatch.json').exists()]
        completed = {f"{r['case']}-{r['rep']}-{r['arm']}-{r['turn']}" for r in rows}
        cli.base.save(out/'rows.json', rows)
        cli.base.save(out/'summary.json', {'status':status, 'completed_calls':len(rows),
            'forwarded_requests':len(dispatched), 'expected_calls':108,
            'outcome_unknown':[label for label in dispatched if label not in completed],
            'not_sent':[label for label in labels if label not in dispatched]})
        cli.base.save(out/'manifest.json', cli.manifest(out))
    print(digest)


if __name__ == '__main__':
    main()
