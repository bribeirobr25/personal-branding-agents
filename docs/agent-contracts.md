# Agent delegation contract — v0.1 specification

**Status:** design contract, not yet an executable agent runtime. A hosting environment may use JSON, typed objects or equivalent messages, but should preserve the semantics.

## Orchestrator → Researcher task (synthetic example)

```json
{
  "task_id": "demo-intake-001",
  "specialist": "researcher",
  "objective": "Review authorized sources and return a draft understanding",
  "authorized_sources": [
    {"source_id": "src-cv", "type": "uploaded_cv", "reference": "private://client/cv"},
    {"source_id": "src-social", "type": "public_profile", "provider": "example-provider", "reference": "https://example.org/profile"}
  ],
  "allowed_tools": ["document_reader", "public_web_fetch"],
  "minimum_needed_context": {"cv_recency": "unknown"},
  "expected_output": "draft_profile_and_access_report",
  "privacy_constraints": ["no_public_commits", "no_credentials", "private_results_only"]
}
```

## Researcher → Orchestrator response (synthetic example)

```json
{
  "task_id": "demo-intake-001",
  "status": "partial",
  "findings": [
    {
      "claim": "Career experience stated in the submitted CV",
      "verification": "user_reported",
      "evidence_refs": ["src-cv"]
    }
  ],
  "evidence_refs": ["src-cv"],
  "access_report": [
    {"source_id": "src-cv", "status": "accessed", "notes": "CV recency not confirmed"},
    {"source_id": "src-social", "status": "blocked", "notes": "Page inaccessible using available tools"}
  ],
  "uncertainties": ["Current role remains to be confirmed"],
  "privacy_flags": [],
  "next_recommended_step": "Ask user to confirm the draft profile"
}
```

## Vocabulary and behavior

**Task status:** `completed`, `partial`, `blocked`, `failed`, `not_started`.

**Per-source access:** `accessed`, `partial`, `blocked`, `not_supported`, `not_attempted`.

**Evidence status:** `verified`, `user_reported`, `unverified`, `contradictory`, `outdated`.

- Specialists respond **to the Orchestrator**, never as a second user-facing persona.
- The Orchestrator checks access coverage and facts and then returns a clear summary to the user for confirmation or correction.
- The researcher may use source adapters only when actually available and authorized. The framework provides no live social API adapters today.
- A public URL is not proof of successful access or verified identity.
- Real user data, identifiable profiles, credential values, source contents and findings belong to a **separate private workspace**. The public examples are fictional.
- A role prompt simulating a specialist does not prove a distinct agent process ran.
- No publication without exact human approval.

## Future implementation acceptance tests

1. Text and speech-to-text user inputs reach the same Orchestrator session.
2. A specialist cannot access tools or sources beyond its assigned scope.
3. Partial or blocked source access is reported, not hidden.
4. The user validates the research summary before strategic positioning.
5. The Orchestrator cannot mark a draft as published without a confirmed action.
6. Public commits, issues, and logs contain no private user data.

## Creative Strategist handoff extension (pre-draft)

Orchestrator may delegate an evidence-backed Storyteller output to Creative Strategist using the same `task_id`, scope and disclosure boundaries. Required payload: `story_id`, `audience`, `positioning_goal`, `user_topic_constraints`, `evidence_refs`, `available_assets`, `channels`, `languages`, `known_rejected_angles`. Expected response: `concepts` (default three genuinely distinct), `comparative_assessment`, `recommended_concept_id`, `rejected_reasons`, `claim_statuses`, `research_access_limitations`, `pre_draft_gate` (`PASS | REVISE | BLOCK`) and `hypotheses_to_test`. See `templates/creative-concept-brief.md`.

Channel Editor requires a selected concept with a PASS gate before drafting; Quality Reviewer still must run all five post-draft checks. On repeated wording-only revisions that fail to address owner feedback, Orchestrator routes back to Creative Strategist. These contracts are prompt-first specifications, not evidence of independent worker execution.

## Integration Manager handoff extension

For a source-access task, Researcher may request Integration Manager to resolve a capability using the same task_id and authorized_sources boundary. Request fields: capability, platform, source_id, access_purpose, authorized_scopes, available_tools, preferred_cost_tier. Response fields: connection_state, selected_provider, capability_status, retrieval_status, accessed_at, returned_count, earliest/latest_post_at, evidence_refs, limitations, fallback_options. Never put credentials in task messages. See [operational contract](integration-operational-contract.md). No actual agent runtime is implemented.
