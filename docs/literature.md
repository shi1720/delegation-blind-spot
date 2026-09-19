# Literature and attribution ledger

Checked 19 September 2026. Entries marked screened still require full method review. A working paper is not described as accepted without separate evidence.

| Source | Role | Inspection |
| --- | --- | --- |
| Angelopoulos et al., [Prediction-Powered Inference](https://arxiv.org/abs/2301.09633) | Prediction plus labeled residual correction | Abstract screened; standard mean-estimation identity used with attribution |
| Zrnic and Candes, [Active Statistical Inference](https://proceedings.mlr.press/v235/zrnic24a.html), ICML 2024 | Label allocation for inference | Primary conference entry and relevant formulas inspected |
| Li, Zrnic and Candes, [Robust Sampling for Active Statistical Inference](https://papers.nips.cc/paper_files/paper/2025/file/6389470564214983604d1ac81631c2c5-Paper-Conference.pdf), NeurIPS 2025 | Robust interpolation between active and uniform sampling | Sections 1 to 3 inspected; pilot adapts equations 1 to 4 with a declared box uncertainty set |
| Ao, Chen and Simchi-Levi, [Prediction-Guided Active Experiments](https://arxiv.org/abs/2411.12036) | Adaptive outcome acquisition and efficiency | Abstract, introduction, and model screened; complete estimator comparison remains |
| Brawand et al., [Active Multiple-Prediction-Powered Inference](https://arxiv.org/abs/2605.08429) | Multiple-predictor routing plus acquisition | Abstract screened; verify claims and assumptions before use |
| Kops and Tsakas, [Choice via AI](https://arxiv.org/abs/2602.04526) | Choice interpretation and identification | Abstract and relevant full-text portions screened |
| Kraft and Larsen, [Consumer Preference Transmission in Agentic Markets](https://ssrn.com/abstract=6864181) | Consumer, prompt, agent, and adoption differences | Primary abstract screened |
| Cherep et al., [ABxLab](https://arxiv.org/abs/2509.25609) | Controlled interface interventions on agent choices | Primary full text inspected, including user profiles and experimental limitations; authors' repository screened |
| [The Basic B*** Effect](https://arxiv.org/abs/2509.02910) | Compression of delegated choice diversity | Abstract screened |

## Claims not available to us as novelty

Selective labeling, prediction correction, uncertainty-based sampling, robustness to bad uncertainty estimates, and agent preference distortion are already studied. A new domain label does not create a new statistical method. Generic non-identification without labels and a random-audit remedy are standard missing-data facts.

## Next comparison questions

1. Does agent policy drift create a new estimand or observation constraint not covered by the existing sampling formulations?
2. Can logs distinguish changed user preferences from changed execution channels, and what randomized or audited observations resolve that ambiguity?
3. What is the minimum feedback needed for product selection, rather than full preference recovery?
4. Do changing agents invalidate only proxy efficiency, or assumptions required for identification? These are different failures.
5. Can realistic tasks demonstrate a measurable frontier between useful delegation and information retained for product learning?


## Additional identification sources

- Kirschner, Lattimore, and Krause (2023), [Linear Partial Monitoring for Sequential Decision Making](https://jmlr.org/papers/v24/22-1248.html). Observability relates decisions to observation maps; a rank or row-space condition is not our invention. Relevant conditions inspected.
- Finkelstein, Adams, Saria, and Shpitser (2021), [Partial Identifiability in Discrete Data with Measurement Error](https://proceedings.mlr.press/v161/finkelstein21b.html). Linear constraints and optimization bounds have direct antecedents. Primary entry and relevant formulation screened; complete method comparison remains.

## API instrument source

[Official Structured Outputs documentation](https://developers.openai.com/api/docs/guides/structured-outputs), retrieved 19 September 2026, supplies the Responses API output-schema contract. Model identity is a required runner argument. Live execution is untested in this release.
