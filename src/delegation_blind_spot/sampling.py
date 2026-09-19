"""Existing sampling constructions, with explicit expected-budget constraints."""

import numpy as np
from scipy.optimize import minimize_scalar


def allocate(scores, budget, floor_fraction=0.05):
    scores = np.asarray(scores, dtype=float)
    n = len(scores)
    if scores.ndim != 1 or n == 0 or not np.all(np.isfinite(scores)) or np.any(scores < 0):
        raise ValueError("scores must be a finite, nonnegative vector")
    if not 0 < budget <= n or not 0 < floor_fraction <= 1:
        raise ValueError("Invalid budget or floor")
    if budget == n:
        return np.ones(n)
    rate = budget / n
    floor = rate * floor_fraction
    if not np.any(scores) or floor_fraction == 1:
        return np.full(n, rate)
    # A strictly positive score for zero-score units avoids a deficient budget
    # when all positive-score units saturate at pi=1.
    score = np.maximum(scores, np.max(scores) * 1e-12)
    lo, hi = 0.0, 1.0
    while np.clip(hi * score, floor, 1.0).sum() < budget:
        hi *= 2
    for _ in range(100):
        mid = (lo + hi) / 2
        if np.clip(mid * score, floor, 1.0).sum() < budget:
            lo = mid
        else:
            hi = mid
    result = np.clip((lo + hi) / 2 * score, floor, 1.0)
    if abs(result.sum() - budget) > 1e-7:
        raise ArithmeticError("Expected audit budget not met")
    return result


def policy(observed, budget, name, floor_fraction=0.05,
           uniform_weight=0.5, error_radius=0.15):
    n = len(observed.arm)
    if not 0 <= uniform_weight <= 1 or not 0 <= error_radius <= 1:
        raise ValueError("Invalid robustness parameter")
    uniform = np.full(n, budget / n)
    # Contrast influence weights are included even when arms are balanced.
    active = allocate(np.abs(observed.weights) * np.sqrt(observed.historical_mse),
                      budget, floor_fraction)
    if name == "uniform":
        return uniform, {"rho": 1.0}
    if name == "historical_active":
        return active, {"rho": 0.0}
    if name == "fixed_mixture":
        return (1 - uniform_weight) * active + uniform_weight * uniform, {"rho": uniform_weight}
    if name != "robust_path":
        raise ValueError("Unknown implementable policy: " + name)
    # Li et al. Eq. 4, with a declared per-unit box uncertainty set.
    # Maximize over 0 <= true MSE <= min(estimated MSE + radius, max residual^2).
    # Coefficients 1/pi are positive, so the inner supremum is the upper corner.
    max_sq_residual = np.maximum(observed.prediction, 1 - observed.prediction) ** 2
    upper = np.minimum(observed.historical_mse + error_radius, max_sq_residual)
    coefficient = observed.weights ** 2 * upper

    def objective(rho):
        return np.sum(coefficient / ((1 - rho) * active + rho * uniform))

    fitted = minimize_scalar(objective, bounds=(0, 1), method="bounded",
                             options={"xatol": 1e-10})
    rho = min([0.0, 1.0, float(fitted.x)], key=objective)
    return (1 - rho) * active + rho * uniform, {"rho": rho, "error_radius": error_radius}


def oracle_policy(population, budget, floor_fraction=0.05):
    """Privileged reference. Main outcomes are intentionally used only here."""
    score = np.abs(population.observed.weights *
                   (population.outcome - population.observed.prediction))
    return allocate(score, budget, floor_fraction)
