# Notebook rules

These rules apply to every notebook the skill produces. The reference notebook is
`assignment3/assignment3.ipynb`; `assignment1` and `assignment2` follow the same task/answer
cell pattern (they only lack the table of contents and anchors). **Never use `assignment4`
or any later notebook as a reference.** Their style is not the one wanted.

The notebook lives at `assignmentN/assignmentN.ipynb` and reads data with relative paths
(`pd.read_csv("data/<file>.csv")`).

## 1. Cell order

| # | cell | type | content |
|---|------|------|---------|
| 0 | Title | markdown | `### Assignment N — <Title exactly as on the website> ###`, blank line, `Participants:`, then the participant list copied **unchanged** from cell 0 of the most recent previous notebook (assignment3). |
| 1 | Table of contents | markdown | `## Table of contents`, then a nested bullet list linking every anchor in order (see §3). |
| 2 | Setup heading | markdown | `<a id="setup"></a>` newline `## Setup — imports and data` |
| 3 | Setup code | code | All imports and every `pd.read_csv(...)`, then `display(df.head())` for each data set. Added by Agent 3, not Agent 2. |
| … | Part heading | markdown | `<a id="partK"></a>` newline `## Part K — <part title verbatim>`, blank line, then the part's introduction text verbatim from the website (data description, definitions, given values). |
| … | Sub-section (only if the page has `###` blocks inside a part) | markdown | `<a id="pK-<slug>"></a>` newline `### <sub-section title>`, blank line, its intro text verbatim. |
| … | Task | markdown | `<a id="pKx"></a>` newline `#### x) <task text verbatim>` |
| … | Answer cell(s) | code / markdown | Directly after the task, added by Agent 3 (see §4). |

The last part of the website (AI-use, overall conclusion, reflection, etc.) follows the same
pattern. Tasks without a letter get a descriptive anchor (`ai`, `conclusion`) and the heading
uses the website's wording (e.g. `#### AI-use`), with the website's instruction text copied
under the heading in the same cell (see assignment3 cells 53 and 55).

## 2. Copying tasks verbatim

- The source of truth is the page's **raw markdown** on GitHub (see `rules/course_site.md`),
  not a summarised fetch of the rendered page.
- Copy the wording **1:1**: same words, order, numbers, units, punctuation. Do not shorten,
  paraphrase, merge, split or "clarify".
- Convert only the **format**, following the mapping table in `rules/course_site.md`:
  `\(...\)` becomes `$...$`, numbered tasks become `a)`, `b)`, …, and data-file links become
  backticked file names (as in assignment3: `$\bar X$`, `` `assignment03_sensor_calibration.csv` ``).
- One cell per lettered task. If a task has sub-bullets on the website, they stay inside that
  task's cell.
- Never put hints, answers, extra notes, emojis or "TODO" text into task or part cells.

## 3. Anchors and table of contents

- Anchor ids: `setup`, `part1`, `part2`, …, `p1a`, `p1b`, …, `p2a`, …, plus `ai` / `conclusion`
  (or another short descriptive id) for unlettered tasks.
- The anchor line is the first line of the heading cell: `<a id="p1a"></a>`.
- Every anchor appears exactly once in the table of contents, in notebook order, and every
  table-of-contents link points to an existing anchor. Format:

  ```
  ## Table of contents

  - [Setup — imports and data](#setup)
  - [Part 1 — <part title>](#part1)
      - [a) <short label of the task>](#p1a)
      - [b) <short label>](#p1b)
  - [Part 4 — AI-use and conclusion](#part4)
      - [AI-use](#ai)
      - [Overall conclusion](#conclusion)
  ```

  The short labels are condensed task names (as in assignment3), the only place where task
  text may be shortened.

## 4. Answers (Agent 3)

Directly after each task cell, add only what the task asks for:

- **Code cell** when the task asks to compute, simulate, report numbers, create a table or plot.
  One code cell per task in most cases. Tables are `pd.DataFrame(...).round(k)` as the last
  expression; scalars are `print(f"...")` lines that show the formula and the value
  (assignment3 cells 22, 28, 34).
- **Markdown cell** only when the task asks for words: *explain, interpret, discuss, compare,
  state, describe, justify, why, conclude*. If the task is only "report / compute / create a
  table / plot", the code cell is the whole answer, with no markdown after it (assignment3 cells
  6, 40, 48).
- If the task asks only for words, answer with a single markdown cell (assignment3 cell 19).
- Markdown style: start directly with the content. No `Answer:` label and no headings. Use
  short bullet points or short paragraphs with **bold lead-ins** that mirror what the task
  asked (e.g. `**Centre:**`, `**Spread:**`, `**Shape:**`; `**Interpretation of the interval:**`).
  Quote the concrete numbers from the executed output, rounded sensibly.
- Every part of a multi-part task is answered (e.g. "construct … verify with SciPy and
  interpret both"), in the task's order.

### What counts as "extra" and is forbidden

- Plots, tables, printed values or code cells the task did not ask for. Exploratory
  `df.describe()`, `df.info()` and similar cells are not allowed outside the Setup cell.
- Markdown that restates the task, announces what the code does ("Below we compute…"),
  summarises the section, or adds tips, caveats or extensions the task did not ask for.
- Additional headings, horizontal rules, "Note:" boxes, or emojis.
- Sentences unrelated to the specific question. Every sentence must answer some part of the task.
- Code comments beyond a few short ones where a step is not obvious. No commented-out code.

### Methods and style must come from the course

- Use the functions and approach shown in the gathered tutorials and session demos
  (`course_material/`), e.g. `scipy.stats`, `statsmodels`, `np.random.default_rng(seed)` with
  the seed the task gives. Do not bring in libraries or methods the course did not use.
- Definitions, formulas, assumptions and interpretations follow the session notes and the book
  chapters. When the materials and general knowledge differ in notation or wording, use the
  materials'.
- Plot style as in assignment3: `fig, ax = plt.subplots(...)`, colours `"#6CA2C6"` (bars or
  main data) and `"#FF8C00"` (reference or fitted line), axis labels with units, a title,
  a legend when there is more than one element, `plt.tight_layout()`, `plt.show()`.
- The notebook must run top to bottom without errors (`nb_tool.py run`), and all numbers in
  markdown must match the stored outputs.

## 5. Page-wide instructions are requirements, not extras

The assignment page's non-task sections (statistical scope, "How to present your work",
"Analysis order", "Submission checklist") apply to every answer. Examples: "state the
population, parameter, … before reporting the software result", "report intervals in
engineering units", "only use Sessions 7–8". Content that one of these sections requires is
**not** extra. Keep it as short as the requirement allows, in the cell of the task it
belongs to. Methods outside the statistical scope are forbidden.

### AI-use cell

Follow assignment3 cell 54: state that Claude Code with the model in use was used, what it
contributed (code following the named tutorials/session demos, markdown text), and how the
work was verified. Keep the same structure and length.
