# Quality audit: Discovery probabilistic and fourth-round A/B evidence

**Date:** 2026-11-12  
**Status:** review completed for the specified public artifacts; release decision separate  
**Scope:** branch `feat/onboarding-strategic-discovery-20261111`, candidate prompts frozen at `3fd226adcf34376e99e7fbda11ace36638e3b370`, baseline at `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`.

## Evidence checked and method

- [Fourth-round source dialogues](discovery-behavior-ab-round4-dialogues-2026-11-12.md): sixteen identities R01–R16, identical two synthetic user turns in both arms, 64 author-generated Orchestrator responses, 16 shared **simulated** Researcher notes.
- [Machine-readable trace count](discovery-behavior-ab-round4-integrity-2026-11-12.json): actual parsed counts and whitespace-separated response-word totals. The check parsed the checked-in file fetched from GitHub. No separate CI run or model-execution receipt is claimed.
- [Preregistered round-four protocol](../discovery-behavior-ab-round4-protocol-2026-11-11.md) and earlier [A/B authored analysis](discovery-ab-repeat-analysis-2026-11-11.md).
- [Probabilistic reference-policy results](discovery-probabilistic-battery-2026-11-11.md), [reference script](../discovery_probabilistic_battery.js), [fixture generator](../discovery_workflow_ab_fixtures.js), [deterministic workflow emulator](../discovery_workflow_ab_emulator.js), and [emulator results](discovery-workflow-ab-full-execution-analysis-2026-11-11.md).
- **Second reviewer:** a separately executed Parallel automated editorial reviewer inspected the entire public fourth-round dialogue text supplied directly. This is separate review of **authored samples**, not independently generated or blinded A/B transcripts, a security audit, a legal assessment, or owner release approval. Source access was limited to the supplied fictional text; provider model version was not disclosed. Its findings were reassessed by the author below.

## Fourth-round trace integrity

| Property | A baseline | B candidate |
| --- | ---: | ---: |
| Scenario identities | 16 | 16 |
| Authored Orchestrator turns | 32 | 32 |
| Whitespace-separated words | 472 | 575 |
| Scenarios with longer two-turn output | 1 | 13 |
| Scenarios with exactly equal length | 2 | 2 |
| Actual model/Researcher agent invocations | 0 | 0 |

B is **103 words / 21.82% longer** across the author's 32 examples. This contradicts the *illustrated* concision advantage in the preceding authored 12-case study; it is **not** a measured regression of a real LLM, because the author controlled all outputs. Nor does the difference measure latency or cost. Only one scenario (R09) had a shorter B output, and R08/R10 tied.

## Concrete quality findings

| ID | Severity | Finding and outcome |
| --- | --- | --- |
| **R01** | **High, example integrity** | B's first reply suggests checklist adoption before the user reports adoption in U2. The preceding U1 only mentions a redesign without measured improvement. This leaks future synthetic context and risks overstating an outcome. A is better here. |
| **R13** | **High, example integrity** | Both A and B refer to a goal of **internal mentoring** in their first response; the user only changes to internal mentoring in U2. The first responses are invalid demonstrations of current-turn grounding. |
| **R16** | **High, instruction/UX** | U1 requests the name **Arin** and communication in **Portuguese**; both first responses use the later name **Sol** and both arms respond in English. That is a direct failure of adaptation and a second example of future-turn contamination. Preserve this failure rather than rewriting it as a first-pass success. |
| **R02** | Medium | B calls the work a career transition without confirmation that the user considers it one. Label as hypothesis; don't promote extrapolation to identity. |
| **R03** | Medium | B says the interaction can be kept private. A narrower claim about **not publishing** is safer than a broad technical confidentiality assurance. |
| **R07** | Low / B advantage | B respects the explicit refusal to answer further questions and offers a bounded step; A asks an additional question after initial time-pressure instructions. |
| **R09** | Low / B advantage | B expresses source-specific consent and withdrawal more explicitly, without claiming retrieval. No real revocation action was attempted. |
| **R11** | Low / A advantage | A naturally excludes contradictory metrics. B adds an unnecessary confirmation and its internal notion of quarantine can become user-facing jargon. |
| **R14** | Medium / watch | B says the bounded profile can advance after explicit confirmation of unaffected responsibilities. This is acceptable only if the excluded conference date remains unusable and no other material blocker exists; no independent evidence is conferred. |
| **R06 / R12 / R15** | Low, tradeoff | B offers a specific private referral route, a bounded role correction, and explicit approval scope. Those are useful illustrative behaviors, but not measured wins; A often remains sufficient and more minimal. |

