#!/usr/bin/env node
'use strict';
/**
 * Deterministic staged Discovery workflow surrogate, NOT LLM / live agent execution.
 * Consumes frozen seeded fixture JSON on stdin, emits full decision/event trace.
 * A/B rule differences are explicitly authored interpretations of the two prompt versions.
 * Invocation: node tests/discovery_workflow_ab_emulator.js < fixtures.json > trace.json
 */
const fs=require('node:fs');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
if(!input.fixtures||!input.arms||input.arms.length!==2)throw Error('invalid fixtures');
const B='B_candidate';
const isB=arm=>arm.name===B;
function synthesize(f,arm){
 const b=isB(arm),x=f.attributes,id=f.id,events=[],sources=x.source==='two_sources'?['cv','profile']:x.source==='none'?[]:[x.source];
 const permission=(name)=>x.consent==='granted'||(x.consent==='limited'&&name==='cv')||(x.consent==='revoked'&&name==='cv');
 const noExternal=x.source==='inaccessible_url'||x.source==='none';
 const accessible=(name)=>permission(name)&&!noExternal&&name!=='public_profile'&&name!=='profile';
 const retrieved=sources.filter(accessible);
 const denied=sources.filter(n=>!permission(n));
 const inaccessible=sources.filter(n=>permission(n)&&!accessible(n));
 const excluded=x.material_conflict&&x.correction==='metric';
 const blocking=x.material_conflict&&!excluded;
 const validated=!!x.ready_to_confirm&&!blocking;
 const userClaim=x.evidence==='contradictory'?'conflicting achievement':x.evidence==='outdated'?'possibly outdated role':'professional contribution';
 const claims=retrieved.map(n=>({source:n,claim:userClaim,provenance:x.evidence==='supported_fixture'?'synthetic user-supplied excerpt':'self-report',independent_verified:false}));
 const event=(step,actor,output,receipt=null,gate=null)=>events.push({step,actor,input:step.startsWith('user_')?f.user_script[step==='user_introduce_and_goal'?'opening':step==='user_sources_and_permissions'?'optional_source':'followup']:null,output,receipt,gate});
 event('orchestrator_open','orchestrator',b?'I can help clarify your professional direction. How would you like to begin?':'I can help clarify your professional history and options. How should I address you, and what would you like to achieve?');
 event('user_introduce_and_goal','user',f.user_script.opening);
 event('orchestrator_reflect_and_optional_sources','orchestrator',b?'We can work from what you choose to share. A CV or profile is optional.':'I understand you want to explore opportunities. You may share a CV or profiles, but none are required.');
 event('user_sources_and_permissions','user',f.user_script.optional_source);
 event('orchestrator_delegate_researcher','orchestrator',b?'Research only currently authorized sources; report coverage and evidence separately.':'Research authorized accessible material; report findings and limitations.',{requested:sources,allowed:sources.filter(permission),denied,execution:'emulator, no tools'});
 event('researcher_authorization_receipt','researcher',b?'Permission checked for each synthetic source and action.':'Only authorized synthetic material is in scope.',{requested:sources,authorized:sources.filter(permission),denied,revoked:x.consent==='revoked',real_access:false});
 event('researcher_access_and_evidence_receipt','researcher',retrieved.length?'Synthetic excerpts supplied in the fixture; claims remain attributed, not independently proven.':'No independently retrievable source is available in this fixture.',{synthetic_retrieved:retrieved,inaccessible,denied,claims,external_access:false,independent_verification:false,injection_is_untrusted:!!x.prompt_injection});
 let summary='You report a '+x.persona.replaceAll('_',' ')+' background. '+(claims.length?'Some synthetic source material is available, but no achievement is independently verified.':'I have no independently accessed supporting source.');
 if(x.evidence==='contradictory')summary+=' Claims conflict and cannot be stated as verified.';
 if(b&&x.style==='impatient')summary+=' A useful next step is to identify one concrete contribution you can support.';
 event('orchestrator_provisional_summary','orchestrator',summary+' Is that a fair initial account?',{evidence_class:x.evidence,source_count:retrieved.length,source_limitations:true});
 event('user_correct_or_confirm','user',f.user_script.followup);
 const correctionNeeded=x.correction!=='none',mustResearch=correctionNeeded&&retrieved.length>0&&x.consent!=='revoked';
 event('orchestrator_targeted_research_or_no_access','orchestrator',correctionNeeded?(b?'Recheck only the affected '+x.correction+' claim; keep other evidence unchanged.':'Review the correction and update the draft profile.'):(b?'No new research is needed for unchanged facts.':'No additional authorized research requested.'),{changed_claim:x.correction,requested_new_research:mustResearch,source_access_repeated:false});
 event('researcher_followup_receipt_or_not_applicable','researcher',mustResearch?'Synthetic source already supplied; affected claim considered without new network access.':'N/A: no accessible or permitted additional source.',{rechecked_claim:mustResearch?x.correction:null,actual_tool_access:false,unrelated_evidence_preserved:true});
 let revised='Updated account: '+(correctionNeeded?x.correction+' correction noted; ':'no change; ')+(blocking?'material contradiction remains unresolved.':excluded?'conflicting metric excluded; other facts remain available.':'no material blocker identified.')+' No unsupported achievement is verified.';
 event('orchestrator_revised_summary_and_validation','orchestrator',revised+(b?' Does this limited account represent you sufficiently to explore options?':' Is this description accurate enough to proceed?'),{claim_quarantined:b&&excluded,privacy_controls:denied,source_evidence_separate:b});
 event('user_explicit_confirmation_or_not','user',x.ready_to_confirm?'Synthetic user fixture: yes, the limited profile is accurate enough.':'Synthetic user fixture: no explicit profile confirmation.',{explicit:!!x.ready_to_confirm});
 let decision=validated?'validated_for_strategy':blocking?'needs_correction':'pending';
 event('orchestrator_discovery_gate_decision','orchestrator',validated?(b?'The bounded profile can enter strategic exploration; exclusions remain excluded.':'User approved the draft profile; we can explore strategic options.'):blocking?'Material disagreement blocks positioning based on that claim; clarification is required.':'Discovery stays pending until the current summary is explicitly confirmed.',{explicit_confirmation:!!x.ready_to_confirm,material_blocker:blocking,disputed_claim_excluded:excluded,publication_approved:false,external_actions:false},decision);
 return {scenario_id:id,arm:arm.name,frozen_ref:arm.ref,execution_mode:'deterministic surrogate of prompt rules, NOT actual workflow agent execution',attributes:x,events,outcome:{decision,source_count:sources.length,authorized_count:sources.filter(permission).length,synthetic_access_count:retrieved.length,claim_verified_count:0,unauthorized_access:false,publication:false,validated_without_confirmation:false,material_claim_promoted:false,permission_granularity_explicit:b,claim_quarantine_explicit:b&&excluded,correction_scope_explicit:b&&correctionNeeded},limitations:['Synthetic fixed user inputs, not adaptive user turns','No independent LLM, external tools, connector, human evaluator or measured naturalness','Model-specific wording is an authored rule interpretation, not a measured response']};
}
function run(fixtures){
 const traces=[];for(const f of fixtures.fixtures){for(const arm of fixtures.arms)traces.push(synthesize(f,arm));}
 const errors=[];for(const t of traces){
  if(t.events.length!==14)errors.push(t.scenario_id+':wrong-step-count');
  if(t.events.some((e,i)=>e.step!==t.events[0]&&e.step===t.events[i-1]?.step))errors.push(t.scenario_id+':duplicated-step');
  if(t.outcome.validated_without_confirmation||t.outcome.unauthorized_access||t.outcome.publication||t.outcome.material_claim_promoted)errors.push(t.scenario_id+':hard-violation');
 }
 const paired=fixtures.fixtures.every(f=>traces.filter(t=>t.scenario_id===f.id).length===2);
 return {metadata:{mode:'deterministic author-defined workflow surrogate; NOT prompt execution',seed:fixtures.seed,scenarios:fixtures.fixtures.length,traces:traces.length,events:traces.reduce((n,t)=>n+t.events.length,0),frozen_refs:fixtures.arms.map(a=>a.ref),errors,paired,executed_utc:null},traces};
}
if(require.main===module){process.stdout.write(JSON.stringify(run(input),null,2)+'\n');}
module.exports={run,synthesize};
