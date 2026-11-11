# Delegation and record contracts: method 0.2.0

Prompt-first specifications, not an enforced worker runtime. See [machine-readable vocabulary](../contracts/framework.json). All specialists return to Orchestrator. It authorizes minimum necessary context and presents validated results to the user.

## Stable envelope

Request fields: `task_id`, `specialist`, `objective`, `authorized_sources`, `allowed_tools`, `minimum_needed_context`, `expected_output`, `privacy_constraints`.

Response fields: `task_id`, `status`, `findings`, `evidence_refs`, `access_report`, `uncertainties`, `privacy_flags`, `next_recommended_step`.

Task: completed / partial / blocked / failed / not_started.
Source access: accessed / partial / blocked / not_supported / not_attempted.
Evidence: verified / user_reported / unverified / contradictory / outdated.
Concept: SELECT / REVISE / BLOCK. Final gate: PASS / REVISE / BLOCK.

These dimensions are not interchangeable. A source can be accessed while its claims remain unverified. State what verification covers. Legacy `user-reported` normalizes to `user_reported` with migration recorded. Reject unknown restrictions rather than silently ignoring fields.

## Domain records

Use stable IDs, version and source references. Unknown values remain null with a reason. Hashes must be calculated over the actual artifact bytes, never fabricated to fill a field.

| Record | Required content beyond ID/version | Invariant |
| --- | --- | --- |
| GoalMap | outcome, audience, constraints, desired/avoided associations, proof gaps, success signals, validation | Goal chosen by the user |
| EvidenceRecord | source/version/locator, claim, verification scope/status, coverage, observation time, rights | Existence is not impact |
| StoryBrief | problem, context, personal role, decision/experiment, result/observation, limits, lesson, evidence, disclosure | No invented outcome |
| CreativeBrief | goal/audience, central claim, proof, current voice, channel/language, constraints, intended action | Material claim change creates a new brief |
| ConceptCandidate | angle, structure, hooks, promise, payoff, proof, format, risk, difference from alternatives | Not just paraphrases |
| ConceptSelection | candidates, selected ID, decision, assessments, blockers, rationale, rejected reasons, reviewer/mode | No score compensates a hard blocker |
| DraftArtifact | concept/brief, content reference/hash, media type, channel/language, claims and assets | Text and final media may have different versions |
| ReviewReport | exact artifact/hash, five results, evidence, findings/remediation, reviewer/mode | Five PASS results are not approval |
| ApprovalRecord | artifact/hash, actor/time, exact scope, action, destination, conditions | No inferred owner consent |
| ActionReceipt | authorization, artifact, provider/job ID, idempotency key, status, confirmation and external reference, cost status | Accepted job is not publication |
| PerformanceExperiment | hypothesis, artifacts/publications, window, definitions, observations, costs, limitations, decision | Interpretation does not replace observations |
| RunCheckpoint | source versions, current stage, artifacts, decisions, approvals, unresolved actions, budget and next action | Resume from evidence, not assumed memory |
| ReuseDecision | component_id, source_ref/revision, material_scope, access_basis, use_mode, reuse_route, legal_basis_and_limitations, obligations, architectural_decision, affected_files, reviewer, evidence, status, reevaluation_trigger | Scope exclusion is not a legal prohibition |

## Editorial and action states

Content: idea -> researched -> briefed -> concept_selected -> drafted -> reviewed -> approved -> published -> measured. Authorized scheduling adds approved -> scheduled -> published. Retain the last confirmed state while recording blocked/revise decisions separately. `draft` migrates to `drafted`; do not retroactively claim old records passed a new gate.

Legacy pre-draft PASS maps to SELECT, not final PASS or approved. Selection must be reconsidered after a material brief change. All five final gates must PASS for the exact artifact before the owner can approve it. Edits after approval create an unapproved version. Unknown action results require reconciliation, not duplicate paid execution.

Onboarding remains a separate path: intake, researched, positioned. User validation of understanding is required before final positioning. No CV or account connection is required.

## Creative handoff

Request preserves story ID, goal, audience, topic constraints, evidence, available assets, channels/languages and rejected angles. Response contains distinct concepts, comparative assessment, selected recommendation, rejected reasons, claim limits, access limitations and hypotheses. Orchestrator sends only a selected concept to Channel Editor; final review remains mandatory.

## Integration Manager handoff

Preserve the existing [operational contract](integration-operational-contract.md): capability, platform, source ID/purpose, authorized scopes, available tools and cost preference; return connection state, provider, capability/retrieval state, retrieval time, count/window, evidence, limitations and fallback. Requests route through Orchestrator. Never embed credentials or expand authorization because a connector exists.

## Compatibility

See [release migration](releases/v0.2.0.md). Envelope semantics remain compatible. New records/states and canonical spelling need explicit migration; unknown values fail safely. The JSON contract is a vocabulary/required-field specification, not a claim that runtime enforcement exists.
