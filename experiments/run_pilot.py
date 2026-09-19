#!/usr/bin/env python3
"""Frozen finite-pool, repeated-audit pilot. No new-method claims."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from delegation_blind_spot.model import make_population
from delegation_blind_spot.sampling import policy, oracle_policy
from delegation_blind_spot.estimation import estimate_batch, exact_design_variance


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def binomial_mcse(rate, n):
    return float(np.sqrt(rate*(1-rate)/n))


def run(config_path, output):
    config = json.loads(config_path.read_text())
    output.mkdir(parents=True, exist_ok=True)
    if (output / 'manifest.json').exists():
        raise FileExistsError('Existing experiment results: choose a new --output to preserve the record')
    started = time.time()
    source_files = sorted((ROOT/'src').rglob('*.py')) + sorted((ROOT/'experiments').glob('*.py'))
    provenance = {
        'config': config,
        'config_sha256': sha(config_path),
        'source_sha256': {str(p.relative_to(ROOT)):sha(p) for p in source_files},
        'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
        'git_commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
        'git_status': subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True),
        'estimand': 'fixed_pool_arm1_mean_minus_arm0_mean',
        'data': 'synthetic_only', 'labels': 'no humans or LLMs',
    }
    replicates, summaries, population_rows, policy_rows = [], [], [], []
    for scenario in config['scenarios']:
        parameters = {k:v for k,v in scenario.items() if k != 'name'}
        pop = make_population(config['population_size'], config['population_seed'], **parameters)
        obs = pop.observed
        population_rows.append(dict(scenario=scenario['name'], target=pop.target,
            expected_target=float(obs.weights @ pop.outcome_probability),
            proxy_target=float(obs.weights @ obs.prediction), observable_sha256=obs.fingerprint(),
            outcome_sha256=hashlib.sha256(pop.outcome.tobytes()).hexdigest()))
        for budget_index, budget in enumerate(config['expected_budgets']):
            for method in config['methods']:
                if method == 'oracle_residual':
                    pi = oracle_policy(pop, budget, config['probability_floor_fraction'])
                    info = {'rho': ''}
                else:
                    pi, info = policy(obs, budget, method, config['probability_floor_fraction'],
                        config['mixture_uniform_weight'], config['robust_squared_error_radius'])
                for arm in [0,1]:
                    for group in [0,1]:
                        subset = (obs.arm == arm) & (obs.stratum == group)
                        policy_rows.append(dict(scenario=scenario['name'], budget=budget, method=method,
                            arm=arm, stratum=group, units=int(subset.sum()),
                            mean_inclusion_probability=float(pi[subset].mean()), rho=info.get('rho','')))
                # Common random numbers couple all policies and worlds at a given budget.
                rng = np.random.default_rng(config['audit_seed'] + budget_index * 104729)
                records = []
                for start in range(0, config['replicates'], 100):
                    size = min(100, config['replicates'] - start)
                    mask = rng.random((size, len(pi))) < pi
                    labels = np.where(mask, pop.outcome, np.nan)
                    batch = estimate_batch(obs, pi, labels, config['confidence_alpha'])
                    for j in range(size):
                        row = {k:float(v[j]) for k,v in batch.items()}
                        row.update(scenario=scenario['name'], budget=budget, method=method,
                                   replicate=start+j, target=pop.target)
                        records.append(row)
                replicates.extend(records)
                estimates = np.array([r['estimate'] for r in records])
                se = np.sqrt(np.array([r['variance_estimate'] for r in records]))
                cost = np.array([r['audit_count'] for r in records])
                correct = np.sign(estimates) == np.sign(pop.target)
                if pop.target == 0:
                    correct_rate = float('nan')
                else:
                    correct_rate = float(correct.mean())
                summary = dict(scenario=scenario['name'], budget=budget, method=method,
                    target=pop.target, proxy_target=float(obs.weights @ obs.prediction),
                    bias=float(estimates.mean()-pop.target),
                    bias_mcse=float(estimates.std(ddof=1)/np.sqrt(len(records))),
                    rmse=float(np.sqrt(np.mean((estimates-pop.target)**2))),
                    empirical_variance=float(estimates.var(ddof=1)),
                    exact_design_variance=exact_design_variance(pop, pi),
                    mean_estimated_variance=float(np.mean(se**2)),
                    correct_selection=correct_rate,
                    selection_mcse=binomial_mcse(correct_rate,len(records)),
                    mean_audits=float(cost.mean()), audit_sd=float(cost.std(ddof=1)),
                    audit_p05=float(np.quantile(cost,.05)),audit_p95=float(np.quantile(cost,.95)),
                    zero_variance_fraction=float(np.mean(se == 0)))
                for interval in ['wald','bernstein']:
                    low = np.array([r[interval+'_low'] for r in records])
                    high = np.array([r[interval+'_high'] for r in records])
                    coverage = float(np.mean((low <= pop.target) & (pop.target <= high)))
                    summary[interval+'_coverage'] = coverage
                    summary[interval+'_coverage_mcse'] = binomial_mcse(coverage,len(records))
                    summary[interval+'_width'] = float(np.mean(np.maximum(0, high-low)))
                    # A decisive interval must exclude zero; a wrong decisive interval
                    # is counted separately from a point-estimate selection mistake.
                    positive, negative = low > 0, high < 0
                    decisive = positive | negative
                    wrong = positive if pop.target < 0 else negative
                    summary[interval+'_decisive_rate'] = float(decisive.mean())
                    summary[interval+'_wrong_decisive_rate'] = float(wrong.mean())
                summaries.append(summary)
        print('Completed', scenario['name'], 'target=', round(pop.target,5), flush=True)
    write_csv(output/'replicates.csv', replicates)
    write_csv(output/'summary.csv', summaries)
    write_csv(output/'populations.csv', population_rows)
    write_csv(output/'policies.csv', policy_rows)
    provenance['outputs_sha256'] = {p.name:sha(p) for p in sorted(output.glob('*.csv'))}
    provenance['elapsed_seconds'] = time.time()-started
    (output/'manifest.json').write_text(json.dumps(provenance, indent=2)+'\n')
    print('Wrote', len(replicates), 'replicate records to', output, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=ROOT/'experiments/pilot-v1.json')
    parser.add_argument('--output', type=Path, default=ROOT/'results/pilot-v1')
    args = parser.parse_args()
    run(args.config.resolve(), args.output.resolve())
