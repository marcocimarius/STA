# Agent 5: Final review

All other agents are done. You do the final, independent end-to-end review of the
notebook (and a consistency pass over the docs). You do not edit files. You report findings.

Inputs: `ASSIGNMENT_URL`, `ASSIGNMENT_DIR`, `N`, `REPO`, `SKILL`.

## Checklist

1. Read `$SKILL/rules/notebook_rules.md`.
2. `nb_tool.py check <nb> --stage answers` and a fresh `nb_tool.py run` on a scratch copy of
   `ASSIGNMENT_DIR`. Must be clean, with outputs identical in substance to the stored ones.
3. **Structure:** title + participants, table of contents (all anchors, in order), setup,
   parts, one cell per task, answers directly after their task, nothing between a task and
   its answer, no stray cells.
4. **Tasks verbatim:** download the page's raw markdown source yourself (`rules/course_site.md`)
   and compare every part, sub-section and task cell with it word by word, applying the mapping table.
5. **Page-wide instructions:** every answer satisfies the page's "How to present your work",
   "Analysis order", "Submission checklist" and statistical scope (quoted in
   `course_material/INDEX.md`). Content they require is not extra (notebook_rules §5).
6. **Answers:** each one answers its task fully and only its task. Flag every extra plot,
   cell, sentence, heading or comment (notebook_rules §4).
7. **Grounded in the material:** for each task, name the course file that supports the method
   and the statements (`course_material/INDEX.md`). Flag anything that has no basis in the
   sessions, tutorials, book chapters or earlier assignments, or that contradicts them.
8. **Docs consistency:** numbers and method names in `docs/*.md` match the notebook. Every
   part has a doc.

## Report

`VERDICT: PASS` or `VERDICT: FAIL`, then numbered findings: file, cell index / doc section,
category (structure / verbatim / extra / incomplete / wrong / ungrounded / docs), the problem,
and the concrete fix.
