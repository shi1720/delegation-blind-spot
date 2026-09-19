#!/usr/bin/env python3
"""Independent controlled multinomial simulation, not new model/customer data."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'src'))
from delegation_blind_spot.identification import channel_intervals, probability_intervals, contrast_bounds


def channel(eta):
    if not np.isfinite(eta) or not 0 <= eta <= 1:
        raise ValueError('eta must lie in [0,1]')
    return (1-float(eta))*np.ones((4,4))/4 + float(eta)*np.eye(4)


def structural(A, p, d, eta):
    q = A @ p
    fit = contrast_bounds(A,A,q,q,d)
    expected_width = float(np.ptp(d)) if eta == 0 else 0.
    width = fit.upper-fit.lower
    if abs(width-expected_width)>1e-7:
        raise ArithmeticError('Structural LP disagrees with the analytic width')
    return {'lower':fit.lower,'upper':fit.upper,'width':width,
            'analytic_width':expected_width,
            'lower_population':fit.lower_population.tolist(),
            'upper_population':fit.upper_population.tolist(),
            'max_constraint_residual':fit.max_constraint_residual}


def one_replicate(A,p,d,ncal,nfield,rng,alpha_channel=.02,alpha_field=.02):
    counts = np.column_stack([rng.multinomial(ncal,A[:,k]) for k in range(4)])
    q = A @ p
    field = rng.multinomial(nfield,q)
    alo,ahi = channel_intervals(counts,alpha_channel)
    qlo,qhi = probability_intervals(field,alpha_field)
    settings = {'field_only':(A,A,qlo,qhi),
                'calibration_only':(alo,ahi,q,q),
                'joint':(alo,ahi,qlo,qhi)}
    output = {}
    target=float(d@p)
    for method,args in settings.items():
        try:
            fit=contrast_bounds(*args,d)
            # Recompute witness feasibility outside the solver wrapper.
            lo,hi,flo,fhi=args
            max_residual=fit.max_constraint_residual
            for pop,joint in [(fit.lower_population,fit.lower_joint),
                              (fit.upper_population,fit.upper_joint)]:
                residual=max(float(np.max(np.abs(joint.sum(axis=0)-pop))),
                    float(np.max(lo*pop-joint)),float(np.max(joint-hi*pop)),
                    float(np.max(flo-joint.sum(axis=1))),
                    float(np.max(joint.sum(axis=1)-fhi)),
                    abs(float(pop.sum()-1)),float(np.max(-pop)),float(np.max(-joint)),0.)
                max_residual=max(max_residual,residual)
            if max_residual>1e-7: raise ArithmeticError('Independent witness check failed')
            resolved=fit.lower>1e-8 or fit.upper < -1e-8
            wrong=(fit.lower>1e-8 and target<=0) or (fit.upper < -1e-8 and target>=0)
            output[method]={'feasible':True,'covered':fit.lower-1e-10<=target<=fit.upper+1e-10,
                'resolved':resolved,'wrong_resolution':wrong,'lower':fit.lower,'upper':fit.upper,
                'width':fit.upper-fit.lower,'max_constraint_residual':max_residual,'error':''}
        except ValueError as exc:
            # Empty confidence/model intersection is retained as failure.
            output[method]={'feasible':False,'covered':False,'resolved':False,
                'wrong_resolution':False,'lower':None,'upper':None,'width':None,
                'max_constraint_residual':None,'error':str(exc)}
    return output


def summarize(records):
    n=len(records)
    if n==0: raise ValueError('Cannot summarize no replicates')
    out={'replicates':n}
    for key in ['feasible','covered','resolved','wrong_resolution']:
        count=sum(bool(r[key]) for r in records); rate=count/n
        out[key+'_count']=count; out[key+'_rate']=rate
        out[key+'_mcse']=float(np.sqrt(rate*(1-rate)/n))
    # A plug-in Monte Carlo SE is zero at a boundary; also show exact count CIs.
    from scipy.stats import beta
    for key in ['covered','wrong_resolution']:
        count=out[key+'_count']
        out[key+'_mc_ci_lower']=0. if count==0 else float(beta.ppf(.025,count,n-count+1))
        out[key+'_mc_ci_upper']=1. if count==n else float(beta.ppf(.975,count+1,n-count))
    widths=[r['width'] for r in records if r['feasible']]
    out['infeasible_count']=n-out['feasible_count']
    out['width_feasible_n']=len(widths)
    for quantile,label in [(.1,'p10'),(.5,'median'),(.9,'p90')]:
        out['width_'+label]=float(np.quantile(widths,quantile)) if widths else None
    out['max_constraint_residual']=max((r['max_constraint_residual'] for r in records if r['feasible']),default=None)
    return out


def write_csv(path,records):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)


def plot(summary,structural_rows,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    fig,axes=plt.subplots(1,3,figsize=(12.2,3.75),layout='constrained')
    etas=sorted({r['eta'] for r in summary}); colors=plt.cm.viridis(np.linspace(.08,.9,len(etas)))
    x=np.arange(len(etas))
    ax=axes[0]
    widths=[next(r['analytic_width'] for r in structural_rows if r['eta']==e and r['cohort']=='positive') for e in etas]
    ax.plot(x,widths,'o-',color='#39455b'); ax.set_xticks(x,[str(e) for e in etas]); ax.set_ylim(-.003,.108)
    ax.set_xlabel('Channel separation (eta)'); ax.set_ylabel('Exact structural width')
    ax.set_title('A. Exact A and exact q')
    styles={'field_only':'--','calibration_only':':','joint':'-'}
    for eta,color in zip(etas,colors):
        for method,style in styles.items():
            rs=sorted([r for r in summary if r['eta']==eta and r['method']==method and r['cohort']=='positive'],key=lambda r:r['calibration_per_class'])
            axes[1].plot([r['calibration_per_class'] for r in rs],[r['width_median'] for r in rs],style,color=color,marker='.' if method=='joint' else None)
        rs=sorted([r for r in summary if r['eta']==eta and r['method']=='joint' and r['cohort']=='positive'],key=lambda r:r['calibration_per_class'])
        axes[2].plot([r['calibration_per_class'] for r in rs],[r['resolved_rate'] for r in rs],'-o',color=color,label=f'{eta:g}')
    axes[1].set_title('B. Finite-sample interval width'); axes[1].set_ylabel('Median width, feasible intervals')
    axes[2].set_title('C. Joint method resolution'); axes[2].set_ylabel('Resolved fraction, all replicates'); axes[2].set_ylim(-.03,1.03)
    for ax in axes[1:]:
        ax.set_xscale('log',base=4); ax.set_xticks([40,160,640,2560],[40,160,640,2560]); ax.set_xlabel('Calibration observations per class')
    for ax in axes: ax.grid(alpha=.15); ax.spines[['top','right']].set_visible(False)
    axes[1].legend(handles=[Line2D([0],[0],color='#444',linestyle=s,label=m.replace('_',' ')) for m,s in styles.items()],loc='upper right',fontsize=7)
    axes[2].legend(title='eta',fontsize=7,title_fontsize=8,ncol=2,loc='upper left')
    fig.suptitle('Controlled multinomial simulation | positive cohort | field size = 2 x calibration/class',fontsize=11)
    for suffix in ['pdf','svg','png']: fig.savefig(output/f'precision-sweep.{suffix}',dpi=180)
    plt.close(fig)


def run(plan,output):
    output=Path(output); output.mkdir(parents=True,exist_ok=False)
    frozen=json.loads(Path(plan).read_text())
    raw=Path(plan).read_bytes()
    manifest={'scope':frozen['scope'],'started_utc':datetime.now(timezone.utc).isoformat(),
        'plan':frozen,'plan_sha256':hashlib.sha256(raw).hexdigest(),
        'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__),ROOT/'src/delegation_blind_spot/identification.py']},
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'status':'running','observations':'controlled multinomial draws, not LLM calls or people'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    d=np.asarray(frozen['contrast']); summaries=[]; all_records=[]; structure=[]
    cells=[(eta,n,cohort,p) for eta in frozen['etas'] for n in frozen['calibration_per_class']
           for cohort,p in frozen['populations'].items()]
    # Each cell is an independent deterministic child stream. Repeated runs
    # reproduce arrays; different budgets/etas do not reuse pseudo-observations.
    children=np.random.SeedSequence(frozen['seed']).spawn(len(cells))
    for ci,((eta,ncal,cohort,p),seed) in enumerate(zip(cells,children)):
        A=channel(eta); p=np.asarray(p); rng=np.random.default_rng(seed)
        nfield=frozen['field_multiplier']*ncal
        structural_result=structural(A,p,d,eta)
        structure.append({'eta':eta,'calibration_per_class':ncal,'cohort':cohort,
            'true_contrast':float(d@p),**structural_result})
        groups={m:[] for m in frozen['methods']}
        for rep in range(frozen['replicates_per_cell']):
            results=one_replicate(A,p,d,ncal,nfield,rng,frozen['alpha_channel'],frozen['alpha_field'])
            for method,r in results.items():
                groups[method].append(r)
                all_records.append({'eta':eta,'calibration_per_class':ncal,'field_n':nfield,
                    'cohort':cohort,'replicate':rep,'method':method,'true_contrast':float(d@p),**r})
        for method,rows in groups.items():
            alpha=(frozen['alpha_field'] if method=='field_only' else frozen['alpha_channel'] if method=='calibration_only' else frozen['alpha_channel']+frozen['alpha_field'])
            summaries.append({'eta':eta,'calibration_per_class':ncal,'field_n':nfield,
                'cohort':cohort,'method':method,'true_contrast':float(d@p),
                'structural_width':structural_result['analytic_width'],'nominal_minimum_coverage':1-alpha,
                **summarize(rows)})
        print(f'{ci+1}/{len(cells)} eta={eta:g} ncal={ncal} cohort={cohort}',flush=True)
    write_csv(output/'replicates.csv',all_records); write_csv(output/'summary.csv',summaries)
    (output/'structural.json').write_text(json.dumps(structure,indent=2,sort_keys=True)+'\n')
    plot(summaries,structure,output)
    manifest.update({'status':'complete','finished_utc':datetime.now(timezone.utc).isoformat(),
        'independent_replicates':len(cells)*frozen['replicates_per_cell'],
        'method_evaluations':len(all_records),'summary_rows':len(summaries),
        'outputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name!='manifest.json'}})
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('precision-sweep-plan.json'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); run(args.plan,args.output)
