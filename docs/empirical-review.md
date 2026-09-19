# Empirical review and validation plan

## What the first benchmark can and cannot establish

The initial three-option experiment contains a balanced offer that is deliberately dominant in one condition. It is useful for checking arithmetic, option remapping and the proposed diagnostic. It is weak evidence about actual customer behavior: pooling was inserted by construction, preference classes were declared by the investigator, and the outcome contrasts were not measured from people.

The v2 benchmark therefore varies menus continuously and does not require a universal winner. It still uses simulated preferences and synthetic utility functions. Actual model responses to those tasks are empirical observations of model behavior, not observations of customer preferences. Three domain framings are not three independent real-world datasets. These limitations belong in the abstract or experimental scope, not only in an appendix.

## Frozen v2 design

The generator supplies travel, cloud-service and workflow-automation framings. Each contains four semantic offer types, four attributes, four preference classes and three market contexts. Attributes are independently perturbed around offer prototypes. Context modifies capacity or support. Weighted utility includes an explicit threshold penalty, so a single large attribute cannot always compensate for an unacceptable constraint. All utilities lie in [0,1]. Option positions are randomized independently; analysis maps the returned ID back to the semantic offer type.

This numerical rule is intentional. It provides an auditable task objective without treating investigator-written natural language as a measurement of human utility. A natural-language transfer study would be an additional experiment with separate validity checks.

Independent random streams generate:

1. A labeled calibration split, sampled separately within each preference class. Market contexts and offer attributes are randomized independently for every request.
2. Three unlabeled deployment cohorts with declared positive, negative and near-boundary population mixtures. Each cohort receives its own sampled menus and latent classes. All cohorts share the calibration split.
3. A frozen independent bank of 4,096 future menus. Two candidate product investments improve capacity or flexibility and impose the same affordability tradeoff. Enumerating the known synthetic utility function over this finite bank defines the primary class contrasts exactly.
4. An independent sample with replacement from that outcome bank. This supplies a secondary analysis in which the class contrasts are estimated rather than known.

The primary estimand is the expected utility difference between the capacity investment and the flexibility investment, under the declared synthetic cohort distribution and finite future-menu bank. It is not the gain from predicting a hidden class correctly. Calibration and field inference never receive the field intent labels. Tests alter those private labels and verify that inference is unchanged.

Prepared tasks, outcomes and evaluation truth have separate SHA-256 hashes. Requests and model versions must be recorded before response analysis. Record API failures, refusals, malformed outputs, request IDs, token usage, latency and returned model identifiers. Never replace a failed response silently. A retry is a new attempt and needs its own record and declared aggregation rule. The analysis rejects missing or duplicate task results.

### Conditions and controls

Use at least two declared model snapshots on identical prepared tasks. This is a paired comparison, not an independent replication of the task population. The `direct` and `concise` policies are available but should not be mixed within a calibration/field analysis. A policy-transfer experiment must explicitly calibrate under one policy and deploy under another, report the violation of stable-channel assumptions, and avoid interpreting its interval as valid by construction.

Algorithmic controls are an exact utility maximizer, uniform random choice and a fixed essential-offer default. They are not model results. The optimum checks achievable competence; random choice checks chance behavior; a fixed default checks complete behavioral pooling. Negative controls must remain visible if actual models are more informative than expected.

### Observation schemas

The action-only schema records semantic offer type or failure. The context-aware schema records market context jointly with that action, including a context-specific failure category. Both are deliberate compressions of the full observable menu. Their comparison studies the consequences of a logging design. It does not establish nonidentification from all information a company could possibly retain. In particular, the rich continuous menu is not supplied to this categorical channel diagnostic. A contextual continuous-feature method is an important future baseline.

### Estimators and reporting

Report, per model, domain, cohort and schema:

- Field optimal-choice rate, mean known synthetic utility, regret, failure rate and exact denominators.
- Calibration counts and observed field counts. Empirical singular values may describe the sample but do not certify population rank.
- A constrained least-squares plug-in estimate of the population and product contrast. This is an intentionally naive baseline. When preferences are not identified, its selected point can be arbitrary.
- A 200-replicate percentile bootstrap that resamples field counts while holding the estimated channel fixed. Explicitly label its omission of calibration uncertainty. Boundary estimates and unidentified parameters also prevent a general coverage guarantee.
- The full channel-and-field partial-identification interval with witness populations and abstention when zero lies in the interval.
- A secondary interval that additionally accounts for uncertainty in the independently sampled class contrasts.

