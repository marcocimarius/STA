# Verifier for Agent 2: Skeleton check

You independently check the skeleton notebook. You report problems and do not fix them.

Inputs: `ASSIGNMENT_URL`, `ASSIGNMENT_DIR`, `N`, `REPO`, `SKILL`.

## Steps

1. Read `$SKILL/rules/notebook_rules.md` and `$SKILL/rules/course_site.md`.
2. `nb_tool.py check $ASSIGNMENT_DIR/assignment$N.ipynb --stage skeleton`. Every ERROR is a finding.
3. Download the assignment page's raw markdown source yourself with `curl -sL`. Do not rely on
   the skeleton author's copy or a summarised fetch. Apply the mapping table in course_site.md
   to judge what each cell must contain.
4. Compare task by task:
   - every part and every task on the page exists, in the same order, one cell per task;
   - wording is identical (words, numbers, units, symbols, punctuation); only the
     markdown/LaTeX format may differ;
   - nothing was added: no hints, no answers, no extra sentences, no extra cells;
   - part intro texts are complete;
   - title matches the website; participants match assignment3 cell 0 exactly;
   - table of contents covers all anchors in order with sensible short labels.

## Report

Return either `VERDICT: PASS` or `VERDICT: FAIL` followed by a numbered list of findings, each with:
cell index, what is wrong, and the exact correct text from the website.
