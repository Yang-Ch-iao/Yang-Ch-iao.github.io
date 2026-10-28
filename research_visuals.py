"""Paper-grounded figures for the homepage. Coordinates are illustrative, not measured data."""
import math
import json
from pathlib import Path

def molworld_figure():
    # One illustrative context per round; the method may select multiple contexts.
    # Accepted candidates have a verified edge to the graph as it existed BEFORE that round.
    # Node centers and region curves use the original introduction figure coordinates.
    paper_nodes=[(177.955,245.92),(188.535,229.82),(210.865,236.455),(211.745,256.72),(192.305,265.505),
                 (176.345,289.375),(140.515,230.555),(212.345,295.295),(226.145,276.105),(212.855,214.425),
                 (181.305,206.885),(151.995,265.11),(236.78,249.705),(134.025,253.29),(162.965,203.385),
                 (152.705,283.165),(278,210),(180.795,318.065),(225.095,310.42),(189.525,185.57),(236.385,229.82),(278,280)]
    nodes=[(75+(x-119)*2.25,18+(332-y)*2.25) for x,y in paper_nodes]
    initial_edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(5,4),(5,0)]
    anchor_sets=[{0,1,2,3,4},{0,4,5,6,11},{0,4,5,11,15}]
    # Draw representative verified links, not every possible MMP connection.
    # Each batch links back to a connected context available before generation.
    displayed_edges={
        1:[(a,6) for a in [0,1,2,3,4]]+
          [(2,7),(3,7),(4,7),(2,8),(3,8),(4,8),
           (0,9),(1,9),(2,9),(0,10),(1,10),(2,10),
           (0,11),(1,11),(4,11),(5,11),(6,11),(7,8),(9,10)],
        2:[(a,12) for a in [0,4,5,6,11]]+
          [(0,13),(6,13),(11,13),(0,14),(4,14),(6,14),
           (0,15),(4,15),(11,15)],
        3:[(a,17) for a in [0,4,5,11,15]]+
          [(4,18),(5,18),(15,18),(0,19),(4,19),(11,19),
           (0,20),(4,20),(11,20)]}
    rejected = {16,21}
    def edge(a,b,classes,round_num=0):
        x,y=nodes[a];xx,yy=nodes[b]
        return f'<path class="{classes}" data-round="{round_num}" data-from="{a}" data-to="{b}" pathLength="1" d="M{x} {y}L{xx} {yy}"/>'
    lines = [edge(a,b,'mw-initial-edge') for a,b in initial_edges]
    for r,pairs in displayed_edges.items():
        lines += [edge(a,b,'mw-verified-edge '+('mw-anchor-link' if a in anchor_sets[r-1] else 'mw-other-link'),r) for a,b in pairs]
    # Highlight only actual edges inside the chosen connected five-node context.
    anchor_edges=[]
    all_edges=list(initial_edges)
    for r,selected in enumerate(anchor_sets,1):
        anchor_edges += [edge(a,b,'mw-anchor-edge',r) for a,b in all_edges if a in selected and b in selected]
        all_edges += displayed_edges[r]
    dots=[]
    for i,(x,y) in enumerate(nodes):
        r=0 if i<6 else 1 if i<12 else 2 if i<17 else 3
        classes='mw-node '+('mw-existing' if r==0 else 'mw-candidate')+(' mw-rejected' if i in rejected else '')
        title='Original molecule' if r==0 else 'Candidate with no verified link; not incorporated' if i in rejected else 'Generated candidate; incorporated only after MMP verification'
        dots.append(f'<g class="{classes}" data-node="{i}" data-round="{r}" transform="translate({x} {y})"><title>{title}</title><circle class="mw-dot" r="6.5"/>')
        for ar,selected in enumerate(anchor_sets,1):
            if i in selected: dots.append(f'<circle class="mw-anchor-ring" data-round="{ar}" r="11"/>')
        if i in rejected:dots.append('<path class="mw-reject-mark" d="M-3-3L3 3M-3 3L3-3"/>')
        dots.append('</g>')
    geometry=json.loads((Path(__file__).parent/'assets/home/data/molworld-intro.json').read_text())
    contours=[geometry[key]['path'] for key in ['inner','middle','outer']]
    def structure(y,variable):
        ring=' '.join(f'{526+20*math.cos(k*math.pi/3):.1f},{y+20*math.sin(k*math.pi/3):.1f}' for k in range(6))
        return f'''<rect x="495" y="{y-38}" width="165" height="70" rx="23" fill="#e8efec"/>
        <polygon points="{ring}" fill="none" stroke="#425650" stroke-width="1.5"/>
        <circle cx="526" cy="{y}" r="13" fill="none" stroke="#425650" stroke-width="1"/>
        <path d="M546 {y}L563 {y}M580 {y}H603M603 {y}L624 {y}M601 {y-4}V{y-22}M605 {y-4}V{y-22}" stroke="#425650" stroke-width="1.5" fill="none"/>
        <text x="572" y="{y+4}" text-anchor="middle" class="chem">NH</text><text x="603" y="{y-27}" text-anchor="middle" class="chem">O</text>
        <circle cx="641" cy="{y}" r="21" fill="{('#f2ddd4' if variable=='H' else '#e5e2f2')}"/><text x="641" y="{y+5}" text-anchor="middle" class="chem">{variable}</text>'''
    return f'''<svg viewBox="0 0 730 445" class="molworld-svg" role="img" aria-labelledby="mw-title mw-desc">
    <title id="mw-title">Select a connected context, generate a batch, then verify its connections</title><desc id="mw-desc">Three illustrative rounds begin with six original molecules, shown in blue. Five connected molecules are selected from the current graph as an anchor context. Multiple candidates are sampled together without predetermined edges. Accepted candidates typically connect to most or all five anchor molecules, with occasional additional links to other molecules. Only representative verified links are drawn to avoid clutter: one candidate per round shows all five anchor links, while the others show several representative connections. New candidates appear green; accepted molecules turn white before the next round. No generated molecules are present at the beginning. These illustrative links appear after MMP verification. Candidates without a verified connection to the current graph are not incorporated. A new five-node context can include previously accepted molecules.</desc>
    <defs><linearGradient id="mw-property-reference" x1="0%" x2="100%"><stop stop-color="#fff0ba"/><stop offset=".5" stop-color="#ffd59e"/><stop offset="1" stop-color="#ce2b1d"/></linearGradient><marker id="mw-property-tip" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ce2b1d"/></marker><linearGradient id="mw-field-base" x2="1" y2="1"><stop stop-color="#f8f2e7"/><stop offset="1" stop-color="#f2e8d5"/></linearGradient><linearGradient id="mw-field-one" x2="1" y2="1"><stop stop-color="#f4ead7"/><stop offset="1" stop-color="#e9d8bd"/></linearGradient><linearGradient id="mw-field-two" x2="1" y2="1"><stop stop-color="#f2e5de"/><stop offset="1" stop-color="#e6cfc3"/></linearGradient><marker id="mw-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7f9084"/></marker></defs>
    <g class="mw-graph">
    <path class="mw-region mw-region-2" d="{contours[2]}"/><path class="mw-region mw-region-1" d="{contours[1]}"/><path class="mw-region mw-region-0" d="{contours[0]}"/>
    {''.join(lines)}{''.join(anchor_edges)}{''.join(dots)}
    </g>
    <rect x="145" y="408" width="174" height="6" fill="url(#mw-property-reference)"/><path d="M315 411H330" stroke="#ce2b1d" stroke-width="6" marker-end="url(#mw-property-tip)"/><text x="237" y="432" text-anchor="middle" class="figure-small">Higher property</text>
    <g class="mw-inset"><text x="490" y="43" class="figure-heading">What does an edge mean?</text><text x="490" y="65" class="figure-small">A verified local structural modification</text>
    {structure(124,'H')}{structure(226,'CH₃')}
    <path d="M575 163V181" stroke="#5d6965" marker-end="url(#mw-arrow)"/><text x="585" y="177" class="figure-small">H → CH₃</text>
    <text x="490" y="284" class="figure-small">Shared scaffold, changed fragment.</text><text x="490" y="303" class="figure-small">MMP = matched molecular pair.</text>
    <path d="M491 335H522" stroke="#758a7e" stroke-width="1.4"/><text x="533" y="339" class="figure-small">Selected verified links</text>
    <circle cx="506" cy="365" r="6.5" fill="#e2f0d9" stroke="#385623" stroke-dasharray="2 2"/><text x="533" y="369" class="figure-small">Candidate awaiting verification</text></g>
    </svg>'''

