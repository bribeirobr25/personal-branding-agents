# Personal Branding Agents

An evidence-led, prompt-first framework for professional reputation, useful communication and learning.

**Method version: 0.3.0.** This repository contains role instructions, workflows, templates, a machine-readable contract vocabulary. It does **not** ship autonomous workers, account connectors, a scheduler, a memory service or automatic social publishing. Use the published release tag and its resolved commit as your reference. See [migration guidance for 0.3.0](docs/releases/v0.3.0.md).

## Purpose and boundaries

Start with the person's desired outcome, not a posting quota or a job title. Support beginners, experienced professionals, people changing careers and people who should not publish publicly. Practical work, proof-building or private conversations can be better next actions than another post.

The public core contains generic methods and independently fictional examples. Real goals, stories, sources, drafts, approvals, account configuration and metrics belong in a separate private workspace. A public contribution never needs access to a client's repository.

## Start without coding or paid services

1. Read [AGENTS.md](AGENTS.md), [architecture](docs/architecture.md) and [privacy](docs/security-and-privacy.md).
2. Use the [Orchestrator](agents/orchestrator.md) and [progressive onboarding](workflows/onboarding.md). Share only authorized information. A CV, account connection and public posting are optional.
3. Copy blank [templates](templates/) into your own private workspace. Establish a [GoalMap](templates/goal-map.md), evidence and knowledge banks before claiming expertise.
4. Follow the [content cycle](workflows/content-cycle.md): story, distinct concepts, selection, channel draft, five final gates and exact human approval.
5. Publish manually only when authorized. Record an actual receipt or URL; measure only available observations.
6. Preserve a [checkpoint](templates/run-checkpoint.json) so another session can resume without pretending to remember hidden context.

See the [fictional creative walkthrough](examples/fictional-client/creative-cycle.md).

## One interface, bounded specialists

The Orchestrator remains the sole user-facing agent. Every specialist returns to it; the editorial sequence is not permission for direct, unrestricted worker delegation.

| Role | Responsibility |
| --- | --- |
| [Orchestrator](agents/orchestrator.md) | Goals, scope, delegation, continuity and approval boundaries |
| [Researcher](agents/researcher.md) | Claims, source coverage and contextual evidence |
| [Positioning Strategist](agents/positioning-strategist.md) | Outcome, audience, credibility and alternatives |
| [Storyteller](agents/storyteller.md) | True decisions, observations and useful lessons |
| [Creative Strategist](agents/creative-strategist.md) | Distinct concepts, hooks and selection rationale |
| [Channel Editor](agents/channel-editor.md) | Native channel/language treatment without changing facts |
| [Quality Reviewer](agents/quality-reviewer.md) | Five final gates; no self-granted owner approval |
| [Performance Analyst](agents/performance-analyst.md) | Observed outcomes, uncertainty and bounded experiments |

[Integration Manager](docs/integration-manager.md) resolves capabilities only when a host actually supplies them. A single assistant playing these roles is a sequential simulation, not independent multi-agent execution.

## Method map

- [Knowledge and positioning](docs/knowledge-and-positioning.md): goals, credibility, interests, voice and reference libraries.
- [Creative methods](docs/creative-methods.md) and [concept gate](docs/creative-concept-gate.md): diversity, opening, promise/payoff, rubric and accessibility.
- [Contracts](docs/agent-contracts.md), [contract vocabulary](contracts/framework.json) and [manifest](framework-manifest.json): portable records and states.
- [Evaluation](docs/evaluation-protocol.md): measuring results and deciding what to try next.
- [Reuse policy](docs/component-reuse-policy.md): lawful learning, licensed reuse and independent development.
- [Optional capabilities](docs/optional-capabilities.md): manual first, optional local/hybrid execution and total cost.

## License

MIT, see [LICENSE](LICENSE). External software, datasets, model weights and media retain their own terms. This repository's license does not grant rights over them.
