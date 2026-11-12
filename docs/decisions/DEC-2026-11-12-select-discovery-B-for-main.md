# DEC-2026-11-12: Select Discovery candidate B for integration

**Decision:** **ACCEPT B AS THE INTENDED `main` DISCOVERY WORKFLOW**. Close the comparative A/B selection phase; open a pull request from `feat/onboarding-strategic-discovery-20261111` into `main`.  
**Owner decision:** The repository owner explicitly chose B to replace the current workflow and instructed preparation of the pull request. This decision is scoped to choosing B and preparing its integration. **The pull request must not be merged automatically by the assistant.**  
**Recorded:** 2026-11-12.  
**Target base:** `main` SHA `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`.  
**Frozen approved behavior:** candidate B instructions SHA `3fd226adcf34376e99e7fbda11ace36638e3b370` (later candidate commits contain tests and evidence). 

## Rationale and trade-offs

B is the preferred Discovery experience for the product; this is a practical **owner product decision**, not a claim of statistical superiority or independent certification.

- [Real, isolated 108-call exploratory A/B battery](../../tests/results/discovery-codex-exploratory-evaluation-2026-11-12.md): 54 calls per arm, 27 two-turn comparisons; author preferred **B in 16**, A in **4**, with **7 ties**. No definitive failures within the exercised conversational gates; **three attribution-precision judgments uncertain**. Review was open-book and not independent.
- B produced **3,112 words** versus A's **4,198** (25.9% fewer), and **4,298 output tokens** versus **5,680**. Its longer instruction bundle consumed **413,003 input tokens** versus **256,132** for A (61.2% more): a known optimization opportunity, not a blocker to selecting B.
- B handled fictional permission withdrawal and correction of goals more directly, particularly R09 and R13. A sometimes provided more concrete contextual questions. Preserve these observations in future improvements without delaying this decision.
- [Separate 32-call language diagnostic](../../tests/results/discovery-r16-language-evaluation-2026-11-12.md) completed 24/24 explicit reply-language checks and 14/14 current-name checks. Original R16 was ambiguous between conversation language and future content language; historical results remain unmodified and should not be recast as a definite model-language violation.

## Integration scope

The *runtime-facing prompt changes* are in:
- `agents/orchestrator.md`;
- `agents/researcher.md`;
- `workflows/onboarding.md`.

The requested PR is **from the existing current candidate branch**, so it also includes the accumulated research, test harnesses, scripts, synthetic fixtures, raw model outputs and audit artifacts. Do not represent that entire diff as three files or suggest that opening the PR automatically promotes only those prompts. Review its full file inventory and privacy/security implications before the actual merge.

The prompt-first framework remains a **specification**, not an autonomous tool-enabled runtime. Source-access enforcement, posting approvals and live specialist independence were not exercised as actual production actions. Do not imply otherwise.

## Historical decisions and readiness boundary

- Keep [the fourth-battery HOLD decision](DEC-2026-11-12-discovery-round4.md) and every original raw failure unchanged. This new record supersedes the old **choice-of-variant HOLD**, **not** the historical evidence or any separate release gate.
- **Owner has approved B as the version to integrate. Owner has requested this PR.** Final merge execution remains a separate action pending PR visibility and normal integration checks.
- Repository [release policy](../release-and-client-upgrade-policy.md) continues to require a full-diff/privacy review and independent review or an expressly scoped owner exception. **No generic conversational preference to stop testing is misreported as a formal review waiver.** Record actual completed checks and any exceptions before merge.
- Do not create tags/releases, automatically update private client pins, change credentials/permissions, remove historical test evidence or delete branches as part of this decision.

## Follow-up after PR creation

1. Verify PR **base=`main`**, **head=`feat/onboarding-strategic-discovery-20261111`** and that `main` has not moved.
2. Confirm required CI and review status on the PR, and disclose the substantial historical test-artifact scope.
3. Request explicit, final merge action when the PR is judged ready. Do not initiate further A/B behavioral batteries by default.
