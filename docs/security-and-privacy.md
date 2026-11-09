# Security & privacy policy for the public framework

**Design goal:** no real client information in this public codebase.

## Never commit
- Real client dossiers, resumes, contact information, private social account data or unpublished posts.
- Access tokens, passwords, API keys, private keys, connection strings or environment files.
- Proprietary employer/client documentation, unreleased product details, investor conversations, contracts or private KPIs.
- Raw prompts/transcripts or model outputs containing personal information.

## Release checklist
1. Check newly added files, file names, metadata and links.
2. Review the **entire diff**, not just the README or latest file.
3. Look for emails, phone numbers, unique handles, private URLs, credentials and identifying combinations.
4. Ensure test data are invented, not de-identified real cases.
5. Review commit history: deleting a secret in a later commit does **not** remove it from public Git history.
6. Verify ownership/permission to publish source, images and quotes.
7. Do not include private repository links, internal paths, access tokens or private issue references.
8. Require an independent reviewer and owner approval for public release.

## Handling incidents
If private or secret material is exposed, stop publishing; revoke/rotate affected credentials where applicable; restrict access and follow GitHub's guidance for sensitive data in repository history. A subsequent deletion alone does not guarantee removal.

## AI provider considerations
Client data sent to third-party models may be processed by those providers. Users should review their providers' retention and privacy settings and avoid sharing restricted data.

## Boundaries
A private repository is an access control, not absolute confidentiality. Review collaborators, integrations, workflows and publishing actions. This public repository does not need access to real client materials to run its examples.
