# R16 language diagnostics: exact execution plan

Status: **AWAITING EXPLICIT OWNER AUTHORIZATION. No diagnostic model calls sent.**

This adds a concrete executor and offline qualification to the [investigation](../docs/proposals/discovery-r16-language-intent-investigation-2026-11-12.md) and [fixture readiness](results/discovery-r16-language-diagnostics-readiness-2026-11-12.md). The [v3 evaluation](results/discovery-codex-pilot-v3-evaluation-2026-11-12.md) and [round-four decision](../docs/decisions/DEC-2026-11-12-discovery-round4.md) remain historical evidence, including failures. The fixture validator and all six documents requested by the owner were read before preparing this plan.

## Frozen scope and authorization

- Branch only: `feat/onboarding-strategic-discovery-20261111`.
- A: `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`; B: `3fd226adcf34376e99e7fbda11ace36638e3b370`.
- Fixture bytes pinned to `e9dc6930afe0c616fa89ca64170679a6310199cb`.
- **32 calls = 16 turns × 2 arms × 1 repetition**, across 24 independent scenario/arm conversations. No judge-model calls. No 108-call battery.
- [Machine plan and exact first-turn payloads](results/discovery-r16-language-plan-2026-11-12/plan.json). Plan SHA-256: `1fdbcc1e8bc773daf7217b49d56f58b6121f6706ad3ce322f8b2b5f1022d7c32`.
- Owner authorization must explicitly cover this plan before `--live`; the command-line hash binds the plan but does not itself prove consent. No permission is inferred from prior pilots.

| Scenario | Turns per arm | Calls | Mandatory reply language by turn |
| --- | ---: | ---: | --- |
| L01 | 2 | 4 | INDETERMINATE; INDETERMINATE |
| L02 | 1 | 2 | Portuguese |
| L03 | 1 | 2 | Portuguese |
| L04 | 1 | 2 | English |
| L05 | 1 | 2 | German |
| L06 | 1 | 2 | German |
| L07 | 2 | 4 | English; Portuguese |
| L08 | 2 | 4 | Portuguese; Portuguese |
| L09 | 1 | 2 | INDETERMINATE |
| L10 | 1 | 2 | Portuguese |
| L11 | 1 | 2 | Portuguese |
| L12 | 2 | 4 | INDETERMINATE; Portuguese |

## Conditions and resource gate

Model `gpt-6.1-sol`, Codex CLI `0.145.0`, low reasoning, unchanged provider sampling defaults. Seed `20261112` controls conversation order only; model sampling seed is unsupported/unset. The model is therefore not promised bitwise reproducible. Frozen host/bundles, model, transport and runner hashes are in the plan; source snapshots are preserved beside it.

Network timeout remains **180 seconds**, CLI timeout **210 seconds**. No automatic retries, resume, timeout increases or output-limit increases. First transport, quota, billing or isolation uncertainty detected by the existing controls stops the entire run. The requested model is fixed in every payload; returned model identity is checked by the separate post-run auditor. A dispatched call without a confirmed answer remains UNKNOWN; subsequent calls are recorded as not forwarded. Historical UNKNOWN calls are never replayed by this runner.

The [sanitized authenticated resource receipt](results/discovery-r16-language-preapproval-resources-2026-11-12.json) confirms a personal ChatGPT included allowance, zero paid-credit balance, credits unavailable and no paid fallback. Exact account quotas and credentials stay outside Git. Availability is a point-in-time observation, not a guarantee that 32 variable-length responses will fit. Before **every** call, the existing gate requires fresh authenticated metadata, known included windows below 90% used, balance zero, no available/unlimited credits and no spend-limit flag. A failed gate sends no model request. No API-key route, credit purchase, redemption, billing-setting change or paid fallback is authorized.

## Context and OS boundary

The [new controller](discovery_r16_language_live.py) projects fixture records to literal user text. It uses the unchanged qualified [transport](discovery_codex_cli.py). Each wire request contains only the arm's frozen instructions, the current user turn and that scenario/arm's actual prior user/assistant messages. Expected fields, purpose, review rubric, future turns and other arms are excluded. Second-turn payloads cannot be finalized until the real first response exists.

