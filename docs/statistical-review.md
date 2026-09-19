# Independent statistical review of benchmark v2

Reviewed `experiments/v2/benchmark.py`, `prepare.py`, and `analyze.py` on 19 September 2026 while development was in progress. This is a code and assumptions review, not external peer review. It does not certify real customer validity.

## Overall assessment

The revised analyzer correctly separates field cohorts, retains failures, uses known synthetic class contrasts for its primary analysis, and accounts for estimated outcome uncertainty in a secondary analysis. The main remaining risks concern interpretation, multiple comparisons, and calibration transport rather than an identified algebraic error.

An early reviewed revision pooled positive, negative, and near cohorts while reading a nonexistent top-level target. The current revision separates `(domain,cohort)` and reads the corresponding target. This issue was communicated and fixed before the frozen main run.

## What the primary target is

The outcome bank is a frozen finite collection of synthetic menus. Each class contrast d_k is exactly the average difference between the optimal synthetic utility after capacity investment and after flexibility investment over that bank. The primary target for a cohort is d^T p, where p is the cohort's declared generating distribution. It is not the realized average of the finite field sample's hidden class labels, and it is not human satisfaction, willingness to pay, or revenue.

Passing these d values as known analyst inputs is permissible for this benchmark, provided it is explicit. It means the primary procedure does not learn customer-value contrasts. The latent field composition p remains unavailable to the estimator and is supplied only for evaluation. The bank is independent of calibration and field generation.

## Sampling and contextual categories

Menus, regimes, option order, and field class labels are independently generated from prespecified distributions using separate streams. For each calibration class, the iid repeated-experiment interpretation includes menu and response randomness. Under a stable response policy with independent calls, categorical response counts have the multinomial interpretation required by the Clopper-Pearson construction. The guarantee is over repetitions of that experiment, including task generation. It is not a confidence assertion conditional on the exact frozen heterogeneous task list alone.

The contextual schema uses 15 categories: five action/failure states crossed with three randomly generated regimes. Because regimes are drawn independently of class from the same distribution in calibration and field, the joint regime/action channel also satisfies q = Ap. This remains valid even though regimes affect choices. It would not remain valid if calibration and field used different regime mixtures without adjustment.

Randomization of prompts does not prove API response stability. Provider updates, temporal dependence, changing refusal behavior, or concurrency-dependent failures can alter the channel. Interleaving tasks helps avoid simple ordering confounds but is not a proof of exchangeability. Record timestamps, returned model identifiers, request configuration, and errors; state stability as an assumption.

## Confidence levels and multiple decisions

With the current default error budgets alpha_A = .02 and alpha_q = .02, the primary LP interval has coverage **at least 96% for each prespecified domain/cohort/schema/model contrast**, conditional on correct model assumptions and known d. The secondary analysis adds alpha_d = .01, giving at least 95% coverage for each such contrast. Calling the primary a conservative 95% interval is technically safe, but reporting the actual 96% lower bound and the budgets is clearer.

The code's calibration function already splits alpha_A over classes and action coordinates, so no additional factor of four or five belongs in that per-contrast union bound. The field function splits alpha_q over its categories. The outcome Hoeffding radius uses a Bonferroni split over four class contrasts. Coupling the four outcome values through common menus does not invalidate the union bound.

These are **marginal per-contrast guarantees, not joint 95% coverage of every reported interval**. Cohorts share calibration, schemas use the same records, and systems can share tasks; dependence does not justify ignoring multiplicity. For D domains, M systems, S schemas, and C cohorts with all cells present, a simple family-wise primary guarantee is at least

    1 - D M S alpha_A - D M S C alpha_q,

truncated below at zero. This bound reuses each calibration event across cohorts. For secondary outcomes shared across systems and schemas, additionally subtract D alpha_d. The bound may be vacuous at current budgets. If a simultaneous claim is required, preallocate the total error across these unique events before execution. Otherwise prominently retain the per-contrast wording and avoid selection-based claims such as “the best-looking interval proves the hypothesis.”

