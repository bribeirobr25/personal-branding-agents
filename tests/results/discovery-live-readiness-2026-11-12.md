# Discovery live A/B readiness and observed results

Date: 2026-11-12. Decision: **HOLD; real model comparison NOT_RUN**.

## What was inspected

Read repository instructions, README, architecture, contracts/vocabulary, privacy,
concept/final gates, release governance, evaluation protocol, original/main and
refined comparison protocols, round-four protocol/dialogues/quality audit, the
round-four decision and turn-bounded follow-up code/results. The original R01/R13/R16
failures and all earlier evidence are unchanged. Baseline main remains
`0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`; frozen B remains
`3fd226adcf34376e99e7fbda11ace36638e3b370`. Working branch started at
`9e84a7404055f3705940ace8e36e5a3368d570d1`.

## Capability discovery before generation

| Mechanism | Observed evidence | Qualification |
| --- | --- | --- |
| Codex CLI | `codex-cli 0.167.0-alpha.4`; `codex login status`: `Logged in using ChatGPT`; exec help supports fresh noninteractive/ephemeral runs | Real inference route potentially available, but no inference request made. Account credit/billing conditions and complete host-context isolation were not verified. Not selected as a validated benchmark adapter. |
| Direct provider APIs | No OPENAI_API / ANTHROPIC_API / GEMINI_API credential variable names found | No credentialed API inference currently demonstrated. No secret values inspected or logged. |
| Local model runtime | `command -v ollama` returned no executable | No locally verified model; this does not prove no other model installation exists. |
| Prior JavaScript workers | Authored answer map and deterministic state logic | Not LLM inference; preserved for transport/reference regression only. |
| New Responses adapter | Implemented, offline-tested against controlled transport doubles | Genuine network inference code, not live exercised; credential, model, owner-approved budget and provider cap pending. |

Official authentication documentation distinguishes ChatGPT subscription access from
API usage-based access: https://learn.chatgpt.com/docs/auth?surface=cli . That does
not establish this account's remaining included allowance or whether a new CLI run
would draw purchased credits. No paid probe, credit purchase, provider call, real
profile access or new external review was performed.

## Deliverables and executed checks

- [Preregistered protocol](../discovery-live-ab-protocol-2026-11-12.md): treatment,
  isolation boundaries, hard gates, editorial anchors, honest limitations and costs.
- [Executor](../discovery_live_ab.py) and [exact fixtures](../discovery_live_cases.json).
- [Offline tests](../test_discovery_live_ab.py), with [full output](discovery-live-offline-checks-2026-11-12.txt): **9 tests passed**.
- [Saved plan](discovery-live-plan-2026-11-12/plan.json): 9 priority cases, 3 repeats,
  108 planned calls; exact prompt snapshots, 18 first-turn request bodies, hashes and
  shuffled schedule. `MODEL_PENDING_OWNER_SELECTION` is a placeholder, not a model
  that was called. Turn-two payloads cannot yet be materialized because they require
  the actual preceding response; the code constructs them at execution time.
- [Existing checks, full stdout/stderr](discovery-live-existing-checks-2026-11-12.json):
  documentation validation, maintenance tests and original deterministic regression
  all exited 0. These are actual local executions, not a claimed new Actions run.

The new offline tests cover exact fixture preservation, current-turn-only request
construction, same-arm actual-history propagation, shared/frozen prompt loading,
reproducible schedule, rejection of missing/tampered approval, timeout with zero
retries, raw incomplete-output preservation, unexpected tool/refusal rejection and
invalid configuration bounds. Test replies explicitly contain transport sentinels;
none is counted as a model response or behavioral success.

## Analysis and remaining work

The architectural flaw of earlier authored answer tables is removed from the new
live path: it sends the actual frozen Markdown method to a model API, with no
expected-answer table. The wire payload cannot expose future case turns or the
other arm's history. Offline tests substantiate construction for the tested cases;
they do not prove real provider behavior or end-to-end safety.

The planned mode compares conversational prompt behavior without tools. It cannot
prove source revocation enforcement, specialist collaboration, production memory,
publication gating or model resistance to actual tool-return injections. Model
replies and behavior scores remain absent, not zero. No A/B winner, concision change,
latency comparison, or safety pass rate is available. Independent review NOT_RUN.

To proceed, choose an inference route whose billing is explicitly accepted. The
implemented API route additionally needs a credential supplied outside Git, a
specific model and an actually enforced provider budget; then regenerate the plan
and bind owner approval to its hash. A subscription-only CLI route would first need
billing verification and a separate adapter/isolation qualification. Do not silently
translate permission to use included subscription allowance into API spending.

No owner approval record was created. No model call was attempted. No merge/release
or main write is part of this contribution. Decision remains HOLD.
