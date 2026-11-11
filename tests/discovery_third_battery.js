'use strict';
const seed=20261111; let state=seed>>>0;
function next(){state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;}
function bit(){return next()<0.5;}
function policy(input){
 const sources={};
 for(const [name,x] of Object.entries(input.sources)){
  const authorized=x.allowed&&!x.withdrawn;
  const accessed=authorized&&x.available;
  const extracted=accessed&&x.claim;
  const verified=extracted&&x.support;
  sources[name]={authorized,accessed,extracted,verified};
 }
 return {sources,validated:input.confirmed&&(!input.contradictionMaterial||input.disputedClaimExcluded),
 disputedClaimPublishable:false,publicationAuthorized:false};
}
const names=['cv','linkedin','portfolio'],iterations=4096;
let checks=0,failed=0,validated=0;const firstFailures=[];
function assert(cond,i,label){checks++;if(!cond){failed++;if(firstFailures.length<12)firstFailures.push({i,label});}}
for(let i=0;i<iterations;i++){
 const sources={};for(const n of names)sources[n]={allowed:bit(),withdrawn:bit(),available:bit(),claim:bit(),support:bit()};
 const input={sources,confirmed:bit(),contradictionMaterial:bit(),disputedClaimExcluded:bit()};
 const out=policy(input);if(out.validated)validated++;
 for(const n of names){
  const x=sources[n],y=out.sources[n];
  assert(!y.accessed||(x.allowed&&!x.withdrawn&&x.available),i,n+':access');
  assert(!y.extracted||y.accessed,i,n+':extraction');
  assert(!y.verified||(y.extracted&&x.support),i,n+':verification');
  const rev=structuredClone(input);rev.sources[n].withdrawn=true;const revoked=policy(rev);
  assert(!revoked.sources[n].accessed,i,n+':revocation');
  assert(names.every(other=>other===n||JSON.stringify(revoked.sources[other])===JSON.stringify(out.sources[other])),i,n+':isolation');
  const unsupported=structuredClone(input);unsupported.sources[n].support=false;
  assert(!policy(unsupported).sources[n].verified,i,n+':support-removal');
 }
 const renamed=structuredClone(input);renamed.displayName='fictional-'+i;
 assert(JSON.stringify(policy(renamed))===JSON.stringify(out),i,'name-invariance');
 assert(!out.validated||input.confirmed,i,'explicit-confirmation');
 assert(!out.validated||!input.contradictionMaterial||input.disputedClaimExcluded,i,'material-contradiction');
 assert(!out.disputedClaimPublishable&&!out.publicationAuthorized,i,'no-publish');
}
console.log(JSON.stringify({date:'2026-11-11',mode:'executed seeded deterministic synthetic policy checks (NOT LLM conversation)',seed,randomSamples:iterations,assertions:checks,failedAssertions:failed,firstFailures,syntheticValidatedStates:validated,limitations:['Shared implementation/assertion assumptions; not an independent oracle.','Synthetic booleans do not implement real granular authorizations or evidence verification.','No LLM calls, real connectors, actual source access, independent evaluator, or end-to-end conversations.','Random sampling is not a population performance estimate.']},null,2));
