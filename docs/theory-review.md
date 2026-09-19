# Theory appendix and independent review

Author of the research manuscript: Shivam Gupta. Internal mathematical review, 19 September 2026. The propositions below are standard consequences of linear identification, convex duality, concentration, and statistical decision theory, specialized to the delegated-choice model. They are not claimed as new general theorems. The complete proofs make the assumptions and limits independently inspectable.

## Scope and notation

Let A be an m-by-K column-stochastic matrix, p belong to the K-dimensional probability simplex, q = Ap, and d be a fixed, known K-vector. The product decision contrast is Delta(p) = d^T p. For feasible q, write P_q = {p >= 0 : Ap = q}, L(q) = min_{p in P_q} d^T p, and U(q) = max_{p in P_q} d^T p. Since each column of A sums to one and q is a probability vector, the equality Ap = q already implies sum(p) = 1. All extrema exist by compactness.

This model describes class composition, not individual recovery. It requires stable within-class behavior and a meaningful outcome contrast. Even a perfectly calibrated channel cannot repair a misspecified outcome measure. Model-generated personas are synthetic inputs, never actual people or customer validation.

## Theorem 1. Global and local decision identification

The contrast is identified for every feasible q if and only if d belongs to row(A). For a particular q, the necessary and sufficient condition is d^T h = 0 for every h in span(P_q - P_q). Thus global non-identification need not imply non-identification at a boundary q.

**Proof.** If d = A^T v, then d^T p = v^T q for every p in P_q. Conversely, if d is outside row(A), the fundamental theorem of linear algebra supplies h in ker(A) with d^T h nonzero. Since 1^T A = 1^T, we have 1^T h = 0. Choose an interior simplex point p_0 and t > 0 small enough that p_0 +/- th remain nonnegative. These two populations share q = Ap_0 and have different contrasts. The local equivalence follows directly from the definition: constancy on P_q is equivalent to orthogonality to all pairwise differences, hence their span. QED.

**A boundary example.** Let A have columns (1,0), (0,1), and (0,1). The second and third classes cannot generally be separated. At q = (1,0), however, the only feasible population is (1,0,0), so every contrast is identified there. A rank-only diagnostic would miss this.

**Attribution.** This is a standard linear observability result. The connection between payoff contrasts and spans of observation maps is central to linear partial monitoring [R1].

## Theorem 2. Exact magnitude of the globally hidden contrast

Define the worst compatible contrast width

    W(A,d) = max_{p,r in simplex : Ap = Ar} |d^T(p-r)|.

Then

    W(A,d) = max_{Ah=0, ||h||_1 <= 2} d^T h
           = 2 min_v ||d - A^T v||_infinity.

The absolute value can be dropped in the first optimization because its feasible set is symmetric. The final expression is the distance from the decision contrast to the observable subspace, multiplied by two. It is zero exactly under Theorem 1.

**Proof.** Every difference h = p-r satisfies Ah = 0 and ||h||_1 <= 2. Conversely, if Ah = 0 and ||h||_1 <= 2, column normalization gives sum(h) = 0. Let h_+ and h_- denote its coordinatewise positive and negative parts; both have mass s = ||h||_1/2 <= 1. For any simplex vector u, p = h_+ + (1-s)u and r = h_- + (1-s)u are probability vectors with p-r = h and Ap = Ar. This proves the first equality, including attainability.

For the second equality consider the finite linear program min_{v,t} t subject to -t1 <= d-A^T v <= t1, t >= 0. Its dual is max_z d^T z subject to Az = 0 and ||z||_1 <= 1. One obtains it by assigning nonnegative multipliers to the two coordinate inequalities, subtracting their multipliers to form z, and enforcing stationarity in the unrestricted v. Both programs are feasible and bounded, so strong LP duality applies. Rescaling z to h = 2z proves the result. QED.

