import itertools
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from delegation_blind_spot.model import Observables, Population, make_population
from delegation_blind_spot.sampling import allocate, policy
from delegation_blind_spot.estimation import estimate, estimate_batch, exact_design_variance


def tiny_population():
    obs = Observables(np.array([0, 0, 1, 1]), np.zeros(4, dtype=int),
                      np.array([0.1, 0.8, 0.4, 0.9]), np.array([.1, .2, .3, .4]))
    return Population(obs, np.array([1., 0., 1., 1.]), np.array([.5] * 4))


class EstimationTests(unittest.TestCase):
    def test_all_audit_subsets_exact_expectation_and_variance(self):
        pop = tiny_population()
        pi = np.array([.2, .4, .7, .9])
        centers, variances, probability = [], [], []
        for bits in itertools.product([False, True], repeat=4):
            mask = np.array(bits)
            result = estimate(pop.observed, pi, np.where(mask, pop.outcome, np.nan))
            probability.append(np.prod(np.where(mask, pi, 1-pi)))
            centers.append(result["estimate"])
            variances.append(result["variance_estimate"])
        probability = np.array(probability)
        centers = np.array(centers)
        self.assertAlmostEqual(probability.sum(), 1.0)
        self.assertAlmostEqual(probability @ centers, pop.target, places=12)
        enumerated_var = probability @ (centers-pop.target) ** 2
        self.assertAlmostEqual(enumerated_var, exact_design_variance(pop, pi), places=12)
        self.assertAlmostEqual(probability @ variances, enumerated_var, places=12)

    def test_all_labels_yield_exact_target_and_zero_width(self):
        pop = tiny_population()
        result = estimate(pop.observed, np.ones(4), pop.outcome)
        self.assertAlmostEqual(result["estimate"], pop.target)
        self.assertEqual(result["variance_estimate"], 0.0)
        self.assertEqual(result["bernstein_low"], result["bernstein_high"])

    def test_no_audits_is_not_a_claim_of_known_truth(self):
        pop = tiny_population()
        result = estimate(pop.observed, np.full(4, .1), np.full(4, np.nan))
        self.assertEqual(result["audit_count"], 0)
        self.assertEqual(result["variance_estimate"], 0)
        self.assertEqual(result["bernstein_low"], -1)
        self.assertEqual(result["bernstein_high"], 1)

    def test_batch_agrees_with_scalar(self):
        pop = tiny_population()
        pi = np.array([.2, .5, .7, 1.])
        labels = np.array([[1., np.nan, 1., 1.], [np.nan, 0., np.nan, 1.]])
        batch = estimate_batch(pop.observed, pi, labels)
        for i in range(2):
            scalar = estimate(pop.observed, pi, labels[i])
            for key in scalar:
                self.assertAlmostEqual(batch[key][i], scalar[key], places=12)

    def test_invalid_propensities_rejected(self):
        pop = tiny_population()
        for pi in [[0, .2, .2, .2], [1.1]*4, [np.nan]*4, [.2]*3]:
            with self.assertRaises(ValueError):
                estimate(pop.observed, pi, pop.outcome)

    def test_invalid_labels_rejected(self):
        pop = tiny_population()
        for bad in [[-1]*4, [1.1]*4, [np.inf]*4]:
            with self.assertRaises(ValueError):
                estimate(pop.observed, np.ones(4), bad)

    def test_bernstein_coverage_by_exhaustive_design(self):
        pop = tiny_population()
        for pi in [np.full(4, .95), np.array([.2, .5, .7, .9])]:
            coverage = 0.
            for bits in itertools.product([False, True], repeat=4):
                mask = np.array(bits)
                result = estimate(pop.observed, pi, np.where(mask, pop.outcome, np.nan), alpha=.1)
                if result["bernstein_low"] <= pop.target <= result["bernstein_high"]:
                    coverage += np.prod(np.where(mask, pi, 1-pi))
            self.assertGreaterEqual(coverage + 1e-12, .9)


class DesignTests(unittest.TestCase):
    def test_budget_saturation_and_zeros(self):
        for scores in [np.zeros(4), np.array([0., 0., 0., 1.]), np.array([1., 2., 3., 4.])]:
            for budget in [.1, 1., 3.8, 4.]:
                p = allocate(scores, budget)
                self.assertAlmostEqual(p.sum(), budget, places=9)
                self.assertTrue(np.all((p > 0) & (p <= 1)))

    def test_cauchy_schwarz_optimum_without_clipping(self):
        a = np.array([1., 4., 9., 16.])
        p = allocate(np.sqrt(a), .5)
        optimum = np.sqrt(a).sum() ** 2 / .5
        self.assertAlmostEqual(np.sum(a/p), optimum, places=9)

    def test_policies_use_only_identical_observables(self):
        world0 = make_population(4000, 7)
        world1 = make_population(4000, 7, shift=.12)
        self.assertEqual(world0.observed.fingerprint(), world1.observed.fingerprint())
        self.assertNotEqual(world0.target, world1.target)
        for name in ['uniform', 'historical_active', 'fixed_mixture', 'robust_path']:
            p0, _ = policy(world0.observed, 100, name)
            p1, _ = policy(world1.observed, 100, name)
            np.testing.assert_array_equal(p0, p1)

    def test_visible_control_changes_observables(self):
        pop = make_population(4000, 7)
        control = make_population(4000, 7, shift=.12, update_prediction=True)
        self.assertNotEqual(pop.observed.fingerprint(), control.observed.fingerprint())

    def test_robust_path_objective_beats_endpoints(self):
        obs = make_population(4000, 7).observed
        p, info = policy(obs, 100, 'robust_path')
        active, _ = policy(obs, 100, 'historical_active')
        uniform, _ = policy(obs, 100, 'uniform')
        upper = np.minimum(obs.historical_mse+.15, np.maximum(obs.prediction, 1-obs.prediction)**2)
        obj = lambda probs: np.sum(obs.weights**2 * upper / probs)
        self.assertLessEqual(obj(p), min(obj(active), obj(uniform)) + 1e-12)
        self.assertTrue(0 <= info['rho'] <= 1)
        self.assertAlmostEqual(p.sum(), 100, places=8)

    def test_parameters_rejected(self):
        for scores, budget in [([-1., 2.], 1), ([np.nan, 1.], 1), ([1, 2], 0), ([1,2], 3)]:
            with self.assertRaises(ValueError):
                allocate(scores, budget)


if __name__ == '__main__':
    unittest.main()
