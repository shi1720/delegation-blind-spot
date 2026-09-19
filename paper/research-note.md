# The Delegation Blind Spot
## Learning What People Want When Agents Make the Choices

Shivam Gupta | Research note 0.1 | 19 September 2026

### Abstract

An agent can serve a customer correctly while leaving a product team unable to distinguish that customer from someone who would benefit from a different future product. This note separates execution quality from the information that execution preserves for product decisions. We model delegated actions as a channel from customer intent to observable behavior and examine the range of product outcomes consistent with that channel. A decision can remain learnable even when customer preferences cannot be fully recovered. Conversely, collecting more of the same behavior cannot resolve an unidentified decision. We implement a diagnostic that returns outcome bounds and explicit, observationally compatible customer populations. A separate synthetic pilot examines established audit estimators under changes in the relationship between telemetry and outcomes. The note contributes a research framing, reproducible instruments, and a falsifiable evaluation plan. Its mathematical tools have established antecedents. It does not yet establish an original algorithm or an empirical result about human customers.

### 1. The question after a successful transaction

Imagine two customers asking their agents to book the same hotel. One values quiet; the other values proximity to a meeting. At today's prices, the same hotel is best for both. Both agents complete the booking perfectly. The hotel platform records two indistinguishable successes.

The platform now has a different decision: invest in soundproofing or improve transport links. The completed bookings do not necessarily reveal which investment would help. The missing information is not an execution error. It is a distinction that was irrelevant to the present choice but becomes relevant to the next product decision.

This problem can arise with human choices too. Delegation is a plausible mechanism that could change which distinctions remain visible, especially when agents bypass browsing, deliberation, and comparison. Whether it does so in practice is an empirical question. More clicks would not automatically solve it, and fewer clicks would not automatically prove it.

The central research question is therefore decision-specific: which differences in customer value remain recoverable from the behavior produced by a particular agent, interface, and task?

### Three questions worth testing

Can a more successful agent make the product less informative about a future customer need? Can a model update look like a change in market demand? Can a company learn enough to choose its next investment without collecting a customer's complete private preferences?

<!-- pagebreak -->

### 2. Define the decision before interpreting the data

Consider K declared customer-intent classes with population proportions p. For a fixed task, interface, and agent configuration, let A contain the conditional probabilities of the observable actions: column k describes the behavior of class k. The company observes action frequencies q.

    q = A p,     p >= 0,     sum(p) = 1

For two proposed product variants, let d[k] be the difference in customer outcome for class k. The target is the population contrast Delta, not an agent's preference for a page or the number of successful clicks.

    Delta = d^T p

The outcome could be independently measured task value, a stated willingness to pay, or a subsequent experience rating. Those are different estimands. A production study must specify one and defend its measurement. A company also needs costs and commercial constraints before treating customer value as an investment recommendation.

### Proposition 1. Preference recovery is stronger than decision recovery

For known A, the contrast d^T p is identified for every feasible population if and only if d is in the row space of A. Here A has columns summing to one, so its row space already includes the all-ones vector. This is a standard linear identification fact, closely related to observability in partial monitoring [1].

Proof. If d = A^T v, then d^T p = v^T q and depends only on observations. Conversely, if d is outside the row space, there is an h in the null space of A with d^T h nonzero. Column normalization implies sum(h) = 0. Choose an interior population p and sufficiently small positive t. Both p + th and p - th are probability vectors and produce the same q, but their contrasts differ. Thus identification fails for at least one feasible q. At a particular boundary q, the simplex constraints can still identify a contrast even when the global condition fails.

The practical implication is narrower than “infer the customer.” A company may need only a specific contrast. Recovering every preference can be unnecessary, expensive, and intrusive.

### Three separate sources of uncertainty

Sampling uncertainty concerns how accurately finite logs estimate q. Identification ambiguity concerns whether even exact q determines Delta. Channel uncertainty concerns whether calibration accurately describes the agent currently serving customers. More traffic reduces the first source under suitable sampling assumptions. It does not automatically reduce the other two.

<!-- pagebreak -->

### 3. Return the competing explanations

For a declared channel A and observed q, define the compatible population set and the decision interval:

    P(A,q) = {p : p >= 0, sum(p) = 1, A p = q}
    L = min over P(A,q) of d^T p
    U = max over P(A,q) of d^T p

If L is positive, variant 1 has greater value throughout this model. If U is negative, variant 0 does. If the interval crosses zero, the diagnostic returns two witness populations that justify opposite decisions. Zero as an endpoint can mean a tie rather than a strict reversal. Bounds are more informative than forcing a recommendation from an unidentified target.

### A transparent example

Take two intent classes. Both produce action frequencies (0.8, 0.2), so each column of A is identical. Let the proposed change improve value by 0.5 for the second class and reduce it by 0.3 for the first. Every possible population composition produces the same logs. The compatible contrast is therefore [-0.3, 0.5]. An all-first-class population and an all-second-class population are explicit witnesses. Infinite traffic would estimate (0.8, 0.2) exactly and leave this interval unchanged.

