'use strict';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const navLinks = [...document.querySelectorAll('.sidebar nav a')];
const sections = [...document.querySelectorAll('main > [id]')];
function updateNavigation(){let current=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<180)current=section;}navLinks.forEach(link=>{const active=link.hash==='#'+current.id;link.classList.toggle('active',active);if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});}
window.addEventListener('scroll',updateNavigation,{passive:true});updateNavigation();
const filters=[...document.querySelectorAll('.filter')];
filters.forEach(button=>button.addEventListener('click',()=>{const category=button.dataset.filter;let count=0;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.publication').forEach(p=>{p.hidden=category!=='all'&&p.dataset.category!==category;if(!p.hidden)count++;});document.getElementById('publication-count').textContent=`${count} publications and manuscripts`; }));

// MolWorld Fig. 1: whole molecules join through verified MMP links.
// Timing and coordinates explain the construction; they are not an experimental rollout.
const world = document.getElementById('molworld');
const svg = world.querySelector('.molworld-svg');
const controls = document.getElementById('world-controls');
const toggle = document.getElementById('world-toggle');
const replay = document.getElementById('world-replay');
const stage = document.getElementById('world-stage');
const nodes = [...world.querySelectorAll('.mw-node:not(.cohort-0)')];
const edges = [...world.querySelectorAll('.mw-growing-edge')];
const earlyField = world.querySelector('.mw-field-early');
const lateField = world.querySelector('.mw-field-late');
const detail = [...world.querySelectorAll('.mw-detail-ring,.mw-detail-guide')];
const mobileFigure = window.matchMedia('(max-width:540px)');
function resizeFigure(){svg.setAttribute('viewBox',mobileFigure.matches?'0 0 440 675':'0 0 730 388');svg.classList.toggle('mobile-layout',mobileFigure.matches);}
mobileFigure.addEventListener('change',resizeFigure);resizeFigure();
let elapsed=0,lastTime=null,frame=null,inView=false,paused=reducedMotion.matches;
const clamp=n=>Math.max(0,Math.min(1,n));
function drawWorld(t){
  edges.forEach(edge=>{edge.style.strokeDashoffset=String(1-clamp((t-Number(edge.dataset.at))/.45));});
  nodes.forEach(node=>{const progress=clamp((t-Number(node.dataset.at))/.3);node.style.opacity=String(progress);node.querySelector('circle').setAttribute('r',String(6.3*(.6+.4*progress)));});
  earlyField.style.opacity=String(clamp((t-1.5)/1.8));
  lateField.style.opacity=String(clamp((t-6.7)/2));
  detail.forEach(el=>el.style.opacity=String(clamp((t-7)/1.5)));
  stage.textContent=t<1.8?'Begin with connected original molecules':t<7?'Earlier generation · extend the starting series':t<12?'Later generation · expand through connected paths':'New molecules remain reachable from the starting series';
}
function updateButton(){toggle.textContent=paused?'Play':'Pause';toggle.setAttribute('aria-label',paused?'Play graph animation':'Pause graph animation');}
function canRun(){return inView&&!document.hidden&&!paused;}
function tick(now){frame=null;if(!canRun()){lastTime=null;return;}if(lastTime!==null)elapsed+=(now-lastTime)/1000;lastTime=now;if(elapsed>17)elapsed=0;drawWorld(elapsed);frame=requestAnimationFrame(tick);}
function syncPlayback(){if(canRun()&&frame===null){lastTime=null;frame=requestAnimationFrame(tick);}else if(!canRun()){if(frame!==null)cancelAnimationFrame(frame);frame=null;lastTime=null;}}
controls.hidden=false;
if(reducedMotion.matches){elapsed=13;drawWorld(elapsed);}else drawWorld(0);
updateButton();
toggle.addEventListener('click',()=>{paused=!paused;updateButton();syncPlayback();});
replay.addEventListener('click',()=>{elapsed=0;drawWorld(0);paused=false;updateButton();syncPlayback();});
new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;syncPlayback();},{threshold:.15}).observe(svg);
document.addEventListener('visibilitychange',syncPlayback);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches){paused=true;elapsed=13;drawWorld(elapsed);updateButton();syncPlayback();}});
