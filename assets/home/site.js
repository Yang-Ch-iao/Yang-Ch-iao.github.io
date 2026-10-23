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
const ROUND_SECONDS=4,CYCLE_SECONDS=ROUND_SECONDS*2;
let elapsed=0,lastTime=null,frame=null,inView=false,paused=reducedMotion.matches;
const clamp=n=>Math.max(0,Math.min(1,n));
const ease=n=>{n=clamp(n);return n*n*(3-2*n);};
function drawWorld(t){
  // Fade generated content into the initial graph without a hold between cycles.
  const cycleFade=t<CYCLE_SECONDS?1-ease((t-(CYCLE_SECONDS-.35))/.35):1;
  for(const node of candidates){
    const local=t-(Number(node.dataset.round)-1)*ROUND_SECONDS;
    const rejected=node.classList.contains('mw-rejected');
    const appear=ease((local-.35)/.85);
    node.style.opacity=String(cycleFade*appear*(rejected?1-ease((local-2.6)/.4):1));
    node.classList.toggle('verified',local>=2.6&&!rejected);
    node.classList.toggle('rejected',local>=2.6&&rejected);
    node.querySelector('.mw-dot').setAttribute('r',String(6.5*(.8+.2*appear)));
  }
  for(const edge of edges){
    const local=t-(Number(edge.dataset.round)-1)*ROUND_SECONDS;
    const progress=ease((local-1.1)/1.5);
    // Earlier connections recede as the next batch is verified.
    const historyFade=1-.65*ease((local-ROUND_SECONDS)/.45);
    edge.style.opacity=String(progress>0?cycleFade*historyFade:0);
    edge.style.strokeDasharray='1';edge.style.strokeDashoffset=String(1-progress);
  }
  for(const anchor of anchors){
    const local=t-(Number(anchor.dataset.round)-1)*ROUND_SECONDS;
    anchor.style.opacity=String(ease(local/.35)*(1-ease((local-2.9)/1.1)));
  }
  const round=t<ROUND_SECONDS?1:2,local=t-(round-1)*ROUND_SECONDS;
  const labels=['Select a connected 5-molecule anchor context','Sample multiple candidates from the whole context','Verify MMP links to the current graph','Incorporate connected candidates; update the graph'];
  const index=local<.35?0:local<1.1?1:local<2.6?2:3;
  stage.textContent=`Round ${round} · ${index+1}/4 · ${labels[index]}`;
  world.querySelector('.mw-graph-caption').textContent=local<.35?'The highlighted five molecules form one connected context.':local<1.1?'The five-molecule context conditions a batch of candidates.':local<2.6?'Selected links show how new molecules connect back to the anchors.':'Only candidates with a verified link to the current graph are added.';
}
function updateButton(){toggle.textContent=paused?'Play':'Pause';toggle.setAttribute('aria-label',paused?'Play graph animation':'Pause graph animation');}
function canRun(){return inView&&!document.hidden&&!paused;}
function tick(now){frame=null;if(!canRun()){lastTime=null;return;}if(lastTime!==null)elapsed=(elapsed+(now-lastTime)/1000)%CYCLE_SECONDS;lastTime=now;drawWorld(elapsed);frame=requestAnimationFrame(tick);}
function syncPlayback(){if(canRun()&&frame===null){lastTime=null;frame=requestAnimationFrame(tick);}else if(!canRun()){if(frame!==null)cancelAnimationFrame(frame);frame=null;lastTime=null;}}
controls.hidden=false;elapsed=reducedMotion.matches?CYCLE_SECONDS:0;drawWorld(elapsed);updateButton();
toggle.addEventListener('click',()=>{if(paused&&elapsed>=CYCLE_SECONDS){elapsed=0;drawWorld(0);}paused=!paused;updateButton();syncPlayback();});
document.getElementById('world-replay').addEventListener('click',()=>{elapsed=0;drawWorld(0);paused=false;updateButton();syncPlayback();});
document.getElementById('world-next').addEventListener('click',()=>{const steps=[.25,.9,2.5,3.2,4.25,4.9,6.5,7.2];elapsed=steps.find(t=>t>elapsed+.1)??.25;paused=true;drawWorld(elapsed);updateButton();syncPlayback();});
new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;syncPlayback();},{threshold:.15}).observe(svg);
document.addEventListener('visibilitychange',syncPlayback);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches){paused=true;elapsed=CYCLE_SECONDS;drawWorld(elapsed);updateButton();syncPlayback();}});

