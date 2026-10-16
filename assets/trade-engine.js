/* TRADE-001: an explicit fixture-based matching simulator, not exchange software. */
(function(root){'use strict';
const U=100000000,MAX=U;
function error(code){throw Error(code);}
function decimal(text,places){const s=String(text).trim();if(!new RegExp('^\\d+(?:\\.\\d{1,'+places+'})?$').test(s))error('NUMBER');const [a,b='']=s.split('.'),n=Number(a)*10**places+Number(b.padEnd(places,'0'));if(!Number.isSafeInteger(n)||n<=0)error('NUMBER');return n;}
function parse({side,type,quantity,limit}){if(!['buy','sell'].includes(side)||!['market','limit'].includes(type))error('SPEC');const qty=decimal(quantity,8);if(qty>MAX)error('SIZE');const price=type==='limit'?decimal(limit,2):null;if(price!==null&&price>10000000)error('PRICE');return {side,type,qty,price};}
function book(name='normal'){const offset={normal:0,drop:-20000,rise:20000,thin:0}[name];if(offset===undefined)error('SCENARIO');const qty=name==='thin'?100000:300000;return {asks:[6000000,6006000,6012000].map(price=>({price:price+offset,qty})),bids:[5994000,5988000,5982000].map(price=>({price:price+offset,qty}))};}
function create(){return {version:1,nextId:1,cash:100000,btc:2000000,book:book(),scenario:'normal',orders:[],active:null,events:[]};}
function clone(x){return JSON.parse(JSON.stringify(x));}
function totals(side,ticks){const gross=side==='buy'?Math.ceil(ticks/U):Math.floor(ticks/U),fee=Math.ceil(gross/1000);return {gross,fee,cash:side==='buy'?gross+fee:gross-fee};}
function reserve(order){if(!order||!['OPEN','PARTIALLY_FILLED'].includes(order.status))return {cash:0,btc:0};const remaining=order.qty-order.filled;
 if(order.side==='sell')return {cash:0,btc:remaining};const max=totals('buy',order.ticks+remaining*order.price),spent=totals('buy',order.ticks);return {cash:max.cash-spent.cash,btc:0};}
function wallet(s){const r=reserve(s.active);return {cash:s.cash,btc:s.btc,reservedCash:r.cash,reservedBTC:r.btc,availableCash:s.cash-r.cash,availableBTC:s.btc-r.btc};}
function fillPlan(s,spec){let remaining=spec.qty;const fills=[];for(const [index,l] of (spec.side==='buy'?s.book.asks:s.book.bids).entries()){if(remaining<=0)break;if(spec.type==='limit'&&(spec.side==='buy'?l.price>spec.price:l.price<spec.price))break;const qty=Math.min(remaining,l.qty);if(qty>0){fills.push({index,price:l.price,qty});remaining-=qty;}}return {fills,remaining};}
function preview(s,spec){if(s.active)error('ACTIVE');if(!spec||!['buy','sell'].includes(spec.side)||!['market','limit'].includes(spec.type)||!Number.isSafeInteger(spec.qty)||spec.qty<=0||spec.qty>MAX||(spec.type==='limit'&&(!Number.isSafeInteger(spec.price)||spec.price<=0||spec.price>10000000)))error('SPEC');
 const plan=fillPlan(s,spec),ticks=plan.fills.reduce((n,f)=>n+f.price*f.qty,0),t=totals(spec.side,ticks),reference=(spec.side==='buy'?s.book.asks:s.book.bids).find(l=>l.qty>0)?.price??null;
 const maximum=spec.type==='limit'?totals(spec.side,ticks+plan.remaining*spec.price):t;
 if(spec.side==='buy'&&maximum.cash>s.cash)error('CASH');if(spec.side==='sell'&&spec.qty>s.btc)error('BTC');
 return {version:s.version,spec:clone(spec),...plan,...t,filled:spec.qty-plan.remaining,average:plan.fills.length?ticks/(spec.qty-plan.remaining):null,reference,slippageBps:plan.fills.length&&reference?((ticks/(spec.qty-plan.remaining)-reference)/reference)*10000*(spec.side==='buy'?1:-1):null,reserveCash:spec.side==='buy'&&spec.type==='limit'?maximum.cash-t.cash:0};}
function applyFills(s,o,plan){const before=totals(o.side,o.ticks),levels=o.side==='buy'?s.book.asks:s.book.bids;for(const f of plan.fills){levels[f.index].qty-=f.qty;o.filled+=f.qty;o.ticks+=f.price*f.qty;o.fills.push({...f,version:s.version});}const after=totals(o.side,o.ticks),delta=after.cash-before.cash;
 if(o.side==='buy'){s.cash-=delta;s.btc+=plan.fills.reduce((n,f)=>n+f.qty,0);}else{s.cash+=delta;s.btc-=plan.fills.reduce((n,f)=>n+f.qty,0);}o.gross=after.gross;o.fee=after.fee;
 const remaining=o.qty-o.filled;o.status=remaining===0?'FILLED':o.type==='market'?(o.filled?'PARTIALLY_FILLED_CANCELLED':'CANCELLED'):(o.filled?'PARTIALLY_FILLED':'OPEN');
 o.history.push({version:s.version,status:o.status,filled:o.filled,gross:o.gross,fee:o.fee});}
function submit(s,quote){if(!quote||quote.version!==s.version)error('STALE');const q=preview(s,quote.spec),o={...q.spec,id:s.nextId++,filled:0,ticks:0,fills:[],history:[],gross:0,fee:0,status:'OPEN'};
 applyFills(s,o,q);s.orders.unshift(o);s.active=['OPEN','PARTIALLY_FILLED'].includes(o.status)?o:null;s.version++;s.events.unshift({kind:'submitted',order:o.id,status:o.status});return clone(o);}
function cancel(s,id){if(!s.active||s.active.id!==id)return false;s.active.status='CANCELLED';s.active.history.push({version:s.version,status:'CANCELLED',filled:s.active.filled,gross:s.active.gross,fee:s.active.fee});s.events.unshift({kind:'cancelled',order:id});s.active=null;s.version++;return true;}
function scenario(s,name){const next=book(name);s.book=next;s.scenario=name;s.version++;if(s.active){const o=s.active,q=fillPlan(s,{...o,qty:o.qty-o.filled});applyFills(s,o,q);if(!['OPEN','PARTIALLY_FILLED'].includes(o.status))s.active=null;}s.events.unshift({kind:'scenario',scenario:name});}
const api={U,decimal,parse,create,preview,submit,cancel,scenario,wallet,reserve,totals};if(typeof module==='object'&&module.exports)module.exports=api;else root.TradeEngine=api;
})(typeof window==='object'?window:globalThis);