Use the known synthetic target only for evaluation after the estimates are computed. Evaluate sign errors, squared contrast error, interval width, abstention and false decisive recommendations. Do not report the fraction of a small number of domain/cohort intervals covering their targets as a calibrated estimate of 95% coverage. Repeated independent datasets are needed for that claim. The earlier repeated synthetic simulation serves a different purpose and must not be pooled with live API runs as though all observations shared one design.

### Coverage assumptions

The implemented channel boxes allocate alpha=0.02, field boxes allocate 0.02, and secondary outcome intervals allocate 0.01. Consequently, under the stated sampling and stable-channel assumptions, the primary known-contrast interval has at least 96% marginal coverage and the secondary estimated-contrast interval has at least 95% marginal coverage for one predeclared domain/cohort/schema. These are not 95% simultaneous guarantees over all models, cohorts and schemas. Shared calibration also induces dependence between reported conditions.

The guarantees are unconditional over independent task generation and independent, stationary provider responses. Freezing a random seed makes an experiment reproducible; it does not turn a random-design theorem into a guarantee conditional on one arbitrary fixed heterogeneous panel. Provider drift, correlated responses, systematic retries, unknown intent classes, prompt-policy changes or selective missingness can invalidate the model. Operational failure is retained as an observed action category, but a changing failure process can still violate stationarity.

The outcome Hoeffding bound is deliberately conservative. Wide intervals are a result to report. Primary analyses use exactly known finite-bank synthetic outcomes to isolate channel learning; this cannot justify assuming known outcomes in a human deployment.

## Real-person validation protocol

No real customer validation has yet been conducted. Simulated personas, including independent language-model agents, cannot be substituted for consenting people or described as participants. A simulated persona study can separately stress-test prompts or develop interview questions.

### Recruitment and consent

Start with a feasibility pilot of 12 to 20 consenting adults who actually make one of the relevant purchasing or workflow decisions. Recruit across different budgets and accessibility needs. Do not claim the pilot is statistically powered. Record recruitment source, inclusion criteria, incentive, consent text, withdrawals and exclusions before analysis. Conduct the appropriate institutional ethics review where required. No recruitment or contact should begin without the investigator's authorization.

Consent must explain that an AI assistant will process the provided preferences, that decisions and feedback will be logged, and that participation is voluntary. Avoid names, employer secrets, account credentials and unnecessary personal details. Specify data retention, access, deidentification, deletion requests and whether quotes may be published. Participants should never be asked to make purchases for the experiment.

### Tasks and outcome measurement

Ask each participant to describe one concrete upcoming decision, constraints and unacceptable outcomes. The investigator must not assign their utility weights and then call those weights revealed human preferences. A short structured elicitation and interview can produce a candidate taxonomy; freeze that taxonomy on a development sample before confirmatory evaluation.

Participants then assess realistic, independently generated menus in two counterbalanced conditions: their own choice and an agent-assisted choice. Keep offer order randomized. Collect preference rankings, acceptability, task satisfaction and a short explanation of disagreements. Those are self-reported outcomes, not realized revenue or long-term welfare.

For the product-decision test, independently randomize which version of a prototype each participant uses, or use a carefully counterbalanced within-person comparison when the carryover assumptions are defensible. Measure successful task completion, time, requests for correction and a blinded preference between resulting plans. Predeclare one primary outcome and a meaningful effect threshold. An optional follow-up can ask whether the recommendation was adopted, with explicit consent and separate analysis of attrition.

The key test is whether the action-log diagnostic correctly predicts when the product ranking remains ambiguous compared with directly measured participant outcomes. Intent labels, assistant choices and outcome assessments should be collected in separate steps. Hold out entire people, not just task rows, between taxonomy development, channel calibration and final evaluation.

### Confirmatory sample size and analysis

After the feasibility pilot, use participant-level variance, response correlation and expected class prevalence to simulate power for the predeclared decision threshold. Freeze the confirmatory sample size, minimum per-class calibration counts and analysis plan before examining confirmatory outcomes. If rare classes make the proposed channel model unusable, report that limitation instead of merging classes after viewing favorable results.

Analyze repeated tasks with participant-level clustering. Report selective participation, missing outcomes, exclusions, uncertainty in both preference classification and customer outcomes, and sensitivity to taxonomy choice. Participant interview quotations require permission and must be traceable to actual transcripts. Qualitative findings should be coded by an explicit procedure and disagreements preserved.

### Go/no-go criteria

Proceed to strong external product claims only if the taxonomy is stable enough to calibrate, behavior and outcomes are measured independently, results survive a held-out participant sample, and the method helps a concrete product decision beyond existing calibrated measurement-error or partial-monitoring baselines. If the intervals are usually unresolved, that is useful evidence about required data collection, not a successful product-recommendation system. If the actual agents preserve relevant preferences well, report that negative result against the proposed blind-spot hypothesis.
