/** Read-only TotalCorner result harvest for TG-confirmed MR1 AH formal receipts.
 * Run from checked-out MR1 state directory; source code stays in public Runner.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {TotalCornerReadOnlyClient} from './src/totalcorner-client.js';
const root='data/mr1-v6-cross-market/formal';
const lines=(await fs.readFile(`${root}/sent.jsonl`,'utf8')).split('\n').filter(Boolean).map(JSON.parse);
const settled=JSON.parse(await fs.readFile(`${root}/settled.json`,'utf8')).entries;
const now=Date.now();
const pending=new Map();
for(const s of lines){
  if(settled[s.signal_id])continue;
  if(!Number.isFinite(Date.parse(s.kickoff_at))||Date.parse(s.kickoff_at)+120*60000>now)continue;
  if(!pending.has(String(s.match_id)))pending.set(String(s.match_id),s);
}
const client=new TotalCornerReadOnlyClient({token:process.env.TOTALCORNER_TOKEN,requestsPerMinute:18,maxRetries:2,returnBusinessErrors:true});
const max=Math.min(Number(process.env.MAX_RESULT_CHECKS||80),120);
const rows=[...pending.values()].sort((a,b)=>Date.parse(a.kickoff_at)-Date.parse(b.kickoff_at));
const tally={pending_eligible_matches:rows.length,checked:0,verified_ft:0,already_saved:0,not_final:0,api_errors:0,identity_rejected:0};
for(const s of rows.slice(0,max)){
 const id=String(s.match_id),file=`data/strategy-shadow-ledger/results/${id}.json`;
 try{const old=JSON.parse(await fs.readFile(file,'utf8'));if(old.status==='FT'){tally.already_saved++;continue;}}catch(e){if(e.code!=='ENOENT')throw e;}
 try{
  const r=await client.get(`/match/view/${encodeURIComponent(id)}`,{columns:'asian,goalLine'});tally.checked++;
  const m=Array.isArray(r.body?.data)?r.body.data[0]:r.body?.data;
  const hg=Number(m?.hg),ag=Number(m?.ag);
  if(String(m?.id)!==id){tally.identity_rejected++;continue;}
  if(String(m?.status).toLowerCase()!=='full'||m.hg===null||m.ag===null||m.hg===''||m.ag===''||!Number.isInteger(hg)||!Number.isInteger(ag)||hg<0||ag<0){tally.not_final++;continue;}
  const observed=r.request_finished_at;
  if(Date.parse(observed)<=Date.parse(s.kickoff_at)){tally.identity_rejected++;continue;}
  const evidence={match_id:id,status:'FT',home_goals:hg,away_goals:ag,home:m.h??null,away:m.a??null,league:m.l??null,kickoff_at:s.kickoff_at,source:'TotalCorner /match/view',observed_at:observed,raw_sha256:createHash('sha256').update(r.raw_body_text).digest('hex'),classification:'VERIFIED_FULL_ID_SCORE',collected_at:observed};
  await fs.mkdir(path.dirname(file),{recursive:true});
  await fs.writeFile(file,JSON.stringify(evidence,null,2)+'\n',{flag:'wx'}).catch(e=>{if(e.code!=='EEXIST')throw e;});
  tally.verified_ft++;
 }catch(e){tally.api_errors++;console.error(`RESULT_QUERY_ERROR match_id=${id} ${String(e.message).slice(0,150)}`);}
}
console.log('MR1_FORMAL_RESULT_HARVEST '+JSON.stringify(tally));
