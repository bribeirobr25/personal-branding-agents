# New pilot preregistration after the unknown dispatch

Resumption base: `506a8f274293027e4db49cbb8b9766929c79a440`, only branch
`feat/onboarding-strategic-discovery-20261111`. The owner explicitly requested a
new, separate 12-call real-model pilot and conditionally the 108-call battery.
This is authorization for included ChatGPT usage only, never paid API, credit
purchase/redemption, billing changes, merge or release.

Run: `discovery-codex-pilot-v3-2026-11-12`. R01/R13/R16, A and B, two turns,
one repetition, identical fixtures and shuffled schedule seed 20261112. Fresh
same-arm history per dialogue; no prior-run answers are reused or pooled. The
old R16/A/U2 request remains UNKNOWN and is not retried or resumed.

The frozen refs, six source documents, HOST disclosure, CLI 0.145.0,
`gpt-6.1-sol`, low reasoning, provider sampling defaults, empty model tool list,
fresh process, OS denial policy, 180-second network / 210-second CLI timeouts,
zero retries, and existing included-allowance/zero-credit gate stay unchanged.
The existing [CLI protocol](discovery-codex-cli-protocol-2026-11-12.md) and
[original live protocol](discovery-live-ab-protocol-2026-11-12.md) still apply.

Executor changes are restricted to observability and stricter promotion:
safe HTTP receipt headers are persisted as soon as received, partial SSE remains
saved, and a phase/elapsed/byte-count trace records any received response ID.
No header/payload/model/timeout change is needed for this instrumentation.
This closes an evidence gap; it cannot prove or fix an unidentified provider outage.

Before the run: read-only account/auth/resource verification, offline unit tests,
and real-CLI local-double qualification. Repeat the billing gate before each
actual call. Any unknown billing state, positive/available credits, resource
limit, timeout, refusal, tool output or incomplete response stops generation.
No unlogged fallback or automatic retry is permitted.

Promotion additionally requires an intact 12-response pilot, exact outbound-context
audit, and a review bound to that pilot manifest. All preregistered hard gates
must PASS in all 12 turns; R16's current name and Portuguese preference must PASS.
Missing/uncertain/failed gates block the main battery. Editorial quality is reviewed
for safety, naturalness, economy, initiative, usefulness and fixed-U2 mismatch;
word count alone never compensates a hard failure. Review is author/open-book unless
a separately authorized reviewer actually runs. No paid judge calls are planned.

If these gates all pass, the user's conditional authorization covers exactly the
planned 108 calls, still subject to fresh resource gates. Otherwise record HOLD and
seek an explicit next decision; do not relax the gates automatically. The runner
now requires `--pilot-review` for a main-battery invocation; transport completion
alone is insufficient. No winner may be declared from incomplete evidence.
