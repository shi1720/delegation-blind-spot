#!/usr/bin/env python3
"""Freeze a varied synthetic benchmark and controls. Does not call any model."""
import argparse
import json
from pathlib import Path
import platform
from benchmark import controls, digest, generate, request


def write(path, data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--model',required=True)
    p.add_argument('--seed',type=int,default=73912)
    p.add_argument('--calibration-per-class',type=int,default=40)
    p.add_argument('--field-size',type=int,default=160)
    p.add_argument('--outcome-audits',type=int,default=256)
    p.add_argument('--policy',choices=['direct','concise'],default='direct')
    p.add_argument('--domains',nargs='+',default=['travel','cloud','workflow'])
    p.add_argument('--populations',nargs='+',default=['positive','negative','near'])
    a=p.parse_args()
    rows,outcomes,truth=generate(a.seed,a.calibration_per_class,a.field_size,
        a.outcome_audits,a.policy,a.domains,a.populations)
    a.output.mkdir(parents=True,exist_ok=False)
    (a.output/'tasks.jsonl').write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in rows))
    (a.output/'requests.jsonl').write_text(''.join(json.dumps({'task_id':r['task_id'],
        'request':request(r,a.model)},sort_keys=True)+'\n' for r in rows))
    (a.output/'controls.jsonl').write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in controls(rows)))
    write(a.output/'outcomes.json',outcomes)
    write(a.output/'evaluation-truth.json',truth)
    write(a.output/'manifest.json',{'benchmark':'delegation-v2','scope':'synthetic profiles and synthetic utilities; no human participants',
        'mode':'prepared_only','model_requested':a.model,'seed':a.seed,
        'policy':a.policy,'domains':a.domains,'populations':a.populations,'calibration_per_class':a.calibration_per_class,
        'field_size':a.field_size,'outcome_audits':a.outcome_audits,'task_count':len(rows),
        'tasks_sha256':digest(rows),'outcomes_sha256':digest(outcomes),'evaluation_truth_sha256':digest(truth),
        'python':platform.python_version(),
        'uncertainty_budget':{'channel':.02,'field':.02,'outcome':.01},
        'selection_policy':'all prepared records must be retained, including refusal and API failure',
        'source_sha256':{f.name:__import__('hashlib').sha256(f.read_bytes()).hexdigest()
            for f in sorted(Path(__file__).parent.glob('*.py'))}})
    print(f'Prepared {len(rows)} tasks. No API calls or human participants.')


if __name__=='__main__': main()
