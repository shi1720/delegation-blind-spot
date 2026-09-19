# Submission-package reference metadata check

Checked 20 September 2026. Scope: all 13 entries in `paper/references.bib`, including all seven short-paper citations and the six remaining full-report/background entries. Changes are limited to bibliography metadata; citation keys are preserved. The first pass covers the short paper below, followed by the full-report pass.

This checks bibliographic identity and available publication metadata, not independent replication of the cited results or exhaustive literature coverage.

| Key | Authoritative record checked | Result and changes |
| --- | --- | --- |
| `finkelstein2021` | [PMLR publisher record and provided BibTeX](https://proceedings.mlr.press/v161/finkelstein21b.html) | Title, four authors, 2021, volume 161, and pages 1798–1808 confirmed. Expanded the exact proceedings and series names; added editors Cassio de Campos and Marloes H. Maathuis and publisher PMLR. |
| `lipton2018` | [PMLR publisher record and provided BibTeX](https://proceedings.mlr.press/v80/lipton18a.html) | Title, three authors, 2018, volume 80, and pages 3122–3130 confirmed. Matched the publisher's author rendering “Zachary Lipton”; expanded proceedings and series names; added editors Jennifer Dy and Andreas Krause and publisher PMLR. |
| `blackwell1953` | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.1214/aoms/1177729032) | Title, David Blackwell, journal, volume 24, issue 2, pages 265–272, June 1953, and DOI confirmed. Added publisher Institute of Mathematical Statistics and publication month. The Project Euclid page did not expose usable text to the browser, so Crossref was used for deposited metadata. |
| `kops2026` | [arXiv primary record](https://arxiv.org/abs/2602.04526) | Christopher Kops and Elias Tsakas, title, February 2026, and identifier confirmed. Changed the entry from a journal article to a preprint (`misc`); added the arXiv-issued DOI, eprint, archive, subject, and month. No journal publication or invented pagination is asserted. |
| `kraft2026` | [SSRN primary record as indexed](https://papers.ssrn.com/sol3/Delivery.cfm/6864181.pdf?abstractid=6864181&mirid=1), corroborated by [Andreas Kraft's research page](https://krandreas.github.io/research.html) | Andreas Kraft and Poet Larsen, exact title, June 2026, working-paper status, SSRN ID 6864181, and DOI 10.2139/ssrn.6864181 confirmed. Changed the article entry to a working-paper `misc` entry and added DOI/month. Direct SSRN abstract retrieval returned 403; the indexed SSRN record supplied its own suggested citation. Its “Chicago Booth Research Paper Forthcoming” label was not converted into an invented journal or series number. |
| `cherep2025` | [Official ICLR 2026 paper listing](https://iclr.cc/virtual/2026/papers.html), [MIT Media Lab author publication page](https://www.media.mit.edu/publications/abxlab/), and [arXiv record](https://arxiv.org/abs/2509.25609) | The work is now an ICLR 2026 publication. Updated type to `inproceedings`, year to 2026, conference title, and [OpenReview record URL](https://openreview.net/forum?id=LUrToUPS4x). Preserved the six-author list as given by MIT and arXiv. The historical key `cherep2025` remains unchanged to avoid breaking citations; it no longer denotes the publication year. The preprint was first posted in 2025 and revised in February 2026. OpenReview itself required browser verification; official ICLR and author records independently establish the venue. No publisher, page range, volume, or conference DOI was invented. |
| `suleymanov2026` | [arXiv primary record](https://arxiv.org/abs/2603.27868) | Elchin Suleymanov, exact title, March 2026, and identifier confirmed. Changed the entry from a journal article to a preprint (`misc`); added the arXiv-issued DOI, eprint, archive, subject, and month. |

## Bibliography conventions

- Protected “AI” from BibTeX sentence-case conversion in the three affected titles.
- arXiv-issued DOIs identify deposited preprints. They do not imply journal peer review.
- PMLR fields match its supplied citation metadata. A missing publisher address was not fabricated merely to suppress a style warning.
- ICLR's conference entry legitimately lacks a verified page range, volume, and publisher address in the consulted records. Retaining an optional-metadata warning is preferable to incorrect bibliography data.
- No claims of new publication status were made for the Kops, Kraft, or Suleymanov works.

## Validation and rebuild handoff

Static checks found 13 unique bibliography keys, with all seven short-paper citation keys present. All original keys remain available. The parent task owns rebuilding and rendering the submission and full report after these changes; this metadata audit does not claim a new PDF was inspected. The expanded PMLR records and corrected ICLR year can change bibliography line wrapping, so the final four-page check must use the rebuilt PDF.


## Remaining full-report references

The six additional records were checked on the same date. Existing complete entries were retained rather than expanded simply to eliminate optional style warnings.

| Key | Authoritative sources | Check and update |
| --- | --- | --- |
| `kirschner2023` | [JMLR publisher record](https://jmlr.org/papers/v24/22-1248.html) and its supplied [BibTeX](https://jmlr.org/papers/v24/22-1248.bib) | Three authors, exact title, year 2023, volume 24, article/issue 346, and pages 1–45 all match. No change needed. |
| `donoho1994` | [Author-hosted published article](https://web.stanford.edu/dept/statistics/cgi-bin/donoho/wp-content/uploads/2018/08/SEOR.pdf) and [publisher-deposited Crossref record](https://api.crossref.org/works/10.1214/aos/1176325367) | Author, title, journal, year, volume 22, issue 1, pages 238–270, and DOI confirmed. Crossref omits pagination, so the original article's first-page imprint is the source for it. No change needed. |
| `lattimore2020` | [Cambridge book page](https://www.cambridge.org/core/books/bandit-algorithms/8E39FD004E6CE036680F90DD0C6F09FC), [publisher front matter](https://assets.cambridge.org/97811084/86828/frontmatter/9781108486828_frontmatter.pdf), and deposited Crossref metadata | Title, both authors, Cambridge University Press, and 2020 confirmed. Added DOI 10.1017/9781108571401 and restored the accent in Szepesvári using TeX syntax. Retained the author's accessible full-text URL. This key is currently not cited by `paper/main.tex`; it remains available and does not justify inserting an unnecessary citation. |
| `ppi2023` | [AAAS-deposited Crossref record](https://api.crossref.org/works/10.1126/science.adi6000) and [author arXiv record](https://arxiv.org/abs/2301.09633) | All five authors, title, Science volume 382, issue 6671, pages 669–674, year 2023, and DOI match. No change needed. |
| `asi2024` | [PMLR publisher record and supplied BibTeX](https://proceedings.mlr.press/v235/zrnic24a.html) | Two authors, title, year 2024, volume 235, pages 62993–63010 confirmed. Expanded exact proceedings/series names and added the seven editors and publisher PMLR. Author rendering now follows the supplied BibTeX (“Emmanuel Candes”). No DOI was invented. |
| `robust2025` | [NeurIPS proceedings record](https://papers.nips.cc/paper_files/paper/2025/hash/6389470564214983604d1ac81631c2c5-Abstract-Conference.html), linked [official BibTeX](https://papers.nips.cc/paper_files/paper/27633-/bibtex), and published paper | Added the officially supplied volume “38, Main Conference,” pages 68727–68756, editors, publisher Curran Associates, Inc., and DOI 10.52202/085713-2312. Author rendering and URL now follow the official BibTeX. Preserved year 2025: the record's HTML upload/publication meta date is April 2026, but the official proceedings citation explicitly uses 2025. |

## Full-report citation relevance check

The current related-work statements are consistent with the consulted primary materials: linear partial monitoring treats payoff/observation relations; Donoho connects inverse estimation and optimal recovery through moduli; prediction-powered and active inference use predicted labels to improve inference with observed outcomes. The robust-sampling paper addresses unreliable uncertainty scores through interpolation with uniform sampling. The report explicitly labels its own robust-path implementation as an adaptation, not a new method or a full reproduction. No claim/citation mismatch requiring a substantive manuscript edit was identified in these passages.

This relevance check is not a proof audit of every theorem, nor an independent implementation reproduction. In particular, the robust-sampling paper's general performance guarantees must not be silently inherited by a different finite-sample implementation; the current report's adaptation disclaimer avoids that overclaim.

All 13 keys remain unique. Every citation key extracted from the short paper and full report is present. Only three of these six extra entries needed metadata changes; optional missing addresses were left alone. The parent task still owns final compilation and visual checking after the update.
