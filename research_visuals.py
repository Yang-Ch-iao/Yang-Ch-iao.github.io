"""Paper-grounded figures for the homepage. Coordinates are illustrative, not measured data."""
import math

def molworld_figure():
    # One illustrative context per round; the method may select multiple contexts.
    # Accepted candidates have a verified edge to the graph as it existed BEFORE that round.
    nodes = [(70,180),(100,110),(145,70),(190,120),(230,75),(275,130),
             (240,200),(180,230),(115,235),(285,260),(350,210),(345,125),
             (75,40),(200,25),(325,38),(400,88),(407,287),
             (30,100),(45,287),(180,330),(355,315),(430,185)]
    initial_edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(1,3),(3,6),
                     (6,7),(7,8),(8,0),(6,9),(9,10),(10,11),(11,5)]
    anchor_sets = [{1,2,3,4,5}, {0,1,7,8,12}]
    verified_edges = {1:[(1,12),(4,13),(11,14),(11,15),(10,15),(14,15)],
                      2:[(12,17),(1,17),(8,18),(7,19),(9,19),(9,20),(10,20),(19,20)]}
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
    # Periodic Catmull–Rom contours keep the boundary smooth at every junction.
    def contour(points):
        segments=[]
        for i,p1 in enumerate(points):
            p0=points[(i-1)%len(points)];p2=points[(i+1)%len(points)];p3=points[(i+2)%len(points)]
            c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
            c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
            segments.append(f'C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]} {p2[1]}')
        return f'M{points[0][0]} {points[0][1]}'+''.join(segments)+'Z'
    contours=[contour([(55,145),(88,82),(171,47),(264,57),(342,96),(373,174),(338,254),(247,286),(147,271),(75,234)]),
              contour([(40,130),(59,39),(166,3),(289,11),(397,51),(427,141),(389,238),(302,291),(187,301),(78,264)]),
              contour([(10,123),(42,35),(155,-6),(287,0),(408,41),(455,149),(410,290),(319,352),(179,366),(52,322),(7,236)])]
    def structure(y,variable):
        ring=' '.join(f'{526+20*math.cos(k*math.pi/3):.1f},{y+20*math.sin(k*math.pi/3):.1f}' for k in range(6))
        return f'''<rect x="495" y="{y-38}" width="165" height="70" rx="23" fill="#e8efec"/>
        <polygon points="{ring}" fill="none" stroke="#425650" stroke-width="1.5"/>
        <circle cx="526" cy="{y}" r="13" fill="none" stroke="#425650" stroke-width="1"/>
        <path d="M546 {y}L563 {y}M580 {y}H603M603 {y}L624 {y}M601 {y-4}V{y-22}M605 {y-4}V{y-22}" stroke="#425650" stroke-width="1.5" fill="none"/>
        <text x="572" y="{y+4}" text-anchor="middle" class="chem">NH</text><text x="603" y="{y-27}" text-anchor="middle" class="chem">O</text>
        <circle cx="641" cy="{y}" r="21" fill="{('#f2ddd4' if variable=='H' else '#e5e2f2')}"/><text x="641" y="{y+5}" text-anchor="middle" class="chem">{variable}</text>'''
    return f'''<svg viewBox="0 0 730 425" class="molworld-svg" role="img" aria-labelledby="mw-title mw-desc">
    <title id="mw-title">Select a connected context, generate a batch, then verify its connections</title><desc id="mw-desc">Two illustrative rounds. Five connected molecules are selected from the current graph as an anchor context. Multiple candidates are sampled together without predetermined edges. MMP verification determines their links, including links to existing molecules outside the anchor and links between accepted candidates. Candidates without a verified connection to the current graph are not incorporated. A new five-node context can include previously accepted molecules.</desc>
    <defs><linearGradient id="mw-field-base" x2="1" y2="1"><stop stop-color="#f8f2e7"/><stop offset="1" stop-color="#f2e8d5"/></linearGradient><linearGradient id="mw-field-one" x2="1" y2="1"><stop stop-color="#f4ead7"/><stop offset="1" stop-color="#e9d8bd"/></linearGradient><linearGradient id="mw-field-two" x2="1" y2="1"><stop stop-color="#f2e5de"/><stop offset="1" stop-color="#e6cfc3"/></linearGradient><marker id="mw-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7f9084"/></marker></defs>
    <g class="mw-graph" transform="translate(6 28) scale(.96)">
    <path class="mw-region mw-region-2" d="{contours[2]}"/><path class="mw-region mw-region-1" d="{contours[1]}"/><path class="mw-region mw-region-0" d="{contours[0]}"/>
    {''.join(lines)}{''.join(anchor_edges)}{''.join(dots)}
    </g>
    <text x="24" y="18" class="figure-small">Current molecule-transfer graph</text>
    <text x="24" y="405" class="figure-small mw-graph-caption">Verified connections determine the expansion.</text>
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

def shape(kind,x,y,color='#515b9c'):
    if kind=='A': return f'<circle cx="{x}" cy="{y}" r="7" fill="{color}"/>'
    if kind=='B': return f'<path d="M{x} {y-8}L{x+8} {y+7}H{x-8}Z" fill="{color}"/>'
    return f'<path d="M{x} {y-9}L{x+3} {y-3}L{x+10} {y-2}L{x+5} {y+3}L{x+6} {y+10}L{x} {y+6}L{x-6} {y+10}L{x-5} {y+3}L{x-10} {y-2}L{x-3} {y-3}Z" fill="{color}"/>'

def rcml_figure():
    panels=''
    for x,label,ys,color in [(20,'Fixed space',[102,161,216],'#6e746e'),(163,'Relation 1',[108,204,146],'#687857'),(270,'Relation 2',[204,156,110],'#b3775b'),(377,'Relation 3',[160,112,211],'#5964a8')]:
        panels+=f'<rect x="{x}" y="68" width="88" height="178" rx="6" fill="white" stroke="#dadfd7"/><text x="{x+44}" y="55" text-anchor="middle" class="figure-small">{label}</text>'
        for kind,y in zip('ABC',ys): panels+=shape(kind,x+44,y,color)
    return f'''<svg viewBox="0 0 486 307" class="rcml-svg" role="img" aria-label="RCML Figure 1 redrawn: the same three sample identities occupy a fixed space in a relation-agnostic model, but distinct positions in three relation-conditioned spaces.">
    <text x="64" y="20" text-anchor="middle" class="figure-heading">One embedding</text><text x="312" y="20" text-anchor="middle" class="figure-heading">A family of embeddings</text>
    {panels}<path d="M121 153H149M143 148L150 153L143 158" stroke="#91968b" fill="none"/>
    {shape('A',85,277)}<text x="99" y="281" class="figure-small">Sample A</text>{shape('B',222,277)}<text x="236" y="281" class="figure-small">Sample B</text>{shape('C',359,277)}<text x="373" y="281" class="figure-small">Sample C</text></svg>'''

XAI = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="XAI-Refine: model explanations are verified against literature, converted into minimal targeted constraints, and validated before the model is updated."><defs><marker id="xai-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#858b7c"/></marker></defs><g fill="#fafbf7" stroke="#d8ddd2"><rect x="10" y="15" width="150" height="55" rx="5"/><rect x="210" y="15" width="150" height="55" rx="5"/><rect x="210" y="110" width="150" height="55" rx="5"/><rect x="10" y="110" width="150" height="55" rx="5"/></g><g class="support-label" text-anchor="middle"><text x="85" y="39">Reliable explanations</text><text x="85" y="56" class="figure-small">from the current model</text><text x="285" y="39">Verify with literature</text><text x="285" y="56" class="figure-small">evidence and scope</text><text x="285" y="133">Minimal revision</text><text x="285" y="151" class="figure-small">targeted constraints</text><text x="85" y="133">Validate & update</text><text x="85" y="151" class="figure-small">accuracy + off-target checks</text></g><g stroke="#858b7c" fill="none" marker-end="url(#xai-arrow)"><path d="M161 42H201"/><path d="M285 71V101"/><path d="M209 137H169"/><path d="M85 109V79"/></g></svg>'''

