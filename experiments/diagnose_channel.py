#!/usr/bin/env python3
"""Small transparent diagnostic examples, not empirical agent evidence."""

from pathlib import Path
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from delegation_blind_spot.identification import contrast_bounds


def main():
    p=np.array([.6,.4])
    d=np.array([-.3,.5])
    examples=[]
    for name,A in [
        ('intent_revealing',np.array([[.9,.1],[.1,.9]])),
        ('intent_pooling',np.array([[.8,.8],[.2,.2]])),
    ]:
        q=A@p
        for radius in [0., .05, .2]:
            lo=np.maximum(0.,A-radius); hi=np.minimum(1.,A+radius)
            r=contrast_bounds(lo,hi,q,q,d)
            examples.append(dict(name=name,channel_radius=radius,actual_contrast=float(d@p),
                lower=r.lower,upper=r.upper,decision=r.decision,
                lower_population=r.lower_population.tolist(),upper_population=r.upper_population.tolist(),
                max_constraint_residual=r.max_constraint_residual))
    out=ROOT/'results'/'channel-diagnostic.json'
    out.write_text(json.dumps({'scope':'constructed channel examples, no human or LLM data',
                               'examples':examples},indent=2)+'\n')
    for row in examples:
        print(row['name'],row['channel_radius'],[round(row['lower'],4),round(row['upper'],4)],row['decision'])


if __name__=='__main__':
    main()
