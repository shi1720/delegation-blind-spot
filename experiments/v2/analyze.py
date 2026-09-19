#!/usr/bin/env python3
"""Analyze frozen benchmark responses. Synthetic utilities are not human evidence."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from delegation_blind_spot.identification import channel_intervals, contrast_bounds, probability_intervals
from benchmark import TYPES, REGIMES, digest


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def response_index(records, task_ids):
    indexed={}
    for record in records:
        tid=record['task_id']
        if tid not in task_ids: raise ValueError('Response references an unknown task')
        if tid in indexed: raise ValueError('Duplicate response: '+tid)
        indexed[tid]=record
    if set(indexed)!=set(task_ids):
        raise ValueError(f'Incomplete run: {len(set(task_ids)-set(indexed))} tasks lack a result. Do not silently drop them.')
    return indexed


def action_index(task,record,context=False):
    choice=record.get('choice_id')
    # Refusal, malformed output and HTTP failure all remain in the observable
    # failure category. Distinct detailed error types remain in raw records.
    a=TYPES.index(task['semantic_choice'][choice]) if choice in task['semantic_choice'] and not record.get('error') else 4
    return a+5*task['regime'] if context else a


def decide(lo,hi,tolerance=1e-8):
    return 'capacity' if lo>tolerance else 'flexibility' if hi<-tolerance else 'unresolved'


def minimum_distance_population(channel,frequency):
    """Declared naive point baseline, not a confidence procedure."""
    k=channel.shape[1]
    fit=minimize(lambda p:float(np.sum((channel@p-frequency)**2)),np.ones(k)/k,
        bounds=[(0.,1.)]*k,constraints=[{'type':'eq','fun':lambda p:p.sum()-1}],
        method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
    if not fit.success: raise ValueError('Point baseline failed: '+fit.message)
    return fit.x,float(np.linalg.norm(channel@fit.x-frequency))


def analyze(rows,records,outcomes,truth,alpha=(.02,.02,.01),bootstrap_replicates=200):
    if len(alpha)!=3 or min(alpha)<=0 or sum(alpha)>=1 or bootstrap_replicates<2:
        raise ValueError('Invalid uncertainty budget or bootstrap count')
    index=response_index(records,{r['task_id'] for r in rows})
    reports=[]
    conditions=sorted({(r['domain'],r['cohort']) for r in rows if r['split']=='field'})
    for domain,cohort in conditions:
        tasks=[r for r in rows if r['domain']==domain and (r['split']=='calibration' or r.get('cohort')==cohort)]
        cal=[r for r in tasks if r['split']=='calibration']
        field=[r for r in tasks if r['split']=='field']
        if not cal or not field: raise ValueError('Both independent splits are required')
        if len({r['policy'] for r in tasks})!=1: raise ValueError('Mixing agent policies invalidates this channel analysis')
        samples=np.asarray(outcomes[domain]['contrast_samples'],dtype=float)
        if samples.ndim!=2 or samples.shape[0]==0 or samples.shape[1]!=4 or not np.all(np.isfinite(samples)) or np.any(np.abs(samples)>1):
            raise ValueError('Invalid synthetic outcome sample')
        estimated_d=samples.mean(axis=0)
        d=np.asarray(outcomes[domain]['known_class_contrasts'],dtype=float)
        # Hoeffding for independent samples in [-1,1], Bonferroni over four
        # classes. Cross-class coupling by common menus does not break the union bound.
        radius=float(np.sqrt(2*np.log(2*4/alpha[2])/len(samples)))
        dlo,dhi=np.maximum(-1,estimated_d-radius),np.minimum(1,estimated_d+radius)
        operational=[]
        for t in field:
            r=index[t['task_id']]
            success=action_index(t,r)<4
            value=t['option_utilities'][r['choice_id']] if success else 0.
            best=max(t['option_utilities'].values())
            operational.append((success,value,best-value,success and r['choice_id'] in t['optimal_choices']))
        op=np.asarray(operational,dtype=float)
        for context in [False,True]:
            actions=15 if context else 5
            counts=np.zeros((actions,4),dtype=int)
            field_counts=np.zeros(actions,dtype=int)
            for t in cal: counts[action_index(t,index[t['task_id']],context),t['private_intent']]+=1
            for t in field: field_counts[action_index(t,index[t['task_id']],context)]+=1
            if np.any(counts.sum(axis=0)==0): raise ValueError('Every class needs independent calibration')
            channel=counts/counts.sum(axis=0)
            q=field_counts/field_counts.sum()
            lower,upper=channel_intervals(counts,alpha[0])
            qlo,qhi=probability_intervals(field_counts,alpha[1])
            # Secondary outcome bounds use an independent outcome sample.
            # Primary d is exactly known within the finite synthetic target bank.
            fit_lo=contrast_bounds(lower,upper,qlo,qhi,dlo)
            fit_hi=contrast_bounds(lower,upper,qlo,qhi,dhi)
            primary=contrast_bounds(lower,upper,qlo,qhi,d)
            point_pop,point_residual=minimum_distance_population(channel,q)
            point=float(d@point_pop)
            bootstrap_seed=int(digest([domain,cohort,context])[:8],16)
            rng=np.random.default_rng(bootstrap_seed)
            bootstrap=[]
            for _ in range(bootstrap_replicates):
                qb=rng.multinomial(len(field),q)/len(field)
                pb,_=minimum_distance_population(channel,qb)
                bootstrap.append(float(d@pb))
            blo,bhi=np.quantile(bootstrap,[.025,.975])
            result={
                'domain':domain,'cohort':cohort,'log_schema':'context_and_action' if context else 'action_only',
                'scope':'actual recorded decisions with synthetic profiles and synthetic product outcomes',
                'calibration_n':len(cal),'field_n':len(field),'outcome_n':len(samples),
                'failure_rate':float(1-op[:,0].mean()),'optimal_choice_rate':float(op[:,3].mean()),
                'mean_synthetic_utility':float(op[:,1].mean()),'mean_synthetic_regret':float(op[:,2].mean()),
                'channel_counts':counts.tolist(),'field_counts':field_counts.tolist(),
                'empirical_channel_singular_values':np.linalg.svd(channel,compute_uv=False).tolist(),
                'known_synthetic_class_contrasts':d.tolist(),
                'lower':primary.lower,'upper':primary.upper,
                'decision':decide(primary.lower,primary.upper),
                'lower_witness_population':primary.lower_population.tolist(),
                'upper_witness_population':primary.upper_population.tolist(),
                'outcome_scope':'Primary contrast is exactly enumerated over a frozen finite synthetic menu bank, not a human outcome.',
                'secondary_estimated_outcome':{'estimate':estimated_d.tolist(),'radius':radius,
                    'lower':fit_lo.lower,'upper':fit_hi.upper,'decision':decide(fit_lo.lower,fit_hi.upper),
                    'warning':'Includes synthetic outcome sampling uncertainty. Conservative Hoeffding intervals may be wide.'},
                'conditional_channel_bootstrap':{'lower':float(blo),'upper':float(bhi),'replicates':bootstrap_replicates,
                    'seed':bootstrap_seed,'warning':'Percentile bootstrap fixes the estimated channel, ignores its calibration error, and has no finite-sample coverage guarantee.'},
                'naive_point_contrast':point,'naive_population':point_pop.tolist(),
                'naive_channel_fit_residual':point_residual,
                'alpha_channel_field_outcome':list(alpha),
                'max_solver_constraint_violation':max(primary.max_constraint_residual,fit_lo.max_constraint_residual,fit_hi.max_constraint_residual),
            }
            # Ground truth is supplied only after the analysis, for evaluation.
            target=float(truth[domain]['cohorts'][cohort]['target_contrast'])
            correct='capacity' if target>0 else 'flexibility' if target<0 else 'tie'
            result['evaluation_only']={'true_contrast':target,'true_decision':correct,
                'interval_contains_target':bool(primary.lower<=target<=primary.upper),
                'conditional_bootstrap_contains_target':bool(blo<=target<=bhi),
                'naive_squared_error':float((point-target)**2),
                'naive_wrong_decision':bool(decide(point,point) not in [correct,'unresolved']),
                'certified_wrong_decision':bool(result['decision'] not in [correct,'unresolved']),
                'note':'One target per domain is not an empirical coverage estimate.'}
            reports.append(result)
    return reports


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepared',type=Path,required=True)
    p.add_argument('--responses',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--system',help='Analyze this system label in a multi-system response file')
    a=p.parse_args()
    rows=load_jsonl(a.prepared/'tasks.jsonl')
    manifest=json.loads((a.prepared/'manifest.json').read_text())
    if digest(rows)!=manifest['tasks_sha256']: raise ValueError('Frozen tasks were modified')
    outcomes=json.loads((a.prepared/'outcomes.json').read_text())
    if digest(outcomes)!=manifest['outcomes_sha256']: raise ValueError('Frozen outcomes were modified')
    truth=json.loads((a.prepared/'evaluation-truth.json').read_text())
    if digest(truth)!=manifest['evaluation_truth_sha256']: raise ValueError('Frozen evaluation truth was modified')
    records=load_jsonl(a.responses)
    if a.system: records=[r for r in records if r.get('system')==a.system]
    systems={r.get('system','unspecified') for r in records}
    if len(systems)>1: raise ValueError('Use --system to select one model/control')
    report={'system':next(iter(systems),'empty'),'source_records':len(records),
        'scope':'Synthetic profiles and utility functions. No customer validation.',
        'reports':analyze(rows,records,outcomes,truth)}
    with a.output.open('x') as stream: json.dump(report,stream,indent=2,sort_keys=True); stream.write('\n')
    print(f'Analyzed {len(records)} complete records across {len(report["reports"])} domain/schema conditions.')


if __name__=='__main__': main()
