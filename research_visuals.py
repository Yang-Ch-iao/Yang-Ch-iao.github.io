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
    verified_edges={1:[(3,12),(8,12),(6,13),(10,14),(11,15),(5,15)],
                    2:[(5,17),(7,18),(10,19),(2,20),(9,20),(19,20)]}
    rejected = {16,21}
    def edge(a,b,classes,round_num=0):
        x,y=nodes[a];xx,yy=nodes[b]
        return f'<path class="{classes}" data-round="{round_num}" data-from="{a}" data-to="{b}" pathLength="1" d="M{x} {y}L{xx} {yy}"/>'
    lines = [edge(a,b,'mw-initial-edge') for a,b in initial_edges]
    for r,pairs in verified_edges.items():
        lines += [edge(a,b,'mw-verified-edge',r) for a,b in pairs]
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
    return f'''<svg viewBox="0 0 730 465" class="molworld-svg" role="img" aria-labelledby="mw-title mw-desc">
    <title id="mw-title">Select a connected context, generate a batch, then verify its connections</title><desc id="mw-desc">Two illustrative rounds. Five connected molecules are selected from the current graph as an anchor context. Multiple candidates are sampled together without predetermined edges. MMP verification determines their links, including links to existing molecules outside the anchor and links between accepted candidates. Candidates without a verified connection to the current graph are not incorporated. A new five-node context can include previously accepted molecules.</desc>
    <defs><linearGradient id="mw-property-reference" x1="0%" x2="100%"><stop stop-color="#fff0ba"/><stop offset=".5" stop-color="#ffd59e"/><stop offset="1" stop-color="#ce2b1d"/></linearGradient><marker id="mw-property-tip" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ce2b1d"/></marker><linearGradient id="mw-field-base" x2="1" y2="1"><stop stop-color="#f8f2e7"/><stop offset="1" stop-color="#f2e8d5"/></linearGradient><linearGradient id="mw-field-one" x2="1" y2="1"><stop stop-color="#f4ead7"/><stop offset="1" stop-color="#e9d8bd"/></linearGradient><linearGradient id="mw-field-two" x2="1" y2="1"><stop stop-color="#f2e5de"/><stop offset="1" stop-color="#e6cfc3"/></linearGradient><marker id="mw-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7f9084"/></marker></defs>
    <g class="mw-graph">
    <path class="mw-region mw-region-2" d="{contours[2]}"/><path class="mw-region mw-region-1" d="{contours[1]}"/><path class="mw-region mw-region-0" d="{contours[0]}"/>
    {''.join(lines)}{''.join(anchor_edges)}{''.join(dots)}
    </g>
    <text x="24" y="18" class="figure-small">Current molecule-transfer graph</text>
    <rect x="145" y="408" width="174" height="6" fill="url(#mw-property-reference)"/><path d="M315 411H330" stroke="#ce2b1d" stroke-width="6" marker-end="url(#mw-property-tip)"/><text x="237" y="432" text-anchor="middle" class="figure-small">Higher property</text>
    <text x="24" y="453" class="figure-small mw-graph-caption">Verified connections determine the expansion.</text>
    <g class="mw-inset"><text x="490" y="43" class="figure-heading">What does an edge mean?</text><text x="490" y="65" class="figure-small">A verified local structural modification</text>
    {structure(124,'H')}{structure(226,'CH₃')}
    <path d="M575 163V181" stroke="#5d6965" marker-end="url(#mw-arrow)"/><text x="585" y="177" class="figure-small">H → CH₃</text>
    <text x="490" y="284" class="figure-small">Shared scaffold, changed fragment.</text><text x="490" y="303" class="figure-small">MMP = matched molecular pair.</text>
    <path d="M491 335H522" stroke="#758a7e" stroke-width="1.4"/><text x="533" y="339" class="figure-small">Verified MMP connection</text>
    <circle cx="506" cy="365" r="6.5" fill="white" stroke="#8d9891" stroke-dasharray="2 2"/><text x="533" y="369" class="figure-small">Candidate awaiting verification</text></g>
    </svg>'''

ENTERPRISE = '''<div class="evidence-figure" role="img" aria-label="The Northstar example from EnterpriseSaga Figure 1: Salesforce identifies the billing update, Slack explains retry charges, and email confirms the resolution; similar records do not answer the same question.">
<div class="case-heading">A question across systems and time</div>
<p class="case-question">What caused Northstar’s duplicate charges, and how were they resolved?</p>
<ol class="evidence-chain"><li><div class="record-meta">SALESFORCE <span>May 6</span></div><strong>Identify the update</strong><p>Duplicate charges linked to the May billing update.</p></li><li><div class="record-meta">SLACK <span>May 7</span></div><strong>Establish the cause</strong><p>Automatic retries charged the customer twice.</p></li><li><div class="record-meta">EMAIL <span>May 9</span></div><strong>Confirm the outcome</strong><p>Retries disabled; refunds issued.</p></li></ol>
<div class="competing-records"><span>RELATED, BUT DIFFERENT</span><p><b>Same customer:</b> an earlier invoice-layout issue.</p><p><b>A proposal:</b> manual review, not the final resolution.</p></div>
</div>'''

