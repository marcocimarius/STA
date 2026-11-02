# Part 4: Comparing two independent proportions (risk difference and two-proportion z test)

Sources: Session 8 notes, Tutorial 8, Brooks Chapter 8 (8.1, 8.4, 8.5), Brooks Chapter 7.4 (score test, null SE).

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [4a: unit, outcome, populations, assumptions, hypotheses](#3-4a-unit-outcome-populations-assumptions-hypotheses)
4. [4b: proportions, risk difference and the interval](#4-4b-proportions-risk-difference-and-the-interval)
5. [4c: the two-proportion z test](#5-4c-the-two-proportion-z-test)
6. [4d: random sampling, random assignment, causation](#6-4d-random-sampling-random-assignment-causation)
7. [Formula sheet](#7-formula-sheet)
8. [Likely oral-exam questions](#8-likely-oral-exam-questions)

---

## 1. The situation in plain words

Two software configurations, A and B, handled **separate** requests. Each request either met the service-level agreement (SLA) or **failed** it:

| configuration | SLA failures | requests |
|---|---|---|
| A | 38 | 300 |
| B | 22 | 320 |

**Question:** do the two configurations have different failure probabilities, and how big is the difference?

The parameter is the **risk difference** $p_A - p_B$: how many more failures (per 100 requests) A has than B.

**The link to earlier parts:**
- Part 1 tested **one** proportion against a fixed 5%.
- Part 2 compared **two independent means**.
- Part 4 compares **two independent proportions**: Part 2's design with Part 1's binary outcome.

There is no data file; the counts in the text are all we need, because a binary outcome is fully summarised by "how many failures out of how many".

---

## 2. Vocabulary you need first

| Term | Meaning in plain words |
|---|---|
| **Binary outcome** | Each request is either a failure (1) or not (0). |
| **$p_A$, $p_B$** | True SLA-failure probabilities of the two configurations. |
| **$\hat p_A$, $\hat p_B$** | Sample proportions: failures / requests. |
| **Risk difference** | $p_A - p_B$, an **absolute** difference, reported in **percentage points**. |
| **Percentage points (pp)** | The unit of a difference between two percentages: 12.67% − 6.88% = 5.79 **pp** (not "5.79%"). |
| **Separate (unpooled) SE** | SE for the **interval**; each group keeps its own $\hat p$. |
| **Pooled SE ($\text{SE}_0$)** | SE for the **test**; uses one common $\hat p$ because $H_0$ says $p_A = p_B$. |
| **Relative risk** | $p_A / p_B$, a ratio. Optional; not the same as an odds ratio (Brooks 8.4). |

---

## 3. 4a: unit, outcome, populations, assumptions, hypotheses

| item | here |
|---|---|
| **Observational unit** | one request |
| **Binary outcome** | SLA failure: yes / no |
| **Populations** | requests served under A and under B, under the test conditions |
| **Parameters** | $p_A$, $p_B$: the SLA-failure probabilities |
| **Comparison order** (fixed in advance) | $p_A - p_B$, so positive = more failures under A |
| **Hypotheses** (two-sided) | $H_0: p_A = p_B$ vs. $H_1: p_A \neq p_B$, $\alpha = 0.05$ |

**Assumptions** (Brooks 8.4, "Conditions and the boundary of the method"):

1. **Independence within and between groups.** Separate requests, independently assigned configurations. If the *same* requests were run on both, the outcomes would be **paired** binary data, and this method would be wrong.
2. **One constant failure probability per configuration** (no drift over the test period).
3. **Enough events and non-events in each group** for the normal approximation: A has 38 failures / 262 non-failures, B has 22 / 298. All are at least 10, so the large-sample method is reasonable.

---

## 4. 4b: proportions, risk difference and the interval

### The numbers

| step | formula | value |
|---|---|---|
| $\hat p_A$ | 38/300 | **0.1267** (12.67%) |
| $\hat p_B$ | 22/320 | **0.0688** (6.88%) |
| risk difference | $\hat p_A - \hat p_B$ | **0.0579 = 5.79 pp** |
| separate SE | $\sqrt{\dfrac{\hat p_A(1-\hat p_A)}{300} + \dfrac{\hat p_B(1-\hat p_B)}{320}}$ | 0.02385 |
| critical value | $z_{0.975}$ = `norm.ppf(0.975)` | 1.960 |
| 95% CI | $0.0579 \pm 1.960 \times 0.02385$ | **[0.0112, 0.1047] = [1.12, 10.47] pp** |

**In words:** A fails on about 5.8 more requests per 100 than B. The true difference is plausibly anywhere from about 1 to 10.5 more failures per 100 requests.

### Why "separate" variances?

The interval estimates $p_A - p_B$ **without** assuming they are equal, so each group's variance is estimated with its **own** $\hat p$ (Brooks 8.4). It is the same structure as Welch in Part 2: independent groups, so the variances add.

$$\operatorname{Var}(\hat p_A - \hat p_B) = \frac{p_A(1-p_A)}{n_A} + \frac{p_B(1-p_B)}{n_B}.$$

### Why z and not t?

For a proportion, the variance $p(1-p)$ is a function of $p$ itself; there is no separate $\sigma$ to estimate with $s$. So there are no degrees of freedom and the large-sample reference is the standard normal.

### Why report in percentage points?

The difference of two percentages is an **absolute** change. "5.79 pp" means 12.67% vs. 6.88%. Saying "5.79% more" would be ambiguous: it could be read as a relative change (A's rate 5.79% higher than B's), which is something completely different. (The relative risk would be $0.1267/0.0688 \approx 1.84$: A fails about 1.8 times as often.)

---

## 5. 4c: the two-proportion z test

### The pooled standard error

The test is computed **assuming $H_0$ is true**, i.e. both configurations share one failure probability. The best estimate of that common $p$ pools all the data:

| step | formula | value |
|---|---|---|
| pooled proportion | $\hat p = \dfrac{38 + 22}{300 + 320}$ | 0.0968 |
| null SE | $\text{SE}_0 = \sqrt{\hat p(1-\hat p)\left(\tfrac{1}{300} + \tfrac{1}{320}\right)}$ | 0.02376 |
| test statistic | $z = 0.0579 / 0.02376$ | **2.438** |
| two-sided p-value | $2\,P(Z \ge 2.438)$ = `2*norm.sf(abs(z))` | **0.0148** |

### The rule to remember (exam favourite)

Session 8 notes (page 6): "The test assumes $H_0$ is true → pool. The interval does not → separate."

| | interval (4b) | test (4c) |
|---|---|---|
| assumes $p_A = p_B$? | no | yes (that is $H_0$) |
| SE | separate: 0.02385 | pooled: 0.02376 |
| reference | $\pm z_{0.975}$ around $\hat p_A - \hat p_B$ | $N(0,1)$ under $H_0$ |

Here the two SEs are almost equal because the groups have similar sizes, but they are **different quantities** and must not be swapped. It is the same idea as Part 1's score test, which uses $p_0$ (not $\hat p$) in the null SE (Brooks 7.4).

Because of this, the interval and the test are **not exact duals** of each other: they use different SEs, so near the boundary they could disagree. Here they agree: the CI excludes 0 and $p < 0.05$.

### Decision and conclusion

$z = 2.438$, $p = 0.0148 < 0.05$ → **reject $H_0$**.

The data provide evidence that the SLA-failure probabilities differ. A had 12.67% failures and B 6.88%: A is estimated to fail **5.79 pp more often**, with plausible differences from **1.12 to 10.47 pp** (95% CI from 4b).

Do not test A and B separately against some target and compare the two decisions. The difference must be tested **directly** (Brooks 8.5; Tutorial 8 "common mistakes").

---

## 6. 4d: random sampling, random assignment, causation

Two kinds of randomness answer two **different** questions (Brooks 8.1). One does not imply the other.

| randomness | what it does | supports |
|---|---|---|
| **Random sampling** of requests from the target population (e.g. production traffic) | the tested requests represent that population | **generalisation**: the estimated rates and difference describe that population, not just the tested requests |
| **Random assignment** of requests to A or B | by chance, both configurations get comparable requests | **causal comparison**: a difference can be attributed to the configuration rather than to pre-existing differences |

```
                   random assignment?
                     no                 yes
 random      no   association, only    causal, but only for
 sampling?        for these requests   these requests
            yes   association, for     causal, and for the
                  the population       population
```

### Why significance alone is not enough for a causal claim

- The p-value (0.0148) only says the observed difference would be **unusual if $p_A = p_B$** under the model. It says nothing about **why** the groups differ.
- **Without random assignment**, A might have received heavier requests or busier time periods. That would raise its failure rate regardless of the configuration (confounding).
- **Without random sampling**, the result applies only to requests like those tested.
- **Even with both**, the claim is limited to the tested conditions (traffic type, load, period) and to an effect somewhere between 1.12 and 10.47 pp. It is not an unrestricted claim about every production setting.

"Independently assigned" in the task description supports independence; it does not by itself say the assignment was **random**. That is why the notebook makes the causal claim conditional on random assignment.

---

## 7. Formula sheet

| | |
|---|---|
| Sample proportions | $\hat p_j = x_j / n_j$ |
| Risk difference | $\hat p_A - \hat p_B$ (in pp: × 100) |
| Separate SE (for the CI) | $\sqrt{\hat p_A(1-\hat p_A)/n_A + \hat p_B(1-\hat p_B)/n_B}$ |
| 95% CI | $(\hat p_A - \hat p_B) \pm z_{0.975}\,\text{SE}$, $z_{0.975}$ = `norm.ppf(0.975)` = 1.960 |
| Pooled proportion (for the test) | $\hat p = (x_A + x_B)/(n_A + n_B)$ |
| Null SE | $\text{SE}_0 = \sqrt{\hat p(1-\hat p)(1/n_A + 1/n_B)}$ |
| z statistic | $z = (\hat p_A - \hat p_B)/\text{SE}_0$ |
| Two-sided p-value | `2 * norm.sf(abs(z))` |
| Relative risk / odds ratio | $p_A/p_B$; $\dfrac{p_A/(1-p_A)}{p_B/(1-p_B)}$ (not interchangeable) |
| Large-sample check | enough events and non-events in each group (here 38/262 and 22/298) |

---

## 8. Likely oral-exam questions

1. **What is the observational unit and the outcome?** One request; SLA failure yes/no.
2. **What is a risk difference and its unit?** $p_A - p_B$, an absolute difference in percentage points: 5.79 pp here.
3. **Why does the interval use separate variances but the test a pooled one?** The test is built under $H_0: p_A = p_B$, so one common $p$ is estimated; the interval does not assume equality.
4. **What are the two SEs here?** Separate 0.02385 (interval), pooled 0.02376 (test). Close, but not interchangeable.
5. **Why z and not t?** The variance of a proportion is determined by $p$; there is no separately estimated $\sigma$ and no df.
6. **When is the normal approximation OK?** Enough events and non-events in each group (38/262 and 22/298 here); and always independent observations.
7. **What changes if the same requests were run on both configurations?** The outcomes would be paired binary data; the independent two-proportion method would be wrong.
8. **Interpret $p = 0.0148$.** If $p_A = p_B$ and the model holds, a difference at least this extreme would occur with probability 0.0148. Not the probability that $H_0$ is true.
9. **What does random sampling give you? Random assignment?** Generalisation to a population; causal attribution to the configuration. Neither implies the other.
10. **Why is "significant" not enough for "A causes more failures"?** Without random assignment, request mix or load could explain the difference; and the claim only covers the tested conditions.
11. **Risk difference vs. relative risk vs. odds ratio?** Absolute difference (5.79 pp) vs. ratio $p_A/p_B$ (about 1.84) vs. ratio of odds; an odds ratio must not be read as a relative risk.
