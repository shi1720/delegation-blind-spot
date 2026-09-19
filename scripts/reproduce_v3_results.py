#!/usr/bin/env python3
"""Verify v0.3 provenance and reproduce offline controls without any API calls.

--verify-only checks stored hashes and reruns the quick parser baseline.
The default additionally reruns all 14,400 controlled multinomial datasets.
Numerical CSV/JSON are compared exactly; figure timestamps are not compared.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify():
    directory = ROOT / 'results/precision-sweep-v3'
    manifest = json.loads((directory / 'manifest.json').read_text())
    if manifest['status'] != 'complete':
        raise ValueError('Sweep execution is not complete')
    plan = ROOT / 'experiments/v3/precision-sweep-plan.json'
    if sha(plan.read_bytes()) != manifest['plan_sha256']:
        raise ValueError('Sweep plan differs from the recorded execution')
    if json.loads(plan.read_text()) != manifest['plan']:
        raise ValueError('Embedded sweep plan differs from the source plan')
    for relative, expected in manifest['source_sha256'].items():
        if sha((ROOT / relative).read_bytes()) != expected:
            raise ValueError('Execution source hash mismatch: ' + relative)
    for name, expected in manifest['outputs_sha256'].items():
        if name == 'replicates.csv':
            raw = gzip.decompress((directory / 'replicates.csv.gz').read_bytes())
        else:
            raw = (directory / name).read_bytes()
        if sha(raw) != expected:
            raise ValueError('Recorded artifact hash mismatch: ' + name)
    parser = json.loads((ROOT / 'results/parser-baseline-v3.json').read_text())
    if sha((ROOT / 'experiments/v3/parser_baseline.py').read_bytes()) != parser['source_sha256']:
        raise ValueError('Parser source differs from its recorded run')
    print('All v0.3 source, plan, output, and compressed-data hashes verified.')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--verify-only', action='store_true')
    args = cli.parse_args()
    verify()
    with tempfile.TemporaryDirectory(prefix='delegation-v03-reproduction-') as temp:
        directory = Path(temp)
        parser_output = directory / 'parser.json'
        subprocess.run([sys.executable, str(ROOT / 'experiments/v3/parser_baseline.py'),
                        '--output', str(parser_output)], check=True)
        actual = json.loads(parser_output.read_text())
        expected = json.loads((ROOT / 'results/parser-baseline-v3.json').read_text())
        if actual != expected:
            raise ValueError('Parser result differs; check dependencies and source data')
        print('Parser: complete exact JSON reproduction passed.')
        if args.verify_only:
            print('Full sweep not rerun (--verify-only).')
            return
        sweep = directory / 'sweep'
        subprocess.run([sys.executable, str(ROOT / 'experiments/v3/precision_sweep.py'),
                        '--output', str(sweep)], check=True)
        frozen = ROOT / 'results/precision-sweep-v3'
        for name in ['replicates.csv', 'summary.csv', 'structural.json']:
            expected = (gzip.decompress((frozen / (name + '.gz')).read_bytes())
                        if name == 'replicates.csv' else (frozen / name).read_bytes())
            if (sweep / name).read_bytes() != expected:
                raise ValueError('Sweep differs: ' + name + '; compare dependency and solver versions')
            print(name + ': exact numerical reproduction passed.')


if __name__ == '__main__':
    main()
