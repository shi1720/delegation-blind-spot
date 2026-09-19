#!/usr/bin/env python3
"""Plot the exploratory equal-observation-count preference-receipt comparison.

Receipt requests repeatedly extract the largest supplied preference weight.
They are not human feedback, customer validation, or diverse natural tasks.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from plot_results import DOMAINS,COHORTS,LABELS,read_json,read_jsonl,sha256,save_figure

ACTION_COLOR='#85919B'
RECEIPT_COLOR='#207D79'


def paired_reports(comparison):
    actions=[r for r in comparison['action_reports'] if r['log_schema']=='action_only']
    receipts=[r for r in comparison['receipt_reports'] if r['log_schema']=='receipt_attribute']
    def index(rows):
        result={(r['domain'],r['cohort']):r for r in rows}
        if len(result)!=len(rows): raise ValueError('Duplicate domain/cohort records')
        return result
    a,b=index(actions),index(receipts)
    if not a or a.keys()!=b.keys(): raise ValueError('Action and receipt conditions do not match')
    for key in a:
        for n in ['calibration_n','field_n']:
            if a[key][n]!=b[key][n]: raise ValueError('Comparison does not have equal observation counts')
        if not np.isclose(a[key]['evaluation_only']['true_contrast'],b[key]['evaluation_only']['true_contrast'],rtol=0,atol=1e-12):
            raise ValueError('Compared conditions do not share the same synthetic target')
        if 'receipt_attribute_accuracy' not in b[key] or any(k in b[key] for k in ['mean_synthetic_utility','mean_synthetic_regret','optimal_choice_rate']):
            raise ValueError('Receipt accuracy must not be described as product-choice utility')
    return a,b


def comparison_summary(comparison):
    actions,receipts=paired_reports(comparison)
    n=sum(r['field_n'] for r in receipts.values())
    totals={'selected_domain_cohort_conditions':len(receipts),'field_receipt_count':n,
        'receipt_attribute_accuracy':float(sum(r['receipt_attribute_accuracy']*r['field_n'] for r in receipts.values())/n),
        'receipt_field_failure_rate':float(sum(r['failure_rate']*r['field_n'] for r in receipts.values())/n),
        'scope':'Explicitly reporting the largest already supplied synthetic preference weight. No product-choice utility, human feedback or privacy guarantee.',
        'interpretation':'Counts summarize selected paired conditions, not an empirical confidence-interval coverage rate.',
        'inference_limit':'The nominal 96% marginal interval method assumes the stated sampling design and stable channels. The exploratory follow-up selection and reuse of original field draws are not adjusted by a selective-inference procedure.',
        'resource_limit':'Equal observation counts do not equalize API cost, privacy exposure, or preference-elicitation burden.'}
    for name,reports in [('original_action',actions),('explicit_receipt',receipts)]:
        totals[name]={'decisive_conditions':sum(r['decision']!='unresolved' for r in reports.values()),
            'unresolved_conditions':sum(r['decision']=='unresolved' for r in reports.values()),
            'false_decisive_conditions':sum(r['evaluation_only']['certified_wrong_decision'] for r in reports.values()),
            'mean_interval_width':float(np.mean([r['upper']-r['lower'] for r in reports.values()]))}
    return totals


def receipt_execution(directory,pricing=None):
    directory=Path(directory)
    manifest=read_json(directory/'manifest.json')
    tasks=read_jsonl(directory/'tasks.jsonl')
    ids={r['task_id'] for r in tasks}
    events=read_jsonl(directory/'responses.jsonl')
    records=[r for r in events if r.get('event')=='result']
    if len(ids)!=len(tasks) or len(records)!=len(ids) or {r['task_id'] for r in records}!=ids:
        raise ValueError('Receipt run is incomplete or has duplicate results')
    tokens=Counter(input_tokens=0,cached_input_tokens=0,output_tokens=0,total_tokens=0)
    errors=Counter();missing=success=0
    returned=Counter()
    for row in records:
        good=row.get('choice_id') in ['A','B','C','D'] and not row.get('error')
        success+=int(good)
        if not good:
            error=row.get('error') or {}
            errors[error.get('type','invalid_choice_without_error') if isinstance(error,dict) else str(error)]+=1
        raw=row.get('response',{})
        model=row.get('model_returned') or raw.get('model')
        if model: returned[model]+=1
        usage=row.get('usage') or raw.get('usage')
        if not usage: missing+=1; continue
        for name in ['input_tokens','output_tokens','total_tokens']: tokens[name]+=int(usage.get(name,0) or 0)
        cache=int(usage.get('input_tokens_details',{}).get('cached_tokens',0) or 0)
        if cache<0 or cache>int(usage.get('input_tokens',0) or 0): raise ValueError('Invalid cached input count')
        tokens['cached_input_tokens']+=cache
    cost=None
    model=manifest['model_requested']
    if pricing and model in pricing:
        p=pricing[model]
        cost={'reported_usage_estimate_usd':float(((tokens['input_tokens']-tokens['cached_input_tokens'])*p['input_per_million']+tokens['cached_input_tokens']*p['cached_input_per_million']+tokens['output_tokens']*p['output_per_million'])/1e6),
            'source':p['source'],'scope':'Estimate for reported token usage only; unknown billing for transport failures is excluded.'}
    return {'model_requested':model,'returned_models':dict(returned),
        'request_count':len(records),'attempt_events':sum(r.get('event')=='attempt' for r in events),
        'valid_receipts':success,'failures':len(records)-success,'error_types':dict(errors),
        'timeout_failures':sum(v for k,v in errors.items() if 'timeout' in k.lower()),
        'connection_reset_failures':sum(v for k,v in errors.items() if 'reset' in k.lower()),
        'distinct_supplied_preference_prompts':manifest['distinct_receipt_prompts'],
        'reported_usage':dict(tokens),'requests_without_reported_usage':missing,'cost':cost,
        'input_sha256':{name:sha256(directory/name) for name in ['manifest.json','tasks.jsonl','responses.jsonl','comparison.json']}}


def receipt_figure(comparisons,output):
    pairs={label:paired_reports(data) for label,data in comparisons.items()}
    conditions=[(d,c) for d in DOMAINS for c in COHORTS]
    if any(set(a)!=set(conditions) for a,b in pairs.values()):
        raise ValueError('The publication layout expects all nine declared domain/cohort conditions')
    fig,axes=plt.subplots(1,len(pairs),figsize=(8.1,6.5),sharex=True,sharey=True,squeeze=False)
    limit=max(abs(r[key]) for pair in pairs.values() for indexed in pair for r in indexed.values() for key in ['lower','upper'])*1.08
    for ax,(label,(actions,receipts)) in zip(axes[0],pairs.items()):
        for y,key in enumerate(conditions):
            if y%3==0: ax.axhspan(y-.5,y+2.5,color='#F4F6F7' if y%6==0 else 'white',zorder=0)
            for rows,offset,color in [(actions,-.14,ACTION_COLOR),(receipts,.14,RECEIPT_COLOR)]:
                row=rows[key]
                ax.plot([row['lower'],row['upper']],[y+offset]*2,color=color,lw=2.2,solid_capstyle='round')
                ax.plot([row['lower'],row['upper']],[y+offset]*2,'|',color=color,markersize=5)
            ax.scatter([actions[key]['evaluation_only']['true_contrast']],[y],marker='D',s=16,color='#1D252A',zorder=5)
        ax.axvline(0,color='#818A91',linestyle=':',lw=1)
        ax.set_xlim(-limit,limit);ax.set_ylim(len(conditions)-.45,-.55)
        ax.set_title(label,fontsize=10,loc='left',pad=12)
        ax.set_xlabel('Product outcome contrast')
        ax.spines[['top','right','left']].set_visible(False)
        ax.tick_params(axis='y',length=0,pad=8);ax.grid(axis='x',alpha=.13)
    axes[0,0].set_yticks(range(len(conditions)),labels=[f'{d.title()} / {LABELS[c]}' for d,c in conditions],fontsize=8)
    fig.suptitle('Equal observation counts: actions and preference receipts',x=.055,ha='left',fontsize=12,weight='bold',y=.98)
    handles=[Line2D([0],[0],color=ACTION_COLOR,lw=2.2,label='Original action logs'),
        Line2D([0],[0],color=RECEIPT_COLOR,lw=2.2,label='Explicit preference receipt'),
        Line2D([0],[0],color='#1D252A',marker='D',linestyle='',markersize=4,label='Known synthetic target')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.047,.95),ncol=3,frameon=False,fontsize=8)
    fig.text(.055,.045,'Exploratory follow-up: repeated extraction from 12 supplied-preference prompts. No human participants.',fontsize=7.8,color='#4E5962')
    fig.text(.055,.023,'Same task IDs and observation counts. Nominal 96% marginal method; no correction for follow-up selection.',fontsize=7.8,color='#4E5962')
    fig.subplots_adjust(left=.255,right=.97,bottom=.135,top=.82,wspace=.10)
    save_figure(fig,output,'receipt-comparison')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mini',type=Path,required=True)
    p.add_argument('--nano',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--pricing',type=Path)
    a=p.parse_args()
    pricing=read_json(a.pricing) if a.pricing else None
    comparisons={}
    summary={'design':'Exploratory follow-up to the original unresolved decision intervals.',
        'scope':'Repeated model extraction of already supplied synthetic preference weights. No human participants, no privacy guarantee.',
        'models':{}}
    for label,directory in [('GPT-5.4 mini',a.mini),('GPT-5.4 nano',a.nano)]:
        data=read_json(directory/'comparison.json')
        comparisons[label]=data
        summary['models'][label]={'comparison':comparison_summary(data),'execution':receipt_execution(directory,pricing)}
    a.output.mkdir(parents=True,exist_ok=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':8,'pdf.fonttype':42,'ps.fonttype':42})
    receipt_figure(comparisons,a.output)
    (a.output/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(f'Wrote receipt comparison figure and auditable summary to {a.output}')


if __name__=='__main__':main()