def rcml_figure():
    # Original product photographs from RCML Figure 2(a), framed with SVG viewports.
    items=[
      ('hat','Sun hat',300,100,(375,277,109,75)),
      ('backpack','Tennis backpack',150,180,(97,196,93,95)),
      ('racket','Tennis racket',300,260,(405,68,97,102)),
      ('rod','Fishing rod combo',550,100,(334,484,80,83)),
      ('reel','Fishing reel',550,260,(98,425,80,93))]
    nodes=''.join(f'<g class="rc-item" data-item="{key}" transform="translate({x} {y})"><title>{label}</title><circle class="rc-item-disc" r="42"/><svg x="{-31*cw/max(cw,ch):.2f}" y="{-31*ch/max(cw,ch):.2f}" width="{62*cw/max(cw,ch):.2f}" height="{62*ch/max(cw,ch):.2f}" viewBox="{cx} {cy} {cw} {ch}" preserveAspectRatio="xMidYMid meet" overflow="hidden"><image href="images/research/rcml-figure2.png" width="2834" height="1082" clip-path="url(#rc-photo-{key})"/></svg><text y="62" text-anchor="middle">{label}</text></g>' for key,label,x,y,(cx,cy,cw,ch) in items)
    photo_clips=''.join(f'<clipPath id="rc-photo-{key}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath>' if key!='hat' else '<clipPath id="rc-photo-hat"><path d="M406 277H484V352H375V323L402 310Z"/></clipPath>' for key,_,_,_,(cx,cy,cw,ch) in items)
    points={key:(x,y) for key,_,x,y,_ in items}
    pairs=[('backpack','racket','tennis'),('backpack','hat','tennis'),('rod','reel','fishing'),('rod','hat','fishing')]
    lines=''.join(f'<line class="rc-distance {"close" if relation=="tennis" else ""}" data-from="{a}" data-to="{b}" data-relation="{relation}" x1="{points[a][0]}" y1="{points[a][1]}" x2="{points[b][0]}" y2="{points[b][1]}"/>' for a,b,relation in pairs)
    return f'''<svg class="relation-space" viewBox="0 0 700 400" role="img" aria-labelledby="rc-title rc-desc"><title id="rc-title">Tennis and fishing relations from RCML Figure 2(a)</title><desc id="rc-desc">For tennis-related co-purchases, the backpack connects to the racket and sun hat. For fishing-related co-purchases, the fishing rod connects to the reel and the same sun hat. Product photos and positive pairs come from the model diagram; embedding positions are illustrative.</desc><defs>{photo_clips}<pattern id="rc-grid" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#e1ddd6"/></pattern></defs><rect class="rc-grid-frame" x="10" y="10" width="680" height="370" rx="12" fill="url(#rc-grid)"/><ellipse class="rc-cluster" cx="225" cy="180" rx="160" ry="162"/>{lines}{nodes}<text class="rc-space-note" x="24" y="390">Same products · relation-specific embeddings</text></svg>'''

XAI = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="XAI-Refine: model explanations are verified against literature, converted into minimal targeted constraints, and validated before the model is updated."><defs><marker id="xai-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#858b7c"/></marker></defs><g fill="#fafbf7" stroke="#d8ddd2"><rect x="10" y="15" width="150" height="55" rx="5"/><rect x="210" y="15" width="150" height="55" rx="5"/><rect x="210" y="110" width="150" height="55" rx="5"/><rect x="10" y="110" width="150" height="55" rx="5"/></g><g class="support-label" text-anchor="middle"><text x="85" y="39">Reliable explanations</text><text x="85" y="56" class="figure-small">from the current model</text><text x="285" y="39">Verify with literature</text><text x="285" y="56" class="figure-small">evidence and scope</text><text x="285" y="133">Minimal revision</text><text x="285" y="151" class="figure-small">targeted constraints</text><text x="85" y="133">Validate & update</text><text x="85" y="151" class="figure-small">accuracy + off-target checks</text></g><g stroke="#858b7c" fill="none" marker-end="url(#xai-arrow)"><path d="M161 42H201"/><path d="M285 71V101"/><path d="M209 137H169"/><path d="M85 109V79"/></g></svg>'''

PROFILE = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="Profile-conditioned latent dynamics: observed transitions supervise a posterior during training; at inference, a prior uses the profile and current context to predict transition codes without future-state access."><text x="10" y="22" class="figure-small">TRAINING · observed state change</text><rect x="10" y="33" width="140" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="80" y="57" class="support-label" text-anchor="middle">State t → state t+1</text><path d="M151 52H181M175 47L182 52L175 57" fill="none" stroke="#929788"/><rect x="190" y="33" width="170" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="275" y="57" class="support-label" text-anchor="middle">Posterior → transition code</text><path d="M275 74V99" stroke="#929788" stroke-dasharray="3 3"/><text x="287" y="91" class="figure-small">supervises</text><text x="10" y="105" class="figure-small">INFERENCE · no future-state input</text><rect x="10" y="116" width="140" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="80" y="137" class="support-label" text-anchor="middle">Profile + current state</text><text x="80" y="155" class="figure-small" text-anchor="middle">and current behavior</text><path d="M151 142H181M175 137L182 142L175 147" fill="none" stroke="#929788"/><rect x="190" y="116" width="170" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="275" y="137" class="support-label" text-anchor="middle">Prior → predicted code</text><text x="275" y="155" class="figure-small" text-anchor="middle">next state + behavior</text></svg>'''