**Interpretation and limit.** W concerns the worst pair of populations over all q. The actual interval U(q)-L(q) can be much smaller. W is not a measured effect size in a real market. The dual distance is a standard quotient-norm and inverse-problem quantity; relating estimation difficulty to a modulus of continuity has substantial antecedents [R3].

## Theorem 3. Exact-observation estimation and decision lower bounds

Fix q with interval [L,U] and width w = U-L. Suppose the only observations are any number of independent draws from q, plus randomization independent of the unknown population. Every compatible population produces the same observation law.

1. For any estimator, its largest mean absolute error over P_q is at least w/2, and its largest mean squared error is at least w^2/4. If q is supplied exactly, the constant midpoint (L+U)/2 attains both bounds.
2. If L < 0 < U, no test can make both opposite-sign endpoint error probabilities smaller than 1/2. With equal prior mass on the endpoints, its average sign error is exactly 1/2.
3. If the loss is the customer-value regret of choosing between variants 0 and 1, the exact-observation minimax regret is

    R_star(q) = (-L U)/(U-L),  if L < 0 < U;
                0,             otherwise.

For a straddling interval, choosing variant 1 with probability t_star = U/(U-L) attains this value. Restricting to deterministic decisions gives minimax regret min(-L,U). At a zero endpoint, a weakly optimal variant exists, and the minimum regret is zero.

**Proof.** Let T have the common distribution of the estimator under the two attainable endpoint populations. Pointwise, |T-L|+|T-U| >= U-L. Taking expectations shows the largest endpoint absolute risk is at least w/2. Also ((T-L)^2+(T-U)^2)/2 = (T-(L+U)/2)^2+w^2/4 >= w^2/4. The midpoint achieves both maxima over every Delta in [L,U] when q is known.

For any possibly randomized decision rule, let t be its common probability of choosing variant 1 under all compatible populations. The endpoint sign errors are t and 1-t. The endpoint regrets are (-L)t and U(1-t). For an intermediate contrast, regret is no larger than the corresponding endpoint regret. Minimizing max((-L)t,U(1-t)) over t in [0,1] equates the two linear terms and yields the stated t_star and value. If the whole interval lies on one side of zero, choosing the weakly better variant incurs zero regret. QED.

**Scope.** The upper-bound attainability statements presume exact q and a known model. For finite data, these are lower bounds, not assertions that q can be learned without further cost. They concern the fixed observation channel. An intervention that changes the channel can break indistinguishability. These are elementary decision-theoretic consequences, not a new impossibility technique [R4].

## Theorem 4. Coarsening cannot reduce ambiguity

Let G be column-stochastic and B = GA. If q is an action distribution under A, then P(A,q) is contained in P(B,Gq). Consequently the B interval at Gq contains the A interval at q. In particular W(B,d) >= W(A,d).

**Proof.** Ap = q implies Bp = GAp = Gq. Minimizing over a larger set can only decrease a lower bound; maximizing can only increase an upper bound. For the global claim, every pair satisfying Ap = Ar also satisfies Bp = Br. QED.

This is a direct finite-channel implication of the comparison-of-experiments viewpoint [R5]. It does not prove that an improved agent is a coarsening of an earlier agent. That relationship would require empirical or structural justification. Task competence and informativeness have no general ordering in this model.

## Theorem 5. Finite-sample certificate with declared approximation bias

Assume A is known and Y_1,...,Y_n are independent categorical actions with distribution q = Ap. Select v independently of these observations. Define epsilon(v) = ||d-A^T v||_infinity and range(v) = max_a v_a-min_a v_a. With probability at least 1-alpha,

    |(1/n) sum_i v[Y_i] - d^T p|
        <= epsilon(v) + range(v) sqrt(log(2/alpha)/(2n)).

If the deployed channel A_prime instead satisfies max_k TV(A_prime[:,k],A[:,k]) <= tau, the same bound remains valid after adding tau range(v), provided the observations are iid from A_prime p. TV is one-half the l1 distance.