ENTERPRISE = '''<figure class="saga-figure" aria-label="EnterpriseSaga construction: Clearpath’s shared company history, activity-grounded records, questions and evidence, followed by question-conditioned augmentation">
<div class="saga-history"><strong>Clearpath</strong><p>A simulated B2B SaaS company for customer support and service operations.</p></div>
<div class="saga-scale">18 months <span>·</span> 12 systems <span>·</span> 1.213B tokens</div>
<div class="saga-generation"><div class="saga-activities">
<div><strong>Projects</strong><span>Projects → subprojects → episodes</span></div>
<div><strong>Recurring operations</strong><span>Streams → archetypes → episodes</span></div>
</div>
<span class="saga-across" aria-hidden="true">→</span>
<div class="saga-records"><strong>Shared facts, different records</strong><div class="saga-sources"><span>Slack</span><span>Jira</span><span>Email</span><span>Salesforce</span><span class="saga-other">+8 systems</span></div></div>
</div>
<div class="saga-questions"><strong>966 questions with traceable evidence</strong><div class="saga-question-types"><div><b>Multi-hop</b><span>Follow evidence from one record to the next.</span></div><div><b>Synthesis</b><span>Combine complementary facts within a shared scope.</span></div></div><p class="saga-support">Reference answers and claims link to supporting files, including alternative sufficient evidence sets.</p></div>
<figcaption class="saga-augmentation"><strong>Question-conditioned augmentation</strong><p>Add comparable activities with different dates, versions, or participants; recheck conflicts and unintended support, then update the evidence annotations.</p></figcaption>
</figure>'''