The implementation also checks a revealing channel whose columns are (0.9, 0.1) and (0.1, 0.9). At population proportions (0.6, 0.4), exact calibration identifies a contrast of 0.02. Allowing each channel entry to vary by 0.05 expands the compatible interval to [-0.03, 0.07]. The exact-calibration decision is not robust to that uncertainty. These numbers are constructed diagnostic examples, not model or customer observations.

### Proposition 2. Channel uncertainty can be handled without guessing a channel

Suppose each channel entry lies within a supplied interval, subject to each column summing to one. Introduce joint masses J[a,k] = A[a,k] p[k]. Enforce the linear constraints:

    sum_a J[a,k] = p[k]
    channel_lower[a,k] p[k] <= J[a,k] <= channel_upper[a,k] p[k]
    frequency_lower[a] <= sum_k J[a,k] <= frequency_upper[a]

Minimizing and maximizing d^T p is a linear program. Every admissible (A,p) maps to feasible (J,p). Conversely, divide each nonzero-mass column of J by p[k] to recover A; a zero-mass column can use any valid channel column. Thus the bounds are attainable within the supplied rectangular model. This uses established partial-identification ideas [2], not a new optimization principle. Correlated channel uncertainty and uncertainty in d require additional treatment.

<!-- pagebreak -->

### 4. What the exploratory pilot actually found

Before designing a new estimator, we tested established ones. The pilot uses fixed synthetic pools of 4,000 records and independent Bernoulli audits. Five scenarios, four expected audit budgets, and five policies each receive 1,000 audit replicates: 100,000 estimator evaluations. Expected audit cost is matched; realized label counts vary and are recorded. These are not 100,000 people or model calls.

The estimator combines a proxy prediction with an inverse-probability correction from audited outcomes. Prediction-powered and active inference already study this strategy [3,4]. We compare uniform sampling, historical-error active sampling, a fixed mixture, and a robust linear-path adaptation of Li et al. [5]. An oracle uses otherwise unavailable residuals and is labeled separately.

In the strong hidden-shift construction, the observable records remain fixed while the actual outcome contrast changes from 0.0065 to -0.104. The proxy contrast stays at 0.0105. This deliberately creates a mismatch. It does not show that agents caused one in the wild.

At an expected budget of 100 audits, historical active sampling has RMSE 0.0663 and 88.9% coverage for its nominal 95% Wald interval. Uniform sampling gives 0.0577 and 93.9%; the robust-path adaptation gives 0.0558 and 93.4%. The coverage Monte Carlo standard errors are approximately 1.0, 0.8, and 0.8 percentage points respectively. These comparisons concern this fixed construction, not universal method rankings. All implementations retain unbiased point estimation under the stated audit design. Poor finite-sample coverage is a separate issue.

![Synthetic pilot results](../results/pilot-v1/pilot-overview.png)

Figure 1. Synthetic pilot: errors and approximate interval coverage under aligned, hidden-shift, and visible-control scenarios. Panels have different error scales. The oracle uses privileged information. The separate conservative Bernstein intervals cover in all recorded replicates but are often too wide to guide a decision.

<!-- pagebreak -->

### 5. From an illustration to a defensible contribution

The next experiment must test a relationship between delegated behavior and independently meaningful outcomes. Merely generating another matrix with identical columns cannot establish that relationship.

### Stage A. Validate the instrument

The repository includes 216 constructed requests spanning travel, cloud services, and workspace subscriptions. Each has two declared intent profiles, two menus, all six option orders, and three repetitions. The utility rules are explicit and the underlying mathematical structure is shared across domains. This is an engineering validation set, not evidence of generalization across three real markets.

One menu makes the same option optimal for both profiles. The other makes their optimal choices differ. Known optimal, uniform-random, and always-balanced controls establish expected behavior. The optimal control illustrates that perfect current choice can coexist with different levels of information about intent. Actual language-model responses remain uncollected. The API runner stores requests, raw responses, returned model identifiers, token usage, failures, and source hashes. A prepared request is never counted as a completed experiment.

### Stage B. Test calibration and transport

Freeze model versions, prompts, task generation, sample sizes, and analysis before the main run. Calibrate action channels on one sample, estimate field frequencies on a separate sample, and evaluate on held-out customer-outcome labels. Compare action-only inference, uniform outcome audits, historical active sampling, robust sampling, and the decision-specific diagnostic. Include agent-version changes, interface changes, absent intent classes, and unchanged-agent controls.

Primary outcomes should be decision error, realized value lost by a wrong decision, uncertainty coverage, and total measurement cost. Task success and human burden must be reported alongside them. An uncertainty method that avoids errors by always refusing to decide may be honest but commercially unhelpful. Evaluate the tradeoff explicitly.

### Stage C. Establish human relevance

With appropriate ethics review or a documented determination, recruit consenting participants for tasks with consequential tradeoffs. Elicit private preferences before delegation and assess outcomes independently afterward. Separate stated preferences, actual choices, and satisfaction rather than substituting one for another. Randomize assistance conditions where feasible. Determine sample size from a declared minimum relevant effect and pilot variance, not a convenient round number. Do not expose private agent conversations merely to improve a company's analytics.

