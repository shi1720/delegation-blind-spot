"""Finite latent-class diagnostic via standard partial-identification LPs.

This module is a research instrument, not a claimed new optimization method.
Channel intervals must apply to the deployed population and agent configuration.
"""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog
from scipy.stats import beta


@dataclass(frozen=True)
class IdentificationResult:
    lower: float
    upper: float
    lower_population: np.ndarray
    upper_population: np.ndarray
    lower_joint: np.ndarray
    upper_joint: np.ndarray
    max_constraint_residual: float

    @property
    def decision(self):
        if self.lower > 1e-8:
            return 'variant_1'
        if self.upper < -1e-8:
            return 'variant_0'
        return 'unresolved'


def probability_intervals(counts, alpha=0.05):
    """Bonferroni Clopper-Pearson intervals for a multinomial count vector.

Coverage pertains to fixed multinomial sampling. The returned coordinate box
is conservative and may contain points outside the probability simplex.
"""
    counts = np.asarray(counts)
    if counts.ndim != 1 or not np.all(np.isfinite(counts)) or np.any(counts < 0) or np.any(counts != np.floor(counts)):
        raise ValueError('Counts must be a nonnegative integer vector')
    if len(counts) == 0 or not 0 < alpha < 1:
        raise ValueError('Invalid alpha or empty counts')
    total = int(counts.sum())
    if total == 0:
        return np.zeros(len(counts)), np.ones(len(counts))
    tail = alpha / (2 * len(counts))
    lower = np.zeros(len(counts))
    upper = np.ones(len(counts))
    positive = counts > 0
    below = counts < total
    lower[positive] = beta.ppf(tail, counts[positive], total-counts[positive]+1)
    upper[below] = beta.ppf(1-tail, counts[below]+1, total-counts[below])
    return lower, upper


def channel_intervals(counts, alpha=0.05):
    """Columns are intent classes, rows are observable action categories."""
    counts = np.asarray(counts)
    if counts.ndim != 2 or counts.shape[1] == 0:
        raise ValueError('Channel counts must be an actions-by-classes matrix')
    pairs = [probability_intervals(counts[:, k], alpha/counts.shape[1])
             for k in range(counts.shape[1])]
    return np.column_stack([p[0] for p in pairs]), np.column_stack([p[1] for p in pairs])


def contrast_bounds(channel_lower, channel_upper, frequency_lower,
                    frequency_upper, contrast):
    """Sharp bounds RELATIVE TO the supplied rectangular uncertainty model.

Let p[k] be latent class mass and J[a,k] the joint action/class mass.
L[a,k] p[k] <= J[a,k] <= U[a,k] p[k] linearizes the channel constraints.
No hidden ground-truth population is supplied to this computation.
"""
    lo = np.asarray(channel_lower, dtype=float)
    hi = np.asarray(channel_upper, dtype=float)
    qlo = np.asarray(frequency_lower, dtype=float)
    qhi = np.asarray(frequency_upper, dtype=float)
    d = np.asarray(contrast, dtype=float)
    if lo.ndim != 2 or lo.shape != hi.shape or 0 in lo.shape:
        raise ValueError('Channel bounds must be nonempty equal-shaped matrices')
    actions, classes = lo.shape
    if qlo.shape != (actions,) or qhi.shape != qlo.shape or d.shape != (classes,):
        raise ValueError('Incompatible frequency or contrast dimensions')
    arrays = [lo, hi, qlo, qhi, d]
    if not all(np.all(np.isfinite(a)) for a in arrays):
        raise ValueError('All inputs must be finite')
    if np.any(lo < 0) or np.any(hi > 1) or np.any(lo > hi):
        raise ValueError('Invalid channel probability bounds')
    if np.any(qlo < 0) or np.any(qhi > 1) or np.any(qlo > qhi):
        raise ValueError('Invalid action-frequency bounds')
    if np.any(lo.sum(axis=0) > 1+1e-10) or np.any(hi.sum(axis=0) < 1-1e-10):
        raise ValueError('Channel columns cannot sum to one within these bounds')
    # Decision variables: p[0:K], then row-major J[0:A,0:K].
    size = classes + actions * classes
    equality = []
    rhs = []
    row = np.zeros(size); row[:classes] = 1
    equality.append(row); rhs.append(1.)
    for k in range(classes):
        row = np.zeros(size); row[k] = -1
        row[classes+k::classes] = 1
        equality.append(row); rhs.append(0.)
    inequalities, limits = [], []
    for a in range(actions):
        total = np.zeros(size)
        total[classes+a*classes:classes+(a+1)*classes] = 1
        inequalities.extend([total, -total]); limits.extend([qhi[a], -qlo[a]])
        for k in range(classes):
            j = classes + a*classes + k
            upper = np.zeros(size); upper[j] = 1; upper[k] = -hi[a,k]
            lower = np.zeros(size); lower[j] = -1; lower[k] = lo[a,k]
            inequalities.extend([upper, lower]); limits.extend([0., 0.])
    Aeq, beq = np.array(equality), np.array(rhs)
    Aub, bub = np.array(inequalities), np.array(limits)
    objective = np.zeros(size); objective[:classes] = d
    solutions = []
    residual = 0.
    for sign in [1., -1.]:
        fit = linprog(sign*objective, A_ub=Aub, b_ub=bub,
                      A_eq=Aeq, b_eq=beq, bounds=(0.,1.), method='highs')
        if not fit.success:
            raise ValueError('No valid bound: ' + fit.message)
        # Verify solver feasibility independently of its status flag.
        violation = max(float(np.max(np.abs(Aeq @ fit.x - beq))),
                        float(np.max(Aub @ fit.x - bub)),
                        float(np.max(-fit.x)), float(np.max(fit.x-1.)), 0.)
        residual = max(residual, violation)
        if violation > 1e-7:
            raise ArithmeticError('Solver witness fails the constraints')
        solutions.append(fit.x)
    lower, upper = solutions
    return IdentificationResult(float(objective @ lower), float(objective @ upper),
        lower[:classes], upper[:classes], lower[classes:].reshape(actions,classes),
        upper[classes:].reshape(actions,classes), residual)
