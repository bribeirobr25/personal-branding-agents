# Codex CLI adapter: partial real pilot, battery blocked

Date: 2026-11-12. Decision: **HOLD**. Branch:
`feat/onboarding-strategic-discovery-20261111`. Main and frozen prompts unchanged.

## Outcome

| Execution | Planned | Forwarded to model service | Complete replies | Unknown | Not forwarded |
| --- | ---: | ---: | ---: | ---: | ---: |
| First pilot setup attempt | 12 | 0 | 0 | 0 | 12 |
| Separate pilot v2 | 12 | 10 | 9 | 1 | 2 |
| Priority battery | 108 | 0 | 0 | 0 | 108 |

The first attempt stopped at its first CLI request because this CLI trims the
instruction file's final newline. The broker rejected that local mismatch before
network dispatch (`forwarded_requests=0`). The correction accepts the CLI's boundary
trim while sending the **complete original frozen prompt bytes** to the model.
Offline qualification was repeated, and a new pilot directory was used. No remote
call was repeated from the first attempt.

In pilot v2, `R16-1-A-2` timed out after **182.223 seconds**. The broker had attempted
one dispatch, but received no response body or provider response ID. Its outcome and
token consumption remain **unknown**, not zero and not a confirmed provider failure.
No automatic retry or resumption occurred. Two R01/B turns were not dispatched.
The protocol's stop-on-timeout rule and the incomplete-pilot gate block the 108 calls.

The [raw pilot](discovery-codex-pilot-v2-2026-11-12/summary.json),
[partial context audit](discovery-codex-pilot-v2-audit-2026-11-12/audit.json),
[first attempt](discovery-codex-pilot-2026-11-12/summary.json), and
[offline 108-call plan](discovery-codex-battery-plan-2026-11-12/plan.json)
are separate artifacts. No missing answer was filled with authored text.

## Authentication and cost verification

The installed binary is **codex-cli 0.145.0**, SHA-256
`1da3f4e0e96028b8a771814293c3033dafd1971f943f6c7e79b0897fe705f590`.
It differs from the version recorded in the earlier environment's readiness report.
`codex login status` confirmed ChatGPT login; no API credential environment variables
were present. Read-only app-server account/limit methods established an included
personal plan, available allowance and zero available paid credits before each
attempt. The [postflight](discovery-codex-postflight-2026-11-12.json) confirmed those
conditions again after the timeout. No purchase, credit reset/redemption, account
change, paid API endpoint, external provider or paid fallback was used.

Full account receipts are retained privately outside Git because AGENTS.md forbids
real account identifiers and analytics in this public core. Public receipts retain
gate predicates and hashes of the private originals. They are not monetary invoices;
`actual_cost_usd` remains null. Snapshot gates cannot atomically lock a provider
account against concurrent changes. The adapter fails closed on unknown/positive
credits and stopped on the first transport failure.

## Isolation evidence and boundaries

The [addendum](../discovery-codex-cli-protocol-2026-11-12.md) documents the exact
transport, billing checks, allowlists and limitations. The CLI runs in a fresh
environment under an outer macOS policy denying repository, personal-home and other
temporary-file content. The actual policy is saved per call. Positive/negative
`cat` controls ran before each attempt. File metadata and system paths remain
readable; this is not a VM or a complete arbitrary-host filesystem policy.

Feature flags alone were insufficient: the offline capture showed extra developer
and environment messages plus `update_plan`, `request_user_input`, and `view_image`.
The loopback broker strips these and constructs the outbound request solely from
the sealed frozen bundle and same-arm current/prior turns. OAuth stays outside the
CLI process; a per-call local capability authenticates that process to the broker.
The fixed remote destination is the native ChatGPT Codex transport. This is a CLI
adapter with a wire broker, not unmodified `codex exec` or the paid Responses API.

The final [offline qualification](discovery-codex-qualification-v10-2026-11-12/summary.json)
passed real-CLI wire checks, OS read denials and rejection of a malicious tool event
**before** the CLI received it. All offline answers are explicitly transport
sentinels and are excluded from live results. Earlier qualification failures remain
recorded: invalid Seatbelt address syntax (v1/v2), unusable broad deny profiles
(v3/v4), canonical-path metadata denial (v5), and absent custom-provider OAuth
forwarding (v6/v7). v8/v9 passed; v10 additionally tests trailing-newline preservation.
Those failed attempts made zero remote inference requests.

The partial audit checked the exact outbound context of all **10 dispatched
requests**, including the timed-out request. Nine received full outputs matching
the CLI final text and their saved transcripts. Each U2 contains only its own
arm's actual U1/A1. No future user turn, alternate arm, expected answer, personal
memory or repository tool is in a model-bound request. This substantiates the
tested context boundary; the **12-call pilot as a whole remains NOT_QUALIFIED**.
Provider internals, compromised trusted controller/OS/binary, production source
access, specialist independence and source revocation enforcement are not certified.

## Observed behavior, author review only

Both arms **failed the Portuguese preference on R16 turn 1**, while correctly using
the current name **Arin**. B's first reply begins “Nice to meet you, Arin” and A's
begins “Arin, you’d like to share”. Neither first reply contains future name Sol.
B switches to Portuguese and Sol only after the actual second user turn. A's second
reply is unavailable because of the timeout. These are real adverse model outputs.

R01/A did not claim checklist adoption in turn 1; it mentioned adoption only after
U2 supplied it. R13/A and B did not invent the later internal-mentoring goal in U1;
they asked about the current goal and adapted after U2. Asking about changed goals
or suggesting an optional non-public route is not itself future-turn leakage.
These are individual observations, not population rates or an A/B winner.

[Author pilot review](discovery-codex-pilot-author-review-2026-11-12.md) contains
turn-level excerpts, hard gates and editorial notes. It is open-book self-review,
not independent or blinded. Arm-free cards and the separate key are available in
the audit directory; no reviewer was falsely claimed to be blinded. No paid judge
calls were made. The main 108-call battery has no behavioral results.

Nine received replies account for 54,040 input and 699 output tokens. The unknown
request is excluded from those totals. Raw observed words are A=347 across five
replies and B=169 across four; this unequal, incomplete sample is **not** a fair
aggregate concision comparison. Per-arm median observed latency was approximately
6.15s and 5.92s, excluding the unknown response; no latency superiority is inferred.

## Validation and continuation boundary

The final offline suite runs 35 unit tests (13 adapter, 9 existing live-API transport,
13 repository-maintenance), plus complete-checkout documentation validation and the
existing synthetic Node regression. Full outputs are recorded in
[offline checks v2](discovery-codex-offline-checks-v2-2026-11-12.json).
The Node answers remain canned transport/reference evidence, never counted as LLM calls.

To continue: reconcile the unknown R16/A/U2 dispatch if the provider can supply a
receipt; otherwise retain it as unknown and explicitly preregister a fresh pilot
attempt in a new directory. Recheck current included usage, then qualify the entire
pilot before the battery. Do not silently resume, pool attempts, increase timeouts,
replace failed responses or relax billing controls. The frozen method needs no edit
to repair transport. Independent review and owner merge approval remain absent.
No merge, release, main update or content publication occurred.