def rcml_figure(baseline=False):
    # Figure 1's fixed-vs-conditioned contrast, with Figure 2(a)'s product photos.
    prefix='rc-base' if baseline else 'rc'
    positions=({'hat':(175,145),'backpack':(65,65),'racket':(65,235),'rod':(285,65),'reel':(285,235)} if baseline else
               {'hat':(135,85),'backpack':(65,145),'racket':(135,215),'rod':(285,65),'reel':(285,235)})
    items=[('hat','Sun hat',(375,277,109,75)),('backpack','Backpack',(97,196,93,95)),('racket','Racket',(405,68,97,102)),('rod','Rod combo',(334,484,80,83)),('reel','Reel',(98,425,80,93))]
    nodes=''.join(f'<g class="rc-item" data-item="{key}" transform="translate({positions[key][0]} {positions[key][1]})"><title>{label}</title><circle class="rc-item-disc" r="27"/><svg x="{-20*cw/max(cw,ch):.2f}" y="{-20*ch/max(cw,ch):.2f}" width="{40*cw/max(cw,ch):.2f}" height="{40*ch/max(cw,ch):.2f}" viewBox="{cx} {cy} {cw} {ch}" preserveAspectRatio="xMidYMid meet" overflow="hidden"><image href="images/research/rcml-figure2.png" width="2834" height="1082" clip-path="url(#{prefix}-photo-{key})"/></svg><text y="44" text-anchor="middle">{label}</text></g>' for key,label,(cx,cy,cw,ch) in items)
    clips=''.join(f'<clipPath id="{prefix}-photo-{key}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath>' if key!='hat' else f'<clipPath id="{prefix}-photo-hat"><path d="M406 277H484V352H375V323L402 310Z"/></clipPath>' for key,_,(cx,cy,cw,ch) in items)
    if baseline:
        title='Traditional relation-agnostic embeddings stay fixed'
        desc='The same five products have one fixed set of embeddings and distances, reused for tennis and fishing relations. Positions are illustrative.'
    else:
        title='RCML embeddings change with the selected relation'
        desc='For tennis, the sun hat is nearer the backpack in embedding space. For fishing, it is nearer the rod combo. Positions and pairwise distances change with the relation; positions are illustrative.'
    return f'''<svg class="embedding-space {'relation-baseline' if baseline else 'relation-space'}" viewBox="0 0 350 300" role="img" aria-labelledby="{prefix}-title {prefix}-desc"><title id="{prefix}-title">{title}</title><desc id="{prefix}-desc">{desc}</desc><defs>{clips}<pattern id="{prefix}-grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#dce0e5"/></pattern></defs><rect x="4" y="4" width="342" height="288" rx="6" fill="url(#{prefix}-grid)"/>{nodes}</svg>'''

