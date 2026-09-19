#!/usr/bin/env python3
"""Offline deterministic supplied-profile baseline for the receipt subset.

This parser reads only supplied numerical weights, not private evaluation labels.
Its identity channel is known within the published four-profile construction.
It is not a method for discovering unknown human preferences.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'experiments/v2'))
from benchmark import WEIGHTS,digest
from delegation_blind_spot.identification import probability_intervals,contrast_bounds

PLAN={
    'design':'Exploratory offline analysis of the already selected receipt field subset.',
    'measurement':'Deterministic argmax of the four explicitly supplied weights; check membership in the published synthetic profile taxonomy.',
    'models_or_human_participants':0,
    'alpha':.04,
    'methods':['known_identity_channel_with_multinomial_CP','direct_bounded_contrast_Hoeffding'],
    'calibration_observations_used':0,
    'selection':'Use every field task in the frozen receipt subset, with no outcome-dependent filtering.',
    'target':'Original known finite-bank synthetic class contrasts, held fixed.',
    'coverage_scope':'Each method has at least96% marginal coverage under its fixed-design iid sampling assumptions. They are reported separately, not intersected. No adjustment for choosing this follow-up after viewing earlier results or for reuse of original field draws.',
    'resource_scope':'Same field observation count as receipts. Does not equalize privacy, elicitation burden or other costs.',
}


def extract_supplied_class(prompt):
    """Return a class via public supplied weights; reject unsupported profiles."""
    payload=json.loads(prompt) if isinstance(prompt,str) else prompt
    preferences=payload['customer_supplied_preferences']
    if not isinstance(preferences,list) or len(preferences)!=4:
        raise ValueError('Expected exactly four supplied attributes')
    attributes={item['attribute_id']:item['weight'] for item in preferences}
    if len(attributes)!=4 or set(attributes)!=set('ABCD'):
        raise ValueError('Attribute IDs must be unique A/B/C/D')
    weights=np.asarray([attributes[a] for a in 'ABCD'],dtype=float)
    if not np.all(np.isfinite(weights)) or np.any(weights<0) or not np.isclose(weights.sum(),1.,rtol=0,atol=1e-12):
        raise ValueError('Invalid supplied weight vector')
    k=int(np.argmax(weights))
    if np.sum(weights==weights[k])!=1:
        raise ValueError('Supplied maximum is not unique')
    # Identity is a property of this declared taxonomy, not of arbitrary users.
    if not np.allclose(weights,WEIGHTS[k],rtol=0,atol=1e-12):
        raise ValueError('Supplied profile falls outside the frozen synthetic taxonomy')
    return k


def decision(lower,upper):
    return 'capacity' if lower>1e-8 else 'flexibility' if upper< -1e-8 else 'unresolved'


def infer_from_counts(counts,contrast,alpha=.04):
    counts=np.asarray(counts)
    d=np.asarray(contrast,dtype=float)
    if counts.shape!=(4,) or d.shape!=(4,) or not np.all(np.isfinite(d)):
        raise ValueError('Four counts and finite class contrasts are required')
    if not 0<alpha<1 or counts.sum()<=0:
        raise ValueError('Positive field count and valid error budget are required')
    qlo,qhi=probability_intervals(counts,alpha)
    fit=contrast_bounds(np.eye(4),np.eye(4),qlo,qhi,d)
    n=int(counts.sum())
    point=float(d@counts/n)
    radius=float(np.ptp(d)*np.sqrt(np.log(2/alpha)/(2*n)))
    h_lower=max(float(d.min()),point-radius)
    h_upper=min(float(d.max()),point+radius)
    return {'field_n':n,'class_counts':counts.astype(int).tolist(),'class_contrasts':d.tolist(),
        'point_contrast':point,'known_channel':'Identity on four declared supplied-weight classes.',
        'known_identity_channel_with_multinomial_CP':{
            'lower':fit.lower,'upper':fit.upper,'decision':decision(fit.lower,fit.upper),
            'lower_witness_population':fit.lower_population.tolist(),
            'upper_witness_population':fit.upper_population.tolist(),
            'max_solver_constraint_violation':fit.max_constraint_residual,'alpha':alpha},
        'direct_bounded_contrast_Hoeffding':{
            'lower':h_lower,'upper':h_upper,'decision':decision(h_lower,h_upper),
            'radius_before_range_intersection':radius,'observation_support':[float(d.min()),float(d.max())],
            'alpha':alpha}}


def analyze(rows,outcomes,alpha=.04):
    groups=defaultdict(list)
    ids=set()
    for row in rows:
        if row['task_id'] in ids: raise ValueError('Duplicate frozen task ID')
        ids.add(row['task_id'])
        if row['split']=='field': groups[(row['domain'],row['cohort'])].append(row)
    if not groups: raise ValueError('No field rows')
    reports=[]
    for (domain,cohort),field in sorted(groups.items()):
        counts=np.zeros(4,dtype=int)
        for row in field: counts[extract_supplied_class(row['prompt'])]+=1
        result=infer_from_counts(counts,outcomes[domain]['known_class_contrasts'],alpha)
        result.update({'domain':domain,'cohort':cohort,'parser_extraction_count':len(field),
            'calibration_observations_used':0,'api_requests':0})
        reports.append(result)
    return reports


def add_evaluation(reports,truth):
    """Attach synthetic target assessment only after inference is complete."""
    for row in reports:
        target=float(truth[row['domain']]['cohorts'][row['cohort']]['target_contrast'])
        correct=decision(target,target)
        row['evaluation_only']={'true_contrast':target,'true_decision':correct}
        for method in PLAN['methods']:
            interval=row[method]
            row['evaluation_only'][method]={
                'contains_target':bool(interval['lower']<=target<=interval['upper']),
                'wrong_decisive':bool(interval['decision'] not in ['unresolved',correct])}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepared',type=Path,default=ROOT/'results/receipt-study-mini')
    p.add_argument('--output',type=Path,default=ROOT/'results/parser-baseline-v3.json')
    a=p.parse_args()
    manifest=json.loads((a.prepared/'manifest.json').read_text())
    rows=[json.loads(s) for s in (a.prepared/'tasks.jsonl').read_text().splitlines() if s.strip()]
    outcomes=json.loads((a.prepared/'outcomes.json').read_text())
    if digest(rows)!=manifest['tasks_sha256'] or digest(outcomes)!=manifest['outcomes_sha256']:
        raise ValueError('Frozen inputs have changed')
    reports=analyze(rows,outcomes,PLAN['alpha'])
    truth=json.loads((a.prepared/'evaluation-truth.json').read_text())
    if digest(truth)!=manifest['evaluation_truth_sha256']: raise ValueError('Frozen evaluation truth has changed')
    add_evaluation(reports,truth)
    summary={method:{'resolved':sum(r[method]['decision']!='unresolved' for r in reports),
        'conditions':len(reports),'wrong_decisive':sum(r['evaluation_only'][method]['wrong_decisive'] for r in reports),
        'mean_width':float(np.mean([r[method]['upper']-r[method]['lower'] for r in reports]))}
        for method in PLAN['methods']}
    artifact={'plan':PLAN,'source_tasks_sha256':manifest['tasks_sha256'],
        'source_outcomes_sha256':manifest['outcomes_sha256'],
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'field_observations':sum(r['field_n'] for r in reports),'reports':reports,'summary':summary,
        'scope':'Offline deterministic extraction of supplied synthetic preferences. Zero new API calls, zero human participants. Descriptive exploratory comparison only.'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x') as stream: json.dump(artifact,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'output':str(a.output),'field_observations':artifact['field_observations'],'summary':summary}))


if __name__=='__main__':main()
