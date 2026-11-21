# Changelog

## 0.6.0 - 2026-11-21

- Adds the Positioning phase (`workflows/positioning.md`), method 0.6.0, contract 0.3.0.
- Keeps the Discovery phase as published in method 0.5.3 (`workflows/onboarding.md`), with a hand-off into Positioning after a direction is chosen.
- The content cycle starts after Positioning closes or stops, once a channel exists.
- Contract 0.3.0 adds machine-checked Positioning `record_state` values `working`, `validated`, and `superseded`. Task envelopes, evidence statuses, content states, and approval records keep their 0.2.0 meaning.
- **Status:** Not validated. Checked only with forced-case simulations on one model family (same-model and structural only). The full forced run did not meet its safety bar; a targeted re-test of the fix met it. Not independently validated.

## 0.5.3

Published tag v0.5.3. Optional Discovery asks. See `docs/releases/v0.5.3.md`.
