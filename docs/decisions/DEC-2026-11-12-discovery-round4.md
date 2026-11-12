# DEC-2026-11-12: Discovery fourth-battery release decision

**Date:** 2026-11-12  
**Decision:** **HOLD / REWORK BEFORE MERGE**  
**Owner approval:** NOT GIVEN by this review  
**Branch:** `feat/onboarding-strategic-discovery-20261111` in the public framework repository. The `main` branch must stay unchanged.

## Frozen A/B candidates

A baseline `main`: `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`.  
B refined candidate workflow: `3fd226adcf34376e99e7fbda11ace36638e3b370`.  
The test reports written later do not change either frozen version.

**B remains a candidate, not a proven better workflow.** Its more explicit source permissions, evidence distinctions, targeted correction, claim-scoped contradictions, bounded validation, and useful initiative are valuable specification changes. A's simple and non-mechanical replies remain an important design reference.

## Gate decision

| Gate | Status | Evidence |
| --- | --- | --- |
| Frozen refs and identical fictional user inputs | PASS for test design | [Round-four protocol](../../tests/discovery-behavior-ab-round4-protocol-2026-11-11.md), [raw dialogues](../../tests/results/discovery-behavior-ab-round4-dialogues-2026-11-12.md) |
| Complete authored fourth-round artifact | PASS for trace integrity only | 16 cases, 64 authored responses; [counts](../../tests/results/discovery-behavior-ab-round4-integrity-2026-11-12.json) |
| No leakage of future user turns into earlier responses | **FAIL** | R01 B prematurely mentions adoption; R13 both arms mention the later goal |
| Correct name and language adaptation | **FAIL** | R16 both arms use later name `Sol` before correction, instead of `Arin`, and fail the Portuguese preference |
| Concision versus baseline | REGRESSION in authored samples | A 472 words, B 575 words, B +21.82%; 13/16 B scenario outputs longer, not actual model latency or performance |
| Probabilistic policy reference consistency | PASS for reference model only | 4,352 cases, 52,224 checks, 0 fails, 120/120 combinations of the six specified axis pairs |
| Deterministic surrogate trace generation | PASS for surrogate only | 24 matched fixtures, 672 stage events; no Markdown workflow prompts executed |
| Actual isolated LLM agents, genuine tool enforcement | NOT_RUN | No prompt-isolated calls, source accesses, consent revocation events or external publication |
| Secondary review | PARTIAL | Separately executed Parallel automated editorial review of provided public authored dialogues. Not independent generation, blind judging, human certification or complete-history security review |
| Owner sign-off to merge/release | NOT_GIVEN | Owner requested test and decision, not merge |

A failure in turn-level integrity cannot be waived by large counts of deterministic tests with different scope. No real behavioral pass rate or comparison winner is established.

## Quality analysis and risks

See the [full quality audit](../../tests/results/discovery-behavior-ab-round4-quality-audit-2026-11-12.md). The fourth round revealed three important integrity defects: **R01, R13 and R16**. Other concerns include unnecessary career-transition assumptions (R02), unsupported broad privacy assurances (R03), internal jargon and question repetition (R11), and possible premature stage wording (R14). B looked more useful in the authored impatient-user and source-revocation cases (R07/R09). In simpler cases A remained at least as natural.

The probabilistic runner compares a hardcoded reference function to its own invariants: publishing and injection are preset safe. The 120/120 coverage counts only the declared six-axis pairs, not all adversarial meanings. The stage emulator uses author-coded A/B branches and common decision logic, **not actual interpreted prompts**. Therefore none of these outcomes proves model compliance or generalizes to actual user behavior.

## Required actions before merge review

