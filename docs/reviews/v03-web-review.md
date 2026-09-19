# Internal skeptical review: ACM The Web Conference 2027

**Status:** internal AI-assisted critique, not a venue review or acceptance prediction. Reviewed on 20 September 2026. Scope: research and short-paper suitability of technical preprint v0.2. Reference commit: `0971596`; `paper/main.tex` SHA-256: `817afa7124d6b31fd5aeabb865f6b1d9ed6a94c97b85a18e8b6c27ca3ca34f29`.

## Recommendation and scores

**Research paper: reject in its current form. Short paper: weak reject, with a plausible narrower revision.** The artifact is unusually candid and reproducible. Its principal obstacle is a substantive contribution supported by Web-relevant evidence, not typography. Additional model calls alone would not repair that obstacle.

Scale: 1 is poor, 3 is adequate but substantially incomplete, 5 is strong.

| Criterion | Score | Reason |
|---|---:|---|
| Significance | 3/5 | Future product value can differ from execution success, an important measurement question. The study does not establish its prevalence or cost on a Web platform. |
| Originality | 2/5 | Identification, LP bounds, optimal-recovery distance, minimax loss and measurement design have acknowledged antecedents. The software synthesis is useful, but neither a distinctive new method nor a surprising empirical discovery is established. |
| Evidence | 2/5 | Actual API traces are real evidence of model behavior. They cover one numerical synthetic task family; the receipt is an extraction of the supplied class label. There is no real-customer evidence or Web interaction. |
| Validity | 3/5 | Claims are carefully qualified, but the experiment does not separate intrinsic ambiguity from conservative finite-sample inference. Stationary independent provider behavior is assumed rather than demonstrated. |
| Reproducibility | 5/5 | Frozen requests, retained failures, pinned snapshots, raw-response provenance, independent data streams and exact offline reanalysis are strong. Reproducibility is not external validity. |
| Venue fit | 2/5 | Agent-mediated marketplaces are a plausible Web problem, but the current task does not require a browser, Web protocol, platform incentive or actual marketplace. |

## Current official venue checks

