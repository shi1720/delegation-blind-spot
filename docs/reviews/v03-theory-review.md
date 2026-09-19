# Internal skeptical technical review, v0.3 planning

Date: 20 September 2026. This is an internal agent-assisted critique, not an actual TMLR or JMLR peer review, editorial decision, or claim of reviewer affiliation. Reviewed the current main manuscript, full appendix, receipt results, `certificates.py`, `identification.py`, and the recorded experiment design.

## Recommendation and scores

**Revise before submission.** The current manuscript is a careful technical preprint, but the strongest scientific takeaway is still insufficiently isolated from the properties of the chosen conservative procedure.

| Dimension | Score, 1 weak to 5 strong | Reason |
|---|---:|---|
| Mathematical correctness | 4 | Proofs are correct under their explicit finite-channel assumptions; numerical and deployment assumptions remain consequential. |
| Original contribution | 2 | Identification, the LP, duality, regret calculations, and confidence propagation are established tools. The measurement framing and released instrument are the main contribution. |
| Empirical evidence | 2 | Auditable model calls, but one synthetic task family; all primary intervals abstain; receipt extraction is direct class reporting. |
| Clarity | 4 | Strong disclosure of synthetic scope and uncertainty. The title and overall narrative still risk suggesting more customer-learning evidence than exists. |

These numerical scores are our internal rubric, not official venue scales. TMLR does not require novelty of a method: its official criteria emphasize supported claims and interest to its audience. It also distinguishes an informative robustness study from merely rerunning familiar ideas. I would request the precision/identifiability analysis below to establish an actionable lesson, rather than reject solely for insufficient novelty. See the [TMLR acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html) and [editorial policies](https://jmlr.org/tmlr/editorial-policies.html), checked 20 September 2026.

JMLR explicitly asks whether work provides a significant, technically correct contribution. On the current evidence I would not recommend JMLR submission. This is an assessment of fit, not ineligibility by rule. See its [reviewer guidelines](https://jmlr.org/reviewer-guide.html).

## Mathematical audit

No blocking algebraic error was identified in the nine appendix results. Global versus local identification is correctly distinguished. The factor of two in the hidden-width dual identity is correct. Exact-observation minimax regret properly minimizes the largest endpoint loss. The rectangular joint-mass transformation handles zero-mass columns correctly. Outcome-box endpoints use nonnegative population masses correctly. The finite-sample certificate chooses weights without field data and recomputes the actual residual, preserving its bias bound even if numerical optimization is imperfect. Drift uses total variation with the correct range factor.

The previous nearly singular exact-width issue has been corrected through an orthonormal row-space basis and an explicit numerical rank tolerance. Structural rank of an estimated channel must still not be treated as population rank. Solver feasibility checks do not make floating-point extrema mathematically exact; do not claim certified machine-precision sharpness or ignore numerical tolerance near a decision boundary. No displayed empirical decision was found to depend on that boundary issue.

## Critical evidence issues

1. **Abstention does not establish a delegation blind spot.** Every primary diagnostic interval includes zero, including the optimum control. The paper properly admits this, but its central empirical result could be a sample-budget and Bonferroni-conservatism effect even when the population channel is fully identifying. That distinction needs a direct experiment, not another caveat.
2. **Observed full rank and exact rank deficiency are different from weak identification.** In an unrestricted stochastic model with at least as many actions as classes, full-rank channels occur arbitrarily close to pooled channels. Finite noisy calibration cannot generally establish an exact structural rank deficiency merely because a confidence interval is wide. Small singular values can produce large sampling sensitivity while the infinite-data contrast is uniquely identified.
3. **Receipt extraction supplies the missing label.** With four uniquely dominant weight profiles, the receipt is a direct class report. Its added information is legitimate but largely stipulated by the benchmark. A deterministic parser requires no language model. A 50% width reduction from this comparison is not evidence of a novel elicitation method, hidden-preference inference, privacy protection, or customer relevance.
4. **Receipt follow-up is exploratory.** It was selected after viewing the primary results and reuses original field draws and actions. The manuscript now correctly avoids conditional post-selection or family-wise guarantees. Preserve that wording; a freeze before new calls is not external preregistration or a fresh independent confirmatory replication.
5. **The provider's sampling model is assumed, not verified.** Seventeen temporally clustered transport failures are retained, which is preferable to deleting them, but retaining them as a category does not prove a stationary iid channel. The current mathematical guarantees are conditional model statements rather than verified finite-sample operational coverage. Sensitivity to omission or contamination would strengthen empirical interpretation without changing the frozen analysis.

## Smallest rigorous unpaid addition

Run a controlled multinomial experiment with four classes and channels

    A_eta = (1-eta) (1/4) 1 1^T + eta I,
    eta in {0, .01, .03, .1, .3, 1}.

Its spectrum is one eigenvalue 1 and three eigenvalues eta. At eta=0 the channel is exactly pooled and the global hidden width is max(d)-min(d). At every eta>0 it is full rank and structural width is zero. Its inverse nevertheless amplifies the informative subspace by 1/eta. This cleanly separates nonidentification from poor finite-sample precision, using an analytic truth that another fitted LLM channel cannot provide.

For fixed d and prespecified population mixtures, compare: exact A and q; exact A with sampled field-frequency uncertainty; sampled channel calibration with exact q; and joint calibration plus field uncertainty. Vary sample budgets, regenerate every calibration and field sample independently per replicate, and retain infeasible intervals in every denominator. Report coverage with Monte Carlo standard errors, decision resolution, wrong resolutions, and interval-width quantiles. The fully revealing endpoint is a perfect class parser; the pooled endpoint is a structural negative control. Do not count these as new model responses or customers.

An optional overlay using the already observed model-channel estimates can illustrate conditioning but must be explicitly conditional on plug-in channels. It cannot convert an estimate into population truth. This additional analysis will not create a new general theorem, but can turn the package into an informative study of where a standard method is useful and where it is vacuous.

## Further changes that would strengthen rather than block

- Add a simpler valid baseline for the known-channel simulation, such as the released linear certificate, to quantify how much width comes from rectangular confidence sets rather than unavoidable uncertainty.
- Compress repeated theorem exposition between main and appendix. Keep the problem-specific interpretation in the main text and full proofs in the appendix.
- Make the known finite-bank value contrast and optimal future selection assumption explicit in every main results caption where space allows.
- Present a table distinguishing exact structural ambiguity, weak identification, calibration error, finite field data, and possible transport failure.
- Explain what an actual product team would need to measure to obtain d and validate the latent taxonomy. The current experiment treats these as supplied inputs.

## Submission eligibility and responsibility

The present named, generic two-column preprint is not a submission-ready TMLR file. TMLR requires an anonymized submission and its official style/template; public preprints are permitted but do not remove anonymization obligations. See the [author guide](https://jmlr.org/tmlr/author-guide.html) and the editorial policies linked above. Eligibility also depends on author quota, non-overlap with archival submissions, and the author's truthful declarations; this review did not verify those account-level facts. Human author review and responsibility cannot be replaced by these internal agent critiques. No simulated persona may be represented as a consenting human participant.

A reasonable next target is a technically bounded TMLR measurement/robustness study after the additional analysis, followed by genuine author review and venue formatting. JMLR currently lacks sufficient demonstrated technical contribution and empirical breadth. Neither assessment predicts acceptance.
