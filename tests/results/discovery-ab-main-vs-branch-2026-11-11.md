# Discovery A/B: main versus candidate, observations and analysis

Date: 2026-11-11. **Study mode:** actual retrieval/read of both frozen GitHub versions and direct deterministic text-pattern inspection, plus **authored paired examples**. No isolated agent or external connector run. No changes to `main`.

## Frozen references and scope
- **A: main** `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`
- **B: candidate** `b3e607c557ab26b764c7e0ef7f2e6a27405718d1`
- Examined `agents/orchestrator.md`, `agents/researcher.md`, `workflows/onboarding.md` at both refs. Same exact text criteria; result script: [`tests/discovery_ab_static_coverage.js`](../discovery_ab_static_coverage.js), executable locally with `git show`.
- Protocol preregistered before the audit: [protocol](../discovery-ab-main-vs-branch-protocol-2026-11-11.md).

## Observed static pattern results
The matched textual patterns were: **A 2/10, B 10/10**. **These are search-pattern matches in documents, NOT feature compliance or agent pass rates.** The 8 extra matches explicitly describe additions in B. A's existing general instructions still cover aspects of consent, contradiction, validation, and evidence; missing an exact pattern does not mean A lacks those behaviors.

| Same criterion, both refs | A main | B candidate | Meaning |
|---|---|---|---|
| Explicit user confirmation wording | no exact match | match | A already requests a response before strategy; B specifies confirmation of bounded profile |
| User confirmation is not independent proof | match | match | shared guardrail |
| Source-by-source permission specification | no exact match | match | B more precise |
| Permission withdrawal prevents new source access | no exact match | match | B newly explicit |
| Access / extraction / independent verification stages | no exact match | match | B more precise |
| Contradiction quarantined per claim | no exact match | match | B newly explicit |
| Bounded profile readiness gate | no exact match | match | B newly explicit |
| Optional contextual initiative | no exact match | match | B newly explicit |
| Targeted correction/re-research | no exact match | match | B newly explicit |
| No automatic publication | match | match | shared guardrail |

## Same-input paired authored dialogues (illustrations, NOT separate model executions)
The paired responses below were written after the author read both source versions and are deliberately grounded in their different levels of specificity. Same user messages and fictional evidence are used in each pair. They **are not an A/B behavioral benchmark**: no isolated prompting, random order, blinded judge, actual researcher runtime, or tool receipts.

### P01: conflicting achievement
**Same user:** “I coordinated a team rollout. My CV says sales rose 40%; a presentation says 400%. I don't have supporting records. Can we keep going?”
**A, plausible baseline-guided response:** “These two metrics conflict, so I cannot confirm either. Can you clarify which is correct or provide evidence before we use them in positioning?”
**B, plausible candidate-guided response:** “Neither percentage is reliable enough to use. We can exclude both and keep only your account of coordinating the rollout, clearly marked as self-reported. Does that narrower description reflect your contribution sufficiently to explore directions?”
**Author critique:** B explicitly permits a bounded validation after quarantining the disputed claim. A is also safe; its instructions do not explicitly require blocking all progress. Thus B's wording is a plausible advantage in specificity, **not an observed win**.

### P02: per-source permission withdrawal
**Same user:** “You may review my résumé and my LinkedIn. Actually, don't access LinkedIn anymore; the résumé is still okay.”
**A, plausible baseline-guided response:** “Understood. I won't check LinkedIn. I can use the résumé you share, and I'll distinguish what it says from independent confirmation.”
**B, plausible candidate-guided response:** “I will not make any new LinkedIn access requests. Your résumé remains separately authorized. I'll report whether I actually read it and which claims, if any, have support beyond the résumé itself.”
**Author critique:** Both honor the user's instruction. B gives a more auditable per-source receipt; **no actual grant/revocation tool event was tested**.

### P03: impatient beginner
**Same user:** “No résumé, no public profiles. I enjoy explaining confusing board-game rules. I have five minutes. Tell me my brand.”
**A, plausible baseline-guided response:** “We can work without documents. You seem interested in explaining difficult topics. What kind of opportunities would you like to explore?”
**B, plausible candidate-guided response:** “One possible strength to investigate is simplifying complex instructions, but that's just a hypothesis from what you've told me. As a quick private test, rewrite one confusing rule and ask a friend to try it. Is your goal to find work involving this skill, or just explore?”
**Author critique:** B offers one low-cost specific action; the baseline already permits useful responses and might produce a similarly helpful one in an actual run. No naturalness or efficiency advantage is demonstrated.

### P04: inaccessible link + corrected role
**Same user:** “Here's my portfolio URL [synthetic inaccessible fixture]. I'm a graphic designer. Correction: I manage a print shop and only design occasionally.”
**A, plausible baseline-guided response:** “I couldn't access the supplied portfolio in this fictional setup. Based on your correction, you manage a print shop and do occasional design. Is that accurate?”
**B, plausible candidate-guided response:** “The portfolio content wasn't accessible in this fictional example, so I haven't assessed it. I've updated only the role claim to print-shop manager, with occasional design work. That may involve valuable operational experience, but I'd need your confirmation. Does this corrected account capture your work?”
**Author critique:** Both avoid inventing access. B additionally illustrates targeted correction and a bounded hypothesis. No actual network call or claim verification happened.

## Monte Carlo: applicability and fair comparison
The third-battery runner `tests/discovery_third_battery.js` evaluates its **own synthetic policy function**. It does not read A or B prompts. Its earlier **4,096 states / 90,112 assertions / 0 failures** therefore cannot measure a difference between the Git refs; rerunning it under a different label would produce an identical policy check. **No Monte Carlo A/B behavioral scores exist.** The prior number is preserved in the separate third-battery receipt, not misattributed to either candidate.

## Synthesis
- **Supported by direct inspection:** B documents more operationally precise rules for permission scope, correction, contradiction, and bounded Discovery; A already has general evidence and consent guardrails. This is a documentation/specification improvement.
- **Not supported:** claiming B produces higher-quality, safer, faster or more natural *actual model conversations*. The four paired dialogues are crafted examples and cannot measure that.
- **Potential regressions to test:** B's extra instructions may increase context length, latency or rote phrasing. Over-specified safety prompts may suppress initiative or lead to repetitive confirmation. Neither ref has been measured in an isolated behavior runner.
- **Decision:** retain branch unmerged. Next evidence step is frozen-ref prompt replay with actual model calls and separated fixtures/evaluation if available; absent that, conduct user-supervised practical trials with explicitly labeled observational status and not blind efficacy claims.

## Execution receipt integrity
A/B text files were read via the connected GitHub file API by exact ref. The pattern audit was evaluated over these exact retrieved texts within this conversation and returned A=2/10 and B=10/10 matching patterns. This is a textual comparison, **not** a claim that the checked-in Node script was separately executed in CI. All examples above are author-generated. No individual personal data, accounts, external URLs or production modifications were used.