Fresh CLI state is combined with the existing external Seatbelt filesystem/network restrictions, disabled tools/features, exact request allowlist, one-use local broker and upstream tool-event rejection. The repository and personal home are denied; only the disposable invocation directory is readable. The CLI does not receive the ChatGPT credential. The trusted controller owns the fixture and authentication but supplies only the sealed payload to the fixed ChatGPT endpoint. This boundary is not established merely by changing directories.

The [fresh local qualification](results/discovery-codex-language-qualification-2026-11-12/summary.json) exercised real CLI/OS controls against a local synthetic transport: allowed reads passed, forbidden reads failed, exact wire projection passed and a malicious tool response was rejected. **Zero remote inference calls**. Local sentinels test plumbing only and will never be reported as diagnostic model answers.

## Review and evidence

After an authorized run, preserve full effective requests, actual same-arm histories, raw SSE, full answers, provider response/request identifiers when supplied, usage, latency, CLI/config versions, safe receipts, exceptions, network phases and manifests. Private authentication/account receipts remain outside Git, bound by public hashes. Audit all received answers independently of the generation manifest with `audit_discovery_codex.py`; the auditor now recognizes both one- and two-turn complete dialogues.

Review each response against these separate dimensions, with quoted evidence:

1. Conversation language: **24 arm-turns have mandatory explicit requests**. Score PASS/FAIL only when an actual response exists; missing responses are UNKNOWN/NOT_SENT. The other **8 arm-turns are INDETERMINATE**, while the observed language is still recorded. Original R16/L01 is not automatically a language failure.
2. Future content language: record preference, acknowledgment or contradiction separately. Actual deliverable compliance remains PENDING unless an artifact is generated. A conversational response in a different requested chat language is not a content-language failure.
3. Current name and changes: check 14 specified-name arm-turns; reject incorrect or premature names. Omitting a vocative is not automatically a name failure. Later corrections affect only later turns.
4. Naturalness, concision, initiative and usefulness: use the existing protocol's 1–5 rubric, actual word counts and evidence. Avoid penalizing a concise clarification merely for not producing a deliverable during Discovery.
5. Unsupported facts, anticipation of future information, source-access claims, sensitive requests, permission/confirmation and premature finalization: retain each observed issue as a separate finding, including a fail when warranted.

This is a single-repetition diagnostic, not evidence of a statistically established winner or causal mechanism. Review by the executing assistant is not independent human review. Compare A/B by scenario and dimension, retaining ties and inconclusive cases. If explicit-language cases pass, the ambiguous historical R16 result does not by itself justify changing the workflow. Unequivocal failures justify only a proposed minimal, separately versioned treatment; frozen A/B must remain unchanged.

## Reproduction

Offline (use a new output path):

```sh
python3 tests/discovery_r16_language_live.py --out /private/tmp/r16-plan-review
node tests/check_discovery_r16_language_fixtures.js
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Only after explicit authorization of the hash above, use a new public run directory and private receipt directory:

```sh
python3 tests/discovery_r16_language_live.py --live \
  --approved-plan-sha256 1fdbcc1e8bc773daf7217b49d56f58b6121f6706ad3ce322f8b2b5f1022d7c32 \
  --out tests/results/discovery-r16-language-live-2026-11-12 \
  --private-out /private/tmp/discovery-r16-language-private-20261112
```

No diagnostic scenario has passed or failed yet. No comparative winner or workflow correction is supported by these offline controls. Next decision: owner authorization for the exact 32 calls, followed by a fresh resource check.

## Completed preparation checks

- [Full final offline checks](results/discovery-r16-language-offline-checks-final-2026-11-12.json): **44 unit tests PASS**, documentation checker PASS and existing synthetic regression PASS.
- [Fixture contract check](results/discovery-r16-language-fixture-check-2026-11-12.json): 12 scenarios, 16 turns, zero failures; not a model behavior test.
- [GitHub Actions 43139150332](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43139150332): **SUCCESS** on preparation commit `17620cff787e5644307a39803605c598fc93cbea`. This CI is offline.
- Remote main remained `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92` after pushing preparation to the authorized branch. No merge or release.