1. Preserve the original raw R01/R13/R16 results; do not rewrite failures as successes.
2. Repair the *evaluation process*: make U2 and hidden persona facts unavailable when generating turn 1; record genuinely accessible source receipts, or state no access.
3. Repeat high-risk cases at minimum **R01, R03, R07, R09, R10, R13, R16**, measuring actual name/language compliance, specific consent scope, factual grounding, conversation quality and concision. Separate prompt executions where available; otherwise label as authored exploratory tests, not a behavioral benchmark.
4. Reassess candidate concision and speculative suggestions against A without stripping its evidence, privacy and confirmation controls.
5. Review the complete public diff, run relevant CI, obtain qualifying independent review or a narrow owner-accepted exception, and request explicit owner approval for any PR merge.

## Resumption checkpoint

**Next permitted task:** a turn-bounded regression battery on the same working branch, maintaining frozen A/B references and original raw evidence.  
**Not authorized:** merge, release, delete branches, publish content, access client-private material or spend on external services.

**Final decision:** **HOLD**. The fourth battery is documented and audited, but the candidate is not ready for merge authorization.

## Follow-up: turn-bounded regression execution (2026-11-12)

The requested corrective test work is now recorded in [the follow-up audit](../../tests/results/discovery-turn-bounded-regression-quality-2026-11-12.md), [worker](../../tests/discovery_turn_bounded_worker.js), [runner](../../tests/discovery_turn_bounded_regression.js), and [actual final CI output](../../tests/results/discovery-turn-bounded-process-ci-v2-2026-11-12.json).

The [final Actions run](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43123529738) passed complete-checkout structure checks and **9 synthetic scenarios / 36 canned responses / 10 rejected negative controls / 0 programmed failures**. An intermediate run failed solely because the workflow expected six rather than ten controls; the corrected final run passed. The earlier in-process surrogate test is **superseded for process-isolation claims**. Its evidence remains preserved.

This improves **test transport integrity**, but the worker still contains pre-authored turn-specific answers. There were **zero LLM prompt calls**, zero genuine Researcher/tool actions, and no independent blinded behavioral result. The candidate B's authored examples remain **longer** than A's (258 versus 222 words) in this focused follow-up. Those numbers are not real model performance.

**Decision unchanged: HOLD / REWORK BEFORE MERGE.** The repaired harness cannot retroactively change R01/R13/R16 original failures or prove B superior. The next acceptance evidence must be actual turn-bounded model/tool execution or clearly labeled human-supervised trials, plus a reviewed public PR and explicit owner merge authorization.

## Follow-up: genuine model executor prepared (2026-11-12)

A [live-model protocol](../../tests/discovery-live-ab-protocol-2026-11-12.md),
[stateless API executor](../../tests/discovery_live_ab.py), exact fictional cases
and offline transport tests now exist. The [readiness report](../../tests/results/discovery-live-readiness-2026-11-12.md)
records available inference mechanisms, executed checks and the pending budget/credential
boundary. Nine offline tests passed; the saved 108-call plan made **zero model calls**.
Codex CLI authentication was found, but billing and complete context isolation were
not qualified. No comparative behavioral result or independent review is claimed.
**HOLD remains unchanged.** All original evidence and frozen prompt versions remain intact.

## Follow-up: Codex CLI adapter and incomplete real pilot (2026-11-12)

The [CLI addendum](../../tests/discovery-codex-cli-protocol-2026-11-12.md) and
[observed results](../../tests/results/discovery-codex-readiness-2026-11-12.md)
record a subscription-only adapter with a model-bound wire allowlist, per-call
OS file-read controls and included-usage/zero-credit checks. Offline real-CLI
qualification passed; feature flags or a separate cwd alone were insufficient.

A first local setup attempt dispatched zero remote requests. The separate 12-call
pilot v2 dispatched 10 requests and preserved nine actual model replies. The tenth,
R16/A/U2, timed out without a response ID/body; its provider outcome is unknown.
Two pilot turns and all 108 priority-battery calls remain unexecuted. No automatic
retry, API-key fallback, credit purchase/redemption or external paid service was used.

