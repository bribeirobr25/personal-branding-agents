# Probabilistic fixtures integrated with A/B Discovery workflow rehearsal

Date: 2026-11-11. Branch: `feat/onboarding-strategic-discovery-20261111`. **Status: fixture integration implemented and checked; workflow behavior executions NOT RUN.**

## Purpose and scope
This step connects the existing probabilistic scenario methodology to a **paired workflow event sequence**. The generated fixture is the exact shared scenario input for both frozen arms. It explicitly enumerates the Orchestrator and Researcher stages through the Discovery validation gate, rather than claiming the earlier 4,352 policy reference states represent conversations.

Source: [`tests/discovery_workflow_ab_fixtures.js`](../discovery_workflow_ab_fixtures.js). Reproduce in a clone with `node tests/discovery_workflow_ab_fixtures.js 20261111 24 > /tmp/discovery-ab-fixtures.json`. The generated JSON contains only fictional user inputs. The output is not a test result.

## Frozen arms
- A main `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92`
- B candidate `3fd226adcf34376e99e7fbda11ace36638e3b370`
- Each arm is instructed to use its own frozen `agents/orchestrator.md`, `agents/researcher.md`, `workflows/onboarding.md`.

## Mandatory per-arm stages
The fixture provides the same fourteen stage labels, in order: orchestrator opening; initial user/goal; optional sources invitation; sources and permissions; Researcher delegation; authorization receipt; access/evidence receipt; provisional summary; user correction/confirmation; targeted re-research or no-access action; follow-up receipt or not applicable; revised summary; user confirmation or not; Discovery gate decision.

For each stage, record **literal user input, literal Orchestrator/Researcher response, observed access status, evidence receipt, decision and execution mode**. Inaccessible fictitious sources must not be labeled retrieved. A no-op specialist event must explicitly be recorded as N/A. No final strategy before profile confirmation, and no publication authorization implied.

## Sampling integration
The generator fixes seed `20261111`, draws fictional combinations across six persona types, five source classes, four consent states, four evidence classes, five correction categories, three user styles, plus injection/material-conflict/readiness booleans. It forces ten dangerous/underrepresented condition templates at the front, then samples the rest deterministically. This is **stratified prioritization + seeded randomization**, not a population-representative draw. The separate policy runner reports pairwise coverage on its own declared axes; this new fixture generator does not claim 100% pairwise coverage.

## Actual integration validation receipt
Read the script from the GitHub candidate branch and evaluated it in the JavaScript execution environment with command-line arguments `20261111 24`:

- **24** unique synthetic scenario IDs generated.
- **2** arms bound to fixed git SHA references.
- **14** required workflow events per scenario.
- A second execution using the same seed and count returned identical structured JSON.
- Changing seed to `20261112` changed the sampled fixtures.
- All 24 fixtures contained the 14-stage event list.
- Ten directed high-risk templates appeared in the initial group.
- No actual user/agent conversations, source fetches, safety enforcement or independent reviews were executed in this integration step.

## What the next execution must produce
Produce per-arm transcripts from the same fixture IDs, preserving exact messages and real steps (or state clearly that a step was simulated), then a comparison report of safety, naturalness, initiative, concision and usefulness. Where genuine isolated model runs are not available, a same-assistant staged roleplay is **illustrative and bias-prone**, not an independent behavioral assessment. Do not score missing outputs as passes. Capture source access truth, permission withdrawal and user confirmation.

The candidate remains candidate; the `main` repository branch is untouched. No merge, release or behavioral performance claim.
