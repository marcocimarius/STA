# Part 3: Estimating a false-rejection proportion (confidence interval for a proportion)

Sources: Session 6 notes, Session 6 demo notebook (Code 4), Tutorial 6, Brooks Chapter 6.4.

**Read Part 2's doc first.** Part 3 uses the same recipe (estimate ± critical value × SE), just for a **proportion** instead of a mean.

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [3a: the proportion is just a mean](#2-3a-the-proportion-is-just-a-mean)
3. [3b: the Wilson interval](#3-3b-the-wilson-interval)
4. [3c: the Wald interval, and why Wilson wins](#4-3c-the-wald-interval-and-why-wilson-wins)
5. [3d: 90%, 95%, 99%](#5-3d-90-95-99)
6. [3e: how many attempts would we need?](#6-3e-how-many-attempts-would-we-need)
7. [Part 2 vs. Part 3 side by side](#7-part-2-vs-part-3-side-by-side)
8. [Formula sheet](#8-formula-sheet)
9. [Likely oral-exam questions](#9-likely-oral-exam-questions)

---

## 1. The situation in plain words

A login system (fingerprint, face ID, password check…) sometimes **wrongly rejects a legitimate user**: a **false rejection**. The company staged **240 real login attempts** by legitimate users and recorded each one:

- `false_reject = 1`: the system wrongly rejected the user,
- `false_reject = 0`: the user got in (correct).

**Question:** what is the **probability $p$** that a legitimate login is wrongly rejected? Again we can't test every login ever, so we estimate $p$ from 240 attempts and say how sure we are.

- **Population:** all legitimate login attempts under the same test conditions (same system, same setup).
- **Parameter:** $p$, the false-rejection probability under those conditions. Fixed but unknown.
- **Estimate:** $\hat p$ ("p-hat"), the share of rejections in our sample.

---

## 2. 3a: the proportion is just a mean

| | value |
|---|---|
| $n$ | 240 attempts |
| $x$ | 20 false rejections |
| $\hat p = x/n$ | 20/240 = **0.0833** (8.3%) |

### Why $\hat p$ is a sample mean

The column is just 0s and 1s. Take the average:

$$\frac{0 + 0 + 0 + 1 + 0 + \dots}{240} = \frac{\text{how many 1s}}{240} = \frac{20}{240} = 0.0833 = \hat p$$

Adding up 0/1 values *counts* the 1s, so **the mean of a 0/1 column = the proportion of 1s**. The code shows this: `y.mean()` gives exactly 0.0833.

**Why that matters:** everything from Part 1 about sample means applies to $\hat p$:

| Part 1 (mean) | Part 3 (proportion) |
|---|---|
| $E[\bar X] = \mu$ | $E[\hat p] = p$ (unbiased) |
| $\operatorname{SE} = \sigma/\sqrt n$ | $\operatorname{SE} = \sqrt{p(1-p)/n}$ |
| CLT: $\bar X$ ≈ normal | CLT: $\hat p$ ≈ normal for large $n$ |

Where does $\sqrt{p(1-p)}$ come from? It's the **standard deviation of a single 0/1 value** (a Bernoulli variable, from Assignment 2): variance $= p(1-p)$. So $\sigma = \sqrt{p(1-p)}$, and $\sigma/\sqrt n$ becomes $\sqrt{p(1-p)/n}$.

---

## 3. 3b: the Wilson interval

```python
proportion_confint(x_rej, n_att, alpha=0.05, method="wilson")
```

- `alpha = 0.05` means 5% is left outside, so this is a **95%** interval.
- `method="wilson"` is the course's default for proportions.

**Result: [0.0546, 0.1252]**, i.e. between **5.5% and 12.5%**.

**Interpretation:** "We estimate that between about 5.5% and 12.5% of legitimate login attempts are falsely rejected under the test conditions." The 95% means the same as in Part 2: if we repeated the 240-attempt test many times, about 95% of the Wilson intervals would contain the true $p$.

### Notice: it's not symmetric

$\hat p = 0.083$, but the interval goes **0.029 below** and **0.042 above** it. Why? A proportion **can't go below 0**, and we're quite close to 0. There's "more room" for $p$ to be higher than lower, so the uncertainty is lopsided. Wilson captures that; Wald (next) doesn't.

You don't need to compute Wilson by hand (statsmodels does it), but here is the formula from the Session 6 notes:

$$\frac{\hat p + \frac{z^2}{2n} \pm z\sqrt{\frac{\hat p(1-\hat p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

The extra $z^2$ terms gently pull the centre towards 0.5 and widen the interval when $n$ is small.

---

## 4. 3c: the Wald interval, and why Wilson wins

### Wald = the simple recipe

The **Wald interval** applies Part 2's recipe directly:

$$\hat p \pm z \cdot \sqrt{\frac{\hat p(1-\hat p)}{n}}$$

Step by step:

| step | value |
|---|---|
| SE = $\sqrt{0.0833 \times 0.9167 / 240}$ | 0.0178 |
| critical value $z_{0.975}$ | 1.960 (normal, not t, because there's no separately estimated σ for a proportion) |
| margin = 1.960 × 0.0178 | 0.0350 |
| interval = 0.0833 ± 0.0350 | **[0.0484, 0.1183]** |

### Comparison

| | lower | upper | centre | width |
|---|---|---|---|---|
| Wald | 0.0484 | 0.1183 | 0.0833 | 0.0699 |
| Wilson | 0.0546 | 0.1252 | 0.0899 | 0.0706 |

- Similar widths.
- Wald is **symmetric** around $\hat p$ (centre = 0.0833 exactly).
- Wilson is **shifted up** (centre 0.0899) and stretches further on the high side.
- Here they don't differ much, because we have enough rejections (20) and acceptances (220); a rule of thumb is that both should be at least 10.

### Why Wilson is the preferred default

Wald pretends $\hat p$ is exactly bell-shaped around itself and plugs $\hat p$ into the SE. That breaks when $p$ is near 0 or 1, or $n$ is small:

**Example 1** (Tutorial 6): 2 out of 20.
- Wald gives [−0.031, 0.231]. A **negative probability** is impossible!
- Wilson gives [0.028, 0.301], which stays inside [0, 1].

**Example 2** (Session 6 demo): 0 failures out of 20.
- $\hat p = 0$, so Wald's SE $= \sqrt{0 \times 1 / 20} = 0$ and Wald gives **[0, 0]**: "we're 100% sure the failure rate is exactly 0", which is nonsense after only 20 tests.
- Wilson gives roughly [0, 0.16]: still honest uncertainty.

On top of this, Wald's real coverage is often **below** the claimed 95% (it understates uncertainty). Wilson **always stays in [0, 1]**, handles $x = 0$, and its coverage is closer to the stated level. So: **report Wilson**, and use Wald only to understand the basic idea.

---

## 5. 3d: 90%, 95%, 99%

| confidence | Wilson interval | width |
|---|---|---|
| 90% | [0.0584, 0.1175] | 0.059 |
| 95% | [0.0546, 0.1252] | 0.071 |
| 99% | [0.0478, 0.1412] | 0.093 |

The code changes `alpha = 1 − level` (0.10, 0.05, 0.01). It's the same trade-off as Part 2d: more confidence gives a wider interval. Note the **upper** limit moves out faster than the lower one: the lopsidedness again, because we're close to 0.

---

## 6. 3e: how many attempts would we need?

**Goal:** a 95% interval with margin of error at most **0.02** (2 percentage points). Ours currently is about 0.035.

Margin $E = z\sqrt{p(1-p)/n}$. Solve for $n$:

$$n \ge \frac{z^2 \cdot p(1-p)}{E^2}$$

The problem: the formula needs $p$, the very thing we're trying to estimate! Two options:

| planning value | $p(1-p)$ | calculation | $n$ |
|---|---|---|---|
| **$p = 0.5$** (worst case) | 0.25 | $1.96^2 \times 0.25 / 0.02^2 = 2400.9$ | **2401** |
| **$\hat p = 0.0833$** (our estimate) | 0.0764 | $1.96^2 \times 0.0764 / 0.02^2 = 733.6$ | **734** |

### Why such a big difference?

$p(1-p)$ measures how "uncertain" a 0/1 variable is, and it peaks at $p = 0.5$:

```
p(1−p)
0.25 |          ●            ← maximum at p = 0.5
     |      ●       ●
     |   ●             ●
0.08 | ●   ← p = 0.083       ●
     +----------------------------  p
     0         0.5          1
```

- **$p = 0.5$ is the safe choice:** it's the worst case, so 2401 attempts guarantees a margin ≤ 0.02 **whatever** the true $p$ is. But it's expensive.
- **$\hat p$ is the cheap choice:** about 3.3× fewer attempts (734). But it **relies on $\hat p$ being close to the truth**. Our own Wilson interval says $p$ could be as high as 0.125. If it is, we'd actually need about **1052** attempts, and 734 would give a margin bigger than 0.02.

**Always round up** (2400.9 → 2401, 733.6 → 734); rounding down would miss the target slightly.

---

## 7. Part 2 vs. Part 3 side by side

| | Part 2 (mean) | Part 3 (proportion) |
|---|---|---|
| Data | numbers (errors in °C) | 0/1 (rejected or not) |
| Parameter | $\mu$ | $p$ |
| Estimate | $\bar x = 0.188$ | $\hat p = 0.083$ |
| SE | $s/\sqrt n$ | $\sqrt{\hat p(1-\hat p)/n}$ |
| Default interval | **t interval** | **Wilson interval** |
| "Teaching only" interval | z interval (only if σ known) | Wald interval |
| Planning formula | $n \ge (z s / E)^2$ | $n \ge z^2 p(1-p)/E^2$ |

---

## 8. Formula sheet

| | |
|---|---|
| Sample proportion | $\hat p = x/n$ = mean of the 0/1 column |
| SE | $\sqrt{\hat p(1-\hat p)/n}$ |
| Wald | $\hat p \pm z_{1-\alpha/2}\sqrt{\hat p(1-\hat p)/n}$ |
| Wilson (statsmodels) | `proportion_confint(x, n, alpha=1-level, method="wilson")` |
| Sample size | $n \ge z^2 p(1-p)/E^2$; $p = 0.5$ is conservative; round **up** |
| Rule of thumb for Wald | $n\hat p \ge 10$ and $n(1-\hat p) \ge 10$ (a diagnostic, not a guarantee) |

---

## 9. Likely oral-exam questions

1. **Why is a proportion a mean?** It's the mean of a 0/1 variable: summing 0s and 1s counts the 1s.
2. **What is the SE of $\hat p$?** $\sqrt{p(1-p)/n}$, because one 0/1 value has variance $p(1-p)$.
3. **Wilson vs. Wald?** Wald = estimate ± z·SE, which is simple but can go below 0, gives [0, 0] when $x = 0$, and under-covers. Wilson stays in [0, 1], is asymmetric near 0/1, and has better coverage. The course default is Wilson.
4. **Why is the Wilson interval not symmetric around $\hat p$?** $p$ is bounded by 0 and 1; near 0 there's more room above than below.
5. **Why z and not t for a proportion?** There's no separately estimated σ; the SE comes directly from $\hat p$.
6. **Why use $p = 0.5$ in planning?** $p(1-p)$ is largest there, so it's the worst case and guarantees the target margin.
7. **What's the risk of planning with $\hat p$?** If the true $p$ is further from 0 (closer to 0.5) than $\hat p$, the sample will be too small.
8. **State the population and parameter.** Population: all legitimate logins under the test conditions. Parameter: $p$, the false-rejection probability.
