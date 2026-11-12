#!/usr/bin/env node
'use strict';
/**
 * Static fixture-contract validation only. Does NOT execute an LLM, compare
 * workflows, infer a behavioral pass rate, or grade languages in model text.
 *
 * Run: node tests/check_discovery_r16_language_fixtures.js
 */
function validate(data){
 const errors=[], ids=new Set();
 let turns=0,explicit=0,notHard=0,divergent=0,nameSlots=0;
 if(data.schema_version!=='1.0')errors.push('wrong schema');
 if(!Array.isArray(data.cases)||data.cases.length!==12)errors.push('expected twelve cases');
 for(const c of data.cases||[]){
  if(ids.has(c.id))errors.push('duplicate id: '+c.id);ids.add(c.id);
  if(!Array.isArray(c.turns)||c.turns.length<1||c.turns.length>2)errors.push('turn count: '+c.id);
  for(const turn of c.turns||[]){
   turns++;if(typeof turn.user!=='string'||!turn.user.trim())errors.push('empty utterance: '+c.id);
   const e=turn.expected;
   if(!e||typeof e.chat_language_hard_gate!=='boolean') {errors.push('missing expected fields: '+c.id);continue;}
   if(e.chat_language_hard_gate){
    explicit++;if(!['en','pt-BR','de'].includes(e.chat_language))errors.push('invalid explicit chat language: '+c.id);
   } else {
    notHard++;if(e.chat_language!==null)errors.push('ambiguous language must not be hard-scored: '+c.id);
   }
   if(e.name)nameSlots++;
   if(e.chat_language&&e.content_language&&e.chat_language!==e.content_language)divergent++;
   if(e.content_language_assertable_now!==false)errors.push('no immediate deliverable provided in Discovery: '+c.id);
   if(typeof e.reason!=='string'||!e.reason.trim())errors.push('missing oracle explanation: '+c.id);
  }
 }
 const original=data.cases?.find(c=>c.id==='L01');
 if(original?.turns?.[0]?.user!=="Call me Arin. I run a small fictional bookstore and want to communicate what I've learned in Portuguese.")errors.push('L01 no longer matches original R16');
 if(original?.turns?.[0]?.expected?.chat_language_hard_gate!==false)errors.push('original ambiguous R16 incorrectly hard-scored');
 if(ids.size!==12||turns!==16||explicit!==12||notHard!==4)errors.push('expected integrity counts changed');
 return {mode:'offline fixture contract validation, NOT model execution',cases:ids.size,turns,
  explicit_chat_language_turns:explicit,not_hard_scored_turns:notHard,
  name_preference_turns:nameSlots,divergent_chat_content_language_turns:divergent,
  failures:errors.length,errors};
}
if(require.main===module){
 const fs=require('node:fs'),path=require('node:path');
 const json=JSON.parse(fs.readFileSync(path.join(__dirname,'discovery-r16-language-diagnostics-2026-11-12.json'),'utf8'));
 const report=validate(json);console.log(JSON.stringify(report,null,2));
 if(report.failures)process.exitCode=1;
}
module.exports={validate};
