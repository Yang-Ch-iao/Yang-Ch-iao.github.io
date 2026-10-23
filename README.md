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

- **EnterpriseSaga:** a static evidence chain based on the Northstar billing example in Figure 1.
- **MolWorld:** A smooth-contour graph with two illustrative rounds following Figure 1 and Section 3.2: select five connected molecules from the current graph, sample multiple candidates together, verify their MMP links, and incorporate connected candidates. Links are not prescribed by conditioning and may reach existing molecules outside the selected context. An unconnected candidate is excluded in each round; the second anchor includes a molecule accepted in the first round. Nodes are whole molecules; edges are MMP relations. The H-to-methyl inset illustrates a local structural modification, not a synthesis reaction. Graph coordinates, batch sizes, and animation timing are schematic. Every accepted candidate has a verified edge to the graph that existed before its generation round.
- **RCML:** a static comparison of fixed and relation-conditioned representation spaces, based on Figure 1.
- **XAI-Refine:** the explanation, literature verification, constrained revision, and validation loop.
- **Profile-conditioned latent dynamics:** training supervision from observed transitions versus inference from the profile and current context.

MolWorld pauses offscreen and when the tab is hidden, supports pause/replay and a step-by-step control, and shows the completed graph by default for reduced-motion preferences. All research figures and core content remain readable without JavaScript.

The previous AcademicPages source is retained for recovery and reference, but is not used to generate the new homepage. The original theme license remains in `LICENSE`.
