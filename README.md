# Personal Branding Agents

**A reusable, prompt-first multi-agent system for personal branding strategy, content creation, reputation management, and learning.**

> **Status: v0.1 foundation.** This repository provides role prompts, reusable workflows, templates, and a fictional end-to-end example. It is **not yet** an automated agent runtime, a scheduler, or a social media integration.

## Why this exists

Posting more is not the same as building a reputation. This project structures the work behind a credible personal brand: researching real evidence, choosing a position, telling useful stories, adapting them for channels, reviewing risks, and learning from results.

## Architecture

```text
             PRIVATE CLIENT WORKSPACE (never commit to this repo)
              goals | background | evidence | approvals | metrics
                                  |
                                  v
                      ORCHESTRATOR / WORKFLOW
                                  |
              +-------------------+-------------------+
              |                   |                   |
          RESEARCHER          STRATEGIST          STORYTELLER
              |                   |                   |
              +-------------------+-------------------+
                                  |
                       CREATIVE STRATEGIST
                                  |
                         CREATIVE CONCEPT GATE
                                  |
                          CHANNEL EDITOR
                                  |
                          QUALITY REVIEWER
                                  |
                         HUMAN APPROVAL
                                  |
                         MANUAL PUBLISHING
                                  |
                             ANALYST
                                  |
                         FEEDBACK / LEARN
```

The public repository contains **methods and fictitious examples**, not real client data. Each user owns a separate private workspace.

## Quick start (no coding required)

1. Clone this repository or read it on GitHub.
2. Make a **private** copy of the files under `templates/` in a separate client workspace. Fill in `client-profile.yaml`; keep it out of this repository.
3. Read [AGENTS.md](AGENTS.md), [architecture](docs/architecture.md) and [privacy guidance](docs/security-and-privacy.md).
4. In your AI assistant, use [the orchestrator](agents/orchestrator.md) to coordinate the stages in [onboarding](workflows/onboarding.md). Feed it **only information you are authorized to share with the AI service**.
5. Produce a documented positioning strategy using [positioning template](templates/positioning.md).
6. Use the [content workflow](workflows/content-cycle.md) to compare concepts, pass the [pre-draft creative gate](docs/creative-concept-gate.md), draft, review and request human approval. Publication is **manual** for this version.
7. Record actual links, outcomes and learning in your **private** copy of [publication tracker](templates/publication-tracker.csv).

Start with the [fictional walkthrough](examples/fictional-client/README.md) to see the flow without exposing personal information.

## Agents
| Specialist | Main responsibility |
| --- | --- |
| [Orchestrator](agents/orchestrator.md) | Scope, delegation, state transitions and review gates |
| [Researcher](agents/researcher.md) | Evidence gathering and claim verification |
| [Positioning Strategist](agents/positioning-strategist.md) | Audience, differentiation and narrative |
| [Storyteller](agents/storyteller.md) | Find stories and lessons from verified evidence |
| [Creative Strategist](agents/creative-strategist.md) | Research attention patterns, compare distinct concepts and pre-draft creative hypotheses |
| [Channel Editor](agents/channel-editor.md) | Adapt selected concepts into native platform scripts and copy |
| [Quality & Privacy Reviewer](agents/quality-reviewer.md) | Factual, strategic, editorial and confidentiality checks |
| [Performance Analyst](agents/performance-analyst.md) | Review observed results and propose experiments |

These are **roles specified as prompts**, not separately executing software agents yet. One AI assistant can play them sequentially; multiple assistants may execute them with human oversight.

## Repository map
- `agents/` reusable agent instructions
- `workflows/` step-by-step guided processes
- `templates/` blank reusable deliverables, including a [creative concept brief](templates/creative-concept-brief.md)
- `docs/` architecture, quality standards, security
- `examples/fictional-client/` invented non-sensitive example
- `docs/creative-strategy-simulation-tests.md` unexecuted fictional regression scenarios

## Operating rules
- **Human approval is required** before publishing, messaging people, or modifying public profiles.
- Mark unverifiable claims as **UNVERIFIED**. Never invent accomplishments, dates, metrics, testimonials or sources.
- Keep client data, credentials, non-public work materials and analytics outside the public repository.
- All examples are fictional. Audit generated output for personal or confidential data before any public commit.

## Roadmap
- [x] Separate public reusable methodology from private client data.
- [x] Create first prompt-first workflow, role definitions, templates and fictional demo.
- [ ] Validate v0.1 with a real private pilot.
- [ ] Define a portable, machine-readable state format and contract tests.
- [ ] Explore optional CLI / runtime, adapter interfaces and automatic quality checks.
- [ ] Evaluate community feedback, metrics and a possible commercial layer.

## License
MIT, see [LICENSE](LICENSE). This license permits commercial reuse; any future commercial offerings must be architecturally and legally compatible with previously published MIT code.
