# Framework releases and private client upgrades

Status: proposed governance policy (2026-11-09). Applies to the reusable public core; individual client workspaces remain private.

## Source of truth
- The public `personal-branding-agents` repository is the source of truth for generic agent roles, task contracts, onboarding, reusable workflows, templates, and quality gates.
- Client-specific positioning, documents, research, drafts, approvals, metrics, and configuration belong only in each client's private workspace.
- A public change must work with independently invented synthetic examples; never copy or lightly anonymize a private client case.

## Public change lifecycle
1. Open a scoped branch and PR in the public framework. Include problem, proposed change, affected contracts/templates, compatibility impact, security considerations, and synthetic acceptance examples.
2. Review architecture, factual quality, privacy and safety. Check full diff, filenames, links, attachments, and potential sensitive information. Require independent review and owner approval before public merge.
3. Merge to public `main` only after checks. Create an immutable Git tag (e.g. `v0.2.0`) and release notes identifying changes, breaking changes, and migration steps. While the framework is pre-1.0, explicitly document compatibility; don't infer it from version numbers.
4. Client implementations consume an explicitly pinned release tag and resolved full commit SHA. Never automatically track moving `main`.

## Private client upgrade lifecycle
1. Create a branch in the private workspace (e.g. `chore/upgrade-framework-v0.2.0`) after the public release.
2. Update the framework version pin and migration notes. For the current prompt-first implementation, this is a **documentation reference**, not an executable dependency, sync, submodule or automated pull.
3. Compare the new public role instructions, contracts, workflows, templates and gates against private overrides and existing strategy. Adapt only necessary private integration files; preserve personal strategy and evidence.
4. Run a conversational onboarding regression and content/quality-gate scenario using safe private test material. Check no private data are sent to the public repository.
5. Open a private PR summarizing the pinned old/new versions, compatibility results, exceptions, rollback plan and reviewer decision. Merge only after review.
6. Record adoption in a private upgrade log. To roll back, restore the previous pin and compatible private adaptations through a new reviewed PR.

## Feedback loop
- Generic improvements discovered through a private pilot become public issues/PRs only after rewriting them as fully synthetic, user-agnostic requirements and examples.
- Private client outcomes, identities, source links, unpublished drafts and metrics never cross that boundary.
- Public release and private adoption are two distinct events. No public PR merge implies automatic private upgrade.

## Future automation
A version-aware updater or CI workflow may later open private upgrade PRs, but only after explicit implementation, least-privilege permissions, privacy review, tests and human approval. No such automation exists today.
