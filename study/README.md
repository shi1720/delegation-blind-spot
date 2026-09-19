# Offline investigator preview

This folder is a **preview instrument**, not an active study and not human validation. It creates only records labeled `instrument_preview_not_human_evidence`. Its code rejects participant mode and never claims to verify who supplied a response. Do not count records from this folder as people in a manuscript.

## Open and test

Open `index.html` in a modern browser. It works from a local file and does not need a server, account, or network. Complete the five steps and download the full and action-only JSON files. Closing or reloading discards the in-memory record. Downloads remain on the device until deleted.

The site makes no external calls, stores no cookies or browser storage, and requests no names, contact details, demographics, or free text. Its content-security policy disables network connections and form submission. No exporter uploads data. The random preview ID is not a verified participant ID; do not join it with identities. An investigator handling future real records still needs a defined retention and deletion process.

Run the core checks:

```sh
node study/test-instrument.cjs
node --check study/instrument.js
```

The automated checks validate assignment boundaries, reference recommendations, and prevention of human-evidence export claims. They do not establish accessibility, consent validity, or browser compatibility. A separate automated Chromium browser pass is recorded in `qa-report.md`; it is tool testing, not participant data. Before real deployment, test keyboard navigation, screen readers, narrow viewports, downloads, reload clearing, and both randomized conditions on supported browsers.

## Instrument structure

1. Preview information and acknowledgment. This is explicitly not research consent.
2. Preference elicitation before choices: quietness weight and confidence.
3. Random assignment with probability 1/2 to an unaided choice or a deterministic reference recommendation. Hotel display order is separately randomized.
4. Independently reported fit, a future-improvement tradeoff, clarity, and burden.
5. Review and local JSON export.

The preference elicitation is separated from the action-only export. It is **not private from the study investigator** if the full record is shared. Both arms provide preferences first, which can itself prime later choice. This is a design limitation, not a model of untouched natural browsing.

The recommendation is a declared arithmetic rule:

`score = w * quietness/10 + (1-w) * (30 - travel_minutes)/30`

where `w = quietness_weight/100`. It recommends the maximum score and uses stable option ID order to break exact ties. This is not a live language-model agent and must not be described as one. A later actual human-agent experiment must use recorded, authenticated model responses or a live model pipeline with accurate provenance, privacy controls, and relevant consent. Adding an AI label to the current rule is not an acceptable substitution.

All choices are hypothetical and carry no cost or actual booking. The fit rating is a self-report, not an experienced-stay outcome. The future-improvement answer is a stated tradeoff, not willingness to pay. Choice, stated preference, confidence, and satisfaction are different measurements and should stay separate.

## Before recruiting actual participants

This version intentionally cannot be activated by a `config.js` flag. Prepare and independently review a participant-specific instrument and protocol first. Required decisions include:

- Named investigator and a monitored study contact.
- Institutional ethics review, exemption, or documented applicable determination. Do not invent an approval or imply that a preview constitutes one.
- Recruitment population, adult eligibility, compensation, consent, withdrawal, retention, secure transfer, and deletion procedures.
- Whether the task remains hypothetical or has real consequences; clearly explain either.
- The actual recommendation system and what participant information it receives, stores, or sends to a model provider.
- A recruitment and assignment mechanism preventing duplicate entries without collecting unnecessary identity data.
- Fixed primary research question, minimum meaningful effect, planned sample size and stopping rule, exclusions, assignment protocol, and analysis.

No participant recruitment, public hosting, data collection, or ethics application has been performed. A code test does not count as a consenting participant. Synthetic personas must remain labeled simulation records in a separate dataset.

`consent-draft.md` is an investigator drafting aid with unresolved placeholders. It is not ready to show to participants or to describe as approved.

## Proposed analysis for a real pilot

This plan is a draft, not a registered protocol. Freeze it before actual participant collection after reviewing the final task and ethics requirements.

**Feasibility objective:** determine whether participants understand the distinctions, can complete the task without undue burden, and interpret the follow-up tradeoff as intended. Report task completion, missingness, clarity, and burden. Do not infer a population effect from a small convenience pilot.

**Candidate primary scientific estimand:** the difference between randomized aid conditions in the probability that the available action-only observations resolve a predeclared future product contrast, at a fixed measurement budget. This requires enough participants, a separate calibration set, a defensible target contrast, and uncertainty propagation. The present single-task preview does not itself estimate that quantity.

**Secondary outcomes:** independently elicited future-improvement preference, reported fit, override frequency in the aided arm, and decision time. Do not score the deterministic aid against the exact utility rule that created its recommendation and call that independent human validation.

**Calibration and evaluation:** fit or calibrate channels only on the designated calibration partition. Evaluate bounds on a held-out partition. If there are multiple tasks per participant, split by participant and cluster uncertainty at the participant level. Report unresolved decisions as abstentions alongside wrong decisions. Do not select only resolved or compliant records.

**Comparison:** compare action-only inference with direct outcome elicitation and the decision-specific bounded diagnostic. Distinguish a randomized causal effect of aid on measured responses from inference about latent customer utility. Assignment may change preferences, comprehension, or reporting itself.

**Power:** select the minimum effect worth detecting and obtain a pilot variance or a justified conservative bound. Simulate the planned design to set sample size before the main study. No defensible participant count is inferred from the number of model calls or synthetic repetitions.

**Exclusions:** predeclare ineligibility, lack of consent, duplicate handling, technical failures, and withdrawal. Never exclude a participant merely for disagreeing with the recommendation. Report denominators for randomized, completed, analyzed, and withdrawn records.

**Integrity:** retain immutable source records and versioned analysis; separately label instrument tests, model simulations, and authentic participant records. No checkbox or local ID can retrospectively certify a human dataset. The investigator must document recruitment and consent provenance without publishing identities.

## Files and limitations

- `index.html`: accessible semantic five-step layout, responsive styling.
- `instrument.js`: in-memory flow, cryptographic random assignment, local exports.
- `instrument-core.js`: declared reference rule and export integrity checks.
- `config.js`: preview-only configuration and unresolved study information.
- `test-instrument.cjs`: core tests without external packages.
- `consent-draft.md`: investigator-only consent checklist and drafting scaffold.

This artifact reduces preparation work for a real study. It does not satisfy the paper's missing human evidence, prove the task has ecological validity, or certify a production research deployment.

## Browser QA reproduction

With Playwright and its Chromium browser installed, run `node study/browser-qa.cjs`. If Playwright is supplied in a separate package directory, set `PLAYWRIGHT_PACKAGE_ROOT` to that node_modules directory. The script uses local file URLs, tests actual random assignment until both arms are seen, and writes screenshots and a machine-readable report under `study/qa-artifacts/`. Downloaded test responses are temporary and are not committed as participant records.
