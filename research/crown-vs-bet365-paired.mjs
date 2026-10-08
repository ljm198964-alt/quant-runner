// Research-only paired Crown vs Bet365 source-market quote comparison.
// Sends at most two parallel GET requests per fixture and pauses between fixtures.
// No Telegram actions, betting execution, strategy or formal ledger changes.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const fixturesPath=path.join('research','crown-vs-bet365-fixtures.json');
const resultsPath=path.join('research','output','crown-vs-bet365-same-time.json');
const summaryPath=path.join('research','output','crown-vs-bet365-summary.txt');
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const secret=process.env.TOTALCORNER_TOKEN;
const fixtureConfig=JSON.parse(await fs.readFile(fixturesPath,'utf8'));
const fixtures=[...fixtureConfig.upcoming,...fixtureConfig.historical];
const RETRIEVAL_GAP_MS=8500;
const MARKET_FIELDS={AH:'asian_list',OU:'goal_list'};
const iso=stamp=>new Date(stamp).toISOString();
const asOfMins=(a,b)=>(Date.parse(a)-Date.parse(b))/60000;
const finite=x=>Number.isFinite(Number(x));
const clampRound=(n,places=5)=>n==null?null:Number(n.toFixed(places));
const median=vals=>vals.length?([...vals].sort((a,b)=>a-b)[Math.floor((vals.length-1)/2)]
 + [...vals].sort((a,b)=>a-b)[Math.floor(vals.length/2)])/2:null;
const mean=vals=>vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:null;
const fmt=val=>val==null?'—':String(val);

