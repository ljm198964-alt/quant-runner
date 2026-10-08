// Read-only Crown source-contract smoke. No Telegram, betting execution, or writes to
// formal ledgers. Two Crown-only requests spaced for TotalCorner VIP budget.
import fs from 'node:fs/promises';
import {mkdir} from 'node:fs/promises';
import {extractCrownPaths} from '../../mr1/src/crown-source.js';

const ids=['200936028','200933914'];
const token=process.env.TOTALCORNER_TOKEN;
if(!token)throw new Error('TOKEN_NOT_CONFIGURED');
const results=[];
for(let i=0;i<ids.length;i++){
  const id=ids[i];
  const url=new URL('https://api.totalcorner.com/v1/match/bookmaker_odds/'+id);
  url.searchParams.set('token',token);
  url.searchParams.set('bookmaker','crown');
  url.searchParams.set('columns','asianList,goalList,oddsList');
  const requestedAt=new Date().toISOString();
  const res=await fetch(url,{headers:{Accept:'application/json'},signal:AbortSignal.timeout(25000)});
  const text=await res.text();
  const receivedAt=new Date().toISOString();
  let payload=null;
  try{payload=JSON.parse(text)}catch{}
  const item=(Array.isArray(payload?.data)?payload.data:[payload?.data])
    .find(x=>x&&String(x.id)===id);
  let status='UNRESOLVED',markets={};
  if(res.ok&&Number(payload?.success)===1&&item){
    const start=item?.start;
    const kickoff=start&&Date.parse(String(start).replace(' ','T')+'+08:00');
    try{
      const crown=extractCrownPaths(payload,id,{
        asOf:receivedAt,kickoff:Number.isFinite(kickoff)?new Date(kickoff).toISOString():null
      });
      status='CROWN_IDENTIFIED';
      markets={
        AH:{events:crown.ahPath.length,latest_line:crown.ahPath[0]?.line??null},
        OU:{events:crown.ouPath.length,latest_line:crown.ouPath[0]?.line??null},
        X1X2:{events:crown.odds1x2Path.length}
      };
    }catch(e){status='CROWN_NOT_VERIFIED:'+String(e?.message||'UnknownError');}
  }else status='API_NOT_SUCCESS_HTTP_'+res.status;
  await fs.writeFile('/tmp/crown-source-smoke-'+id+'.json',JSON.stringify(payload));
  results.push({fixture_id:id,requested_at:requestedAt,received_at:receivedAt,
    http_status:res.status,source:'TotalCorner /match/bookmaker_odds?bookmaker=crown',
    market:markets,status:status,order_executed:false});
  console.log(JSON.stringify({id,status,markets}));
  if(i+1<ids.length)await new Promise(resolve=>setTimeout(resolve,5000));
}
await mkdir('research/output',{recursive:true});
await fs.writeFile('research/output/crown-source-smoke.json',
  JSON.stringify({protocol:'CROWN_ONLY_SOURCE_READ_TEST',request_count:ids.length,
    results,real_bookmaker_fill_proven:false,telegram_write:false},null,2)+'\n');
if(!results.some(r=>r.status==='CROWN_IDENTIFIED'))
  throw new Error('CROWN_SOURCE_CONTRACT_NOT_VERIFIED');
