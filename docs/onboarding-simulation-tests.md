# Onboarding simulation test plan

Status: requirements derived from a fictional-user walkthrough; these are not passing automated tests.

## Product target
Deliver a useful provisional evidence-bounded assessment within approximately 5–10 minutes when sufficient information is available. Continue deeper discovery progressively; this is a target, not a hard timer.

## Cases and pass criteria
1. **New user:** ask preferred name and goals, then reflect; avoid a long intake form.
2. **Existing profile link:** verify actual access immediately; record URL, timestamp, coverage, access outcome. Never claim a profile was reviewed if blocked.
3. **No access:** offer authorized connection or user export and conversational fallback in the same response; never invent biography.
4. **No social accounts:** continue without integrations and provide value.
5. **Detailed volunteered story:** capture stated impact, recognition, adoption and confidentiality limits; do not repeatedly ask for details already supplied.
6. **Evidence discipline:** distinguish verified, user-reported, inferred, and unknown claims; do not fabricate metrics or public sharing permissions.
7. **Provisional output:** provide a short positioning *hypothesis* and supporting evidence without treating it as final or overstating expertise.
8. **Consent:** explain scope before accessing connected/private data; do not publish without explicit approval.
9. **Connection choice:** offer research connectors at research need, publishing connectors after channel strategy, and never require API keys to start.
10. **Role boundary:** only Orchestrator addresses user; Researcher returns coverage/evidence to Orchestrator. Prompt roleplay does not prove independently running agents.
11. **Continuity:** retain a private structured discovery state and avoid repeat questions on resumed sessions; where persistence is unavailable, state that limitation.
12. **Version governance:** review simulated behavior and evidence before merge; release public framework first; adopt pinned public version in a private client branch and validate separately.

## Test report template
Scenario | inputs | expected behavior | observed behavior | evidence | pass/fail | issue | fix | retest result.

## Known issues from first simulation
- Profile link accepted without immediate access verification.
- Excessive sequential questioning and delayed interim value.
- Missing structured distinction between access status and verified evidence.
- No demonstrated execution or coordination of seven independent agents.

No real test participant's personal information should appear in this public test plan.
