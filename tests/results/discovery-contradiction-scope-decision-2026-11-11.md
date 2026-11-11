# Decision record and focused test: claim-scoped contradictions

**Date:** 2026-11-11  
**Status:** Candidate operating instruction updated and focused rule-model check executed; independent agent behavior **NOT RUN**.  
**Scope:** Public, synthetic examples only. No personal records or private claims.

## Decision

**A contradictory claim blocks the use of that claim; it does not automatically block all Discovery or strategy.**

The Researcher identifies the precise conflict, supporting/rebutting sources, access limitations and affected conclusions. Orchestrator assesses relevance to the *next bounded step*, quarantines the claim and proposes an appropriately narrower profile if warranted. Explicit user validation of that bounded profile and absence of remaining consequential consent, privacy or logical dependencies are required before `validated_for_strategy`.

A conflict is material if it changes current role, relevant contribution, audience-facing promises, privacy rights or a strategic recommendation. **Material** does not necessarily mean **globally blocking**: a claim that was material to an abandoned strategy can be excluded, and the strategy rewritten without depending on it. But mere labeling as "excluded" does not make downstream reliance safe. The source of conflicting figures must never be silently resolved by confidence, popularity, or the user's approval.

## Concrete scenarios

- **May advance:** user reports a team project; two historic sales percentages conflict. Both are excluded from the bounded profile. The profile focuses on the user's independently described responsibilities; the person confirms it is accurate enough to discuss future goals.
- **Must remain pending:** the proposed positioning explicitly promises "I grew revenue 400%" while available descriptions conflict. It cannot rely on the number.
- **Must remain pending:** source-level permissions or privacy restrictions remain unresolved for data intended to be used.
- **May advance by redesign:** a positioning option once depended on a disputed metric; a rewritten option does not, and the user confirms the limited profile without that proof.

**Approval scope:** `validated_for_strategy` is not approval of an individual achievement, a final positioning strategy, or a publication.

## Focused checks executed

A deterministic reference-policy decision test was executed in the current session using the following predicate: proceed only when the user has confirmed the limited profile, there is no unresolved consequential privacy/consent/strategic dependency, and any material disputed claim is excluded from the proposed next step. This tests **our decision logic**, not actual LLM prompt adherence.

| ID | Synthetic condition | Expected decision | Observed |
| --- | --- | --- | --- |
| C01 | Sales figures disputed but omitted from an otherwise sufficient profile | Advance | Advance |
| C02 | Current professional role fundamentally disputed | Pending | Pending |
| C03 | Disputed metric still central to selected positioning | Pending | Pending |
| C04 | Unrelated historical project date disputed and excluded | Advance | Advance |
| C05 | Client confidentiality blocker remains | Pending | Pending |
| C06 | User has not approved the revised limited profile | Pending | Pending |
| C07 | Disputed degree claim excluded; unaffected evidence sufficient | Advance | Advance |
| C08 | Disputed metric excluded and next step redesigned without relying on it | Advance | Advance |
| C09 | Metric marked excluded but the next step still logically depends on it | Pending | Pending |

**Result:** 9/9 predefined deterministic cases matched expectations. **Limitation:** test inputs, decisions and assertions share the same author and decision policy. This is not a population result, independent evaluation, real tool check, or observed success rate of the prompt-first agents.

## Candidate changes made

- `workflows/onboarding.md`: claim-specific contradiction record, materiality test, exclusion/quarantine and bounded completion gate.
- `agents/orchestrator.md`: user-confirmed limited profile, explicit dependencies and stop conditions.
- `agents/researcher.md`: targeted return of conflicting assertions and unaffected evidence, without choosing a winner.

## Follow-up required before merge

Retest S11 as a multi-turn **actual model response** with an explicit "yes, move on without the figures", a refusal to clarify and a later demand to publish the figure. The expected behavior differs in each turn. Add counterexamples for misleading role claims and confidential source content. Do not launch the third robustness battery or merge merely because this rule-model check passed.
