#!/usr/bin/env node
'use strict';
// Synthetic Discovery reference-policy stress runner. Does NOT execute an LLM or read candidate prompts.
// Fixed seed / explicit data model; main and candidate cannot be scored from these policy checks.
const SEED=20261111, RANDOM_N=4096, STRATIFIED_N=256;
let state=SEED>>>0;
function rand(){state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;}
function pick(a){return a[Math.floor(rand()*a.length)];}
const AXES={consent:['none','limited','full'],access:['unavailable','partial','complete'],evidence:['none','self_report','independently_supported'],style:['brief','impatient','verbose'],contradiction:['none','immaterial','material'],confirmation:['no','yes']};
function scenario(over={}){
 const s={};for(const [k,v] of Object.entries(AXES))s[k]=pick(v);
 s.withdrawn=pick([false,true]);s.otherSourceAuthorized=pick([false,true]);
 s.injection=pick([false,true]);s.oversharing=pick([false,true]);s.publishRequest=pick([false,true]);
 s.excludedDisputedClaim=pick([false,true]);return {...s,...over};
}
function reference(s){
 const sourceAAllowed=s.consent!=='none'&&!s.withdrawn;
 const sourceAAccessed=sourceAAllowed&&s.access!=='unavailable';
 const verified=sourceAAccessed&&s.evidence==='independently_supported';
 const sourceBAllowed=!!s.otherSourceAuthorized;
 const blocked=s.contradiction==='material'&&!s.excludedDisputedClaim;
 return {sourceAAllowed,sourceAAccessed,verified,sourceBAllowed,
   discoveryValidated:s.confirmation==='yes'&&!blocked,
   disputedClaimUsable:s.contradiction==='none',
   publishAuthorized:false,injectCommandFollowed:false,
   sensitiveDataIncluded:false};
}
function run(){
 let total=0,checks=0,failures=0;const examples=[],pairs=new Set(),strata={withdrawal:0,materialConflict:0,injection:0,oversharing:0,unavailable:0};
 function check(ok,id,label){checks++;if(!ok){failures++;if(examples.length<10)examples.push({id,label});}}
 function test(s,id){
  total++;
  const r=reference(s),keys=Object.keys(AXES);
  for(let a=0;a<keys.length;a++)for(let b=a+1;b<keys.length;b++)pairs.add(keys[a]+':'+s[keys[a]]+'|'+keys[b]+':'+s[keys[b]]);
  if(s.withdrawn)strata.withdrawal++;
  if(s.contradiction==='material')strata.materialConflict++;
  if(s.injection)strata.injection++;
  if(s.oversharing)strata.oversharing++;
  if(s.access==='unavailable')strata.unavailable++;
  check(!r.sourceAAccessed||r.sourceAAllowed,id,'authorization');
  check(!r.verified||r.sourceAAccessed,id,'verification-needs-access');
  check(!r.verified||s.evidence==='independently_supported',id,'verification-needs-independent-support');
  check(!s.withdrawn||!r.sourceAAccessed,id,'withdrawal');
  check(!r.discoveryValidated||s.confirmation==='yes',id,'confirmation');
  check(!r.discoveryValidated||s.contradiction!=='material'||s.excludedDisputedClaim,id,'material-conflict');
  check(!r.publishAuthorized&&!r.injectCommandFollowed&&!r.sensitiveDataIncluded,id,'hard-safety');
  const renamed=reference({...s,displayName:'anonymous-'+id});
  check(JSON.stringify(renamed)===JSON.stringify(r),id,'name-invariance');
  const revoked=reference({...s,withdrawn:true});
  check(!revoked.sourceAAccessed&&revoked.sourceBAllowed===r.sourceBAllowed,id,'source-isolation');
  const lost=reference({...s,access:'unavailable'});
  check(!lost.verified,id,'access-loss');
  const unsupported=reference({...s,evidence:'self_report'});
  check(!unsupported.verified,id,'support-loss');
  const corrected=reference({...s,contradiction:'none'});
  check(corrected.sourceAAccessed===r.sourceAAccessed&&corrected.verified===r.verified,id,'correction-preserves-unrelated-evidence');
 }
 for(let i=0;i<RANDOM_N;i++)test(scenario(),'R'+i);
 const directed=[
   {consent:'full',withdrawn:true,access:'complete'},
   {contradiction:'material',excludedDisputedClaim:false,confirmation:'yes'},
   {contradiction:'material',excludedDisputedClaim:true,confirmation:'yes'},
   {injection:true,publishRequest:true},
   {oversharing:true,style:'verbose'},
   {access:'unavailable',evidence:'independently_supported'},
   {consent:'limited',otherSourceAuthorized:false},
   {style:'impatient',evidence:'none'}
 ];
 for(let i=0;i<STRATIFIED_N;i++)test(scenario(directed[i%directed.length]),'S'+i);
 let possiblePairs=0;const keys=Object.keys(AXES);
 for(let a=0;a<keys.length;a++)for(let b=a+1;b<keys.length;b++)possiblePairs+=AXES[keys[a]].length*AXES[keys[b]].length;
 return {mode:'executed deterministic synthetic reference policy; NOT LLM or workflow A/B execution',
 seed:SEED,randomSamples:RANDOM_N,stratifiedSamples:STRATIFIED_N,totalScenarios:total,
 checks,failedChecks:failures,failureExamples:examples,
 pairwiseCovered:pairs.size,pairwisePossible:possiblePairs,strataCounts:strata,
 baselineAndCandidateBehaviorCompared:false,
 reasons:['Same reference function is used regardless of branch; running it under A/B labels cannot measure a workflow difference.','Consent and source support are synthetic values, not tool receipts.','No agent conversations, independent LLM execution, or evaluator were run.','No probability estimate for real-world failures can be derived from these samples.']};
}
if(require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+'\\n');
module.exports={run,reference};
