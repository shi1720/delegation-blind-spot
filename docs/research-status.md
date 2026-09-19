# Research status

Author: Shivam Gupta. Started 19 September 2026.

Selected direction: The Delegation Blind Spot. Working title: Learning What People Want When Agents Make the Choices.

## Full objective

Produce a technically correct, original research contribution with commercial relevance, implemented code, genuine experiments, supported figures, a well-cited manuscript, a public GitHub artifact, and a suitable venue strategy. Include accurate author details. Follow the eventual venue's authorship and disclosure requirements. Do not fabricate results, participation, claims of originality, or acceptance.

## Current gate

The initial pilot asks whether familiar statistical methods already address the simplest form of the problem. It does not claim a new algorithm. A substantive paper needs more than a synthetic label-shift example plus an existing inverse-probability estimator.

## Completed milestone, 19 September 2026

- Seven-page research note with explicit attribution and limitations, rendered and visually checked.
- 100,000 synthetic audit estimator evaluations with 1,000 replicates per cell. Four numerical CSV outputs reproduced byte for byte.
- Decision-specific identification bounds, uncertainty boxes, and explicit feasible witness populations.
- 28 passing tests, including exhaustive finite examples for the audit estimator.
- 216 prepared constructed agent tasks and 648 control decisions, with balanced option orders.
- An actual-model experiment runner prepared using the official Responses API documentation. No API credential is loaded in the research process, and no live model calls or human study have been run.

The central candidate question is whether successful delegation preserves the information needed for a specific future product decision. The general algebra and LP are existing ideas. An empirical contribution needs calibration, held-out outcomes, and evidence that ordinary alternatives do not already solve the intended task.

## Unresolved requirements

- Identify a precise contribution beyond active statistical inference, robust sampling, adaptive experimentation, and delegated preference transmission.
- Inspect closest methods and released code rather than relying on abstracts.
- Model the causal path from user goals through delegated execution to actual outcomes. Do not equate proxy drift with agent causation.
- Identify a real task environment in which outcomes have independent meaning and can be elicited from people.
- Preregister a main evaluation only after the exploratory pilot. Keep these stages separate.
- Establish proof assumptions and have each claimed result independently checked.
- Run real model and real human evaluations with suitable consent and ethics arrangements.
- Produce and visually verify the final manuscript and figures.
- Publish the validated artifact to GitHub with appropriate licensing and reproducibility instructions.

## Stop or revise criteria

If established methods solve the intended task under equivalent information and cost, do not rename them as a new contribution. If the observed phenomenon follows only from deliberately changing unseen labels, the result is a sanity check, not an empirical discovery. If the target outcome is unclear, fix the estimand before optimizing it. If all meaningful evidence is synthetic, do not claim industry-wide or human-behavior conclusions.
