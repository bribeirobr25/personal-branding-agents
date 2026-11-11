# Proposal: Progressive Discovery and Strategic Positioning

**Date:** 2026-11-11  
**Status:** Design decisions recorded; implementation and behavioral validation pending  
**Scope:** Public, user-agnostic method only. No real user transcripts, biographies, social handles, account data or private research records are included.  
**Baseline:** Public framework method 0.2.0. This proposal does not change the released contracts or claim autonomous execution.

## Purpose

Make the journey from first contact to positioning a conversational, evidence-led process. Separate **understanding who the person is today** from **deciding what outcomes and reputation they wish to build next**. Do not turn intake into a form or treat content publishing as a default goal.

The Orchestrator remains the sole user-facing role. Specialist prompts return bounded findings through it. An individual assistant may simulate the roles sequentially; this document does not imply a working worker runtime, connector, memory service or background research process.

## Decision 01: Presentation and validated Discovery

### Phase 1. Presentation

- Introduce the framework and the kind of help it offers in plain, brief language.
- Invite a preferred form of address and, optionally, an initial hope or goal.
- Do **not** require a CV, social links, credentials or a detailed biography in the first message.
- If goals or materials are volunteered early, record them without forcing the later strategy phase or asking again.
- **Exit:** the relationship and conversational scope are established; no strategic positioning is assumed.

### Phase 2. Personal and Professional Discovery

1. **Listen:** gather professional history, activities, experiences, projects, skills and interests progressively. Use information already supplied and ask only for consequential gaps.
2. **Invite optional materials:** résumé/CV (including whether current), portfolio, website and relevant social profiles. Conversation-only participation must remain possible.
3. **Scope and authorize access:** say which materials/sources can actually be accessed and request any separate authorization required. Never treat a URL as permission to access a private account.
4. **Research:** Orchestrator dispatches scoped work to Researcher. Record source coverage, retrieval date, evidence status and contradictions. Distinguish verified information, user reports, hypotheses, unknowns and inaccessible sources; a source's claims are not automatically independently verified.
5. **Reflect:** Researcher returns to Orchestrator, which presents a short, understandable profile summary, meaningful sources/limits and remaining gaps.
6. **Validate:** ask the person whether this is an accurate enough understanding, and what should be corrected or added.
7. **Iterate if needed:** on meaningful additions, contradictions or corrections, update the private profile and research only the affected questions. Explain missing results or blocked access truthfully. Show the revised understanding and ask again. Do not restart the full intake or endlessly repeat unavailable queries.
8. **Exit:** user confirms that the profile is sufficiently accurate **for strategy to begin**. This is validation of shared understanding, not external proof that every claim is true.

Store source records, real profile, feedback and approvals only in the user's separate private workspace. Preserve a resumable checkpoint if the host provides persistence. If the user declines research, continue with appropriately labeled self-reported information. No fixed number of questions or repeated mandatory research cycle.

### Discovery acceptance criteria

- A first-time user can converse naturally without documents or social accounts.
- Research is limited to sources actually accessible and authorized.
- Researcher-to-Orchestrator-to-user feedback is traceable and never fabricated.
- Corrections lead to targeted supplementary research or transparent no-result reporting.
- No strategy is finalized before the user validates the Discovery summary.

## Decision 02: Strategic Discovery & Positioning

**Entry gate:** Phase 2 profile has been validated as sufficiently accurate for strategy. No new mandatory phase is inserted between Discovery and Strategy. The user may state aspirations at any time; deep exploration and approval occur here.

Use the **Brand Journey** questions associated with Caleb Ralston as a methodological reference, adapted for people with different aims and levels of experience:

1. **Desired outcome:** What does the person actually want to achieve, why, on what horizon, and what is explicitly *not* a goal?
2. **Needed reputation:** What would the relevant people need to know or trust about them for that outcome?
3. **Reputation-building actions:** What work, projects, behavior, proof and relationships would legitimately earn that reputation?
4. **Learning needs:** What skills, knowledge, experience or proof are missing before those actions are credible?

Do not import commercial conversion targets or follower-growth assumptions as universal success metrics. Public content may be irrelevant or counterproductive for some people.

