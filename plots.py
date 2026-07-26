# The Interpretability Residual

Measuring what circuit-based auditing does not explain, and deciding whether that measurement is worth funding.

Submission to **HIMPact Hacks '26**. Author: Samridhi Bharti.

## What this is

Mechanistic interpretability reports how much of a behaviour a circuit explains. It does not report what it fails to explain, even though that number is already available. The IOI circuit in GPT-2 small explains roughly 87% of the relevant logit difference; the remaining ~13% is not tracked by anyone.

This project defines that remainder as the **interpretability residual**:

```
R(B; M, T, A) = 1 - completeness(metric M, task T, ablation method A)
```

and asks a decision-theoretic question: is measuring it worth funding?

## Main results

| Result | Value |
|---|---|
| Belief threshold (closed form) | `p* = c_hedge / (c_ignore + c_hedge)` |
| Threshold at 6:1 harm asymmetry | 0.15 (analytic 0.143, simulated 0.146) |
| P(measurement worth funding) | 0.61 |
| Required metric separation (TPR - FPR) | 0.20 at prior 0.20, >0.70 at prior 0.10 |

The belief threshold is structurally robust: it reduces to the ratio between the two error costs, so it does not depend on the prior. The measurement threshold is genuinely prior-dependent and should be read as a range.

## Repository layout

```
paper/     submitted PDF
code/      decision model, Monte Carlo, robustness sweeps, plots
figures/   generated figures
docs/      reference list
```

## Running the code

```bash
pip install -r requirements.txt
python code/monte_carlo.py    # VoI under parameter uncertainty
python code/voi_model.py      # threshold robustness sweeps
python code/plots.py          # regenerate figures
```

No GPU, no model weights, no data download. Everything runs in a few seconds.

## Important caveat

All cost and informativeness parameters are **illustrative**. They demonstrate the structure of the decision and locate the thresholds; they are not empirical estimates. Real values need cost data from funders and separation estimates from interpretability groups. The residual itself is a bound on *achieved* coverage, not on achievable coverage: it never shows that anything is unexplainable in principle.

## Declaration of AI use

AI tools were used to accelerate drafting, generate plotting code, and locate the interpretability reliability literature. The framing, the residual definition, the hypothesis set, the experimental design and the parameter choices are my own.
