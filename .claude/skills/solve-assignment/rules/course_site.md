# The course website and how to read it

The user gives **only the assignment page link**, e.g.
`https://rbrooksdk.github.io/STA1_26/assignments/assignment_04_one_and_two_sample_tests/#preparation-resources-and-ai`.
Ignore the `#fragment`. Everything else is found from that page.

## Site layout (verified for STA1_26)

The site is an MkDocs build of the public GitHub repo `RBrooksDK/STA1_26` (`docs_dir: .`).
Every page has a markdown source in the repo, and the raw source is the most reliable
copy of the text (exact wording, LaTeX, links):

| Site page | Raw source |
|---|---|
| `<site>/assignments/<slug>/` | `https://raw.githubusercontent.com/RBrooksDK/STA1_26/main/assignments/<slug>.md` |
| `<site>/<NN_Session_Title>/` | `.../main/<NN_Session_Title>/README.md` |
| `<site>/<NN_Session_Title>/Tutorial_NN_notebook/` | `.../main/<NN_Session_Title>/Tutorial_NN_notebook.ipynb` (and `Tutorial_NN.md`) |
| `<site>/data/<file>` | `.../main/data/<file>` |

`<site>` = `https://rbrooksdk.github.io/STA1_26`. The full file list:
`curl -s "https://api.github.com/repos/RBrooksDK/STA1_26/git/trees/main?recursive=1"`.

Derive the repo path from the page URL. If the site ever moves to another host or repo, find the
"edit/view source" or GitHub link in the page HTML (`curl -sL <url> | grep -o 'href="[^"]*github[^"]*"'`).

## The assignment page

- `# Assignment N — <Title>`. N and the title come from here.
- `!!! info "Practical information"` holds the **statistical scope** ("Sessions 7–8 and Brooks,
  Chapters 7–8").
- `## Preparation, resources and AI` names the sessions, tutorials, book chapters and data files,
  and includes `### How to present your work` and `### Working with AI`. It often names sessions
  only by number ("Sessions and Tutorials 7 and 8") with links to the session READMEs.
- `## Part K — <title>`: intro text, sometimes `### <sub-section>` blocks with their own intro,
  and the tasks as a **numbered markdown list** (`1.`, `2.`, …).
- The last Part is AI-use and conclusion with `### AI-use` and `### Overall conclusion`.
- `## Submission checklist` and `## Theory and code at the oral exam` come after the parts.

## A session page (`<NN_Session_Title>/README.md`)

- Intro, Key Concepts, Learning Objectives.
- `### Session Preparation:` gives the book chapter ("Brooks: Chapter 7"), linked to the book.
- `### Resources`:
  - **Session material**: a GitHub tree `.../<NN_...>/session_material` with demo notebooks
    (e.g. `hypothesis_testing_demo.ipynb`) and sometimes data.
  - **Session notes**: a Google Drive link, either a single file (`drive.google.com/file/d/<ID>/view`)
    or a folder. Download a file with
    `curl -sL -o <out>.pdf "https://drive.google.com/uc?export=download&id=<ID>"`.
  - **Tutorial NN**: `Tutorial_NN_notebook.ipynb` (plus `Tutorial_NN.md`) in the session folder.
- Session folders are named `NN_<Title>`; the list is in the repo tree and on `<site>/Sessions/`.
  When the assignment names a session only by number, find its folder there.

## The book

`https://raw.githubusercontent.com/RBrooksDK/STA_book_v1/main/main.pdf` (the site links it
through `docs.google.com/viewer?url=...`; download the raw URL). It has bookmarks, so
`pdf_tool.py toc` finds chapter page ranges.

## Mapping page text to notebook cells (as assignment3 did it)

| Page source | Notebook |
|---|---|
| `# Assignment N — Title` | `### Assignment N — Title ###` + participants |
| `## Part K — title` + intro paragraphs | one `## Part K — title` cell with the intro verbatim |
| Lead-in line "Complete the following tasks:" directly before the list | dropped (the only allowed omission; assignment3 did this) |
| `### <sub-section>` inside a Part + its intro | one `### <sub-section>` cell with its intro verbatim |
| Numbered task `1.` `2.` … | one `#### a)` `#### b)` … cell each. Letters run **continuously through the whole Part**, across sub-sections, so ids stay unique (`p1a`…`p1f`) |
| `### AI-use` / `### Overall conclusion` in the last Part | `#### AI-use` / `#### Overall conclusion` task cells with their text |
| `\( ... \)` / `\[ ... \]` | `$ ... $` / `$$ ... $$` |
| `[file.csv](../data/file.csv)` | `` `file.csv` `` |
| other links `[text](url)` | `text` |
| Preparation, How to present, Working with AI, Analysis order, Submission checklist, Oral exam | **not** copied into the notebook. They are binding instructions for Agent 3 and the verifiers (see notebook_rules §5) |
