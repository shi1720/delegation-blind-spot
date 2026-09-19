# Final technical review of v0.3

Date: 20 September 2026. Internal AI-assisted mathematical and statistical audit, not external peer review or venue acceptance.

## Verdict

No blocking mathematical or statistical error found in the reviewed main manuscript, generated control results, or IUI poster. This verdict is restricted to correctness and consistency of the declared models, proofs, code, and reported synthetic evidence. It does not establish novelty, external validity, or publication suitability.

## Verified claims

- The controlled channel has eigenvalues 1, eta, eta, eta. At eta=0 the contrast interval is [-.04,.06]; for every positive eta the exact known-channel, known-frequency interval has width zero. The distinction between structural ambiguity and finite precision is correct.
- The inverse weights satisfy A_eta^T v=d and have range range(d)/eta. The displayed Hoeffding radius and sufficient sample-size formula are correct for fixed known channel and iid field observations. The text correctly avoids claiming necessary or minimax-optimal sample complexity. A confidence radius by itself is not a universal guarantee of sign resolution.
- Six strengths, four budgets, three mixtures, and 200 repetitions give 72 cells and 14,400 simulated datasets. Three interval methods give 43,200 evaluations. The 98%, 98%, and 96% guarantees use the stated separate or combined error budgets and are explicitly not an equal-confidence ranking or simultaneous guarantee.
- At eta=.01 with 2,560 calibration observations per class and 5,120 field observations, all 200 joint intervals in each of the three mixtures remain unresolved with width .10. Thus the poster's statement applies to all three mixtures. The positive-mixture eta=.1 rates of 98%, 54%, and 1% and median joint width .07651 agree with the released table.
- The 84 infeasible intervals and four incorrect resolutions are retained and are all field-only cases. Feasibility-conditioned widths are distinguished from unconditional coverage and resolution denominators. The 200/200 two-sided 95% Clopper-Pearson lower bound is .98172466, supporting the stated .982 approximation but not perfect-coverage inference.
- The deterministic parser extracts only supplied numerical preferences and validates membership in the declared four-profile taxonomy. Private intent labels enter only later evaluation. Its identity channel is known under that construction. The 720 field records, seven of nine resolved conditions, zero incorrect resolutions, and mean widths .02285 and .02727 match the saved analysis. The CP and direct Hoeffding methods each allocate alpha=.04 and are reported separately, not intersected.
- Main and receipt counts are consistent: 4,800 primary attempts with 4,783 valid responses and 17 retained failures; 2,400 receipt calls without failures. The receipt repeats only 12 distinct supplied-profile prompts per model, is explicitly exploratory, and does not represent human validation. The parser and controlled simulation add no API calls.
- The known finite-bank target is best attainable synthetic utility, not realized future model behavior or commercial return. Current wording correctly prevents an unresolved finite-budget interval from being presented as proof of structural information loss in the unknown LLM channel.

## Verification scope

Read the current generated control section, main manuscript, and poster, and inspected the parser implementation and result artifact. Rechecked the relevant sweep summary rows. All six parser tests and all five controlled-sweep tests passed with unittest. Earlier reviews inspected the theory proofs and LP witnesses; the independent empirical reviewer verified all sweep output hashes and a small reproducibility run. This final pass did not rerun the full 14,400-dataset sweep or make additional model calls.

The retained assumptions remain material: iid/stable response channels, a correct finite taxonomy, independently supplied outcomes, and marginal fixed-design coverage. Post-selection exploratory receipt and parser findings are not selectively adjusted confirmatory tests. All observations are synthetic computational tasks, with zero human participants. The paper states these limitations adequately for the claims audited here.

## Reviewed file fingerprints

- `paper/main.tex`: `606ae982e935589569e6362fb76ecdfefd6a46962038cbdad16c2fa6db5d149d`
- `paper/generated/control-results.tex`: `840743b0ebf4ea7e8db1265a80c148d1146b6388864c0428386d99dfcb13ca29`
- `paper/submission/iui-poster.tex`: `2348090a6dbab20cfa071a827b453cbfd894972b36b85b79b44b8788ff191cb6`
- `experiments/v3/parser_baseline.py`: `99bf6ac85d1adaadc2b137a0edbcedd5db8c1470cb4d11ecaabbdcf1d0f857e0`
- `results/parser-baseline-v3.json`: `23ff2f6d63f59a1224a3484e5c2103e7a9a0092a58af7e4caabbe9e789ac5382`
- `results/precision-sweep-v3/summary.csv`: `fade12e570c528d82e4b9c706492e56c497a0ca27e909bb0fca0b377f9762afe`