The partial audit found only the frozen bundle and current/same-arm prior transcript
in each dispatched payload. Both arms nevertheless failed the Portuguese preference
in R16/U1, while using Arin rather than future name Sol. These are separate behavioral
and isolation findings. Full-pilot qualification, independent review, comparative
winner and merge authorization remain absent. **HOLD remains unchanged.**

## Follow-up: fresh complete pilot v3, behavioral gate blocked (2026-11-12)

The owner authorized a fresh pilot after investigating the prior timeout.
[Investigation](../../tests/results/discovery-codex-timeout-investigation-2026-11-12.md)
found no recoverable provider ID/body; the old R16/A/U2 stays UNKNOWN. It was not
retried or mixed with new results. Executor instrumentation now preserves network
phase, early safe headers and partial-stream response IDs without changing prompts,
model, timeouts, quotas or billing/isolation controls.

The [separately preregistered pilot v3](../../tests/discovery-codex-resumption-protocol-2026-11-12.md)
completed **12/12 real model calls**, with all twelve context audits passing and no
timeout. Included-usage/zero-credit checks passed before every call and after the
run. No paid API, credit purchase/redemption or external paid service was used.
All 38 offline unit tests and the existing local checks passed.

The [complete evaluation](../../tests/results/discovery-codex-pilot-v3-evaluation-2026-11-12.md)
records repeated R16/U1 Portuguese failures in **both arms**, with correct current
names and successful language/name correction only at U2. B was shorter in all
three pilot pairs (303 versus 425 words), but this does not compensate the language
failures or establish a winner. Review is open-book author review, not independent.

The pilot is complete and transport-isolated, but **NOT_QUALIFIED behaviorally**.
The new promotion gate rejects its manifest-bound failed review before account
access or inference. The **108-call battery remains NOT_RUN**. A separate correction
round/new frozen candidate, or an explicit owner change to the promotion criteria,
is needed before further generation. No exception, merge, release or main change
was performed. **HOLD remains unchanged.**

## Follow-up: authorized R16 language diagnostics (2026-11-12)

After explicit owner authorization of the exact 32-call plan, the separate
[L01–L12 diagnostic run](../../tests/results/discovery-r16-language-evaluation-2026-11-12.md)
completed **32/32 genuine model calls** with unchanged frozen A/B prompts. All
32 context/transport audits passed, with no inference timeout or retry. Included
ChatGPT allowance, zero credit balance and unavailable paid credits were checked
before every call and after completion. All response IDs are preserved; the
provider receipts do not expose `x-request-id`, which remains null.

Both arms passed all **24 explicit reply-language checks** and all **14 specified
name occurrences**. Eight ambiguous reply-language observations are INDETERMINATE,
including the original R16/L01; future content language is reviewed separately.
No artifact was generated, so future artifact-language compliance remains pending.
No fabrication, false access claim, consent expansion, unauthorized publication
claim or premature final positioning was observed in these 32 replies; this does
not certify production tool or publication enforcement.

The older report's statement that R16/U1 was already an explicit request for the
assistant's immediate Portuguese reply is not supported by its literal wording.
It describes intended communication/content language. Historical FAIL labels and
raw outputs remain intact under their old rubric; this is a dated oracle
clarification, not deletion or silent relabeling of evidence. Explicit Portuguese,
German and English reply requests succeeded in the new diagnostic sample.

**No workflow language correction is justified by this evidence.** B was shorter
in ten of twelve scenario pairs (754 versus 898 total words), with editorial
tradeoffs and no overall winner. One repetition and open-book author review do
not establish universal compliance, causality or independent acceptance.

The 108-call battery is **NOT_RUN / NOT_AUTHORIZED** by this diagnostic approval.
Its historical promotion gate was not changed. Further execution requires
specific owner authorization and an explicit versioned treatment of the clarified
R16 oracle in that gate. No prompts, main branch, merge or release were changed.
**HOLD remains unchanged.**
