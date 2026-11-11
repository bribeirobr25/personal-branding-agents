# Decision: candidate Discovery workflow and next probabilistic evaluation

**Date:** 2026-11-11
**Status:** decision / next-battery plan, **NOT executed test results**
**Repo:** `bribeirobr25/personal-branding-agents`
**Working branch:** `feat/onboarding-strategic-discovery-20261111`

## Decision
The refined Discovery onboarding workflow currently in this branch is the **candidate** for a future release, **not approved, merged, or proven behaviorally superior**. Keep the current candidate prompts frozen while evaluating. The reference `main` remains the comparison baseline and is not modified. Earlier 12-case paired dialogues were same-assistant authored examples; the third battery's 4,096 Monte Carlo states exercised a synthetic policy, not actual prompt behavior.

## Next battery: hybrid probabilistic / combinatorial design

**Objective:** probe both versions with the *same* reproducible combinations and detect wins, failures and regressions in safety *and* conversational quality.

1. **Seeded Monte Carlo with explicit distribution.** Generate fictional personas and event sequences (optional identity, experience, documents, accessible/unavailable sources, source-specific consent and withdrawal, correction, contradictory claims, disclosure level, time pressure, and preferred tone). Record seed, generator, per-feature distribution, selection process and denominators. Samples are not real population frequencies.
2. **Stratified / rare-case oversampling.** Force coverage of high-risk cases even if rare under uniform sampling: revoked consent after prior access, conflicting achievements, fabricated external validation, sensitive oversharing, prompt injection, no evidence, changing objectives, a user who refuses to publish. Report strata separately and do not derive population error rates from oversampled results.
3. **Pairwise / combinatorial coverage.** Cover each pair among consent state, source accessibility, evidence class, user style, contradiction status and goal clarity; use explicit directed safety cases for interactions pairwise misses. Record coverage matrix and uncovered combinations.
4. **Metamorphic relations.** Changing name/pronouns should not change evidence; loss of source access must remove corresponding access claims; revoking one source must not affect another; correcting a claim must preserve unrelated verified history; a change in goals must not imply publication consent.
5. **Adversarial sequences.** Test contradictory corrections, untrusted source instructions, fabricated results, impatient requests to skip validation, and attempts to reuse withdrawn permissions. Ensure no simulator secret truth leaks to the evaluated workflow.

## Fair A/B protocol
- Freeze the exact SHA of baseline `main` and current candidate **before test execution**.
- Use **identical synthetic scenarios, same order-independent facts, and identical fixtures** for both arms; alternate arm order to reduce presentation bias. Retain literal inputs/outputs per arm.
- Evaluate separately: (A) hard safety/evidence/consent gates, (B) naturalness, concision, meaningful initiative, adaptability and user value; highlight baseline wins and candidate regressions instead of assuming a winner.
- Distinguish modes per case: **reference-policy deterministic test**, **authored same-context conversation illustration**, **actual model prompt execution** (only with genuine isolated invocations), or **not executed**.
- If isolated agent/model sessions and independent grading are unavailable, use the first two modes but do **not** claim Monte Carlo or pairwise counts demonstrate actual model behavior. Never claim a blind evaluator when the same assistant authored both arms.
- Run policy-scale simulations plus a **preselected, manageable subset of stratified conversations**; no implication that thousands of rule samples equal thousands of real conversations.
- Register the protocol and frozen SHA before tests, then raw results, totals, violations, qualitative reviews, known limitations, and decisions **in this same branch**. Do not modify `main`, merge, or release automatically.

## Acceptance direction
A candidate may be proposed for review only if no critical issues emerge in exercised cases, improvements are linked to transparent evidence, regressions are documented and addressed, and repository governance/review plus owner authorization are satisfied. A zero-failure synthetic-policy run by itself is insufficient.

**Execution status at this commit:** only the decision and prospective test protocol are recorded. No next-battery samples or conversations have been executed under this decision.
