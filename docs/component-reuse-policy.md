# Learning, reuse and independent development

Project policy, not a legal opinion. Apply to the specific component, version, activity and distribution mode. Architecture and scope decisions must not be presented as universal legal prohibitions.

## Decision principles

Learn concepts through lawful access; reuse code, skill text and templates when the actual license permits and its conditions are fulfilled; implement independently where appropriate. Do not rebuild a permitted component merely to call it original. Conversely, renaming or superficially rewriting restricted expression with an LLM does not establish independence.

Functional similarity alone is not our criterion for prohibited copying. Code, documentation, media, model weights, wrapper, runtime and service access can have different rights. A wrapper's license does not grant runtime rights; a runtime's terms do not automatically revoke independent third-party grants. A public repository or free plan is not a license for every included asset.

Noncommercial use is not a blanket exemption. Private execution, distribution of free code, hosted access and work for a business/client are different activities. Evaluate applicable terms and mandatory legal rights rather than assuming every clause is enforceable or every learning activity exempt. Escalate uncertainty only for the affected activity; other independent work can continue.

## Procedure

Record a ReuseDecision: component_id, source_ref/source_revision, material_scope, access_basis, use_mode, reuse_route, legal_basis_and_limitations, obligations, architectural_decision, affected_files, reviewer, evidence, status and reevaluation_trigger. Retain the actual rights basis, notices, dependency/asset boundaries, technical assessment and product-scope reason.

Keep route and process status separate. Routes include conceptual learning, licensed reuse, adaptation, independent implementation, runtime/API use and interoperability. Process status is candidate, cleared_for_stated_use, needs_clarification, out_of_scope or rejected_for_stated_use. A cleared component is cleared only for the stated use, not every future deployment. State legal uncertainty separately from capability, cost, safety or priority. For licensed reuse preserve required attribution and mark changes as required; do not claim authorship of the reused portion.

For independent development, record sources and requirements, what was reused under license, what was newly written and how it was tested. A formal clean-room process is not asserted unless it actually occurred, nor required as a universal label for every independent implementation. Interoperability needs activity-specific analysis, not an automatic ban on all format converters or permission for unrestricted decompilation.

## Illustrative legal background

German software law distinguishes protected expression from underlying ideas/principles (§69a(2)); authorized users may observe/study/test within the conditions in §69d(3). Section 69g preserves other legal disciplines and addresses contradictory contract clauses. These provisions are not automatically extended to every document, online service or asset, and this policy does not decide a particular supplier dispute. Sources: [§69a](https://www.gesetze-im-internet.de/urhg/__69a.html), [§69d](https://www.gesetze-im-internet.de/urhg/__69d.html), [§69g](https://www.gesetze-im-internet.de/urhg/__69g.html).

The [MIT text](https://opensource.org/license/mit) grants broad reuse rights subject to its conditions; third-party rights remain separate. For other licenses read the actual applicable version and deployment terms. Do not treat copyleft obligations as a universal prohibition or impose a supplier's terms on unrelated independently licensed material.

## Practical boundary

Open-source-first is an architectural preference, not a mandate to replicate entire products. Keep essential data/contracts portable; services can be optional adapters. Evaluate cost per approved artifact including maintenance, retries and human review. No dependency, paid call or license acceptance is authorized by this document. Use [the template](../templates/reuse-decision.json) and evaluation cases L01-L08.
