# Internal skeptical review for a v0.3 poster submission

Review date: 20 September 2026. Target: IUI 2027 Posters, with CHI 2027 Posters considered separately.

**Status:** AI-generated internal critique requested by the author. This is not an official venue review, an external expert endorsement, or evidence of acceptance. Scores below use an internal five-point rubric and are not the venue's form.

Reviewed: `paper/main.tex`, generated primary/receipt result sections, the release validation report, and current primary venue pages. The source hash at inspection was `817afa7124d6b31fd5aeabb865f6b1d9ed6a94c97b85a18e8b6c27ca3ca34f29`. The current PDF has 14 pages. This review is not an independent re-execution of the experiments or proof audit.

## Verdict

**Current artifact: not ready to submit to either poster track.** It is a long custom-format technical preprint, not the required short submission. The most realistic next submission is a focused **IUI 2027 Poster** about the design of decision-relevant measurement in delegated interfaces. Computational-only evidence is compatible with that limited work-in-progress contribution. A human study is not necessary to submit an honestly scoped poster, but simulated profiles cannot support claims about what customers actually want.

**Internal recommendation: 2/5, weak reject in current form.** A four-page version with a clear interface contribution, a compact worked example, the negative primary result, the accurately scoped receipt follow-up, and complete research-provenance disclosure could reach a defensible borderline or weak-accept discussion. That is a revision target, not an acceptance prediction.

Do not choose the demo track merely because code exists. The statistical package and investigator-only questionnaire are not yet a demonstrated, novel intelligent user interface with a coherent live demonstration.

## Verified venue requirements

### IUI 2027 Posters

