# Follow-up evaluation: turn-bounded Discovery regression after round-four HOLD

**Date:** 2026-11-12  
**Execution class:** *actual GitHub Actions execution of a deterministic two-process, authored-response harness*, **not** LLM inference or agent behavioral validation.  
**Candidate:** `3fd226adcf34376e99e7fbda11ace36638e3b370` (frozen refined B prompts). **Baseline:** `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92` (frozen main A).

## Original issue and correction

The fourth-round authored roleplay permitted the same author to anticipate future user turns: **R01** leaked later checklist adoption, **R13** anticipated the later internal-mentoring objective, and **R16** used the user's future name and failed their Portuguese-language preference. The original [failed examples](discovery-behavior-ab-round4-dialogues-2026-11-12.md) and [HOLD decision](../../docs/decisions/DEC-2026-11-12-discovery-round4.md) remain intact.

An initial regression script projected `slice(0,step)` but erroneously passed the full scenario object (including future data) to its local generation function. That attempt and its raw [v1 result](discovery-turn-bounded-regression-2026-11-12.json) are **superseded for isolation claims**, not deleted.

The revised suite implements:

1. A separate Node child process per response, with the parent transmitting only the currently visible user turns, source-specific synthetic permission flags and current name/language preferences.
2. Worker allowlisting of fields and required turn count, plus a **fixed per-turn fixture checksum**. The checksum uses a noncryptographic FNV-style string hash and is **only for test fixture consistency**, not adversarial security authentication. The worker's pre-authored answer map still contains future-turn answers and therefore does not establish independent semantic isolation.
3. Ten explicit negative controls, rejecting extra future fields, wrong turn count, a same-count substituted future message, tampered withdrawn permission, future name substitution, wrong-language state, and four deliberately bad output strings.
4. Directed regression on R01, R03, R07, R09, R10, R11, R13, R14 and R16, including the original three major failure cases.
5. Same synthetic current-turn input for A/B, no network/source tools, no publication actions and no real account data.

## Verified GitHub Actions receipts

- [First successful process-mode execution](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43123112175), on `ff3d1ec35d767c2079184d5d67b2dfc63c949093`: 9 cases, 36 canned replies, six negative controls, no harness failures. [Archived exact output](discovery-turn-bounded-process-ci-2026-11-12.json).
- [Intermediate failed CI run](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43123512781), on `ff33ced8a7d1e16b2c7e2177d3fd3656b0a45b8a`: expected **six** controls in the YAML despite the new runner producing **ten**. A stale test expectation caused exit code 1; this is recorded, not suppressed.
- [Final successful CI run](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43123529738), on `b493bf5cb56ea378a36985d3c328593e43964194`: both complete-checkout `python3 tools/check_documentation.py` and child-process turn regressions passed. [Full exact CI output copied to Git](discovery-turn-bounded-process-ci-v2-2026-11-12.json).

| Actual checked item | Final CI result |
| --- | ---: |
| Directed fictional scenarios | **9** |
| Scripted A + B responses | **36** (18 per arm) |
| Child-process worker invocations | **36** |
| Visible-turn projections verified | **36** |
| Programmed response checks | **36** |
| Intentionally invalid inputs/outputs rejected | **10/10** |
| Harness assertions failed | **0** |
| Authored Orchestrator words, A / B | **222 / 258** |

B's canned responses were **36 words (16.2%) longer** than A's in this follow-up, confirming there is **no observed evidence that B is inherently more concise**. This is authored output length only, not model cost or user-rated quality. The preceding round-four authored examples likewise favored A on brevity.

## Quality review and remaining risks

A separately executed automated reviewer inspected the first version's public code and correctly flagged that the worker could accept a same-length substituted input and that a canned reply table can contain knowledge of later turns. The updated fixture checks reject the targeted substitution, and the process boundary prevents transmitting the raw future user turn in the normal path. **The remaining conceptual limitation is not removed:** the worker has a pre-authored response table, so the code cannot prove that a real model would avoid exploiting unavailable context.

The checks for Portuguese phrasing use explicit strings/markers and are necessarily incomplete; they cannot replace multilingual user testing. Consent revocation is synthetic view-state validation, **not** enforcement by a live provider. Prompt injection is a synthetic document-text example, not a tool-level injection attempt. The source-safe result describes what the harness does, not observed privacy/LLM compliance.

**Do not label this batch a behavioral pass rate, blind study, or independent A/B victory.** The CI proves the reproducible structural tests and script executed; it does **not** execute the Markdown `Orchestrator` or `Researcher` prompts with a model.

## Updated decision and resumption

- **Round-four evidence hygiene:** improved; critical trace-leak examples remain preserved as FAIL in the original run.
- **Harness transport-level isolation:** passed the explicitly programmed synthetic cases and negative controls.
- **Candidate workflow behavioral superiority:** **NOT_VERIFIED**.
- **Release / merge status:** **HOLD**, unchanged.
- **Next step:** if real model runner is available, execute actual frozen A/B prompts in separate contexts, using per-turn fixtures and logging true model/tool outputs; if not, perform human-supervised practical trials with truthfully stated limitations. Reassess brevity, user usefulness, privacy and actual consent handling before owner approval.

All source code, raw results, CI evidence and this analysis are in the same candidate branch; `main` and the privately adopted framework pin were not changed.
