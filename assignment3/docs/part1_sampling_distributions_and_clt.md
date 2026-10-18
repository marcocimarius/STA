# Part 1: Sampling distributions and the CLT

Sources: Session 5 notes, Session 5 demo notebook, Tutorial 5, Brooks Chapter 5.

Contents:

1. [The big idea: repeated studies](#1-the-big-idea-repeated-studies)
2. [Three distributions you must not confuse](#2-three-distributions-you-must-not-confuse)
3. [The population model](#3-the-population-model-exponential-with-μ--σ--60)
4. [1a: centre and spread of the sample mean](#4-1a-centre-and-spread-of-the-sample-mean)
5. [1b: shape and the central limit theorem](#5-1b-shape-and-the-central-limit-theorem)
6. [1c: a probability for the sample mean](#6-1c-a-probability-for-the-sample-mean)
7. [1d: planning a sample size](#7-1d-planning-a-sample-size)
8. [1e: the law of large numbers](#8-1e-the-law-of-large-numbers)
9. [1f: what the CLT does not do](#9-1f-what-the-clt-does-not-do)
10. [Formula sheet](#10-formula-sheet)
11. [Likely oral-exam questions](#11-likely-oral-exam-questions)

---

## 1. The big idea: repeated studies

> **The population mean is fixed; the sample mean varies.**

**The real-life problem.** A service company wants the *average restoration time* of all repairs, $\mu$. Nobody knows it, because not every repair can be measured. So you run a **study**: time 5 repairs and average them. Suppose you get $\bar x = 95$ minutes. Can you trust that 95? Would another 5 repairs have given 94, or 30? You only did the study once, so you cannot tell.

**What Part 1 does.** We play god. We *know* the truth ($\mu = 60$) and we can repeat the same study as often as we like. Here are 4 of our 20,000 simulated studies with $n = 5$:

```
study 1: [ 79.9  53.9 198.2 139.0   4.1] -> mean 95.0
study 2: [ 27.9  56.3  39.1 199.2   9.2] -> mean 66.3
study 3: [  5.0 142.7  28.8  59.3  92.8] -> mean 65.7
study 4: [ 77.5  11.1  86.7  62.2  33.6] -> mean 54.2
```

Every study uses the same population and the same method, yet each gives a different answer. Study 1 did nothing wrong; it was unlucky and caught a 198-minute repair.

**The list of 20,000 study means, and how it is spread out, is the sampling distribution.** It shows every answer your study *could* have given, and how often each comes up.

**Why this matters later.** In Part 1 we know the truth, so the simulation is a demonstration that the formulas work. In Parts 2–3 you have *one* real study and do not know the truth. You cannot simulate 20,000 studies there, but you can use the formula $\operatorname{SE} = s/\sqrt n$ to say how far your one answer probably is from the truth. That is a **confidence interval**.

### Small exact example (from the Session 5 notes)

Population $= \{1, 2, 3\}$ with $\mu = 2$. Draw samples of size $n = 2$ with replacement. There are 9 possible samples:

| sample | 1,1 | 1,2 | 1,3 | 2,1 | 2,2 | 2,3 | 3,1 | 3,2 | 3,3 |
|---|---|---|---|---|---|---|---|---|---|
| $\bar x$ | 1 | 1.5 | 2 | 1.5 | 2 | 2.5 | 2 | 2.5 | 3 |

So $\bar X$ takes the values 1, 1.5, 2, 2.5, 3 with probabilities 1/9, 2/9, 3/9, 2/9, 1/9. This is the *exact* sampling distribution: centred at $\mu = 2$ and less spread out than the population. In Part 1 we cannot list every possible sample, so we **simulate** many of them instead.

---

## 2. Three distributions you must not confuse

| Name | What it describes | In Part 1 |
|---|---|---|
| **Population distribution** | All possible *individual* values $X$ | Single restoration times: Exponential, mean 60 |
| **Observed sample** | The $n$ values collected in *one* study | One row of the simulated matrix |
| **Sampling distribution** | The values a *statistic* (here $\bar X$) takes across *repeated* samples of the same size $n$ | The 20,000 sample means for a given $n$ |

A **statistic** is any number computed from a sample ($\bar x$, $s$, $\hat p$, …). Before the sample is drawn it is a random variable (capital $\bar X$); after drawing it is a number (lowercase $\bar x$).

---

## 3. The population model: exponential with $\mu = \sigma = 60$

The exponential distribution (Assignment 2) models waiting and repair times. It has one parameter, the rate $\lambda$:

$$\mu = \frac{1}{\lambda}, \qquad \sigma = \frac{1}{\lambda}$$

So the mean and SD are always equal. Here $\lambda = 1/60$, giving $\mu = \sigma = 60$ minutes. The distribution is **strongly right-skewed** (many short repairs, a few very long ones). It is clearly **not normal**, which makes it a good test case for the CLT.

**NumPy detail:** `rng.exponential(scale=...)` takes **scale = mean = $1/\lambda$**, *not* the rate. So we pass `scale=60`.

**Seed:** `np.random.default_rng(2026)` creates one random generator with a fixed seed. The same seed gives the same "random" numbers every run, so the results are **reproducible**. Like the tutorial, we create it once and reuse it in 1a–1e. Run the cells **top to bottom**, otherwise the numbers change.

---

## 4. 1a: centre and spread of the sample mean

### The code

```python
for n in sample_sizes:
    samples = rng.exponential(scale=mu, size=(n_rep, n))  # each row is one sample of size n
    means[n] = samples.mean(axis=1)                       # one sample mean per row
```

`size=(n_rep, n)` creates a matrix with **20,000 rows and $n$ columns**. **Each row is one study.** `.mean(axis=1)` averages across each row, which gives 20,000 sample means:

```
          col1   col2  ...  coln      row mean
sample 1  42.1  101.3  ...  12.9  →   x̄₁
sample 2   7.4   55.0  ...  80.2  →   x̄₂
   ...                                ...
sample 20000                     →   x̄₂₀₀₀₀
```

Do not mix up the two "sizes": **20,000 is the number of repeated studies**, not the $n$ in $\sigma/\sqrt n$. More repetitions make the *histogram* smoother; a larger $n$ makes the *standard error* smaller.

### The theory

Assume $X_1, \dots, X_n$ are **i.i.d.** (independent and identically distributed) with mean $\mu$ and SD $\sigma$.

**Centre:** $E[\bar X] = \frac{1}{n}(E[X_1] + \dots + E[X_n]) = \frac{1}{n} n\mu = \mu$.
On average the sample mean hits the truth, so it is **unbiased**.

**Spread:** independent variances add, so $\operatorname{Var}(\bar X) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}$. Taking the square root:

$$\boxed{\operatorname{SE}(\bar X) = \frac{\sigma}{\sqrt n}}$$

The **standard error** is the *standard deviation of the sampling distribution*: how far a single study's $\bar x$ typically lands from $\mu$.

| Quantity | Spread of what? |
|---|---|
| $\sigma$ | Individual observations in the population |
| $s$ | Estimated individual spread, from one sample |
| $\sigma/\sqrt n$ | Means from repeated samples of size $n$ |
| $s/\sqrt n$ | Estimated SE when $\sigma$ is unknown (Part 2) |

> More observations make the *average* more stable. They do not make the *individual* values less spread out.

### Our results

| $n$ | mean of means | theoretical SE | SD of means | meaning |
|---|---|---|---|---|
| 1 | 60.33 | 60.00 | 60.20 | one repair can miss the truth by about 60 min |
| 5 | 59.50 | 26.83 | 26.68 | an average of 5 typically misses by about 27 min |
| 20 | 59.94 | 13.42 | 13.35 | typically misses by about 13 min |
| 80 | 59.99 | 6.71 | 6.74 | typically misses by about 7 min |

- The centre stays at 60, which confirms $E[\bar X] = \mu$.
- The spread shrinks like $1/\sqrt n$: **4× the data halves the SE** (20 → 80 gives 13.4 → 6.7).
- The simulation matches the formula, so the one-line formula replaces 20,000 simulated studies.

These two formulas work for **any** population shape (they need only i.i.d. and a finite $\sigma$). They give the **centre and spread** of $\bar X$, not its **shape**. The shape is the job of the CLT.

---

## 5. 1b: shape and the central limit theorem

### Two different results

| Situation | Result | Symbol |
|---|---|---|
| Population is **normal** | $\bar X \sim N(\mu, \sigma^2/n)$ **exactly**, for every $n$ | $\sim$ ("is distributed as") |
| Population is **not normal**, finite variance (our case) | $\bar X \approx N(\mu, \sigma^2/n)$ **approximately**, improving as $n$ grows. This is the **Central Limit Theorem** | $\approx$ ("approximately") |

Use $\sim$ only for the exact normal case and $\approx$ for the CLT. The course explicitly lists mixing these up as a common mistake.

**Notation trap:** the second parameter of $N(\cdot,\cdot)$ is the **variance** $\sigma^2/n$. But SciPy's `scale` wants the **SD**, so we pass `norm.pdf(x, loc=mu, scale=sigma/np.sqrt(n))`. (In the Session 5 demo: "SciPy `scale` is the SD of whichever random quantity we model.")

### The code

The code follows Tutorial 5. For each $n$ it draws a **density histogram** of the 20,000 means (`density=True`, so the bar areas sum to 1 and can be compared with a PDF). It then overlays the normal curve `norm.pdf(x_grid, loc=mu, scale=se)`. The $n=1$ panel also shows the exponential population curve, because for $n=1$ the means *are* single observations.

### What the plot shows

- **$n=1$**: the exponential population itself, with its peak at 0 and a long right tail. The normal curve is terrible and even puts probability on negative times.
- **$n=5$**: still clearly right-skewed.
- **$n=20$**: nearly bell-shaped, with a slight right skew.
- **$n=80$**: close to normal.

So, as $n$ grows, the **centre stays at 60**, the **spread shrinks** ($\sigma/\sqrt n$) and the **shape becomes more normal** (CLT).

**There is no magic "$n = 30$" rule.** How fast the shape becomes normal depends on how skewed the population is. A mildly skewed population needs a small $n$; a heavily skewed one needs a large $n$.

---

## 6. 1c: a probability for the sample mean

**Question:** what is the chance that a study's average restoration time exceeds 75 minutes?

Two ways to get it:

1. **Simulation:** count the share of the 20,000 simulated means above 75: `np.mean(means[n] > 75)`. (A comparison like `means[n] > 75` gives an array of True/False; the mean of True/False is the proportion of True.)
2. **CLT approximation:** pretend $\bar X \sim N(60, \sigma^2/n)$ and compute the upper tail with `norm.sf(75, loc=mu, scale=se)`. `sf` is the survival function, $P(\bar X > 75) = 1 - \text{CDF}$.

By hand, for $n = 20$: $\operatorname{SE} = 60/\sqrt{20} = 13.42$, $z = (75-60)/13.42 = 1.12$, and $P(Z > 1.12) \approx 0.13$.

| $n$ | SE | $z$ | simulated | CLT |
|---|---|---|---|---|
| 20 | 13.42 | 1.12 | 0.1334 | 0.1318 |
| 80 | 6.71 | 2.24 | 0.0186 | 0.0127 |

**Interpretation:**

- At $n=20$ the two agree well.
- At $n=80$ the CLT **underestimates** the tail by about a third, even though the histogram looks almost normal. Why? The sampling distribution still carries a bit of the exponential's right skew, so its **right tail is longer** than the normal curve's. And 75 is 2.24 SE out, far in the tail, which is exactly where small shape differences matter most.
- This is not simulation noise: with 20,000 repetitions the simulated proportion is accurate to about $\pm 0.001$.
- **Lesson:** "approximately normal" is good near the centre, but tail probabilities are where the CLT is weakest. Here the simulation is the better answer, because it uses the true exponential model.
- The probability drops from 0.13 to 0.02 because a larger $n$ gives a smaller SE, so being 15 minutes off becomes rare.

---

## 7. 1d: planning a sample size

**Question:** how many repairs must a study time so that the SE is at most 6 minutes?

Solve the SE formula for $n$ (the same method as the plate example in the Session 5 notes and Code 2 of the demo):

$$\frac{\sigma}{\sqrt n} \le 6 \iff \sqrt n \ge \frac{60}{6} = 10 \iff n \ge 100$$

In code, `np.ceil` rounds up: `n_required = int(np.ceil((sigma / target_se) ** 2))`. **Always round up**, because rounding down would give an SE slightly above the target.

Check the neighbours: $n = 99$ gives SE $= 6.03 > 6$ (fails), and $n = 100$ gives SE $= 6.00$ (passes). So **$n = 100$**.

**Simulation check:** 20,000 studies of $n=100$ give an SD of means of 6.02; for $n=99$, 6.08. The 6.02 is slightly above 6. That does not contradict the formula: a simulated SD has its own simulation noise (roughly $\pm 0.03$ here), and $n=100$ sits *exactly* on the boundary SE $= 6$. Simulation confirms the formula *approximately*; the formula is what decides the exact smallest $n$.

---

## 8. 1e: the law of large numbers

### The code

```python
one_sequence = rng.exponential(scale=mu, size=n_lln)               # ONE sequence of 5,000 repairs
running_mean = np.cumsum(one_sequence) / np.arange(1, n_lln + 1)
```

- `np.cumsum` gives running totals: $x_1$, $x_1+x_2$, $x_1+x_2+x_3$, …
- Dividing by $1, 2, 3, \dots$ gives the running mean $\bar x_k$ = the mean of the first $k$ observations.

### The theory

**Law of large numbers (LLN):** as you keep adding observations to *one* sequence, the running mean $\bar x_k$ gets closer and closer to $\mu$.

Our run: 67.9 after 10, 59.9 after 100, 60.1 after 1,000 and 59.1 after 5,000 observations. It wobbles a lot at first, then settles. It does **not** approach 60 in a straight line; the wobbles just become smaller. The remaining gap at 5,000 (about 0.9) is about one SE ($60/\sqrt{5000} \approx 0.85$), which is perfectly normal.

### LLN vs. sampling distribution / CLT

This is a common exam trap:

| | LLN (1e) | Sampling distribution / CLT (1a–1c) |
|---|---|---|
| Data | **One** sequence, growing length $k$ | **Many** independent samples, each of **fixed** size $n$ |
| Points | Neighbouring points share almost all data | Each mean uses fresh, independent data |
| Says | $\bar x_k$ **gets close to** $\mu$ | the **shape** of $\bar X$ is approximately normal, with spread $\sigma/\sqrt n$ |
| Picture | a line settling on $\mu$ | a histogram becoming bell-shaped |

---

## 9. 1f: what the CLT does not do

The assignment requires this statement explicitly. The CLT is about **sample means** only. It does **not**:

1. **make individual values normal.** One restoration time is still exponential. For "P(one repair > 75 min)" use the exponential model, never the normal.
2. **fix dependence.** If repairs are linked (e.g. one big outage causes many slow repairs), the i.i.d. assumption fails and $\sigma/\sqrt n$ is too optimistic.
3. **fix drift.** If the average changes over time, there is no single $\mu$ to converge to.
4. **fix unrepresentative sampling.** If only easy repairs are recorded, $\bar X$ is centred on the wrong value. A bigger $n$ just makes the wrong answer more precise.

---

## 10. Formula sheet

| | |
|---|---|
| Sample mean | $\bar X = \frac{1}{n}\sum X_i$ |
| Centre | $E[\bar X] = \mu$ |
| Variance | $\operatorname{Var}(\bar X) = \sigma^2/n$ |
| Standard error | $\operatorname{SE}(\bar X) = \sigma/\sqrt n$ |
| Normal population | $\bar X \sim N(\mu, \sigma^2/n)$ exactly |
| CLT (non-normal) | $\bar X \approx N(\mu, \sigma^2/n)$ |
| Standardise | $z = (\bar x - \mu)/\operatorname{SE}$ |
| Sample size for target SE | $n \ge (\sigma/\text{target})^2$, round **up** |
| SciPy | `norm(loc=mu, scale=SE)`: scale is an SD, not a variance |

---

## 11. Likely oral-exam questions

1. **What is a sampling distribution?** The distribution of a statistic across repeated samples of the same size from the same population.
2. **Why is $\bar X$ a random variable?** It depends on which sample happened to be drawn; a new sample gives a new value.
3. **Why is $E[\bar X] = \mu$?** By linearity of expectation. It means $\bar X$ is unbiased.
4. **SD vs. SE?** The SD is the spread of individual values; the SE is the spread of sample means across repeated samples.
5. **Why $\sqrt n$?** The variance scales with $1/n$ and the SD is its square root. So 4× the data halves the SE.
6. **What does the CLT say, and when is it exact?** $\bar X \approx N(\mu, \sigma^2/n)$ for large $n$. It is exact (not approximate) for any $n$ only if the population is normal.
7. **Is $n=30$ always enough?** No; it depends on the population's skewness. Even at $n=80$ our tail probability was off by a third.
8. **LLN vs. CLT?** The LLN: one growing sequence's mean settles at $\mu$. The CLT: the distribution of many fixed-$n$ means is approximately normal.
9. **Does a large $n$ make the data normal?** No. Only the sampling distribution of the *mean* becomes approximately normal.
10. **Why a seed?** Reproducibility.
11. **Why 20,000 repetitions?** A smooth, stable histogram with little simulation noise. It is unrelated to $n$.