The current [official call](https://iui.acm.org/2027/call-for-posters-demos/) lists **10 November 2026, 23:59 AoE** as the deadline; notification is 14 December and camera-ready is 18 December. It welcomes scientific results and work in progress. The submission is **up to four pages excluding references**, using the **ACM single-column** template and CCS classification, through PCS. A draft visual poster is recommended rather than required. Accepted work appears in companion proceedings and is expected to be presented in person. The conference is 8 to 11 February 2027 in Helsinki.

The same call explicitly says submissions need not be anonymized, but its sample LaTeX declaration includes `anonymous`. This is an internal inconsistency, not a reason to invent a requirement. Preparing an anonymous review PDF using the supplied example is compatible with the permissive prose; keep attributed metadata separately. Recheck the PCS track instructions before submission.

### CHI 2027 Posters

The [official call](https://chi2027.acm.org/authors/posters/) gives **21 January 2027 AoE** and requires an **anonymous, single-column paper of at most four pages excluding references**, an **A0 visual poster**, and **key discussion points**. A separate optional appendix is not expected to determine the decision. The call accepts nascent methodological or theoretical contributions and says poster work is non-archival. It requires four review-responsibility slots assigned to submitting authors; a sole author must verify the operational treatment in PCS rather than invent coauthors. The page contains one stray “6-page” reference despite repeated four-page instructions: prepare four pages.

CHI is plausible as a discussion-oriented fallback, especially if the interface contribution becomes clearer. It requires additional submission artifacts and anonymization; the current named GitHub URL and PDF author metadata cannot simply be copied into an anonymous package. Essential methodology belongs in the short paper, not hidden in the optional appendix.

### ACM methods disclosure

The [current ACM authorship policy](https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship), updated 14 May 2026, distinguishes writing assistance from conducting research. Its indexed primary-policy text requires detailed **Methods** disclosure for AI use affecting research design, code, data generation, analysis, testing, validation, and reproducible artifacts. Writing-only assistance no longer requires disclosure. Both venue calls refer authors to ACM policy. Direct retrieval of the canonical ACM page returned 403 during this check; the policy text was available in search indexing of ACM's publication site. Recheck the canonical policy before submission.

The manuscript describes models under test but does not describe the AI-assisted research-development workflow. Those are different uses. Add a factual methods paragraph naming the research-assistance system and its roles, generated artifacts, actual human verification performed, and remaining limitations. Do not say a human independently verified proofs or analyses unless that occurred. Do not count internal agent reviews as external reviewers. The author must accept responsibility for all claims.

## Strict scored assessment

| Dimension | Score / 5 | Assessment |
| --- | ---: | --- |
| Importance | 4 | Learning from agent-mediated behavior is timely and relevant to intelligent interfaces. |
| Originality | 2 | Most formal results specialize established identification and decision theory. The receipt experiment extracts an explicit class label. |
| IUI relevance | 3 | The question concerns an interface measurement problem, but the current paper reads primarily as a statistics report. |
| Methodological transparency | 4 | Failures, negative results, model versions, synthetic scope, and post-selection limits are stated carefully. |
| Empirical persuasiveness | 2 | One constructed task family, two related snapshots, and universal primary abstention do not establish practical product utility. |
| Clarity for a poster audience | 2 | Too many theorem families, baselines, stages, and qualifications compete with the main idea. |
| Reproducibility potential | 4 | The declared raw traces, hashes, tests, and exact reanalysis are strong. This review did not rerun them. |
| Discussibility | 4 | Contrasting action logs, supplied preferences, and confirmed outcomes can support an excellent focused poster conversation. |
| Submission compliance | 1 | Wrong current template and length; detailed AI-research provenance and poster-specific framing are missing. |

Internal reviewer confidence: **4/5** for venue fit and narrative assessment, **2/5** for mathematical correctness because this is not an independent theorem review.

## Major concerns, ranked

### 1. The contribution is broader in presentation than in evidence

The title promises learning what people want. The experiment has no people, unknown preferences, observed satisfaction, or real product investment. Its strongest substantiated result is about inference from a deliberately specified measurement channel and known synthetic utility contrasts. Retain the memorable main title if desired, but use a precise subtitle such as **“A Computational Study of Decision-Relevant Logging for AI Delegates.”** Open with the declared measurement question, not an assertion of general customer learning.

The poster contribution should be a decision-oriented diagnostic and a design provocation, supported by a bounded computational study. It should not be presented as a new preference-learning algorithm or a general impossibility of learning from agents.

### 2. The primary experiment tests conservatism more directly than a delegation blind spot

Every conservative interval is unresolved, including those from the optimal-choice control. This could reflect limited calibration, small product contrasts, coordinate-box conservatism, or insufficient logging. It is not direct evidence that agent capability destroys information. The manuscript correctly acknowledges this, but the poster must put that finding near its headline result rather than let readers infer a successful remedy.

Minimum revision: show one compact decomposition distinguishing exact-channel ambiguity from finite-sample uncertainty on an existing constructed example. If further computations are added, name them sensitivity analysis rather than silently enlarging the primary study. Avoid reporting a fraction of 36 selected, dependent conditions as coverage.

### 3. Receipt success is an instrument control, not discovered customer insight

The receipt identifies the maximum of four numerical weights already provided. Twelve distinct prompts are repeated, and the leading attribute reveals the designed class. A deterministic parser would do this without a language model. The value is the contrast between recording relevant supplied information and recording only an action, not model intelligence.

Minimum revision: include the deterministic extractor as an explicit conceptual or implemented control, state that zero parsing uncertainty is available for the structured source, and explain why the interface should preserve that field. Do not use 2,400 calls as an implied measure of diversity. Do not call equal counts equal cost. Report six of nine receipt conditions still unresolved per model.

### 4. There is no concrete interface proposal to assess yet

The paper proposes a “decision receipt,” but most of its source distinctions are prose. A poster reader needs to see what a practitioner receives: the future decision, observed action, supplied preference, agent-inferred claim, customer-confirmed outcome, uncertainty interval, and missing-information state. A compact example should visibly distinguish observed, supplied, inferred, and confirmed fields.

A new receipt mockup or local diagnostic view could help, but label it a proposed interface without usability validation. Do not reuse the offline participant questionnaire as proof that analysts can interpret the diagnostic. A discussion-ready conceptual artifact is enough for a poster; no fabricated usability test is needed.

### 5. The practical decision contrast is treated as known by design

A real firm rarely knows each latent class's future outcome contrast. The paper's contrast assumes optimal future selection over synthetic menu banks. That assumption is useful for isolating measurement, but it relocates a difficult product-learning problem into the setup. Explain who could supply the contrast in practice and what would happen if it is uncertain. One sentence and a limitation box suffice in the poster; an unsupported business-success claim does not.

### 6. New relevant literature must narrow the positioning

A current search located additional close work, below. Do not pad the references. Add only sources used to make a precise distinction. No “first” or “industry-defining” claim is presently supported by this review.

## Closest prior work and update to the novelty boundary

1. **Suleymanov, A Revealed Preference Framework for AI Alignment (2026).** [Primary paper](https://arxiv.org/abs/2603.27868), [full text](https://arxiv.org/html/2603.27868v1). Introduction and model inspected. A mixture-of-Luce model identifies aspects of alignment and compliance from stochastic choices across menus, with label-swap limitations when only AI choices are observed. This is a direct missing comparison. Our target is a future product contrast across a calibrated finite population, not reconstruction of a principal-agent utility pair. Our unresolved coarse-log results cannot refute richer-menu identification under that model.
2. **Kraft and Larsen, Consumer Preference Transmission in Agentic Markets (2026).** [Primary working paper record](https://ssrn.com/abstract=6864181). Current abstract checked. It already treats differences between consumer preferences, prompts, agents, and adoption selection and includes conjoint and incentivized-bookstore evidence. The distinct candidate here is decision-specific measurement bounds and source-labeled receipts, not first recognition that agents transform demand. Full empirical comparison remains necessary for a longer paper.
3. **Kops and Tsakas, Choice via AI (2026).** [Primary paper](https://arxiv.org/abs/2602.04526). Previously inspected model. It studies recommendation interpretation and preference identification. Avoid conflating execution errors, preference misalignment, and loss of information needed by a third-party analyst.
4. **Cherep et al., ABxLab (2025).** [Primary paper](https://arxiv.org/abs/2509.25609). Previously inspected. It is a direct antecedent for controlled agent-choice experiments with profiles and product attributes. A new domain skin or multiple model snapshots does not independently establish a new benchmark contribution.
5. **Du, Who Chooses How Preferences Are Aggregated? (2026).** [Primary abstract](https://arxiv.org/abs/2608.23966), submitted 25 August. Screened abstract only. It separates rule execution from delegated authority in group recommendations. It is adjacent, not the same target, but demonstrates that execution competence versus another decision property is already an active framing. Do not claim a substantive theorem overlap without reading further.
6. **Chen, Zhu and Zheng, When Synthetic Users Fail (2026).** [Primary abstract](https://arxiv.org/abs/2607.26348), submitted 28 July. Screened abstract only. It evaluates simulated survey respondents against actual human data and non-LLM baselines. Relevant to why our synthetic profiles are instrument inputs, not customer validation. It does not show every form of simulation is useless, and no such claim belongs here.

The established statistical spine remains Blackwell informativeness, linear partial monitoring, measurement-error partial identification, and BBSE label-shift estimation. Cite these as foundations; three pages of specialized proofs do not become an IUI interaction contribution solely through new notation.

## Concrete four-page compression strategy

Target approximately **1,650 to 1,900 words before references**, subject to actual rendering in the official ACM single-column template. This is a planning budget, not a promise that every template version fits. Never shrink fonts, margins, caption size, or line spacing to force compliance.

| Page | Content | Approximate allocation |
| --- | --- | --- |
| 1 | Precise title, 120-word abstract, one hotel scenario, one sentence defining the practitioner, concise contribution, compact receipt example or measurement schematic | 350 to 420 words plus small visual |
| 2 | Decision target and one equation `q=Ap, Delta=d^T p`; one standard identification fact with a two-sentence argument; bounds and calibration assumptions; the frozen computational design | 450 to 500 words |
| 3 | One combined results display: primary 0/18 per model; follow-up 3/9 versus matched 0/9; widths, denominators, 12-prompt scope; negative result explained directly | 350 to 420 words plus one compact table/figure |
| 4 | Source distinctions in the receipt, three design implications, limitations, discussion questions, concise AI-research methods disclosure, artifact availability | 450 to 550 words |

**Keep in the short paper:** the exact task/data scope; actual model snapshots; the primary failure to resolve; the exploratory status and limited receipt task; uncertainty assumptions; why this matters to an interface designer; three pointed discussion questions.

**Remove from the short paper:** worst-case width duality, full minimax regret proof, bias-aware certificate derivation, audit-estimator pilot, lengthy cross-model transport results, compute accounting beyond a short provenance statement, and the future participant-instrument implementation. Preserve them in a separately identified technical report or allowed supplementary material. A reviewer must be able to understand and assess the poster without opening those files.

**Compress related work into about 180 words:** one paragraph on delegated choice and transmission, one on established channel inference, ending with the narrow operational difference. Do not spend a page disclaiming every possible overclaim; instead make each claim precise where it appears.

**One useful visual:** show the same observed choice alongside two compatible synthetic intent mixtures that favor opposite future improvements, then show which additional field would distinguish them. Label this an exact constructed example. Keep it separate from the measured model-result table so the reader cannot confuse a demonstration with an empirical finding.

**Suggested discussion questions:**

- Which supplied preference fields should an interface preserve for a declared future decision, and which should it deliberately avoid collecting?
- When should an analyst use direct customer-outcome measurement instead of recovering latent intent from an agent's behavior?
- How can a decision receipt distinguish an observed action, an agent's inference, and an independently confirmed outcome without suggesting that all three are equally reliable?

## Submission-ready gates for the IUI poster

1. Produce a separate four-page single-column ACM source and PDF. Keep the 14-page preprint intact as a different artifact. Include verified CCS concepts and avoid guessed publication metadata.
2. Replace customer-learning and algorithm-novelty implications with the computational measurement contribution. Show the negative primary result and narrow receipt result on equal footing.
3. Add a concrete, clearly labeled receipt/diagnostic example. Check that it is useful to the proposed analyst, not merely decorative.
4. Add the direct revealed-preference comparison and verify every cited source that supports a substantive claim.
5. Include detailed, factual AI-research assistance disclosure in Methods, covering the work actually performed. Human author review and accountability remain necessary.
6. Validate all numbers against immutable result files; do not imply an independent repeated-sampling coverage study or significance result.
7. Render the official template, confirm the main content ends within four pages, inspect references/figures, and check accessibility and PDF metadata. Select named versus anonymous mode deliberately in view of the IUI call's inconsistent example.
8. Prepare a draft visual poster, title, abstract, keywords, and a clearly scoped artifact link. Recheck PCS-specific instructions and the current CFP immediately before submission. No submission or external communication is authorized by this internal review itself.

Passing these gates can make a computational work-in-progress poster genuinely ready to submit. It cannot make customer validation, external peer review, or acceptance already true.
