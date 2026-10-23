"""Paper-grounded figures for the homepage. Coordinates are illustrative, not measured data."""
import math

def molworld_figure():
    # Three cohorts follow the visual grammar of MolWorld Fig. 1.
    nodes = [
        (197,158,0),(238,116,0),(281,161,0),(263,216,0),(209,225,0),
        (135,110,1),(173,66,1),(247,57,1),(322,99,1),(349,175,1),
        (322,250,1),(261,281,1),(157,271,1),(106,201,1),
        (71,131,2),(109,54,2),(189,24,2),(294,28,2),(377,73,2),
        (419,139,2),(403,241,2),(333,308,2),(210,328,2),(108,304,2)]
    parents = {5:[0],6:[5,1],7:[1,6],8:[7,2],9:[2,8],10:[3,9],11:[3,4],12:[4,11],13:[0,5,12],14:[13,5],15:[5,6],16:[6,7],17:[7,8],18:[8,9],19:[9],20:[9,10],21:[10,11],22:[11,12],23:[12,13]}
    starts = [0]*5 + [1.8+i*.48 for i in range(9)] + [7.0+i*.48 for i in range(10)]
    lines=[]
    for a,b in [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]:
        x,y,_=nodes[a];xx,yy,_=nodes[b]
        lines.append(f'<path class="mw-initial-edge" d="M{x} {y}L{xx} {yy}"/>')
    for child,ps in parents.items():
        x,y,g=nodes[child]
        for parent in ps:
            xx,yy,_=nodes[parent]
            lines.append(f'<path class="mw-growing-edge" data-at="{starts[child]:.2f}" pathLength="1" d="M{xx} {yy}L{x} {y}" style="stroke-dasharray:1;stroke-dashoffset:0"/>')
    dots=[]
    for i,(x,y,g) in enumerate(nodes):
        dots.append(f'<g class="mw-node cohort-{g}" data-at="{starts[i]+(.38 if g else 0):.2f}" transform="translate({x} {y})"><title>{["Original molecule","Earlier-generated molecule","Later-generated molecule"][g]}</title><circle r="6.3"/></g>')
    def structure(y,variable):
        ring=' '.join(f'{526+20*math.cos(k*math.pi/3):.1f},{y+20*math.sin(k*math.pi/3):.1f}' for k in range(6))
        return f'''<rect x="495" y="{y-38}" width="165" height="70" rx="23" fill="#e8efec"/>
        <polygon points="{ring}" fill="none" stroke="#425650" stroke-width="1.5"/>
        <circle cx="526" cy="{y}" r="13" fill="none" stroke="#425650" stroke-width="1"/>
        <path d="M546 {y}L563 {y}M580 {y}H603M603 {y}L624 {y}M601 {y-4}V{y-22}M605 {y-4}V{y-22}" stroke="#425650" stroke-width="1.5" fill="none"/>
        <text x="572" y="{y+4}" text-anchor="middle" class="chem">NH</text><text x="603" y="{y-27}" text-anchor="middle" class="chem">O</text>
        <circle cx="641" cy="{y}" r="21" fill="{('#f2ddd4' if variable=='H' else '#e5e2f2')}"/><text x="641" y="{y+5}" text-anchor="middle" class="chem">{variable}</text>'''
    return f'''<svg viewBox="0 0 730 388" class="molworld-svg" role="img" aria-labelledby="mw-title mw-desc">
    <title id="mw-title">Molecule-transfer graph expansion</title><desc id="mw-desc">Adapted from Figure 1 of MolWorld. Blue outlined original molecules are joined by earlier-generated and later-generated molecules through MMP relations. New molecules stay connected to the original series. The inset illustrates a shared chemical scaffold with a local H-to-methyl substitution.</desc>
    <defs><linearGradient id="mw-property" gradientUnits="userSpaceOnUse" x1="77" y1="372" x2="400" y2="372"><stop stop-color="#efcf89"/><stop offset="1" stop-color="#c76c56"/></linearGradient><marker id="mw-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#b76c55"/></marker><marker id="mw-property-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#c76c56"/></marker></defs>
    <g transform="translate(0 14) scale(.96)">
    <path class="mw-field mw-field-late" d="M48 150Q45 108 78 89Q74 30 123 29Q153 3 196 8Q235 0 278 9Q326-5 345 36Q400 33 405 79Q451 105 438 163Q460 215 421 250Q411 295 359 302Q329 348 275 330Q227 366 183 340Q127 353 106 322Q58 321 65 268Q22 236 44 199Z"/>
    <path class="mw-field mw-field-early" d="M85 168Q83 119 125 95Q137 42 187 47Q221 24 261 42Q305 31 332 73Q377 97 365 141Q399 194 360 231Q365 278 310 284Q275 319 225 300Q173 316 147 289Q92 278 101 235Q68 214 85 168Z"/>
    <path class="mw-field mw-field-initial" d="M169 174Q166 135 201 124Q220 91 251 105Q286 106 294 144Q320 174 292 205Q293 239 256 242Q223 265 196 240Q168 225 179 201Z"/>
    {''.join(lines)}{''.join(dots)}
    <ellipse cx="335" cy="138" rx="30" ry="55" transform="rotate(-25 335 138)" class="mw-detail-ring"/><path d="M367 124L488 95" class="mw-detail-guide"/>
    </g>
    <g class="mw-inset"><text x="490" y="35" class="figure-heading">What does an edge mean?</text><text x="490" y="57" class="figure-small">A local structural modification</text>
    {structure(116,'H')}{structure(218,'CH₃')}
    <path d="M575 155V173" stroke="#5d6965" marker-end="url(#mw-arrow)"/><text x="585" y="169" class="figure-small">H → CH₃</text>
    <text x="490" y="276" class="figure-small">Shared scaffold, changed fragment.</text><text x="490" y="295" class="figure-small">MMP = matched molecular pair.</text></g>
    <path d="M77 372H400" stroke="url(#mw-property)" stroke-width="5" marker-end="url(#mw-property-arrow)"/><text x="239" y="361" text-anchor="middle" class="figure-small">Exploration toward higher-property regions</text>
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
