#!/usr/bin/env python3
"""Prepare requests, run declared controls, or execute actual Responses API calls.

No API call is made unless --execute is supplied. No automatic retry hides
failures or duplicates a potentially billable request.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from delegation_blind_spot.tasks import make_tasks, parse_response, request_body


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--model', required=True, help='Exact model ID, recorded without substitution')
    parser.add_argument('--repetitions', type=int, default=3)
    parser.add_argument('--max-output-tokens', type=int, default=512)
    parser.add_argument('--max-calls', type=int, default=216)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if args.execute and args.controls:
        parser.error('Controls and live model experiments require separate outputs')
    if args.max_calls < 1 or args.max_output_tokens < 16:
        parser.error('Invalid request limits')
    key = os.environ.get('OPENAI_API_KEY')
    if args.execute and not key:
        parser.error('Set OPENAI_API_KEY securely in the process environment; do not put it in this repository')
    args.output.mkdir(parents=True, exist_ok=False)
    tasks = make_tasks(args.repetitions)
    # Randomize execution order to distribute time drift across conditions.
    random.Random(20260919).shuffle(tasks)
    prepared = [{'task': task, 'request': request_body(task, args.model, args.max_output_tokens)}
                for task in tasks]
    serialized = '\n'.join(json.dumps(row, sort_keys=True) for row in prepared)+'\n'
    (args.output/'requests.jsonl').write_text(serialized)
    source_paths = [Path(__file__), ROOT/'src/delegation_blind_spot/tasks.py']
    write_json(args.output/'manifest.json', {
        'scope': 'constructed profiles and utilities; instrument validation only',
        'mode': 'live_api' if args.execute else 'controls' if args.controls else 'prepared_only',
        'model_requested': args.model, 'task_count': len(tasks), 'max_calls': args.max_calls,
        'max_output_tokens': args.max_output_tokens, 'repetitions': args.repetitions,
        'request_sha256': hashlib.sha256(serialized.encode()).hexdigest(),
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
        'python': platform.python_version(), 'created_unix': time.time(),
        'cost_policy': 'Request count and output tokens capped. Dollar cost is not estimated without verified model pricing. Usage is recorded from each response.',
    })
    if args.controls:
        rng = random.Random(170)
        rows = []
        for task in tasks:
            controls = {'optimal': task['optimal_choice'],
                        'uniform_random': rng.choice(['A', 'B', 'C']),
                        'always_balanced': next(k for k,v in task['semantic_choice'].items() if v == 'balanced')}
            for name, choice in controls.items():
                rows.append({'task_id': task['id'], 'control': name, 'choice_id': choice,
                             'utility': task['utilities'][choice],
                             'regret': max(task['utilities'].values())-task['utilities'][choice]})
        write_json(args.output/'controls.json', rows)
        print(f'Wrote {len(rows)} control decisions. No model was called.')
        return
    if not args.execute:
        print(f'Prepared {len(tasks)} requests. No model was called.')
        return
    usage = {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0}
    completed = failures = attempted = 0
    with (args.output/'responses.jsonl').open('x') as stream:
        for row in prepared[:args.max_calls]:
            started = time.time()
            attempted += 1
            stream.write(json.dumps({'event': 'attempt', 'task_id': row['task']['id'], 'time': started})+'\n')
            stream.flush()
            record = {'event': 'result', 'task_id': row['task']['id']}
            try:
                request = urllib.request.Request('https://api.openai.com/v1/responses',
                    data=json.dumps(row['request']).encode(), method='POST',
                    headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json'})
                with urllib.request.urlopen(request, timeout=120) as response:
                    raw = json.load(response)
                    record['request_id'] = response.headers.get('x-request-id')
                record['response'] = raw
                for name in usage:
                    usage[name] += raw.get('usage', {}).get(name, 0) or 0
                record['choice_id'] = parse_response(raw)
                completed += 1
            except urllib.error.HTTPError as error:
                record['error'] = {'type': 'HTTPError', 'status': error.code}
                failures += 1
            except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
                record['error'] = {'type': type(error).__name__}
                failures += 1
            record['elapsed_seconds'] = time.time()-started
            stream.write(json.dumps(record, sort_keys=True)+'\n'); stream.flush()
            write_json(args.output/'progress.json', {'attempted': attempted, 'completed': completed,
                'failures': failures, 'usage': usage, 'planned_tasks': len(tasks)})
            if 'error' in record:
                print('Stopped after a failed or incomplete request. It remains in the record; no automatic retry.')
                break
    print(json.dumps({'completed': completed, 'failures': failures, 'usage': usage}))


if __name__ == '__main__':
    main()
