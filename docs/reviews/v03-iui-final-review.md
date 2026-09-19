# Final internal IUI 2027 poster review

Review date: 20 September 2026. This is a skeptical AI-assisted internal review, not an official venue review, external approval, or evidence that a submission has been made.

## Material inspected

- `paper/submission/iui-poster.tex` and all four rendered pages of `output/pdf/iui-poster.pdf`, including references.
- The recorded primary and receipt results, the deterministic parser output, and the controlled sensitivity summary.
- The functioning offline inspector, whose earlier functional QA covered all 72 recorded conditions at desktop and mobile sizes. No participant study was conducted.
- The current official IUI and CHI poster calls, accessed again on the review date.

Reviewed source SHA-256: `2348090a6dbab20cfa071a827b453cbfd894972b36b85b79b44b8788ff191cb6`.
Reviewed PDF SHA-256: `cb256351a697595cf0b62ec354794665fd7dbfb3fad2bab733afff96cdaff9d2`.
These identify the reviewed versions; later edits require a corresponding final check.

## Conditional verdict

**Weak accept as an IUI work-in-progress poster, conditional on the human author completing the submission checks below.** I found no remaining manuscript-level blocker in this version. This is not a recommendation to submit it as a completed, generalizable human-preference study, a new identification theorem, or a validated decision-support system.

The defensible contribution is now narrow and visible: a decision-specific measurement audit, compatible endpoint witnesses, an inspectable research prototype, and computational controls that prevent a negative result from being misread as an impossibility result. The paper provides a useful conversation for researchers building interfaces between delegates, customers, and product analysts. The strongest scientific improvement is its separation of task execution, measurement precision, and structural identification. Its strongest remaining weakness is the absence of evidence that real analysts understand or benefit from the proposed interface.

Internal scores use a five-point scale where five is strongest. They are not IUI's official scoring rubric.

| Dimension | Score | Assessment |
| --- | --- | --- |
| IUI poster fit | 4/5 | An early computational result and concrete interface question, with a functioning diagnostic artifact. |
| Originality | 3/5 | Useful operational synthesis. The mathematical foundations and broader delegated-preference problem are established. |
| Technical support for stated claims | 4/5 | Real recorded model calls, conservative bounds, explicit controls, and restrained interpretation. No real-demand inference. |
| Clarity | 4/5 | Self-contained and readable. The sensitivity paragraph remains compressed. |
| Human-centered contribution | 3/5 | A plausible analyst workflow and evidence-provenance distinction; its practical value remains untested. |
| Overall poster recommendation | 3/5 | Borderline favorable / weak accept for discussion, not a full-paper acceptance prediction. |

## Blocking issues

**No identified manuscript-level blockers.** In particular, the previous overlength, template, missing concrete artifact, and missing research-AI disclosure concerns have been addressed.

The following are submission prerequisites outside this manuscript review, not completed facts:

1. A human author must scrutinize the methods, claims, references, and authorship responsibilities. AI reviews and passing tests do not provide independent human verification.
2. Complete accurate PCS author, affiliation, conflicts, track, and any requested disclosure fields. Confirm the intended submission and presentation arrangements. A LaTeX footer saying “Manuscript submitted to ACM” does not establish that PCS submission occurred.
3. Verify the uploaded artifact and repository are accessible and match the reviewed release. This review did not audit a live PCS record or certify every public repository file.
4. Complete an accessibility check of the actual uploaded PDF, including screen-reader order. The figure has a useful `\Description`, text is selectable, and visual reading is good; those observations are not a full accessibility certification.

## Format and venue checks

