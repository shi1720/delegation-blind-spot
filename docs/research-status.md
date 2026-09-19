# Research status

Author: Shivam Gupta. Version 0.2.0. Updated 19 September 2026.

Selected direction: The Delegation Blind Spot. Working title: Learning What People Want When Agents Make the Choices.

## Objective and current conclusion

Produce a technically correct research contribution with implemented code, actual model experiments, supported figures, proofs, a cited manuscript, reproducible artifacts, and an honest publication strategy. Human/customer claims require genuine human evidence. No participation, originality, approval, or acceptance can be fabricated.

The primary model study is complete. Its main result is a limitation: all 36 conservative product-decision intervals remain unresolved at the tested budget. This does not demonstrate a useful decision remedy. A completed exploratory receipt follow-up resolves 3 of 9 selected conditions per model by explicitly collecting already supplied preference information. The primary negative result remains unchanged. Final release checks and broader customer validation remain separate requirements.

## Completed work

- Decision-specific identification and uncertainty bounds with explicit witness populations, a proof appendix, and computational checks. General row-space identification and LP partial identification are attributed antecedents.
- A technical-preprint manuscript in LaTeX with generated numerical content and vector figures. The earlier seven-page 0.1 note remains a historical artifact.
- 100,000 synthetic audit estimator evaluations. Four numerical CSV outputs reproduced byte for byte. These are not model calls or participants.
- A primary experiment frozen before execution, but not externally preregistered, with 2,400 shared constructed tasks and two pinned model snapshots.
- 4,800 primary API attempts: 2,391 valid mini choices and 2,392 valid nano choices, with 17 transport failures retained and no replacement retries.
- A completed 2,400-request receipt follow-up with all responses valid, bringing the two-stage total to 7,200 attempts, 7,183 valid responses, and 17 retained failures.
- Independent calibration and field partitions, declared synthetic utility outcomes, algorithmic controls, label-shift point estimates, conditional bootstrap, and conservative channel bounds.
- Per-model field performance on 1,440 tasks: 73.19% utility-maximizing choices for mini and 55.69% for nano. These are specific to the frozen synthetic generator and include delivery failures in the denominator.
- All 18 intervals per model unresolved. Conditions share data, and this descriptive count is not an empirical coverage estimate. Conditional marginal guarantees require the stated assumptions.
- An explicitly exploratory cross-model transport sensitivity analysis. It intentionally violates stable-channel assumptions and has no claimed transport coverage guarantee.
- Compressed request/response artifacts, hashes, recorded usage and errors, numerical reanalysis scripts, and publication figure generation.
- A preview-only offline study instrument with random assignment, an accurately labeled deterministic reference aid, separate preference/outcome questions, truthful test-data exports, and desktop/mobile browser QA. This is study preparation, not human validation.

Exact values and provenance: [primary summary](../results/model-study-summary/summary.json), [frozen primary plan](../experiments/v2/frozen-study-plan.json), and [archive manifest](../results/model-artifacts.json).

## Completed exploratory receipt follow-up

A separate explicit-preference receipt experiment was frozen after observing the primary negative result and before its own model calls. It completed 1,200 queries per model using 12 distinct prompts across four supplied-weight profiles and three domain framings. Both models correctly reported the largest supplied weight on every calibration and field request, with no delivery failures. These are repeated extraction tasks, not independent customer decisions.

For each model, the attribute-only receipt channel resolves 3 of 9 selected domain/cohort conditions, compared with 0 of 9 for matched action-only observations. All three resolved cases are the positive cohort, one per domain, and none contradicts its known synthetic target. The other six conditions remain unresolved. Average interval width is 0.0435969805 for receipts versus 0.0872040609 for the same-count action subset.

The follow-up is exploratory and was selected after the primary result. The reuse of original field draws and follow-up selection have no selective-inference correction. Counts of resolved conditions are descriptive, not a significance test, coverage estimate, or guaranteed post-selection confidence statement. Equal observation counts do not make collection costs, privacy exposure, or response burden equal.

The result concerns extraction of information already stated in a synthetic prompt. A deterministic extractor could provide the same attribute. It is not discovery of unknown human preferences, a privacy mechanism, or proof that an LLM is necessary. See the [recorded receipt summary](../results/receipt-study-summary/summary.json), [figure](../results/receipt-study-summary/receipt-comparison.pdf), and [frozen receipt plan](../experiments/v2/frozen-receipt-plan.json).

## Evidence boundaries

There are **zero human participants** and **zero real-customer outcome measurements**. Synthetic profiles, model-generated personas, and browser test responses cannot be counted as humans. The three primary domain framings share a mathematical generator and do not establish three-market generalization. Provider calls are real model experiments, but repeated calls and finite synthetic utilities do not establish human behavior or industry prevalence.

The primary intervals have at least 96% marginal coverage under the declared channel and sampling model, not guaranteed coverage under arbitrary provider drift, correlated errors, unknown intent classes, or outcome misspecification. Zero false certified decisions caused by universal abstention is not a successful product-selection policy. A future paper must quantify usefulness as well as uncertainty.

## Remaining requirements for a broader publication claim

1. Complete final release QA: verify primary and receipt numerical reproduction with `python3 scripts/reproduce_model_results.py --require-receipts`, inspect the final paper, and confirm that archive hashes and reported counts agree. Preserve the exploratory follow-up status.
2. Demonstrate a contribution beyond established partial identification, label-shift estimation, active inference, and delegated preference transmission. Code and naming alone do not establish novelty.
3. Investigate sharper uncertainty methods and realistic feedback costs without tuning a positive story on the reported evaluation set.
4. Obtain independent expert scrutiny of the proofs, estimands, uncertainty model, and empirical comparisons. Automated or agent review is not external peer review.
5. Have the human author review and be able to defend every claim, mathematical step, and methodological choice.
6. For customer relevance, finalize the task, consent, ethics determination, recruitment, sample size, independent outcomes, and real data collection. No genuine customer study is currently complete.
7. Select a venue, review its current scope, formatting, authorship and AI-use policy, and produce the correct anonymous or attributed submission artifacts. A technical preprint is not a venue-compliant submission by default.
8. Local release checks are recorded in [release validation](release-validation.md): four exact numerical reproductions, 63 Python tests, 14 offline instrument assertions, and inspection of all 14 PDF pages. The versioned release does not imply venue acceptance.

## Stop or revise criteria

If established methods solve the target under equivalent information and cost, do not rename them as new. If uncertainty bounds refuse every decision, report that limitation. If the phenomenon is manufactured entirely by a hidden-label change, present it as a diagnostic sanity check. If the outcome lacks independent meaning, repair the estimand before optimizing an estimator. If all preference evidence is synthetic, keep human and market conclusions out of the abstract and results.
