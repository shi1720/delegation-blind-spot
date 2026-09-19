# Decision Evidence Inspector

A functioning offline research prototype for inspecting **precomputed** results from the Delegation Blind Spot computational study. It is separate from the nonactive participant-study preview in `study/`.

Open `inspector/index.html` directly in a modern browser. There is no hosting requirement, network request, model call, analytics, storage, or user-data collection. The page displays 72 recorded conditions through model, task-framing, synthetic-cohort, and observation-schema selectors.

## What the viewer shows

- Primary action-only and context-plus-action bounds.
- Paired follow-up action-only and explicit-preference receipt bounds.
- The known synthetic class-level contrast d, calibration/field counts, and field failures.
- Compatible lower/upper endpoint mixtures and their implied contrast.
- Observed, supplied, inferred, and customer-confirmed evidence as distinct categories. Customer confirmation is explicitly absent.
- Source paths, SHA-256 hashes, and recorded solver constraint residuals.

True evaluation population proportions and target contrasts are omitted from the embedded data. Cohorts are labeled A/B/C without sign-revealing population names. The known class contrast d remains visible because it is an assumption supplied to this diagnostic. It is not a measured human outcome.

The endpoint mixtures are witnesses under recorded channel and field uncertainty boxes, not estimated population proportions. Lower and upper witnesses need not use the same exact channel. The viewer does not run a linear program or independently recertify the full constraint system. Its builder checks witness simplex sums and implied endpoint contrasts against stored results.

## Build and test

From the repository root:

```sh
python3 inspector/build_data.py
node inspector/test-core.cjs
node --check inspector/app.js
```

The builder reads only the two recorded primary analyses and the two completed receipt comparisons. It emits deterministic `data.js` with hashes of its source files. No raw model calls or external dependencies are needed. A source change requires rebuilding the dataset and reviewing the changed provenance. The core test covers every selection and the withheld evaluation-truth boundary.

## Interpretation

The primary sample has 80 calibration records per class/domain and 160 field records per cohort/domain. The follow-up has 40 and 80 respectively. Compare receipt reporting against **Follow-up / matched actions** for equal observation counts, not against the larger primary sample. Equal counts are not equal costs, privacy exposure, or elicitation burden.

The follow-up is exploratory, selected after the primary results. It repeats 12 distinct supplied-weight prompts per model and lacks selective-inference correction. Reporting an explicit weight is not discovering a real customer's preference. A deterministic parser could extract that field. The nominal primary marginal guarantee requires stable channels, a finite declared intent taxonomy, and the stated sampling design; it is not simultaneous coverage or a drift guarantee.

This is an inspectable scientific artifact, not a validated commercial decision tool or a deployed intelligent interface. No user study establishes usability or decision quality. Browser testing, where recorded, is automated software QA and never customer validation.

## Browser QA and figure source

The final [QA report](qa-report.md) records 144 checked viewport/condition combinations in local headless Chromium, including keyboard navigation and no-network assertions. Run `node inspector/browser-qa.cjs` with Playwright/Chromium installed; a separate package location can be supplied through `PLAYWRIGHT_PACKAGE_ROOT`.

For an illustrative paper screenshot, `qa-artifacts/desktop-primary.png` shows an unresolved recorded condition and its compatible witnesses. `qa-artifacts/desktop-receipt.png` shows the corresponding explicit-preference follow-up. These are actual rendered prototype states, not a usability study or generated mockups. Sample budgets differ between the primary and follow-up screens; use the matched-action selector for an equal-count comparison.
