#!/usr/bin/env python3
"""Equal-budget original-action versus explicit-preference receipt comparison."""
import argparse
import json
from pathlib import Path
from analyze import analyze, load_jsonl, response_index
from benchmark import digest


def final_records(path):
    return [r for r in load_jsonl(path) if r.get('event')=='result']


def receipt_operational_scope(reports):
    for row in reports:
        row['receipt_attribute_accuracy']=row.pop('optimal_choice_rate')
        row.pop('mean_synthetic_utility')
        row.pop('mean_synthetic_regret')
        row['operational_metric_scope']='Fraction accurately reporting the largest already supplied synthetic preference weight. Not product-choice accuracy or human preference validation.'
        row['scope']='Actual model responses reporting explicit synthetic preferences; known finite-bank synthetic future-product contrasts.'
        row['log_schema']='receipt_attribute' if row['log_schema']=='action_only' else 'context_and_receipt_attribute'
    return reports


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepared',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True,help='Original complete action experiment directory')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    manifest=json.loads((a.prepared/'manifest.json').read_text())
    source_manifest=json.loads((a.source/'manifest.json').read_text())
    if source_manifest['model_requested']!=manifest['model_requested']:
        raise ValueError('Equal-budget comparison requires the same requested model snapshot')
    rows=load_jsonl(a.prepared/'tasks.jsonl')
    original_subset=load_jsonl(a.prepared/'source-action-tasks.jsonl')
    original_full=load_jsonl(a.source/'tasks.jsonl')
    if digest(rows)!=manifest['tasks_sha256'] or digest(original_subset)!=manifest['source_action_subset_sha256'] or digest(original_full)!=manifest['source_tasks_sha256']:
        raise ValueError('Frozen task hashes do not match')
    ids={r['task_id'] for r in rows}
    if ids!={r['task_id'] for r in original_subset}: raise ValueError('Receipt and action subsets are not paired')
    receipts=final_records(a.prepared/'responses.jsonl')
    if any(r.get('system')!=manifest['model_requested'] for r in receipts):
        raise ValueError('Receipt response model does not match frozen requested model')
    response_index(receipts,ids)
    all_actions=final_records(a.source/'responses.jsonl')
    if any(r.get('system')!=manifest['model_requested'] for r in all_actions):
        raise ValueError('Original action response model does not match the paired snapshot')
    response_index(all_actions,{r['task_id'] for r in original_full})
    actions=[r for r in all_actions if r['task_id'] in ids]
    outcomes=json.loads((a.prepared/'outcomes.json').read_text())
    truth=json.loads((a.prepared/'evaluation-truth.json').read_text())
    if digest(outcomes)!=manifest['outcomes_sha256'] or digest(truth)!=manifest['evaluation_truth_sha256']:
        raise ValueError('Frozen outcome hashes do not match')
    receipt_reports=receipt_operational_scope(analyze(rows,receipts,outcomes,truth))
    action_reports=analyze(original_subset,actions,outcomes,truth)
    result={'model':manifest['model_requested'],
        'design':'Exploratory follow-up, frozen before new receipt responses; original action baseline uses the same task IDs and label budgets.',
        'scope':'The model reports preference weights it was explicitly given. This is not human feedback, privacy protection, or discovery of unknown customer preferences.',
        'confidence_scope':'At least 96% marginal coverage per primary known-contrast condition under iid stable receipt/action channels; not simultaneous coverage across the compared conditions. Human outcome uncertainty is not represented.',
        'receipt_task_count':len(rows),'receipt_reports':receipt_reports,'action_reports':action_reports,
        'source_selection_manifest':manifest}
    with a.output.open('x') as stream: json.dump(result,stream,indent=2,sort_keys=True); stream.write('\n')
    print(f'Analyzed {len(rows)} receipt responses and their same-budget original-action baseline. No human data.')


if __name__=='__main__': main()
