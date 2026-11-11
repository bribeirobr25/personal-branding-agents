#!/usr/bin/env python3
"""Seeded policy-transition Monte Carlo for Discovery; NOT an LLM behavior test."""
import json, random, sys
SEED = 20261111
N = 2400
rng = random.Random(SEED)
dims = {
  "recognition": ["unknown","established","prominent"],
  "evidence": ["none","self_report","accessible","contradictory"],
  "consent": ["allowed","limited","refused","withdrawn"],
  "style": ["brief","verbose","impatient","corrective"],
  "source": ["available","inaccessible"],
  "confirmation": ["yes","no"],
  "material_blocker": [False,True],
}
def policy(x):
  access = x["consent"] in ("allowed","limited") and x["source"]=="available"
  external_verified = access and x["evidence"]=="accessible"
  needs_correction = x["evidence"]=="contradictory"
  blockers = x["material_blocker"] or needs_correction
  validated = x["confirmation"]=="yes" and not blockers
  return {"access":access,"external_verified":external_verified,"validated":validated,
          "retained_unrelated":True,"publication_authorized":False,
          "has_provisional_feedback":True}
def assert_invariants(x,y):
  assert not y["access"] or x["consent"] in ("allowed","limited")
  assert not y["external_verified"] or (y["access"] and x["evidence"]=="accessible")
  assert not y["validated"] or (x["confirmation"]=="yes" and not x["material_blocker"] and x["evidence"]!="contradictory")
  assert not y["publication_authorized"]
  assert y["retained_unrelated"] and y["has_provisional_feedback"]
  no_access = dict(x,source="inaccessible")
  assert not policy(no_access)["external_verified"]
  renamed = dict(x,display_name="Synthetic Different Name")
  assert policy(renamed)==y
  no_consent = dict(x,consent="withdrawn")
  assert not policy(no_consent)["access"]
  not_confirmed = dict(x,confirmation="no")
  assert not policy(not_confirmed)["validated"]
  unrelated_correction = dict(x,unrelated_claim_corrected=True)
  assert policy(unrelated_correction)["retained_unrelated"]
samples=[]
issues=[]
counts={"access":0,"external_verified":0,"validated":0,"blocked":0,"failures":0}
for i in range(N):
  x={k:rng.choice(v) for k,v in dims.items()}
  y=policy(x)
  try: assert_invariants(x,y)
  except AssertionError: counts["failures"]+=1;issues.append({"run":i,"input":x,"output":y})
  for k in ("access","external_verified","validated"):counts[k]+=int(y[k])
  counts["blocked"]+=int(not y["validated"])
  if i<12:samples.append({"run":i,"input":x,"output":y})
report={
  "mode":"seeded rule-model Monte Carlo; NOT agent conversations, NOT LLM run",
  "seed":SEED,"runs":N,"dimensions":{k:v for k,v in dims.items()},
  "counts":counts,"checks_per_run":10,"examples_first_12":samples,
  "failure_examples":issues[:20],
  "interpretation":"No invariant failures means this tiny reference policy is internally consistent on sampled combinations; it does not demonstrate that the prompt-first framework follows the policy.",
  "selection_bias":"Synthetic independent uniform dimensions overrepresent implausible combinations; estimates are not user-population rates."
}
json.dump(report,sys.stdout,indent=2,ensure_ascii=False)
print()
