# Publication and novelty review

Reviewed 19 September 2026. This is a critical research-development review, not peer review or a statement of acceptance. It reviews research note 0.1 and the repository's declared instrument. The review distinguishes direct inspection from preliminary screening and does not certify that the literature search is exhaustive.

## Assessment

The framing is useful, but the initial mathematical ingredients are established. The strongest credible direction is a decision-specific measurement study of delegated product activity: characterize which proposed changes are supported by observed behavior, expose competing compatible customer populations, and measure whether limited extra feedback resolves a consequential disagreement under realistic agent changes.

A complete manuscript can be produced from simulations and actual model responses if every empirical claim is limited to those settings. A study of human customer preferences requires human observations. Model personas are useful for instrument stress tests and cannot be relabeled as customers, participants, or human validation. A disclosure is part of the method, not an optional acknowledgment.

## Closest overlaps and their implications

| Antecedent | Direct overlap | Consequence for this paper |
| --- | --- | --- |
| [Blackwell, Equivalent Comparisons of Experiments (1953)](https://doi.org/10.1214/aoms/1177729032) | Comparing observation channels by their value for decisions has a classical foundation. | Do not claim that task performance and information for other decisions are the same, or that their separation is a new general theorem. Explain why application-specific execution utility is not the same criterion as informativeness. Bibliographic record verified; full original proof not inspected in this review. |
| [Kirschner, Lattimore and Krause, Linear Partial Monitoring (2023)](https://jmlr.org/papers/v24/22-1248.html) | Decision contrasts and feedback maps determine observability. | The row-space/null-space proposition is background, not a novel contribution. Sequential probe selection needs comparison with this literature if it becomes a main algorithm. Relevant formulation reviewed in the existing ledger and primary conference/journal record rechecked. |
| [Finkelstein et al., Partial Identifiability in Discrete Data with Measurement Error (2021)](https://proceedings.mlr.press/v161/finkelstein21b.html) | Optimization under measurement-error restrictions produces partial-identification bounds. | A joint-mass LP is a useful implementation, not a new general bounding principle. Any claim of sharpness must name the exact uncertainty model. Primary abstract and bibliographic record checked, full theorem-by-theorem comparison outstanding. |
| [Lipton, Wang and Smola, Detecting and Correcting for Label Shift with Black Box Predictors (2018)](https://proceedings.mlr.press/v80/lipton18a.html) | A calibrated confusion channel maps latent class prevalence to observed predictions. Inversion estimates prevalence under conditional stability. | This is a missing direct baseline and related-work citation. Our channel model is mathematically close. Distinguish singular-channel, decision-specific set identification from full class-proportion estimation and explicitly evaluate conditional/channel shift. Primary paper introduction and model inspected. |
| [Kops and Tsakas, Choice via AI (2026)](https://arxiv.org/abs/2602.04526) | Delegated recommendations can fail to identify preferences because interpretation and preferences are jointly latent. | Preference ambiguity under AI choice is already studied. Our stochastic population channel and future product contrast are a different modeling focus, not proof of novelty. Primary introduction, setup, and model inspected. |
| [Kraft and Larsen, Consumer Preference Transmission in Agentic Markets (2026)](https://ssrn.com/abstract=6864181) | Consumer information in prompts, agent responsiveness, preference pooling, and adoption selection are already examined. | Do not claim first evidence of consumer heterogeneity being obscured by agents. Their work includes human evidence, so synthetic profiles alone are a weaker empirical basis. The authors' institutional summary reports a conjoint experiment and an incentivized bookstore task; full empirical protocol still needs inspection. [Institutional source](https://www.chicagobooth.edu/research/center-for-applied-artificial-intelligence/research/our-faculty-research/2026/consumer-preference-transmission-in-agentic-markets). |
| [Cherep et al., ABxLab (2025)](https://arxiv.org/abs/2509.25609) | Controlled product menus and stated user profiles probe actual agent decisions. | Running model choices on several domains is not by itself a new benchmark contribution. Differentiate by calibrated population recovery, decision regret, compatible witnesses, and feedback repair. Primary manuscript inspected in the earlier ledger and re-opened. |
| [Zrnic and Candes, Active Statistical Inference (2024)](https://proceedings.mlr.press/v235/zrnic24a.html) and [Li et al., Robust Sampling for Active Statistical Inference (2025)](https://papers.nips.cc/paper_files/paper/2025/file/6389470564214983604d1ac81631c2c5-Paper-Conference.pdf) | Selective true-label acquisition, residual correction, and robust allocation already address bad prediction/uncertainty models. | Keep the audit pilot as baseline validation or appendix. Undercoverage of a Wald approximation in a constructed sparse-label setting is not a new estimation result. Use correct finite-sample baselines before asserting improved reliability. Earlier equation-level inspection recorded in the ledger. |
| [Sagnol and Pronzato, Fast Screening Rules for Optimal Design via Quadratic Lasso Reformulation (2023)](https://jmlr.org/papers/v24/22-1305.html) | Optimal design can target one linear contrast rather than reconstruct all parameters. | “Ask only what matters to this decision” has established c-optimal design ancestors. This source is a contemporary entry point, not a claim that it introduced c-optimality. Abstract screened only. |

## A defensible narrow contribution statement

A provisional statement, conditional on finishing the experiments:

> We operationalize decision-specific observability for delegated product activity. Given independently specified customer-value contrasts, calibrated action channels, and sampling uncertainty, an executable diagnostic returns compatible decision bounds and witness populations. Controlled model experiments measure when successful task execution leaves these decisions unresolved and how additional feedback changes that ambiguity under calibration and channel drift.

This statement deliberately does not claim a new LP, a new observability theorem, proof of widespread customer harm, or a completed human study. If the current result is merely that hand-designed pooled menus hide intent, then the empirical contribution is instrument validation and the manuscript should remain a technical report or work-in-progress submission.

## Questions that could produce a stronger contribution

1. **Decision transport across agent updates.** Can a calibration certificate trained on one agent remain valid for a particular product contrast after a model update even when full preference estimates change? Which drift components matter to the target contrast, and which are harmless? Compare with label-shift assumptions and robustness to channel misspecification.
2. **Decision-specific feedback with a privacy budget.** Can a company choose a product change from a deliberately coarse customer response while avoiding unnecessary preference recovery? Measure the response burden and information disclosed as well as regret. A privacy claim requires a precise threat model and metric, not merely collecting fewer fields.
3. **Competing explanations for stable demand.** Can unchanged aggregate logs conceal both changes in the customer mix and changes in the agent? Use controlled interventions that separately manipulate those factors. A decomposition cannot be identified from a single uncalibrated aggregate channel alone.
4. **Current utility versus learning value.** Can a low-burden follow-up resolve a decision without making the current customer choose a worse option? Deliberately degrading the menu to extract information is not an acceptable default. Compare optional, consented feedback with passive signals and direct randomized outcome measurement.

These are research questions. No priority, novelty, or positive-result guarantee follows from naming them.

## Required empirical revisions

### What actual model experiments can establish

They can establish how named model snapshots behave under specified synthetic tasks and prompts, whether the calibration implementation covers its declared model, and whether an intervention changes the available information. They cannot establish how real customer preferences are distributed, what customers value, or whether customers will answer a feedback question accurately.

The existing three domain skins share a mathematical template. Count them as three task contexts within one instrument family, not three independent real-world replications. Three repeated responses per condition are insufficient to interpret small probability differences precisely. Report intervals and actual per-cell denominators rather than treating repeated model responses as independent human subjects.

Before calling the experiment confirmatory, freeze the following:

- Primary target contrast and utility measurement; intent classes; channel and field sampling units.
- Model snapshot IDs, prompts, option-order balancing, repetitions, failure categories, retries, exclusions, and budget.
- Separate calibration and evaluation samples. Resampling the same collected decisions is a simulation based on empirical probabilities, not additional independent model calls.
- Primary metric: decision error or regret at specified measurement cost. Also report interval coverage, abstention, width, execution utility, and audit burden.
- Baselines: action-frequency plug-in; constrained label-shift estimation with its stated invertibility/stability conditions; partial-identification diagnostic; uniform direct outcome audit; robust active audit where applicable.
- Controls: known optimal chooser, random chooser, pooled chooser, perfectly informative channel, irrelevant extra feedback, agent-version drift, omitted intent class, and noisy/misspecified feedback.
- Confidence treatment: paired comparisons when common task instances are used; clustering by underlying task/person where appropriate; multiplicity handling for many contrasts; predeclared bootstrap unit if bootstrapping.

Do not present samples from two models as evidence about “AI agents” in general. Do not silently exclude refused or malformed outputs if those failures differ by intent or menu. A failure can be an observable action category or have explicit missingness bounds.

### What genuine customer validation requires

A practical first study could recruit consenting adults for a bounded travel or software-plan decision. Collect preferences privately before delegation, let the agent complete the task, and collect a separately measured outcome or incentivized tradeoff after the choice. Randomize a transparent feedback request and evaluate whether it resolves the specified product decision at an acceptable burden. Validate that the response means what the model assumes. A price willingness measure, satisfaction score, and revealed tradeoff are not interchangeable labels.

Prepare participant materials, data minimization, consent, compensation, eligibility, withdrawal rules, and an ethics review or documented determination before collection. Determine sample size from the minimum relevant effect and the analysis design. Recruitment authorization, access to participants, and actual responses remain prerequisites. No simulated persona can satisfy them. Synthetic persona evaluations should be labeled exactly that and kept analytically distinct.

## Proof and reporting requirements

- State all spaces, column-stochastic conventions, observables, estimands, and quantifiers before each theorem.
- Distinguish global identification for every feasible population from local identification at one boundary observation.
- For uncertain-channel sharpness, prove both maps between `(A,p)` and `(J,p)`, including zero-mass columns. Name rectangularity and feasibility assumptions.
- For confidence coverage, explicitly allocate the total error probability between channel calibration, field frequencies, and any estimated outcome contrasts. A union-bound guarantee is conditional on model correctness and exchangeability assumptions, not immunity to drift.
- Report algorithmic complexity and numerical tolerance only if established. Solver success alone does not prove a witness satisfies the original model.
- An impossibility result should specify the experiment, sample size, parameter alternatives, and loss. It should not imply that direct outcome measurements or interventions are impossible.
- Include one table mapping each contribution claim to its theorem, experiment, artifact, and limitation. Keep scope statements near results rather than relegating them to the last paragraph.

## Packaging requirements

For a research-grade artifact: pinned dependencies or a tested environment lock, clean installation instructions, deterministic synthetic fixtures, immutable raw model records with provenance, exact analysis commands, result manifests, figures generated from recorded results, test coverage for boundary cases, a license, a citation file, and a versioned archive. Document cost and compute. Public raw records must exclude credentials and any non-consented personal information. A reproducible API request does not guarantee identical remote responses.

For the manuscript: use one explicit venue's official class only after deciding that venue. Until then use a conventional technical preprint with numbered theorems, equations, sections, references, appendices, accessible figure captions, and source code. Do not label a custom PDF renderer “ACM compliant” or “publication ready” merely because it is visually polished. A human author must read, verify, and be able to defend every claim and proof.

## Realistic publication paths as of 19 September 2026

| Path | Verified timing and format | Assessment |
| --- | --- | --- |
| [IUI 2027 Posters and Demos](https://iui.acm.org/2027/call-for-posters-demos/) | 10 November 2026 deadline; up to four pages excluding references in ACM single-column submission format; demo video up to five minutes. | Most realistic near-term work-in-progress target if the diagnostic becomes an intelligible interactive product-research tool. This is not a full-paper acceptance claim. |
| [The Web Conference 2027](https://www2027.thewebconf.org/important-dates/) | Research abstracts 18 October, full papers 25 October 2026. Short abstracts 9 November, short/demo papers 16 November. | Potential fit for agent-mediated web commerce, but needs an actual web measurement contribution and completed evaluation. Do not rush into the research track with synthetic menu illustrations alone. |
| [CHI 2027 Posters](https://chi2027.acm.org/authors/posters/) | 21 January 2027; up to four pages excluding references; anonymous ACM single-column submission. | Useful for an early human-facing study or prototype. The main paper deadline was 10 September 2026 and has passed. [Official dates](https://chi2027.acm.org/). |
| [TMLR](https://jmlr.org/tmlr/) | Rolling submissions with the mandatory official LaTeX template. | Not a default target for this workflow. The [current FAQ](https://jmlr.org/tmlr/faq.html) expects human-sourced ideas, claims, and results and explicitly requires a first-page AI-assistance disclosure. The author must resolve compliance honestly before considering submission. The journal's evidence standard also excludes inflated novelty claims. [Criteria](https://jmlr.org/tmlr/acceptance-criteria.html). |

The TMLR policy point is substantive: neither changing the paper's wording nor hiding the research workflow resolves it. No submission should claim compliance that has not been established. For ACM, follow the selected venue's current research-method and AI-use requirements; do not infer that permission for copyediting excuses omission of model-generated research data.

## Release gate

A polished preprint release is possible once the reported claims and generated artifacts agree. A human-validated, publication-ready paper is not complete until genuine validation, relevant baseline comparison, independent technical scrutiny, author review, and venue-specific requirements are satisfied. Preserve this distinction in the abstract, README, and release notes.
