# Part 3: Paired building-energy measurements (paired t procedure)

Sources: Session 8 notes, Tutorial 8, Brooks Chapter 8 (8.1, 8.3, 8.5), Brooks Chapter 7.3 (normality of the analysed quantity).

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [3a: genuine pairs and the difference column](#3-3a-genuine-pairs-and-the-difference-column)
4. [3b: plots and diagnosing the differences](#4-3b-plots-and-diagnosing-the-differences)
5. [3c: the paired t test and interval](#5-3c-the-paired-t-test-and-interval)
6. [3d: why pairing matters, and the recommendation](#6-3d-why-pairing-matters-and-the-recommendation)
7. [Formula sheet](#7-formula-sheet)
8. [Likely oral-exam questions](#8-likely-oral-exam-questions)

---

## 1. The situation in plain words

36 buildings got a new **control system** (a retrofit). For **each building**, daily energy use was measured **before** and **after** the retrofit, in kWh/day.

**Question:** does the retrofit reduce energy use, and by how much?

For each building we compute

$$D = \text{before} - \text{after},$$

so **positive $D$ = the building saves energy**. The parameter is $\mu_D$, the population mean of these differences: the average saving per building.

**The link to Parts 1 and 2:** Part 2 also had two columns of numbers, but they came from *different* specimens. Here both numbers in a row come from the **same building**. That changes everything: we turn the two columns into **one column of differences** and run the **one-sample t test from Part 1** on it.

---

## 2. Vocabulary you need first

| Term | Meaning in plain words |
|---|---|
| **Observational unit** | The thing measured. Here one **building** (measured twice), not one measurement. |
| **Paired observations** (Def. 8.2) | Each observation in one condition has a specific, meaningful partner in the other. |
| **Difference $D_i$** | The within-pair change for building $i$: before − after. |
| **$\mu_D$** | Population mean difference: the mean saving per building for buildings like these. |
| **$\bar d$, $s_D$** | Sample mean and SD of the 36 differences. |
| **$n$** | The number of **pairs** (36), not the number of measurements (72). |
| **Correlation $\rho$ / $r$** | How strongly before and after values move together across buildings. |

---

## 3. 3a: genuine pairs and the difference column

### Why the rows are genuine pairs

- Both values in a row come from the **same building**. Each "before" has one specific, meaningful "after" partner.
- A building's size, use and insulation affect **both** measurements. A big office uses a lot before *and* after.
- The pairing comes from the **design** (same 36 buildings measured twice), not from the row order. Shuffling the "after" column would destroy real information; in Part 2, sorting would have created fake information.

### Setting up

- **Population and parameter:** buildings of this type receiving the retrofit; $\mu_D$ in kWh/day.
- **Comparison order (fixed in advance):** before − after, so positive = reduction (the same choice as Brooks Example 8.3).

### The difference column

```python
energy["D"] = energy["before_kwh_day"] - energy["after_kwh_day"]
```

| quantity | formula | value |
|---|---|---|
| number of pairs | $n$ | 36 |
| mean difference | $\bar d$ | **4.823 kWh/day** |
| SD of differences | $s_D$ (`d.std(ddof=1)`) | **4.504 kWh/day** |
| standard error | $s_D/\sqrt n = 4.504/6$ | **0.751 kWh/day** |

**SD vs. SE again:** $s_D = 4.50$ says individual buildings' savings vary a lot (some even use *more* afterwards). SE = 0.75 says how much the *average* saving would change if we repeated the study with 36 other buildings.

---

## 4. 3b: plots and diagnosing the differences

### The three plots

1. **Paired-values plot:** one line per building from "before" to "after". Most lines slope **down** (less energy after). Buildings with high use before tend to have high use after as well. That shared building level is what pairing removes.
2. **Histogram of $D$:** fairly flat, roughly symmetric around $\bar d = 4.82$, range −2.90 to 13.17 kWh/day. Most of the mass is to the right of 0.
3. **QQ-plot of $D$:** points close to the line, no curvature, no isolated extreme points.

Numerical checks: **0 values beyond 1.5 IQR**, Shapiro–Wilk on the differences $W = 0.969$, $p = 0.403$ (no clear evidence against normality; supplementary only).

### Why diagnose D, not the two raw columns?

The paired t test **is** a one-sample t test on $D$. Its assumptions (independent, approximately normal) concern **the differences only** (Theorem 8.2; Brooks 7.3: "A paired t procedure concerns the paired differences, not the two measurements separately").

```
   before values: spread over many building sizes   → may look skewed/bimodal
   after  values: same building-size spread          → may look skewed/bimodal
   D = before − after: building size cancels out     → this is what must be ~normal
```

The raw columns mostly show **how different the buildings are** from each other, which is irrelevant to the test. They could look non-normal while $D$ is perfectly fine, or the other way round.

**Independence** still cannot be seen in any plot. It relies on the 36 buildings being separate units, e.g. not sharing one central control system.

With 36 pairs, no outliers and a straight QQ-plot, the paired t procedure is reasonable.

---

## 5. 3c: the paired t test and interval

### Hypotheses

- $H_0: \mu_D = 0$ kWh/day (no change on average)
- $H_1: \mu_D \neq 0$ kWh/day (two-sided)
- $\alpha = 0.05$, df $= n - 1 = 35$

### Step by step (Theorem 8.2)

| step | formula | value |
|---|---|---|
| test statistic | $t = (\bar d - 0)/(s_D/\sqrt n) = 4.823/0.751$ | **6.425** |
| degrees of freedom | $n - 1$ (pairs!) | **35** |
| two-sided p-value | $2\,P(T_{35} \ge 6.425)$ | **$2.1 \times 10^{-7}$** |
| critical value | $t_{35,\,0.975}$ | 2.030 |
| 95% CI | $4.823 \pm 2.030 \times 0.751$ | **[3.30, 6.35] kWh/day** |

### The code

```python
res_p = ttest_rel(energy["before_kwh_day"], energy["after_kwh_day"], alternative="two-sided")
ci_d  = t.interval(0.95, df=n_d - 1, loc=d_bar, scale=se_d)
```

- `ttest_rel(before, after)` computes before − after row by row and runs a one-sample t test on it. It is identical to `ttest_1samp(d, popmean=0)` (Tutorial 8: "in another costume").
- The **argument order** sets the sign: `ttest_rel(after, before)` would give $t = -6.425$ and the same p-value.

### Decision

$p = 2.1 \times 10^{-7} < 0.05$ → **reject $H_0$**. The interval [3.30, 6.35] excludes 0, consistent with the test (duality). The data provide evidence that mean energy use is **lower after** the retrofit.

---

## 6. 3d: why pairing matters, and the recommendation

### What an independent-samples test would throw away

| | SD (kWh/day) |
|---|---|
| before (between buildings) | 6.63 |
| after (between buildings) | 7.35 |
| **differences** | **4.50** |

Correlation between before and after: **$r = 0.797$** (strong).

Why is the SD of $D$ so much smaller? Brooks 8.3 / Session 8 notes (page 5):

$$\operatorname{Var}(D) = \sigma_X^2 + \sigma_Y^2 - 2\rho\,\sigma_X\sigma_Y.$$

With a strong **positive** correlation, the last term subtracts most of the building-to-building variation. Each building acts as **its own control**.

| analysis | standard error |
|---|---|
| ignoring the pairing (independent, $\sqrt{s_b^2/36 + s_a^2/36}$) | 1.651 kWh/day |
| paired ($s_D/\sqrt{36}$) | **0.751 kWh/day** |

The independent SE is **more than twice** as large. An independent test would therefore give a much wider interval and less power, for exactly the same data. It would also be **wrong**, not just inefficient: it treats the 72 measurements as independent, while the before and after values of one building are clearly linked (Tutorial 8: do not run `ttest_ind` on paired rows).

The reverse mistake also exists: pairing unrelated observations (as sorting would in Part 2) invents a dependence the design does not contain (Brooks 8.3).

### Interpretation in kWh/day

- **Estimate:** the retrofit reduces mean energy use by **4.82 kWh/day per building**.
- **Interval:** mean reductions from **3.30 to 6.35 kWh/day** are compatible with the data (95% CI). Even the smallest plausible value is a clear saving.

### Practical recommendation

- Recommend the retrofit for similar buildings **if** a saving of roughly 3–6 kWh/day per building justifies its cost. The statistics give the size; the cost decision is an engineering/economic judgement.
- **Limitation:** this is a before–after design **without a comparison group**. Weather, occupancy or usage may have differed between the two periods, and part of the reduction could come from that. Pairing removes building-to-building differences, but **not** time-period differences. A causal claim would need e.g. a control group of buildings without the retrofit measured over the same periods.

---

## 7. Formula sheet

| | |
|---|---|
| Differences | $D_i = X_i - Y_i$ (order fixed in advance) |
| Parameter | $\mu_D = E[D]$ |
| Summary | $\bar d$, $s_D$, SE $= s_D/\sqrt n$ with $n$ = number of pairs |
| Paired t | $t_{\text{obs}} = (\bar d - \Delta_0)/(s_D/\sqrt n)$, df $= n-1$, usually $\Delta_0 = 0$ |
| Paired CI | $\bar d \pm t_{n-1,\,1-\alpha/2}\,s_D/\sqrt n$ |
| Why pairing helps | $\operatorname{Var}(D) = \sigma_X^2 + \sigma_Y^2 - 2\rho\,\sigma_X\sigma_Y$ |
| SciPy | `ttest_rel(x, y, alternative="two-sided")` ≡ `ttest_1samp(x - y, popmean=0)`; CI: `t.interval(0.95, n-1, loc=d_bar, scale=se_d)` |

---

## 8. Likely oral-exam questions

1. **What is the observational unit?** One building, measured twice. So $n = 36$ pairs, not 72 observations.
2. **Why are these genuine pairs?** Both values come from the same building; the partner is specific and meaningful, set by the design.
3. **Why is a paired test a one-sample test?** We reduce each pair to one difference and test whether the mean difference is 0: exactly Part 1's t test on $D$.
4. **Which data must be approximately normal?** The differences, not the before and after columns separately.
5. **Why does pairing give a smaller SE?** The strong positive correlation ($r = 0.797$) removes building-to-building variation: $\operatorname{Var}(D) = \sigma_X^2 + \sigma_Y^2 - 2\rho\sigma_X\sigma_Y$. SE 0.751 vs. 1.651 kWh/day.
6. **What would go wrong with `ttest_ind` here?** It ignores the pairing: wrong independence assumption, SE more than twice as large, wider interval, less power.
7. **What are df and why?** $n - 1 = 35$, because the analysis is a one-sample t on 36 differences.
8. **Interpret the result in units.** Mean saving 4.82 kWh/day per building, plausibly 3.30 to 6.35 kWh/day.
9. **Can you conclude the retrofit *caused* the saving?** Not fully: without a comparison group, changes in weather or use between the periods could contribute.
10. **What does the argument order in `ttest_rel` do?** It sets the sign of $D$; swapping gives $t = -6.425$ with the same p-value and a mirrored interval.
