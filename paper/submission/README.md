# IUI 2027 Posters submission package

Prepared 20 September 2026. No submission has been made.

## Target and official requirements

Target: [IUI 2027 Posters and Demos](https://iui.acm.org/2027/call-for-posters-demos/), poster track. Deadline: **10 November 2026, 23:59 Anywhere on Earth**. The call permits research results and work in progress, with a maximum of **four pages excluding references**, using the ACM single-column template and CCS concepts. A draft visual poster is recommended rather than required. A demo video is a demo-track requirement, not a requirement of this poster package. Check the live call and PCS fields before uploading; accepted work requires the venue's presentation and registration arrangements.

The current poster manuscript is four pages total including references. It is self-contained within its computational scope. The longer technical report is an accompanying public research artifact, not extra pages needed to understand the submitted claims.

## Build and contents

From the repository root:

```sh
make submission
```

Output: `output/pdf/iui-poster.pdf`. Tectonic is required and may fetch its public TeX/font bundle on first use. The file uses `acmart` version 2.20, dated 16 August 2026, in the class options shown in the call: `manuscript,review,anonymous`. No font-size, margin or class-file modifications are used. `template-provenance.json` records the CTAN source and hashes. The unmodified class and original `.dtx`/`.ins` sources retain their LaTeX Project Public License notices. The ACM bibliography style separately declares a public-domain license in its header. These upstream notices are preserved; the template files are not relicensed as project-owned MIT code. See [CTAN acmart](https://ctan.org/pkg/acmart).

The portable submission-source archive preserves these relative paths:

- `paper/submission/iui-poster.tex`, the unmodified ACM files, metadata, and this README
- `paper/references.bib`
- `paper/generated/audit-example.pdf`

From an extracted archive, run `tectonic paper/submission/iui-poster.tex --outdir output/pdf` after creating `output/pdf`. Source includes a figure description, selectable text, live references and URLs. A formal PDF/UA certification or assistive-technology audit has not been performed.

## Anonymity and portal choices

The call's prose says submissions need not be anonymized, while its sample class includes `anonymous`. We follow that sample and retain the named public repository link, which is permitted by the non-anonymity wording. This is not a double-blind-ready package for a different venue. Confirm the actual IUI portal instructions before upload. If the portal instead requires anonymity, remove identifying links and use a genuinely anonymous artifact. Do not simply reuse this PDF for CHI or WWW.

Author and contact metadata are in `submission-metadata.json` for portal entry. Affiliation is not invented; confirm the appropriate institution or independent-research status directly. The review template's stock manuscript footer is not evidence that anything was submitted. No fabricated DOI, ISBN, acceptance or external reviewer endorsement appears in the paper.

## Author checks before upload

1. Read the manuscript and technical report, verify the argument and sources, and take responsibility for the research claims.
2. Confirm the selected track, live format requirements, author metadata, conflicts, and any supplementary-file fields in PCS.
3. Preserve the research-AI methods disclosure. It covers formulation, proof drafting, experimental design, implementation, analysis and writing, plus internal AI critique. The human author remains accountable under [ACM's authorship policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship).
4. Preserve the synthetic-data and exploratory-analysis labels. There are zero human participants and no customer validation. The known product contrast is a constructed outcome model.
5. Verify the uploaded PDF preview, reference links, final title and abstract. If accepted, follow the separate camera-ready, accessibility, registration and poster instructions.

This package is scoped to a computational work-in-progress contribution. Internal AI reviews are recorded for transparency and are not peer review, an acceptance prediction, or a substitute for author scrutiny.
