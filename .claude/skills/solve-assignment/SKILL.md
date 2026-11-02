---
name: solve-assignment
description: Solve an STA course assignment end to end from just its assignment page link (rbrooksdk.github.io/STA1_26/assignments/...). An orchestrator runs agents that find and gather the course material (session notes, tutorials, book chapters, data) by browsing the course site, build the notebook skeleton with tasks copied verbatim, answer each task from the material, verify the answers, write docs, and run a final review. Use when the user gives an assignment link and asks to solve, do or set up the assignment.
argument-hint: <assignment-page-url>
---

# Solve assignment: orchestrator

You are the **orchestrator**. You do not gather material, write the notebook, or write docs
yourself. You start the agents below with the Agent tool, wait for them, read their reports,
run the verification loops, and tell the user the outcome. Subagents cannot start
other agents, so all spawning happens here.

`SKILL` = this skill's directory (`<repo>/.claude/skills/solve-assignment`).
`REPO` = the repository root (the folder with `assignment1/`, `assignment2/`, …).
Python for all scripts: `$REPO/.venv/bin/python`.

## 0. Set up the run

1. The only argument is `ASSIGNMENT_URL`, the assignment page link. If it is missing, ask for it.
   Derive `N` from the URL slug (`assignment_04_...` gives 4) and confirm it against the page's
   `# Assignment N — …` heading (`curl -sL` the raw source, see `rules/course_site.md`).
   Everything else (sessions, tutorials, book chapters, data) is found by Agent 1 from that page.
2. `ASSIGNMENT_DIR = $REPO/assignment$N`. If it already contains a notebook, docs or
   material, ask the user before continuing: start fresh (move the old files to
   `assignment$N/_old/`), or stop. Never delete anything.
3. Create `ASSIGNMENT_DIR/{data,course_material,docs}`.
4. Reference rule for every agent: assignment3 is the model (notebook + docs + course_material
   layout). Assignment1/2 notebooks follow the same cell pattern. **Assignment4 and later are
   never references.**

## Starting an agent

Use `subagent_type: "general-purpose"` and this prompt (fill in the values):

```
You are <ROLE> in the solve-assignment workflow.
Read <SKILL>/agents/<BRIEF>.md fully and follow it exactly.
ASSIGNMENT_URL=<url>
ASSIGNMENT_DIR=<abs path>
N=<n>
REPO=<abs path>
SKILL=<abs path>
Scratch area: <your scratchpad dir>/<role>/  (temporary files only)
[FINDINGS:
<numbered findings, verbatim from the verifier>]
```

Agents run in the background. Wait for their completion notification and do not guess
their results. After each agent, read its final report and run
`nb_tool.py check` or `outline` yourself to confirm the claimed state before moving on.

## 1. Material and skeleton (in parallel)

Start both in the same message:
- **Agent 1** (gatherer): brief `1_gather`.
- **Agent 2** (skeleton): brief `2_structure`.

When Agent 2 is done, run the **skeleton check loop**:
1. Start a new verifier agent with brief `2v_structure_check`.
2. `PASS`: the loop ends. `FAIL`: start Agent 2 again with brief `2_structure` and the
   findings as `FINDINGS`. Tell it the notebook exists and it must only correct the listed
   findings, then rebuild.
3. Repeat with a **fresh** verifier. After 3 failed rounds, stop and show the user the
   remaining findings.

When Agent 1 is done, read `course_material/INDEX.md`. If anything essential is missing
(session notes, tutorial, book chapter, or a data file), tell the user what is missing and
ask whether to continue or how to get it (e.g. a login-protected Drive folder), before
starting phase 2.

## 2. Answers

Start only when Agent 1 has finished **and** the skeleton check loop has passed.

- **Agent 3** (answers): brief `3_answer`.
- Then the **answer check loop**: a fresh verifier with brief `3v_answer_check`. On `FAIL`,
  start Agent 3 again with `FINDINGS`, then a fresh verifier. Maximum 3 rounds, then escalate
  to the user with the open findings.

## 3. Docs

Start when the answer check loop has passed.

- **Agent 4** (docs): brief `4_docs`.

## 4. Final review

Start when Agent 4 is done.

- **Agent 5** (final reviewer): brief `5_final_review`.
- On `FAIL`, route each finding:
  - notebook findings (structure, verbatim, extra, incomplete, wrong, ungrounded) go to
    Agent 3 with `FINDINGS`, followed by a fresh `3v_answer_check`;
  - docs findings go to Agent 4 with `FINDINGS`;
  - then run Agent 5 again. Maximum 2 rounds, then escalate to the user.

## 5. Report to the user

Briefly report:
- what was gathered (and anything missing);
- the notebook path, number of tasks, and that the final check/run is clean;
- the docs files;
- the verifier rounds needed and any finding left open or any assumption an agent made.

Do not commit. The user reviews and commits.

## Rules for you

- Never answer tasks or edit the notebook or docs yourself, even for a "quick fix". Send it to
  the responsible agent with `FINDINGS`, so the verifiers stay independent.
- Pass verifier findings on verbatim. Do not soften or filter them.
- Every verification round uses a new verifier agent, never a resumed one.