**Proof.** The expectation of the sample mean under A is v^T Ap. The absolute difference from d^T p is at most ||d-A^T v||_infinity because p is a probability vector. Hoeffding's inequality controls deviation of the bounded iid variables v[Y_i] from their mean by the second term. Apply the triangle inequality. Under drift, the expectation difference introduced in each class is at most range(v) times the total variation distance between the two action laws. Averaging over p bounds the additional bias by tau range(v). QED.

**Use.** This separates an irreducible approximation term, sampling noise, and channel drift. If v minimizes the displayed bound using only A,d,n,alpha and a declared tau, the guarantee still applies because v is independent of the field sample. Optimizing v against the same field data without further argument invalidates this simple proof. Plugging an estimated channel into a zero-drift formula is not covered. Bias-aware linear inverse estimation is established methodology [R3], and concentration is standard [R4].

## Theorem 6. Multiple probes identify a contrast through their joint span

Let E probe conditions have known channels A_e. Suppose the condition is independently assigned with known positive probability rho_e, is logged, and does not change the latent class composition p. The joint condition/action channel is B = vertical_stack(rho_e A_e). The contrast is globally identified exactly when

    d belongs to row(B) = span(union_e row(A_e)).

Equivalently, every h invisible to every probe, A_e h = 0 for all e, must satisfy d^T h = 0. Independent randomization and recording the condition are essential. If condition labels are discarded, the channel becomes sum_e rho_e A_e, which can lose information.

**Proof.** B is column-stochastic. Its null space is the intersection of the null spaces of A_e because all rho_e are positive. Apply Theorem 1 and the fundamental theorem of linear algebra. If condition labels are discarded, their joint categories are merged by a stochastic map, so Theorem 4 applies. QED.

**Counterexample to unlogged variation.** Take two equally probable probes, A_1 = identity_2 and A_2 with its two rows exchanged. Each recorded condition identifies both classes. Their unlogged average has two identical columns (1/2,1/2), identifying no nonconstant contrast. More interface variation alone need not yield more useful information.

**Experimental implication.** A useful probe must resolve a null direction relevant to d. It need not recover all class proportions. Optimizing which probes to run, their sample allocation, and their user cost connects directly to established experimental design and partial monitoring [R1,R4].

## Proposition 7. Continuous cost allocation for fixed probe weights

Suppose independent samples from each condition have fixed positive sizes n_e. Let fixed weights v_e satisfy sum_e A_e^T v_e = d, and let sigma_e^2 = Var_{q_e}(v_e[Y]). The estimator sum_e mean_i v_e[Y_ei] is unbiased with variance sum_e sigma_e^2/n_e. For positive costs c_e and continuous allocation budget sum_e c_e n_e = C, if all sigma_e are positive, this variance is minimized at

    n_e = C (sigma_e/sqrt(c_e)) / sum_j sigma_j sqrt(c_j),
    variance_min = (sum_e sigma_e sqrt(c_e))^2/C.

**Proof.** Unbiasedness and variance follow from the weight identity and independent samples. By Cauchy-Schwarz,

    (sum_e sigma_e sqrt(c_e))^2
      <= (sum_e sigma_e^2/n_e)(sum_e c_e n_e).

Equality holds at the displayed proportional allocation. QED.

This is the familiar optimal allocation calculation, not a new acquisition algorithm. Integer counts, unknown variances, adaptive selection, and data-dependent weights need separate treatment. If some variances are zero, the formula is an infimum allowing zero limiting allocation to those conditions; any required positive minimum count must be handled explicitly.

## Proposition 8. Rectangular uncertainty, finite-sample coverage, and failure states

The existing joint-mass LP is exact relative to its declared rectangular channel set and frequency box, provided every channel column box contains at least one probability vector. The proof in `docs/channel-diagnostic.md` correctly treats zero-mass columns.

Suppose the channel box covers A with probability at least 1-alpha_A and the frequency box covers Ap with probability at least 1-alpha_q. If the finite-class model and fixed d are correct, the LP interval covers d^T p with probability at least 1-alpha_A-alpha_q. Independence of the two confidence events is not required for this union bound. No optional stopping or adaptive use is implied by fixed-sample Clopper-Pearson intervals.