function parseApiTime(raw){
  const s=String(raw??'').trim();
  if(!s)return null;
  const time=s.includes('T')?s:s.replace(' ','T');
  const qualified=/Z$|[+-]\d{2}:?\d{2}$/.test(time)?time:time+'+08:00';
  const ms=Date.parse(qualified);
  return Number.isFinite(ms)?new Date(ms).toISOString():null;
}
function lineOf(raw){
  const pieces=String(raw??'').replace(/\s+/g,'').split(',').map(Number);
  return pieces.length>=1&&pieces.length<=2&&pieces.every(Number.isFinite)?
    pieces.reduce((a,b)=>a+b,0)/pieces.length:null;
}
function normalizeMovement(record,market){
  if(!Array.isArray(record)||record.length<5)return null;
  const at=parseApiTime(record[4]);
  if(!at)return null;
  const closed=record[7]===1||String(record[7])==='1';
  const line=lineOf(record[1]);
  const a=record[2]==null?null:Number(record[2]);
  const b=record[3]==null?null:Number(record[3]);
  const isInPlay=record[0]!=null&&!['','0'].includes(String(record[0]));
  return {observed_at:at,line,price1:a,price2:b,closed,
    is_in_play:isInPlay,market};
}
function latestAt(records,market,when,kickoff){
  if(!Array.isArray(records)||!records.length)return {status:'NO_MOVEMENT_HISTORY'};
  const events=records.map(row=>normalizeMovement(row,market)).filter(Boolean)
    .filter(x=>Date.parse(x.observed_at)<=Date.parse(when) &&
      Date.parse(x.observed_at)<Date.parse(kickoff) && !x.is_in_play)
    .sort((a,b)=>Date.parse(a.observed_at)-Date.parse(b.observed_at));
  if(!events.length)return {status:'NO_PREMATCH_EVENT_ASOF'};
  const last=events.at(-1);
  if(last.closed)return {status:'LATEST_EVENT_CLOSED',observed_at:last.observed_at};
  if(last.line==null||!(last.price1>1&&last.price2>1))
    return {status:'LATEST_EVENT_INVALID',observed_at:last.observed_at};
  const conflicts=events.filter(e=>e.observed_at===last.observed_at&&
    (e.line!==last.line||e.price1!==last.price1||e.price2!==last.price2));
  if(conflicts.length)return {status:'SAME_TIME_EVENT_CONFLICT',observed_at:last.observed_at};
  return {status:'OPEN_QUOTE',observed_at:last.observed_at,line:last.line,
    price1:last.price1,price2:last.price2,
    quote_age_minutes:clampRound(asOfMins(when,last.observed_at),2),
    available_history_events:events.length};
}
async function getOne(id,source){
  const requestStartedAt=new Date().toISOString();
  const url=new URL(source==='crown'?
    'https://api.totalcorner.com/v1/match/bookmaker_odds/'+encodeURIComponent(id):
    'https://api.totalcorner.com/v1/match/odds/'+encodeURIComponent(id));
  url.searchParams.set('token',secret);
  if(source==='crown')url.searchParams.set('bookmaker','crown');
  url.searchParams.set('columns','asianList,goalList');
  try{
    const res=await fetch(url,{headers:{Accept:'application/json'},signal:AbortSignal.timeout(20000)});
    const raw=await res.text();
    const finished=new Date().toISOString();
    let body=null;
    try{body=JSON.parse(raw)}catch{}
    const raw_hash=createHash('sha256').update(raw).digest('hex');
    const out={source,request_started_at:requestStartedAt,received_at:finished,
      http_status:res.status,api_success:body?.success,
      x_rate_limit_remaining:res.headers.get('x-rate-limit-remaining'),
      raw_response_sha256:raw_hash,status:'UNKNOWN'};
    if(!res.ok||body?.success!==1){
      out.status='PROVIDER_RESPONSE_NOT_SUCCESS';
      out.error_code=body?.error?.code??null;
      return out;
    }
    const data=Array.isArray(body?.data)?body.data:[body?.data];
    const matches=data.filter(m=>m&&String(m.id)===String(id));
    if(matches.length!==1){out.status='MATCH_ID_NOT_UNIQUE';return out;}
    const match=matches[0];
    let lists=match;
    if(source==='crown'){
      const entries=match.bookmakers||[];
      const books=entries.filter(e=>e.slug==='crown');
      if(books.length!==1){out.status='CROWN_NOT_OFFERED';return out;}
      lists=books[0];
      out.crown_bookmaker_identified=true;
    }
    out.status='FOUND';
    out.fixture_name=[match.h,match.a].filter(Boolean).join(' vs ');
    out.kickoff_from_provider=parseApiTime(match.start);
    out.market_histories={
      AH:Array.isArray(lists.asian_list)?lists.asian_list:[],
      OU:Array.isArray(lists.goal_list)?lists.goal_list:[]
    };
    out.history_sizes={AH:out.market_histories.AH.length,OU:out.market_histories.OU.length};
    return out;
  }catch(e){
    return {source,request_started_at:requestStartedAt,
      received_at:new Date().toISOString(),status:'REQUEST_FAILED',
      error_type:e?.name||'UnknownError'};
  }
}
function pairAt(defaultSource,crownSource,asof,kickoff,fixture){
  const market={};
  for(const m of ['AH','OU']){
    const a=defaultSource?.status==='FOUND'?latestAt(defaultSource.market_histories[m],m,asof,kickoff):
      {status:'SOURCE_UNAVAILABLE'};
    const b=crownSource?.status==='FOUND'?latestAt(crownSource.market_histories[m],m,asof,kickoff):
      {status:'SOURCE_UNAVAILABLE'};
    const both=a.status==='OPEN_QUOTE'&&b.status==='OPEN_QUOTE';
    const sameLine=both&&Math.abs(a.line-b.line)<1e-8;
    const timeGap=both?asOfMins(b.observed_at,a.observed_at):null;
    const entry={bet365:a,crown:b,same_line:sameLine,
      crown_minus_bet365_line:both?clampRound(b.line-a.line,3):null,
      crown_minus_bet365_price1:sameLine?clampRound(b.price1-a.price1,3):null,
      crown_minus_bet365_price2:sameLine?clampRound(b.price2-a.price2,3):null,
      quote_update_time_gap_minutes:both?clampRound(timeGap,2):null,
      both_quote_ages_within_15m:both&&a.quote_age_minutes<=15&&b.quote_age_minutes<=15,
      both_quote_ages_within_60m:both&&a.quote_age_minutes<=60&&b.quote_age_minutes<=60,
      quote_events_within_15m:both&&Math.abs(timeGap)<=15,
      quote_events_within_60m:both&&Math.abs(timeGap)<=60,
      both_fresh_and_close_15m:both&&a.quote_age_minutes<=15&&b.quote_age_minutes<=15&&Math.abs(timeGap)<=15,
      both_fresh_and_close_60m:both&&a.quote_age_minutes<=60&&b.quote_age_minutes<=60&&Math.abs(timeGap)<=60,
      active_at_common_asof:both};
    if(fixture.mode==='historical_tg_asof'){
      const contracts=fixture.tg_contracts||[];
      entry.tg_contracts=contracts.filter(t=>t.market===m)
        .filter(t=>t.tg_sent_at===asof)
        .map(t=>{
          const target=m==='AH'?(t.side==='AWAY'?-Number(t.target_line):Number(t.target_line)):
            Number(t.target_line);
          const lineFits=both&&Math.abs(target-b.line)<1e-8;
          const sidePriceIndex=(m==='OU'?(t.side==='UNDER'?2:1):(t.side==='AWAY'?2:1));
          return {...t,crown_matches_TG_contract:lineFits,
            crown_price_at_same_TG_line:lineFits?(sidePriceIndex===1?b.price1:b.price2):null,
            crown_minus_TG_sent_price:lineFits&&finite(t.tg_decimal_price)?
              clampRound((sidePriceIndex===1?b.price1:b.price2)-Number(t.tg_decimal_price),3):null,
            original_TG_contract_not_verified_as_Crown:true};
        });
    }
    market[m]=entry;
  }
  return market;
}
function summarize(all){
  const marketSummaries={};
  for(const m of ['AH','OU']){
    const matched=all.flatMap(f=>f.comparison_events.map(e=>({...e.market[m],mode:f.mode,
      match_id:f.match_id,label:f.label,asof:e.asof})));
    const good=matched.filter(x=>x.active_at_common_asof);
    const same=good.filter(x=>x.same_line);
    const fresh60=good.filter(x=>x.both_fresh_and_close_60m);
    const fresh15=good.filter(x=>x.both_fresh_and_close_15m);
    marketSummaries[m]={
      samples:matched.length,available_both:good.length,
      line_same:same.length,line_different:good.length-same.length,
      abs_line_diff_median:median(good.map(x=>Math.abs(x.crown_minus_bet365_line))),
      abs_line_diff_mean:clampRound(mean(good.map(x=>Math.abs(x.crown_minus_bet365_line))),4),
      difference_by_line:good.reduce((a,x)=>{
        const k=String(x.crown_minus_bet365_line);a[k]=(a[k]||0)+1;return a;},{}),
      same_line_price1_crown_minus_default_median:median(same.map(x=>x.crown_minus_bet365_price1)),
      same_line_price2_crown_minus_default_median:median(same.map(x=>x.crown_minus_bet365_price2)),
      same_line_abs_price1_diff_median:median(same.map(x=>Math.abs(x.crown_minus_bet365_price1))),
      same_line_abs_price2_diff_median:median(same.map(x=>Math.abs(x.crown_minus_bet365_price2))),
      last_quote_event_gap_min_median:median(good.map(x=>Math.abs(x.quote_update_time_gap_minutes))),
      both_quote_age_under60_and_event_gap60:fresh60.length,
      both_quote_age_under15_and_event_gap15:fresh15.length,
      fresh60_line_same:fresh60.filter(x=>x.same_line).length,
      fresh60_line_changed:fresh60.filter(x=>!x.same_line).length,
      fresh60_line_abs_diff_median:median(fresh60.map(x=>Math.abs(x.crown_minus_bet365_line))),
      historic_asof_paired:good.filter(x=>x.mode==='historical_tg_asof').length,
      live_fetch_paired:good.filter(x=>x.mode==='same_fetch_snapshot').length,
      note:'Both API endpoints were fetched in one short batch. Market-event timestamps may differ greatly; do not claim synchronous bookmaker quotes if aged.'
    };
  }
  return marketSummaries;
}
async function main(){
  if(!secret)throw new Error('TOTALCORNER_TOKEN_REQUIRED');
  const began=new Date().toISOString();
  const all=[];
  for(let i=0;i<fixtures.length;i++){
    const fixture=fixtures[i];
    const started=Date.now();
    // Exactly 2 simultaneous API GETs per selected fixture, <= one pair every 8.5 s.
    const [bet,crown]=await Promise.all([
      getOne(fixture.match_id,'bet365_default'),
      getOne(fixture.match_id,'crown')]);
    const comparisonEvents=[];
    const eventTimes=fixture.mode==='historical_tg_asof'?
      [...new Set((fixture.tg_contracts||[]).map(x=>x.tg_sent_at))].sort():
      [new Date(Math.max(Date.parse(bet.received_at),Date.parse(crown.received_at))).toISOString()];
    const fetchGap=Math.abs(Date.parse(bet.request_started_at)-Date.parse(crown.request_started_at))/1000;
    const responseGap=Math.abs(Date.parse(bet.received_at)-Date.parse(crown.received_at))/1000;
    for(const asof of eventTimes){
      if(Date.parse(asof)>=Date.parse(fixture.kickoff_at))continue;
      comparisonEvents.push({asof,market:pairAt(bet,crown,asof,fixture.kickoff_at,fixture)});
    }
    all.push({
      match_id:fixture.match_id,label:fixture.label,mode:fixture.mode,
      kickoff_at:fixture.kickoff_at,paired_request_start_gap_seconds:clampRound(fetchGap,2),
      paired_received_gap_seconds:clampRound(responseGap,2),
      sources:{
        default_bet365:Object.fromEntries(Object.entries(bet).filter(([key])=>key!=='market_histories')),
        crown:Object.fromEntries(Object.entries(crown).filter(([key])=>key!=='market_histories'))
      },
      comparison_events:comparisonEvents
    });
    // Do not reveal token; print only progress and provider/price-source availability.
    console.log('PAIR',i+1,'OF',fixtures.length,fixture.match_id,
      'BET365',bet.status,'CROWN',crown.status,
      'MARKETS_OK',comparisonEvents.filter(e=>e.market.OU.active_at_common_asof).length);
    if(i+1<fixtures.length)await pause(Math.max(0,RETRIEVAL_GAP_MS-(Date.now()-started)));
  }
  const report={
    protocol:'CROWN_VS_BET365_SAME_ASOF_PAIRED_RESEARCH_20261008',
    research_only:true,telegram_write:false,formal_strategy_changed:false,
    bookmaker_execution_verified:false,
    api_calls_planned:fixtures.length*2,
    api_calls_attempted:all.length*2,
    fetched_started_at:began,fetched_completed_at:new Date().toISOString(),
    timezone_assumption:'Asia/Shanghai for unoffset TotalCorner event timestamps',
    historic_mode:'At the same historical M1 Telegram sent time, reconstruct Crown and default quotes using full movement histories; historical event timestamp is not proof of actual execution.',
    fresh_mode:'Both provider API GETs start in parallel within the same pair, but underlying bookmaker update timestamps may be many minutes/hours apart.',
    source_labels:{default:'TotalCorner /match/odds is Bet365 per TotalCorner docs',crown:'TotalCorner /match/bookmaker_odds?bookmaker=crown is Crown-labelled aggregator'},
    summary_by_market:summarize(all),
    fixture_comparisons:all
  };
  await fs.mkdir(path.dirname(resultsPath),{recursive:true});
  await fs.writeFile(resultsPath,JSON.stringify(report,null,2)+'\n');
  const lines=[
    'Crown versus Bet365: paired time-window audit',
    'Started '+began+', finished '+report.fetched_completed_at,
    'Matches '+all.length+', attempted API calls '+report.api_calls_attempted,
    ...['AH','OU'].map(m=>m+' '+JSON.stringify(report.summary_by_market[m])),
    ...all.map(row=>[row.match_id,row.mode,row.label,
      'AH '+row.comparison_events.map(x=>{
        const m=x.market.AH;
        return m.active_at_common_asof?[x.asof,'B',m.bet365.line,m.bet365.price1,m.bet365.price2,
          'C',m.crown.line,m.crown.price1,m.crown.price2,
          'Quote age',m.bet365.quote_age_minutes,m.crown.quote_age_minutes,
          'event gap',m.quote_update_time_gap_minutes].join(' '):
          m.bet365.status+'/'+m.crown.status;}).join(' | '),
      'OU '+row.comparison_events.map(x=>{
        const m=x.market.OU;
        return m.active_at_common_asof?[x.asof,'B',m.bet365.line,m.bet365.price1,m.bet365.price2,
          'C',m.crown.line,m.crown.price1,m.crown.price2,
          'Quote age',m.bet365.quote_age_minutes,m.crown.quote_age_minutes,
          'event gap',m.quote_update_time_gap_minutes].join(' '):
          m.bet365.status+'/'+m.crown.status;}).join(' | ')
    ].join(' | '))
  ];
  await fs.writeFile(summaryPath,lines.join('\n')+'\n');
  console.log('COMPLETED',JSON.stringify(report.summary_by_market));
}
export {parseApiTime,lineOf,normalizeMovement,latestAt,pairAt,summarize};
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
