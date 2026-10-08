import test from 'node:test';
import assert from 'node:assert/strict';
import {latestAt,parseApiTime,pairAt,summarize} from './crown-vs-bet365-paired.mjs';

test('TotalCorner profile unoffset times parse in Asia Shanghai',()=>{
  assert.equal(parseApiTime('2026-10-08 18:00:00'),'2026-10-08T10:00:00.000Z');
  assert.equal(parseApiTime('2026-10-08T11:00:00Z'),'2026-10-08T11:00:00.000Z');
});
test('As-of pairing reconstructs exact common market time and different line',()=>{
  const asof='2026-10-08T12:00:00Z';
  const kickoff='2026-10-09T12:00:00Z';
  const defaults={status:'FOUND',market_histories:{OU:[
    [null,'2.5, 3.0',1.90,1.90,'2026-10-08 19:45:00',null,null],
    [null,'2.75',1.84,1.95,'2026-10-08 20:15:00',null,null]
  ],AH:[[null,'-0.5',1.90,1.90,'2026-10-08 20:00:00',null,null]]}};
  const crown={status:'FOUND',market_histories:{OU:[
    [null,'3.0',1.92,1.88,'2026-10-08 19:50:00',null,null]
  ],AH:[[null,'-0.75',1.96,1.84,'2026-10-08 19:55:00',null,null]]}};
  const fixture={mode:'same_fetch_snapshot'};
  const x=pairAt(defaults,crown,asof,kickoff,fixture);
  assert.equal(x.OU.bet365.line,2.75);
  assert.equal(x.OU.crown.line,3);
  assert.equal(x.OU.crown_minus_bet365_line,.25);
  assert.equal(x.AH.crown_minus_bet365_line,-.25);
  assert.equal(x.OU.same_line,false);
  assert.equal(x.AH.same_line,false);
});
test('Same handicap line computes comparable two-sided prices',()=>{
  const asof='2026-10-08T12:00:00Z';
  const kickoff='2026-10-09T12:00:00Z';
  const base={status:'FOUND',market_histories:{AH:[
    [null,'-0.25',1.85,1.95,'2026-10-08 19:57:00']
  ],OU:[[null,'2.5',1.90,1.90,'2026-10-08 19:59:00']]}};
  const crown={status:'FOUND',market_histories:{AH:[
    [null,'-0.25',1.90,1.92,'2026-10-08 19:58:00']
  ],OU:[[null,'2.5',1.96,1.88,'2026-10-08 19:58:00']]}};
  const r=pairAt(base,crown,asof,kickoff,{mode:'same_fetch_snapshot'});
  assert.equal(r.OU.same_line,true);
  assert.equal(r.OU.crown_minus_bet365_price1,.06);
  assert.equal(r.OU.crown_minus_bet365_price2,-.02);
  assert.equal(r.AH.crown_minus_bet365_price1,.05);
  assert.equal(r.AH.crown_minus_bet365_price2,-.03);
  assert.equal(r.OU.both_fresh_and_close_15m,true);
  assert.equal(r.AH.both_fresh_and_close_15m,true);
});
test('Latest suspension blocks a stale open quote and prevents false comparison',()=>{
  const kickoff='2026-10-09T12:00:00Z';
  const rows=[
    [null,'2.5',1.9,1.9,'2026-10-08 19:30:00',null,null,0],
    [null,null,null,null,'2026-10-08 20:00:00',null,null,1]
  ];
  assert.equal(latestAt(rows,'OU','2026-10-08T12:10:00Z',kickoff).status,
    'LATEST_EVENT_CLOSED');
  assert.equal(latestAt(rows,'OU','2026-10-08T11:50:00Z',kickoff).status,
    'OPEN_QUOTE');
});
test('Backtested TG send quote never selects a future market event',()=>{
  const cutoff='2026-10-06T12:00:00Z';
  const kickoff='2026-10-06T20:00:00Z';
  const rows=[
    [null,'2.25',1.85,1.95,'2026-10-06 18:00:00'],
    [null,'2.5',1.98,1.83,'2026-10-06 21:00:00']
  ];
  const val=latestAt(rows,'OU',cutoff,kickoff);
  assert.equal(val.status,'OPEN_QUOTE');
  assert.equal(val.line,2.25);
  assert.equal(val.price1,1.85);
});