// RCML: shared sample identities move between illustrative relation-specific spaces.
const relationCard=document.getElementById('multimodal');
const relationPlot=relationCard.querySelector('.relation-space');
const relationButtons=[...relationCard.querySelectorAll('[data-embedding-relation]')];
const relationPlay=document.getElementById('relation-play');
const relationLayouts={
 tennis:{hat:[135,85],backpack:[65,145],racket:[135,215],rod:[285,65],reel:[285,235]},
 fishing:{hat:[215,85],backpack:[65,235],racket:[65,65],rod:[285,145],reel:[215,215]}
};
function relationTarget(mode){return relationLayouts[mode];}
const relationCopy={tennis:['Tennis-related co-purchases','Under the tennis relation, the hat is nearer the backpack in embedding space.'],fishing:['Fishing-related co-purchases','Under the fishing relation, the hat moves nearer the rod combo and farther from the backpack.']};
let relationMode='tennis',relationPositions=structuredClone(relationTarget('tennis')),relationFrame=null,relationTimer=null,relationVisible=false,relationAuto=!reducedMotion.matches;
function paintRelation(points){
 for(const [key,xy] of Object.entries(points))relationPlot.querySelector(`[data-item="${key}"]`).setAttribute('transform',`translate(${xy[0]} ${xy[1]})`);
 for(const key of ['backpack','rod']){const distance=Math.hypot(points.hat[0]-points[key][0],points.hat[1]-points[key][1]);document.getElementById(`distance-bar-${key}`).style.width=`${distance/350*100}%`;}
 relationPositions=points;
}
function setRelation(mode){
 relationMode=mode;relationCard.dataset.relation=mode;
 relationButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.embeddingRelation===mode)));
 document.getElementById('relation-name').textContent=relationCopy[mode][0];document.getElementById('relation-explanation').textContent=relationCopy[mode][1];
 document.getElementById('distance-backpack').textContent=mode==='tennis'?'Closer':'Farther';document.getElementById('distance-rod').textContent=mode==='fishing'?'Closer':'Farther';
 if(relationFrame!==null)cancelAnimationFrame(relationFrame);
 if(reducedMotion.matches){paintRelation(structuredClone(relationTarget(mode)));relationFrame=null;return;}
 const from=structuredClone(relationPositions),to=relationTarget(mode);let start=null;
 function animate(now){if(start===null)start=now;const t=ease((now-start)/850);const next={};for(const key of Object.keys(from))next[key]=from[key].map((v,i)=>v+(to[key][i]-v)*t);paintRelation(next);if(t<1)relationFrame=requestAnimationFrame(animate);else relationFrame=null;}
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

// XAI-Refine: follow the accepted-update feedback loop without implying every update passes.
const xaiCard=document.getElementById('xai-refine');
const xaiToggle=document.getElementById('xai-toggle');
let xaiPaused=reducedMotion.matches,xaiVisible=false;
function syncXaiLoop(){xaiCard.classList.toggle('loop-running',xaiVisible&&!document.hidden&&!xaiPaused);xaiToggle.textContent=xaiPaused?'Play':'Pause';xaiToggle.setAttribute('aria-label',xaiPaused?'Play XAI refinement loop':'Pause XAI refinement loop');}
xaiToggle.hidden=false;xaiCard.classList.add('has-loop-motion');
xaiToggle.addEventListener('click',()=>{xaiPaused=!xaiPaused;syncXaiLoop();});
new IntersectionObserver(entries=>{xaiVisible=entries[0].isIntersecting;syncXaiLoop();},{threshold:.15}).observe(xaiCard);
document.addEventListener('visibilitychange',syncXaiLoop);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches)xaiPaused=true;syncXaiLoop();});syncXaiLoop();

// Jump from a research direction to its papers in the full publication list.
document.querySelectorAll('[data-publication-filter]').forEach(link=>link.addEventListener('click',()=>{const button=filters.find(button=>button.dataset.filter===link.dataset.publicationFilter);if(button)button.click();}));
