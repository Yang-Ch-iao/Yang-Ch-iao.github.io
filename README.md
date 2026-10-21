# Yang Qiao — personal website

Live site: https://yang-ch-iao.github.io/

A static academic homepage, served by GitHub Pages from the root of the `master` branch. No package installation or backend is required. `.nojekyll` bypasses the previous Jekyll theme.

## Update content

- **Publications and contact links:** edit `content.json`, then run `python3 build_home.py`.
- **Biography, research, education, service, and teaching:** edit the corresponding text in `build_home.py`, then run `python3 build_home.py`.
- **CV:** replace `files/Yang_Qiao_CV.pdf` and `files/Yang_Qiao_CV.docx`.
- **Photograph:** replace `images/profile.jpg`. Cropping is controlled by `.portrait-frame` in `assets/home/site.css`.
- **Design:** edit `assets/home/site.css`.
- **Interactive diagrams and publication filters:** edit `assets/home/site.js`.

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

All research diagrams are conceptual illustrations, not experimental results. EnterpriseSaga has play/pause and step controls; MolWorld has a keyboard-accessible stage slider; RCML lets visitors change the semantic relation. Animations respect reduced-motion preferences. Publications and other core content remain readable without JavaScript.

The previous AcademicPages source is retained for recovery and reference, but is not used to generate the new homepage. The original theme license remains in `LICENSE`.
