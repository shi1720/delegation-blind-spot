# Version 0.2.0 release validation

Validated 19 September 2026. This report concerns the computational artifact, not peer review, human validation, or venue acceptance.

## Recorded checks

- Python: 63 unit tests passed, including identification, proof-derived boundary cases, uncertainty bounds, experiment record validation, receipt comparisons, and plotting summaries.
- Offline study preview: 14 core assertions passed. Separate browser QA covered desktop and mobile in both reference-aided and unaided flows. See `study/qa-report.md`.
- All four model analyses reproduced with exact JSON equality: Mini primary, Nano primary, Mini receipt with paired original actions, and Nano receipt with paired original actions. Reproduction made no provider calls.
- Sixteen compressed raw-record artifacts passed compressed and expanded SHA-256 checks. Existing differing local files are not overwritten by the unpacker.
- All returned model identifiers in the completed runs match the requested pinned snapshots. Failed transports are retained without substituted responses.
- The primary plan was pushed in commit `ab59d81` before its API calls. The exploratory receipt plan was pushed in `b766cae` before its new API calls. The follow-up was motivated by the primary results and is not presented as confirmatory preregistration.
- Final PDF: 14 pages, searchable text, 50 link annotations, generated numerical tables, four vector research figures, bibliography and full proof appendix. Every page was rendered and visually inspected. A table overflow was corrected; the final build has no overfull-box, unresolved-reference or missing-glyph warning. Minor underfull-line warnings remain from mathematical and narrow-column typesetting.
- PDF extraction contains the verified response totals and receipt interval widths, with no unresolved citation markers or em dashes.
- Credential-pattern scan passed for repository candidates and expanded compressed response records. Credentials are supplied only through the execution environment and are not included in the release.
- `git diff --check` passed after documentation whitespace cleanup.

## Evidence ledger

| Study | API attempts | Valid responses | Retained transport failures |
| --- | ---: | ---: | ---: |
| Primary | 4,800 | 4,783 | 17 |
| Exploratory receipt follow-up | 2,400 | 2,400 | 0 |
| Total | 7,200 | 7,183 | 17 |

The excluded one-call connectivity check is not part of these counts. Primary tasks use synthetic profiles and known synthetic utility rules. Receipt calls repeat 12 distinct supplied-weight prompts per model. None represents a recruited person or customer outcome.

The primary diagnostic leaves all 36 reported conditions unresolved. In the matched-count exploratory comparison, receipts resolve 3 of 9 conditions per model versus 0 of 9 for original actions. Six receipt conditions per model remain unresolved. The mean interval width falls from 0.0872040609 to 0.0435969805. These are descriptive benchmark results, with no correction for choosing the follow-up after seeing the primary result.

## Reproduce

```sh
python3 -m pip install -r requirements.txt
make test
make reproduce
python3 paper/build_results.py
make paper
```

`make paper` requires Tectonic. The separate browser QA script requires Playwright. Neither is needed to rerun the recorded numerical analysis. API requests are necessary only for an explicitly requested new live run, which need not reproduce provider outputs exactly.

## Remaining external requirements

Real customer recruitment and evidence, independent expert review, human-author review, a selected venue's format and disclosure requirements, and any ethics determination remain separate requirements. The investigator preview is deliberately not an active participant-collection system. The release is a technical preprint and reproducible research artifact, not a validated commercial product or accepted paper.
