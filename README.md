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

Research is grouped by direction: EnterpriseSaga under LLM Agents & Retrieval; MolWorld and XAI-Refine under AI for Science; RCML and MILNet under Multimodal Learning. XAI-Refine shows a circular explanation–knowledge loop around an explicit brain-age model. Verification compares model and domain claims using retrieved evidence; minimal revision yields a regularization term for retraining. Only accepted updates return to explanation discovery. Its Pause control and reduced-motion behavior preserve a readable static loop. MILNet leads with complementary local/global views and correct-prediction-gated mutual learning. Two original dataset photographs corresponding to Figure 3, with illustrative local/global outlines, support a newly typeset outcome table; these are the paper’s case outcomes, not an aggregate accuracy claim. Each research card introduces the problem and core method illustrated by its adjacent figure.

Profile-conditioned latent dynamics remains in the complete publication list, but is not a featured research card.

The XAI-Refine science-papers link jumps to Publications and activates the AI for science filter. Figure provenance remains documented here rather than in visitor-facing production captions.

MILNet displays the original photographs by default, with the paper’s detector annotations and a short explanation available in a native disclosure. Images come from the public `coderchen01/MMSD2.0` Hugging Face mirror, `mmsd-clean` validation split: `865927535187697664` (context) and `881702009786781696` (faces), matched to `headacheboy/data-of-multimodal-sarcasm-detection/text/valid2.txt` and visually checked against Figure 3. Images retain their full content and natural proportions; no inpainting or reconstructed imagery is used. The original meme lettering is part of the input. The outcome table follows the paper’s case-study prose; it does not infer class labels from the figure’s ambiguous bar colors.

MolWorld runs two four-second rounds in a continuous eight-second loop, with overlapping selection, generation, verification and incorporation transitions and no end-of-cycle hold. A brief fade resets generated content to the original graph. Manual pause, step, replay, offscreen suspension and reduced-motion static rendering remain available. XAI labels and correction flow follow Sections 4.2–4.3 and Figure 1.

XAI’s verification node receives a neutral-question route from model claims and a separate, right-hand literature-corpus input. Its output is compiled into verified domain claims before comparison.

MolWorld’s original peripheral molecules have local perimeter links, and every generated molecule has at least three displayed connections. The animation retains 19 original and 28 representative generated edges. XAI returns to a circular animated loop with an explicit central brain-age model, model-to-explanation and retraining-to-model links, plus a separate domain corpus exchanging queries and evidence with Verify. MILNet cycles between local detail, global context and complementary views using a few uniform illustrative outlines over the original photos; these are not measured attention or detector outputs. Its animation supports pause, offscreen suspension and reduced motion. Original Figure 3 remains in the evidence disclosure.

Featured-paper introductions are paraphrased from their abstracts and central method descriptions (EnterpriseSaga latest local manuscript; MolWorld v2; RCML; XAI-Refine; MILNet), emphasizing the problem and specific contribution rather than explaining UI controls. Desktop cards use 40% introduction / 60% figure columns; narrow screens retain stacked layouts.

The homepage uses a centered reading column with a short, non-sticky row of section links below the biography. Desktop research entries pair unboxed introductions with separate figure panels; screens up to 900px stack the introduction above the figure. Section numbering and the fixed sidebar have been removed. Contact links and publication filters use text rather than pills.

EnterpriseSaga and MolWorld receive larger project titles and fuller introductions. XAI-Refine, RCML and MILNet retain their core methods and complete interactive figures in more compact entries. The biography now describes recent work directly and links to the corresponding projects; no new research claims or personal history were introduced.