def xai_loop_connections():
    # One rounded loop supplies the visible stroke, arrow tangents, and motion path.
    route = 'M127 45H243Q303 45 303 105V187Q303 247 243 247H127Q67 247 67 187V105Q67 45 127 45Z'
    boxes = [(35,9,110,72),(215,18,120,54),(238,118,130,54),(120,220,130,54),(2,118,120,54)]
    points = [(127,45)]
    def line(end):
        start=points[-1]
        points.extend((start[0]+(end[0]-start[0])*t/100,start[1]+(end[1]-start[1])*t/100) for t in range(1,101))
    def curve(control,end):
        start=points[-1]
        for i in range(1,201):
            t=i/200
            points.append(((1-t)**2*start[0]+2*(1-t)*t*control[0]+t*t*end[0],(1-t)**2*start[1]+2*(1-t)*t*control[1]+t*t*end[1]))
    line((243,45));curve((303,45),(303,105));line((303,187));curve((303,247),(243,247))
    line((127,247));curve((67,247),(67,187));line((67,105));curve((67,45),(127,45))
    arrows=[]
    for x,y,w,h in boxes:
        inside=lambda pt:x-6<=pt[0]<=x+w+6 and y-6<=pt[1]<=y+h+6
        i=next(i for i in range(1,len(points)) if inside(points[i]) and not inside(points[i-1]))
        px,py=points[i-1];qx,qy=points[i-2]
        angle=math.degrees(math.atan2(py-qy,px-qx))
        arrows.append(f'<path class="xai-arrowhead" d="M0 0L-5 -2.5L-5 2.5Z" transform="translate({px:.3f} {py:.3f}) rotate({angle:.3f})"/>')
    cutouts=''.join(f'<rect x="{x-6}" y="{y-6}" width="{w+12}" height="{h+12}" fill="black"/>' for x,y,w,h in boxes)
    return f'''<defs><mask id="xai-loop-gaps" maskUnits="userSpaceOnUse" x="0" y="0" width="510" height="280"><rect width="510" height="280" fill="white"/>{cutouts}</mask></defs>
<path class="xai-track" d="{route}" mask="url(#xai-loop-gaps)"/>{''.join(arrows)}
<g mask="url(#xai-loop-gaps)"><circle class="xai-flow-dot" r="2.5" style="offset-path:path('{route}')"/></g>'''

