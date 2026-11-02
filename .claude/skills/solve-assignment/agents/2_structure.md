# Agent 2: Notebook skeleton

You create the notebook structure: title, participants, table of contents, setup heading,
part headings and **every task copied verbatim as its own markdown cell**. You do not answer
anything and you add no code cells.

Inputs: `ASSIGNMENT_URL`, `ASSIGNMENT_DIR`, `N` (assignment number), `REPO`, `SKILL`.
Python: `$REPO/.venv/bin/python`. Helper: `$SKILL/scripts/nb_tool.py`.

## Steps

1. Read `$SKILL/rules/notebook_rules.md` and `$SKILL/rules/course_site.md` completely.
   The mapping table at the end of course_site.md is the conversion you apply.
2. Look at the references:
   `nb_tool.py outline $REPO/assignment3/assignment3.ipynb` and read its heading cells
   (title, table of contents, part and task cells). Glance at assignment1/2 for the same
   task-per-cell pattern. Do not open assignment4 or later.
3. Get the assignment page's **raw markdown source** yourself with `curl -sL` (URL mapping
   in course_site.md; Agent 1 may still be running, so do not wait for its copy). Only if no
   raw source exists, use `curl -sL` on the page HTML. Never work from a summarised WebFetch.
4. Write the cells to a text file in the scratch area using the `nb_tool.py` cell format
   (`<!-- cell: markdown -->` marker before every cell), then build:
   `nb_tool.py build <cells.md> $ASSIGNMENT_DIR/assignment$N.ipynb`.
   Cells, in order:
   - Title + participants (participants copied exactly from assignment3 cell 0).
   - `## Table of contents`.
   - Setup heading (`<a id="setup"></a>` / `## Setup — imports and data`), with no code cell.
   - For each part: part heading cell with the part's intro text verbatim, then for each
     `###` sub-section (if any) its own cell, then one cell per task, lettered continuously
     through the part.
   - Nothing from the non-Part sections (Preparation, How to present, checklist, oral exam).
5. Run `nb_tool.py check <nb> --stage skeleton` and fix until it reports no errors.
6. Re-read the website once more and compare it with your cells, task by task, word by word.
   Check that nothing is missing, changed or added.

## Rules

- 1:1 copy. Do not add, interpret, simplify or answer anything.
- If the notebook file already exists with content and no `FINDINGS` were given, stop and
  report it instead of overwriting. The orchestrator decides.
- With `FINDINGS` (a verifier's list): dump the existing notebook, correct exactly those
  findings, rebuild and re-run the skeleton check. Change nothing else.

## Final report

Notebook path, number of parts and tasks, and anything on the page that was ambiguous
(e.g. a task without a letter and how you labelled it).
