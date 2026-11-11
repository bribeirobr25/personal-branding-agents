# Per-source authorization and evidence checks, follow-up

**Date:** 2026-11-11  
**Commit implementing reference policy:** `a68e265d58cb5a6f90134353f66878fc8082ad5c`  
**Scope:** branch-only test model; not a released framework change.

## Corrections

- Three synthetic sources have individual `allowed`, `withdrawn`, `available`, `contains_claim`, and `independent_support` flags.
- Access requires permission and availability per source. Permission for LinkedIn does not grant Instagram access.
- Extracting a claim requires actual access in the fixture.
- A claim is marked `verified` in the *reference model* only when an independent-support fixture flag is set; a readable post by itself is `user_reported`.
- Withdrawing consent prohibits subsequent access in the *reference model*. This does not prove actual connector revocation.
- Five directed cases exercise restricted source permission, read-but-unverified content, independent support, consent withdrawal, and inaccessible source.

## Executed verification

An equivalent JavaScript reference-policy harness was run in the execution environment after the Python script was committed; this was **not** execution of the GitHub Python script itself. The Python file could not be downloaded into the Python runtime because the environment's DNS lookup for GitHub failed. The equivalent JavaScript harness used a 32-bit LCG with seed 20261111 (therefore **not** Python's `random.Random` sample sequence).

- 5 directed synthetic scenarios.
- 2,400 stochastic synthetic samples.
- 57,837 evaluated assertions, including conditional invariants.
- 0 observed invariant failures.

**Interpretation:** internal consistency of the reference policy under those synthetic inputs, not functional adherence by LLM agents. Test and implementation share assumptions. The Python version remains to be executed in an environment with repository checkout; real role-based conversations, access receipts, claim verification, and independent assessment have not yet been run. The third robustness battery remains separate.

## Required before a functional PASS

Run model prompts in isolated user/agent contexts with source-granular authorization and actual tool logs. Score whether the Orchestrator and Researcher distinguish `accessed`, `extracted` and `verified`, including after the person withdraws permission. Compare candidate branch to frozen baseline and preserve transcript evidence; do not infer real-world efficacy from stochastic policy-model checks.
