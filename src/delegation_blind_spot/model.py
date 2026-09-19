"""Synthetic finite-pool data. Policies receive Observables, never Population."""

from dataclasses import dataclass
import hashlib
import numpy as np


@dataclass(frozen=True)
class Observables:
    arm: np.ndarray
    stratum: np.ndarray
    prediction: np.ndarray
    historical_mse: np.ndarray

    def __post_init__(self):
        n = len(self.arm)
        arrays = (self.arm, self.stratum, self.prediction, self.historical_mse)
        if any(x.ndim != 1 or len(x) != n for x in arrays):
            raise ValueError("Observable arrays must have equal one-dimensional shapes")
        if not np.all(np.isin(self.arm, [0, 1])) or len(np.unique(self.arm)) != 2:
            raise ValueError("Both binary arms must be represented")
        if not np.all(np.isfinite(self.prediction)) or np.any((self.prediction < 0) | (self.prediction > 1)):
            raise ValueError("Predictions must be finite and in [0,1]")
        if not np.all(np.isfinite(self.historical_mse)) or np.any(self.historical_mse < 0):
            raise ValueError("Historical MSE must be finite and nonnegative")
        for x in arrays:
            x.setflags(write=False)

    @property
    def weights(self):
        return np.where(self.arm == 1, 1.0 / (self.arm == 1).sum(),
                        -1.0 / (self.arm == 0).sum())

    def fingerprint(self):
        h = hashlib.sha256()
        for x in (self.arm, self.stratum, self.prediction, self.historical_mse):
            h.update(str(x.dtype).encode())
            h.update(x.tobytes())
        return h.hexdigest()


@dataclass(frozen=True)
class Population:
    observed: Observables
    outcome: np.ndarray
    outcome_probability: np.ndarray

    @property
    def target(self):
        return float(self.observed.weights @ self.outcome)


def make_population(n, seed, shift=0.0, target_stratum=0, update_prediction=False):
    if n < 20 or n % 20:
        raise ValueError("n must be a positive multiple of 20")
    if not 0 <= shift <= 0.4 or target_stratum not in (0, 1):
        raise ValueError("Invalid synthetic shift")
    rng = np.random.default_rng(seed)
    # Exact balance within each arm removes random composition differences.
    arm = np.repeat([0, 1], n // 2)
    stratum = np.tile(np.repeat([0, 1], [9 * n // 20, n // 20]), 2)
    prediction = np.where(stratum == 0, np.where(arm == 0, 0.990, 0.995),
                          np.where(arm == 0, 0.40, 0.46))
    probability = prediction.copy()
    probability[(arm == 1) & (stratum == target_stratum)] -= shift
    # Same uniforms across worlds establish a paired, explicit construction.
    outcome = (rng.random(n) < probability).astype(float)
    if update_prediction:
        prediction = probability.copy()
    historical_mse = prediction * (1.0 - prediction)
    observed = Observables(arm, stratum, prediction, historical_mse)
    outcome.setflags(write=False)
    probability.setflags(write=False)
    return Population(observed, outcome, probability)