The count of intervals containing truth across a handful of dependent benchmark cells is a diagnostic, not a repeated-sampling coverage estimate. A coverage experiment needs independent complete repetitions of calibration, field generation, and outcome sampling at a declared target or target distribution. The 200 bootstrap resamples are not 200 independent experiments.

## Estimated outcomes and bootstrap baseline

Secondary contrast observations are sampled with replacement from the fixed bank. Conditional on that bank, each class's observations are iid bounded values in [-1,1]. The radius sqrt(2 log(8/alpha_d)/n) is a valid two-sided Hoeffding plus Bonferroni bound over four classes. The LP evaluates the lower coordinate vector for its lower endpoint and upper coordinate vector for its upper endpoint; this is valid because class masses are nonnegative. The bound can be wide, but width is not a correctness error. Do not replace it with a narrower interval after seeing the result without documenting an exploratory change.

The percentile bootstrap holds the estimated channel and known d fixed, and resamples only empirical field action frequencies. It omits calibration error and can also behave poorly under boundary or nonunique inverse solutions. The analyzer correctly labels it as having no finite-sample coverage guarantee. It is a deliberately limited baseline, not a “95% confidence interval” with proven conditional validity. Two hundred resamples give a coarse descriptive percentile estimate. Its failures cannot by themselves establish that all bootstrap methods fail.

## Failure handling and non-identification

Refusal, malformed output, and HTTP failure are retained as a fifth observable category, with context if applicable. Every prepared task must have a record, and duplicates or missing records fail analysis. This prevents a simple success-only selection bias. Operational utility assigns failure zero, which is an explicit benchmark convention, not a measured customer loss. Transport requires calibration and field failures to arise under the same relevant operating conditions.

Empirical singular values describe the sampled matrix. Finite sampling can make an empirically full-rank channel even when its population columns coincide. They do not establish identification or a stable inverse. Likewise, the constrained minimum-distance baseline can return a point from a nonunique or weakly identified solution set. Its existence is not evidence that the underlying composition is identified.

## Readiness checks communicated to the implementer

- Reject an empty outcome matrix before computing means or a Hoeffding radius.
- Correct the stale comment implying the primary d is estimated; only the secondary outcome is estimated.
- Include and verify a hash for `evaluation-truth.json`, in addition to task and outcome hashes, to make the evaluation target tamper-evident.
- Preserve known synthetic outcome disclosure in every table and figure caption.
- Label confidence guarantees per contrast and the bootstrap as an unguaranteed baseline.
- Preserve failure categories in all denominators and display failure rates alongside competence.

## Recommended manuscript wording

“Each primary interval propagates calibration and field-frequency uncertainty with error budgets 0.02 and 0.02. Under a stable channel and the stated randomized sampling design, its marginal coverage is at least 96% for the prespecified synthetic contrast. These are not simultaneous guarantees across the reported conditions. Class-level contrasts are exactly evaluated on a frozen synthetic menu bank. A secondary analysis also propagates uncertainty from a separate sample of synthetic outcomes. No human participants or customer outcomes are represented by these experiments.”

## Main-manuscript audit after live execution

The three main theorems match the complete appendix arguments. The linear certificate's approximation, sampling, and total-variation drift terms match the implemented LP. The reference to best attainable future utility correctly discloses that future choices are optimized by the utility rule, not observed from the tested agent. No mathematical theorem error was identified in this review.

The following editorial precision points were sent to the manuscript author: distinguish 4,800 model requests from 2,400 unique shared tasks; state the channel-box simplex feasibility assumptions in the main LP; describe the operational regret as a difference of synthetic utilities rather than imply division by optimal utility; and define the binary value-regret loss explicitly if space permits. Main-text edits remain with the author.

The coarsening theorem concerns exact observation models or nested feasible sets. The empirical five-category and fifteen-category procedures construct their Bonferroni confidence boxes separately. Those finite-sample feasible sets need not be nested, so the contextual interval can be wider even though exact contextual observations are at least as informative. This is confidence-set conservatism, not a contradiction of the theorem or proof that recording context harms information.

The frozen plan records SHA-256 hashes of raw file bytes; prepared manifests record canonicalized JSON digests. Both conventions were checked against the task and outcome files and are internally consistent. They should not be compared as though they use the same serialization.

