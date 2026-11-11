# Discovery A/B repeat after concise-dialogue refinement: comparative analysis

**Date:** 2026-11-11. **Scope:** same 12 synthetic Discovery scenarios as prior battery. **Evidence type:** same-assistant authored paired example transcripts, **not actual isolated prompt executions**. No real agents, tools, research access, blind evaluator or measured user outcomes. See [preregistered protocol](../discovery-ab-repeat-post-concision-protocol-2026-11-11.md).

## Frozen versions / outputs

- A baseline main: `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`, [full A examples](discovery-ab-repeat-main-dialogues-2026-11-11.md).
- B candidate after concise-delivery refinement: `3fd226adcf34376e99e7fbda11ace36638e3b370`, [full B examples](discovery-ab-repeat-branch-dialogues-2026-11-11.md).
- Same 12 U1 and U2 synthetic messages per arm, reproduced from first paired study, 24 authored arm dialogues and 48 user-facing authored responses (two each).
- Odd scenarios were planned for A-first drafting, even for B-first; **this was not independent randomized model execution**. User U2 stays fixed even when it does not naturally respond to an arm's preceding question.

## Measured properties of the **authored artifacts**, not of workflow model behavior

Counting whitespace-delimited words only in the 24 authored Orchestrator messages in each arm:

| Text statistic | A main | B refined branch |
|---|---:|---:|
| Orchestrator response count | 24 | 24 |
| Total authored response words | 619 | 579 |
| Mean words per response | 25.79 | 24.13 |
| Scenarios whose two B responses are shorter | n/a | 10 / 12 |
| Scenarios whose two A responses are shorter | 1 / 12 | n/a |
| Same combined length | 1 / 12 | 1 / 12 |

**Interpretation:** In these *specific written examples*, B is 40 words shorter across 24 responses (about **6.5% fewer words**), while preserving more detailed governance instructions in its source files. This does **not** establish that B will be shorter on actual execution; an author can deliberately control length.

## Scenario-by-scenario editorial assessment

| Scenario | What baseline A does well | What refined B adds / risk | Authored example assessment |
|---|---|---|---|
| S01 experienced operator | No unsupported impact | Optional credible reliability angle; additional question | B slightly more specific; A appropriately restrained |
| S02 career changer | Corrects volunteer vs paid work | Tentative bridge via structured checks without invented achievement | B more consultative, conditional on user fit |
| S03 private beginner | Respects no documents | Concrete private experiment; may oversuggest | B more actionable in this example |
| S04 famous creator, inaccessible archive | Does not claim audit | Zero-coverage language and optional topic-map alternative | B slightly more explicit, both safe |
| S05 old posts, changed voice | Does not generalize three examples | Suggests a current sample; B assumes user can supply one | B useful; A gives more open discovery |
| S06 security specialist, no publicity | Honors no-publication | Confidential proof brief, optional; potential extra exposure if mishandled | B more specific if confidential brief is wanted |
| S07 impatient user | Concrete case example, asks relevant goal question | Stops asking after user declines details | **B better aligned with stated impatience** in written example |
| S08 oversharing | Short, professional redirection | Similar but one word longer in aggregate | **No convincing winner; A is at least as good** |
| S09 revoked LinkedIn, CV permitted | Respects withdrawal | Source-specific permission status is explicit | B more auditable in text, not tested in tools |
| S10 injection in document | Rejects source command | Similar refusal, slightly shorter in B | **No convincing winner**, both demonstrate intended stance |
| S11 40% vs 400% | Blocks unsupported metric | Quarantines affected claim, moves with bounded confirmation | B clearer about safe continuation |
| S12 corrected profession | Targeted correction and no invented access | Adds optional operational hypothesis | **Tradeoff**: B initiative vs A avoids unrequested speculation |

**No statistically defensible win count** can be inferred from these editorial judgments. Text wording is intentionally influenced by each version's documented design.

## Hard-gate review of authored examples

In both written arms, no response claims real source access, publishes anything, or independently verifies user-reported metrics. Fictional approval is separated from independent verification. **This observation only describes authored texts**; neither real-source authorization, consent-revocation enforcement, LLM injection defense, nor actual agent handoffs were exercised. Therefore do **not** report either arm as 12/12 passing a behavioral safety benchmark.

## What improved versus the *previous authored study*?

B's concise-delivery changes can be illustrated without removing its additional source-permission, claim-scoped contradiction, correction and validation rules. The previous report warned about possible verbosity. In this new **author-guided** set, B examples are modestly shorter in aggregate than A and still offer relevant optional directions. This is a plausible design improvement but not a measured regression fix. A remains a useful minimalist reference for privacy-sensitive users, source-limited cases and when an insight would be forced.

## Risks / regression watchlist

- B may become more verbose than A in actual executions despite these authored examples, especially when describing internal gate mechanics.
- B may over-offer speculative ideas to users who only need factual correction; S08 and S12 suggest no need to force initiative.
- A's simpler wording may preserve naturalness better in privacy-sensitive situations; preserve discretion to give a short answer without suggestions.
- A/B examples have the same author and context, making expectancy bias and cross-arm information leakage unavoidable. Fixed U2 may not match each generated A1/B1 turn; results should not be used to estimate real conversation quality.
- The previous 4,096-state Monte Carlo script reads neither version's prompt files; its results do **not** differentiate A and B.

## Decision

**Provisional design preference:** keep B's governance rules and concise delivery; do not discard A's simplicity. **Behavioral superiority: unverified.** No further mandatory workflow changes are supported by this subjective study alone. Keep candidate unmerged and avoid claiming that the framework was independently validated.

**Next useful step:** real user-supervised trials with prompt snapshots and authentic turn-level feedback, or isolated two-arm model runs and blinded reviewers when supported. In either case store literal outputs, actual tool receipts, criteria and specific failures. The reports and protocol are stored only in the candidate branch; `main` was not modified.