The current [IUI 2027 call](https://iui.acm.org/2027/call-for-posters-demos/) permits four pages excluding references, single-column ACM format, and requires CCS. The deadline is 10 November 2026, 23:59 AoE. A draft visual poster is recommended, not mandatory. Accepted work is expected to be presented in person.

The PDF has four pages **including** references. It uses the supplied `manuscript,review,anonymous` class options, and PDF metadata identifies acmart 2.20. The source contains two relevant CCS descriptions. No manual margin, line-spacing, or font-size compression is visible in the manuscript source. The public repository identifies the author, but IUI explicitly says anonymization is unnecessary even though its example uses `anonymous`. This combination is therefore not a rejection issue under the current wording. It should not be described as a strictly anonymous package.

The same files are **not ready for CHI submission**. The [CHI 2027 poster call](https://chi2027.acm.org/authors/posters/) requires anonymity, an A0 poster, and key discussion points; its deadline is 21 January 2027. A named repository link would need appropriate anonymization. Do not assume IUI compliance transfers to CHI.

## Scientific claims and evidence

The primary result is stated accurately as 4,800 attempts, 4,783 valid choices, 17 retained failures, and zero resolved comparisons out of 18 per model. The different execution accuracies are not treated as proof that capability and information are unrelated. The optimal-choice control is explicitly reported, and all-unresolved intervals are correctly attributed to the tested procedure and budget rather than established structural information loss.

The follow-up is clearly exploratory: 1,200 additional requests per model but only 12 distinct prompts. Its perfect reporting is retrieval of supplied synthetic weights, not latent preference discovery or customer validation. Reporting 3/9 versus 0/9 at matched observation counts is appropriately qualified by unequal costs and absent selective-inference adjustment. The deterministic parser's 7/9 result is a valuable counterweight to a claim that another LLM call is necessary.

The sensitivity family explicitly distinguishes an exactly unidentified channel at zero strength from full-rank but weak channels at positive strength. The 14,400 generated datasets and unequal nominal guarantees across ablations are disclosed. This makes the statistical caveat substantive rather than merely defensive. The parser and sensitivity outputs inspected are consistent with the corresponding reported claims.

The row-space statement is correctly described as a standard fact. The noisy-channel LP endpoints are attainable within the stated rectangular restrictions, not claimed as universally optimal uncertainty regions. Coverage is marginal, conditional on sampling and calibration assumptions; the paper expressly disclaims protection against a wrong outcome model and simultaneous coverage over all comparisons. It correctly says the two endpoint witnesses need not use one identical exact channel.

Closest direct overlaps are acknowledged through Kops and Tsakas, Kraft and Larsen, Suleymanov, and ABxLab, alongside Blackwell, label shift, and measurement-error partial identification. The paper does not support a priority claim over all adjacent literature, and it currently makes none. Its novelty should remain the executable decision audit and proposed evidence interface, not a renamed impossibility theorem.

## Rendering, figure, and remaining nonblocking improvements

All four pages were visually inspected at 110 dpi. No clipped text, overlapping elements, broken equations, unresolved citations, or overflowing tables were observed. The page-two figure is readable and accurately captioned as a compact rendering of recorded inspector data, not a screenshot of a tested user interface. It displays a zero-crossing interval and alternative synthetic witnesses without presenting them as actual customer segments.

Nonblocking refinements, in priority order:

1. Split the long “Separating uncertainty sources” paragraph into sensitivity and direct-measurement controls if layout permits. The present version is legible, but this is the highest cognitive-load passage.
2. Add a short table note that the parser uses a known identity channel while the model reports retain estimated-channel uncertainty. The explanation already appears in the prose, so this is clarity rather than a missing methodological disclosure.
3. Clean incomplete bibliography metadata where authoritative records supply it. The build warnings concern metadata, not missing citations. Do not invent volume, publisher, or page values for preprints.
4. A discussion poster could foreground one question: can analysts distinguish an information gap from a precision gap when viewing the same unresolved interval? This is a concrete next study, not evidence already obtained.

No new model calls or synthetic personas are needed to remove these presentational issues. Real analyst evaluation would strengthen a future full paper but is not automatically required for this explicitly scoped WIP submission.

## Research-AI disclosure

The “AI-assisted research methods” paragraph discloses assistance with formulation, retrieval, proofs, design, implementation, analysis, figures, and writing. It distinguishes the tested models from the research-assistance workflow and internal AI critique from independent peer review. It describes checks without claiming that they replace human accountability. This is materially more appropriate than describing the process as writing assistance alone.

The relevant policy is the [ACM Policy on Authorship](https://www.acm.org/publications/policies/new-acm-policy-on-authorship), including its research-use disclosure provisions reviewed earlier in this audit. The official policy mirror returned HTTP 403 on the final refresh, so this report does not claim a fresh complete policy fetch. The current IUI call still explicitly incorporates that policy. The final author should retain an accurate disclosure, not remove it to make the work appear less AI-assisted.

## Release judgment

The reviewed document is a plausible IUI poster submission artifact after human-author and portal checks. It is not externally reviewed, accepted, submitted, human-validated, or a production decision tool. No evidence in this review supports describing synthetic users as real people, and the current paper consistently avoids that error.
