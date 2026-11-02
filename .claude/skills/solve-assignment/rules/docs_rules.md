# Docs rules

Reference: `assignment3/docs/*.md` (read at least one in full before writing). Never use
`assignment4` or later docs as the reference.

## Files

- One file per assignment part that has statistical content: `docs/partK_<snake_case_topic>.md`
  (e.g. `part2_estimating_a_mean.md`). The AI-use/conclusion part gets no doc.
- Each file explains that part's theory and every task of it: **what** was done, **how**
  (formula, code function, numbers), and **why** that method, plus how the result is read.

## Skeleton of each file (as in assignment3)

```
# Part K: <part title> (<statistical topic>)

Sources: Session X notes, Tutorial X, <demo notebook if any>, <Book> Chapter Y.

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [Ka: <short task label>](#...)
...
N-1. [Formula sheet](#...)
N. [Likely oral-exam questions](#...)

---

## 1. The situation in plain words
## 2. Vocabulary you need first        (table: Term | Meaning in plain words)
## 3. Ka: <short label>                (one section per task, ### subsections only if needed)
...
## Formula sheet                       (table: formula | expression, incl. the SciPy/statsmodels call)
## Likely oral-exam questions          (numbered, bold question + 1–3 sentence answer)
```

Sections are separated by `---`. Contents links must resolve to the GitHub-style heading slugs.

## Writing style

- Explain in plain words first, then the formula, then the numbers from the notebook.
- Explain in detail, but keep it readable: short paragraphs (2–4 sentences), bullet lists,
  small tables for "step | formula | value", and an occasional ASCII sketch when it makes a
  picture clearer. Aim for roughly 180–300 lines per file. Do not repeat the same point in
  several sections.
- Link each part to the previous ones and to the course ("**The link to Part 1:** …").
- Every number must match the executed notebook. Every definition and formula must match the
  session notes / book, and name the source where a reader might want to look it up.
- Mention the code function used and why (e.g. "`x.std(ddof=1)` divides by $n-1$").
- Call out common mistakes and exam favourites (e.g. what "95% confidence" does and does not mean).