The 2027 research CFP requires a Web-specific scientific challenge and explicit first-page track relevance; merely using an API is insufficient. It specifies double-blind review, anonymous `acmart` review format, eight self-contained content pages and twelve pages total including references/appendix. An anonymized preprint submission is allowed. The current manuscript instead uses `article`, names its author in text and PDF metadata, and links an identifying repository. A separate anonymous submission build is required. Candidate tracks include User Modeling, Personalization and Agentic Web Users, and Evaluation, Human Computation, and Resources. These are possible fits, not exemptions from the evidence requirements. [Official research CFP](https://www2027.thewebconf.org/research-track-papers/)

Research abstract/paper deadlines are 18/25 October 2026. Short-paper abstract/paper deadlines are 9/16 November 2026, all AoE. [Official dates](https://www2027.thewebconf.org/important-dates/)

The research page links a separate [short-paper OpenReview group](https://openreview.net/group?id=ACM.org/TheWebConf/2027/Conference_Short_Papers), but its rendered page did not expose category-specific page limits. Do not import a previous year's short-paper limit or infer one from the common research-page wording. Verify the active submission invitation before finalizing a short-paper build.

## Contribution as a reviewer would understand it

The paper translates classical statistical identification into a useful product-oriented question, packages exact and uncertainty-aware diagnostics, and demonstrates that a particular conservative procedure can abstain even when agents perform tasks moderately well. It then demonstrates that explicitly returning an already supplied class attribute makes those constructed preferences more observable. That is an honest methods-and-measurement artifact. It is not currently evidence that agent adoption causes a new market-level blind spot, that an AI receipt generator is needed, or that the proposed inference is practically competitive.

The authors deserve credit for making those limits explicit. Nevertheless, a sequence of disclaimers cannot supply the missing central contribution. A stronger short paper should choose one empirical question and answer it sharply, rather than present many standard theorems plus two weakly diagnostic studies.

## Concrete blockers

### 1. The observability problem needs a Web actor boundary

Who knows the input preferences: the customer's browser agent, a model provider, the merchant, or all three? If the merchant itself supplies the weighted preference prompt, it already has the leading weight and need not infer it from transactions. If a third-party assistant retains the preferences while the merchant receives only a booking, the information boundary is plausible. State that architecture explicitly and identify exactly which fields each party can observe or obtain with consent. The current numerical API experiment does not instantiate that boundary.

A minimal defensible revision would model an external assistant interacting with a merchant-facing selection endpoint, with an explicit observability table. A genuinely stronger empirical study would use a controlled Web interface and real menus or catalog attributes, while retaining synthetic preferences as such. Merely wrapping the same arithmetic task in HTML would not establish external validity.

### 2. Every primary interval abstains, including the optimal chooser

The main experiment's 36 unresolved conditions do not demonstrate intrinsic nonidentification. The same conservative method also abstains for the exact-optimum control. A procedure that never recommends anything can achieve zero wrong recommendations without being practically informative.

Existing analysis records provide a useful warning: all twelve distinct model/domain/schema empirical channel matrices have positive smallest singular values, ranging from approximately 0.059 to 0.255. This does not certify population rank or prove stable invertibility, but it directly motivates separating finite-sample uncertainty from structural ambiguity. Do not describe the observed abstention as an established rank deficiency.

The highest-value revision is a decomposition of exact-channel ambiguity, calibration uncertainty, field uncertainty and their combination. Report it before adding more calls.

### 3. The receipt follow-up provides the hidden class by design

There are only twelve distinct receipt prompts. The four synthetic classes have different leading weights. Correctly returning that maximum is the class label, and a deterministic parser can do it without any model calls. The observed 100% extraction accuracy is neither general preference understanding nor a validation of the originally supplied preferences.

The necessary baseline is direct deterministic extraction with a known identity channel, eliminating unnecessary calibration uncertainty. A direct bounded sample mean of the known class contrast is another essential comparator. Both use the same field records. If they are more informative or cheaper, state that explicitly. This could support a useful design lesson about collecting the required statistic, but does not establish a new agent capability or inference algorithm.

### 4. The comparison lacks a calibrated practical alternative

The conditional bootstrap is explicitly incomplete because it ignores channel-estimation error. Beating its apparent confidence or contrasting its errors with universal abstention is not a compelling baseline comparison. A full calibration-and-field bootstrap may be a useful descriptive comparator, with careful warnings about boundaries and nonidentification; it is not automatically a guaranteed method. Direct observation of the class and direct outcome contrast should be included. Avoid selecting whichever procedure becomes decisive on the observed targets.

### 5. The task taxonomy and target carry most of the conclusion

The investigator declares four classes, assigns utilities and knows the future-product contrast. An actual platform would need a defensible taxonomy and outcome measurement. Three semantic framings share the same generator and cannot substitute for three external datasets. A repeated-sampling study within the generator is useful for checking procedure behavior, but cannot validate the taxonomy for customers.

### 6. The receipt evidence is post-selection

The follow-up was chosen after the primary experiment and reuses its field draws. The manuscript now says this, correctly. Preserve that distinction in every figure and abstract summary. A fixed-design marginal coverage statement does not become a selective guarantee for an adaptively chosen follow-up. A new independent field cohort would strengthen confirmatory claims, but is unnecessary if the paper remains explicitly exploratory and makes no confirmatory significance claim.

## Highest-value offline improvements

1. **Analytic controlled-channel sweep.** Choose a fully specified family that moves continuously from informative to pooled channels. Cross channel informativeness, sample size and contrast margin; include both directions and near-zero contrasts. Use many independent multinomial datasets, report Monte Carlo uncertainty, resolution, false-decisive risk and width. This identifies where the diagnostic is useful and where it is merely conservative. No simulated draw may be counted as a fresh LLM response.
2. **Known-channel versus estimated-channel decomposition.** At common targets, compare exact channel/exact frequencies, exact channel/finite field samples, finite calibration/exact frequencies and joint uncertainty. Keep the target population and contrast fixed across these ablations. The known reference is an experimental control, not an assertion that the deployed model channel is known.
3. **Deterministic supplied-profile parser.** On the existing receipt subset, parse the maximum supplied weight, use the resulting known identity observation channel, and compare frequency-based intervals with a bounded direct-contrast mean interval at comparable marginal confidence. Do not use private evaluation labels to extract the field value.
4. **Optional empirical-reference sensitivity.** Treat estimated model channels as explicitly constructed reference channels and generate repeated multinomial samples from them. This characterizes a plug-in simulation, not the true model sampling distribution. Publish all channels and sample-size conditions, including unfavorable cases.
5. **Matched measurement cost accounting.** Keep observation count, API tokens, calibration labels, privacy exposure and human burden separate. A conceptual receipt field may cost more than logging an action even if both produce one categorical observation.

The analytic family and parser baseline are the smallest worthwhile additions. A larger API run without a new question has low value. More model families would test generality only after the measurement diagnosis is resolved. Human validation cannot be supplied by personas or simulated agents; the present short-paper route need not claim customer validation at all.

## A defensible revision target

One viable short-paper thesis is: **under a specified agent-mediated platform boundary, uncertainty about calibration can dominate product-decision inference, and a deliberately collected decision-relevant statistic can be preferable to behavioral inversion.** The contribution would be a transparent measurement analysis and executable benchmark, with a clear taxonomy of structural ambiguity versus finite-sample ambiguity. The paper must still demonstrate a substantive Web-specific implication and compare the simpler direct measurement approach.

Move most standard proofs and the unrelated audit-estimator pilot out of the short-paper narrative. Keep only the identification result needed to interpret the experiment, one uncertainty result, the uncertainty-source ablation, and a parsimonious measurement comparison. Preserve full derivations in the archival technical report. Format compliance should be addressed after this argument is settled.

## Exit criteria for a new review

- The first page identifies the Web platform/assistant information boundary and names a scientific question the results actually answer.
- One primary result has evidence beyond universal abstention or extracting a provided label.
- Structural ambiguity, sampling uncertainty, taxonomy assumptions and outcome assumptions are reported separately.
- Direct supplied-class extraction and an appropriate direct-contrast baseline appear alongside the more complex method.
- All new simulations are separately labeled, their designs are fixed before inspecting their results, and repeated-sampling claims include Monte Carlo uncertainty.
- The abstract avoids implying human validation, general market prevalence, or a new general estimator.
- An anonymous venue-compliant build has been checked, while the named public preprint and full reproducible artifact remain available.

Satisfying these would justify another review, not an automatic acceptance recommendation. It would likely improve the short-paper case more than the full research-paper case.

## Follow-up implementation audit, separate from the v0.2 verdict

At the investigator's request, an offline parser baseline was added after the review above. It parses only the weights in each supplied prompt, verifies membership in the published synthetic taxonomy, and does not read private intent or future-choice labels. There are 720 field records, zero new API calls and zero channel-calibration observations. Known identity-channel inference with field-only Clopper-Pearson bounds resolves 7/9 conditions, with mean width 0.02285. A direct bounded-contrast Hoeffding interval also resolves 7/9, with mean width 0.02727. Neither produces a wrong decisive sign in these selected conditions. Each method separately uses alpha 0.04; their intervals are not intersected. Six tests cover taxonomy restrictions, label non-use, constant contrasts and a small exhaustive coverage calculation. This is a stronger simplicity baseline and an important limitation of the LLM receipt procedure, not human validation.

An independent code audit also inspected the proposed controlled multinomial precision sweep. Its channel is `(1-eta) * 11^T/4 + eta * I`. It correctly distinguishes positive-eta full rank from complete pooling at zero; the declared contrast range is 0.10. Independent calibration columns, separate field multinomial draws, channel/field error allocations, retained infeasible replicates and conditional-on-feasibility width summaries match the stated design. Field-only and calibration-only intervals have nominal lower coverage 98%, while joint intervals have 96%; these are uncertainty-source ablations, not equal-confidence method rankings. Thirty replicate constructions and ninety method evaluations reproduced exactly in a small independent smoke check, with verified solver residuals. This is a software check, not a coverage-rate estimate.

Minor points communicated to the implementing reviewer: the plan's `decision_tolerance` currently matches a hardcoded value rather than being passed through; witness-check arithmetic errors abort the run whereas the plan's failure wording mentions retaining invalid intervals; the inherited `near` mixture has contrast 0.0154 rather than zero. None invalidates the inspected fixed plan, but descriptions should remain precise. In particular, do not describe this design as a null-effect/type-I-error experiment. The complete sweep and its results still require their own review before manuscript claims are strengthened.

The completed sweep was then independently checked: its manifest reports 14,400 independent simulated datasets, 43,200 method evaluations and 216 summary rows. Every recorded output hash matched. Eighty-four infeasible intervals occur in the field-only ablation and remain in its coverage denominator; the other two methods have none. The minimum observed per-cell field-only coverage is 0.96 against a nominal lower bound of 0.98, with only 200 replicates per cell, so Monte Carlo intervals and multiplicity must accompany any interpretation. No inference of a violated theorem follows from that minimum alone. Calibration-only and joint intervals contain their targets in every recorded replicate, reflecting conservatism rather than proving universal coverage.

For the positive cohort at 2,560 calibration observations per class, joint resolution is zero at eta 0, 0.01 and 0.03, 0.01 at eta 0.1, and 1.0 at eta 0.3 and 1. This is useful evidence that exact identifiability and practical finite-sample resolution differ in the declared channel family. It does not estimate the true channels of the two API models or establish a property of real Web customers. The full run was hash-audited; the independent numerical rerun covered the small smoke design, not all 43,200 evaluations.
