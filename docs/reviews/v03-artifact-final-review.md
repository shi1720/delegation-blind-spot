# v0.3 final computational artifact audit

Date: 20 September 2026. This is an internal AI-assisted artifact audit, not an independent human peer review, venue decision, or customer validation. The audit made no model API requests and changed no manuscript or experimental implementation.

## Verdict

**Pass for the numerical consistency and reproducibility checks below.** No numerical blocker was found in the current IUI poster manuscript or technical report. The evidence supports a computational work-in-progress contribution about auditing synthetic delegated choices. It does not establish human preference recovery, customer outcomes, real product success, or a general empirical law about agent-mediated markets.

The IUI poster draft and the longer report now distinguish structural non-identification from finite-sample uncertainty, compare the receipt follow-up with a deterministic supplied-input extractor, and preserve unresolved and unsuccessful outcomes. These changes address substantive omissions in the earlier internal review. They do not turn the synthetic benchmark into a human study.

## Audited source snapshots

At the numerical audit, SHA-256 values were:

| File | SHA-256 |
| --- | --- |
| `paper/main.tex` | `606ae982e935589569e6362fb76ecdfefd6a46962038cbdad16c2fa6db5d149d` |
| `paper/submission/iui-poster.tex` | `2348090a6dbab20cfa071a827b453cbfd894972b36b85b79b44b8788ff191cb6` |
| `experiments/v3/parser_baseline.py` | `99bf6ac85d1adaadc2b137a0edbcedd5db8c1470cb4d11ecaabbdcf1d0f857e0` |

The generated model, receipt, and control results sections were also read against their underlying result artifacts. Later editorial changes require a new source snapshot; these hashes identify exactly the text covered here.

## Independent clean reproduction

The full controlled sweep was independently rerun, from its frozen plan, into a separate output directory:

```sh
python3 experiments/v3/precision_sweep.py \
  --plan experiments/v3/precision-sweep-plan.json \
  --output tmp/v03-sweep-reproduction
```

All 72 design cells completed, with 200 independent datasets per cell: 14,400 datasets and 43,200 method evaluations. The following numerical artifacts matched the released files **byte for byte**:

| Artifact | SHA-256 |
| --- | --- |
| `replicates.csv` | `0e3ca1a114c48f728b7d15990768aba26d20c70415ce37419735954987d63584` |
| `summary.csv` | `fade12e570c528d82e4b9c706492e56c497a0ca27e909bb0fca0b377f9762afe` |
| `structural.json` | `c69f63a3aac6d794c15e4cacf48e9ebb2543a133bfe83946b959d4e79238e870` |

The PNG also matched exactly. PDF/SVG hashes differed because generated figure metadata is not fixed; these differences did not affect the identical numerical data or raster rendering. Execution timestamps necessarily differ.

The parser baseline was rerun again for this final audit:

```sh
python3 experiments/v3/parser_baseline.py \
  --output tmp/parser-baseline-v3-final-reproduction.json
```

The entire parsed JSON exactly equaled `results/parser-baseline-v3.json`, including source hashes and all nine conditions. Earlier exact reanalysis of all four recorded model/receipt studies via `scripts/reproduce_model_results.py --require-receipts` had passed; it was not redundantly rerun for this final sweep check. No API responses were regenerated or replaced.

## Source and plan provenance

The current sweep and identification implementation hashes match the original completed-run manifest:

- Sweep implementation: `8c7c78d14a9cff05c4cd4d4600b13b63bb82eb66690baa210408dfdf6ea2d15a`.
- Identification implementation: `34ca9dea09600858bbac25c0720b7a9bb9fbc3eac8e85fc002ffc4dc9cec4755`.
- Frozen plan: `84acfad40223d95a654b73122d655ceb9fda07359819bb6546580c40ce107b96`.

Thus the executable code and plan used in the original draws are the same as those independently rerun. Subsequent tolerance/failure-policy clarifications were documentation changes, not numerical changes after observing results. In particular, the implemented decision threshold is the fixed `1e-8` value recorded in the plan, although the implementation does not dynamically read that field. Numerical witness errors abort execution; they are not ordinary infeasible constraint sets. No such witness error occurred. Infeasible constraint sets remain in unconditional coverage denominators. The gzip archive was created after simulation for distribution, with lossless content and fixed gzip timestamp; it is not a second experiment.

