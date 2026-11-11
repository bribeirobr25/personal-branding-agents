# Second-battery seeded policy Monte Carlo execution

**Date:** 2026-11-11. **Mode:** deterministic JavaScript reference-policy sampling in the execution environment; not an LLM or connector test. **PR status:** unmerged branch only.

**Random algorithm:** 32-bit linear congruential generator, state `20261111`; update `state = (1664525 * state + 1013904223) mod 2^32`, uniform draw `state / 2^32`. This is **NOT identical** to the Python `random.Random` sample stream in `tests/discovery_policy_monte_carlo.py`; the exact generator matters for reproduction. Inputs are independently sampled uniform categories, not a model of the real population.

Dimensions: `recognition` (3); `evidence` (4); `consent` (4); `style` (4); `source` (2); `confirmation` (2); `material_blocker` (2).

**Executed:** 2400 sampled states; 26400 invariant checks; **0 failed checks**. Predicted access allowed: 595; evidence classified as externally verified *by this simplistic reference policy*: 147; predicted Discovery validated: 422. These are synthetic state counts, **not** empirical outcomes or performance estimates.

Invariants tested: authorized access; verified-claim requires access; no premature validation; no publication; unrelated information retained; provisional feedback; loss of verification on source inaccessibility; invariance to display-name change; withdrawal stops access; no validation without confirmation; unrelated correction does not erase unrelated facts.

**Failure examples:** none.

**Limitations / risks:** This policy model assumes `accessible` evidence can be marked verified without inspecting the underlying claim. A real Researcher must distinguish access from independent verification. `limited` consent is modeled as general access and does **not** enforce source-by-source authorization. Both are simplifications that must be addressed in future tool-level tests, not treated as passed features. No LLM conversation, data access, actual withdrawal enforcement, or independent reviewer was run. A zero failure result only means the sampled cases fit the simplistic rules written by the test author.

**Related:** [scripted conversation handoffs](discovery-second-battery-scripted-2026-11-11.md); [protocol](../../docs/proposals/discovery-simulation-protocol-2026-11-11.md).
