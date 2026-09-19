"""Decision loss and bias-aware linear certificates from established theory.

These routines operationalize the proofs in docs/theory-review.md. They do
not introduce a new general inference or optimal-recovery method.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class DecisionRisk:
    choose_variant_one_probability: float
    worst_case_regret: float
    deterministic_worst_case_regret: float


def minimax_decision(lower, upper):
    """Exact-q minimax randomized decision for an attainable contrast interval."""
    if not np.isfinite(lower) or not np.isfinite(upper) or lower > upper:
        raise ValueError('Expected finite ordered bounds')
    if lower >= 0:
        return DecisionRisk(1., 0., 0.)
    if upper <= 0:
        return DecisionRisk(0., 0., 0.)
    probability=upper/(upper-lower)
    return DecisionRisk(probability, -lower*upper/(upper-lower), min(-lower,upper))


def validate_channel(channel, contrast):
    A=np.asarray(channel,dtype=float); d=np.asarray(contrast,dtype=float)
    if A.ndim!=2 or 0 in A.shape or d.shape!=(A.shape[1],):
        raise ValueError('Incompatible channel and contrast')
    if not np.all(np.isfinite(A)) or not np.all(np.isfinite(d)) or np.any(A<0):
        raise ValueError('Invalid numeric inputs')
    if not np.allclose(A.sum(axis=0),1.,rtol=0,atol=1e-10):
        raise ValueError('Channel columns must sum to one')
    return A,d


def _weights(A,d,range_penalty):
    m,K=A.shape
    # Variables v[m], approximation error epsilon, minimum v, maximum v.
    size=m+3; rows=[]; rhs=[]
    for k in range(K):
        row=np.zeros(size); row[:m]=-A[:,k]; row[m]=-1
        rows.append(row); rhs.append(-d[k])
        row=np.zeros(size); row[:m]=A[:,k]; row[m]=-1
        rows.append(row); rhs.append(d[k])
    for a in range(m):
        row=np.zeros(size); row[a]=1; row[m+2]=-1
        rows.append(row); rhs.append(0.)
        row=np.zeros(size); row[a]=-1; row[m+1]=1
        rows.append(row); rhs.append(0.)
    objective=np.zeros(size); objective[m]=1
    objective[m+1]=-range_penalty; objective[m+2]=range_penalty
    fit=linprog(objective,A_ub=np.array(rows),b_ub=np.array(rhs),
        bounds=[(None,None)]*m+[(0,None),(None,None),(None,None)],method='highs')
    if not fit.success: raise ArithmeticError('Certificate optimization failed')
    if np.max(np.array(rows)@fit.x-np.array(rhs))>1e-7:
        raise ArithmeticError('Certificate witness violates constraints')
    v=fit.x[:m]
    return v,float(np.max(np.abs(d-A.T@v)))


def worst_hidden_width(channel,contrast):
    """Structural width for a numerically resolved row space of a known channel.

    SVD uses the standard eps * max(shape) * largest singular value threshold.
    Below that numerical threshold, structural rank is not resolved. This
    quantity does not account for calibration error or finite-sample stability.
    """
    A,d=validate_channel(channel,contrast)
    _,singular,right=np.linalg.svd(A,full_matrices=False)
    tolerance=np.finfo(float).eps*max(A.shape)*singular[0]
    basis=right[singular>tolerance]
    # LP feasibility tolerances must not mistake nearly identical columns for
    # exact pooling. The orthonormal basis preserves the resolved row space.
    _,epsilon=_weights(basis,d,0.)
    return 2*epsilon


@dataclass(frozen=True)
class LinearCertificate:
    weights: np.ndarray
    approximation_bias: float
    sampling_radius: float
    drift_radius: float
    sample_size: int
    alpha: float

    @property
    def radius(self):
        return self.approximation_bias+self.sampling_radius+self.drift_radius

    def interval(self, counts):
        counts=np.asarray(counts)
        if counts.shape!=self.weights.shape or np.any(~np.isfinite(counts)) or np.any(counts<0) or np.any(counts!=np.floor(counts)) or counts.sum()!=self.sample_size:
            raise ValueError('Counts must match the declared sample size and action space')
        estimate=float(self.weights@counts/self.sample_size)
        return estimate-self.radius, estimate+self.radius


def linear_certificate(channel,contrast,sample_size,alpha=.05,tv_drift=0.):
    """Choose weights BEFORE field data, using a known or externally bounded channel.

    Field observations must be iid. tv_drift bounds each class-column total
    variation distance to the deployed channel. An estimated channel is not
    automatically known; calibration error must be included in tv_drift or
    handled with the joint-mass confidence-set diagnostic instead.
    """
    A,d=validate_channel(channel,contrast)
    if not isinstance(sample_size,(int,np.integer)) or sample_size<1 or not 0<alpha<1 or not 0<=tv_drift<=1:
        raise ValueError('Invalid sample, confidence, or drift setting')
    noise=np.sqrt(np.log(2/alpha)/(2*sample_size))
    v,epsilon=_weights(A,d,noise+tv_drift)
    span=float(np.ptp(v)); v.setflags(write=False)
    return LinearCertificate(v,epsilon,span*noise,span*tv_drift,int(sample_size),alpha)
