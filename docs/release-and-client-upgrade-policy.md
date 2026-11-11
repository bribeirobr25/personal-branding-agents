# Framework releases and private client upgrades

Governance policy for the reusable public core; individual client workspaces remain private. Clarified before the first 0.2.0 release to distinguish required owner authority from review exceptions.

## Source of truth

- The public repository is the source of truth for generic roles, contracts, onboarding, workflows, templates and quality gates.
- Client-specific positioning, documents, research, drafts, approvals, metrics and configuration belong only in each client's private workspace.
- A public change must work with independently invented synthetic examples; never copy or lightly anonymize a private client case.

## Public change lifecycle

1. Open a scoped branch/PR with problem, proposed change, affected contracts/templates, compatibility, security considerations and synthetic acceptance examples.
2. Review architecture, factual quality, privacy and safety. Check the complete diff, filenames, links, attachments and metadata. Obtain an independent review of the release-relevant content and explicit owner approval before merge, subject only to the narrowly defined review exception below.
3. Merge only after the applicable gates. Create an immutable Git tag and release notes identifying changes, breaking changes, evidence, limitations and migration. Pre-1.0 version numbers do not establish compatibility by themselves.
4. Client workspaces pin a release tag and resolved full commit SHA, never automatically track moving main.

## Authority and exceptions

**Explicit owner approval is always required and cannot be waived by an assistant, reviewer, tool result or checklist.** Approval must identify the work/scope to be merged; unexpected material changes require renewed approval. Owner identity/authority evidence stays in the appropriate private records; public notes may state approval without reproducing private conversations.

Independent review is the default. It may be human or a separately executed automated reviewer, but its identity, source coverage, findings, limitations and resolutions must be recorded. Same-model role switching or author self-review is not independent review. A separately executed automated review is not a human security/legal certification. A source-access failure is not a completed review; supplied source snapshots may be reviewed with their scope explicitly recorded.

Only the owner may explicitly accept an exception for a particular NOT_RUN review or test gate. The record must state the exact gate, release candidate/scope, reason, risk, compensating evidence, follow-up owner and expiry/review trigger. A general instruction to finish work is not an implied waiver. An exception does not turn NOT_RUN into PASS and does not carry forward to another release. Unresolved material privacy, fabrication or unauthorized-action failures block release, not merely the score average. No review exception replaces owner approval.

## Private client upgrade lifecycle

1. After the public release, create or finish a staged private adoption branch.
2. Update the release tag, resolved commit and migration notes. In this prompt-first version this is a documentation reference, not executable sync, a submodule or automatic pull.
3. Compare public instructions/contracts/workflows/templates/gates with private overrides. Adapt only necessary integration files; preserve strategy, evidence and history.
4. Run conversational onboarding and content/quality-gate regressions using safe private or synthetic test material. No private data may be sent to the public repository.
5. Open/update a private PR with old/new references, compatibility evidence, exceptions, rollback and reviewer decision. Merge only after review and explicit owner authorization.
6. Record adoption. Rollback restores the previous reference and compatible adaptations through a reviewed PR without erasing evidence or publications.

Public release and private adoption are separate events. Neither public merge nor a manifest version automatically upgrades clients. Future automation requires explicit implementation, least privilege, privacy review, tests and authorization; no automatic client updater is provided.

## Versioning and objective gates

Use Semantic Versioning tags vMAJOR.MINOR.PATCH. Pre-1.0 PATCH is compatible correction; MINOR is feature/contract evolution with breaking changes prominent. Tags/notes follow reviewed merges.

For each public release record PASS, FAIL or NOT_RUN for: scope/synthetic cases; changed contracts/migration; repeatable onboarding/content simulations; full-diff/privacy/metadata inspection; factual/quality review; independent review; and owner approval. A failed required gate blocks merge. A NOT_RUN test/review gate must be resolved or covered by the explicit owner exception above. Publication/content approval is separate from repository merge authorization.

State precisely what passed: manual open-book prompt simulation is not an automated runtime test; static structure is not behavior; independently reviewed outputs do not prove autonomous execution or market performance. Runtime/media enforcement is required only before those optional capabilities are enabled.

## Feedback, automation and maintenance

Generic improvements found through private use enter public PRs only as independently fictional requirements and examples. Identities, client outcomes, private links, drafts and metrics stay private.

CI may check complete-checkout structure, contracts, references, fixtures and maintenance safety. It must not automatically merge, infer owner approval or read private client data. Repository branch cleanup is separately authorized administration, not a framework agent capability. Its plan must protect current/main, confirm preserved work and no open dependencies, and use exact-head concurrency guards. Do not delete unique work or rewrite history to pass a gate.
