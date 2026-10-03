/* HOME-006: dependency-free geometric 3D miniature island. Canvas2D renders
   world-space 3D meshes through an orthographic camera; draggable orbit + zoom.
   All market numbers remain driven by the existing evidence-aware data pipeline. */
(()=>{'use strict';
const canvas=document.getElementById('islandCanvas'),viewport=document.getElementById('islandViewport'),pins=document.getElementById('islandPins');if(!canvas||!viewport)return;
const ctx=canvas.getContext('2d',{alpha:true});if(!ctx)return;
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const locations=[{id:'p01',x:-3.35,z:-1.7,h:2.1,color:'#4e9cdb',title:'Market Tower',sub:'P01 · UNDERSTAND',number:'01',emoji:'🏙️'},
{id:'p02',x:-1.35,z:-2.7,h:2.1,color:'#8d70d9',title:'Prediction District',sub:'P02 · COMPARE',number:'02',emoji:'🔮'},
{id:'int',x:.8,z:.35,h:1.9,color:'#39aaa8',title:'Intelligence Hub',sub:'INT · CONTEXTUALIZE',number:'03',emoji:'🌐'},
{id:'p03',x:3.2,z:-1.4,h:2.2,color:'#e48b67',title:'Agent Lab',sub:'P03 · INVESTIGATE',number:'04',emoji:'🔥'},
{id:'learn',x:2.6,z:2.4,h:1.25,color:'#76b779',title:'Blockchain School',sub:'LEARN · EXPLORE',number:'05',emoji:'🎓'}];
let angle=-.66,tilt=.77,zoom=1,frame=0,drag=false,lastX=0,downX=0,downY=0,hover=null;
const shapes=[];let camW=900,camH=580,scale=65;
const color=(hex,m=1)=>{const n=parseInt(hex.replace('#',''),16);return `rgb(${Math.max(0,Math.min(255,Math.round((n>>16)*m)))},${Math.max(0,Math.min(255,Math.round(((n>>8)&255)*m)))},${Math.max(0,Math.min(255,Math.round((n&255)*m)))})`};
const V=(x,y,z)=>[x,y,z];
function polygon(verts,fill,stroke=null,width=1){shapes.push({verts,fill,stroke,width,depth:verts.reduce((a,p)=>a+depth(p),0)/verts.length})}
function depth(p){const x=p[0]*Math.cos(angle)-p[2]*Math.sin(angle),z=p[0]*Math.sin(angle)+p[2]*Math.cos(angle);return z*Math.cos(tilt)+p[1]*Math.sin(tilt)}
function project(p){const x=p[0]*Math.cos(angle)-p[2]*Math.sin(angle),z=p[0]*Math.sin(angle)+p[2]*Math.cos(angle);return [camW/2+x*scale,camH*.54+(z*Math.sin(tilt)-p[1]*Math.cos(tilt))*scale]}
function quad(a,b,c,d,fill,stroke=null){polygon([a,b,c,d],fill,stroke)}
function box(x,y,z,w,h,d,base,roof=true){const a=V(x-w/2,y,z-d/2),b=V(x+w/2,y,z-d/2),c=V(x+w/2,y,z+d/2),dd=V(x-w/2,y,z+d/2);const A=V(a[0],y+h,a[2]),B=V(b[0],y+h,b[2]),C=V(c[0],y+h,c[2]),D=V(dd[0],y+h,dd[2]);quad(a,b,B,A,color(base,.78));quad(b,c,C,B,color(base,.86));quad(c,dd,D,C,color(base,.67));quad(dd,a,A,D,color(base,.93));quad(A,B,C,D,roof?color(base,1.22):base);return [A,B,C,D]}
function cyl(x,y,z,r,h,col,sides=12){const ring=[],top=[];for(let i=0;i<sides;i++){const a=i/sides*Math.PI*2;ring.push(V(x+Math.cos(a)*r,y,z+Math.sin(a)*r));top.push(V(x+Math.cos(a)*r,y+h,z+Math.sin(a)*r))}for(let i=0;i<sides;i++)quad(ring[i],ring[(i+1)%sides],top[(i+1)%sides],top[i],color(col,.75+i/sides*.24));polygon(top,col)}
function cone(x,y,z,r,h,col,n=8){const p=V(x,y+h,z);for(let i=0;i<n;i++){const a=i*2*Math.PI/n,b=(i+1)*2*Math.PI/n;polygon([V(x+r*Math.cos(a),y,z+r*Math.sin(a)),V(x+r*Math.cos(b),y,z+r*Math.sin(b)),p],color(col,.78+.24*Math.cos(a)))} }
function tree(x,z,s=1,t=0){cyl(x,.15,z,.075*s,.38*s,'#a47d63',7);if(t%3===0){cone(x,.42*s,z,.43*s,.88*s,t%2?'#47a897':'#5ab18b',8);cone(x,.8*s,z,.3*s,.55*s,'#7ed4a3',8)}else{cyl(x,.5*s,z,.37*s,.34*s,t%2?'#60b8a2':'#6fbe83',9);cone(x,.76*s,z,.35*s,.5*s,t%2?'#78c5a9':'#8ed49a',9)}}
function windows(x,y,z,w,h,d,base,rows,cols){for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const ww=w/(cols+1)*.52,hh=h/(rows+1)*.55;const xx=x-w/2+(c+1)*w/(cols+1),yy=y+(r+1)*h/(rows+1);quad(V(xx-ww/2,yy-hh/2,z-d/2-.008),V(xx+ww/2,yy-hh/2,z-d/2-.008),V(xx+ww/2,yy+hh/2,z-d/2-.008),V(xx-ww/2,yy+hh/2,z-d/2-.008),((r+c)%4===0)?'#d9f7ff':base)}}
function building(loc){const {x,z,id,color:base}=loc;
// shared paved plazas + flower planters
box(x,-.02,z,1.72,.12,1.78,'#f6f4e8');for(let a=0;a<6;a++){const t=a/6*Math.PI*2;const xx=x+Math.cos(t)*1.03,zz=z+Math.sin(t)*1.06;if(Math.abs(xx)>4.65||Math.abs(zz)>3.65)continue;tree(xx,zz,.4,a)}
if(id==='p01') {box(x,.12,z,1.05,1.95,.95,base);windows(x,.12,z,1.05,1.95,.95,'#bce7fc',6,4);box(x,.12,z+.57,1.55,.7,.55,'#66b4d5');box(x,2.08,z,.75,.16,.76,'#e4f5fc');box(x,2.25,z,.12,.43,.12,'#f2bb71')}
if(id==='p02'){cyl(x,.12,z,.72,.36,'#7569bc');box(x,.45,z,.96,1.25,.94,base);windows(x,.45,z,.96,1.25,.94,'#e8e4ff',4,3);cone(x,1.7,z,.75,.78,'#bd9be8',6);cyl(x,2.42,z,.08,.12,'#ffe8a3',8)}
if(id==='int'){cyl(x,.12,z,.86,.48,'#3d9f9c',12);cyl(x,.6,z,.72,.7,'#73c9cb',12);cone(x,1.29,z,.77,.65,'#a7f2ec',12);cyl(x,1.85,z,.09,.19,'#e8fafa');}
if(id==='p03'){box(x,.12,z,.99,1.9,.96,base);windows(x,.12,z,.99,1.9,.96,'#fce6da',6,3);box(x,2.04,z,.73,.24,.72,'#edc3b1');cyl(x,2.29,z,.08,.52,'#e7a068');cone(x,2.75,z,.24,.3,'#f8db91');for(let a=0;a<6;a++){let t=a/6*Math.PI*2;cyl(x+Math.cos(t)*.94,.12,z+Math.sin(t)*.92,.045,.38,'#f1c7a2')}}
if(id==='learn'){box(x,.12,z,1.6,.96,1.25,base,false);windows(x,.12,z,1.6,.96,1.25,'#ddf9e8',3,5);const A=V(x-.9,1.08,z-.76),B=V(x+.9,1.08,z-.76),C=V(x+.9,1.08,z+.76),D=V(x-.9,1.08,z+.76),E=V(x,1.72,z-.76),F=V(x,1.72,z+.76);polygon([A,B,E],'#94cba0');polygon([D,C,F],'#6da87d');quad(A,E,F,D,'#8abf8d');quad(E,B,C,F,'#70a77c');box(x,.12,z-1.03,.46,.18,.5,'#e7ba77')}
}
function road(points,w=0.23){for(let i=0;i<points.length-1;i++){const a=points[i],b=points[i+1],dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz),px=-dz/l*w/2,pz=dx/l*w/2;quad(V(a[0]+px,.13,a[1]+pz),V(b[0]+px,.13,b[1]+pz),V(b[0]-px,.13,b[1]-pz),V(a[0]-px,.13,a[1]-pz),'#f6d6bd');const steps=Math.ceil(l*3);for(let j=0;j<steps;j++){if(j%2)continue;let t=(j+.35)/steps,u=(j+.65)/steps;quad(V(a[0]+dx*t,.14,a[1]+dz*t-.012),V(a[0]+dx*u,.14,a[1]+dz*u-.012),V(a[0]+dx*u,.14,a[1]+dz*u+.012),V(a[0]+dx*t,.14,a[1]+dz*t+.012),'#ffffff')}}}
const routes=[[[-3.35,-1.7],[-1.35,-2.7],[.8,.35],[3.2,-1.4]],[[.8,.35],[2.6,2.4]],[[-3.35,-1.7],[-1.8,1.4],[.8,.35]]];
function draw(){const dpr=Math.min(devicePixelRatio||1,2),r=viewport.getBoundingClientRect();camW=r.width;camH=r.height;if(camW<20)return;const tw=Math.round(camW*dpr),th=Math.round(camH*dpr);if(canvas.width!==tw||canvas.height!==th){canvas.width=tw;canvas.height=th}ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,camW,camH);scale=Math.min(camW/12.4,camH/9.3)*zoom;
// soft atmospheric shadows, coastline and 3D layered terrain
const bg=ctx.createRadialGradient(camW*.5,camH*.57,10,camW*.5,camH*.57,camW*.5);bg.addColorStop(0,'#d5f4ef');bg.addColorStop(.6,'#e8f4fc');bg.addColorStop(1,'#f8f5ff');ctx.fillStyle=bg;ctx.fillRect(0,0,camW,camH);
shapes.length=0;const n=16,outer=[],edge=[],lower=[];for(let i=0;i<n;i++){const t=i/n*Math.PI*2;const xx=Math.cos(t)*5.25,zz=Math.sin(t)*4.1;outer.push(V(xx,.08,zz));edge.push(V(xx*.99,-.22,zz*.99));lower.push(V(xx*.89,-.65,zz*.89))}for(let i=0;i<n;i++){quad(outer[i],outer[(i+1)%n],edge[(i+1)%n],edge[i],i%2?'#79c6b9':'#83d3c6');quad(edge[i],edge[(i+1)%n],lower[(i+1)%n],lower[i],i%2?'#4a99a3':'#59abb0')}polygon(outer,'#d7edce');
// winding paths, central plaza, stream, gardens
road([[-4.15,-2.5],[-2.9,-.4],[-.4,-.7],[1.4,-.3],[3.8,-2.4]],.32);road([[-2.9,-.4],[-1.8,2.8],[1.5,2.6],[2.6,2.4]],.3);road([[-1.35,-2.7],[-.4,-.7],[.8,.35]],.28);road([[.8,.35],[2.6,2.4]],.28);
cyl(-.5,.09,1.1,.65,.08,'#9fdcdb',14);cyl(-.5,.17,1.1,.35,.08,'#b6ece5',14);cyl(-.5,.25,1.1,.13,.32,'#eaf9f4',12);
const trees=[[-4,1.8],[-3.5,2.9],[-2.8,3],[-2,2.3],[-1.3,1.7],[-.3,3.3],[.65,2.9],[1.6,3.1],[3.8,2.5],[4,1.2],[4.1,.1],[3.4,.6],[2.3,-3.2],[1.1,-3.2],[-.2,-3.4],[-2.6,-3.3],[-4.1,-.1],[-4.2,-1.4],[-3.4,.8],[.2,1.9],[2.4,.8]];trees.forEach(([x,z],i)=>tree(x,z,.55+(i%4)*.13,i));
for(const loc of locations)building(loc);
// garden lamps + floating 3D info beacons
for(const [x,z] of [[-2.4,-1.3],[0,-1.6],[2.4,-.4],[1.9,1.7],[-2.3,1.2]]){cyl(x,.15,z,.045,.43,'#a9b6c0');cone(x,.58,z,.16,.24,'#ffe3a3',6)}
shapes.sort((a,b)=>b.depth-a.depth);for(const sh of shapes){const pts=sh.verts.map(project);ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fillStyle=sh.fill;ctx.fill();if(sh.stroke){ctx.strokeStyle=sh.stroke;ctx.lineWidth=sh.width;ctx.stroke()}}
// active signals and research-only hot zone (not transaction routes)
const t=reduce?0:frame*.004;for(let ri=0;ri<routes.length;ri++){const path=routes[ri];ctx.strokeStyle=['#7a80ee','#36b4a9','#e4a15c'][ri];ctx.lineWidth=2.4;ctx.setLineDash([5,7]);ctx.beginPath();path.forEach(([x,z],i)=>{const p=project(V(x,.17,z));i?ctx.lineTo(...p):ctx.moveTo(...p)});ctx.stroke();ctx.setLineDash([]);if(!reduce){let pos=(t*.18+ri*.27)%1;const seg=(path.length-1)*pos,j=Math.min(path.length-2,Math.floor(seg)),u=seg-j;const x=path[j][0]*(1-u)+path[j+1][0]*u,z=path[j][1]*(1-u)+path[j+1][1]*u;const [px,py]=project(V(x,.23,z));ctx.beginPath();ctx.arc(px,py,5,0,Math.PI*2);ctx.fillStyle=['#7872ed','#24bdb2','#f5b360'][ri];ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=15;ctx.fill();ctx.shadowBlur=0}}
const loc=locations[3],center=project(V(loc.x,.16,loc.z)),radius=scale*(1.0+(!reduce?.06*Math.sin(t*3):0));ctx.beginPath();ctx.ellipse(center[0],center[1],radius,radius*.55,-.2,0,Math.PI*2);ctx.strokeStyle='#f6a478aa';ctx.lineWidth=3;ctx.setLineDash([8,7]);ctx.stroke();ctx.setLineDash([]);
// position actual keyboard-focusable markers over world-space structures
for(const loc of locations){const el=pinMap[loc.id];if(!el)continue;const p=project(V(loc.x,loc.h+.67,loc.z));el.style.left=`${Math.max(55,Math.min(camW-55,p[0]))}px`;el.style.top=`${Math.max(112,Math.min(camH-90,p[1]-12))}px`}
frame++;if(!reduce&&document.visibilityState==='visible')requestAnimationFrame(draw)}
const pinMap={};for(const loc of locations){const btn=document.createElement('button');btn.type='button';btn.className='island-pin';btn.style.setProperty('--pin-color',loc.color);btn.setAttribute('aria-label',`Enter ${loc.title}`);btn.innerHTML=`<span class="pin-number">${loc.number}</span>${loc.emoji} ${loc.title}<small>${loc.sub}</small>`;btn.addEventListener('click',()=>{document.querySelector(`.district[data-zone="${loc.id}"]`)?.click()});pins.appendChild(btn);pinMap[loc.id]=btn}
const clamp=(n,min,max)=>Math.min(max,Math.max(min,n));function refresh(){if(reduce)draw()}
viewport.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;drag=true;lastX=downX=e.clientX;downY=e.clientY;viewport.classList.add('dragging');viewport.setPointerCapture(e.pointerId)});
viewport.addEventListener('pointermove',e=>{if(!drag)return;angle=clamp(angle+(e.clientX-lastX)*.006,-1.48,.22);lastX=e.clientX;refresh()});
const release=()=>{drag=false;viewport.classList.remove('dragging')};viewport.addEventListener('pointerup',release);viewport.addEventListener('pointercancel',release);
viewport.addEventListener('wheel',e=>{if(e.ctrlKey)return;e.preventDefault();zoom=clamp(zoom-e.deltaY*.0006,.83,1.3);refresh()},{passive:false});
document.getElementById('islandLeft').addEventListener('click',()=>{angle=clamp(angle-.2,-1.48,.22);refresh()});document.getElementById('islandRight').addEventListener('click',()=>{angle=clamp(angle+.2,-1.48,.22);refresh()});document.getElementById('islandReset').addEventListener('click',()=>{angle=-.66;zoom=1;refresh()});
new ResizeObserver(refresh).observe(viewport);draw();
})();