## Checks against manuscript claims

| Claim | Artifact finding |
| --- | --- |
| Primary requests | 4,800 attempted, 4,783 valid, 17 retained transport failures; no retry substitution. |
| Main decisiveness | 0/36 conservative primary intervals exclude zero. This is a result of this estimator and design, not proof that every channel is structurally non-identifying. |
| Field action optimality | Mini 73.19%, Nano 55.69%; their reported utility regrets are 0.0186 and 0.0573 after rounding. |
| Receipt follow-up | 2,400 valid requests, 12 distinct repeated supplied-profile prompts; 3/9 decisive per model, versus 0/9 matched-count action intervals. |
| Receipt interval widths | Mean action width 0.08720 and receipt width 0.04360 after rounding. Equal observation counts do not mean equal cost, privacy, or elicitation effort. |
| Combined requests | 7,200 attempts, 7,183 valid, 17 transport failures, excluding the separate connectivity smoke call. |
| Deterministic extractor | 720 existing field observations, 7/9 decisive, zero wrong decisive conditions; mean CP width 0.022846606965198867. No model or calibration calls required. |
| Separate direct-outcome comparator | 7/9 decisive; mean Hoeffding width 0.027271398768654684. Its interval is not silently intersected with the CP interval. |
| Sweep structure | Six eta values, four calibration sizes, three mixtures, 200 repetitions; 14,400 independent datasets, 43,200 method evaluations, 216 summary rows. |
| Weak identifiable channel | At eta 0.01 and 2,560 calibration observations per class, all three cohort joint analyses resolve 0/200; median width remains 0.1. The exact population identified width is zero when eta is positive. |
| Positive cohort, eta 0.1, largest budget | Field-only resolution 196/200 (98%), calibration-only 108/200 (54%), joint 2/200 (1%); joint median width 0.07650702240558453. |
| Sweep failures | 84 infeasible intervals and four wrong resolutions, all in the field-only analysis; retained in the relevant denominators. |

The inspector example also matches the recorded cloud/positive/action-only interval: lower bound `-0.0334272130089567`, upper bound `0.050002319335935116`; the lower witness assigns approximately 89.534% to portability-first and 10.466% to support-first, and the upper witness is capacity-first. With channel uncertainty, these witnesses need not use the same fixed channel. The manuscript states that distinction.

## Interpretation and submission boundaries

- The primary model results use two pinned models and one synthetic construction with three domain framings. They are not three independent real-world validations.
- The receipt extension was motivated by the primary result and reuses field draws. Its fixed-design marginal guarantees are conditional on the stated sampling/stability assumptions; they are not selective-inference or simultaneous guarantees after searching for an improvement.
- The supplied preferences explicitly encode the synthetic class. Correct receipt extraction is not evidence of recovering hidden human intent. The no-API parser makes that limitation visible.
- The controlled sweep is new simulation evidence, not additional LLM or human evidence. Its field-only and calibration-only procedures have 98% marginal targets and the joint procedure a 96% marginal target under the stated assumptions. Observed 200/200 coverage does not prove perfect coverage: its two-sided 95% binomial lower bound is approximately 0.9817. No simultaneous coverage claim across all cells is warranted.
- The IUI poster CFP permits non-anonymous submissions according to the venue check recorded by the coordinating author, despite the provided sample class using `anonymous`. The public artifact link is therefore not an anonymity blocker for this IUI package. Recheck the actual submission-system instructions at upload. This finding does not apply to a double-blind WWW or CHI submission.
- This audit does not claim that a submission was made, that a venue will accept it, or that every typesetting and upload requirement is met. Final PDF visual QA, final source snapshot, metadata, and the submission-system checks belong to the release step.

No blocking numerical correction is requested for the audited drafts. Preserve the explicit synthetic scope, exploratory labels, failed-request accounting, and marginal-versus-simultaneous distinctions in the final release.