### The bar for the main paper

A credible contribution would show when existing product telemetry supports the wrong investment conclusion, whether the diagnostic catches that failure under realistic calibration error, and what limited additional feedback fixes it at acceptable cost. A new name, an LP, or a synthetic reversal alone does not meet that bar.

<!-- pagebreak -->

### 6. Product implications and competing explanations

The unit of validation should include the agent configuration. If the same customers generate different actions after a model update, an ordinary dashboard may attribute the change to demand. Conversely, stable action frequencies do not establish stable preferences. Both claims require validation beyond a plausible story.

A useful product-learning report would declare the decision under consideration, the target outcome, the calibrated agent/interface configuration, the outcome interval, the competing populations, and the extra observation needed to resolve the disagreement. That report is a proposed operational artifact, not a proven standard.

Feedback can be designed around the disagreement. If two compatible populations differ only in the value of flexibility, asking about flexibility may be more useful than collecting a broad personal profile. Choosing that question efficiently remains an experimental-design problem with substantial existing literature. Questions can also influence preferences and participation, so responses are not automatically unbiased labels.

An agent's explanation is another measurement channel, not privileged access to customer truth. It may help, but must be calibrated against independently elicited preferences or outcomes. Likewise, a user's override of an agent is selected behavior: a quiet user need not be a satisfied one.

### Why ordinary A/B testing is not invalidated

Randomization can identify effects on outcomes that are actually measured under the experiment's assumptions. The concern here is the substitution of agent activity for unmeasured customer value. If a company directly measures the relevant customer outcome in a sound experiment, this particular information gap may already be resolved. Retention, refunds, and support contacts may supply useful signals, although each has its own timing and selection issues.

### Closest work and the remaining gap

Partial monitoring connects learnability to the observation structure [1]. Measurement-error research constructs bounds on partially identified quantities [2]. Prediction-powered inference and active sampling address efficient acquisition of real labels [3-5]. Choice via AI studies rationalization and identification when an agent can interpret menus differently [6]. ABxLab experimentally studies agent responses to product attributes, interfaces, and stated user profiles [7].

Our proposed study connects these concerns to the value of a specific future product decision under a calibrated and potentially changing agent channel. That connection is a research direction, not a completed novelty claim. A fuller review of delegated preference transmission and adaptive experimentation remains necessary.

### Limitations

The current model assumes a finite known intent taxonomy, a meaningful and known contrast d, stable within-class behavior, and usable calibration. All can fail. No human study or live model experiment is reported here. The pilot is exploratory, the proofs have not received independent expert review, and no new statistical estimator is claimed. Nothing in this note establishes venue readiness or an industry-wide effect.

<!-- pagebreak -->

### References

[1] Kirschner, J., Lattimore, T., and Krause, A. (2023). Linear Partial Monitoring for Sequential Decision Making: Algorithms, Regret Bounds and Applications. Journal of Machine Learning Research, 24(346), 1-45. https://jmlr.org/papers/v24/22-1248.html

[2] Finkelstein, N., Adams, R., Saria, S., and Shpitser, I. (2021). Partial Identifiability in Discrete Data with Measurement Error. Proceedings of UAI, PMLR 161, 1798-1808. https://proceedings.mlr.press/v161/finkelstein21b.html

[3] Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., and Zrnic, T. (2023). Prediction-Powered Inference. https://arxiv.org/abs/2301.09633

[4] Zrnic, T. and Candes, E. J. (2024). Active Statistical Inference. Proceedings of ICML, PMLR 235, 62993-63010. https://proceedings.mlr.press/v235/zrnic24a.html

[5] Li, P., Zrnic, T., and Candes, E. J. (2025). Robust Sampling for Active Statistical Inference. Advances in Neural Information Processing Systems. https://papers.nips.cc/paper_files/paper/2025/file/6389470564214983604d1ac81631c2c5-Paper-Conference.pdf

[6] Kops, C. and Tsakas, E. (2026). Choice via AI. Working paper. https://arxiv.org/abs/2602.04526

[7] Cherep, M., Ma, C., Xu, A., Shaked, M., Maes, P., and Singh, N. (2025). A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments. https://arxiv.org/abs/2509.25609

### Reproducibility and status

Companion code: delegation-blind-spot. The repository includes the frozen exploratory pilot configuration, source hashes, 100,000 numerical audit evaluations, summaries, plotting code, channel-bound witnesses, and tests. Two runs produced byte-identical numerical CSV outputs. The constructed agent instrument generated 648 control decisions; these are deterministic or pseudorandom controls, not LLM responses.

Twenty-eight automated checks pass, including exhaustive small-population checks of estimator expectation and variance, feasible bound witnesses, uncertainty monotonicity, option-order balancing, and response failure handling. Such checks reduce implementation risk. They do not replace statistical review or empirical validation.

The next milestone is a frozen main experiment with real model responses and an independently defensible outcome measure. The present document is an early research note, not a peer-reviewed paper. Authorship, contributor acknowledgments, and tool-use disclosures must satisfy the eventual venue's requirements before submission.
