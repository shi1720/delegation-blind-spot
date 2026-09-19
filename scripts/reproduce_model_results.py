#!/usr/bin/env python3
"""Recompute recorded model and available receipt analyses exactly.

No model API is called. Missing receipt comparisons are reported as unavailable,
not as successful reproductions. Use --require-receipts for a full release check.
"""
import argparse
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-receipts',action='store_true')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='delegation-reproduction-') as temp:
        for suffix in ['mini','nano']:
            prepared=ROOT/'results'/('model-study-'+suffix)
            model=json.loads((prepared/'manifest.json').read_text())['model_requested']
            output=Path(temp)/(suffix+'.json')
            subprocess.run([sys.executable,str(ROOT/'experiments/v2/analyze.py'),
                '--prepared',str(prepared),'--responses',str(prepared/'responses.jsonl'),
                '--output',str(output),'--system',model],check=True)
            actual=json.loads(output.read_text())
            expected=json.loads((prepared/'analysis.json').read_text())
            if actual!=expected:
                raise ValueError('Numerical reproduction differs for '+suffix+'; compare dependency and solver versions')
            print(suffix+': exact JSON numerical reproduction passed')
            receipt=ROOT/'results'/('receipt-study-'+suffix)
            expected_receipt=receipt/'comparison.json'
            if not expected_receipt.exists():
                if args.require_receipts: raise ValueError('Required receipt comparison missing for '+suffix)
                print(suffix+': receipt comparison is not available; receipt reproduction skipped')
                continue
            receipt_output=Path(temp)/(suffix+'-receipts.json')
            subprocess.run([sys.executable,str(ROOT/'experiments/v2/analyze_receipts.py'),
                '--prepared',str(receipt),'--source',str(prepared),'--output',str(receipt_output)],check=True)
            actual=json.loads(receipt_output.read_text())
            expected=json.loads(expected_receipt.read_text())
            if actual!=expected:
                raise ValueError('Receipt JSON reproduction differs for '+suffix+'; compare dependencies, solver versions and source artifacts')
            print(suffix+': exact receipt and equal-budget baseline JSON reproduction passed')


if __name__=='__main__': main()
