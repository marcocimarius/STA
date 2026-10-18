# Part 2: Estimating mean sensor error (confidence interval for a mean)

Sources: Session 6 notes, Session 6 demo notebook, Tutorial 6, Brooks Chapter 6.

Contents:

1. [The situation in plain words](#1-the-situation-in-plain-words)
2. [Vocabulary you need first](#2-vocabulary-you-need-first)
3. [2a: summary numbers, SD vs. SE](#3-2a-summary-numbers-sd-vs-se)
4. [2b: checking the data with plots](#4-2b-checking-the-data-with-plots)
5. [2c: building the 95% t interval](#5-2c-building-the-95-t-interval)
6. [2d: 90%, 95%, 99%](#6-2d-90-95-99)
7. [2e: how many sensors would we need?](#7-2e-how-many-sensors-would-we-need)
8. [2f: the bootstrap](#8-2f-the-bootstrap)
9. [Formula sheet](#9-formula-sheet)
10. [Likely oral-exam questions](#10-likely-oral-exam-questions)

---

## 1. The situation in plain words

A company has temperature sensors. Each sensor was compared with an exact reference thermometer:

$$\text{error} = \text{sensor reading} - \text{true temperature}$$

- An error of +0.3 means the sensor read 0.3 °C **too high**.
- An error of −0.5 means it read 0.5 °C **too low**.

We tested **64 sensors**. The real question is not about these 64. It is about **all sensors of this type**: *on average, do they read too high or too low, and by how much?*

That "average error of all sensors" is called $\mu$ (mu). We can never measure it exactly, because we can't test every sensor. Part 2 is about **estimating $\mu$ from the 64 sensors and saying how sure we are**.

**The link to Part 1:** in Part 1 we *knew* the truth (60) and watched how sample means bounce around it. Now we *don't* know the truth and have only **one** sample. Part 1 taught us that a sample mean typically misses the truth by about one **standard error**. Part 2 uses that to build a "give or take" range.

---

## 2. Vocabulary you need first

| Term | Meaning in plain words |
|---|---|
| **Parameter** ($\mu$) | The true number for the whole population. Fixed, but unknown. |
| **Estimate** ($\bar x$) | Our best guess, computed from the sample. |
| **Point estimate** | A single number guess: "the average error is 0.19 °C". |
| **Confidence interval (CI)** | A range guess: "the average error is between 0.03 and 0.34 °C". |
| **Margin of error** ($E$) | The "give or take" part: interval = estimate ± margin. |
| **Critical value** | A multiplier that decides how wide the interval is (about 2 for 95%). |
| **Confidence level** | 90%, 95% or 99%: how often the *method* catches the truth. |

**The basic recipe for every confidence interval** (Session 6 notes):

$$\text{estimate} \;\pm\; \underbrace{\text{critical value} \times \text{standard error}}_{\text{margin of error}}$$

```
     estimate − E          estimate          estimate + E
  |-------------------------|-------------------------|
                            <------ margin E -------->
  <-------------------- total width 2E -------------->
```

---

## 3. 2a: summary numbers, SD vs. SE

| | value | in words |
|---|---|---|
| $n$ | 64 | number of sensors tested |
| $\bar x$ | 0.1883 °C | average error of our 64 sensors: they read about 0.19 °C too high |
| $s$ | 0.6257 °C | how much individual sensors differ from each other |
| $\operatorname{SE} = s/\sqrt n$ | 0.0782 °C | how much the *average* would change if we tested 64 different sensors |

### Standard deviation vs. standard error

This is the same idea as in Part 1, now with real data:

- **SD $s$ = 0.63**: look at *individual sensors*. One reads +1.2 and another −0.5; a typical sensor is about 0.63 °C away from the average.
- **SE = 0.078**: look at the *average of 64 sensors*. If we repeated the whole study with 64 new sensors, the new average would typically be about 0.08 °C different.

SE = SD / √64 = SD / 8. Averaging cancels out much of the randomness, so the average is 8 times more stable than one sensor.

**Why $s$ and not $\sigma$?** In Part 1 we *knew* $\sigma = 60$. Here nobody tells us the true spread of all sensors, so we **estimate** it with $s$ from the sample. That makes the SE an *estimated* SE, and it is why we later use **t** instead of **z**.

**Code note:** `x.std(ddof=1)` divides by $n-1$, the sample standard deviation (as in Assignments 1–2).

---

## 4. 2b: checking the data with plots

Before building a t interval, we check whether its assumption is believable. The t interval is **exact if the population is normal** (bell-shaped). For non-normal data it is an approximation that works well if $\bar X$ is approximately normal.

**Histogram:** roughly bell-shaped and symmetric, centred near 0.19, with no crazy outliers. The orange normal curve fits well.

**QQ-plot (quantile–quantile plot):** this plot answers "do the data look normal?" more precisely than a histogram.
- Each dot is one sensor. The x-axis shows where it *would* be if the data were perfectly normal; the y-axis shows where it *actually* is.
- **Dots on the straight line** means the data look normal.
- **Dots bending away** (an S-shape or a curve) means skew or heavy tails.

Here the dots hug the line, and only the top few are slightly above it, so the data look normal enough. With $n = 64$ the CLT (Part 1) also helps: even mildly non-normal data give a near-normal $\bar X$.

### Why plots cannot prove independence

**Independent** means one sensor's error tells you nothing about another's. Plots show **what values** you got, not **how** you got them. Example: if 20 of the sensors came from one faulty production batch, their errors would be linked, but the histogram could look exactly the same. Independence must come from **how the study was designed** (here: "independently selected sensors"). If it is violated, the SE formula $s/\sqrt n$ is too small, so the interval is too narrow and looks more precise than it really is.

---

## 5. 2c: building the 95% t interval

### Step by step

| step | formula | value |
|---|---|---|
| 1. degrees of freedom | $n - 1$ | 63 |
| 2. critical value | $t_{63,\,0.975}$ = `t.ppf(0.975, 63)` | 1.9983 |
| 3. standard error | $s/\sqrt n$ | 0.0782 |
| 4. margin of error | critical value × SE | 1.9983 × 0.0782 = 0.1563 |
| 5. interval | $\bar x \pm E$ | 0.1883 ± 0.1563 = **[0.032, 0.345] °C** |

Then we verify with SciPy: `t.interval(0.95, 63, loc=xbar, scale=se)` gives the same result. Note that `scale` is the **SE**, not $s$.

### What is "t" and why not "z"?

In Part 1, 1c we used the **normal (z) curve**: about 95% of its area lies within ±1.96 of the centre. So a 95% interval would be $\bar x \pm 1.96 \times \operatorname{SE}$.

But that only works if we know the *true* $\sigma$. We only have $s$, an estimate that is itself a bit random. To be honest about that extra uncertainty, we use the **t distribution**: a bell curve with **fatter tails** than the normal, so its critical value is a bit bigger (wider interval).

```
normal z:   95% within ±1.960
t, df=63:   95% within ±1.998   ← slightly wider, because s is estimated
t, df=5:    95% within ±2.571   ← much wider with tiny samples
```

**Degrees of freedom (df = n − 1)** set how fat the tails are. A small sample means $s$ is unreliable, so the tails are fat and the interval wide. A large sample means $s$ is reliable, so t comes very close to z. The rule is: **$\sigma$ unknown → use t**, even when $n$ is large. Tutorial 6: "A large sample is not a reason to pretend σ is known."

**Why 0.975 and not 0.95?** A 95% interval leaves 5% outside, split into 2.5% on each side. So we need the point with 97.5% of the area below it:

```
 2.5% |<------------- 95% ------------->| 2.5%
    -1.998              0             +1.998
```

### Interpreting the interval

**Correct:** "We estimate that the mean calibration error of all sensors of this type is between 0.032 and 0.345 °C." The whole interval is above 0, so the sensors seem to read slightly too high on average.

**About the mean, not individual sensors:** individual sensors in the data range from −1.2 to +1.6 °C. The interval says nothing like "95% of sensors are within 0.03–0.34".

### Interpreting "95% confidence" (exam favourite)

The 95% is about the **method**, not this one interval:

> If we repeated the study many times (64 new sensors each time, a new interval each time), about **95% of those intervals would contain the true $\mu$**.

```
true μ (fixed, unknown)
         |
   |-----|-----|        covers ✓
      |--|--------|     covers ✓
 |-------|---|          covers ✓
           |-------|    misses ✗   ← about 1 in 20 misses
    |----|------|       covers ✓
```

**Wrong:** "There is a 95% probability that $\mu$ is between 0.032 and 0.345." $\mu$ is a fixed number; it is either inside or not. The *interval* is what's random (it changes with each sample), not $\mu$.

---

## 6. 2d: 90%, 95%, 99%

| confidence | critical value | margin | interval | width |
|---|---|---|---|---|
| 90% | 1.669 | 0.131 | [0.058, 0.319] | 0.261 |
| 95% | 1.998 | 0.156 | [0.032, 0.345] | 0.313 |
| 99% | 2.656 | 0.208 | [−0.020, 0.396] | 0.416 |

The code uses `t.ppf((1 + level) / 2, df)`: for 90% that's 0.95, for 95% it's 0.975, for 99% it's 0.995.

**Confidence–precision trade-off.** Think of a fishing net:
- A **wider net** (99%) catches the fish ($\mu$) more often, but tells you less precisely where it is.
- A **narrower net** (90%) is more precise but misses more often.

You can't have both with the same data. **The only way to get narrower *and* more confident is more data** (larger $n$ → smaller SE).

**Interesting detail:** only the 99% interval contains 0. So at 99% confidence, "the sensors are perfectly calibrated on average" ($\mu = 0$) is still a plausible value, while at 90% and 95% it is not. (This is just reading the intervals; formal hypothesis tests come in Session 7.)

---

## 7. 2e: how many sensors would we need?

**Goal:** a 95% interval with margin of error at most **0.10 °C** (currently it's 0.156).

The margin is $E = z \cdot s / \sqrt n$. Solve for $n$:

$$n \ge \left(\frac{z \cdot s}{E}\right)^2 = \left(\frac{1.960 \times 0.6257}{0.10}\right)^2 = 150.42 \;\Rightarrow\; \textbf{151 sensors}$$

- **Round UP** (always): 150 sensors give a margin of 0.1001, just over the target.
- We use **z = 1.96** (not t) because t depends on $n$, which is what we are solving for. The assignment says to use the normal value.
- We use **$s$ as a "planning value"**: our best guess of the spread in a future study.
- **Why it's only approximate:** the future study's $s$ will differ a bit, and its t value (≈1.976 for n = 151) is slightly bigger than 1.96.

**Rule of thumb:** margin ∝ 1/√n, so to shrink the margin from 0.156 to 0.10 (×0.64) you need $(0.156/0.10)^2 \approx 2.4\times$ more sensors.

This is the same idea as Part 1d (smallest $n$ for SE ≤ 6), now with the critical value included.

---

## 8. 2f: the bootstrap

### The idea

We want to know how much $\bar x$ would vary across repeated studies, but we can't repeat the study. The **bootstrap** fakes it by using our own sample as a stand-in for the population:

1. Draw 64 values **with replacement** from our 64 sensors (some sensors get picked twice, some not at all).
2. Compute the mean of this "fake sample".
3. Repeat 10,000 times, which gives 10,000 bootstrap means.
4. **Percentile interval** = the middle 95% of them (cut 2.5% from each end).

It's Part 1's simulation, except that instead of a known exponential population we resample our **observed data**.

```python
bootstrap((x,), np.mean, confidence_level=0.95, n_resamples=10_000,
          method="percentile", rng=np.random.default_rng(2026))
```

(Tutorial 6 writes `random_state=`; our SciPy version calls the same argument `rng=`.)

### Results

| interval | lower | upper | width |
|---|---|---|---|
| t interval | 0.032 | 0.345 | 0.313 |
| bootstrap | 0.041 | 0.341 | 0.300 |

They are very close, and the histogram of bootstrap means is bell-shaped. This is a nice confirmation that the t interval's normal assumption is fine here. The bootstrap is slightly narrower because it has no "fat tails" correction for estimating $\sigma$.

### What the comparison CANNOT tell you

Both intervals come from **the same 64 sensors**. The bootstrap only reshuffles them and adds no new information. So if:
- the 64 sensors are **not representative** (e.g. all from one good batch),
- the sensors are **not independent**, or
- the **reference thermometer itself is wrong**,

then **both** intervals are wrong in the same way, and they will *still agree* with each other. Agreement ≠ correctness. It cannot prove the sample is representative, that the 95% coverage really holds, or that $\mu$ is actually inside.

---

## 9. Formula sheet

| | |
|---|---|
| Sample mean | $\bar x = \frac{1}{n}\sum x_i$ |
| Estimated SE | $s/\sqrt n$ |
| t interval | $\bar x \pm t_{n-1,\,1-\alpha/2}\cdot s/\sqrt n$ |
| z interval (only if σ known) | $\bar x \pm z_{1-\alpha/2}\cdot \sigma/\sqrt n$ |
| Critical values (SciPy) | `t.ppf((1+level)/2, n-1)`, `norm.ppf((1+level)/2)` |
| Margin of error | $E$ = critical value × SE; width = $2E$ |
| Sample size for margin $E$ | $n \ge (z\,\sigma_{\text{plan}}/E)^2$, round **up** |
| SciPy check | `t.interval(level, n-1, loc=xbar, scale=se)` |

---

## 10. Likely oral-exam questions

1. **Estimator vs. estimate?** The estimator is the *method/formula* ($\bar X$, random before sampling); the estimate is the *number* it gave (0.1883).
2. **Bias vs. precision?** Bias means systematically off-target (e.g. a broken reference thermometer). Precision means how small the random scatter is (the SE). A narrow interval shows precision, not lack of bias.
3. **SD vs. SE?** Spread of individual sensors vs. spread of the average across repeated studies.
4. **Why t and not z?** σ is unknown and estimated by $s$; t accounts for that extra uncertainty.
5. **What are degrees of freedom?** $n-1$. They control how fat t's tails are; as df grows, t approaches z.
6. **What does 95% confidence mean?** 95% of intervals from repeated studies would contain μ. Not "95% probability μ is in this interval".
7. **Why does a higher confidence level give a wider interval?** A bigger critical value. Trade-off: confidence vs. precision.
8. **How do you make the interval narrower without losing confidence?** Increase $n$; the width ∝ 1/√n, so 4× the data halves it.
9. **What is a percentile bootstrap?** Resample the data with replacement many times, compute the mean each time, and take the middle 95%.
10. **What can't the bootstrap fix?** A biased or unrepresentative or dependent sample, because it reuses the same data.
11. **Why can't plots establish independence?** They show values, not the collection process. Independence comes from the design.
