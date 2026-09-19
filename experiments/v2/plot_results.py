#!/usr/bin/env python3
"""Publication figures and audited summaries from completed model experiments.

Never treats constructed profiles as human participants, counts a model failure
as success, or estimates coverage from the small set of displayed targets.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

COLORS={'action_only':'#277F86','context_and_action':'#8A579C'}
DOMAINS=['travel','cloud','workflow']
COHORTS=['positive','negative','near']
LABELS={'positive':'Capacity-heavy','negative':'Flexibility-heavy','near':'Mixed'}
MODEL_COLORS=['#277F86','#BD643E','#658058','#8A579C','#77818A']


def read_json(path):
    return json.loads(Path(path).read_text())


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execution_summary(directory,pricing=None):
    directory=Path(directory)
    manifest=read_json(directory/'manifest.json')
    tasks=read_jsonl(directory/'tasks.jsonl')
    task_ids={t['task_id'] for t in tasks}
    if len(task_ids)!=len(tasks): raise ValueError('Duplicate task IDs in frozen tasks')
    events=read_jsonl(directory/'responses.jsonl')
    attempts=[r for r in events if r.get('event')=='attempt']
    final=[r for r in events if r.get('event')=='result']
    final_ids=[r['task_id'] for r in final]
    if len(final_ids)!=len(set(final_ids)): raise ValueError('Duplicate final response records')
    if set(final_ids)!=task_ids: raise ValueError('Completed results do not match all frozen tasks')
    if manifest['task_count']!=len(tasks): raise ValueError('Manifest task count mismatch')
    by_id={t['task_id']:t for t in tasks}
    errors=Counter()
    statuses=Counter()
    returned=Counter()
    tokens=Counter(input_tokens=0,cached_input_tokens=0,output_tokens=0,total_tokens=0)
    success=missing_usage=0
    latencies=[]
    split_counts=Counter()
    for row in final:
        split_counts[by_id[row['task_id']]['split']]+=1
        valid=row.get('choice_id') in by_id[row['task_id']]['semantic_choice'] and not row.get('error')
        success+=int(valid)
        error=row.get('error')
        if error:
            name=error.get('type','unknown') if isinstance(error,dict) else str(error)
            errors[name]+=1
            if isinstance(error,dict) and error.get('status') is not None:
                statuses[str(error['status'])]+=1
        elif not valid:
            errors['invalid_choice_without_error']+=1
        raw=row.get('response',{})
        model=row.get('model_returned') or raw.get('model')
        if model: returned[model]+=1
        usage=row.get('usage') or raw.get('usage')
        if not usage:
            missing_usage+=1
        else:
            for name in ['input_tokens','output_tokens','total_tokens']:
                tokens[name]+=int(usage.get(name,0) or 0)
            cached=int(usage.get('input_tokens_details',{}).get('cached_tokens',0) or 0)
            if cached>int(usage.get('input_tokens',0) or 0) or cached<0:
                raise ValueError('Cached tokens exceed recorded input tokens')
            tokens['cached_input_tokens']+=cached
        if row.get('elapsed_seconds') is not None:
            latencies.append(float(row['elapsed_seconds']))
    timeout=sum(v for k,v in errors.items() if 'timeout' in k.lower())
    reset=sum(v for k,v in errors.items() if 'reset' in k.lower())
    costs=None
    model_requested=manifest['model_requested']
    if pricing and model_requested in pricing:
        price=pricing[model_requested]
        rates=[float(price[k]) for k in ['input_per_million','cached_input_per_million','output_per_million']]
        if not all(np.isfinite(r) and r>=0 for r in rates): raise ValueError('Invalid token prices')
        uncached=tokens['input_tokens']-tokens['cached_input_tokens']
        costs={'reported_usage_estimate_usd':float((uncached*rates[0]+tokens['cached_input_tokens']*rates[1]+tokens['output_tokens']*rates[2])/1e6),
               'rate_source':price.get('source'), 'rates_usd_per_million':price,
               'scope':'Estimate for reported token usage only. Transport failures may have unreported billable usage; this is not the account invoice.'}
    return {'model_requested':model_requested,'returned_models':dict(returned),
        'prepared_tasks':len(tasks),'attempt_events':len(attempts),'final_results':len(final),
        'valid_choices':success,'failures':len(final)-success,'failure_types':dict(errors),
        'http_status_counts':dict(statuses),'timeout_failures':timeout,'connection_reset_failures':reset,
        'failure_type_limit':'Wrapped URLError causes cannot be recovered when the source record omitted the inner exception.',
        'split_counts':dict(split_counts),'reported_usage':dict(tokens),
        'requests_without_reported_usage':missing_usage,'cost':costs,
        'latency_seconds':{'mean':float(np.mean(latencies)),'median':float(np.median(latencies)),
            'p95':float(np.quantile(latencies,.95))} if latencies else None,
        'input_sha256':{name:sha256(directory/name) for name in ['manifest.json','tasks.jsonl','responses.jsonl','analysis.json']}}


def unique_field_reports(analysis):
    selected={}
    for row in analysis['reports']:
        if row['log_schema']=='action_only':
            key=(row['domain'],row['cohort'])
            if key in selected: raise ValueError('Duplicate domain/cohort analysis')
            selected[key]=row
    if not selected: raise ValueError('Missing action-only reports for operational summary')
    return list(selected.values())


def aggregate_performance(analysis):
    reports=unique_field_reports(analysis)
    result={}
    for domain in ['all']+sorted({r['domain'] for r in reports}):
        rows=reports if domain=='all' else [r for r in reports if r['domain']==domain]
        total=sum(r['field_n'] for r in rows)
        if total<=0: raise ValueError('Empty field cohort')
        result[domain]={'field_n':total}
        for metric in ['optimal_choice_rate','mean_synthetic_regret','mean_synthetic_utility','failure_rate']:
            result[domain][metric]=float(sum(r[metric]*r['field_n'] for r in rows)/total)
    return result


def save_figure(fig,output,name):
    for ext in ['pdf','png']:
        fig.savefig(output/f'{name}.{ext}',dpi=240,facecolor='white')
    plt.close(fig)


def competence_figure(analyses,output):
    fig,axes=plt.subplots(1,2,figsize=(8.1,3.8),sharey=True)
    labels=list(analyses)
    positions=np.arange(3)
    barheight=.66/max(len(labels),1)
    maxregret=0.
    for i,(label,analysis) in enumerate(analyses.items()):
        performance=aggregate_performance(analysis)
        rates=[performance[d]['optimal_choice_rate']*100 for d in DOMAINS]
        regrets=[performance[d]['mean_synthetic_regret'] for d in DOMAINS]
        maxregret=max(maxregret,max(regrets))
        y=positions+(i-(len(labels)-1)/2)*barheight
        for ax,values in zip(axes,[rates,regrets]):
            ax.barh(y,values,height=barheight*.88,label=label,color=MODEL_COLORS[i%len(MODEL_COLORS)])
    axes[0].set_yticks(positions,labels=[d.title() for d in DOMAINS])
    axes[0].invert_yaxis()
    axes[0].set_xlim(0,100)
    axes[0].set_xlabel('Optimal choices (%)')
    axes[1].set_xlim(0,max(.005,maxregret*1.12))
    axes[1].set_xlabel('Mean utility regret')
    for ax in axes:
        ax.grid(axis='x',alpha=.16)
        ax.set_axisbelow(True)
        ax.spines[['top','right','left']].set_visible(False)
        ax.tick_params(axis='y',length=0)
    fig.suptitle('Task competence on varied delegated-choice menus',x=.08,ha='left',fontsize=12,weight='bold')
    fig.legend(*axes[0].get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.075,.92),ncol=min(len(labels),3),frameon=False)
    fig.text(.08,.035,'Observed field performance. Synthetic utilities; failures remain in the denominator and receive utility zero.',fontsize=8,color='#4E5962')
    fig.subplots_adjust(left=.12,right=.97,top=.77,bottom=.19,wspace=.18)
    save_figure(fig,output,'task-performance')


def forest_figure(analyses,output):
    fig,axes=plt.subplots(1,len(analyses),figsize=(8.1,6.5),sharex=True,sharey=True,squeeze=False)
    conditions=[(d,c) for d in DOMAINS for c in COHORTS]
    ymin,ymax=-.55,len(conditions)-.45
    limit=max(abs(r[key]) for a in analyses.values() for r in a['reports'] for key in ['lower','upper'])*1.08
    for ax,(label,analysis) in zip(axes[0],analyses.items()):
        by_key={(r['domain'],r['cohort'],r['log_schema']):r for r in analysis['reports']}
        if len(by_key)!=len(analysis['reports']): raise ValueError('Duplicate forest conditions')
        for y,(domain,cohort) in enumerate(conditions):
            if y%3==0: ax.axhspan(y-.5,y+2.5,color='#F4F6F7' if y%6==0 else '#FFFFFF',zorder=0)
            for schema,offset in [('action_only',-.14),('context_and_action',.14)]:
                r=by_key[(domain,cohort,schema)]
                ax.plot([r['lower'],r['upper']],[y+offset]*2,color=COLORS[schema],lw=2.2,solid_capstyle='round')
                ax.plot([r['lower'],r['upper']],[y+offset]*2,'|',color=COLORS[schema],markersize=5)
            target=by_key[(domain,cohort,'action_only')]['evaluation_only']['true_contrast']
            ax.scatter([target],[y],marker='D',s=16,color='#1D252A',zorder=5)
        ax.axvline(0,color='#818A91',linestyle=':',lw=1)
        ax.set_xlim(-limit,limit)
        ax.set_ylim(ymax,ymin)
        ax.set_title(label,fontsize=10,loc='left',pad=12)
        ax.set_xlabel('Product outcome contrast')
        ax.spines[['top','right','left']].set_visible(False)
        ax.tick_params(axis='y',length=0,pad=8)
        ax.grid(axis='x',alpha=.13)
    axes[0,0].set_yticks(range(len(conditions)),labels=[f'{d.title()} / {LABELS[c]}' for d,c in conditions],fontsize=8)
    fig.suptitle('What the logs support about the next product decision',x=.055,ha='left',fontsize=12,weight='bold',y=.98)
    handles=[Line2D([0],[0],color=COLORS[s],lw=2.2,label=l) for s,l in [('action_only','Action-only logs'),('context_and_action','Context + action logs')]]
    handles.append(Line2D([0],[0],color='#1D252A',marker='D',linestyle='',markersize=4,label='Known synthetic target'))
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.047,.95),ncol=3,frameon=False,fontsize=8)
    fig.text(.055,.045,'Contrast: capacity minus flexibility investment. Calibration and field uncertainty included; synthetic outcomes known.',fontsize=7.8,color='#4E5962')
    fig.text(.055,.023,'At least 96% marginal coverage under the stated stable-channel assumptions; no simultaneous-coverage claim.',fontsize=7.8,color='#4E5962')
    fig.subplots_adjust(left=.255,right=.97,bottom=.135,top=.82,wspace=.10)
    save_figure(fig,output,'decision-intervals')


def analyze_decisions(analysis):
    rows=analysis['reports']
    return {'displayed_conditions':len(rows),
        'decisive_conditions':sum(r['decision']!='unresolved' for r in rows),
        'unresolved_conditions':sum(r['decision']=='unresolved' for r in rows),
        'false_decisive_conditions':sum(r['evaluation_only']['certified_wrong_decision'] for r in rows),
        'naive_wrong_sign_conditions':sum(r['evaluation_only']['naive_wrong_decision'] for r in rows),
        'mean_interval_width':float(np.mean([r['upper']-r['lower'] for r in rows])),
        'interpretation':'Descriptive counts over dependent, selected synthetic conditions. Not an estimate of confidence-interval coverage or general customer prevalence.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mini',type=Path,required=True)
    p.add_argument('--nano',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--pricing',type=Path)
    p.add_argument('--controls',type=Path,nargs='*',default=[])
    a=p.parse_args()
    pricing=read_json(a.pricing) if a.pricing else None
    analyses={}
    summary={'scope':'Real provider responses to synthetic profiles and synthetic utility functions. No human participants.',
        'models':{},'pricing_sha256':sha256(a.pricing) if a.pricing else None}
    for label,directory in [('GPT-5.4 mini',a.mini),('GPT-5.4 nano',a.nano)]:
        data=read_json(directory/'analysis.json')
        execution=execution_summary(directory,pricing)
        analyses[label]=data
        summary['models'][label]={'execution':execution,'performance':aggregate_performance(data),
                                  'decisions':analyze_decisions(data)}
    a.output.mkdir(parents=True,exist_ok=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':8,
        'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
    forest_figure(analyses,a.output)
    for path in a.controls:
        data=read_json(path)
        analyses[data['system']]=data
    competence_figure(analyses,a.output)
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(f'Wrote publication figures and audited summary to {a.output}')


if __name__=='__main__': main()