**Proof.** On the intersection of the two coverage events, (p,J=A diag(p)) is feasible. Therefore the minimum cannot exceed d^T p and the maximum cannot be smaller. The intersection has probability at least 1-alpha_A-alpha_q by the union bound. QED.

An infeasible LP must return a failure state or a model-consistency warning, not an artificially narrow confidence interval or a confident decision. An invalid latent-class taxonomy is not repaired by conservative numerical intervals. Propagating finite-sample uncertainty through a partial-identification LP is explicitly covered by Finkelstein et al. [R2], including their supplementary Proposition 1.

### Uncertainty in the outcome contrast

If d is only known to lie in a coordinate rectangle [d_lower,d_upper] independently of the other uncertainty sets, then sharp overall lower and upper bounds are obtained by minimizing d_lower^T p and maximizing d_upper^T p over the existing feasible set. Nonnegativity of p justifies choosing each coordinate endpoint. If this rectangle is a confidence set with error alpha_d, the same union-bound argument gives total coverage at least 1-alpha_A-alpha_q-alpha_d. Correlation between outcome and channel parameters can make these rectangular bounds conservative.

### Missing intent classes

Do not merely widen a contrast interval calculated from contaminated field frequencies and declare protection against omitted classes. Those frequencies may no longer satisfy the original model. An explicit contamination extension is available when an upper bound eta_bar on unknown-class mass is substantively defensible. Use known-class masses z >= 0, an unknown action-mass vector u >= 0, and eta in [0,eta_bar]. Enforce

    sum_k z_k = 1-eta;   sum_a u_a = eta;
    q_lower <= sum_k J[:,k] + u <= q_upper;
    sum_a J[a,k] = z_k;
    L[a,k] z_k <= J[a,k] <= U[a,k] z_k.

If unknown-class contrasts lie in [-D,D], introduce t with -D eta <= t <= D eta and optimize d^T z+t. These are linear constraints. Every allowed contaminated model maps to feasible masses. Conversely, normalize each nonzero known-class column as before and normalize u/eta when eta > 0; an unknown class with contrast t/eta realizes the residual. Thus this is sharp for the broad contamination model, not for a model with further unknown-class structure. The current implementation does not yet expose this extension.

## Findings from the code audit

- `identification.py` correctly validates channel-column feasibility, input finiteness, and solver witnesses. The fixed 1e-8 decision threshold is a numerical tolerance, not a substantively meaningful product-effect threshold.
- `probability_intervals` correctly uses a Bonferroni split over multinomial coordinates, and `channel_intervals` splits over classes. Callers must still allocate alpha between calibration, field frequency, and any uncertain outcomes.
- A fixed-sample binomial interval assumes iid trials with a common probability. Pooling a balanced, deterministic set of distinct prompts is not automatically iid multinomial sampling from a random prompt population. Options include random sampling from a prespecified prompt distribution, separate stratum intervals with declared weights, or a concentration argument valid for the actual stratified design. Repeated generations of identical synthetic personas are not independent human respondents.
- The code compares scalar contrast endpoints, not financial return. A rollout decision also requires costs, capacity, risk, and an appropriate value measure.
- Changes in unknown A and changes in p can be observationally confounded. A real model update experiment should retain a common reference panel and independent outcome measurements, rather than interpret every change in q as demand drift.

## Proposed manuscript placement and novelty boundary

Put Theorems 1, 2, and 3 in the main theory section, with one worked witness. Put Theorems 4 through 6, the allocation calculation, and uncertainty extensions in an appendix unless empirical experiments directly depend on them. Explain that the application-specific object and empirical study are the contribution being developed. Do not advertise routine linear algebra as a new learning theory.

A stronger paper would establish, on properly documented model experiments, the empirical tradeoff among task value, decision ambiguity, and the cost of a targeted additional channel. Real customer validation requires actual consenting people and an appropriate study protocol. Simulated agents can test instrument sensitivity and generate hypotheses, but cannot substitute for human evidence or be concealed as respondents.