## Explicit-preference receipt follow-up review

Reviewed `prepare_receipts.py`, `analyze_receipts.py`, and the frozen receipt plan before receipt results were available. No blocking implementation error was found in the inspected subset selection, paired-ID verification, failure retention, or removal of placeholder utility metrics. The source task and target hashes are checked. The comparison has equal selected task counts and calibration/field sizes, not equal token cost, latency, privacy loss, or human burden.

The 1,200 requests per model repeat only 12 distinct prompts: four supplied profiles in each of three framings. Within a class and framing, repeated responses can estimate a stable response distribution if calls are independent and stationary. They are not 1,200 independent customers or diverse preference-elicitation tasks. The field class labels are the reused original random draws, not newly recruited people. Finite-sample statements rely on the repeated-experiment distribution of those original class draws and the current response calls; conditioning on the exact frozen class composition changes that interpretation.

Because each profile has a different uniquely dominant attribute, a correct receipt is effectively a direct observation of the latent class in this benchmark. A deterministic argmax over already supplied weights would produce the same receipt with no language model. The extension can demonstrate the informational value of retaining explicit preference information relative to a behavioral proxy. It cannot demonstrate discovery of unexpressed preferences, that an LLM is necessary for the receipt, or that this transmission protects privacy. An offline perfect-receipt reference is useful for distinguishing extraction reliability from the value of the extra information.

The receipt prompt changes the task from choosing an option to extracting an explicit weight maximum. Receipts explicitly set reasoning effort `none`, whereas original requests omit it; the official model pages for both snapshots list `none` as the default, so this serialization difference is not evidence of a changed effective reasoning level. The changed prompts and objectives still make this a comparison of task-and-measurement configurations, not a controlled change to logging alone. This should remain visible rather than be presented as a telemetry-only treatment effect. Official model references checked: https://developers.openai.com/api/docs/models/gpt-5.4-mini and https://developers.openai.com/api/docs/models/gpt-5.4-nano .

The follow-up was selected after observing unresolved primary results. The prospective freeze before new receipt calls is valuable but does not retroactively make this a confirmatory comparison selected before primary outcomes. The reused action subset and field draws carry that history. The existing 96% statement is a fixed-design marginal theorem under the declared model; it is not a selective guarantee conditional on choosing this follow-up after inspecting the original results. Report exploratory descriptive resolution counts, do not interpret them as a significance test, and do not claim joint protection over all reported decisions. A new independent replication with the complete receipt design declared before any outcomes would support stronger confirmatory interpretation.

Lexicographic subset selection depends only on task IDs and declared strata, not individual response correctness. The subset is therefore transparent and reproducible. This reduces a direct cherry-picking risk but does not remove the broader post-selection caveat. Retaining the original execution order does not prove independent receipt failures; returned model IDs, timestamps, and infrastructure-error clustering should be audited as in the primary run.

## Bibliography and primary results check

Primary publisher or repository metadata was rechecked for Lipton et al. (2018), Angelopoulos et al. (2023), Cherep et al. (2025/2026 revision), Kops and Tsakas (2026), Zrnic and Candes (2024), and Kraft and Larsen (2026). The bibliography's authors, titles, and cited preprint years match the checked records. A publication-quality improvement is to cite the published Prediction-Powered Inference article as *Science* 382(6671), 669-674 (2023), DOI 10.1126/science.adi6000; retaining its arXiv link as a public copy is appropriate. Existing mathematical references were checked earlier in this review.

The generated primary results were recomputed from the two `analysis.json` files: 1,440 field tasks per model, maximizing-choice rates 73.1944% and 55.6944%, mean synthetic regrets 0.01862847 and 0.05728125, and field failure rates 0.34722% and 0.27778%. The naive sign-error counts are 2 and 4 of 18 conditions; fixed-channel bootstrap inclusion counts are 14 and 16; all primary diagnostic conditions are unresolved. These agree with the generated manuscript text. The manuscript correctly treats these as descriptive counts and separates transport failures from reasoning errors.
