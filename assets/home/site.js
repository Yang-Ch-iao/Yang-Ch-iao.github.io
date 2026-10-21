'use strict';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const navLinks = [...document.querySelectorAll('.sidebar nav a')];
const sections = [...document.querySelectorAll('main > [id]')];
function updateNavigation(){let current=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<180)current=section;}navLinks.forEach(link=>{const active=link.hash==='#'+current.id;link.classList.toggle('active',active);if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});}
window.addEventListener('scroll',updateNavigation,{passive:true});updateNavigation();
const filters=[...document.querySelectorAll('.filter')];
filters.forEach(button=>button.addEventListener('click',()=>{const category=button.dataset.filter;let count=0;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.publication').forEach(p=>{p.hidden=category!=='all'&&p.dataset.category!==category;if(!p.hidden)count++;});document.getElementById('publication-count').textContent=`${count} publications and manuscripts`; }));

// These are explanatory diagrams, not live benchmark traces or experimental results.
const enterprise=document.getElementById('enterprise-demo');
const evidenceDescriptions=['Select a question to trace its evidence.','1 / 3 · Locate the original decision.','2 / 3 · Find the later change in another system.','3 / 3 · Link the evidence across systems and time.'];
let evidenceStep=0,evidenceTimer=null;
function setEvidenceStep(step){evidenceStep=step;enterprise.querySelectorAll('.node').forEach(n=>n.classList.toggle('highlight',Number(n.dataset.step)<=step&&Number(n.dataset.step)>0));enterprise.querySelectorAll('.evidence-edge').forEach(n=>n.classList.toggle('visible',Number(n.dataset.step)<=step));document.getElementById('evidence-status').textContent=evidenceDescriptions[step];}
function stopEvidence(){clearInterval(evidenceTimer);evidenceTimer=null;document.getElementById('evidence-play').textContent='Play';document.getElementById('evidence-play').setAttribute('aria-pressed','false');}
document.getElementById('evidence-next').addEventListener('click',()=>{stopEvidence();setEvidenceStep((evidenceStep+1)%4);});
document.getElementById('evidence-play').addEventListener('click',()=>{if(evidenceTimer){stopEvidence();return;}setEvidenceStep(evidenceStep===3?0:evidenceStep+1);document.getElementById('evidence-play').textContent='Pause';document.getElementById('evidence-play').setAttribute('aria-pressed','true');evidenceTimer=setInterval(()=>{if(evidenceStep===3)stopEvidence();else setEvidenceStep(evidenceStep+1);},1500);});

const worldSlider=document.getElementById('world-step');
const worldDescriptions=['0 / 3 · Begin with connected known molecules.','1 / 3 · Predict a possible local graph expansion.','2 / 3 · Generate a candidate from the selected context.','3 / 3 · Add a candidate linked by a verified MMP relation.'];
function updateWorld(){let step=Number(worldSlider.value);document.querySelectorAll('.world-future').forEach(n=>{const threshold=Number(n.dataset.step);n.classList.toggle('visible',step>=threshold);n.classList.toggle('predicted',step===1&&threshold===1);});document.getElementById('world-status').textContent=worldDescriptions[step];worldSlider.setAttribute('aria-valuetext',worldDescriptions[step]);}
worldSlider.addEventListener('input',updateWorld);updateWorld();
const relationButtons=[...document.querySelectorAll('[data-relation]')];
const relationDescriptions={object:'Object relation · connect the two bird images.',color:'Color relation · connect the two blue images.',scene:'Scene relation · connect the outdoor scenes.'};
relationButtons.forEach(button=>button.addEventListener('click',()=>{relationButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.relation-edge').forEach(e=>e.classList.toggle('visible',e.dataset.edge===button.dataset.relation));document.getElementById('relation-status').textContent=relationDescriptions[button.dataset.relation];}));
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopEvidence();});
new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stopEvidence();}).observe(enterprise);
reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches)stopEvidence();});
