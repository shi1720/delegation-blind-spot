#!/usr/bin/env python3
"""Execute frozen synthetic tasks against real models, preserving every attempt.

Credentials are read only from OPENAI_API_KEY. No automatic retry or resume can
silently replace an observation. Each output directory must be prepared first.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request


def decode_choice(raw):
    if raw.get('status') != 'completed':
        raise ValueError('incomplete')
    content=[c for item in raw.get('output',[]) if item.get('type')=='message'
             for c in item.get('content',[])]
    if any(c.get('type')=='refusal' for c in content):
        raise ValueError('refusal')
    answer=json.loads(''.join(c['text'] for c in content if c.get('type')=='output_text'))
    if not isinstance(answer,dict) or set(answer)!={'choice_id'} or not isinstance(answer['choice_id'],str) or answer['choice_id'] not in ('A','B','C','D'):
        raise ValueError('invalid_schema')
    return answer['choice_id']


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directories',type=Path,nargs='+',required=True)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--requests-per-second',type=float,default=8.)
    p.add_argument('--max-total-requests',type=int,default=6000)
    args=p.parse_args()
    key=os.environ.get('OPENAI_API_KEY')
    if not key: p.error('OPENAI_API_KEY is not configured')
    if not 1<=args.workers<=32 or not 0<args.requests_per_second<=20:
        p.error('Invalid concurrency limits')
    datasets=[]
    for directory in args.directories:
        requests=directory/'requests.jsonl'
        rows=[json.loads(s) for s in requests.read_text().splitlines()]
        if (directory/'responses.jsonl').exists(): p.error('Refusing to overwrite responses in '+str(directory))
        manifest=json.loads((directory/'manifest.json').read_text())
        datasets.append((directory,rows,manifest))
    total=sum(len(rows) for _,rows,_ in datasets)
    if total>args.max_total_requests: p.error(f'{total} exceeds request cap')
    streams={d:(d/'responses.jsonl').open('x') for d,_,_ in datasets}
    for d,_,manifest in datasets:
        execution={'scope':'Real API responses to synthetic profiles; zero human participants',
            'model_requested':manifest['model_requested'], 'started_unix':time.time(),
            'request_sha256':hashlib.sha256((d/'requests.jsonl').read_bytes()).hexdigest(),
            'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'workers':args.workers,'global_requests_per_second':args.requests_per_second,
            'automatic_retries':0,'max_total_requests':args.max_total_requests,
            'endpoint':'https://api.openai.com/v1/responses'}
        (d/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    lock=threading.Lock(); next_slot=[time.monotonic()]

    def run(directory,row):
        with lock:
            scheduled=max(time.monotonic(),next_slot[0])
            next_slot[0]=scheduled+1/args.requests_per_second
        time.sleep(max(0,scheduled-time.monotonic()))
        request=row['request']; start=time.time()
        record={'task_id':row['task_id'],'system':request['model'],'source':'live_api',
                'started_unix':start,'choice_id':None}
        with lock:
            streams[directory].write(json.dumps({'event':'attempt','task_id':row['task_id'],'time':start})+'\n')
            streams[directory].flush()
        try:
            req=urllib.request.Request('https://api.openai.com/v1/responses',
                data=json.dumps(request).encode(),method='POST',
                headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=60) as response:
                raw=json.load(response)
                record['request_id']=response.headers.get('x-request-id')
            record['response']=raw
            record['model_returned']=raw.get('model')
            record['usage']=raw.get('usage',{})
            record['choice_id']=decode_choice(raw)
        except urllib.error.HTTPError as error:
            record['error']={'type':'HTTPError','status':error.code}
        except (urllib.error.URLError,TimeoutError,OSError,ValueError,KeyError,TypeError) as error:
            record['error']={'type':type(error).__name__}
        record['elapsed_seconds']=time.time()-start
        return directory,record

    progress={str(d):{'completed':0,'failures':0,'input_tokens':0,'output_tokens':0} for d,_,_ in datasets}
    # Interleave models to reduce model-by-time confounding.
    jobs=[]
    for i in range(max(len(rows) for _,rows,_ in datasets)):
        jobs.extend((d,rows[i]) for d,rows,_ in datasets if i<len(rows))
    finished=0
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures=[pool.submit(run,d,row) for d,row in jobs]
            for future in as_completed(futures):
                d,record=future.result(); record['event']='result'
                with lock:
                    streams[d].write(json.dumps(record,sort_keys=True)+'\n'); streams[d].flush()
                state=progress[str(d)]; state['completed']+=1
                state['failures']+=int('error' in record)
                for name in ['input_tokens','output_tokens']:
                    state[name]+=record.get('usage',{}).get(name,0) or 0
                (d/'progress.json').write_text(json.dumps(state,indent=2)+'\n')
                finished+=1
                if finished%100==0 or finished==total:
                    print(json.dumps({'finished':finished,'total':total,'progress':progress}),flush=True)
    finally:
        for stream in streams.values(): stream.close()


if __name__=='__main__': main()
