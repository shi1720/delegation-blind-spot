# A decision-specific observability diagnostic

This is an implementation of a standard partial-identification construction for a proposed delegated-choice experiment. It is not claimed as a new general linear-programming method.

## Model

Assume a finite, declared set of K customer-intent classes with population masses p. A fixed agent configuration induces an actions-by-classes channel A: each column is a probability distribution over observable action categories. The product sees action frequencies q=A p. For a specified pair of candidate product changes, d_k is the independently defined difference in customer outcome for class k. The target is d^T p.

The intent taxonomy, the outcome contrast, and the stability of A are substantive assumptions. A prototype with arbitrary hand-selected classes cannot validate them for real customers.

## Bounds and witnesses

With known A and q, minimize and maximize d^T p over p>=0, sum p=1, A p=q. If the interval contains zero, both product rankings remain possible under the stated information. Return witness populations, not a guessed recommendation. Rank deficiency does not imply every decision is unresolved: a contrast may be identified even when individual class masses are not.

For uncertain channels, suppose L_ak <= A_ak <= U_ak, independently by coordinate, with simplex columns. Introduce joint masses J_ak=A_ak p_k. Then:

    sum_k p_k = 1; p_k >= 0
    sum_a J_ak = p_k
    L_ak p_k <= J_ak <= U_ak p_k
    q_lower[a] <= sum_k J_ak <= q_upper[a]

All constraints are linear. Minimize and maximize d^T p over p,J. The implementation verifies each solver witness against the constraints.

## Why the parameterization is exact for this uncertainty set

Every feasible original pair (A,p) maps to J=A diag(p), which satisfies these inequalities. Conversely, for a feasible (J,p), construct A_ak=J_ak/p_k for p_k>0. The column sum is one and the interval bounds hold. If p_k=0, all entries of that J column are zero; choose any simplex column within [L[:,k],U[:,k]], which exists by the input feasibility check. This reconstructs an admissible A with the required frequencies. Hence the LP extrema are attainable within the supplied model, up to numerical tolerances.

The argument relies on a rectangular uncertainty description. Correlated constraints across channel columns, common model parameters, or unmodeled class behavior require an extended formulation. Do not label a coordinate-box result sharp relative to those richer models.

## Finite-sample interpretation

For multinomial calibration counts, the code constructs Bonferroni Clopper-Pearson coordinate intervals. For K separately calibrated columns, split the channel error probability across the columns as well. For field counts, use another simultaneous interval box. If the channel and field boxes jointly cover their true probabilities and the target model is correct, the LP interval contains d^T p. Allocate alpha between the calibration and field stages explicitly before claiming overall coverage.

This does not account for sampling uncertainty in d, unknown or missing intent classes, selective customer participation, within-class changes, or a deployed agent differing from calibration. These must be handled before applying the diagnostic to actual product decisions. A narrow interval under the wrong channel can still be wrong.

## Antecedents and novelty boundary

[Linear Partial Monitoring](https://jmlr.org/papers/volume24/22-1248/22-1248.pdf) and [Information Directed Sampling for Linear Partial Monitoring](https://proceedings.mlr.press/v125/kirschner20a.html) already connect decision learnability to observation structure. [Finkelstein et al.](https://proceedings.mlr.press/v161/finkelstein21b/finkelstein21b.pdf) study partial identification under measurement error using linear programs. Choice via AI also studies identification in delegated choice. Their exact methods require further comparison.

Our open research question is how to construct, validate, and use decision-specific observation models for actual delegated product tasks under changing agents. This diagnostic is a tool for that study. The existence of an LP or a rank condition alone is not an original contribution.
