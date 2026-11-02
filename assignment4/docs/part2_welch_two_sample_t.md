# Part 2: Independent coating processes (Welch two-sample t procedure)

Sources: Session 8 notes, Tutorial 8, Brooks Chapter 8 (8.1, 8.2, 8.5).

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [2a: why independent, group summaries, boxplots](#3-2a-why-independent-group-summaries-boxplots)
4. [2b: the Welch test and interval](#4-2b-the-welch-test-and-interval)
5. [2c: checking the assumptions](#5-2c-checking-the-assumptions)
6. [2d: zero, the 8-hour threshold and the recommendation](#6-2d-zero-the-8-hour-threshold-and-the-recommendation)
7. [Formula sheet](#7-formula-sheet)
8. [Likely oral-exam questions](#8-likely-oral-exam-questions)

---

## 1. The situation in plain words

A factory has a **standard** coating process and a **modified** one. Specimens were coated with one process or the other, and each specimen's **durability** (hours until failure) was measured:

- 48 specimens with the modified process,
- 44 *different* specimens with the standard process.

**Question:** does the modified process last longer *on average*, and by how much? The parameter is a **difference of two population means**:

$$\delta = \mu_{\text{modified}} - \mu_{\text{standard}} \quad \text{(hours)}.$$

A positive $\delta$ means the modified coating lasts longer. An increase of **at least 8 hours** is what engineering considers worth having.

**The link to Part 1:** Part 1 compared *one* mean with a fixed number (0 °C). Now we compare *two* means with each other. The recipe is the same (Session 8 notes, page 1):

$$\text{test statistic} = \frac{\text{estimate} - \text{null value}}{\text{standard error}}.$$

Only the estimate (a difference) and its SE (built from two samples) change.

---

## 2. Vocabulary you need first

| Term | Meaning in plain words |
|---|---|
| **Independent samples** (Def. 8.1) | Knowing the observations in one group tells you nothing about the other; observations are also independent within each group. |
| **Paired observations** (Def. 8.2) | Each observation in one condition has a specific, meaningful partner in the other (e.g. the same unit measured twice). |
| **Comparison order** | Which group is subtracted from which. Fixed **before** looking at the data, because swapping flips the sign. Here: modified − standard. |
| **Welch's procedure** | The default t procedure for two independent means. Allows the two groups to have **different** variances. |
| **Pooled procedure** | The classical alternative that assumes **equal** population variances. Not our default. |
| **Welch–Satterthwaite df ($\nu$)** | The approximate degrees of freedom for Welch's t; usually not a whole number. |
| **Practical threshold** | The smallest effect that matters in practice (8 h). Comes from engineering, not from statistics. |

**Design first** (Session 8 notes, page 1): "The design — how the data were collected — decides the test. Not the spreadsheet."

---

## 3. 2a: why independent, group summaries, boxplots

### Why independent and not paired

- Each specimen received **only one** coating process. The 48 modified and 44 standard specimens are **different units**.
- No specimen has a natural partner in the other group. The group sizes even differ (48 vs. 44), so a one-to-one pairing is impossible.
- Sorting the two columns and matching them row by row would **invent** a pairing the design does not contain (Session 8 notes, page 2: "Is that a paired design? → NO!").

```
   Independent (this part)          Paired (Part 3)
   modified    standard             before      after
     m1          s1                   b1 ------- a1
     m2          s2                   b2 ------- a2
     m3          s3                   b3 ------- a3
     ...         ...                  ...  same building
   no links between groups          each row = one unit
```

### Group summaries

| process | $n$ | mean (h) | SD (h) |
|---|---|---|---|
| modified | 48 | 132.49 | 22.19 |
| standard | 44 | 117.29 | 15.75 |

`x.std(ddof=1)` gives the sample SD (divides by $n-1$), as in earlier assignments.

**Reading the boxplots:** the modified box sits clearly higher (higher median), but it is also **taller**: the modified process is more variable (SD 22.19 vs. 15.75 h). Unequal spread is exactly the situation Welch's procedure is built for.

---

## 4. 2b: the Welch test and interval

### Hypotheses

- $H_0: \delta = 0$ h (no difference in mean durability)
- $H_1: \delta \neq 0$ h (two-sided, as the assignment asks)
- $\alpha = 0.05$

### The standard error of a difference

For independent samples there is no covariance term, so the variances simply **add** (Session 8 notes, page 2):

$$\operatorname{Var}(\bar X_m - \bar X_s) = \frac{\sigma_m^2}{n_m} + \frac{\sigma_s^2}{n_s}
\quad\Rightarrow\quad
\text{SE} = \sqrt{\frac{s_m^2}{n_m} + \frac{s_s^2}{n_s}}.$$

Note: variances add even though we *subtract* the means. Two uncertain numbers give a more uncertain difference.

### Step by step

| step | formula | value |
|---|---|---|
| estimated difference | $\bar x_m - \bar x_s = 132.49 - 117.29$ | **15.20 h** |
| standard error | $\sqrt{22.19^2/48 + 15.75^2/44}$ | 3.987 h |
| test statistic | $15.20 / 3.987$ | **$t = 3.812$** |
| Welch–Satterthwaite df | formula below | **$\nu = 84.84$** |
| two-sided p-value | $2\,P(T_{84.84} \ge 3.812)$ | **0.00026** |
| critical value | $t_{84.84,\,0.975}$ | 1.988 |
| 95% CI | $15.20 \pm 1.988 \times 3.987$ | **[7.27, 23.13] h** |

The df formula (Brooks 8.2):

$$\nu = \frac{\left(\dfrac{s_m^2}{n_m} + \dfrac{s_s^2}{n_s}\right)^2}{\dfrac{(s_m^2/n_m)^2}{n_m - 1} + \dfrac{(s_s^2/n_s)^2}{n_s - 1}}.$$

$\nu$ always lies between $\min(n_m, n_s) - 1 = 43$ and $n_m + n_s - 2 = 90$. It is lower when one group's variance term dominates.

### The code

```python
res_w = ttest_ind(modified, standard, equal_var=False, alternative="two-sided")
ci_w  = t.interval(0.95, df=res_w.df, loc=diff, scale=se_w)
```

- `equal_var=False` is what makes it **Welch**. The default `equal_var=True` would be the pooled test.
- The **order of the arguments** sets the comparison order: `ttest_ind(modified, standard)` estimates modified − standard.
- `res_w.df` returns $\nu$, so the interval uses the same df as the test (Tutorial 8 does exactly this).

### Why no variance pre-test?

The assignment forbids running e.g. Levene's test and then switching between pooled and Welch. Reasons (Brooks 8.2, Session 8 notes page 4):

- Welch performs well when variances are equal **and** stays correct when they are not, so there is nothing to gain from switching.
- A pre-test adds a **data-dependent decision** before the main test, which distorts the stated error rates.
- Similar sample SDs do not prove equal population variances anyway.

### Decision

$p = 0.00026 < 0.05$ → **reject $H_0$**. The data provide evidence that mean durability differs between the processes. The modified process is estimated to last **15.20 h longer** on average (95% CI 7.27 to 23.13 h). The interval excludes 0, which agrees with the test (duality, as in Part 1).

---

## 5. 2c: checking the assumptions

Brooks Table 8.2 lists what to check. The notebook looks at each group separately with a histogram and a QQ-plot of **residuals** (value − group mean).

### Independence: from the design, not the plots

- **Between groups:** separate specimens, each with one process → independent by design.
- **Within groups:** specimens must not be linked, e.g. cut from the same panel or tested together on one rig in one session. That has to be documented by whoever ran the study; it cannot be read from numbers.

### Shape and unusual observations

| group | min | max | beyond 1.5 IQR | Shapiro–Wilk |
|---|---|---|---|---|
| modified | 68.12 h | 180.77 h | 2 (low) | $W = 0.970$, $p = 0.247$ |
| standard | 72.93 h | 151.87 h | 1 (low) | $W = 0.977$, $p = 0.523$ |

- Both histograms are **single-peaked** with a somewhat longer **lower tail**.
- QQ-plots: points follow the line in the middle; the lowest few bend below it.
- Shapiro–Wilk (supplementary): no clear evidence against normality.
- **Outliers:** 2 low modified specimens (68.12 and 76.48 h), 1 low standard specimen. Not extreme enough to dominate the means.
- **Sample size helps:** with 48 and 44 specimens, the CLT makes each sample **mean** close to normal even if individual durabilities are mildly skewed. The t procedure is about means, so this is what matters.

**Do not delete outliers** just because they are low. Remove a specimen only with a documented cause (e.g. a defective specimen).

### What the plots cannot establish

- that specimens are **independent** (within or between groups),
- that they **represent** future production of each process,
- that the difference is **caused** by the process (that needs random assignment),
- that durability was **measured the same way** in both groups,
- that the population is **exactly** normal (they only show no clear departure).

Brooks 8.2: "Large samples improve the normal approximation for the sample means; they do not repair dependence, selection bias, confounding, or incompatible measurements."

---

## 6. 2d: zero, the 8-hour threshold and the recommendation

```
   0                7.27   8                  15.20               23.13   (hours)
   |-----------------[=====|====================*===================]
   no difference     lower  practical          estimate             upper
                     limit  threshold
```

| comparison | result | meaning |
|---|---|---|
| CI vs. **0** | whole interval above 0 | an increase in mean durability is supported ($p = 0.00026$) |
| estimate vs. **8 h** | 15.20 h, almost twice the threshold | the best guess is a practically important gain |
| CI vs. **8 h** | lower limit 7.27 h is **just below** 8 h | a gain slightly below 8 h is still plausible |

So the data establish **an increase**, but do **not** establish at 95% confidence that the increase is **at least 8 h**. "Significant" and "important" are two different questions (Brooks 7.5): the test answers the first, the interval against the threshold answers the second.

**Recommendation (as in the notebook):**
- Prefer the modified process: the increase is well supported and most plausible values exceed 8 h.
- If switching is costly, run a confirmation study with more specimens to narrow the interval and rule out a gain below 8 h (the SE shrinks like $1/\sqrt n$).
- Investigate the two very low modified specimens and the larger spread (SD 22.19 vs. 15.75 h). A process that is better on average but less consistent may produce more early failures.

**Causation:** whether the *process* causes the gain depends on how specimens were assigned to processes. With random assignment, a causal reading is supported; without it, other differences between the batches could contribute (Brooks 8.1).

---

## 7. Formula sheet

| | |
|---|---|
| Parameter | $\delta = \mu_1 - \mu_2$ (order fixed in advance) |
| Estimate | $\bar x_1 - \bar x_2$ |
| Welch SE | $\sqrt{s_1^2/n_1 + s_2^2/n_2}$ |
| Welch t | $t_{\text{obs}} = \dfrac{(\bar x_1 - \bar x_2) - \Delta_0}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$, usually $\Delta_0 = 0$ |
| Welch–Satterthwaite df | $\nu = \dfrac{(s_1^2/n_1 + s_2^2/n_2)^2}{\frac{(s_1^2/n_1)^2}{n_1-1} + \frac{(s_2^2/n_2)^2}{n_2-1}}$ |
| Welch CI | $(\bar x_1 - \bar x_2) \pm t_{\nu,\,1-\alpha/2}\,\text{SE}$ |
| Pooled (not default) | $s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}$, SE $= s_p\sqrt{1/n_1 + 1/n_2}$, df $= n_1+n_2-2$ |
| SciPy | `ttest_ind(x1, x2, equal_var=False, alternative="two-sided")`; CI: `t.interval(0.95, df=res.df, loc=diff, scale=se)` |

---

## 8. Likely oral-exam questions

1. **How do you decide between independent and paired?** From the design: here each specimen got one process and has no partner, so the samples are independent. The spreadsheet layout does not decide it.
2. **Why Welch and not the pooled t test?** Welch does not assume equal variances, works well when they are equal, and the groups here have SDs 22.19 vs. 15.75 h.
3. **Why not run a variance test first?** It adds a data-dependent choice that distorts error rates, and Welch is fine either way.
4. **Why is the df 84.84 and not an integer?** Welch–Satterthwaite approximates the null distribution; $\nu$ depends on the two variance terms and lies between 43 and 90.
5. **Why do the variances add for a difference?** For independent samples $\operatorname{Var}(\bar X_1 - \bar X_2) = \sigma_1^2/n_1 + \sigma_2^2/n_2$; there is no covariance term.
6. **What does the interval [7.27, 23.13] h tell you that $p = 0.00026$ does not?** The size of the effect and its uncertainty, which you need for the 8-hour threshold.
7. **Is the increase practically important?** Probably (estimate 15.20 h), but not established: the lower limit 7.27 h is below 8 h.
8. **What can the plots not tell you?** Independence, representativeness, causation, comparable measurement, or exact normality.
9. **Why is a mild skew acceptable here?** The test concerns means; with 48 and 44 specimens the CLT makes the sample means approximately normal.
10. **Why not test each process against a target and compare the two p-values?** A difference must be tested directly (Brooks 8.5); one significant and one non-significant result does not show the groups differ.
11. **Can you say the modified process *causes* longer durability?** Only if specimens were randomly assigned to the processes; otherwise it is an association.