XAI = '''<svg viewBox="0 0 510 280" class="support-svg xai-loop" role="img" aria-labelledby="xai-title xai-desc"><title id="xai-title">XAI-Refine: a closed explanation–knowledge loop</title><desc id="xai-desc">Extract reliable explanations, verify them against literature, derive a minimal revision and training constraint, then validate the candidate model. Refine updates the brain-age model only after validation; the updated model then feeds Explain for the next iteration. The same explanatory variable and measurement operator are retained for explanation, regularization, and validation; compatible differentiable surrogates are used for training when required.</desc>
<defs><marker id="xai-loop-arrow" viewBox="0 0 5 5" refX="5" refY="2.5" markerUnits="userSpaceOnUse" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#8798b0"/></marker></defs>
<!--xai-connections-->
<g class="xai-step"><rect x="215" y="18" width="120" height="54" rx="7"/><text x="275" y="40" class="xai-step-title">01 · Explain</text><text x="275" y="57" class="xai-step-detail">Measure with Φⱼ</text></g>
<g class="xai-step"><rect x="238" y="118" width="130" height="54" rx="7"/><text x="303" y="140" class="xai-step-title">02 · Verify claims</text><text x="303" y="157" class="xai-step-detail">Model ↔ domain claims</text></g>
<g class="xai-step"><rect x="120" y="220" width="130" height="54" rx="7"/><text x="185" y="242" class="xai-step-title">03 · Regularize</text><text x="185" y="259" class="xai-step-detail">Constrain the same Φⱼ</text></g>
<g class="xai-step xai-validation"><rect x="2" y="118" width="120" height="54" rx="7"/><text x="67" y="140" class="xai-step-title">04 · Refine</text><text x="67" y="157" class="xai-step-detail">Retrain · re-check Φⱼ</text></g>
<g class="xai-central-model"><rect x="35" y="9" width="110" height="72" rx="9"/><text x="90" y="29" class="xai-model-name">Brain-age model</text><text x="90" y="51" class="xai-model">fₜ → fₜ₊₁</text><text x="90" y="69" class="xai-center-note">Accepted update</text></g>
<g class="xai-shared-operator"><title>Dashed links mark the same explanatory variable and measurement operator shared by Explain, Regularize, and Refine; they are not additional process-flow arrows.</title>
<path class="xai-shared-link" d="M239 78V84C239 98 185 88 185 108V214M128 145H185"/>
<g class="xai-shared-ports"><circle cx="239" cy="78" r="2"/><circle cx="128" cy="145" r="2"/><circle cx="185" cy="214" r="2"/></g>
<rect class="xai-shared-label-bg" x="139" y="132" width="92" height="26" rx="13"/>
<text x="185" y="149" class="xai-shared-label">Same operator Φⱼ</text>
</g>
<g class="xai-corpus"><title>Domain corpus: scientific literature retrieved to verify model claims</title><path d="M412 116C412 104 502 104 502 116V165C502 177 412 177 412 165Z"/><path class="xai-corpus-rim" d="M412 116C412 128 502 128 502 116"/><text x="457" y="143">Domain corpus</text><text x="457" y="159" class="xai-corpus-detail">Scientific literature</text></g>
<path class="xai-corpus-link" d="M368 134H407" marker-end="url(#xai-loop-arrow)"/>
<path class="xai-corpus-link" d="M412 157H373" marker-end="url(#xai-loop-arrow)"/>
<text x="390" y="127" class="xai-evidence-label">Query</text><text x="390" y="172" class="xai-evidence-label">Evidence</text>
</svg>'''.replace('<!--xai-connections-->', xai_loop_connections())

