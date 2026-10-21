"""Build the GitHub Pages homepage with Python's standard library. Run python3 build_home.py."""
from pathlib import Path
from html import escape
import json
import math

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())
def esc(value): return escape(value, quote=True)
def heading(n, title): return f'<div class="section-heading"><span class="number">{n}</span><h2>{title}</h2></div>'
def external(label, url): return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
def pub_html(p):
    title = external(esc(p['title']), p['url']) if p['url'] else esc(p['title'])
    authors = ''.join(('<strong>' + esc(t) + '</strong>') if i % 2 else esc(t) for i,t in enumerate(p['authors'].split('**')))
    links = external('Paper',p['url']) if p['url'] else ''
    if p['title'].startswith('EnterpriseSaga'): links = external('Project & leaderboard',data['enterprise'])
    status = '<p class="pub-status">Accepted · Findings of EMNLP 2026</p>' if 'accepted' in p['status'] else ''
    if 'revised' in p['status']:
        year = p['status'].split('revised ')[1].strip('.')
        status = f'<p class="pub-status">Revised {esc(year)}</p>'
    return f'<article class="publication" data-category="{p["category"]}"><div class="venue">{p["venue"]}</div><div><h3 class="pub-title">{title}</h3><p class="authors">{authors}</p><div class="text-links">{links}</div>{status}</div></article>'

