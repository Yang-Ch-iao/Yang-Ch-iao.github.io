'use strict';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const navLinks = [...document.querySelectorAll('.sidebar nav a')];
const sections = [...document.querySelectorAll('main > [id]')];
function updateNavigation(){let current=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<180)current=section;}navLinks.forEach(link=>{const active=link.hash==='#'+current.id;link.classList.toggle('active',active);if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});}
window.addEventListener('scroll',updateNavigation,{passive:true});updateNavigation();
const filters=[...document.querySelectorAll('.filter')];
filters.forEach(button=>button.addEventListener('click',()=>{const category=button.dataset.filter;let count=0;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.publication').forEach(p=>{p.hidden=category!=='all'&&p.dataset.category!==category;if(!p.hidden)count++;});document.getElementById('publication-count').textContent=`${count} publications and manuscripts`; }));

// Two schematic generation rounds, following MolWorld Section 3.2.
// Context conditioning does not prescribe a parent or an edge for a candidate.
const world=document.getElementById('molworld');
const svg=world.querySelector('.molworld-svg');
svg.classList.add('has-motion');
const controls=document.getElementById('world-controls');
const toggle=document.getElementById('world-toggle');
const stage=document.getElementById('world-stage');
const candidates=[...world.querySelectorAll('.mw-candidate')];
const edges=[...world.querySelectorAll('.mw-verified-edge')];
const anchors=[...world.querySelectorAll('.mw-anchor-ring,.mw-anchor-edge')];
const mobileFigure=window.matchMedia('(max-width:540px)');
function resizeFigure(){svg.setAttribute('viewBox',mobileFigure.matches?'0 0 460 445':'0 0 730 445');svg.classList.toggle('mobile-layout',mobileFigure.matches);}
mobileFigure.addEventListener('change',resizeFigure);resizeFigure();
let elapsed=0,lastTime=null,frame=null,inView=false,paused=reducedMotion.matches;
const clamp=n=>Math.max(0,Math.min(1,n));
const ease=n=>{n=clamp(n);return n*n*(3-2*n);};
function drawWorld(t){
  for(const node of candidates){
    const local=t-(Number(node.dataset.round)-1)*12;
    const rejected=node.classList.contains('mw-rejected');
    const appear=ease((local-3)/.7);
    node.style.opacity=String(appear*(rejected?1-ease((local-8.4)/.7):1));
    node.classList.toggle('verified',local>=7.2&&!rejected);
    node.classList.toggle('rejected',local>=7.2&&rejected);
    node.querySelector('.mw-dot').setAttribute('r',String(6.5*(.8+.2*appear)));
  }
  for(const edge of edges){
    const local=t-(Number(edge.dataset.round)-1)*12;
    const progress=ease((local-6)/1.2);
    edge.style.opacity=String(progress>0?1:0);
    edge.style.strokeDasharray='1';edge.style.strokeDashoffset=String(1-progress);
  }
  for(const anchor of anchors){
    const local=t-(Number(anchor.dataset.round)-1)*12;
    anchor.style.opacity=String(ease(local/.7)*(1-ease((local-9)/.8)));
  }
  const round=t<12?1:2,local=t-(round-1)*12;
  const labels=['Select a connected 5-molecule anchor context','Sample multiple candidates from the whole context','Verify MMP links to the current graph','Incorporate connected candidates; update the graph'];
  const index=local<3?0:local<6?1:local<9?2:3;
  stage.textContent=`Round ${round} · ${index+1}/4 · ${labels[index]}`;
  world.querySelector('.mw-graph-caption').textContent=local<3?'The highlighted five molecules form one connected context.':local<6?'The five-molecule context conditions a batch of candidates.':local<9?'Most verified links return to the five anchors; a few reach other molecules.':'Only candidates with a verified link to the current graph are added.';
}
function updateButton(){toggle.textContent=paused?'Play':'Pause';toggle.setAttribute('aria-label',paused?'Play graph animation':'Pause graph animation');}
function canRun(){return inView&&!document.hidden&&!paused;}
function tick(now){frame=null;if(!canRun()){lastTime=null;return;}if(lastTime!==null)elapsed+=(now-lastTime)/1000;lastTime=now;drawWorld(Math.min(elapsed,24));if(elapsed>=25){elapsed=24;paused=true;updateButton();lastTime=null;return;}frame=requestAnimationFrame(tick);}
function syncPlayback(){if(canRun()&&frame===null){lastTime=null;frame=requestAnimationFrame(tick);}else if(!canRun()){if(frame!==null)cancelAnimationFrame(frame);frame=null;lastTime=null;}}
controls.hidden=false;elapsed=reducedMotion.matches?24:0;drawWorld(elapsed);updateButton();
toggle.addEventListener('click',()=>{if(paused&&elapsed>=24){elapsed=0;drawWorld(0);}paused=!paused;updateButton();syncPlayback();});
document.getElementById('world-replay').addEventListener('click',()=>{elapsed=0;drawWorld(0);paused=false;updateButton();syncPlayback();});
document.getElementById('world-next').addEventListener('click',()=>{const steps=[1,4,7.8,10.5,13,16,19.8,22.5];elapsed=steps.find(t=>t>elapsed+.1)??1;paused=true;drawWorld(elapsed);updateButton();syncPlayback();});
new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;syncPlayback();},{threshold:.15}).observe(svg);
document.addEventListener('visibilitychange',syncPlayback);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches){paused=true;elapsed=24;drawWorld(elapsed);updateButton();syncPlayback();}});

