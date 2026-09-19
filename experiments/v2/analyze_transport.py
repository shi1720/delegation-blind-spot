#!/usr/bin/env python3
"""Exploratory cross-model transport sensitivity; not a valid coverage experiment.

Uses only already collected observations. It makes zero provider requests.
"""
import argparse
import json
from pathlib import Path
from analyze import analyze, load_jsonl, response_index
from benchmark import digest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--calibration',type=Path,required=True)
    p.add_argument('--field',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    manifests=[json.loads((d/'manifest.json').read_text()) for d in [a.calibration,a.field]]
    for key in ['tasks_sha256','outcomes_sha256','evaluation_truth_sha256']:
        if manifests[0][key]!=manifests[1][key]: raise ValueError('Transport requires identical frozen tasks and targets')
    rows=load_jsonl(a.calibration/'tasks.jsonl')
    if digest(rows)!=manifests[0]['tasks_sha256']: raise ValueError('Modified frozen tasks')
    indices=[]
    for directory in [a.calibration,a.field]:
        records=[r for r in load_jsonl(directory/'responses.jsonl') if r.get('event')=='result']
        indices.append(response_index(records,{r['task_id'] for r in rows}))
    # Preserve provenance without copying large raw responses or relabeling a
    # field model response as if it came from the calibration model.
    selected=[]
    for t in rows:
        origin=0 if t['split']=='calibration' else 1
        raw=indices[origin][t['task_id']]
        selected.append({'task_id':t['task_id'],'choice_id':raw.get('choice_id'),
            'error':raw.get('error'),'source_model':raw.get('model_returned',raw.get('system')),
            'source_directory':str([a.calibration,a.field][origin]),
            'source_request_id':raw.get('request_id'),'source':'reused_live_api_observation'})
    outcomes=json.loads((a.calibration/'outcomes.json').read_text())
    truth=json.loads((a.calibration/'evaluation-truth.json').read_text())
    if digest(outcomes)!=manifests[0]['outcomes_sha256'] or digest(truth)!=manifests[0]['evaluation_truth_sha256']:
        raise ValueError('Modified frozen targets')
    reports=analyze(rows,selected,outcomes,truth)
    label=manifests[0]['model_requested']+' calibrated / '+manifests[1]['model_requested']+' deployed'
    result={'system':label,'design':'Exploratory post-hoc reuse of already collected responses',
        'scope':'Synthetic profiles; no human participants; no new API calls',
        'coverage_warning':'Calibrating one model and deploying another violates the stable-channel assumption. Displayed intervals are sensitivity diagnostics and carry no stated coverage guarantee.',
        'calibration_model':manifests[0]['model_requested'],'field_model':manifests[1]['model_requested'],
        'reports':reports,'provenance':selected}
    with a.output.open('x') as stream: json.dump(result,stream,indent=2,sort_keys=True); stream.write('\n')
    print(f'Wrote exploratory transport analysis to {a.output}. No coverage guarantee or new provider calls.')


if __name__=='__main__': main()
