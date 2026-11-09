# Architecture — v0.3 (conversation-led agent system)

## Core principle: one user-facing agent

**The Orchestrator (Head of Personal Branding) is the sole conversational point of contact for the user.** The user should not have to select or switch between specialist agents.

The Orchestrator receives input, decides which specialist should work, delegates with a constrained task brief, checks the specialist's result, and explains the finding and next decision in plain language. Specialist-to-specialist communication goes through the Orchestrator and shared task contracts rather than bypassing the user-facing layer.

## Logical architecture

```text
User (text / ChatGPT voice / external speech-to-text interface)
       |
       v
Interaction adapter (normalizes input; optional, host-dependent)
       |
       v
ORCHESTRATOR / HEAD OF PERSONAL BRANDING  <---->  Private client workspace
       |    (sole user-facing agent)               (history, permissions,
       |                                           source references, drafts,
       |                                           decisions, approvals)
       +--> Researcher / Evidence Auditor
       |        +--> Source-access adapters (if available and authorized)
       |                +--> Public webpages / search
       |                +--> Uploaded documents / CV
       |                +--> Official connected accounts / APIs
       |                +--> User-supplied exports
       +--> Positioning Strategist
       +--> Storyteller
       +--> Channel Editor
       +--> Quality & Privacy Reviewer
       +--> Performance Analyst
       |
       v
Human validation / explicit approval gates
       |
       v
Manual publishing in v0.1; connectors are future work
```

**Voice is an interface, not a separate brand strategist.** A host may transcribe speech (for example through a voice assistant or a third-party dictation tool such as Wispr Flow). The same Orchestrator should handle the normalized text/transcript while preserving user intent. This repository does **not** implement voice, Wispr Flow, or native ChatGPT adapters.

## Orchestrator ↔ specialist contract

See [delegation contract](agent-contracts.md). In summary:

**Task request** (Orchestrator → specialist): `task_id`, `specialist`, `objective`, `authorized_sources`, `allowed_tools`, `minimum_needed_context`, `expected_output`, and `privacy_constraints`.

**Task response** (specialist → Orchestrator): `task_id`, `status`, `findings`, `evidence_refs`, `access_report`, `uncertainties`, `privacy_flags`, and `next_recommended_step`.

Only the Orchestrator decides how to present results and when to ask the user to validate or correct findings. A specialist must never claim sources were accessed if they were not.

## Source connectors are capabilities, not assumed permissions

The Researcher is responsible for synthesis; source-access adapters handle interactions with documents, webpages or provider APIs. The Orchestrator authorizes a bounded task; the Researcher uses only capabilities actually present in the execution environment.

A URL is not proof of access. Inspect each source and return per-source statuses such as `accessed`, `partial`, `blocked`, `not_supported`, or `not_attempted`. Respect authentication, provider policies and user permission. Never collect account credentials in prompts. Do not promise complete social-media access.

## Separation of responsibilities

**Public core (this repository):** agent role prompts, contracts, workflow guidance, blank templates, fictional data, and future adapter specifications.

**Private client implementation (separate workspace):** documents, sources, real profile data, state, authorized connections, audit logs, approvals and outcomes.

**Optional runtime (future):** actual subagent execution, session management, connector API calls, voice adapters, validation and persistence. **None of these automation capabilities are shipped in the current prompt-first implementation.**

## Execution modes

- **Supported conceptually now:** a person runs one LLM sequentially through the role prompts and workflow, documenting outputs manually. This simulates delegation.
- **Future multi-agent execution:** orchestrator invokes distinct workers through an agent runtime, enforces schemas, manages failures/retries and persists state. Not yet implemented.
- **Future channels:** speech-to-text, chat, messaging, or app interfaces may connect through an adapter. No adapters currently provided.

## Standard workflow

1. **First user-facing interaction:** Orchestrator briefly introduces itself and asks for an optional preferred name and main goals. It does not request CVs or social links yet.
2. **Second user-facing interaction:** Orchestrator reflects the answer and *then* invites existing CVs, portfolio and social links, all optional. If already supplied, it skips the request.
3. Orchestrator explains source access limitations and permissions, then sends bounded authorized references to Researcher, never blanket permission to crawl unrelated material.
4. Researcher reviews sources it can actually access, records per-source coverage, and returns a draft profile **to Orchestrator**.
5. Orchestrator summarizes findings to the user, names gaps/inaccessible sources, and requests correction or confirmation.
6. Once validated, Orchestrator delegates strategy, content, review and measurement tasks as appropriate.
7. Human approval is required for the exact content before publication; only verified actions are marked completed.

## Versioning and security

- Preserve stable task IDs and explicit state transitions.
- Minimize context passed between workers, including private identifiers and data.
- Store source inventories and raw results in the private workspace only.
- A public framework upgrade never requires committing client data.
- Public examples must be independently synthetic.
- Tool availability and authorization must be checked at runtime.

## Non-goals today

No production agent runtime, no social network API connectors, no automated login, no OAuth, no voice integration, no persistent memory service, no automatic publishing, and no built-in metrics.
