# Varied delegated-choice benchmark

This is a synthetic-profile instrument-validation benchmark. Live provider responses, when collected, are model evidence. They are not customer validation.

Prepare a frozen experiment without making any API call:

```sh
python3 experiments/v2/prepare.py --output results/v2-prepared \
  --model EXACT_MODEL_SNAPSHOT --calibration-per-class 32 --field-size 64
```

The default three domains and three deployment cohorts yield 960 tasks. Calibration is shared between the cohorts. `requests.jsonl` contains `{task_id, request}` records for the Responses API. The prepared prompt contains the declared customer objective. It does not contain the private field intent label or the future product outcome contrast. `tasks.jsonl` also contains private simulation truth for evaluation and should never be sent wholesale to the model.

To evaluate a declared algorithmic control:

```sh
python3 experiments/v2/analyze.py --prepared results/v2-prepared \
  --responses results/v2-prepared/controls.jsonl --system optimal \
  --output results/v2-prepared/optimal-analysis.json
```

Live response records must contain `task_id`, `system` and either a valid `choice_id` in A/B/C/D or an explicit `error`. Preserve raw provider responses, requested and returned model versions, usage and attempt history in the experiment artifact. Pass the completed per-task result file to the same analyzer. The analyzer requires every frozen task to have exactly one final result. It will not turn missing requests into successes or drop failures.

The analyzer reports a known-synthetic-outcome primary interval, sampled-outcome secondary interval, naive constrained least-squares point estimate and conditional-channel bootstrap, for action-only and context-aware logs. Detailed design, caveats and a real-person validation plan are in `docs/empirical-review.md`.

Do not treat the hypothetical `positive`, `negative` and `near` mixtures as estimates of real customer populations. Their names describe synthetic contrast directions; target contrasts remain in the hashed evaluation artifact. Model snapshots and provider-side response randomness must be recorded, not inferred from the generator seed.

## Publication figures and execution accounting

After both models have complete `analysis.json` and `responses.jsonl` files:

```sh
python3 experiments/v2/plot_results.py \
  --mini results/model-study-mini --nano results/model-study-nano \
  --output results/model-study-summary --pricing experiments/v2/pricing.json
```

The output includes vector PDF and raster PNG figures, a summary of field competence and decision intervals, hashes of the analyzed inputs, and counts of every completed choice, timeout, connection reset and other error. Cost estimates use reported tokens and the cited prices. Missing usage from failed transport requests prevents treating this estimate as an exact bill. Supplying optional `--controls` analysis files adds controls to the task-performance comparison.

The plotted intervals concern known finite-bank synthetic outcomes and have marginal guarantees under the stated assumptions. The number of plotted conditions containing the target is not an empirical coverage estimate. Action-only and context-aware rows reuse the same field observations; aggregate competence counts each field task once.

An explicitly exploratory cross-model transport analysis reuses existing records:

```sh
python3 experiments/v2/analyze_transport.py \
  --calibration results/model-study-mini --field results/model-study-nano \
  --output results/model-study-controls/transport-mini-to-nano.json
```

That sensitivity analysis violates the stable-channel assumption by design. Its intervals have no stated coverage guarantee, it is not part of the frozen primary experiment, and it makes no additional model calls.

## Exploratory explicit-preference receipt extension

The primary experiment left all tested decisions unresolved. The following separately frozen follow-up asks whether adding an explicit, limited preference report helps. It is motivated by that result and must not be described as part of the original preregistered experiment.

```sh
python3 experiments/v2/prepare_receipts.py \
  --source results/model-study-mini --output results/receipt-study-mini
```

The default selection takes the first 40 lexicographic IDs in each calibration class and the first 80 IDs in each field cohort, within each domain, then preserves the original execution order. No response value or utility determines selection. This creates 1,200 requests per model. The paired original-action baseline uses exactly those task IDs and budgets from already collected responses.

The new question asks which attribute has the largest weight in the preferences already supplied to the agent. It does not ask the model to infer unknown preferences. The task reduces to 12 distinct prompts, four weight profiles in three domain framings, repeatedly queried to estimate the response channel. These are not 1,200 different human customer decisions. `choice_id` now represents an attribute ID. The prepared manifest states the mapping and records this change of measurement.

After actual receipt responses have been collected using the same `run_live.py` pipeline:

```sh
python3 experiments/v2/analyze_receipts.py \
  --prepared results/receipt-study-mini --source results/model-study-mini \
  --output results/receipt-study-mini/comparison.json
```

The comparison reports preference-report accuracy and decision bounds. Product-choice utility and regret are inapplicable to the receipt and are removed from its output. Synthetic future-product outcome contrasts remain those of the original independent finite menu bank. A useful receipt result would establish the value of explicitly collecting relevant information in this constructed task; it would not establish real-customer validity, general preference discovery, privacy protection, or a novel partial-identification estimator.

After both receipt comparisons are complete:

```sh
python3 experiments/v2/plot_receipts.py \
  --mini results/receipt-study-mini --nano results/receipt-study-nano \
  --output results/receipt-study-summary --pricing experiments/v2/pricing.json
python3 scripts/reproduce_model_results.py --require-receipts
```

The comparison figure checks matched task budgets and outcomes, labels the repeated 12-prompt measurement task, and displays action-only and attribute-only channels. The summary records receipt failures and usage separately from the original experiment. Exact reproduction reruns analysis against recorded responses, including the paired original-action subset, without contacting any model provider.
