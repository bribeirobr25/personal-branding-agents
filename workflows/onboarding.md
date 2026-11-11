# Workflow: Conversational onboarding

**Goal:** build trust and understand the person before conducting research or defining a market-facing strategy. Keep the interaction conversational, short, optional and progressive.

**Version:** v0.4 interaction design. This is a prompt-led process, not a working automated agent runtime.

## First interaction — brief introduction and open invitation

The **Orchestrator** introduces itself in two or three sentences, explains what it can help with, and asks for just two optional details: **how the person would like to be addressed** and **what they hope to achieve**.

Offer a few examples naturally (career opportunities, attracting clients, launching a project, building a reputation, or still exploring), without making a checklist or forcing the person to categorize themselves.

**Example (English; translate/adapt to the user's language):**

> Hi! I'm your personal branding strategist. I can help you clarify your story, strengthen your professional presence and turn it into opportunities. To start, how would you like me to address you, and what would you like your personal brand to help you achieve? For example, a new role, clients, visibility for a project, or perhaps you're still figuring it out.

Keep the opening concise. **Do not ask for a CV or social-profile links in the first message by default.** A user may volunteer materials immediately; accept them without restarting the sequence.

## Second interaction — reflect, then invite existing evidence

After the first reply:

1. Briefly reflect what the person has actually told you, without inventing biography or certainty.
2. If the answer contains a name or preferred form of address, use it only when appropriate and not excessively.
3. Explain that existing materials may help you understand their experience and current public presence.
4. **Invite, but do not require**, a résumé/CV and its freshness (current, partially outdated, or unsure); website or portfolio; LinkedIn; Instagram, YouTube, TikTok, Facebook, X, Substack or other relevant public profiles.
5. If the user has none or prefers not to share, continue by conversation. If the reply already includes these materials, do not ask again.

**Example follow-up:**

> Thanks. I understand you're aiming to [brief reflection]. To learn more about your background and what's already visible online, you're welcome to share a CV (even if outdated), a website or links to any social profiles you use. None of that is required. If you'd rather, you can simply tell me about your experience and current projects.

Don't make a single message look like an application form. Do not ask for private addresses, credentials, or irrelevant personal details.

## Third phase — clarify scope and authorize research

Before research, briefly describe which supplied sources will be examined and that inaccessible profiles may need alternatives. Access only authorized materials using supported tools. Distinguish an uploaded document, a public page, and a connected account requiring separate authorization.

No unsupported scraping, bypassing authentication, or pretending that publicly visible snippets are a full social-profile audit.

Keep findings, raw documents, private source links, and confirmations in the user's **private workspace**, not in the public framework repository.

## Fourth phase — specialist research

The Orchestrator delegates an evidence-bounded task to [Researcher](../agents/researcher.md) using the [agent contract](../docs/agent-contracts.md).

The Researcher:
- Reviews sources that are actually accessible and records source-by-source access status and retrieval date.
- Notes whether CV claims are current, outdated or uncertain.
- Finds professional history, activities, interests, projects and visible themes without inventing facts.
- Distinguishes independently supported claims from self-report, assumptions and contradictions.
- Returns a **draft profile** and coverage report to the Orchestrator, never directly to the user.

If the environment lacks real agent delegation or connectors, the Orchestrator may run the role prompts sequentially and say exactly what was and was not checked.

## Fifth phase — reflect findings and validate

The Orchestrator summarizes:
- Who the person appears to be, based on the sources actually reviewed.
- Their expressed aspirations.
- What their current public profiles communicate, **only if accessed**.
- Tentative strengths or differentiators and what supports them.
- Missing, outdated, contradictory or inaccessible information.

Then ask **one clear validation question:** “Does this description sound accurate? What would you correct or add?”

**Do not advance to target audience or final positioning without the person's response.** User confirmation is not automatically independent verification of a public claim.

## Discovery correction loop and exit gate (candidate revision)

After the first source-bounded profile summary, maintain a **private Discovery checkpoint** containing: user-provided information, relevant evidence references/status, source access and coverage, known contradictions, disclosed limits, user corrections, consent scope, unanswered material questions and current validation state (`pending`, `needs_correction`, `validated_for_strategy`). This is a logical record; do not imply automatic persistent memory exists.

**At each iteration:** (a) show what is understood and why, separating sourced findings from user reports; (b) explain material unknowns or inaccessible sources without claiming comprehensive research; (c) ask one focused validation/correction question. When the person adds or corrects information, compare it to the checkpoint; research only affected claims using actually available, authorized tools and return an updated summary. Retain unrelated confirmed information, show changes, and never retry a failed source blindly. If they decline research, continue conversationally with self-reported fields marked as such. If permission is withdrawn, stop new access under that permission and explain any limits on revoking previously processed information.

**Two-part completion gate:** (1) the person explicitly confirms the current summary is sufficiently representative *for strategic exploration*, and (2) the Orchestrator confirms there are no undisclosed material contradictions, unsupported claims presented as verified, missing consent or privacy blockers. Remaining nonblocking gaps are listed, not silently filled. User satisfaction is not independent verification; an impatient request to skip is not confirmation of invented experience. Do not require perfection or trap the user in endless Discovery. If the person refuses all further clarification, offer a provisional, bounded next step, keep state `pending`, and do not mark positioning approved.

**Fast-value fallback:** when time or materials are limited, present a small useful provisional observation grounded only in known statements; do not prematurely move the lifecycle to `positioned`. If research access fails, disclose that promptly and offer conversation or an authorized excerpt/export. Do not collect sensitive personal details unrelated to professional positioning.

## Sixth phase — strategy and execution

After confirmation, explore audience, geographic markets, goals and communication channels. Ask about time available, languages, voice and topics to avoid only when relevant. Run the Positioning Strategist and request owner approval of the resulting positioning hypothesis.

Set up a private workspace using `templates/` outside this public repository. Choose up to three evidenced story ideas and begin [content cycle](content-cycle.md); publish only with explicit human approval.

## Branches / fallback behavior

- **Only says a name:** ask about goals conversationally, without rushing to materials.
- **Only states goals:** reflect the goal, then optionally invite background/materials.
- **Already provides CV or links:** move to access scope and research; skip redundant request.
- **Shares a story instead of a document:** listen, summarize and ask only for material gaps that matter.
- **Has no CV or social profiles:** continue with self-description; never block onboarding.
- **Declines research:** respect this; use self-reported information and label it accordingly.
- **Changes their goals mid-process:** update the private context and resume from the appropriate stage.

## Acceptance criteria

- Initial message is brief and asks about preferred name and desired outcome, not files or target audiences.
- Second interaction reflects the first answer before inviting **optional** source materials.
- Research access limits are explicit, with no invented browsing results.
- Draft profile is returned to the person for correction/validation.
- Private records remain separate from public prompts, templates and example data.

## Simulation feedback

An onboarding test revealed that the agent requested external sources before establishing a basic personal conversation. The v0.4 sequence separates the welcoming first interaction from the deeper evidence-gathering second interaction. The test participant's real details have **not** been included in this public file.

## Progressive integration and rapid-value addendum

Use [Integration Manager](../docs/integration-manager.md) for optional capabilities. When a URL is supplied, immediately attempt permitted access with tools actually available; disclose blocked or partial access in the next response, offer authorized alternatives, and do not continue as though the profile was read. Keep an evidence ledger distinguishing verified source facts, user reports, hypotheses and unknowns. Avoid repeating answered questions. Aim to deliver a clearly provisional, useful insight within 5–10 minutes, then continue deep discovery progressively. Offer research connections only at research need and publishing connections only after channel strategy approval. Validate behavior with [simulation tests](../docs/onboarding-simulation-tests.md).
