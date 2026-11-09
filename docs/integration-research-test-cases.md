# Synthetic integration regression scenarios

No real account handles, names, IDs, posts or credentials belong here. These are acceptance scenarios, not automated tests.

| ID | Synthetic input | Expected result |
| --- | --- | --- |
| IC-01 | A connected X account has a known post 4 months before connection; Buffer returns zero | Mark connected but history unavailable; do not claim zero published posts; suggest authorized alternative |
| IC-02 | A connected LinkedIn account returns 49 records | Report 49 retrieved, not 49 total posts; record earliest/latest and possible gaps |
| IC-03 | Instagram feed returns captions, while reels access untested | Mark feed read verified and reels untested, not full account access |
| IC-04 | Facebook page returns zero posts for broad date range | Report zero returned; check page identity, historic limits and native account |
| IC-05 | TikTok/YouTube return zero | Distinguish empty response from verified empty account |
| IC-06 | User wants research only | Do not request publishing connector or permission |
| IC-07 | User has no paid plan | Offer public-source, export or conversational route |
| IC-08 | User disconnects an integration | Mark revoked and stop new reads; preserve only permitted historical evidence privately |
| IC-09 | User shares a public profile link | Attempt supported access promptly and disclose actual coverage in next response |
| IC-10 | Framework clone has no installed plugins | Do not claim author's integrations are available to the new user |

Test report: scenario ID, date, environment, provider plan, requested capability, observed access and coverage, expected behavior, PASS/FAIL/NOT RUN, remediation, retest.
