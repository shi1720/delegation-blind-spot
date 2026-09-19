#!/usr/bin/env python3
"""Verify v0.3 provenance and reproduce offline controls without any API calls.

--verify-only checks stored hashes and reruns the quick parser baseline.
The default additionally reruns all 14,400 controlled multinomial datasets.
--parser-atol explicitly permits cross-platform rounding in parser float leaves;
it never relaxes source hashes, discrete values, or sweep byte comparisons.
Numerical CSV/JSON are compared exactly by default; figure timestamps are not compared.
"""
import argparse
import gzip
import hashlib
import json
import math
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


def compare_parser(actual, expected, atol=0.0, path='$'):
    """Return absolute float differences; all non-float structure remains exact."""
    if not math.isfinite(atol) or atol < 0:
        raise ValueError('Parser absolute tolerance must be finite and nonnegative')
    if type(actual) is not type(expected):
        raise ValueError('Parser value type differs at ' + path)
    if isinstance(expected, dict):
        if actual.keys() != expected.keys():
            raise ValueError('Parser keys differ at ' + path)
        return [d for key in expected for d in compare_parser(actual[key], expected[key], atol, path + '.' + key)]
    if isinstance(expected, list):
        if len(actual) != len(expected):
            raise ValueError('Parser list length differs at ' + path)
        return [d for i, (a, e) in enumerate(zip(actual, expected))
                for d in compare_parser(a, e, atol, path + '[' + str(i) + ']')]
    if isinstance(expected, float):
        if not math.isfinite(actual) or not math.isfinite(expected):
            raise ValueError('Nonfinite parser value at ' + path)
        difference = abs(actual - expected)
        if difference > atol:
            raise ValueError('Parser numerical result differs at ' + path +
                             ': absolute difference ' + str(difference) + ' exceeds ' + str(atol))
        return [difference] if difference else []
    if actual != expected:
        raise ValueError('Parser exact value differs at ' + path)
    return []


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--verify-only', action='store_true')
    cli.add_argument('--parser-atol', type=float, default=0.0,
                     help='Explicit absolute tolerance for parser float leaves only; default exact. Counts, decisions, types, keys and hashes remain exact.')
    args = cli.parse_args()
    if not math.isfinite(args.parser_atol) or args.parser_atol < 0:
        cli.error('--parser-atol must be finite and nonnegative')
    verify()
    with tempfile.TemporaryDirectory(prefix='delegation-v03-reproduction-') as temp:
        directory = Path(temp)
        parser_output = directory / 'parser.json'
        subprocess.run([sys.executable, str(ROOT / 'experiments/v3/parser_baseline.py'),
                        '--output', str(parser_output)], check=True)
        actual = json.loads(parser_output.read_text())
        expected = json.loads((ROOT / 'results/parser-baseline-v3.json').read_text())
        differences = compare_parser(actual, expected, args.parser_atol)
        if differences:
            print('Parser: cross-platform numerical equivalence passed at absolute tolerance ' +
                  str(args.parser_atol) + '; ' + str(len(differences)) +
                  ' float leaves differ; maximum absolute difference ' + str(max(differences)) +
                  '. Non-float values and provenance match exactly. This is not byte-exact reproduction.')
        else:
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
