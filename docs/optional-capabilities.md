# Optional capabilities and build/reuse decisions

The shipped method is manual/prompt-first. This page describes future choices, not working integrations or a claim that named hosts are available.

| Need | Initial route | Adoption evidence |
| --- | --- | --- |
| Audience research | Conversation and authorized supplied sources | Coverage, quality, rights and scope; no invasive enrichment |
| Web discovery/extraction | Manual URLs/exports | Search is not crawling; authorized sources, freshness and failure behavior |
| Creative references | Small local index | Exportability, rights, useful retrieval and current voice |
| Text generation | Host chosen by user | Task quality, privacy, language, context and cost under a common contract |
| Local inference | Candidate only | Runtime and weight licenses, revision/quantization/hardware, offline test and limitations |
| Motion/editing | Optional experiment | Own requirements, actual final render, rights, readability and reproducibility; no assumed feature parity |
| Publication | Manual exact approved version | Destination/action authorization and real receipt |
| Metrics | Authorized exports | Definitions, window, missingness, comparability and useful decision |
| Orchestration | Sequential role prompting | Independent workers, isolation, persistence and failures must be demonstrated before claiming automation |

Manual, local and hybrid modes share records. A local test must record model/configuration and demonstrate no network call; inadequate capability means stop or offer an authorized alternative, not silently send private context to a cloud provider. No specific model is declared sufficient without testing.

Reuse an appropriate permitted component before building a replacement. Adapt when changes are bounded. Build when a material requirement or unacceptable dependency remains. Defer when no observed bottleneck justifies the operational burden. Costs include implementation, compute, inference, media, review, retries, maintenance and exit, not just per-generation price.

No warehouse, full marketing cloud or multi-agent runtime is required to deliver one useful case. A text pilot must not be blocked by optional video production. Apply [reuse policy](component-reuse-policy.md), [security](security-and-privacy.md) and release governance before activation.
