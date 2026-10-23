# Yang Qiao — personal website

Live site: https://yang-ch-iao.github.io/

A static academic homepage, served by GitHub Pages from the root of the `master` branch. No package installation or backend is required. `.nojekyll` bypasses the previous Jekyll theme.

## Update content

- **Publications and contact links:** edit `content.json`, then run `python3 build_home.py`.
- **Biography, research, education, service, and teaching:** edit the corresponding text in `build_home.py`, then run `python3 build_home.py`.
- **CV:** replace `files/Yang_Qiao_CV.pdf` and `files/Yang_Qiao_CV.docx`.
- **Photograph:** replace `images/profile.jpg`. Cropping is controlled by `.portrait-frame` in `assets/home/site.css`.
- **Design:** edit `assets/home/site.css`.
- **Paper figures:** edit `research_visuals.py`, then run `python3 build_home.py`.
- **MolWorld animation and publication filters:** edit `assets/home/site.js`.

Commit both source changes and the regenerated `index.html`, then push to `master`. GitHub Pages publishes the result automatically. Existing `/publications/`, `/portfolio/`, `/teaching/`, and `/cv/` links redirect to the appropriate content.

## Preview

```sh
python3 build_home.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/ in a browser.

## Publication status

EnterpriseSaga and Profile-Conditioned Latent Dynamics are listed as manuscripts. Add an arXiv URL to `content.json` once it is public. MMPT-RAG is listed as accepted in Findings of EMNLP 2026; its link is intentionally empty until the public version contains the correct author list.

## Interaction notes

Research figures are redrawn from the papers rather than generic animations:

- **EnterpriseSaga:** a compact adaptation of Figure 2: company context → parallel project / operations planning → activity-grounded artifacts, followed by multi-hop and synthesis question design, verified support, and question-conditioned refinement. Scale statistics come from the abstract and benchmark summary; token counts include exported metadata and serialization.
- **MolWorld:** Original Figure 1 vector contours, RGB colors, and molecule positions extracted from the paper PDF, with two illustrative rounds following Section 3.2: select five connected molecules from the current graph, sample multiple candidates together, verify their MMP links, and incorporate connected candidates. Following the author’s clarification, accepted candidates in the schematic have verified links to four or five anchor molecules, with a few additional links to other molecules; conditioning itself does not guarantee an edge. An unconnected candidate is excluded in each round; the second anchor includes a molecule accepted in the first round. Nodes are whole molecules; edges are MMP relations. The H-to-methyl inset illustrates a local structural modification, not a synthesis reaction. Graph coordinates, batch sizes, and animation timing are schematic. Every accepted candidate has a verified edge to the graph that existed before its generation round.
- **RCML:** Figure 1’s central comparison, illustrated with Figure 2(a)’s original product photos and tennis / fishing pairs. The traditional panel retains identical item positions across relation switches; only the RCML panel moves. Coordinates are schematic, not measured results. No graph edges are drawn. Separate distance bars track the displayed pairwise Euclidean distances on one common scale: the hat is nearer the backpack for tennis and nearer the rod for fishing. These bars are illustrative, not empirical measurements.
- **XAI-Refine (within AI for Science):** the explanation, literature verification, constrained revision, and validation loop.
- **Profile-conditioned latent dynamics:** training supervision from observed transitions versus inference from the profile and current context.

RCML supports automatic or manual relation switching and reduced-motion preferences. MolWorld pauses offscreen and when the tab is hidden, supports pause/replay and a step-by-step control, and shows the completed graph by default for reduced-motion preferences. All research figures and core content remain readable without JavaScript.

The previous AcademicPages source is retained for recovery and reference, but is not used to generate the new homepage. The original theme license remains in `LICENSE`.

Research cards are grouped by direction: EnterpriseSaga under 01; MolWorld and XAI-Refine under 02; RCML and MILNet under 03. XAI-Refine shows a closed loop with an animated flow marker; the feedback arrow represents accepted updates only. Its Pause control and reduced-motion behavior preserve a readable static loop. MILNet displays the complete case-study Figure 3 from the paper at its intrinsic 1380:638 aspect ratio, with a full-resolution image link. The two cases demonstrate complementary local/global strengths.

Profile-conditioned latent dynamics remains in the complete publication list, but is not a featured research card.

The XAI-Refine science-papers link jumps to Publications and activates the AI for science filter. Figure provenance remains documented here rather than in visitor-facing production captions.
