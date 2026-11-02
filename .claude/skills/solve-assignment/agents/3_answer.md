# Agent 3: Answer the tasks

You answer every task in the skeleton notebook, using only the gathered course material
as the basis for methods and explanations.

Inputs: `ASSIGNMENT_DIR`, `N`, `REPO`, `SKILL`, and possibly `FINDINGS` (a verifier's list
of problems to fix. In that case fix exactly those and leave everything else as it is).
Python: `$REPO/.venv/bin/python`. Helper: `$SKILL/scripts/nb_tool.py`.

## Before writing anything

1. Read `$SKILL/rules/notebook_rules.md` completely. §4 (answers, "extra" is forbidden) is the core of your job.
2. Read `ASSIGNMENT_DIR/course_material/INDEX.md`. Its scope and page-wide instructions
   (How to present your work, Analysis order, Submission checklist) apply to every answer
   (notebook_rules §5). Then read the relevant materials: tutorials
   (all code), session transcripts (check the PDF pages for formulas you rely on), the book
   chapter extracts and demo notebooks.
3. Study `$REPO/assignment3/assignment3.ipynb` as the style model: how long answers are, how
   code prints results, how markdown answers start. Assignment1/2 notebooks may be used for
   methods from earlier topics. Never use assignment4 or later.

## Working method

1. `nb_tool.py dump <nb> <scratch>/cells.md`, edit the text file, `nb_tool.py build <scratch>/cells.md <nb>`.
   Never change task, part, title or table-of-contents cells, except when a finding in
   `FINDINGS` names one of them and gives the correct website text.
2. Fill the Setup code cell, then go task by task. Write the code first, build, and run
   `nb_tool.py run <nb>`. Read the actual outputs (`nb_tool.py outline`, or open the
   notebook JSON) and only then write the markdown, quoting those numbers.
3. For each task, ask yourself:
   - Which words in the task demand something (compute, table, plot, explain, compare,
     interpret, verify)? Answer each one, in order, and nothing else.
   - Which material shows how this is done? Use that function, formula and wording.
   - Is any cell, plot, sentence or comment not required by the task? Remove it.
4. Word limits given by the task (e.g. "150–250 words") must be met. Count them.
5. Finish with `nb_tool.py run <nb>` (must print OK) and
   `nb_tool.py check <nb> --stage answers` (no ERRORs, and resolve every WARNING).

## Final report

For each task: the material it is based on (file + section/page), and any assumption you
had to make. Do not paste the answers.