PROFILE = '''<svg viewBox="0 0 370 188" class="support-svg" role="img" aria-label="Profile-conditioned latent dynamics: observed transitions supervise a posterior during training; at inference, a prior uses the profile and current context to predict transition codes without future-state access."><text x="10" y="22" class="figure-small">TRAINING · observed state change</text><rect x="10" y="33" width="140" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="80" y="57" class="support-label" text-anchor="middle">State t → state t+1</text><path d="M151 52H181M175 47L182 52L175 57" fill="none" stroke="#929788"/><rect x="190" y="33" width="170" height="38" rx="5" fill="#f2f0e8" stroke="#ddd9cb"/><text x="275" y="57" class="support-label" text-anchor="middle">Posterior → transition code</text><path d="M275 74V99" stroke="#929788" stroke-dasharray="3 3"/><text x="287" y="91" class="figure-small">supervises</text><text x="10" y="105" class="figure-small">INFERENCE · no future-state input</text><rect x="10" y="116" width="140" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="80" y="137" class="support-label" text-anchor="middle">Profile + current state</text><text x="80" y="155" class="figure-small" text-anchor="middle">and current behavior</text><path d="M151 142H181M175 137L182 142L175 147" fill="none" stroke="#929788"/><rect x="190" y="116" width="170" height="52" rx="5" fill="#eff1f8" stroke="#d5d9e9"/><text x="275" y="137" class="support-label" text-anchor="middle">Prior → predicted code</text><text x="275" y="155" class="figure-small" text-anchor="middle">next state + behavior</text></svg>'''
