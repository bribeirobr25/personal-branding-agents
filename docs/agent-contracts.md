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
