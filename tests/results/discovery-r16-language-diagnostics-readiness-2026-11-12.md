# R16 language diagnostics: inspection, fixtures and readiness

**Date:** 2026-11-12  
**Status:** static diagnosis and offline fixture validation **COMPLETE**; live model A/B diagnostic **NOT_RUN**.  
**Versions:** A `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`, B `3fd226adcf34376e99e7fbda11ace36638e3b370`; frozen prompts unchanged.  
**Working branch only:** `feat/onboarding-strategic-discovery-20261111`.

## Evidence evaluated

The [investigation](../../docs/proposals/discovery-r16-language-intent-investigation-2026-11-12.md) reviewed the literal two-turn R16 fixture, the actual outbound frozen first-turn requests for both A/B, the response records, the host instruction and shared/frozen agent and onboarding prompts, and the v3 evaluation report.

**Observed:** Both arms returned English at U1 with the correct current name Arin, and switched to Portuguese with the corrected name Sol at U2. Both U1 requests contained the English-language message: `I ... want to communicate what I've learned in Portuguese.` Neither request said `Please reply to me in Portuguese`. Thus the original U1 establishes **content-language intent**, but an immediate Portuguese **conversation** requirement is ambiguous. The original report's hard FAIL remains historically recorded under its original rubric. This follow-up flags a **test-oracle clarification**, rather than claiming proof that explicit requests for Portuguese are ignored.

The shared host instructions contain no chat-versus-content-language distinction. Both onboarding prompts use an English example, and candidate B also says to reply in the user's language; the English input does not resolve which language that refers to. These observations suggest plausible causes but **do not experimentally isolate a causal mechanism**.

## Prepared diagnostic fixtures

- [Diagnostic cases](../discovery-r16-language-diagnostics-2026-11-12.json): **12** fictional scenario IDs, **16** user turns, including the unchanged original R16 as L01.
- **12** turns have an unambiguous, explicit current-turn assistant response-language request and therefore a language hard gate.
- **4** turns are not hard-scored for assistant chat language because their language intent is ambiguous or content-only.
- **6** turns deliberately request different languages for the conversation and future output.
- **7** turns specify a preferred current name. Name changes are constrained to the turn in which the user requests them.
- All deliverable-language preferences are **pending** (no deliverable is generated in this Discovery fixture suite). A future artifact can be evaluated separately.

The dataset covers English input requesting Portuguese or German replies, native German/Portuguese reply-language requests, English replies with Portuguese future content, explicit chat/content differences, later name corrections, later language changes and the ambiguous original case.

## Reproducible validation and CI

The [static validator](../check_discovery_r16_language_fixtures.js) checks dataset structure, expected hard-gate labels and preservation of the unchanged original R16 text. It is **not a multilingual model response grader**.

- **Actual GitHub Actions run:** [43137518361](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43137518361), completed **SUCCESS** on commit `15de1db7a23bf67ebb521852ac2f19b612ac9ac6`.
- Checkout documentation validation, language fixture validation and existing synthetic process-level regressions all passed. This CI does **not** make new model calls or certify a human-like assistant's language behavior.
- An earlier intermediate run [43137239757](https://github.com/bribeirobr25/personal-branding-agents/actions/runs/43137239757) failed because the investigation document linked to the fixture **before the fixture file existed**; the missing target was added and subsequent CI passed. Preserve this transient failure as part of the sequence.

## Recommendation and decision boundary

1. **Do not alter frozen A/B workflows yet.** The first fix is to the test's **requirement and oracle**: distinguish `conversation_language` from `deliverable_language` and avoid scoring ambiguous content-language mentions as explicit chat-language violations.
2. In a **new, separately authorized and versioned real-call pilot**, execute the exact diagnostic fixtures using frozen A and B prompts and context isolation. Evaluate explicitly requested languages from the actual generated answers, plus the current name at each turn, and preserve all raw calls, cost/quota gates and negative evidence.
3. If an **unambiguous** next-reply language request fails, consider the [minimal prompt clarification](../../docs/proposals/discovery-r16-language-intent-investigation-2026-11-12.md) as a new treatment B2, with a new frozen SHA and a separately preregistered comparison. Do not treat B2 and old B as the same version.
4. Keep the old v3 pilot and original R16 FAIL labels intact. Do **not** infer permission to execute the previously blocked 108-call batch from this offline outcome; the old HOLD and owner/gate requirements remain active.

**Completion claim:** investigation, test redesign, fixture validation and CI evidence registered. **Not claimed:** prompt-level causality, live language compliance, comparative winner, new pilot execution, merge, release or owner-approved exception.
