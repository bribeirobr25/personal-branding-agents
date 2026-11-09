# Integration capability matrix

Status: v0.1 research findings and design proposal. Last reviewed 2026-11-09. Provider behavior, subscription plans and API access can change.

## Separate capabilities, not just platforms
Evaluate each provider/account for: connection discovery, public profile reading, authenticated profile reading, historic post text and URLs, media, engagement metrics, publication/scheduling, history depth, access scope, pricing, and disconnection. **Connected != history accessible.** Unknown != unsupported; empty result != no posts.

| Platform | Initial candidate | Historical evidence | Limitations and validation |
| --- | --- | --- | --- |
| Instagram | Metricool | In an authorized pilot, returned historic feed captions, dates and links | Check reels/stories separately, time window, professional-account eligibility and metrics |
| Facebook | Metricool | Connected page recognized; no posts returned in broad query | Test older history, page vs personal profile, provider retention and permissions |
| TikTok | Metricool | Connected account recognized; no videos returned | Do not conclude account is empty without native verification |
| YouTube | Metricool | Channel recognized; returned zero video count in pilot | Validate published-video inventory, Shorts and account scopes |
| LinkedIn | Buffer | Imported historic text and timestamps in pilot | Determine coverage window, completeness, personal vs page accounts and metric access |
| X | Buffer for publishing; separate research route | Connected X account recognized, but historical query returned zero | Verify plan limits, historic import window and official X API/export alternatives |
| Substack | Buffer for managed posts; direct export for articles | Imported a subset of historic text and dates in pilot | Verify whether full article bodies and complete archive are available |

## Evidence and confidence
- **Observed via authorized integrations:** capabilities above, with all user identifiers and original post text excluded from this public repository.
- **Provider documentation requiring periodic recheck:** Buffer's X import may depend on plan and a limited lookback window. Do not hard-code a universal 30-day/100-post guarantee without current, directly verified official documentation.
- **Unverified:** historical limits for Buffer LinkedIn and Substack; Metricool Facebook older posts, Instagram reels/stories, TikTok and YouTube full archives.
- **Recommendation, not vendor endorsement:** prefer Metricool for supported Instagram/Facebook/TikTok/YouTube analytics and Buffer for supported LinkedIn/X/Substack publishing and available post data, but select based on proven capabilities for that account.

## Standard connector probe
1. Discover account identity and connection status without exposing credentials.
2. Request minimal read-only scope; record user consent where required.
3. Retrieve a bounded sample and verify earliest/latest timestamps, post count, text, URLs and metrics.
4. Compare with an owner-confirmed known post (especially one predating connection); record gaps and possible causes.
5. Classify each capability: verified, partial, unavailable, untested, or error, with date and provenance.
6. Offer export, official API or conversation fallback; never require a paid integration to start onboarding.
7. Keep actual account inventory, post text, private URLs and raw API outputs in a separate private workspace.

## Research vs analytics vs publishing
Research adapters fetch evidence. Analytics adapters measure outcomes. Publishing adapters schedule/send only after explicit approval. A vendor may support one, two or all three; permissions must be verified independently.

## Maintenance
Recheck provider limitations on connection, plan change, permission change, and at least before every release that makes provider recommendations. Record documentation URL, checked date, plan and scope in a private or sanitized evidence log.