## Primary-source review ledger

[R1] Kirschner, J., Lattimore, T., and Krause, A. (2023). *Linear Partial Monitoring for Sequential Decision Making: Algorithms, Regret Bounds and Applications.* JMLR 24(346), 1-45. https://jmlr.org/papers/volume24/22-1248/22-1248.pdf. Inspected primary full text, model, observability definitions, and related work. It already connects decision contrasts to feedback spans and experimental information costs.

[R2] Finkelstein, N., Adams, R., Saria, S., and Shpitser, I. (2021). *Partial Identifiability in Discrete Data With Measurement Error.* UAI, PMLR 161, 1798-1808. https://proceedings.mlr.press/v161/finkelstein21b.html. Supplement: https://proceedings.mlr.press/v161/finkelstein21b/finkelstein21b-supp.pdf. Inspected primary abstract and supplement Section 1, Proposition 1, and its proof. LP bounds and their confidence-set propagation are established, not new here.

[R3] Donoho, D. L. (1994). *Statistical Estimation and Optimal Recovery.* Annals of Statistics 22(1), 238-270. https://doi.org/10.1214/aos/1176325367. Author-hosted copy: https://web.stanford.edu/dept/statistics/cgi-bin/donoho/wp-content/uploads/2018/08/SEOR.pdf. Primary abstract and introductory formulation screened. Provides the relevant inverse-estimation and optimal-recovery antecedent. No claim that all details of our categorical setup are verbatim instances of its Gaussian theorem.

[R4] Lattimore, T., and Szepesvari, C. (2020). *Bandit Algorithms.* Cambridge University Press. Author-hosted text: https://tor-lattimore.com/downloads/book/book.pdf. Chapters 5, 13-15, and 21 provide the concentration, lower-bound, and experimental-design context. The elementary lower bounds here are proved directly rather than attributed as new.

[R5] Blackwell, D. (1953). *Equivalent Comparisons of Experiments.* Annals of Mathematical Statistics 24(2), 265-272. https://doi.org/10.1214/aoms/1177729032. Bibliographic record and primary-linked abstract checked; publisher body access did not render. The coarsening implication used here is proved directly and does not require the full equivalence theorem.

## Proposition 9. Calibration with a fixed heterogeneous prompt panel

A fixed balanced prompt panel can still support a conservative calibration interval without pretending that all response trials have the same categorical distribution. For one class k, let Y_1,...,Y_n be independent agent responses to a prespecified panel. Write P(Y_i=a) = A_ia and define the panel-average channel A_bar[a,k] = (1/n) sum_i A_ia. For m response categories and K calibrated classes, define empirical frequencies A_hat and

    radius_k = sqrt(log(2 m K / alpha_A)/(2 n_k)).

Then, simultaneously over all actions and classes, |A_hat[a,k]-A_bar[a,k]| <= radius_k with probability at least 1-alpha_A. Clip interval endpoints to [0,1]. Different response probabilities across prompts are permitted. No unknown response is silently discarded: a failed or refused response must either be its own declared action category, or be handled by an explicit missing-data model.

**Proof.** For any fixed action and class, the independent indicators 1{Y_i=a} lie in [0,1]. The version of Hoeffding's inequality for independent, not necessarily identically distributed variables gives a two-sided error probability at most 2 exp(-2 n_k radius_k^2) = alpha_A/(mK). A union bound over mK coordinates proves the result. QED.

This estimates the fixed-panel average channel, not an arbitrary deployment channel. Interpreting it as the deployed channel requires a matched prompt composition or an explicit transport bound. Dependence across repeated API calls, common backend randomness, or adaptive prompt selection is not covered by this elementary calculation. A separately randomized sample of prompts from a prespecified distribution can instead target that distribution's channel under iid assumptions. This is a standard concentration alternative to the exact-binomial construction, not a new calibration method.
