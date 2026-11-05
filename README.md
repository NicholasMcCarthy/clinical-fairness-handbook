# Clinical Fairness Handbook

A Quarto textbook and practical resource for clinicians, researchers, ML engineers, auditors, and service leads. The working edition is dated **5 November 2026**.

The book develops the clinical arguments in the current CFT short and long manuscripts. It distinguishes prediction quality, decision fairness, uncertainty, and patient outcomes. It includes 15 substantive chapters, 5 practical appendices, 51 cited sources, equations with plain-language explanations, worked examples, exercises and suggested answers, and 15 illustration briefs.

## Read and build

Install [Quarto](https://quarto.org/docs/get-started/) (tested with **1.11.9**). No R, Jupyter, Python execution engine, clinical datasets, or toolkit installation is required to render the prose book.

```sh
quarto render --to all
quarto preview
```

The HTML book opens at `_book/index.html`. The EPUB is `_book/Clinical-Fairness-Handbook.epub`. The HTML includes search, chapter navigation, light/dark themes, cross-references, linked citations, and an EPUB download. Some reading systems need MathML support to display EPUB equations. The HTML uses MathJax and may need network access to load its math runtime on first use.

On Windows, the helper also recognises a portable Quarto at `.tools/bin/quarto.exe`:

```powershell
.\scripts\render.ps1
.\scripts\render.ps1 -Format html
.\scripts\render.ps1 -Preview
```

The portable tool directory, generated books, and review artifacts are ignored by Git. A fresh checkout needs Quarto installed or supplied locally. No machine-wide settings are changed by the helper.

## Contents

- Foundations: introduction, clinical applications, data and audit design, and four modelling tasks.
- Evaluation: clinical utility, fairness criteria, uncertainty and small groups.
- Interventions: binary, multiclass, regression, survival, and broader fairness research.
- Practice: worked cases, CFT use, reporting and monitoring.
- Appendices: glossary, audit worksheet, exercise answers, illustration briefs, and source notes.

`_quarto.yml` controls the book. Chapters are independent `.qmd` sources. `references.bib` contains only cited sources. Styles live in `styles/`.

## Check changes

The standard-library checker verifies chapter registration, citations, cross-reference targets, illustration accounting, local links in the rendered HTML, EPUB package contents, and the arithmetic of the principal teaching examples:

```powershell
& C:/Users/Nick/anaconda3/envs/cft/python.exe scripts/check_book.py
```

On another machine, use `python scripts/check_book.py`. Render both formats first for a complete check. This checks the document package and teaching arithmetic, not clinical validity or the truth of every cited claim.

For individual formats, use `quarto render --to html --no-clean` or `quarto render --to epub --no-clean` to preserve the other output. The Windows helper includes this option.

## Sources and editorial status

`sources/manifest.json` records file hashes and commits from the publication and toolkit repositories. The book can render independently of those sibling checkouts. The source-notes appendix maps manuscript arguments to handbook content and distinguishes research algorithms from native CFT adaptations.

All numerical teaching examples are labelled as invented. Historical benchmark results have not been relabelled. No new clinical model experiments were run. The book contains textual illustration placeholders rather than borrowed figures; the briefs explain what each eventual figure should show.

The next editorial tasks are author/methodological review, original illustrations, and decisions about authorship, licensing, and publication. The book has not been published or represented as externally reviewed.
