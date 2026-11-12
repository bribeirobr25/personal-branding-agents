# R16 language-intent investigation and proposed remediation

**Date:** 2026-11-12  
**Scope:** public, independently fictional Discovery R16 test. No user account data.  
**Status:** investigation completed; correction **proposed but not applied** to frozen workflows. No model calls were made for this investigation.  
**Frozen baseline:** `main` at `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`.  
**Frozen candidate:** `B` at `3fd226adcf34376e99e7fbda11ace36638e3b370`.  
**Pilot evidence:** [v3 evaluation](../../tests/results/discovery-codex-pilot-v3-evaluation-2026-11-12.md), [R16 input fixture](../../tests/discovery_live_cases.json), and the four raw R16 turn records in [v3 rows](../../tests/results/discovery-codex-pilot-v3-2026-11-12/rows.json).

## Evidence observed directly

The first R16 user message **actually sent** to each arm was identical:

> Call me Arin. I run a small fictional bookstore and want to communicate what I've learned in Portuguese.

The second user message was:

> Actually call me Sol. Keep Portuguese. I haven't shared sales data.

Both outbound R16/U1 requests contain the frozen instructions and exactly that English-language user sentence, not a separate explicit `Please reply to me in Portuguese` directive. Tools were empty. The v3 context audit reports matching scoped payloads for 12/12 calls. The actual R16/U1 answers are in English, each using **Arin**. Both R16/U2 answers switch to Portuguese and correctly use **Sol** after the name change. This occurred in a fully completed 12/12 live-inference pilot; the larger 108-call battery was blocked. These observations stand.

**Crucial ambiguity:** `want to communicate what I've learned in Portuguese` naturally specifies the **language of the user's intended communication/content**, but does **not unequivocally request that the assistant's present conversational response be in Portuguese**. English dialogue while correctly recognizing future Portuguese content is therefore a reasonable interpretation. The original test rubric treated this as a mandatory current-turn conversation-language preference and gave both arms a hard FAIL. That is a **test-oracle / requirement-clarity defect**, not conclusive evidence of an agent ignoring a direct response-language instruction. The U2 phrase `Keep Portuguese` strengthens the user's language preference but remains compatible with content and/or conversation until context clarifies it.

**Do not rewrite or retrospectively relabel original v2/v3 reviews.** They truthfully reflect the preregistered rubric and actual outputs. Record this as a new interpretation, explain the mismatch, and amend **future** test requirements only under a versioned protocol. Existing HOLD and non-promotion remain in effect.

## Static prompt inspection

The frozen live runner's HOST instruction asks for the next user-facing Orchestrator reply and discloses tool limits; it contains **no explicit conversation-vs-deliverable-language rule**.

Both onboarding prompt versions supply an English example with the heading `Example (English; translate/adapt to the user's language)`. In the baseline, the document later says to explore `languages` when relevant to strategy. The candidate's compactness section additionally says `default to a concise response in the user's language`. Since the R16/U1 **input sentence is in English**, that rule does not unequivocally resolve whether the user's preference refers to the current chat or planned content. Shared contract language fields concern channel/draft languages rather than a separate conversation-language field.

These are **plausible contributors**, not experimentally isolated causes. We have **not** shown that English prompt examples caused the English responses, or that the candidate is generally unable to comply with an explicit Portuguese conversation-language request.

## Proposed minimal product clarification (NOT APPLIED)

Create a **new versioned candidate** of the Discovery instructions only after approval of the revised test contract; do not rewrite prior frozen commits or overwrite the old A/B traces. The proposed insertion, placed near the beginning of Orchestrator/onboarding instructions, is:

> **Language and address intent.** Track `conversation_language` (how the assistant responds now) independently from `deliverable_language` (language of posts, profiles or other future outputs). An explicit request such as `Please reply in Portuguese` must govern the very next user-facing response, regardless of the language used to type the request. An explicit deliverable-language preference does not by itself require changing the chat language; preserve it for future work. If a sentence such as `I want to communicate my experience in Portuguese` leaves the intended scope unclear, do not infer a hard conversation-language requirement. Continue naturally in the current conversation language or ask one brief scope clarification if needed. Apply name and language corrections **only when provided** and from the next response onward. Preserve normal evidence, consent and Discovery validation gates.

The product team may separately choose to proactively switch conversation language whenever a user names a content language, but that is a UX **product decision** requiring its own acceptance criteria, not a failure demonstrably implied by R16/U1.

## Preregistered diagnostic fixture plan

Use [versioned language-intent cases](../../tests/discovery-r16-language-diagnostics-2026-11-12.json). Keep two **independent scoring tracks**:

1. `conversation_language`: a hard gate **only when the user explicitly directs the assistant's reply language**; allow names/technical tokens or quotations in other languages, but assess the dominant response language manually.
2. `deliverable_language`: check when an actual deliverable is requested and produced; otherwise record it as a pending preference, **not** as a current response-language failure.

Also check current preferred name at each turn, preservation of non-language facts, no invented outcomes, no premature validation, and no publication without approval. Explicit instructions in English requesting replies in Portuguese or German are necessary negative controls for language-of-input bias. The original ambiguous R16 should be re-run and scored **INDETERMINATE for current-turn response language**, not FAIL/PASS. Include natural-language variation, explicit changes at U2, mixed chat/deliverable preferences, and name changes.

**Comparison strategy:** run frozen A and B first on the revised diagnostic fixtures with real isolated model calls, preserving complete outputs and settings. Only if an unambiguous conversational-language failure is observed should a separately versioned B2 patch be implemented and tested against the frozen baseline and unpatched B, with approvals and fresh resources. Do not compare new B2 to old B while silently changing the oracle or sampling method.

## What was and was not validated here

**Executed:** read the original literal R16 fixtures, two model-bound first-turn payloads and four actual replies, inspected the frozen prompt instructions/host contract and comparison rubric, identified the semantic ambiguity and drafted an explicit diagnostic contract.

**Not executed:** additional LLM calls, independent A/B behavior tests with the rewritten cases, a language-priority causal experiment, changes to the real workflow prompts, a release review, the 108-call battery, a merge or any paid inference.

**Decision:** R16 requires a **test-definition correction before a workflow correction**. HOLD stays in place until the new unambiguous cases and applicable approval gates are reviewed. A prompt patch without disambiguating the requested behavior would risk overfitting to a misleading acceptance test.
