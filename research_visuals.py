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
    initial_edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(5,4),(6,0),(7,3),(8,3),(9,2),(10,1),(11,0),(5,7),(7,8)]
    anchor_sets=[{0,1,2,3,4},{0,4,5,11,15}]
    # Illustrative dense anchor connectivity, clarified by the paper's author.
    # Most accepted candidates link to four or five context molecules; a few links
    # also reach other existing molecules. Verification still decides acceptance.
    candidate_anchors={1:{12:[0,1,2,3,4],13:[0,1,3,4],14:[0,1,2,3,4],15:[0,1,2,4]},
                       2:{17:[0,4,5,11,15],18:[0,4,5,15],19:[0,4,5,11,15],20:[0,4,11,15]}}
    extra_edges={1:[(8,12),(6,13),(10,14),(11,15),(5,15)],
                 2:[(7,18),(10,19),(2,20),(19,20)]}
    verified_edges={r:[(a,n) for n,context in group.items() for a in context]+extra_edges[r]
                    for r,group in candidate_anchors.items()}
    rejected = {16,21}
    def edge(a,b,classes,round_num=0):
        x,y=nodes[a];xx,yy=nodes[b]
        return f'<path class="{classes}" data-round="{round_num}" data-from="{a}" data-to="{b}" pathLength="1" d="M{x} {y}L{xx} {yy}"/>'
    lines = [edge(a,b,'mw-initial-edge') for a,b in initial_edges]
    for r,pairs in verified_edges.items():
        lines += [edge(a,b,'mw-verified-edge '+('mw-anchor-link' if a in anchor_sets[r-1] else 'mw-other-link'),r) for a,b in pairs]
    # Highlight only actual edges inside the chosen connected five-node context.
    anchor_edges=[]
    all_edges=initial_edges+verified_edges[1]
    for r,selected in enumerate(anchor_sets,1):
        anchor_edges += [edge(a,b,'mw-anchor-edge',r) for a,b in all_edges if a in selected and b in selected]
    dots=[]
    for i,(x,y) in enumerate(nodes):
        r=0 if i<12 else 1 if i<17 else 2
        classes='mw-node '+('mw-existing' if r==0 else 'mw-candidate')+(' mw-rejected' if i in rejected else '')
        title='Existing molecule' if r==0 else 'Candidate with no verified link; not incorporated' if i in rejected else 'Generated candidate; incorporated only after MMP verification'
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
    <title id="mw-title">Select a connected context, generate a batch, then verify its connections</title><desc id="mw-desc">Two illustrative rounds. Five connected molecules are selected from the current graph as an anchor context. Multiple candidates are sampled together without predetermined edges. Accepted candidates typically connect to most or all five anchor molecules, with occasional additional links to other molecules. These illustrative links appear after MMP verification. Candidates without a verified connection to the current graph are not incorporated. A new five-node context can include previously accepted molecules.</desc>
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
    <path d="M491 335H522" stroke="#758a7e" stroke-width="1.4"/><text x="533" y="339" class="figure-small">Verified MMP connection</text>
    <circle cx="506" cy="365" r="6.5" fill="white" stroke="#8d9891" stroke-dasharray="2 2"/><text x="533" y="369" class="figure-small">Candidate awaiting verification</text></g>
    </svg>'''

ENTERPRISE = '''<div class="es-framework" aria-label="EnterpriseSaga coarse-to-fine construction framework, adapted from Figure 2">
<div class="es-metrics"><div><strong>1.213B</strong><span>tokens</span></div><div><strong>18</strong><span>months</span></div><div><strong>12</strong><span>systems</span></div><div><strong>966</strong><span>questions</span></div></div>
<div class="es-framework-heading"><span>01</span><strong>Simulate a shared company history</strong></div>
<div class="es-construction">
<div class="es-company"><div class="es-mini-label">COMPANY CONTEXT</div><strong>People &amp; roles</strong><span>Business objectives<br>Dated changes</span></div>
<div class="es-branches"><div class="es-branch"><strong>Project planning</strong><span>Projects → subprojects → episodes</span></div><div class="es-branch"><strong>Recurring operations</strong><span>Streams → archetypes → episodes</span></div></div>
<div class="es-artifacts"><div class="es-mini-label">ACTIVITY-GROUNDED ARTIFACTS</div><strong>Shared facts,<br> different systems</strong><span>Slack · Jira · Email ·<br> Salesforce · +8 sources</span></div>
</div>
<div class="es-framework-heading es-qa-heading"><span>02</span><strong>Build questions with traceable evidence</strong></div>
<div class="es-qa-grid">
<div class="es-question-design"><div class="es-qa-type"><span>Multi-hop</span><div class="es-path" aria-label="One result identifies the next evidence"><i>A</i><b>→</b><i>B</i><b>→</b><i>C</i></div><small>Each result identifies the next evidence.</small></div><div class="es-qa-type"><span>Synthesis</span><div class="es-merge" aria-label="Combine complementary facts"><i>A</i><b>+</b><i>B</i><b>+</b><i>C</i><b>→</b><i>Answer</i></div><small>Combine facts within one business scope.</small></div></div>
<div class="es-grounding"><div class="es-mini-label">VERIFIED SUPPORT</div><strong>Question ↔ claims ↔ files</strong><ul><li>Reference answers &amp; answer subfacts</li><li>Alternative sufficient evidence sets</li><li>Scoped search &amp; support verification</li></ul></div>
</div>
<div class="es-refinement"><span aria-hidden="true">↺</span><div><strong>Question-conditioned refinement</strong><p>Add comparable activities with different dates, versions, or participants. Check conflicts and unintended support; update evidence annotations.</p></div></div>
</div>'''

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

XAI = '''<svg viewBox="0 0 530 520" class="support-svg xai-loop" role="img" aria-labelledby="xai-title xai-desc">
<title id="xai-title">XAI-Refine: domain knowledge guides model correction</title>
<desc id="xai-desc">Reliable model explanations yield model claims. Model claims generate neutral questions for retrieval and verification. An explicit literature corpus supplies the evidence; verified evidence is compiled into domain claims. Compare the claims on the same variable, measurement and scope; minimally revise the model explanation to satisfy the evidence. Translate the revision into a new regularization term, refine the predictor, and validate prediction, targeted change and non-target drift. Only accepted models return to explanation discovery.</desc>
<defs><marker id="xai-loop-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#8999af"/></marker><marker id="xai-return-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#6082ac"/></marker></defs>
<g class="xai-route" marker-end="url(#xai-loop-arrow)">
<path d="M156 76V116"/><path d="M354 76V86H396V116"/>
<path d="M450 47H417"/><path d="M260 147H276V47H292"/>
<path d="M156 178V197H278V218"/><path d="M396 178V197H278" marker-end="none"/>
<path d="M278 280V299H156V318"/><path d="M260 351H292"/>
<path d="M396 384V401H278V420"/>
</g>
<path class="xai-feedback" d="M94 462H34Q24 462 24 450V57Q24 47 34 47H52" marker-end="url(#xai-return-arrow)"/>
<path class="xai-feedback-pulse" d="M94 462H34Q24 462 24 450V57Q24 47 34 47H52" pathLength="100"/>
<text class="xai-cycle-label" x="12" y="268" transform="rotate(-90 12 268)">Re-explain the accepted model</text>
<g class="xai-block xai-model-side"><rect x="52" y="18" width="208" height="58" rx="7"/><text class="xai-block-title" x="156" y="43">Current model · fₜ</text><text class="xai-block-detail" x="156" y="63">Learned brain-age predictor</text></g>
<g class="xai-block xai-domain-side xai-verifier"><rect x="292" y="18" width="125" height="58" rx="7"/><text class="xai-block-title" x="354" y="42">Retrieve &amp; verify</text><text class="xai-block-detail" x="354" y="62">Scientific evidence</text></g>
<g class="xai-corpus"><title>Literature corpus: external scientific evidence for verification</title><path d="M450 27C450 15 526 15 526 27V68C526 80 450 80 450 68Z"/><path class="xai-corpus-rim" d="M450 27C450 39 526 39 526 27"/><text x="488" y="49">Literature</text><text x="488" y="65">corpus</text></g>
<text class="xai-connector-label" x="156" y="101">Reliable explanations</text><text class="xai-connector-label" x="396" y="105">Compile evidence</text>
<g class="xai-block xai-model-side"><rect x="52" y="116" width="208" height="62" rx="7"/><text class="xai-block-title" x="156" y="142">Model claims</text><text class="xai-block-detail" x="156" y="163">What the model has learned</text></g>
<g class="xai-block xai-domain-side"><rect x="292" y="116" width="208" height="62" rx="7"/><text class="xai-block-title" x="396" y="142">Verified domain claims</text><text class="xai-block-detail" x="396" y="163">Evidence-consistent relations</text></g>
<g class="xai-block xai-comparison"><rect x="94" y="218" width="368" height="62" rx="7"/><text class="xai-block-title" x="278" y="244">Compare model ↔ domain claims</text><text class="xai-block-detail" x="278" y="265">Align variable, measurement &amp; scope; identify the gap</text></g>
<g class="xai-block"><rect x="52" y="318" width="208" height="66" rx="7"/><text class="xai-block-title" x="156" y="344">Minimal claim revision</text><text class="xai-block-detail" x="156" y="365">Nearest admissible relation</text></g>
<g class="xai-block xai-regularizer"><rect x="292" y="318" width="208" height="66" rx="7"/><text class="xai-block-title" x="396" y="344">New regularization · Rₜ</text><text class="xai-block-detail" x="396" y="365">Penalize deviation from revision</text></g>
<g class="xai-block xai-update"><rect x="94" y="420" width="368" height="82" rx="7"/><text class="xai-block-title" x="278" y="445">Refine model · fₜ → fₜ₊₁</text><text class="xai-loss" x="278" y="468">Prediction loss + λRₜ</text><text class="xai-block-detail" x="278" y="490">Accept after prediction, revision &amp; drift checks</text></g>
</svg>'''

MILNET = '''<div class="milnet-story">
<div class="milnet-method-title">Complementary views. Selective mutual learning.</div>
<div class="milnet-views"><div><span>LOCAL</span><strong>Objects &amp; relations</strong></div><span class="milnet-transfer-icon" aria-label="Two-way knowledge transfer">⇄</span><div><span>GLOBAL</span><strong>Image–text context</strong></div></div>
<div class="milnet-gate"><span class="milnet-pass">✓ Correct prediction → teach</span><span>Incorrect prediction → skip</span></div>
<table class="milnet-results">
<caption>Different blind spots, complementary strengths</caption>
<thead><tr>
<th scope="col"><span class="milnet-table-label">Two examples<br>from the paper</span></th>
<th scope="col"><img class="milnet-clean-photo" src="images/research/milnet-context-original.jpg" width="720" height="540" loading="lazy" alt="Three men whose contrasting hair and beards provide a clue across the whole scene."/><span>Whole-scene context</span><small>“Umar Akmal with his fans”</small></th>
<th scope="col"><img class="milnet-clean-photo" src="images/research/milnet-faces-original.jpg" width="649" height="500" loading="lazy" alt="Basketball players on a bench with distinct facial expressions; the meme comments on Kyle getting paid."/><span>Facial details</span><small>“Korver’s getting paid”</small></th>
</tr></thead>
<tbody><tr><th scope="row">Local only</th><td class="miss">✕ Missed</td><td class="hit">✓ Correct</td></tr><tr><th scope="row">Global only</th><td class="hit">✓ Correct</td><td class="miss">✕ Missed</td></tr><tr class="milnet-result"><th scope="row">MILNet</th><td class="hit">✓ Correct</td><td class="hit">✓ Correct</td></tr></tbody></table>
<details class="milnet-evidence">
<summary>Inspect the paper’s local cues</summary>
<div class="milnet-cue-notes"><p><strong>Context beyond individual objects.</strong> Separate head and hair detections miss the relationship between the men’s hair and beards. A mistaken beard label also misleads the local branch.</p><p><strong>Details within the scene.</strong> Individual facial expressions help the local branch interpret the basketball post, where the global-only model fails.</p></div>
<img src="images/research/milnet-case-study.png" width="1380" height="638" loading="lazy" alt="Original Figure 3: object detections and model predictions for the two cases. Colored boxes mark the paper’s local regions."/>
<a href="https://ojs.aaai.org/index.php/AAAI/article/view/26138/25910" target="_blank" rel="noopener noreferrer">Original Figure 3 · MILNet, AAAI 2023 ↗</a>
</details>
</div>'''

PROFILE = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="Profile-conditioned latent dynamics: observed transitions supervise a posterior during training; at inference, a prior uses the profile and current context to predict transition codes without future-state access."><text x="10" y="22" class="figure-small">TRAINING · observed state change</text><rect x="10" y="33" width="140" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="80" y="57" class="support-label" text-anchor="middle">State t → state t+1</text><path d="M151 52H181M175 47L182 52L175 57" fill="none" stroke="#929788"/><rect x="190" y="33" width="170" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="275" y="57" class="support-label" text-anchor="middle">Posterior → transition code</text><path d="M275 74V99" stroke="#929788" stroke-dasharray="3 3"/><text x="287" y="91" class="figure-small">supervises</text><text x="10" y="105" class="figure-small">INFERENCE · no future-state input</text><rect x="10" y="116" width="140" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="80" y="137" class="support-label" text-anchor="middle">Profile + current state</text><text x="80" y="155" class="figure-small" text-anchor="middle">and current behavior</text><path d="M151 142H181M175 137L182 142L175 147" fill="none" stroke="#929788"/><rect x="190" y="116" width="170" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="275" y="137" class="support-label" text-anchor="middle">Prior → predicted code</text><text x="275" y="155" class="figure-small" text-anchor="middle">next state + behavior</text></svg>'''
