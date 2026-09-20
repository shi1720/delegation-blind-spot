# Submission plan and live status

Checked 20 September 2026. **No paper has been submitted.** Prepared files are not evidence of submission, acceptance, or peer review. The following are the three most suitable options among the verified calls, ranked by fit for the current computational scope rather than prestige alone.

| Rank | Venue and track | Deadline (AoE) | Fit and package |
| --- | --- | --- | --- |
| 1 | [ACM IUI 2027 Posters](https://iui.acm.org/2027/call-for-posters-demos/) | 10 November 2026 | Best fit: an inspectable decision-support workflow with a bounded computational study. Official single-column ACM manuscript and figure description prepared. |
| 2 | [ACM CHI 2027 Posters](https://chi2027.acm.org/authors/posters/) | 21 January 2027 | Good fit for the measurement and interface-design questions. Anonymous single-column manuscript, anonymous A0 visual poster, and discussion points prepared. No human usability claim. |
| 3 | [The Web Conference 2027 Short Papers](https://www2027.thewebconf.org/research-track-papers/) | Abstract 9 November; paper 16 November 2026 | A more demanding alternative, focused on agentic Web users and platform measurement. Anonymous two-column draft prepared. Its short-track form and precise length requirement still require verification after login. |

## Concurrent review

The [ACM simultaneous-submission policy](https://www.acm.org/publications/policies/simultaneous-submissions), read on the live publisher site, normally prohibits overlapping review and requires explicit published exceptions and notification of all affected chairs. The Web Conference call explicitly excludes work under review at a peer-reviewed conference or journal with proceedings. CHI describes its poster content as non-archival and reusable, but that does not itself establish permission from every other venue for concurrent review. Do not tick an exclusivity declaration that is untrue or silently submit these versions simultaneously. Formatting changes and title changes do not make them independent studies.

Recommended route: arXiv plus IUI as the first conference target. Reassess CHI using the IUI decision and the applicable overlap rules. WWW is an alternative archival target, not an additional simultaneous archival submission. No chair has granted an exception. No letters have been sent.

## Account and portal status

- PCS: one login attempt using the author's supplied credentials failed. Registration is filled with name and email; CAPTCHA completion awaits the browser-required action-time confirmation. No account or submission confirmation has been received.
- arXiv: one supplied-credential login attempt failed. First registration page is filled, with CAPTCHA and privacy-policy acceptance awaiting action-time confirmation. No account, endorsement, upload, or article identifier exists from this workflow.
- OpenReview: the WWW Short Papers portal is visibly open, with a submission button and November deadlines. Login explicitly accepts its Terms of Use. Action-time confirmation is pending; no login attempt or submission has been made here.
- Credentials are not stored in this repository.

## Format and author checks

The IUI and CHI paper limits are four body pages excluding references. Their templates are unmodified official `acmart`; the anonymous CHI PDF omits identifying artifact links and author metadata. The A0 poster contains no identifying name, email, or repository URL. The WWW draft uses the official `sigconf,review,anonymous` class and states Web relevance on page one. Its shared call lists an eight-page body/twelve-page total limit without clearly separating the short-paper specification; verify the short-track form before calling the draft submission-ready.

CHI requires four review-responsibility slots assigned to actual authors. Do not invent coauthors; the portal must determine whether a sole author can cover the slots. IUI and CHI require registration and presentation if accepted. WWW requires conference registration and may require an APC for an unaffiliated corresponding author. No fees have been paid or committed.

Use Shivam Gupta and shivam1720406@gmail.com consistently. The technical report uses Independent Research, without attributing this work to a former employer. Institutional conflicts and author declarations must be answered truthfully from the author's history, with clarification for information not established by the resume or other author-provided records.

## CHI key discussion points

When a product team cannot distinguish competing customer-value hypotheses from an agent's actions, what should its interface show and what should it measure next? The poster invites three concrete discussions: which supplied preference fields merit retention; how consent, privacy and burden should limit decision receipts; and how to present endpoint witness populations without encouraging analysts to mistake them for estimates of real customers. We seek feedback on the design of a genuine analyst study and customer-outcome validation, neither of which this computational paper claims to have completed.

## arXiv package

`python3 scripts/package_arxiv.py` creates `output/submission/delegation-blind-spot-arxiv-source.zip` with root `main.tex`, bibliography source and compiled `.bbl`, appendix, generated result sections and all five vector figures. It contains no rendered manuscript PDF or unrelated source. `arxiv-source-manifest.json` records each dependency hash. A local isolated Tectonic build passes. The arXiv server's selected TeX processor and compiled preview must still be verified after upload. Suggested primary category: cs.HC; cs.AI may be considered as a cross-list if appropriate under moderation. Do not claim endorsement, moderation approval, or a submission identifier before they exist.
