# Operational contract: Orchestrator, Integration Manager, Researcher

**Status:** prompt-first role specification, not working connector code or independently running agents.

**Method 0.2.0 routing clarification:** all capability requests and results are dispatched through the Orchestrator. References below to a Researcher request or Integration Manager return describe payload ownership, not direct specialist-to-specialist calls. The stable fields and capability/connection states are unchanged.

## Ownership
- Orchestrator alone talks to the user, selects timing, captures consent, dispatches capability tasks and validates outputs.
- Integration Manager determines available providers, account connection status, scope, cost and per-capability coverage. It returns to Orchestrator and does not interpret professional positioning or publish content.
- Researcher requests access capabilities through Orchestrator, examines only retrieved evidence, and reports provenance, uncertainty and confidentiality flags back to Orchestrator.
- Quality Reviewer checks privacy, consent, claims and evidence before any public content; publication remains a separately approved action.

## Flow
1. Orchestrator receives optional profile URL or account description, identifies research purpose and approved scope.
2. Researcher submits a scoped request to Orchestrator for `read_public_profile`, `read_authorized_account`, `read_historical_posts` or `read_post_metrics` for each source.
3. Orchestrator dispatches it to Integration Manager, which checks environment tools and provider capabilities in [matrix](integration-capability-matrix.md); it may propose Metricool, Buffer, native API, export or no-connector fallback. User authorization is required before connecting an account.
4. Integration Manager returns provider, connection state, capability state, retrieval status, checked timestamp, count and earliest/latest available dates, limits, evidence references and fallback to Orchestrator, which passes the authorized result to Researcher.
5. Researcher evaluates actual evidence. Distinguishes verified source data, user reports, hypotheses and unknowns; flags gaps and no-results ambiguities.
6. Orchestrator explains the findings and blocked access promptly, offers alternatives without repeatedly requesting known facts, and delivers a provisional useful assessment when possible.
7. No private client data, URLs, credentials or raw results are committed to this public framework.

## Capability states
`verified` | `partial` | `unavailable` | `untested` | `error`.
Connection states are separate: `not_configured` | `authorization_required` | `connected` | `limited` | `failed` | `revoked`.

## Minimum synthetic response
```json
{
  "task_id": "synthetic-001",
  "source_id": "example-x",
  "platform": "x",
  "provider": "example-publisher",
  "connection_state": "connected",
  "capability": "read_historical_posts",
  "capability_status": "unavailable",
  "retrieval_status": "success_zero_results",
  "returned_count": 0,
  "earliest_post_at": null,
  "latest_post_at": null,
  "coverage_note": "Zero retrieved does not imply zero published",
  "fallback_options": ["official_api_if_authorized", "user_export", "conversation"]
}
```

## Acceptance
Use [synthetic cases](integration-research-test-cases.md) and [onboarding tests](onboarding-simulation-tests.md). Report PASS, FAIL, NOT RUN with evidence. A document-only test cannot prove real provider connectivity, complete historical coverage or autonomous agent execution.
