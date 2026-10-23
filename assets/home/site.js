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
function resizeFigure(){svg.setAttribute('viewBox',mobileFigure.matches?'0 0 460 855':'0 0 730 425');svg.classList.toggle('mobile-layout',mobileFigure.matches);}
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
  world.querySelector('.mw-region-1').style.opacity=String(ease((t-9)/1.2));
  world.querySelector('.mw-region-2').style.opacity=String(ease((t-21)/1.2));
  const round=t<12?1:2,local=t-(round-1)*12;
  const labels=['Select a connected 5-molecule anchor context','Sample multiple candidates from the whole context','Verify MMP links to the current graph','Incorporate connected candidates; update the graph'];
  const index=local<3?0:local<6?1:local<9?2:3;
  stage.textContent=`Round ${round} · ${index+1}/4 · ${labels[index]}`;
  world.querySelector('.mw-graph-caption').textContent=local<3?'The highlighted five molecules form one connected context.':local<6?'Candidates are sampled together; connections are not assigned yet.':local<9?'Links can reach molecules outside the selected anchor.':'Only candidates with a verified link to the current graph are added.';
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
