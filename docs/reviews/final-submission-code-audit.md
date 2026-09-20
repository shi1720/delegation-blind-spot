# Final submission code audit

Date: 20 September 2026. Audited commit: `c75ec642eec66729e695b26e20fcfb21e705ed3f`.

This is an internal AI-assisted code and artifact audit, not external peer review or human/customer validation. No API calls were made. No experimental source, recorded data, manuscript, branch, or remote reference was changed.

## Result

**No remaining substantive code error was found in the audited release.** All fresh checks below passed. This supports the reproducibility of the reported computational study, not a claim of general validity outside its stated synthetic construction.

| Fresh check | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | All 80 tests passed. |
| `node study/test-instrument.cjs` | All 14 offline instrument assertions passed. |
| `node inspector/test-core.cjs` | All 72 selections, witness endpoints, decisions, denominators, and withheld-truth checks passed. |
| `python3 experiments/diagnose_channel.py` | Expected revealing/pooling behavior and uncertainty widening reproduced. |
| `python3 scripts/reproduce_model_results.py --require-receipts` | Complete exact JSON reanalysis passed for both primary model studies and both receipt/action comparisons. |
| `python3 scripts/reproduce_v3_results.py --verify-only` | Frozen source/plan/output/archive hashes passed; parser reproduced with complete exact JSON equality on this macOS environment. |
| Read-only archive verification | All 16 compressed model artifacts matched their compressed and uncompressed SHA-256 values; all existing unpacked copies matched the archives exactly. |

The full 14,400-dataset sweep had already been independently rerun with byte-identical numerical CSV/JSON outputs in the preceding final artifact audit. Its source and plan hashes still match the original execution. It was not redundantly rerun here after verification-only/documentation changes. See `v03-artifact-final-review.md` for the original rerun hashes and numerical cross-checks.

## Code paths reviewed

- Joint-mass LP construction, probability constraints, conservative multinomial intervals, zero-count handling, solver witness validation, and decision thresholds.
- Frozen primary analysis: independent calibration/field handling, cohort separation, retained failed responses, position-to-semantic remapping, known versus estimated outcome contrasts, and conditional bootstrap warnings.
- Receipt pairing, task and outcome hashes, model selection, and removal of inapplicable product-choice utility metrics.
- Deterministic baseline: supplied-weight extraction, rejection of unsupported profiles, separation of evaluation truth from inference, and separate CP and Hoeffding intervals.
- Controlled sweep: deterministic independent streams, analytic structural comparison, error budgets, infeasible cases retained in denominators, numerical-error abort behavior, and Monte Carlo interval reporting.
- Verification helpers, archive consistency, and the narrowly scoped cross-platform float comparison. Exact comparison remains the default. CI's explicit `1e-12` parser tolerance does not relax types, counts, decisions, schema, or provenance; sweep byte comparisons remain exact. Nonfinite inputs and invalid tolerances are rejected. The helper reports the number and maximum magnitude of unequal float leaves.

No fix to verification code was necessary. The frozen experiments were not modified to make tests pass.

## Read-only repository state

The working tree was clean at audit start. The only local branch shown was `main`, tracking `origin/main`, at the audited commit. A fresh `git ls-remote --heads origin` returned only `refs/heads/main`, also at that commit. No branch deletion or other git mutation was performed. This report itself is a new, uncommitted audit artifact for the coordinating author to include.

## Boundaries retained for submission

The primary model experiment remains a synthetic study with two pinned models, not a customer trial. The receipt task extracts explicitly supplied preferences, and its follow-up was motivated by the primary result. Its marginal confidence statements do not become simultaneous or selective-inference guarantees. The deterministic parser is limited to the declared four-profile taxonomy. Controlled multinomial simulations are not new model responses or people. These are interpretation limits, not failed computational checks.

Submission-system eligibility, conflicts, author consent, final venue formatting, PDF appearance, and any actual upload are outside this code audit. A computationally reproducible artifact alone does not establish acceptance or submission readiness for every venue.
