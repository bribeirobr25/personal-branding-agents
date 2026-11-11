# A/B evaluation protocol: main versus Discovery candidate

Date: 2026-11-11. Repo: `bribeirobr25/personal-branding-agents`. Comparative artifacts live **only in candidate branch**; no write to main.

## Frozen inputs
- Baseline main: `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92` (prior verified baseline).
- Candidate before this A/B study: `b3e607c557ab26b764c7e0ef7f2e6a27405718d1` (third-battery report commit).
- Compare identical three files from each frozen ref: `agents/orchestrator.md`, `agents/researcher.md`, `workflows/onboarding.md`.
- These are design/prompt differences. No autonomous runtime or independent role isolation exists.

## Precommitted measurement
**Track 1, actual static document examination**: nine substantive rules (explicit confirmation, factual-claim boundary, source-level granularity, withdrawal, access-vs-verification, claim-scoped contradiction, bounded readiness, context-aware initiative, correction loop) plus one common no-automatic-publication rule. Evaluate each version against the **same exact textual conditions**. Mark explicit-document coverage only; this is not correctness or a response pass rate. Save criterion-by-criterion evidence.

**Track 2, same-assistant authored paired conversations**: use same synthetic user turns and sources for baseline and candidate, 4 representative scenarios (conflicting achievement, withdrawal of one source, no-CV impatient user, unavailable link and role correction). Write full example responses under each workflow's guidance and critique them separately for safety and usefulness. **No model execution claim:** the author knows both workflows; narrative examples are illustrative, not prompt-isolated agent tests. Avoid inventing connector receipts.

**Track 3, Monte Carlo applicability audit**: third battery's policy runner reads neither git ref nor workflow. Running it twice would compare the same reference-policy implementation to itself. Report NOT APPLICABLE for behavioral A/B, preserve unchanged numerical third-battery report for regression only.

## Interpretation
Do not translate rule documentation counts into actual LLM performance. Distinguish *explicit in document* from *implicitly present in existing general instructions*. Attribute improvements to added specificity, not validated runtime. Do not assert branch superiority in naturalness without matched isolated prompt conversations. Preserve raw outputs and analysis, including regressions and limitations.