### Six progressive strategic moments

| Stage | Orchestrator / specialist task | Expected private deliverable |
| --- | --- | --- |
| **3.1 Outcomes and motivations** | Explore the person's intended outcomes, reasons, priorities, horizon, capacity and constraints; distinguish current interests from decisions. | Validated draft outcome map |
| **3.2 Desired reputation** | Identify desired/unwanted associations and reputation needed for each outcome. Avoid declaring unearned expertise. | Reputation/association map |
| **3.3 Audiences, problems and opportunities** | Identify relevant audiences, problems they face, potential contributions and potential opportunities. Use Researcher for authorized market or audience evidence where a material claim needs checking. | Audience/problem/contribution map |
| **3.4 Actions, proof, differentiation and gaps** | Evaluate contextual credibility, personal contribution, skills and interests by topic; distinguish expert and learner claims; determine work/proof and learning still needed. | Evidence-based strategic diagnosis and action/learning gaps |
| **3.5 Alternative positions and trade-offs** | Develop genuinely different defensible hypotheses. Compare whom each serves, benefits, risks, unwanted associations, practical effort and what it leaves out. | Compared positioning options with evidence and limitations |
| **3.6 Discussion and owner validation** | Orchestrator presents alternatives, answers objections and records corrections. Only explicit user validation makes the selected hypothesis an approved direction. | User-approved positioning hypothesis, goals and decision record |

This is **progressive conversation**, not a rigid six-page questionnaire. The Orchestrator may revisit earlier hypotheses when new facts materially affect them. Researcher remains available throughout Strategy and returns findings to Orchestrator; it does not contact the user independently. Unknown or contradictory claims stay qualified.

### Strategy completion gate

Do not advance as if the strategy were approved until there is adequate user validation of:

- desired outcomes and non-goals;
- audience, problem and expected contribution;
- desired reputation and associations to avoid;
- contextual evidence, differentiators and boundaries;
- practical actions and learning/proof gaps;
- defensible alternatives with trade-offs;
- the selected hypothesis and rationale.

A preference for a concept is not permission to publish, send messages, purchase services or connect accounts.

## Downstream boundary

After approved positioning: establish a modest, evidence-backed content or non-public action plan. When content is useful, reuse the existing Storyteller -> Creative Strategist -> concept SELECT -> Channel Editor -> five final quality gates -> exact human approval -> confirmed publication -> measurement process. This proposal neither bypasses the current gates nor implements autonomous workers or publishing.

## Source fidelity and reuse

- The four reverse-journey questions are attributed here to the publicly discussed Brand Journey approach; the six-stage conversational workflow, safeguards and gates are **our proposed adaptation**, not a claim that the external author prescribed this exact implementation.
- Do not copy protected course transcripts, scripts, personal examples, paid workbooks or proprietary expression into the public repository.
- Maintain the current reusable, non-client-specific framework boundary.

## Existing documents to reconcile in a future implementation PR

- [Onboarding](../../workflows/onboarding.md): make the correction/research/validation loop explicit while preserving voluntary early goals and optional source materials.
- [Orchestrator](../../agents/orchestrator.md) and [Researcher](../../agents/researcher.md): scoped handoffs, supplemental research, return and truthful coverage.
- [Positioning Strategist](../../agents/positioning-strategist.md) and [Knowledge & Positioning](../knowledge-and-positioning.md): six strategic moments and alternatives, using existing GoalMap rather than incompatible parallel state.
- [GoalMap](../../templates/goal-map.md), [Architecture](../architecture.md) and contracts: review only the necessary additions; preserve compatibility and user approval.
- Evaluation: build independently fictional beginner, experienced, career-transition, low-disclosure and no-content scenarios. Test correction loops and no-result behavior. Record actual executions separately from unrun scenarios.

## Status, decisions and next step

**Recorded:** proposal for the first three phases and the deepened strategic transition, including responsibilities, gates and expected outputs.  
**Not yet done:** modifying active workflows/contracts, executing simulations, independent review, release, private adoption or merging this branch.  
**Next:** review the six Strategy moments with representative synthetic cases, then prepare an implementation PR with explicit compatibility/privacy checks and user approval before merge.
