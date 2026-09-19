"""Design-based residual correction and clearly separated interval assumptions."""

import numpy as np
from scipy.stats import norm


def validate_design(observed, pi):
    pi = np.asarray(pi, dtype=float)
    if pi.shape != observed.arm.shape or not np.all(np.isfinite(pi)) or np.any((pi <= 0) | (pi > 1)):
        raise ValueError("Every inclusion probability must be in (0,1]")
    return pi


def estimate(observed, pi, audited_labels, alpha=0.05):
    """Missing labels MUST be NaN. The estimator never receives their values."""
    pi = validate_design(observed, pi)
    labels = np.asarray(audited_labels, dtype=float)
    if labels.shape != pi.shape or not 0 < alpha < 1:
        raise ValueError("Invalid label shape or alpha")
    seen = ~np.isnan(labels)
    if not np.all(np.isfinite(labels[seen])) or np.any((labels[seen] < 0) | (labels[seen] > 1)):
        raise ValueError("Observed labels must be in [0,1]")
    w = observed.weights
    r = labels[seen] - observed.prediction[seen]
    center = float(w @ observed.prediction + np.sum(w[seen] * r / pi[seen]))
    var_hat = float(np.sum(w[seen] ** 2 * r ** 2 * (1 - pi[seen]) / pi[seen] ** 2))
    wald_radius = norm.ppf(1 - alpha / 2) * np.sqrt(var_hat)
    radius = bernstein_radius(observed, pi, alpha)
    return {
        "estimate": center,
        "variance_estimate": var_hat,
        "wald_low": max(-1.0, center - wald_radius),
        "wald_high": min(1.0, center + wald_radius),
        "bernstein_low": max(-1.0, center - radius),
        "bernstein_high": min(1.0, center + radius),
        "audit_count": int(seen.sum()),
    }


def bernstein_radius(observed, pi, alpha=0.05):
    pi = validate_design(observed, pi)
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    # pi=1 contributes an identically zero random term.
    uncertain = pi < 1
    if not uncertain.any():
        return 0.0
    w = observed.weights
    a = np.maximum(observed.prediction, 1 - observed.prediction)
    variance_bound = np.sum(w ** 2 * a ** 2 * (1 - pi) / pi)
    bound = np.max(np.abs(w[uncertain]) * a[uncertain] / pi[uncertain])
    log_term = np.log(2.0 / alpha)
    return float(np.sqrt(2 * variance_bound * log_term) + (2 / 3) * bound * log_term)


def exact_design_variance(population, pi):
    pi = validate_design(population.observed, pi)
    r = population.outcome - population.observed.prediction
    return float(np.sum(population.observed.weights ** 2 * r ** 2 * (1 - pi) / pi))


def estimate_batch(observed, pi, audited_labels, alpha=0.05):
    """Vectorized replicates of estimate; missing entries remain NaN."""
    pi = validate_design(observed, pi)
    labels = np.asarray(audited_labels, dtype=float)
    if labels.ndim != 2 or labels.shape[1] != len(pi) or not 0 < alpha < 1:
        raise ValueError("Invalid batch shape or alpha")
    seen = ~np.isnan(labels)
    if not np.all(np.isfinite(labels[seen])) or np.any((labels[seen] < 0) | (labels[seen] > 1)):
        raise ValueError("Observed labels must be in [0,1]")
    r = np.where(seen, labels - observed.prediction, 0.0)
    center = observed.weights @ observed.prediction + np.sum(r * (observed.weights / pi), axis=1)
    var_hat = np.sum(r ** 2 * (observed.weights ** 2 * (1 - pi) / pi ** 2), axis=1)
    wald_radius = norm.ppf(1 - alpha / 2) * np.sqrt(var_hat)
    radius = bernstein_radius(observed, pi, alpha)
    return dict(estimate=center, variance_estimate=var_hat,
                wald_low=np.maximum(-1.0, center-wald_radius),
                wald_high=np.minimum(1.0, center+wald_radius),
                bernstein_low=np.maximum(-1.0, center-radius),
                bernstein_high=np.minimum(1.0, center+radius),
                audit_count=seen.sum(axis=1))