MILNET = '''<div class="milnet-story">
<div class="milnet-animation-header"><div class="milnet-method-title">Complementary views. Selective mutual learning.</div><button id="milnet-toggle" class="small-button" hidden aria-label="Pause MILNet illustration">Pause</button></div>
<div class="milnet-views"><div><span>LOCAL</span><strong>Objects &amp; relations</strong></div><span class="milnet-transfer-icon" aria-label="Two-way knowledge transfer">⇄</span><div><span>GLOBAL</span><strong>Image–text context</strong></div></div>
<div class="milnet-gate"><span class="milnet-pass">✓ Correct prediction → teach</span><span>Incorrect prediction → skip</span></div>
<p class="milnet-view-caption" id="milnet-view-caption">Complementary views · selective sharing</p>
<table class="milnet-results">
<caption>Different blind spots, complementary strengths</caption>
<thead><tr>
<th scope="col"><span class="milnet-table-label">Two examples<br>from the paper</span></th>
<th scope="col"><svg class="milnet-case milnet-case-a" viewBox="0 0 720 540" role="img" aria-label="Animated illustration of local object details versus whole-scene context; boxes are explanatory, not measured model attention."><image href="images/research/milnet-context-original.jpg" width="720" height="540"/><g class="milnet-local-focus"><rect x="75" y="85" width="170" height="215" rx="10"/><rect x="285" y="80" width="160" height="260" rx="10"/></g><g class="milnet-global-focus"><rect x="18" y="65" width="684" height="355" rx="12"/></g></svg><span>Whole-scene context</span><small>“Umar Akmal with his fans”</small></th>
<th scope="col"><svg class="milnet-case milnet-case-b" viewBox="0 0 649 500" role="img" aria-label="Animated illustration of facial details versus the whole basketball scene; boxes are explanatory, not measured model attention."><image href="images/research/milnet-faces-original.jpg" width="649" height="500"/><g class="milnet-local-focus"><rect x="192" y="90" width="115" height="170" rx="10"/><rect x="435" y="140" width="115" height="160" rx="10"/></g><g class="milnet-global-focus"><rect x="14" y="55" width="620" height="320" rx="12"/></g></svg><span>Facial details</span><small>“Korver’s getting paid”</small></th>
</tr></thead>
<tbody><tr><th scope="row">Local only</th><td class="miss">✕ Missed</td><td class="hit">✓ Correct</td></tr><tr><th scope="row">Global only</th><td class="hit">✓ Correct</td><td class="miss">✕ Missed</td></tr><tr class="milnet-result"><th scope="row">MILNet</th><td class="hit">✓ Correct</td><td class="hit">✓ Correct</td></tr></tbody></table>
<details class="milnet-evidence">
<summary>Inspect the paper’s local cues</summary>
<p class="milnet-illustration-note">The animated outlines illustrate local and global viewing scales; they are not measured attention maps.</p><div class="milnet-cue-notes"><p><strong>Context beyond individual objects.</strong> Separate head and hair detections miss the relationship between the men’s hair and beards. A mistaken beard label also misleads the local branch.</p><p><strong>Details within the scene.</strong> Individual facial expressions help the local branch interpret the basketball post, where the global-only model fails.</p></div>
<img src="images/research/milnet-case-study.png" width="1380" height="638" loading="lazy" alt="Original Figure 3: object detections and model predictions for the two cases. Colored boxes mark the paper’s local regions."/>
<a href="https://ojs.aaai.org/index.php/AAAI/article/view/26138/25910" target="_blank" rel="noopener noreferrer">Original Figure 3 · MILNet, AAAI 2023 ↗</a>
</details>
</div>'''

PROFILE = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="Profile-conditioned latent dynamics: observed transitions supervise a posterior during training; at inference, a prior uses the profile and current context to predict transition codes without future-state access."><text x="10" y="22" class="figure-small">TRAINING · observed state change</text><rect x="10" y="33" width="140" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="80" y="57" class="support-label" text-anchor="middle">State t → state t+1</text><path d="M151 52H181M175 47L182 52L175 57" fill="none" stroke="#929788"/><rect x="190" y="33" width="170" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="275" y="57" class="support-label" text-anchor="middle">Posterior → transition code</text><path d="M275 74V99" stroke="#929788" stroke-dasharray="3 3"/><text x="287" y="91" class="figure-small">supervises</text><text x="10" y="105" class="figure-small">INFERENCE · no future-state input</text><rect x="10" y="116" width="140" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="80" y="137" class="support-label" text-anchor="middle">Profile + current state</text><text x="80" y="155" class="figure-small" text-anchor="middle">and current behavior</text><path d="M151 142H181M175 137L182 142L175 147" fill="none" stroke="#929788"/><rect x="190" y="116" width="170" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="275" y="137" class="support-label" text-anchor="middle">Prior → predicted code</text><text x="275" y="155" class="figure-small" text-anchor="middle">next state + behavior</text></svg>'''
