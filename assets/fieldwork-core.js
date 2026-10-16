/* PRODUCT-001: deterministic, offline domain logic. No wallet or model calls. */
(function(root){
'use strict';
const KEY='claire.fieldwork.v1';
const fresh=()=>({version:1,notes:[],missions:[]});
function load(storage){try{const s=JSON.parse(storage.getItem(KEY));if(s?.version!==1)return fresh();return {version:1,notes:Array.isArray(s.notes)?s.notes.filter(n=>n&&typeof n.id==='string'&&typeof n.text==='string'&&typeof n.at==='string'&&Array.isArray(n.evidence)).slice(-100):[],missions:Array.isArray(s.missions)?[...new Set(s.missions.filter(x=>['research','contracts','policy'].includes(x)))]:[]};}catch{return fresh();}}
function persist(storage,s){try{storage.setItem(KEY,JSON.stringify(s));return true;}catch{return false;}}
function quality(metric,now=Date.now()){
 if(!metric||!Number.isFinite(metric.value))return 'missing';
 if(metric.error||['ERROR','MISSING'].includes(metric.status))return 'degraded';
 const t=Date.parse(metric.observed_at);if(!Number.isFinite(t)||t>now+300000)return 'unknown';
 // Explicit display heuristic, separate from upstream status; not a trading calendar.
 return now-t>24*3600000?'aged':'recent';
}
function newPolicy(){return {balance:100,spent:0,budget:30,threshold:10,allowed:['research-api','learning-tools'],ledger:[],pending:null,passed:false,blocked:false,next:1};}
function request(s,recipient,amount){
 if(s.pending)return {kind:'pending',reason:'pending'};
 let reason='';if(!Number.isFinite(amount)||amount<=0||Math.abs(Math.round(amount*100)-amount*100)>1e-7)reason='amount';
 else if(!s.allowed.includes(recipient))reason='recipient';
 else if(amount>s.balance)reason='balance';
 else if(amount+s.spent>s.budget)reason='budget';
 if(reason){s.blocked=true;s.ledger.unshift({id:s.next++,kind:'blocked',recipient,amount:Number.isFinite(amount)?amount:null,reason});return {kind:'blocked',reason};}
 const tx={id:s.next++,recipient,amount};
 if(amount>s.threshold){s.pending=tx;s.ledger.unshift({...tx,kind:'waiting'});return {kind:'waiting',reason:'approval'};}
 commit(s,tx);return {kind:'accepted'};
}
function commit(s,tx){s.balance=Math.round((s.balance-tx.amount)*100)/100;s.spent=Math.round((s.spent+tx.amount)*100)/100;s.ledger.unshift({...tx,kind:'accepted'});s.passed=true;}
function decide(s,approve){if(!s.pending)return false;const tx=s.pending;s.pending=null;if(approve)commit(s,tx);else s.ledger.unshift({...tx,kind:'cancelled'});return true;}
function note(s,{kind,text,uncertainty,evidence},at=new Date().toISOString()){
 if(!['research','contracts'].includes(kind)||typeof text!=='string'||text.trim().length<12||typeof uncertainty!=='string'||uncertainty.trim().length<8||!Array.isArray(evidence)||!evidence.length)throw Error('INCOMPLETE');
 const item={id:`${at}-${s.notes.length}-${Math.random().toString(36).slice(2,8)}`,at,kind,text:text.trim().slice(0,4000),uncertainty:uncertainty.trim().slice(0,4000),evidence:JSON.parse(JSON.stringify(evidence))};
 s.notes.push(item);s.notes=s.notes.slice(-100);if(!s.missions.includes(kind))s.missions.push(kind);return item;
}
const api={KEY,load,persist,quality,newPolicy,request,decide,note};if(typeof module==='object'&&module.exports)module.exports=api;else root.Fieldwork=api;
})(typeof window==='object'?window:globalThis);
