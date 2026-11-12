# Integration Manager (design specification)

Status: proposed, prompt-first specification; no executable OAuth, APIs, or connectors are included.

## Responsibilities
- Orchestrator is the sole user-facing agent. It decides *when* to offer optional integrations based on the user's immediate goal.
- Integration Manager discovers available capabilities in the user's own environment, explains purpose, access scope, cost/limits and permission requirements, and tracks connection status. It must never imply that a connector available to the framework author is installed for a cloned user.
- Researcher requests capabilities (e.g., read_public_profile, import_user_export, read_authorized_account), not specific vendors. Publication and analytics are separate capabilities.

## Progressive connection points
1. Initial 5–10 minute onboarding: ask goals and existing channels; do not require credentials or integrations.
2. At evidence collection: try permitted public access and report actual results immediately. If unavailable, offer optional authorized connection, profile export, or conversation fallback.
3. After positioning and editorial strategy approval: offer publishing/scheduling (e.g., Buffer) and analytics only for selected channels.
4. Allow later connection, replacement and disconnection via Integration Manager.

## Capability record (private workspace only)
Record: provider, capability, account owner, connection_state (not_configured|available|authorization_required|connected|limited|failed|revoked), scope, permitted actions, last_verified_at, failure_reason, cost/limits, and revocation instructions. Do not store tokens or private account content in the public repo.

## Adapter contract (future runtime)
Input: capability, source URL/account reference, consent scope, request purpose. Output: status (success|partial|blocked|unsupported|error), accessed_at, coverage, source references, facts with evidence, limitations and next authorized fallback. Never report success without actual access.

## Vendor boundary
Buffer can support connected-channel publishing, scheduling and metrics, subject to permissions. Do not assume it provides complete LinkedIn/X/Instagram profile history. Other platform APIs have eligibility, access, and rate limits; public search is not equivalent to authenticated account access. Avoid prohibited scraping and authentication bypass.

## Acceptance scenarios
- A LinkedIn URL is blocked: disclose immediately; do not ask about already supplied facts; offer export or conversation.
- A user has no integrations: onboarding and provisional value still work.
- A user wants only research: do not prompt for Buffer publishing connection.
- A connected publisher lacks profile-reading scope: report capability mismatch.
- An integration fails or is revoked: preserve previously verified provenance, mark current access unavailable, offer fallback.
- No action that publishes, messages, edits profiles or authorizes account access occurs without appropriate user authorization and approval.

## Operational handoff

Use the [capability matrix](integration-capability-matrix.md) and [operational contract](integration-operational-contract.md). The Integration Manager is a **logical specialist role** invoked by Orchestrator or Researcher; it is not yet an autonomous connector service. A user can decline integrations and continue onboarding. Each read must return its actual provider, status, time and coverage; provider support alone never proves the user's account is readable.
