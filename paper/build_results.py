#!/usr/bin/env python3
"""Generate manuscript numerical prose from the recorded analysis, not hand-entry."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'results/model-study-summary/summary.json').read_text())
models=summary['models']
mini=models['GPT-5.4 mini']; nano=models['GPT-5.4 nano']
generated=ROOT/'paper/generated'; generated.mkdir(exist_ok=True)
attempts=sum(m['execution']['attempt_events'] for m in models.values())
valid=sum(m['execution']['valid_choices'] for m in models.values())
failed=sum(m['execution']['failures'] for m in models.values())
assert attempts==4800 and valid+failed==4800
macros='\\newcommand{\\ModelCalls}{'+format(attempts,',')+'}\n'
macros+='\\newcommand{\\AbstractResult}{All 36 conservative primary decision intervals remain unresolved despite different execution accuracy.}\n'
(generated/'results-macros.tex').write_text(macros)

text=r'''\subsection{Execution competence and decision uncertainty}
The primary run recorded ATTEMPTS attempts, VALID valid choices, and FAILED transport failures. Both returned model identifiers match their pinned requested snapshots. Failed records are retained as an observable category. No retries replace them.

Table~\ref{tab:model-performance} reports field-task performance, counting a failure as no delivered utility. Mini chooses a utility maximizer more often and incurs lower mean synthetic regret. These are descriptive results for the frozen generator, not a general model ranking. Calibration tasks are excluded from these field-performance denominators.

\begin{table}[t]
\centering\small
\begin{tabular}{@{}lrr@{}}
\toprule Field metric & Mini & Nano \\\midrule
Tasks & 1,440 & 1,440 \\
Utility-maximizing choice & MINIACC\% & NANOACC\% \\
Mean synthetic regret & MINIREGRET & NANOREGRET \\
Field delivery failures & MINIFAIL\% & NANOFAIL\% \\\bottomrule
\end{tabular}
\caption{Real model responses to constructed utility objectives. Regret is best available utility minus delivered utility, on the declared $[0,1]$ scale.}
\label{tab:model-performance}
\end{table}

The joint-mass diagnostic leaves all 18 conditions per model unresolved. It contains each known synthetic target, but this does not establish an empirical coverage rate: conditions share calibration data, and the set is small and selected. Zero wrong certified decisions is achieved here by abstaining on every condition. Even the optimal-choice control leaves all 18 corresponding intervals unresolved. At this budget, conservative coordinate boxes are not a practically sufficient product-selection procedure.

The constrained point baseline selects the wrong sign in MINIWRONG of 18 Mini conditions and NANOWRONG of 18 Nano conditions. The fixed-channel percentile bootstrap contains the known target in MINIBOOT of 18 and NANOBOOT of 18 conditions, respectively. These are descriptive counts, not a calibrated coverage comparison. The bootstrap omits calibration error; the conservative method includes it but sacrifices decisiveness. This experiment does not isolate intrinsic channel nonidentification from finite-sample uncertainty.

\begin{figure*}[t]
\centering\includegraphics[width=.94\textwidth]{../results/model-study-summary/task-performance.pdf}
\caption{Primary field-task performance by semantic framing. The three framings share a mathematical generator. Real provider failures remain in the operational scores.}
\label{fig:performance}
\end{figure*}

\begin{figure*}[t]
\centering\includegraphics[width=.95\textwidth]{../results/model-study-summary/decision-intervals.pdf}
\caption{Primary decision intervals for the known finite-bank synthetic contrast. Each row uses the same independent calibration within a domain. Markers show the evaluation-only true target. All intervals cross zero. Nominal marginal coverage is at least 96\% under the stated model and sampling assumptions; this is not a simultaneous guarantee.}
\label{fig:intervals}
\end{figure*}

\subsection{Compute and interpretation}
Recorded tokens imply an estimated US\$COST for the primary run at the documented standard rates. This is not an invoice: failed transport requests may have unreported billable usage. Timeouts and connection resets are not evidence of model reasoning errors. Their temporal clustering also cautions against treating every operational error as an independent stationary draw. Conditional mathematical coverage statements must not be mistaken for verified provider independence.

The secondary analysis also propagates synthetic outcome estimation error and is more conservative. Exact outcome-bank values describe best attainable utility after future investment, not realized future behavior of the tested models. The primary findings justify investigating additional measurement channels, not declaring that all delegated product activity is inherently uninformative.
'''
replacements={'ATTEMPTS':format(attempts,','),'VALID':format(valid,','),'FAILED':str(failed),
    'COST':f"{sum(m['execution']['cost']['reported_usage_estimate_usd'] for m in models.values()):.3f}"}
for short,model in [('MINI',mini),('NANO',nano)]:
    op=model['performance']['all']
    replacements[short+'ACC']=f"{100*op['optimal_choice_rate']:.2f}"
    replacements[short+'REGRET']=f"{op['mean_synthetic_regret']:.4f}"
    replacements[short+'FAIL']=f"{100*op['failure_rate']:.2f}"
    replacements[short+'WRONG']=str(model['decisions']['naive_wrong_sign_conditions'])
    analysis=json.loads((ROOT/'results'/('model-study-'+short.lower())/'analysis.json').read_text())
    replacements[short+'BOOT']=str(sum(r['evaluation_only']['conditional_bootstrap_contains_target'] for r in analysis['reports']))
for key,value in replacements.items(): text=text.replace(key,value)
(generated/'model-results.tex').write_text(text)
print('Generated result prose from completed primary experiment.')

receipt=json.loads((ROOT/'results/receipt-study-summary/summary.json').read_text())
rmodels=receipt['models']
rmini=rmodels['GPT-5.4 mini']; rnano=rmodels['GPT-5.4 nano']
ra=sum(x['execution']['request_count'] for x in rmodels.values())
rf=sum(x['execution']['failures'] for x in rmodels.values())
assert ra==2400 and rf==0
for item in rmodels.values():
    assert item['comparison']['receipt_attribute_accuracy']==1
    assert item['comparison']['explicit_receipt']['decisive_conditions']==3
    assert item['comparison']['original_action']['decisive_conditions']==0
    assert item['comparison']['explicit_receipt']['false_decisive_conditions']==0
macros += r'\newcommand{\AbstractReceipt}{A separately frozen exploratory follow-up adds 2,400 calls reporting already supplied preferences. At matched observation counts, these reports resolve three of nine contrasts per model, while action-only logs resolve none.}'+'\n'
(generated/'results-macros.tex').write_text(macros)
rt=r'''\subsection{Explicit preference information at matched counts}
The exploratory follow-up recorded 2,400 completed receipt requests, with no delivery failures. Both models returned their requested snapshots and correctly reported the largest supplied weight on every calibration and field request. This is accuracy on 12 repeated, explicitly specified prompts, not evidence of general preference understanding. The two models therefore induce identical empirical receipt channels and identical receipt intervals on the shared task subset.

Each model's receipt channel resolves three of nine primary follow-up conditions, compared with zero of nine using the matched original actions. All three resolved conditions are the positive cohort, one per domain; none contradicts the known synthetic target. The negative and near cohorts remain unresolved. Mean interval width decreases from ACTIONWIDTH for action logs to RECEIPTWIDTH for receipts, a REDUCTION\% reduction. These figures summarize the selected conditions and do not constitute a significance test or a post-selection coverage guarantee.

\begin{table}[t]
\centering\small
\begin{tabular}{@{}lrr@{}}
\toprule Paired measure, per model & Actions & Receipts \\\midrule
Calibration per class/domain & 40 & 40 \\
Field per cohort/domain & 80 & 80 \\
Resolved contrasts / conditions & 0 / 9 & 3 / 9 \\
Incorrect resolved contrasts & 0 & 0 \\
Mean interval width & ACTIONWIDTH & RECEIPTWIDTH \\\bottomrule
\end{tabular}
\caption{Exploratory comparison. Both models have the same reported interval summaries. Perfectly reporting the supplied leading attribute directly reveals the constructed intent class. Counts do not equalize monetary cost or elicitation burden.}
\label{tab:receipt}
\end{table}

\begin{figure*}[t]
\centering\includegraphics[width=.94\textwidth]{../results/receipt-study-summary/receipt-comparison.pdf}
\caption{Action-only and attribute-only intervals on the same selected task IDs. The receipt collects explicit preference information omitted from the action log; it does not discover an unobserved human preference. The follow-up was chosen after the primary results, so these are exploratory comparisons without selective-inference correction.}
\label{fig:receipt}
\end{figure*}

The result separates two limitations. Even a directly observed class does not resolve every small contrast under this finite-sample procedure. Yet the same number of observations is more useful when it records a relevant class attribute instead of a behavioral proxy. The receipt's remaining uncertainty is sampling and channel-calibration uncertainty within the declared model, rather than a demonstrated loss of the supplied class information. Since a deterministic extractor would provide the same field, this experiment supports explicit measurement design, not the necessity of an LLM receipt generator.

Reported usage implies an additional US\$RECEIPTCOST for the follow-up. Across the two studies, there are 7,200 attempted API requests, 7,183 valid responses, and 17 retained transport failures. The excluded connectivity test is not part of these counts. All preferences and product outcomes remain synthetic.
'''
aw=rmini['comparison']['original_action']['mean_interval_width']
rw=rmini['comparison']['explicit_receipt']['mean_interval_width']
assert abs(aw-rnano['comparison']['original_action']['mean_interval_width'])<1e-10
assert abs(rw-rnano['comparison']['explicit_receipt']['mean_interval_width'])<1e-10
for key,val in {'ACTIONWIDTH':f'{aw:.4f}','RECEIPTWIDTH':f'{rw:.4f}',
    'REDUCTION':f'{100*(1-rw/aw):.1f}',
    'RECEIPTCOST':f"{sum(m['execution']['cost']['reported_usage_estimate_usd'] for m in rmodels.values()):.3f}"}.items(): rt=rt.replace(key,val)
(generated/'receipt-results.tex').write_text(rt)
print('Generated receipt result prose from completed exploratory follow-up.')