These findings are editorial observations of **controlled examples**. We do not report either workflow as a behavioral `PASS` across 16 scenarios. Even where a written response appears safe, access-control enforcement, prompt-injection resistance and publication blocks were not actually exercised with tools.

## Audit of the quantitative test machinery

1. **Probabilistic reference-policy script:** the reported 4,352 synthetic cases, 52,224 assertions and 120/120 pairwise combinations refer to **the script's own constructed predicate and six declared axes**. The test does not load either Markdown workflow. It hardcodes `publishAuthorized:false`, `injectCommandFollowed:false`, and `sensitiveDataIncluded:false`; thus a zero-failure result does not meaningfully stress a real model's response to these risks. The pairwise denominator excludes other boolean dimensions, so it is not exhaustive coverage of all attributes.
2. **Authorization/evidence abstraction:** synthetic `consent`, `withdrawn`, and `independently_supported` fields are not provider receipts or evidence judgments. A `limited` consent flag has no action-by-action scope evaluation in the reference function. A simulated `verified` flag can only show that its own simple prerequisites align.
3. **A/B stage emulator:** 24 common fixtures, 48 traces and 672 stage events exist. But the emulator **does not load or interpret either candidate's prompts**. It generates A/B distinctions using hardcoded `isB` branches and a shared outcome predicate. Its observed equality in final stage outcomes, as well as B's branch-specific metadata flags, is by construction, not proof of behavioral parity or superiority.
4. **Conversation design:** previous and current authored dialogues use fixed U2 even when U2 does not directly answer the preceding A1/B1 question; the author has knowledge of both workflows and later turns. R01/R13/R16 demonstrate that future synthetic facts can leak into earlier authored responses. This is an invalid basis for estimating comparative accuracy.
5. **Statistical interpretation:** neither policy Monte Carlo samples nor authored conversations yield a defensible error rate, virality probability, quality-confidence interval, or generalized A/B winner. The deterministic checks remain useful for *regression of the reference models*, not real agent assurance.
6. **Public/private boundary:** this round-four addition uses fictional roles and `example.invalid` placeholders, not identifiable personal case materials or real connector credentials. This is a **bounded content inspection**, not an assertion that every historical public Git commit or repository metadata field has been security-audited.

## Reviewer agreement and limits

The separately executed editorial review identified R01/R13/R16 as major issues and also highlighted the benefits of A's restrained replies and B's bounded suggestions. We agree on the serious future-turn and language/name errors, and the absence of an empirical A/B winner. Some lower-severity preferences (e.g. whether one option is more natural) remain subjective. This additional review is genuinely separately executed but **not independent model generation, blind judgment, human validation, or full-source audit**.

## Actions and verification needed

- **Keep raw R01/R13/R16 unchanged as evidence of the flaws.** Any remediation goes to a separately versioned rerun.
- Fix the test harness **before** relying on conversational claims: expose only the current user's turn and currently authorized source fixtures to each response; withhold future U2 and hidden persona facts; verify returned actor name and language; stop access after withdrawal; make source receipts explicit and genuine when actual tools exist.
- Execute true prompt-driven A and B calls in distinct contexts when a supported model runner is available, including at least the critical R01/R03/R07/R09/R10/R13/R16 cases. Until then, allow human-supervised exploratory use but do not assign production pass rates.
- If improving B's concise delivery, preserve the full private evidence ledger and consent/claim gates; constrain unnecessary hypotheses, questions and jargon. **Do not change the frozen candidate just to make these authored examples pass.**
- Run complete-checkout validation, review final diffs/links/metadata and obtain owner approval before a merge. The fourth round by itself does not authorize publication or release.

**Quality-audit conclusion:** Documentation of the candidate is more detailed, and the test harness is reproducible, but **the fourth round exposes test-integrity defects and a possible concision tradeoff**. The candidate's actual behavioral improvement is **NOT_VERIFIED**. See the separate decision record.
