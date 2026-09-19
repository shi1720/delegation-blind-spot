# Investigator preview QA

Tested 19 September 2026 using headless Chromium 151.0.7922.34 and local `file://` URLs. No server, hosting, recruitment, or participant collection was used. Every input was an automated tool-test response.

## Results

Four completed browser flows covered both unaided and reference-aided conditions at desktop 1440 x 1000 and mobile 390 x 844. Actual cryptographic assignment happened to produce both arms within two runs for each viewport; random assignment was not overridden.

Passed:

- Preview acknowledgment required before proceeding.
- Preference certainty, hotel selection, and all four outcome answers required.
- Checkbox activation with Space, navigation with Tab, button activation with Enter, slider adjustment with ArrowRight, and radio selection with Space.
- Focus moves to the new step heading when progressing.
- Reference-aided condition explicitly identifies the arithmetic rule and says it is not live AI.
- Full and action-only downloads succeed and use `PREVIEW-NOT-HUMAN-DATA` filenames.
- Full records label themselves `instrument_preview_not_human_evidence`, set human verification false, and say research consent was not collected.
- Action-only export omits preference and outcome answers while preserving the same choice and preview labels.
- Clear/restart returns to the first step and hides the completed record view.
- No local or session storage entries and no HTTP(S) requests observed.
- No browser JavaScript errors and no horizontal overflow at the checked choice screens.

Desktop and mobile reference-aided full-page screenshots were visually inspected. Text, recommendation, hotel attributes, radio controls, and buttons were readable with no collisions or clipping. The mobile layout stacks attributes and uses full-width primary buttons. Unaided screenshots were also saved; the automated flow checked their behavior and layout width.

## Artifacts and reproduction

- `browser-qa.cjs`: reproducible local browser test.
- `qa-artifacts/browser-qa-results.json`: browser version and individual test-case results.
- `qa-artifacts/desktop-reference_aided.png` and `mobile-reference_aided.png`: inspected screenshots.
- Corresponding unaided screenshots: saved test artifacts.

Run with an installed Playwright package and browser using `node study/browser-qa.cjs`, or supply `PLAYWRIGHT_PACKAGE_ROOT` for a separate package directory. The core test file separately passes 14 assertions.

## Limits

This is a Chromium functional and visual check, not a complete accessibility audit or cross-browser certification. Select menus were populated through browser automation rather than a full keyboard-only end-to-end traversal. Screen readers, Safari, Firefox, touchscreen hardware, long text translations, and live participant comprehension were not tested. The tool-test responses are not human or customer evidence and must never enter a participant dataset. No ethics status or consent validity is inferred from these tests.