// RCML: shared sample identities move between illustrative relation-specific spaces.
const relationCard=document.getElementById('multimodal');
const relationPlot=relationCard.querySelector('.relation-space');
const relationButtons=[...relationCard.querySelectorAll('[data-embedding-relation]')];
const relationPlay=document.getElementById('relation-play');
const relationLayouts={
 tennis:{hat:[155,85],backpack:[65,145],racket:[155,215],rod:[285,65],reel:[285,235]},
 fishing:{hat:[195,85],backpack:[65,65],racket:[65,235],rod:[285,145],reel:[195,215]}
};
function relationTarget(mode){return relationLayouts[mode];}
function clusterBounds(points,mode){const group=mode==='tennis'?['hat','backpack','racket']:['hat','rod','reel'];const xs=group.map(k=>points[k][0]),ys=group.map(k=>points[k][1]);return {cx:(Math.min(...xs)+Math.max(...xs))/2,cy:(Math.min(...ys)+Math.max(...ys))/2,rx:(Math.max(...xs)-Math.min(...xs))/2+56,ry:(Math.max(...ys)-Math.min(...ys))/2+54};}
const relationCopy={tennis:['Tennis-related co-purchases','Tennis shoppers connect the backpack with the racket and sun hat.'],fishing:['Fishing-related co-purchases','Fishing shoppers connect the rod combo with the reel and the same sun hat.']};
let relationMode='tennis',relationPositions=structuredClone(relationTarget('tennis')),relationFrame=null,relationTimer=null,relationVisible=false,relationAuto=!reducedMotion.matches;
let relationCluster=clusterBounds(relationPositions,relationMode);
function paintRelation(points,bounds=clusterBounds(points,relationMode)){
 for(const [key,xy] of Object.entries(points))relationPlot.querySelector(`[data-item="${key}"]`).setAttribute('transform',`translate(${xy[0]} ${xy[1]})`);
 for(const line of relationPlot.querySelectorAll('.rc-distance')){const p=points[line.dataset.from],q=points[line.dataset.to];line.setAttribute('x1',p[0]);line.setAttribute('y1',p[1]);line.setAttribute('x2',q[0]);line.setAttribute('y2',q[1]);line.classList.toggle('close',line.dataset.relation===relationMode);}
 const cluster=relationPlot.querySelector('.rc-cluster');for(const [key,value] of Object.entries(bounds))cluster.setAttribute(key,value);relationCluster=bounds;
 relationPositions=points;
}
function setRelation(mode){
 relationMode=mode;relationCard.dataset.relation=mode;
 relationButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.embeddingRelation===mode)));
 document.getElementById('relation-name').textContent=relationCopy[mode][0];document.getElementById('relation-explanation').textContent=relationCopy[mode][1];
 document.getElementById('distance-backpack').textContent=mode==='tennis'?'Closer':'Farther';document.getElementById('distance-rod').textContent=mode==='fishing'?'Closer':'Farther';
 if(relationFrame!==null)cancelAnimationFrame(relationFrame);
 if(reducedMotion.matches){paintRelation(structuredClone(relationTarget(mode)));relationFrame=null;return;}
 const from=structuredClone(relationPositions),to=relationTarget(mode),oldCluster={...relationCluster},newCluster=clusterBounds(to,mode);let start=null;
 function animate(now){if(start===null)start=now;const t=ease((now-start)/850);const next={};for(const key of Object.keys(from))next[key]=from[key].map((v,i)=>v+(to[key][i]-v)*t);const bounds={};for(const key of Object.keys(oldCluster))bounds[key]=oldCluster[key]+(newCluster[key]-oldCluster[key])*t;paintRelation(next,bounds);if(t<1)relationFrame=requestAnimationFrame(animate);else relationFrame=null;}
 relationFrame=requestAnimationFrame(animate);
}
function scheduleRelation(){clearTimeout(relationTimer);relationTimer=null;if(relationAuto&&relationVisible&&!document.hidden)relationTimer=setTimeout(()=>{setRelation(relationMode==='tennis'?'fishing':'tennis');scheduleRelation();},3600);}
function relationButton(){relationPlay.textContent=relationAuto?'Pause':'Play';relationPlay.setAttribute('aria-label',relationAuto?'Pause relation animation':'Play relation animation');}
relationButtons.forEach(b=>b.addEventListener('click',()=>{setRelation(b.dataset.embeddingRelation);scheduleRelation();}));
relationPlay.hidden=false;relationPlay.addEventListener('click',()=>{relationAuto=!relationAuto;relationButton();if(relationAuto)setRelation(relationMode==='tennis'?'fishing':'tennis');scheduleRelation();});
new IntersectionObserver(entries=>{relationVisible=entries[0].isIntersecting;scheduleRelation();},{threshold:.1}).observe(relationPlot);
document.addEventListener('visibilitychange',scheduleRelation);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches){relationAuto=false;relationButton();scheduleRelation();setRelation(relationMode);}});
relationButton();paintRelation(structuredClone(relationTarget(relationMode)));
