# Inspector QA

20 September 2026. Automated software checks only, not a user study.

- Rebuilding `data.js` from the same four source analyses produced identical bytes. SHA-256: `8d7159c2b415812b6263734a1cfa25891b3cfd756895049ca8a79f76ae52a892`.
- Core tests verified all 72 selections, endpoint witness dot products and simplex sums, declared decisions, sample counts, and omission of evaluation-only truth.
- Headless Chromium 151.0.7922.34 exercised all 72 conditions at 1440 x 1100 and 390 x 844, checking displayed intervals, decisions, and witness endpoints against the embedded recorded data.
- Keyboard Tab navigation, Enter activation of the assumptions disclosure, reset behavior, source hashes, and model identifiers passed.
- No HTTP(S) requests, browser errors, console/CSP errors, browser storage, or document-level horizontal overflow occurred in the final pass.
- Initial mobile grid overflow was fixed. The witness table now stays within a keyboard-focusable, horizontally scrollable region with an explicit mobile scroll cue. Chart tick spacing adapts to the available width.
- Desktop primary/receipt and mobile primary/receipt screenshots are in `qa-artifacts/`. Desktop primary, desktop receipt, and mobile views were visually inspected for readability and collisions.

Reproduce with Playwright and Chromium installed:

```sh
node inspector/browser-qa.cjs
```

Set `PLAYWRIGHT_PACKAGE_ROOT` if Playwright lives in a separate node_modules directory. The test reads local file URLs and makes no API calls. A machine-readable report is in `qa-artifacts/browser-qa-results.json`.

Limitations: Chromium only; no screen-reader, Safari, Firefox, or real-user usability validation. The browser displays precomputed bounds and does not rerun the LP or establish statistical assumptions. Passing software checks does not make the tool a validated product-decision system.