def molecule(x,y,active=False):
    points=[(x+13*math.cos(i*math.pi/3),y+13*math.sin(i*math.pi/3)) for i in range(6)]
    lines=''.join(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>' for a,b in zip(points,points[1:]+points[:1]))
    circles=''.join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3"/>' for a,b in points)
    return f'<g class="molecule {"active" if active else ""}">{lines}{circles}</g>'

enterprise_svg='''<svg viewBox="0 0 320 175" role="img" aria-label="Conceptual example of linking a decision, a later change, and an outcome across enterprise systems.">
<path d="M53 150H303" stroke="#c8cbc0"/><text x="260" y="167" class="label">time →</text>
<text x="0" y="32">Email</text><text x="0" y="79">Ticket</text><text x="0" y="126">Docs</text>
<g stroke="#e0e2d8" stroke-dasharray="2 4"><path d="M53 35H305M53 82H305M53 129H305"/><path d="M85 15V147M172 15V147M260 15V147"/></g>
<path class="evidence-edge" data-step="2" d="M105 36C132 36 126 77 153 77"/><path class="evidence-edge" data-step="3" d="M191 79C222 79 216 126 244 126"/>
<g class="node" data-step="1"><rect x="57" y="19" width="61" height="30" rx="5"/><text x="87" y="38" text-anchor="middle">Decision</text></g>
<g class="node" data-step="2"><rect x="141" y="63" width="64" height="30" rx="5"/><text x="173" y="82" text-anchor="middle">Change</text></g>
<g class="node" data-step="3"><rect x="231" y="111" width="66" height="30" rx="5"/><text x="264" y="130" text-anchor="middle">Outcome</text></g>
<g class="node" data-step="0" opacity=".45"><rect x="241" y="20" width="46" height="24" rx="4"/><text x="264" y="36" class="label" text-anchor="middle">other</text><rect x="64" y="111" width="46" height="24" rx="4"/><text x="87" y="127" class="label" text-anchor="middle">other</text></g></svg>'''

world_svg=f'''<svg viewBox="0 0 320 175" role="img" aria-label="Conceptual molecule-transfer graph: a world model predicts an expansion and a verified candidate joins the graph.">
<path class="world-edge" d="M54 88L119 43L169 105L54 88M119 43L169 105"/>
{molecule(54,88)}{molecule(119,43)}{molecule(169,105)}
<text x="34" y="123" class="label">known</text>
<g class="world-future" data-step="1"><path d="M169 105L249 56" class="world-edge"/>{molecule(249,56,True)}<text x="226" y="25" class="label">candidate</text></g>
<g class="world-future" data-step="2"><circle cx="249" cy="56" r="23" fill="none" stroke="#4d58a6" stroke-width=".8"/></g>
<g class="world-future" data-step="3"><path d="M169 105L249 56" stroke="#4d58a6" stroke-width="2"/><text x="202" y="113" class="label">verified MMP</text><path d="M271 66l4 4 8-10" fill="none" stroke="#4d58a6" stroke-width="2"/></g>
<text x="13" y="162" class="label">molecules = nodes · MMP relations = edges</text></svg>'''

def scene(x,y,color,kind,outdoor):
    base=f'<g transform="translate({x},{y})"><rect class="relation-node" width="94" height="58" rx="5"/>'
    if outdoor: base+='<path d="M5 46L28 26L48 46L68 30L89 46" fill="#e9ecdf"/><circle cx="78" cy="12" r="5" fill="#dddcc5"/>'
    else: base+='<path d="M9 44V9H85V44" fill="none" stroke="#e6e6df"/><path d="M46 9V44M9 23H85" stroke="#e6e6df"/>'
    if kind=='bird': base+=f'<path d="M30 31Q32 15 48 24L53 20L55 25L63 29L55 32Q49 43 37 36L25 40Z" fill="{color}"/><circle cx="51" cy="26" r="1.4" fill="white"/>'
    else: base+=f'<path d="M25 32H70L61 41H34Z" fill="{color}"/><path d="M46 13V31H30Z" fill="{color}" opacity=".7"/>'
    return base+'</g>'

relation_svg=f'''<svg viewBox="0 0 320 175" role="img" aria-label="Four illustrated images. A blue outdoor bird can relate to a red indoor bird by object, a blue indoor boat by color, or a red outdoor boat by scene.">
<path class="relation-edge visible" data-edge="object" d="M114 39H206"/><path class="relation-edge" data-edge="color" d="M67 68V107"/><path class="relation-edge" data-edge="scene" d="M111 63L210 111"/>
{scene(20,10,'#667bb9','bird',True)}{scene(206,10,'#b97c70','bird',False)}{scene(20,107,'#667bb9','boat',False)}{scene(206,107,'#b97c70','boat',True)}
<text x="67" y="82" text-anchor="middle" class="label">anchor</text></svg>'''

nav_items=[('about','00','About'),('research','01','Research'),('publications','02','Publications'),('experience','03','Experience'),('education','04','Education'),('service','05','Service'),('teaching','06','Teaching')]
nav=''.join(f'<a href="#{id}"><span>{num}</span>{name}</a>' for id,num,name in nav_items)
pubs=''.join(pub_html(p) for p in data['publications'])
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yang Qiao · Machine Learning Research · Emory University</title>
<meta name="description" content="Yang Qiao is a Ph.D. student at Emory University working on LLM agents and retrieval, AI for science, and multimodal learning.">
<meta property="og:title" content="Yang Qiao · Machine Learning Research"><meta property="og:description" content="LLM agents and retrieval · AI for science · Multimodal learning. Ph.D. student at Emory University."><meta property="og:type" content="website"><meta property="og:url" content="https://yang-ch-iao.github.io/"><meta property="og:image" content="https://yang-ch-iao.github.io/images/profile.jpg">
<link rel="canonical" href="https://yang-ch-iao.github.io/"><link rel="icon" href="assets/home/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/home/site.css"><script src="assets/home/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<aside class="sidebar" aria-label="Site navigation"><a class="brand" href="#about">Yang Qiao</a><div class="side-description">Ph.D. student · Emory<br>LLM agents & retrieval<br>AI for science<br>Multimodal learning</div><nav aria-label="Sections">{nav}</nav><div class="side-bottom"><a href="mailto:{data['email']}">Email ↗</a><a href="{data['scholar']}" target="_blank" rel="noopener noreferrer">Google Scholar ↗</a><a href="files/Yang_Qiao_CV.pdf" target="_blank">Curriculum vitae ↗</a><div class="copyright">Atlanta, GA<br>© 2026 Yang Qiao</div></div></aside>
<header class="mobile-header"><a class="brand" href="#about">Yang Qiao</a><div><a href="#research">Research</a><a href="#publications">Papers</a><a href="files/Yang_Qiao_CV.pdf">CV ↗</a></div></header>
<main id="main"><div class="hero" id="about"><div class="hero-copy"><div class="hero-title"><div class="eyebrow">Machine learning · Emory University</div><h1>Yang Qiao <span class="name-cn" lang="zh">乔炀</span></h1><div class="research-tags">LLM agents & retrieval · AI for science · Multimodal learning</div></div><div class="hero-body"><p class="intro">I build machine learning methods for retrieving evidence, modeling scientific systems, and understanding relationships across modalities.</p><p class="bio">I'm a Ph.D. student in Computer Science and Informatics at Emory University, advised by <a href="https://cs.emory.edu/~lzhao41/">Liang Zhao</a>. Previously, I studied computer science and physics at Shandong University.</p><div class="hero-links"><a class="pill primary" href="mailto:{data['email']}">Email ↗</a><a class="pill" href="{data['scholar']}" target="_blank" rel="noopener noreferrer">Scholar ↗</a><a class="pill" href="files/Yang_Qiao_CV.pdf" target="_blank">CV ↓</a><a class="pill" href="{data['linkedin']}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a></div><p class="availability">Seeking research / applied science internships for Summer 2027.</p></div></div><div class="hero-photo"><div class="portrait-frame"><img class="portrait" src="images/profile.jpg" alt="Yang Qiao" width="170" height="220" fetchpriority="high"></div><div class="photo-note">Atlanta, Georgia</div></div></div>

<section id="research">{heading('01','Research')}<p class="section-note">Three directions, from evidence-grounded reasoning to scientific world models.</p>
<article class="research-card" id="enterprise-demo"><div class="diagram"><div class="diagram-label"><span>Cross-system evidence</span><div class="controls"><button class="small-button" id="evidence-play" aria-pressed="false">Play</button><button class="small-button" id="evidence-next" aria-label="Next evidence step">Step →</button></div></div>{enterprise_svg}<div class="step-status" id="evidence-status" aria-live="polite">Select a question to trace its evidence.</div><div class="diagram-note">Conceptual example · How did the decision change?</div></div><div class="card-copy"><div class="category">01 / LLM AGENTS & RETRIEVAL</div><h3>Reasoning over evolving enterprise knowledge</h3><p>EnterpriseSaga tests how agents retrieve evidence and reason across systems and time. I led its development: a 1.213-billion-token synthetic enterprise benchmark with 966 evidence-grounded questions and seven retrieval pipelines and agents.</p><div class="partner">Research internship · Causal Dynamics Lab</div><div class="text-links">{external('Project & leaderboard',data['enterprise'])}<a href="#publications">Manuscript ↓</a></div></div></article>

<article class="research-card"><div class="diagram"><div class="diagram-label"><span>A molecule-transfer graph</span><span>Explore ↓</span></div>{world_svg}<label class="sr-label" for="world-step" hidden>Graph expansion stage</label><input type="range" id="world-step" min="0" max="3" step="1" value="0" aria-label="Molecule graph expansion stage"><div class="step-status" id="world-status" aria-live="polite"></div><div class="diagram-note">Conceptual illustration · molecular structures are schematic</div></div><div class="card-copy"><div class="category">02 / AI FOR SCIENCE</div><h3>World models for molecular optimization</h3><p>MolWorld introduces molecule-transfer graphs for sequential molecular optimization. A world model predicts local graph expansion to guide generation, while verified matched molecular pair relations keep new candidates connected to known molecules.</p><div class="partner">Research collaboration with Merck & Co., Inc.</div><div class="text-links">{external('MolWorld paper','https://arxiv.org/abs/2605.08954')}<a href="#science-more">More scientific applications ↓</a></div></div></article>

<article class="research-card"><div class="diagram"><div class="diagram-label"><span>Change the relation</span></div><div class="controls" style="margin-top:8px" role="group" aria-label="Semantic relation"><button class="small-button" data-relation="object" aria-pressed="true">Object</button><button class="small-button" data-relation="color" aria-pressed="false">Color</button><button class="small-button" data-relation="scene" aria-pressed="false">Scene</button></div>{relation_svg}<div class="step-status" id="relation-status" aria-live="polite">Object relation · connect the two bird images.</div><div class="diagram-note">Conceptual example · one sample, different relations</div></div><div class="card-copy"><div class="category">03 / MULTIMODAL LEARNING</div><h3>Representations that depend on the relation</h3><p>RCML conditions multimodal representations on natural-language relations, so the same sample can express different aspects of relevance. Its contrastive objective connects image–text alignment with many-to-many relations across samples.</p><div class="partner">Related work: MILNet · multimodal sarcasm detection</div><div class="text-links">{external('RCML paper','https://arxiv.org/abs/2508.17497')}{external('MILNet · AAAI 2023','https://ojs.aaai.org/index.php/AAAI/article/view/26138')}</div></div></article>

<div class="related-work" id="science-more"><article><h3>XAI-Refine</h3><p>An explanation–knowledge loop that verifies brain-age model explanations against neuroscience literature and turns that evidence into targeted training constraints.</p><p>With Emory Radiology and Neurology.</p><div class="text-links">{external('Paper','https://arxiv.org/abs/2609.09388')}</div></article><article><h3>Human behavior simulation</h3><p>I proposed a world-model formulation that separates stable psychometric traits from evolving behavioral states, using observed transitions as training supervision.</p><p>With Emory Psychiatry and Behavioral Sciences.</p><div class="text-links"><a href="#publications">Manuscript ↓</a></div></article></div></section>

<section id="publications">{heading('02','Publications & manuscripts')}<div class="filters" role="group" aria-label="Filter publications"><button class="filter" data-filter="all" aria-pressed="true">All</button><button class="filter" data-filter="agents" aria-pressed="false">Agents & retrieval</button><button class="filter" data-filter="science" aria-pressed="false">AI for science</button><button class="filter" data-filter="multimodal" aria-pressed="false">Multimodal</button><button class="filter" data-filter="causal" aria-pressed="false">Causal representations</button></div><p class="filter-count" id="publication-count" aria-live="polite">8 publications and manuscripts</p>{pubs}<p class="scholar-note">Also on <a href="{data['scholar']}" target="_blank" rel="noopener noreferrer">Google Scholar ↗</a></p></section>

<section id="experience">{heading('03','Experience')}<div class="timeline-row"><h3>Causal Dynamics Lab <span class="role">· Research Intern</span></h3><span class="date">May – Aug 2026</span><p class="timeline-copy">Led EnterpriseSaga from benchmark design and synthetic company simulation to retrieval implementation and evaluation. Built a setting for testing evidence retrieval and reasoning over evolving enterprise knowledge. {external('Project',data['enterprise'])}</p></div></section>

<section id="education">{heading('04','Education')}<div class="timeline-row"><h3>Emory University</h3><span class="date">2024 – present</span><p class="detail">Ph.D. in Computer Science and Informatics · Expected 2029<br>Advisor: Liang Zhao</p></div><div class="timeline-row"><h3>Shandong University</h3><span class="date">2021 – 2024</span><p class="detail">Master's in Computer Science and Technology<br>Advisor: Xuemeng Song · Co-advisor: Liqiang Nie</p></div><div class="timeline-row"><h3>Shandong University</h3><span class="date">2016 – 2020</span><p class="detail">B.Sc. in Physics</p></div></section>

<section id="service">{heading('05','Academic service')}<div class="service-grid"><div><h3>JOURNAL REVIEWER</h3><p>IEEE Transactions on Multimedia</p><p>IET Image Processing</p></div><div><h3>CONFERENCE REVIEWER</h3><p>NeurIPS</p></div></div></section>

<section id="teaching">{heading('06','Teaching')}<p class="section-note">Teaching Assistant · Emory University</p><div class="teaching-line"><strong>CS 325 · Artificial Intelligence</strong><span class="date">Spring 2026 · Fall 2025</span></div><div class="teaching-line"><strong>CS 253 · Data Structures and Algorithms</strong><span class="date">Spring 2025</span></div></section>
<footer><a href="mailto:{data['email']}">{data['email']}</a><a class="back-top" href="#about">Back to top ↑</a></footer></main></body></html>'''
(ROOT/'index.html').write_text(html)
print('Built index.html with',len(data['publications']),'publications.')
