# Architecture — v0.1

## Separation of responsibilities

**Public core (this repository):** reusable prompts, stage contracts, quality gates, blank templates, generic examples and documentation.

**Private client workspace (outside this repository):** factual biography, goals, source documents, project links, audience constraints, tone choices, drafts, approval decisions, outreach details and results.

**Optional future runtime:** integrations for research, storage, scheduling, analytics and approvals. These are **not implemented** in v0.1.

## Contract between layers
Inputs should be selected, minimum-necessary fields drawn from a private workspace. Outputs should be stored back in that private workspace. Never log sensitive inputs or outputs into public build artifacts or issues.

## Execution model: prompt-first
A single LLM can run the seven specialist roles *sequentially*. Multi-model delegation is optional; the specification does not assert that parallel AI processes exist. The owner remains accountable for facts, consent and publishing.

## Stages and required deliverables
| Stage | Role | Output | Gate |
| --- | --- | --- | --- |
| Intake | Orchestrator | Profile + scope + consent boundaries | Required fields or explicit gaps |
| Research | Researcher | Evidence inventory | Sourced / user-reported / unverified tags |
| Positioning | Strategist | Positioning narrative and audiences | Owner review |
| Story mining | Storyteller | Cases and narrative angles | Evidence/permissions check |
| Content | Channel Editor | Channel-specific drafts | Editorial checks |
| Review | Quality Reviewer | Pass/fail report with fixes | All critical findings resolved |
| Approval | Human owner | Approval for exact revision | Explicit decision |
| Publication | Human / authorized integration | Canonical link and timestamp | Proven action completion |
| Learning | Analyst | Observations, hypotheses and next test | Source timestamps provided |

## Versioning principles
- Keep templates backward compatible when reasonable.
- Version any future machine-readable schema; record migration instructions.
- A public framework upgrade must never require committing client data.
- Don't silently sync data across repositories.
- Public examples must not be derived from identifiable private cases.

## Non-goals of v0.1
Not a production-grade agent platform, no automatic publishing, no OAuth management, no platform APIs, no persistent memory service, no built-in engagement metrics.
