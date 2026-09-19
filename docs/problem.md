# Estimand, observation model, and pilot identities

## Scope of the first executable model

We freeze a population of N units, split equally between two product variants X in {0,1}. Each unit has observable telemetry S, a prediction f in [0,1], and an outcome Y in {0,1}. Historical residual scores are observable to the allocator. The main outcome vector is hidden until a unit is audited. The target is the finite-pool contrast:

    delta = sum_i w_i Y_i,
    w_i = 1/n_1 if X_i=1, otherwise -1/n_0.

This is a stratified finite-pool measurement problem. It does not yet identify a real population average treatment effect or establish a causal explanation for a change in outcomes.

For each unit independently, audit I_i is Bernoulli(pi_i), with probabilities chosen from observable information before the main labels are exposed. The expected budget is sum_i pi_i. We require strictly positive probabilities. Sampling from a finite pool with a fixed number of labels would have different inclusion dependencies and variance formulas; it is not implemented here.

## Established correction identity

    delta_hat = sum_i w_i [ f_i + I_i (Y_i-f_i)/pi_i ].

Conditional on the fixed pool and the selected probabilities, E[I_i/pi_i]=1, so E[delta_hat]=delta. This is the standard prediction-assisted inverse-probability correction used in the cited literature, not a new theorem.

Writing r_i=Y_i-f_i, independence yields:

    V = sum_i w_i^2 r_i^2 (1-pi_i)/pi_i.

An unbiased design-based variance estimate is:

    V_hat = sum_{audited i} w_i^2 r_i^2 (1-pi_i)/pi_i^2.

An approximately normal interval uses delta_hat +/- 1.96 sqrt(V_hat). Small budgets and highly unequal probabilities can make this approximation unreliable. We explicitly measure its coverage in the pilot; we do not infer validity from unbiasedness.

## Conservative finite-pool interval

Let a_i=max(f_i,1-f_i), since Y_i is bounded in [0,1]. Then V is bounded by

    V_max = sum_i w_i^2 a_i^2 (1-pi_i)/pi_i.

Each centered summand has absolute magnitude at most b=max_i |w_i| a_i/pi_i. Bernstein's inequality gives the conservative two-sided radius

    sqrt(2 V_max log(2/alpha)) + (2/3)b log(2/alpha).

Intersect the resulting interval with [-1,1]. This is a standard concentration bound adapted to the stated observation model, not a new bound. It may be too wide to select a product with small budgets. Its assumptions exclude correlated audit decisions, outcome-dependent label availability, unrecorded propensities, or changing the target pool midway through measurement.

## Two observationally identical worlds

Fix X, S, f, and historical errors in two worlds. Change only the hidden outcome-generating probabilities. Any procedure that receives only those fixed observables has the same output distribution in both worlds. If the target contrast has different signs, that procedure cannot choose correctly in both with probability above one half under equal prior world probabilities. This is an elementary indistinguishability argument, not evidence of a newly discovered impossibility theorem.

Main-study work must demonstrate a plausible delegated-task mechanism that creates such ambiguity, not merely set Y differently in a simulator.

## What labels mean

The eventual target is customer-assessed value of the delegated outcome, not imitation of what a person would click without assistance. Pilot Y is a synthetic binary outcome only. Actual preference labels, instrumental outcomes, satisfaction, and business value are not interchangeable.
