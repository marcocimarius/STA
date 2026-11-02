# Part 1: One-sample decisions (one-sample t test and exact binomial test)

Sources: Session 7 notes, Session 7 demo notebook (Codes 1–4), Tutorial 7, Brooks Chapter 7.

**The link to Assignment 3:** the two data files are the same as in Assignment 3. There we *estimated* the mean sensor error and the false-rejection probability with confidence intervals. Now we *test* a specific claim about each one. Same data, same estimates, a new question.

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [1a: the one-sample t test for the mean sensor error](#3-1a-the-one-sample-t-test-for-the-mean-sensor-error)
4. [1b: reading the p-value correctly](#4-1b-reading-the-p-value-correctly)
5. [1c: duality and practical importance](#5-1c-duality-and-practical-importance)
6. [1d: the one-sided exact binomial test](#6-1d-the-one-sided-exact-binomial-test)
7. [1e: Wilson interval vs. exact test](#7-1e-wilson-interval-vs-exact-test)
8. [1f: Type I and Type II errors](#8-1f-type-i-and-type-ii-errors)
9. [Formula sheet](#9-formula-sheet)
10. [Likely oral-exam questions](#10-likely-oral-exam-questions)

---

## 1. The situation in plain words

Part 1 has **two separate one-sample studies**. In each, one population is compared with a **fixed reference value**:

| study | data | parameter | reference value | question |
|---|---|---|---|---|
| Mean sensor error | 64 sensors, error in °C | $\mu$ = mean calibration error | 0 °C | Is the mean error different from zero (either direction)? |
| False rejections | 240 login attempts, 0/1 | $p$ = false-rejection probability | 5% | Is $p$ *above* the 5% target? |

A **hypothesis test** asks: *if the claim were exactly true, would data like ours be surprising?* A sample never matches the claim exactly, even when the claim is true, because samples vary. The test measures how far off the sample is **in units of its expected random variation** (Brooks 7.2).

The overall method from the Session 7 notes (page 4):

```
1. State H0 and H1        (try to disprove H0)
2. Choose alpha           (before looking at results)
3. Compute the test statistic
4. Reject / fail to reject (p-value or critical value)
5. Conclude in context
```

---

## 2. Vocabulary you need first

| Term | Meaning in plain words |
|---|---|
| **Null hypothesis $H_0$** | The claim we assume true to build the reference distribution, e.g. "$\mu = 0$". Contains the equality. |
| **Alternative $H_1$** | The departures from $H_0$ the study is designed to detect, e.g. "$\mu \neq 0$". |
| **Two-sided / one-sided** | Two-sided: a departure in either direction counts. One-sided: only one direction counts (fixed **before** seeing data). |
| **Test statistic** | (estimate − null value) / SE under $H_0$. "How many standard errors away from the claim?" |
| **Null distribution** | The distribution of the test statistic if $H_0$ is true (here: $t_{63}$, or Binomial(240, 0.05)). |
| **p-value** | Probability, *assuming $H_0$ and the model*, of a statistic at least as extreme as the one observed. |
| **Significance level $\alpha$** | The chosen upper bound on the probability of rejecting a true $H_0$. Here 0.05. |
| **Reject / fail to reject** | $p \le \alpha$ → reject $H_0$. $p > \alpha$ → fail to reject. Never "accept $H_0$". |
| **Type I / Type II error** | Rejecting a true $H_0$ (false positive) / not rejecting a false $H_0$ (false negative). |
| **Power** | $1-\beta$: the probability of rejecting $H_0$ when a specific alternative is true. |

The error table from the Session 7 notes (page 1):

| decision | $H_0$ true | $H_0$ false |
|---|---|---|
| fail to reject | correct (TN), prob. $1-\alpha$ | **Type II error** (FN), prob. $\beta$ |
| reject | **Type I error** (FP), prob. $\alpha$ | correct (TP), prob. $1-\beta$ = power |

**Courtroom analogy** (notes, page 2): $H_0$ = "innocent". "Not guilty" means guilt was not proven; it does **not** prove innocence. Likewise "fail to reject $H_0$" is not "$H_0$ is true".

---

## 3. 1a: the one-sample t test for the mean sensor error

### Setting up before computing

- **Population and parameter:** all sensors of this type; $\mu$ = mean of (sensor reading − reference temperature), in °C.
- **Unit and design:** one sensor; one sample of 64 independently selected sensors.
- **Hypotheses (two-sided, because both "too hot" and "too cold" matter):** $H_0:\mu = 0$ °C vs. $H_1:\mu \neq 0$ °C.
- **Level:** $\alpha = 0.05$.

Why two-sided? The team asks whether the mean error *differs* from zero. Brooks 7.1: the direction must follow the question and be fixed before the data are seen. Picking "$>$" because $\bar x$ happens to be positive would invalidate $\alpha$.

### Why a t test?

$\sigma$ is unknown, so we estimate it with $s$. Theorem 7.2 (Session 7 notes, page 6): if the population is normal and $H_0$ is true,

$$T = \frac{\bar X - \mu_0}{S/\sqrt n} \sim t_{n-1}.$$

This is the same reason as in Assignment 3: estimating $\sigma$ adds uncertainty, so we use $t$ (fatter tails) instead of $z$.

### Step by step

| step | formula | value |
|---|---|---|
| sample mean | $\bar x$ | 0.1883 °C |
| sample SD | $s$ (`x.std(ddof=1)`) | 0.6257 °C |
| standard error | $s/\sqrt n = 0.6257/8$ | 0.0782 °C |
| test statistic | $(\bar x - 0)/\text{SE}$ | **$t = 2.4069$** |
| degrees of freedom | $n-1$ | **63** |
| two-sided p-value | $2\,P(T_{63} \ge 2.4069)$ = `2*t.sf(abs(t_obs), 63)` | **0.0190** |

The notebook computes $t$ by hand and checks it with `ttest_1samp(x, popmean=0, alternative="two-sided")`. Both give $t = 2.4069$, df = 63, $p = 0.01903$. Always set `alternative=` explicitly (Tutorial 7), so the code matches the stated $H_1$.

**In words:** the sample mean is 2.41 standard errors above 0. Under $H_0$ that is unusual, but not extremely so.

### Checking the assumption

The t test needs **independent** sensors (from the design) and an approximately **normal** population of errors (Brooks Table 7.4).

- **Histogram:** single-peaked and roughly symmetric, no extreme values.
- **QQ-plot (`probplot`):** points close to the straight line.
- **Shapiro–Wilk (`shapiro`):** $W = 0.990$, $p = 0.874$, so no evidence against normality.

Shapiro–Wilk is **supplementary** (Tutorial 7, Brooks 7.3): with small $n$ it can miss real departures, and with large $n$ it flags tiny ones. A large Shapiro p-value does not *prove* normality, and no plot or test can show independence.

---

## 4. 1b: reading the p-value correctly

### The correct sentence

> If the population mean error were exactly 0 °C and the assumptions held, a $t$ statistic at least as far from 0 as $|t| = 2.41$ (in either direction) would occur in about **1.9%** of repeated samples of 64 sensors.

```
                 null distribution t(63)
                        _.-'''-._
                      .'         '.
     shaded 0.95% → _/             \_ ← shaded 0.95%
  ______________.--'                 '--.______________
          -2.41            0            +2.41
     two-sided p = 0.0095 + 0.0095 = 0.019
```

Two-sided means **both tails** count: a mean error of −0.188 °C would be just as much evidence against $\mu = 0$ as +0.188 °C.

### What the p-value is NOT (exam favourite)

The p-value is $P(\text{data this extreme} \mid H_0)$, **not** $P(H_0 \mid \text{data})$ (Brooks 7.2, Example 7.2). So all of these are wrong:

- "There is a 1.9% chance that the mean error is zero."
- "There is a 98.1% chance that the sensors are biased."
- "There is a 1.9% chance the result happened by chance."
- "The bias is large / important." (the p-value says nothing about size)

$P(H_0 \mid \text{data})$ would need a Bayesian model with prior probabilities. A frequentist test does not supply it.

### Decision and conclusion

$p = 0.019 < \alpha = 0.05$ → **reject $H_0$**. The data provide evidence that the population mean calibration error differs from 0 °C; the sample mean of +0.188 °C suggests the sensors read slightly **too high** on average.

Equivalent critical-value rule (notes, page 3): reject if $|t| > t_{63,\,0.975} = 1.998$. Here $2.41 > 1.998$, same decision.

---

## 5. 1c: duality and practical importance

### The interval

`t.interval(0.95, df=63, loc=xbar, scale=se)` gives

$$0.1883 \pm 1.998 \times 0.0782 = [0.0320,\ 0.3446]\ ^\circ\text{C}.$$

This is exactly the 95% interval from Assignment 3, Part 2.

### Duality (Theorem 7.3)

For a **two-sided** test and an interval **built from the same method**:

$$\text{reject } H_0:\mu=\mu_0 \text{ at level } \alpha \iff \mu_0 \text{ lies outside the } 100(1-\alpha)\% \text{ interval.}$$

Why? Both use the same $\bar x$, the same SE and the same $t_{63}$ distribution. "$|t| > 1.998$" is the same inequality as "$\mu_0$ is more than $1.998 \times \text{SE}$ away from $\bar x$".

```
 -0.5        0       0.032   0.188    0.345         0.5   (°C)
  |----------|---------[=======*=======]-------------|
  practical  null      95% CI (all plausible means)  practical
  limit      value     0 is outside → reject         limit
```

Here 0 °C is outside → reject, consistent with $p = 0.019$. Every value inside the interval (e.g. 0.1 or 0.3 °C) would *not* be rejected.

### Statistical significance vs. practical importance

The team says an absolute mean error below 0.50 °C is small in practice. The **whole interval** [0.032, 0.345] lies inside $(-0.50, 0.50)$.

| question | answered by | answer |
|---|---|---|
| Is the mean error exactly 0? | test / does CI contain 0? | No, evidence of a shift ($p = 0.019$) |
| Does the shift matter? | CI vs. 0.50 °C limit | No, even the largest plausible value (0.345 °C) is small |

So the result is **statistically significant but not practically important**. Brooks Example 7.10 is almost the same situation (mean 0.12 °C, tolerance ±0.5 °C). The p-value only tells us a shift is *detectable*; the interval and the engineering limit tell us whether its *size* matters.

---

## 6. 1d: the one-sided exact binomial test

### Setting up

- **Population and parameter:** legitimate login attempts under the test conditions; $p$ = probability a legitimate attempt is falsely rejected.
- **Unit and design:** one staged attempt; 240 independent attempts.
- **Hypotheses (one-sided, pre-specified):** $H_0: p \le 0.05$ vs. $H_1: p > 0.05$. The question is only whether the target is **exceeded**, so only the upper tail counts.
- **Level:** $\alpha = 0.05$.

The test is calculated at the boundary $p_0 = 0.05$, the null value "most favourable to the alternative" (Brooks 7.1). If the data are surprising for $p = 0.05$, they are even more surprising for any $p < 0.05$.

### Why exact?

Under $H_0$ and independent attempts with a constant $p$, the count of false rejections is **exactly** binomial (Definition 7.9):

$$X \sim \text{Binomial}(240,\ 0.05), \qquad \text{p-value} = P_{0.05}(X \ge x).$$

No normal approximation is needed. (The large-sample score test would also be possible here, since $np_0 = 12$ and $n(1-p_0) = 228$ are both $\ge 10$, but the assignment asks for the exact test, which is valid at any $n$.)

### Numbers

| step | value |
|---|---|
| $n$, $x$ | 240 attempts, 20 false rejections |
| $\hat p = x/n$ | 20/240 = **0.0833** (8.33%) |
| expected count under $H_0$ | $240 \times 0.05 = 12$ |
| exact p-value $P(X \ge 20 \mid p=0.05)$ | **0.0185** |
| code | `binomtest(20, n=240, p=0.05, alternative="greater")` |

We observed 20 where 12 were expected. **Decision:** $0.0185 < 0.05$ → **reject $H_0$**. **Conclusion:** under these test conditions, the data provide evidence that the false-rejection probability exceeds the 5% target.

**Note on discreteness:** with a discrete count, the actual Type I error probability of an exact test can be *smaller* than $\alpha$ (Definition 7.5), because only certain p-values are attainable.

---

## 7. 1e: Wilson interval vs. exact test

### The interval as plausible values

`proportion_confint(20, 240, alpha=0.05, method="wilson")` gives **[5.46%, 12.52%]** (the same interval as Assignment 3, Part 3). All plausible values are above 5%, so the target is plausibly exceeded by about 0.5 to 7.5 percentage points. This gives the *size* of the problem, which the p-value does not.

### Why this is not the exact dual of the test

Duality (Theorem 7.3) needs two conditions. Both fail here:

| condition for duality | exact test | Wilson interval |
|---|---|---|
| **same method** | binomial probabilities directly | normal approximation of the **score** statistic $(\hat p - p_0)/\sqrt{p_0(1-p_0)/n}$ |
| **same direction** | one-sided, all 5% in upper tail | two-sided, 2.5% in each tail |

The matching pairs (Brooks 7.4, 7.5) are:
- two-sided **score test** ↔ **Wilson** interval,
- **exact binomial test** ↔ an exact (binomial-based) interval.

So for a count near the boundary, the exact test could reject while the Wilson lower limit is still below 5%, or the other way round. Here both point the same way, but that is a coincidence of these data, not a guarantee. Session 7 demo (Code 4): "Do not claim the two methods have identical decision boundaries." That is why the notebook uses Wilson only as an **estimate of plausible values**, not as a second test.

---

## 8. 1f: Type I and Type II errors

The notebook uses the false-rejection study ($H_0: p \le 0.05$, $H_1: p > 0.05$).

| error | what happens | probability | operational consequence |
|---|---|---|---|
| **Type I** (false positive) | conclude "target missed" when $p \le 5\%$ really | at most $\alpha = 0.05$ | unnecessary retuning or delayed release; a more permissive retune might let in unauthorised users |
| **Type II** (false negative) | fail to detect that $p > 5\%$ | $\beta$ | system approved although it locks out too many legitimate users: more help-desk calls, lost working time |

**$\beta$ is not a single number.** It depends on how far the true $p$ is above 5%, on $n$, and on $\alpha$ (Brooks 7.2). A true $p$ of 5.5% is hard to detect with 240 attempts (large $\beta$); a true $p$ of 12% is easy (small $\beta$, high power). Lowering $\alpha$ reduces Type I errors but, with everything else fixed, raises $\beta$.

**Which error could we have made?** We rejected $H_0$ in 1d, so the only possible error is a **Type I** error. A Type II error is only possible after "fail to reject".

---

## 9. Formula sheet

| | |
|---|---|
| General test statistic | (estimate − null value) / SE under $H_0$ |
| One-sample t | $t = (\bar x - \mu_0)/(s/\sqrt n)$, df $= n-1$; `ttest_1samp(x, popmean=mu0, alternative=...)` |
| Two-sided t p-value | $2\,P(T_{n-1} \ge \lvert t\rvert)$ = `2*t.sf(abs(t_obs), n-1)` |
| t interval | $\bar x \pm t_{n-1,\,0.975}\,s/\sqrt n$; `t.interval(0.95, n-1, loc=xbar, scale=se)` |
| Duality (two-sided, same method) | reject $H_0:\theta=\theta_0$ ⇔ $\theta_0$ outside the $100(1-\alpha)\%$ CI |
| Exact binomial test | $X \sim \text{Bin}(n,p_0)$; upper-tail $p = P_{p_0}(X \ge x)$; `binomtest(x, n, p0, alternative="greater")` |
| Score statistic (for comparison) | $z = (\hat p - p_0)/\sqrt{p_0(1-p_0)/n}$; needs $np_0, n(1-p_0) \ge 10$ |
| Wilson interval | `proportion_confint(x, n, alpha=0.05, method="wilson")`; dual of the two-sided score test |
| Decision rule | $p \le \alpha$ → reject; $p > \alpha$ → fail to reject |
| Errors | $P(\text{reject} \mid H_0) \le \alpha$; $P(\text{not reject} \mid H_1) = \beta$; power $= 1-\beta$ |

---

## 10. Likely oral-exam questions

1. **What is a p-value?** The probability, assuming $H_0$ and the model, of a test statistic at least as extreme as observed. For the sensors: 0.019.
2. **Why is the p-value not $P(H_0 \mid \text{data})$?** It conditions on $H_0$, not on the data; reversing the conditional would need a Bayesian prior.
3. **One-sided or two-sided, and who decides?** The engineering question, before seeing the data. Sensor: either direction matters → two-sided. Logins: only exceeding the target matters → one-sided.
4. **Why a t test and not a z test for the sensors?** $\sigma$ is unknown and estimated by $s$; the statistic then follows $t_{63}$ under normality.
5. **What does "fail to reject" mean?** The data are not strong enough evidence against $H_0$; it is not proof of $H_0$ (courtroom: "not guilty" ≠ innocent).
6. **Explain test–interval duality with your numbers.** 0 °C lies outside [0.032, 0.345] °C ⇔ the two-sided t test rejects at 5% ($p = 0.019$).
7. **Significant but not important?** The sensor bias is detectable ($p = 0.019$) but the whole interval is within the ±0.50 °C practical limit.
8. **Why an exact binomial test?** Under $H_0$ the count is exactly Binomial(240, 0.05), so no normal approximation is needed; $P(X \ge 20) = 0.0185$.
9. **Why is the Wilson interval not the dual of the exact test?** Different method (score vs. exact) and different direction (two-sided vs. one-sided). Wilson is dual to the two-sided score test.
10. **Type I vs. Type II error here, and which could have occurred?** Type I: wrongly concluding the target is missed; Type II: missing a real exceedance. We rejected, so only a Type I error is possible.
11. **What affects power?** Larger $n$, larger true effect and lower variability increase power; a smaller $\alpha$ reduces it.
12. **What can Shapiro–Wilk not tell you?** It cannot prove normality (large $p$ may just mean low power) and it says nothing about independence.
