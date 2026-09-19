# Controlled separation of structural ambiguity and finite precision

This v3 extension is a new controlled multinomial simulation. It does not modify the frozen v2 tasks or analyses and collects no API responses or human observations. The plan and random seed were written before execution in `experiments/v3/precision-sweep-plan.json`; the output manifest records the plan and implementation hashes before sampling.

## Model and analytic controls

There are four latent classes and four actions. The channel is

    A_eta = (1-eta) (1/4) 1 1^T + eta I_4,

with eta in {0, .01, .03, .1, .3, 1}. The fixed outcome contrast is d = (.06, .02, -.04, -.02). The three population mixtures inherit the labels positive, negative, and near from v2: (.65,.10,.15,.10), (.15,.10,.65,.10), and (.42,.18,.27,.13). Their true contrasts are .033, -.017, and .0154, respectively. Here “near” is an inherited label, not an assertion that its contrast is close to zero.

The channel has eigenvalue 1 in the all-ones direction and eigenvalue eta on each of the other three dimensions. Consequently eta=0 is exactly pooled: every population has the same action law and the compatible contrast interval is [min(d),max(d)] = [-.04,.06]. Every eta>0 is full rank, so exact knowledge of A and q identifies p and gives structural width zero. The inverse amplifies contrasts in the informative subspace by 1/eta. Thus weak but positive separation can produce poor finite-sample precision without structural nonidentification. At eta=1 the action directly observes class, equivalent to a perfect parser of this declared taxonomy.

For every condition the script solves the exact-A, exact-q population LP, retains both witnesses and numerical residuals, and checks its width against this analytic answer. This check does not use an estimated channel as population truth.

## Sampling and methods

For each eta, calibration size per class in {40,160,640,2560}, and each of the three mixtures, generate 200 independent complete repetitions. Each repetition draws a multinomial calibration column of the specified size for each class and an independent multinomial field sample of size twice the calibration count per class. Separate child random streams are used across cells; methods within a repetition share the same samples for paired comparisons. There are 72 cells and 14,400 independent repetitions, with 43,200 method evaluations.

The methods differ only in which information is known:

| Method | Channel information | Field information | Marginal coverage lower bound |
|---|---|---|---:|
| Field only | Exact A | Simultaneous field-frequency box, alpha .02 | 98% |
| Calibration only | Simultaneous calibration box, alpha .02 | Exact q | 98% |
| Joint | Calibration box, alpha .02 | Field-frequency box, alpha .02 | 96% |

The boxes use the same Bonferroni Clopper-Pearson construction as v2. The estimator receives exact d in all cases. This is an uncertainty decomposition, not a comparison against different real-world data acquisition costs. Exact q or exact A are controlled oracle conditions.

## Metrics and numerical validation

Coverage, resolution, and wrong-resolution rates use all 200 repetitions as their denominator. An infeasible interval counts as uncovered and unresolved, is retained in raw records, and is reported separately. Width quantiles are explicitly conditional on feasibility. Each returned lower and upper witness is independently checked against the supplied channel, probability, and joint-mass constraints in addition to the solver wrapper's check. The decision threshold is the implementation constant 1e-8, matching the frozen plan, and reported inclusion tolerance is 1e-10. A numerical witness violation raises an error and aborts rather than being classified as an ordinary infeasible interval; no such violation occurred. The frozen plan's invalid-interval wording refers to intervals rejected as infeasible by the model constraints.

Each Bernoulli rate includes its plug-in Monte Carlo standard error, sqrt(rate(1-rate)/200). At rate zero or one that plug-in error is zero and is not proof of certainty. Exact two-sided 95% binomial intervals for the Monte Carlo coverage and wrong-resolution probabilities are also supplied. These Monte Carlo intervals concern repeatability of the simulation frequency; they are distinct from the 96% or 98% inferential intervals being evaluated. No family-wise claim is made over cells.

`summary.csv` gives every cell and method; `replicates.csv` retains individual interval endpoints and failures; `structural.json` gives exact-model witness controls. The vector figure displays the positive cohort only and separates exact structural width, median finite-sample width, and joint-method resolution. All three cohorts remain in the tabular results.

## Reproduction

    python3 -m unittest discover -s tests -p test_precision_sweep.py -v
    python3 experiments/v3/precision_sweep.py --output results/precision-sweep-v3-reproduction

The output directory must not exist. The script uses the frozen plan by default and refuses to overwrite an earlier run. Numerical CSVs reproduce from the plan and software environment. Figure metadata and execution timestamps can differ across builds.

This analysis can diagnose whether a procedure confuses limited sample precision with structural ambiguity. It cannot establish the true channel or customer relevance of the earlier language-model experiment. It is not a new identification theorem or a new general statistical method.

## Observed controlled results

All 14,400 repetitions completed, yielding 43,200 intervals. Eighty-four intervals were infeasible, all in the field-only method, and remain in its denominators. There were four wrong resolutions, also all field-only. Empirical cell coverage ranged from 96% to 100% for field-only and was 100% for calibration-only and joint. These cell rates have Monte Carlo error and do not prove exact coverage; every summary includes its uncertainty.

For the positive cohort at eta=.01 and calibration count 2,560 per class, structural width is exactly zero, while the joint median interval width is .1 and no repetition resolves the decision. At eta=.1 at that same budget, field-only resolution is 98%, calibration-only is 54%, and joint resolution is 1%; the joint median width is .076507. At the perfect-class endpoint eta=1 with 40 calibration observations per class and 80 field observations, joint resolution is 81%, compared with 99% field-only and 100% calibration-only; joint resolution reaches 100% at calibration count160. The pooled eta=0 channel retains structural width .1 at all budgets. These results directly separate structural ambiguity, weak separation, and conservative finite calibration/field uncertainty.

The distributed `replicates.csv.gz` is a lossless deterministic gzip archive of the full raw CSV; decompression was verified byte-for-byte. Numerical outputs and the archive are checksummed in the manifest.
