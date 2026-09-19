#!/usr/bin/env python3
"""Figures from recorded results only. Synthetic scope is stated on the figure."""

import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COLORS = {'uniform':'#234E70','historical_active':'#C55A31','fixed_mixture':'#8F6AB5',
          'robust_path':'#188579','oracle_residual':'#7B8188'}
LABELS = {'uniform':'Uniform + correction', 'historical_active':'Historical active',
          'fixed_mixture':'Fixed 50% mixture','robust_path':'Robust path (prior method)',
          'oracle_residual':'Oracle residuals'}


def plot(directory):
    rows = list(csv.DictReader((directory/'summary.csv').open()))
    cfg = json.loads((directory/'manifest.json').read_text())['config']
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 7.5), constrained_layout=True)
    scenarios = ['aligned', 'silent_strong', 'visible_control']
    titles = ['Aligned predictions', 'Hidden outcome shift', 'Updated-prediction control']
    for col,(scenario,title) in enumerate(zip(scenarios,titles)):
        for method in cfg['methods']:
            data = sorted([r for r in rows if r['scenario']==scenario and r['method']==method],
                          key=lambda r:float(r['budget']))
            x=np.array([float(r['budget']) for r in data])
            style='--' if method=='oracle_residual' else '-'
            for row,key in enumerate(['rmse','wald_coverage']):
                y=np.array([float(r[key]) for r in data])
                axes[row,col].plot(x,y,style,marker='o',markersize=4,
                    color=COLORS[method],label=LABELS[method],linewidth=1.6)
                if row==1:
                    err=np.array([float(r['wald_coverage_mcse']) for r in data])*1.96
                    axes[row,col].fill_between(x,y-err,y+err,color=COLORS[method],alpha=.09)
        axes[0,col].set_title(title,fontsize=12,fontweight='bold',pad=10)
        axes[1,col].axhline(.95,color='#333333',linestyle=':',linewidth=1)
        axes[1,col].set_ylim(0.3,1.02)
        axes[1,col].set_xlabel('Expected audit labels')
        for ax in axes[:,col]:
            ax.set_xscale('log')
            ax.set_xticks(cfg['expected_budgets'],[str(x) for x in cfg['expected_budgets']])
            ax.spines[['top','right']].set_visible(False)
            ax.grid(axis='y',alpha=.18)
    axes[0,0].set_ylabel('RMSE of outcome contrast')
    axes[1,0].set_ylabel('Coverage of nominal 95% Wald interval')
    fig.suptitle('The Delegation Blind Spot | baseline falsification pilot\n'
                 'Synthetic fixed populations; 1,000 audit replicates; no human or LLM evidence',
                 fontsize=14)
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=3,frameon=False,fontsize=9)
    for extension in ['png','pdf','svg']:
        fig.savefig(directory/f'pilot-overview.{extension}',dpi=180,bbox_inches='tight')
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--results',type=Path,default=ROOT/'results/pilot-v1')
    plot(parser.parse_args().results.resolve())
