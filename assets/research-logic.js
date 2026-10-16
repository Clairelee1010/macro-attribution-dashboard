/* Pure quality policy shared by the page and regression checks. */
(function(root){
'use strict';
const finite=x=>typeof x==='number'&&Number.isFinite(x);
function ageState(time,now=Date.now(),hours=36){const t=Date.parse(time);return !Number.isFinite(t)?'MISSING_TIME':t>now+300000?'FUTURE_TIME':now-t>hours*3600000?'STALE':'RECENT';}
function quality(docs,now=Date.now()){
 const m=docs.market||{},n=docs.news||{},eq=docs.equity||{};
 const rows=['US10Y','DXY','VIX','BTC','ETH'].map(k=>{const x=m.metrics?.[k]||{};return {id:k,...x,quality:!finite(x.value)?'MISSING':ageState(x.observed_at,now)};});
 return {generated_at:m.generated_at||null,p02_time:docs.predictions?.generated_at||null,matched_events:finite(docs.predictions?.summary?.matched_events)?docs.predictions.summary.matched_events:null,rows,missing:rows.filter(x=>x.quality==='MISSING').length,old:rows.filter(x=>x.quality!=='RECENT'&&x.quality!=='MISSING').length,fallback:rows.filter(x=>x.source_type==='FALLBACK').length,source_errors:(Array.isArray(n.errors)?n.errors:[]),news_count:Array.isArray(n.items)?n.items.length:0,news_time:n.generated_at||null,insufficient_pairs:(eq.pairs||[]).filter(x=>x.comparison?.status!=='COMPARABLE'),file_errors:docs.errors||[]};
}
function probability(x){return finite(x)&&x>=0&&x<=1?(x*100).toLocaleString('en-US',{maximumFractionDigits:2})+'%':null;}
function reviewCase(c,now=Date.now()){
 return {contracts:(c.contracts||[]).map(x=>({...x,display_probability:probability(x.implied_probability),time_state:ageState(x.retrieved_at,now),closed:!Number.isFinite(Date.parse(x.market_close_time))||Date.parse(x.market_close_time)<=now})),comparison:'WITHHELD',future_event:(c.event?.meeting_dates||[]).some(x=>Date.parse(x+'T23:59:59Z')>=now)};
}
const api={finite,ageState,quality,probability,reviewCase};if(typeof module==='object')module.exports=api;else root.ClaireResearch=api;
})(typeof window==='undefined'?globalThis:window);
