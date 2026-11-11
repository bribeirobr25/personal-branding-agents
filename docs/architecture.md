# Architecture: prompt-first method 0.2.0

## One conversational interface

The Orchestrator is the sole user-facing agent. It checks authorization, delegates minimum context, validates results and asks the user to confirm important findings. Specialist-to-specialist requests return through it. Integration Manager is a capability-resolution role, not an additional public persona.

```text
User / optional host transcription -> Orchestrator <-> private workspace
                                      |-> Researcher
                                      |-> Positioning Strategist
                                      |-> Storyteller
                                      |-> Creative Strategist
                                      |-> Channel Editor
                                      |-> Quality Reviewer
                                      |-> Performance Analyst
```

Voice is an input interface. No voice adapter, account API, worker runtime or persistent memory service is implemented. One LLM can execute these prompts sequentially with human supervision; do not call that independent multi-agent execution.

## Separate layers

| Layer | Included now | Not implied |
| --- | --- | --- |
| Public method | Prompts, contracts, blank templates, synthetic examples and evaluation protocols | Real client sources or results |
| Private workspace | Maintained separately by each user; current goals, evidence, drafts, permissions and observations | Automatic synchronization or access from the public repo |
| Optional host | Actual tools and persistence supplied by the user's environment | Availability, authorization, coverage or safe isolation merely because a connector is named |
| Optional adapters | Capability contracts and future requirements | Working publishers, crawlers, local inference or video renderers |

## Workflow boundaries

Progressive onboarding introduces the role and optional name/goals, then invites optional evidence, scopes access, researches, returns findings for user validation and only then positions. Reuse already supplied information. A conversation-only route is valid. See [onboarding](../workflows/onboarding.md).

After a validated goal: evidence/interest -> StoryBrief -> CreativeBrief -> distinct concepts -> SELECT -> channel draft -> five final PASS results -> owner approval of the exact artifact/action -> confirmed manual publication -> measured learning. Scheduling is optional and needs its own authorization and receipt.

Knowledge stores are logically separate evidence, credibility, interest, voice and reference records; they can start as files. They do not require five databases or agents. A reference library must not become an unlicensed media archive. See [knowledge](knowledge-and-positioning.md).

The [delegation contract](agent-contracts.md) preserves task IDs, authorized sources, allowed tools and evidence references. A zero result does not prove that an account is empty. A fetched post does not prove every achievement in its text. Missing access and unsupported facts are different states.

## Progress and versioning

`framework-manifest.json` identifies method/contract versions, not an installed runtime or published tag. Earlier architecture/onboarding version headings described document iterations, not semantic releases. Private users adopt an explicit public release and resolved SHA after compatibility review; moving main is not an automatic dependency.

Useful generic improvements may be published using independently fictional scenarios. Private identities, metrics, unpublished stories, source links, transcripts and decision histories remain private. Client-specific languages, priorities and goals are configuration, not public defaults.

## Non-goals and next boundaries

No autonomous publishing, scraping, cold outreach, credential collection, production worker isolation, actual local model stack or scheduled analytics. [Optional capabilities](optional-capabilities.md) gives conditions for future implementations without expanding the first content cycle.
