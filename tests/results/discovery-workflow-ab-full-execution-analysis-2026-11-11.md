# Discovery A/B: executed sequential surrogate workflows, 24 paired scenarios

**Date:** 2026-11-11. **Status:** emulated workflow-stage execution **completed**, actual LLM prompt/agent execution **not performed**. All six raw event files are committed to the candidate branch. No changes to main or either frozen prompt.

## Fixed A/B configuration
A baseline `main` = `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`. B refined candidate = `3fd226adcf34376e99e7fbda11ace36638e3b370`. Generation seed `20261111`. The same 24 synthetic fixture IDs and user utterances are replayed in each arm; the evaluator knows both arms. Execution is a deterministic **surrogate implementing authored interpretations** of the frozen rules; it **does not load, interpret or execute the markdown agent prompts at runtime**. It cannot measure how real LLM calls would respond.

## Artifacts and reproduction
- Fixture generator: [`tests/discovery_workflow_ab_fixtures.js`](../discovery_workflow_ab_fixtures.js)
- Stage-based emulator: [`tests/discovery_workflow_ab_emulator.js`](../discovery_workflow_ab_emulator.js)
- Raw traces: [part 01](discovery-ab-full-events-part-01-2026-11-11.json), [02](discovery-ab-full-events-part-02-2026-11-11.json), [03](discovery-ab-full-events-part-03-2026-11-11.json), [04](discovery-ab-full-events-part-04-2026-11-11.json), [05](discovery-ab-full-events-part-05-2026-11-11.json), [06](discovery-ab-full-events-part-06-2026-11-11.json).
- In a local Node.js clone: `node tests/discovery_workflow_ab_fixtures.js 20261111 24 > /tmp/discovery-fixtures.json` followed by `node tests/discovery_workflow_ab_emulator.js < /tmp/discovery-fixtures.json > /tmp/discovery-traces.json`.
- The scripts were retrieved from the committed branch and evaluated in the JS tool environment; the resultant full traces were committed in six files and subsequently read for this analysis. No LLM inference, external connectors, live sources or independent reviewer was invoked.

## Results (deterministic surrogate, NOT behavioral compliance rates)

| Measured trace property | A main | B candidate |
|---|---:|---:|
| Scenario executions | 24 | 24 |
| Stage events | 336 | 336 |
| Validated-for-strategy decisions | 7 | 7 |
| Pending decisions | 11 | 11 |
| Needs-correction decisions | 6 | 6 |
| Staged unauthorized access / publication events | 0 | 0 |
| Explicit per-source permission handling flag | 0 | 24 |
| Explicit targeted-correction handling flag | 0 | 22 |
| Explicit claim quarantine flag | 0 | 2 |
| Orchestrator-word total in generated surrogate outputs | 2,598 | 2,608 |

**Important:** flags in B are values supplied by the emulator's author-defined branch policy. A's zero does **not** prove that the baseline LLM would fail the rule, and B's numbers do **not** prove genuine model compliance. All final Discovery decisions are identical because both branches use the same explicitly coded decision predicates. The model itself forbids source access/publication; zero violations follows from the constructed policy and is **not** real-world safety evidence.

## Interpretation, including where main performs at least as well
- **No measured improvement in final gate outcomes:** Both versions produce exactly 7 validated, 11 pending and 6 correction-needed states under the surrogate.
- **Governance detail:** B's prompts explicitly describe source-specific permissions, affected-claim correction and quarantine; the surrogate represents these explicitly. This confirms *design intent and trace schema*, not behavioral superiority.
- **Brevity:** A's generated Orchestrator text is **10 whitespace-separated words shorter overall** across 24 scenarios, about 0.4% shorter than B. This tiny difference is an artifact of hand-written templates and should not inform real quality conclusions.
- **No valid winner for naturalness, initiative, or usefulness:** Template-generated language was not judged as actual conversational output and cannot support a creativity score.
- **Stress-case caveats:** The generated cases include synthetic consent withdrawal, unsupported evidence, contradictions and prompt-injection flags, but these are booleans, not actual tool-event transcripts or hidden adversarial prompts. The user messages are fixed rather than adaptive responses to previous agent questions. A staged Researcher receipt does not demonstrate a genuine delegated task.

## Reproduction and integrity checks
- 24 unique scenario IDs and two arm IDs; all 48 traces contain the same 14 ordered stage names.
- **672 total events**; internal emulator validator returned zero trace-shape / hard-flag errors, with paired=true.
- Fixture generator reproduced exactly with seed `20261111`; changing to `20261112` changed the fixture set.
- 14 stages are a *Discovery-slice* convention, not the complete professional branding workflow beyond the Discovery exit gate.
- Do not compare the separate 4,352 reference-policy cases as if they had executed these agent prompts. They are distinct evidence classes.

## Next decision and completion boundary
**Completed:** reproducible scenario-to-workflow-stage integration; deterministic paired stage traces; retention of all event records; comparative analysis. **Not completed:** live or truly prompt-driven Orchestrator/Researcher LLM role executions, independent validation, actual connectors or user testing. For prompt-based behavioral inference, use an actual model execution facility with frozen agent instructions, controlled source fixtures and separate A/B contexts. Without that, staged same-model roleplay remains an illustration, not quantified performance evidence.

**Decision:** candidate remains proposed and unmerged; no change to `main`. No evidence justifies claiming B categorically superior or marking release gates passed.
