# Codex CLI subscription-only addendum

This adds a transport to the [live protocol](discovery-live-ab-protocol-2026-11-12.md).
It changes neither frozen A/B prompts nor the original adverse evidence. The owner
requested a separate 12-call pilot (R01/R13/R16, one repetition, two arms/two turns)
followed, only after successful isolation, by the original 108-call priority battery.
That instruction supersedes the earlier optional 36-call setup pilot. No paid calls,
credit redemption, API-key fallback, merge or main changes are authorized.

## Preregistered implementation and settings

`discovery_codex_cli.py` uses installed `codex-cli 0.145.0`, model `gpt-6.1-sol`,
low reasoning effort, ordinary/default service tier, provider sampling defaults,
one fresh process per turn and no retries. The model is a service alias, not a
guaranteed immutable model snapshot. Returned model/version and usage are retained.
The ChatGPT Codex transport has no validated output-token cap in this adapter;
the API adapter's 2048-token setting is not falsely claimed to apply. Timeout is
180 seconds for network reads, 210 seconds for the CLI. Output length is not scored
as quality. Both arms receive identical execution settings.

The six documents and existing HOST disclosure are loaded with the existing
frozen loader: three treatment documents from each arm, three shared documents
from A. Every input and full response is saved. U2 is constructed only after A1
has actually returned for that same case/repetition/arm. Future user turns,
expected answers, review rubric, other-arm history and real profiles are excluded.

## Isolation boundary, tested rather than inferred from cwd

An offline real-CLI capture established that disabling features alone still adds
environment context and tools. The adapter therefore uses a loopback wire broker:

1. CLI receives only the frozen instructions and serialized bounded transcript.
   Fresh home/config, allowlisted environment, no global/project instructions,
   skills, plugins, connectors, shell, browser or memory; no resumed thread.
2. An outer macOS Seatbelt policy denies content reads/writes under `/Users`,
   other temporary directories, volumes and this repository. Only the per-call
   scratch directory is excepted. File metadata and operating-system paths remain
   readable; this is a scoped host-content policy, not a general VM boundary.
   CLI outbound networking is restricted to the one localhost broker port.
   Actual positive/negative file reads run before every generation.
3. The broker authenticates a random per-call localhost capability, checks the
   exact CLI instructions/envelope, and constructs a fresh outbound payload from
   its allowlist. CLI-added developer/environment messages, tools, session/cache
   IDs and client metadata are not forwarded. Only the frozen instructions and
   current same-arm transcript reach the model. Outbound tools are empty.
4. OAuth remains in the trusted controller, outside the generation process.
   Codex CLI app-server performs account/auth/limit reads without starting a model
   turn. The broker uses that verified ChatGPT authentication only at the fixed
   native Codex ChatGPT endpoint, never the paid API endpoint. The custom-provider
   CLI did not attach ChatGPT OAuth in offline qualification; forwarding OAuth
   directly from its headers was consequently rejected as an implementation path.
5. The broker accepts one request, denies redirects and never retries. It buffers
   and validates the complete provider SSE stream before the CLI receives it.
   Tool/refusal/incomplete outputs stop the run; no generated tool can execute.
   CLI final text must match the actual provider final text exactly.

The trusted controller has the fixtures and credentials; it is outside the model
boundary. There is no claim of defense against a compromised OS, Python runtime,
CLI binary or malicious administrator. Separate directories alone are not evidence.
No production memory, real source access, independent specialist or tool-enabled
source-revocation security is measured. The offline sentinels are transport doubles,
never behavioral answers or part of the live battery.

## Included usage and private receipts

Before each call, require ChatGPT auth on a recognized personal included plan,
known available quota below 90% used, no reached limit, no spend-control block,
`hasCredits=false`, `unlimited=false`, and balance zero. Unknown, stale or positive
credit states fail closed. No account mutations, purchases, reset redemptions,
automatic retries or paid fallback exist. These checks observe current account
state; they are not an atomic provider billing lock or a dollar invoice. A concurrent
account change is outside the adapter's control. A limit stops the run rather than
authorizing credits. The initial read-only check met these conditions.

Full account receipts remain in a private directory, mode 0700, outside Git; they
contain account identities and private quota analytics prohibited by AGENTS.md.
Public receipts contain the gate predicates and a hash of the private raw receipt.
OAuth/access/refresh tokens and localhost capabilities are never logged. All model
inputs, outputs, SSE, CLI stdout/stderr, configs, versions/hashes, safe receipt
headers, errors, completed/unknown counts and manifests are retained. Early offline
qualification artifacts that contain host usernames are privately preserved and
explicitly redacted in their public copies; model text is never edited.

## Promotion and interpretation

The pilot is stored separately. The 108-call command requires the successful
12-call pilot, matching adapter/binary hashes and an intact artifact manifest.
Any failed/unknown attempt is preserved and not silently retried or resumed.
Transport/isolation success is not a behavioral PASS. The original hard gates,
editorial rubric, fixed-U2 mismatch caveat and independent-review limitations remain.
No judge calls are included, and no A/B winner or merge decision follows from
successful generation alone. HOLD remains until the required review is completed.

Commands (private path must be outside Git):

```sh
python3 -m unittest discover -s tests -p 'test_discovery_codex_cli.py' -v
python3 tests/discovery_codex_qualify.py --out /tmp/new-offline-qualification
python3 tests/discovery_codex_cli.py --stage pilot --live --out /tmp/new-pilot --private-out /tmp/private-pilot-receipts
python3 tests/discovery_codex_cli.py --stage battery --live --pilot /tmp/new-pilot --out /tmp/new-battery --private-out /tmp/private-battery-receipts
```

Official references consulted: [authentication](https://learn.chatgpt.com/docs/auth?surface=cli),
[pricing/included usage](https://learn.chatgpt.com/docs/pricing),
[app-server account methods](https://learn.chatgpt.com/docs/app-server), and
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
The installed CLI help and generated schema, plus actual offline captures, govern
version-specific behavior; current documentation may describe newer versions.

## Resumption clarification (2026-11-12)

The [new-pilot preregistration](discovery-codex-resumption-protocol-2026-11-12.md)
adds early network receipts and an explicit behavior gate without changing the
model or existing limits. For the current executor, the battery command above
also requires `--pilot-review /path/to/manifest-bound-review.json`. A complete
transport run alone is no longer sufficient: all twelve hard-gate reviews and
R16 name/language checks must PASS. A failed or missing review blocks execution.
