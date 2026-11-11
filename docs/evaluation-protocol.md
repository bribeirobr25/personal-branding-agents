# Evaluation: method, implementation and results are different

Separate behavioral correctness, editorial usefulness and actual outcomes. A static validation, a model preference and market evidence are not interchangeable.

## Invented cases and honest execution

[Scenario inventory](../tests/scenarios.json) specifies E01-E32 and L01-L08. All start NOT_RUN. These are newly authored generic scenarios, not private transcripts or actual client results. Existing [creative scenarios](creative-strategy-simulation-tests.md), [onboarding scenarios](onboarding-simulation-tests.md) and [integration cases](integration-research-test-cases.md) remain available; historical results are not reset or inferred.

For each run record case/fixture and protocol versions, method commit, host/model/settings, real tool availability, exact input and observed output, expected result, reviewer, mode, status, time/cost and remediation. Simulation is not enforcement. A text response recognizing a budget limit does not demonstrate a payment gateway prevents overspend. Runtime, media, local/offline and deletion cases need corresponding technical tests before capability activation.

The [walkthrough](../examples/fictional-client/creative-cycle.md) is illustrative, not an executed test or independent review. Store real client runs privately. Public logs may contain only independently synthetic material. Do not label an expected answer PASS without execution.

## Editorial comparison

Compare a baseline prompt-first cycle with the new concept stage using identical evidence, goal, audience, length and model/host when isolating the method. Preselect varied synthetic briefs for learners, transitions, strong/weak evidence and channels. An initial 12 briefs and up to three repetitions per condition is a proposed engineering sample, not statistical proof.

Pre-register the rubric and acceptable effort before seeing results. Randomize labels/order for blind human review where feasible; disclose limitations. Record fidelity, utility, clarity, voice, revisions, cost, latency and diversity. Examine worsening cases, not only favorable examples. Reserve unused briefs for a later generalization check.

Any critical fabrication/privacy/authorization failure blocks release. Better styling does not offset worse factual integrity. If usefulness gains do not justify effort, simplify rather than declare the specialist superior. Same-model judging is not independent review. Optional ablation can test which method component helps; simulation of costs cannot invent human preference or audience demand.

## Measurement

Define each metric's purpose, unit, source, numerator/denominator, time window/zone, coverage and aggregation. Missing data is not zero, summed per-post reach is not unique audience, and small nonuniform samples are not comparable by default. Median-zero comparisons use absolute differences rather than infinite multipliers.

Distinguish exposure, useful response, qualified conversation, opportunity and realized outcome according to the user's goal. Do not enrich or infer intentions from engagement. Record observation, user-reported source, traceable referral and causal inference separately. One strong post is exploratory evidence, not proof of a hook's causal effect.

Cycle: prior hypothesis -> artifact/version -> confirmed publication -> defined observation -> interpretation with limits -> keep/vary/stop/investigate. Vary one main factor where possible. Content percentages and fixed observation windows are candidate methods, not universal rules. Review charged costs, not only advertised estimates.

## Release evidence

`tools/check_documentation.py` validates files/contracts/scenario inventory only. New behavioral tests, independent review and owner approval remain separate release gates. See [candidate report](releases/v0.2.0.md). Do not suppress NOT_RUN by silently redefining it as PASS.
