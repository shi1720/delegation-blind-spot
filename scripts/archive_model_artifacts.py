#!/usr/bin/env python3
"""Create deterministic compressed archives and a manifest from completed runs."""
from pathlib import Path
import gzip
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def main():
    archives=[]
    dirs=sorted((ROOT/'results').glob('model-study-*'))+sorted((ROOT/'results').glob('receipt-study-*'))
    for directory in dirs:
        if not (directory/'execution.json').exists(): continue
        for name in ['tasks.jsonl','requests.jsonl','controls.jsonl','responses.jsonl','source-action-tasks.jsonl']:
            source=directory/name
            if not source.exists(): continue
            data=source.read_bytes(); compressed=gzip.compress(data,mtime=0)
            archive=source.with_suffix(source.suffix+'.gz'); archive.write_bytes(compressed)
            archives.append({'archive':str(archive.relative_to(ROOT)),
                'uncompressed_path':str(source.relative_to(ROOT)),
                'archive_sha256':hashlib.sha256(compressed).hexdigest(),
                'uncompressed_sha256':hashlib.sha256(data).hexdigest(),
                'uncompressed_bytes':len(data),'archive_bytes':len(compressed)})
    if not archives: raise ValueError('No completed model runs found')
    (ROOT/'results/model-artifacts.json').write_text(json.dumps({
        'scope':'Real API records with synthetic input profiles; no human participants',
        'archives':archives},indent=2)+'\n')
    print('Archived',len(archives),'files;',sum(a['archive_bytes'] for a in archives),'compressed bytes')


if __name__=='__main__': main()
