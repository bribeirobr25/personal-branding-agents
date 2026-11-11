#!/usr/bin/env node
// Static text-coverage comparison, NOT agent execution or model quality evaluation.
// Run from a full local clone with both frozen commits available:
// node tests/discovery_ab_static_coverage.js
const {execFileSync}=require('node:child_process');
const REF={main:'0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92',candidate:'b3e607c557ab26b764c7e0ef7f2e6a27405718d1'};
const PATHS=['agents/orchestrator.md','agents/researcher.md','workflows/onboarding.md'];
const RULES=[
['explicit-user-confirmation',/explicit(ly)? (user )?confirm|explicit profile confirmation|person explicitly confirms/i],
['factual-boundary',/confirmation (does not|is not) independent|not automatically independent verification/i],
['source-granular-permission',/per.source|source.level permission|source-specific grant/i],
['withdrawal-stops-access',/withdraw(n|al).*?(stop|prevent|new access)|stop.*?(new )?access.*?withdraw/i],
['access-extraction-verification-separated',/authorization.*access.*extraction.*verification|access.*extraction.*independent/i],
['claim-scoped-contradiction',/claim.level block|claim.scoped contradiction|disputed claim/i],
['bounded-discovery-readiness',/validated_for_strategy|bounded current profile|two.part completion gate/i],
['contextual-initiative',/one.*(grounded|optional).*?(insight|observation|next step)|useful initiative/i],
['targeted-correction-loop',/research only affected claims|only affected research|correction loop|process only changed or contradictory/i],
['no-automatic-publication',/no automatic.*publish|publish only with explicit human approval|no.*automatic.*publishing/i]
];
const texts={};for(const [side,sha] of Object.entries(REF)){texts[side]=PATHS.map(p=>execFileSync('git',['show',sha+':'+p],{encoding:'utf8'}));}
const results=RULES.map(([criterion,re])=>{const row={criterion};for(const side of Object.keys(REF)){const i=texts[side].findIndex(t=>re.test(t));row[side]={patternMatched:i!==-1,sourceFile:i>=0?PATHS[i]:null};}return row});
console.log(JSON.stringify({type:'static textual regex audit, NOT an agent test',refs:REF,results,count:Object.fromEntries(Object.keys(REF).map(s=>[s,results.filter(r=>r[s].patternMatched).length])),warning:'No pattern match does not mean the behavior is absent; present wording may express it differently. A match does not mean behavior works.'},null,2));
