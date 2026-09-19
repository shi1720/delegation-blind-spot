# The Delegation Blind Spot

**Research in progress. Author: Shivam Gupta.**

Working question: how can a product learn customer outcomes when its observable interactions are produced by agents?

This repository starts with a falsification pilot, not a finished paper or a claim of a new estimator. It implements established audit-corrected estimators and active sampling baselines, then examines shifts in the relationship between visible telemetry and unobserved outcomes. The initial data are entirely synthetic. No language model or human participant results are included.

## Reproduce the pilot

Python 3.9 or later, with the versions in `requirements.txt`:

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 experiments/run_pilot.py --config experiments/pilot-v1.json
python3 experiments/plot_pilot.py --results results/pilot-v1
```

The runner records configuration and source hashes, software versions, seeds, per-replicate estimates, realized audit costs, and summary metrics. A regeneration must match the timing-free numerical outputs. The exact expected audit budget is matched across implementable sampling policies; independent Bernoulli selection means realized cost varies and is reported.

## What is and is not measured

- Target: the difference between two **fixed synthetic population** outcome means. It is not a population causal treatment effect estimate from a real randomized trial.
- Audit estimator: a prediction-plus-inverse-probability residual correction. This is established survey-sampling and prediction-powered inference machinery.
- Baselines: uniform, historical-error active sampling, a fixed mixture, and a robust linear-path policy adapted from Li, Zrnic, and Candes (2025). An oracle policy uses otherwise unavailable outcome residuals and is labeled as such.
- Intervals: an ordinary design-based Wald approximation and a conservative finite-population Bernstein bound. The former is not guaranteed at tiny audit budgets. The latter depends on independent sampling and bounded outcomes.
- Test setting: observable data can be identical in two worlds with different outcomes. This is constructed, not evidence that a deployed product exhibits that phenomenon.
- Intended next work: full novelty subtraction; a distinct method if warranted; realistic delegated-task environments; real model experiments; a consented human study; proofs, manuscript, and reproducible publication artifacts.

See `docs/problem.md`, `docs/literature.md`, and `docs/research-status.md`. Numerical pilot success cannot establish originality or justify a claim about customer behavior.
