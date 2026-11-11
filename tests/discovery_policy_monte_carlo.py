#!/usr/bin/env python3
"""Discovery authorization/evidence policy reference checks, not an LLM-agent test.

Run: python3 tests/discovery_policy_monte_carlo.py
No accounts, connector access, models or network calls are used.
"""
import json
import random

SEED = 20261111
N = 2400
SOURCES = ("linkedin", "instagram", "cv")
rng = random.Random(SEED)

def evaluate(s):
    """Return per-source permission, retrieval, extracted claims and verification.

    This is a synthetic reference model. 'Verified' requires independent support
    in the fixture; an accessible post by itself merely supports 'user_reported'.
    """
    result = {}
    for name in SOURCES:
        src = s[name]
        allowed = bool(src["allowed"]) and not bool(src["withdrawn"])
        accessed = allowed and bool(src["available"])
        extracted = accessed and bool(src["contains_claim"])
        verified = extracted and bool(src["independent_support"])
        result[name] = {
            "authorized": allowed,
            "accessed": accessed,
            "claim_extracted": extracted,
            "claim_verified": verified,
            "evidence_status": ("verified" if verified else
                                "user_reported" if extracted else "unknown"),
        }
    return result

def check(s, result):
    for name in SOURCES:
        x = s[name]
        y = result[name]
        assert not y["accessed"] or y["authorized"]
        assert not y["accessed"] or x["available"]
        assert not y["claim_extracted"] or y["accessed"]
        assert not y["claim_verified"] or (y["claim_extracted"] and x["independent_support"])
        assert y["evidence_status"] == ("verified" if y["claim_verified"] else
            "user_reported" if y["claim_extracted"] else "unknown")
        if x["withdrawn"]:
            assert not y["accessed"]
        if not x["allowed"]:
            assert not y["accessed"]
        # Losing access cannot leave an externally verified claim in this run.
        without_access = {k: dict(v) for k,v in s.items()}
        without_access[name]["available"] = False
        assert not evaluate(without_access)[name]["claim_verified"]
        # Permission for one source cannot enable another.
        others = {k: dict(v) for k,v in s.items()}
        others[name]["allowed"] = not others[name]["allowed"]
        assert all(evaluate(others)[other] == result[other]
                   for other in SOURCES if other != name)

def source(allowed, available, contains_claim=True, independent_support=False, withdrawn=False):
    return dict(allowed=allowed, available=available,
                contains_claim=contains_claim,
                independent_support=independent_support, withdrawn=withdrawn)

# Directed functional cases, before randomized sampling.
fixed = {
    "linkedin_yes_instagram_no": {
        "linkedin": source(True, True), "instagram": source(False, True),
        "cv": source(False, False)},
    "read_post_not_verified": {
        "linkedin": source(True, True, True, False),
        "instagram": source(False, False), "cv": source(False, False)},
    "independent_evidence": {
        "linkedin": source(True, True, True, True),
        "instagram": source(False, False), "cv": source(False, False)},
    "withdrawn_consent": {
        "linkedin": source(True, True, True, True, True),
        "instagram": source(False, False), "cv": source(False, False)},
    "no_access": {
        "linkedin": source(True, False, True, True),
        "instagram": source(False, False), "cv": source(False, False)},
}
for name, scenario in fixed.items():
    r = evaluate(scenario)
    check(scenario, r)
    if name == "linkedin_yes_instagram_no":
        assert r["linkedin"]["accessed"] and not r["instagram"]["accessed"]
    if name == "read_post_not_verified":
        assert r["linkedin"]["claim_extracted"] and not r["linkedin"]["claim_verified"]
    if name == "independent_evidence":
        assert r["linkedin"]["claim_verified"]
    if name == "withdrawn_consent":
        assert not r["linkedin"]["accessed"]
    if name == "no_access":
        assert not r["linkedin"]["claim_verified"]

failures=[]
for i in range(N):
    s={name: source(*[rng.choice([False,True]) for _ in range(5)])
       for name in SOURCES}
    try:
        check(s, evaluate(s))
    except AssertionError:
        failures.append(i)

out = {
    "mode":"synthetic rule-policy test, NOT LLM conversations",
    "seed":SEED, "random_samples":N, "directed_cases":len(fixed),
    "source_permissions":"per-source, with withdrawal",
    "evidence_chain":"authorization -> access -> extraction -> independent support",
    "failures":len(failures), "sample_failure_indices":failures[:10],
    "limitations":[
      "The policy implementation and assertions share assumptions and are not an independent evaluator.",
      "Source-level authorization is represented only by booleans; real grants, scopes and revocation must be checked against tool logs.",
      "Independent_support is a synthetic fixture flag; real evidence evaluation requires separate verified sources.",
      "No LLM agents, social networks, or independent behavioral simulations were run."
    ]
}
print(json.dumps(out, ensure_ascii=False, indent=2))
