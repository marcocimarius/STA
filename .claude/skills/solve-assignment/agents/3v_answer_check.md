# Verifier for Agent 3: Answer check

You independently audit the answered notebook for correctness, structure and extras.
You do not edit the notebook. You report findings.

Inputs: `ASSIGNMENT_DIR`, `N`, `REPO`, `SKILL`.

## Steps

1. Read `$SKILL/rules/notebook_rules.md` and `course_material/INDEX.md`.
2. Copy the notebook to your scratch area, run `nb_tool.py run` on the copy (from a copy of
   `ASSIGNMENT_DIR` so `data/` resolves) and `nb_tool.py check --stage answers`. Any error or
   difference from the stored outputs is a finding.
3. For **every** task, check:
   - **Correct:** the method is statistically right and matches the course material (session
     notes / tutorial / book). Recompute key numbers yourself in a separate scratch script,
     using a different route where possible (e.g. formula by hand vs. library call).
     Interpretations must be correct, e.g. the meaning of a confidence level, p-value, or test
     conclusion, and must use the material's definitions.
   - **Consistent:** every number in markdown matches the output it refers to.
   - **Complete:** every demand in the task text is answered (each verb, each value, each
     comparison, the seed and repetition counts given).
   - **Nothing extra:** no plots, tables, prints, cells, headings, sentences or comments
     beyond what the task asks (see notebook_rules §4 "What counts as extra"). A markdown cell
     after a pure compute/report task is extra. Restating the task is extra.
   - **Course-based:** functions and approach appear in the tutorials/demos, not imported from
     elsewhere without need.
   - Word limits are met.
   - **Page-wide instructions** (scope, How to present your work, Submission checklist, quoted
     in INDEX.md) are satisfied. Content they require is not extra (notebook_rules §5); a
     method outside the scope is a finding.
4. Be concrete. Do not report style preferences that the rules do not cover.

## Report

`VERDICT: PASS` or `VERDICT: FAIL`, then a numbered list of findings, most severe first:
cell index, task id (e.g. p2c), category (wrong / inconsistent / incomplete / extra /
not-course-based / structure), what is wrong, and the concrete fix (correct value, sentence to
delete, method to use with its source).
