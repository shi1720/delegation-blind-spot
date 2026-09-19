"""Independent numerical cross-checks of the appendix's mathematical claims.

These tests validate identities on constructed finite problems. They are not
empirical evidence about people or a proof by numerical experiment.
"""
import sys
from pathlib import Path
import unittest
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from delegation_blind_spot.identification import contrast_bounds


def worst_pair_width(a, d):
    """Primal: optimize directly over two indistinguishable simplex points."""
    k = len(d)
    equality = np.vstack([
        np.hstack([a, -a]),
        np.r_[np.ones(k), np.zeros(k)],
        np.r_[np.zeros(k), np.ones(k)],
    ])
    rhs = np.r_[np.zeros(a.shape[0]), 1., 1.]
    fit = linprog(np.r_[-d, d], A_eq=equality, b_eq=rhs,
                  bounds=(0., 1.), method='highs')
    if not fit.success:
        raise AssertionError(fit.message)
    return -fit.fun, fit.x[:k], fit.x[k:]


def rowspace_distance(a, d):
    """Dual geometry: minimum infinity distance without population variables."""
    m, k = a.shape
    inequalities = np.vstack([
        np.column_stack([-a.T, -np.ones(k)]),
        np.column_stack([a.T, -np.ones(k)]),
    ])
    fit = linprog(np.r_[np.zeros(m), 1.], A_ub=inequalities,
                  b_ub=np.r_[-d, d], bounds=[(None, None)]*m+[(0., None)],
                  method='highs')
    if not fit.success:
        raise AssertionError(fit.message)
    return fit.fun


class TheoryTests(unittest.TestCase):
    def test_global_width_equals_dual_distance_across_channels(self):
        rng = np.random.default_rng(19491)
        for m, k in [(1, 4), (2, 5), (3, 6), (5, 3)]:
            for _ in range(5):
                a = rng.dirichlet(np.ones(m), size=k).T
                d = rng.normal(size=k)
                width, p, r = worst_pair_width(a, d)
                dual = rowspace_distance(a, d)
                self.assertAlmostEqual(width, 2*dual, places=7)
                np.testing.assert_allclose(a @ p, a @ r, atol=1e-8)
                self.assertAlmostEqual(width, d @ (p-r), places=7)

    def test_rowspace_contrast_has_zero_global_ambiguity(self):
        a = np.array([[.8, .2, .6], [.2, .8, .4]])
        d = a.T @ np.array([-.4, .9])
        width, _, _ = worst_pair_width(a, d)
        self.assertAlmostEqual(width, 0., places=8)

    def test_local_boundary_identification_despite_global_ambiguity(self):
        a = np.array([[1., 0., 0.], [0., 1., 1.]])
        d = np.array([.2, -.3, .5])
        q = np.array([1., 0.])
        local = contrast_bounds(a, a, q, q, d)
        self.assertAlmostEqual(local.lower, .2)
        self.assertAlmostEqual(local.upper, .2)
        self.assertAlmostEqual(worst_pair_width(a, d)[0], .8)

    def test_coarsening_widens_local_and_global_ambiguity(self):
        a = np.array([[.8, .1, .2], [.1, .8, .2], [.1, .1, .6]])
        g = np.array([[1., 1., 0.], [0., 0., 1.]])
        b = g @ a
        p = np.array([.2, .4, .4]); d = np.array([-.3, .5, .2])
        q = a @ p
        fine = contrast_bounds(a, a, q, q, d)
        coarse = contrast_bounds(b, b, g @ q, g @ q, d)
        self.assertLessEqual(coarse.lower, fine.lower+1e-9)
        self.assertGreaterEqual(coarse.upper, fine.upper-1e-9)
        self.assertGreaterEqual(worst_pair_width(b,d)[0],
                                worst_pair_width(a,d)[0]-1e-9)

    def test_logged_probe_identity_prevents_cancellation(self):
        a1 = np.eye(2); a2 = a1[::-1]
        logged = np.vstack([.5*a1, .5*a2])
        unlogged = .5*(a1+a2)
        d = np.array([-.3, .5])
        self.assertAlmostEqual(worst_pair_width(logged,d)[0], 0.)
        self.assertAlmostEqual(worst_pair_width(unlogged,d)[0], .8)

    def test_randomized_regret_formula_solves_endpoint_game(self):
        for lower, upper in [(-.3,.5), (-1.,.01), (-.05, .9)]:
            # Independent two-variable LP minimizes worst endpoint regret.
            fit = linprog([0.,1.], A_ub=[[-lower,-1.],[-upper,-1.]],
                          b_ub=[0.,-upper], bounds=[(0.,1.),(0.,None)],
                          method='highs')
            self.assertTrue(fit.success)
            expected_t = upper/(upper-lower)
            expected_risk = -lower*upper/(upper-lower)
            self.assertAlmostEqual(fit.x[0], expected_t)
            self.assertAlmostEqual(fit.x[1], expected_risk)
            self.assertLessEqual(expected_risk, min(-lower,upper)+1e-10)

    def test_cost_allocation_bound_and_equality(self):
        sigma = np.array([.2,.8,1.1]); cost = np.array([1.,2.,5.])
        budget = 100.
        optimal = budget*(sigma/np.sqrt(cost))/np.sum(sigma*np.sqrt(cost))
        target = np.sum(sigma*np.sqrt(cost))**2/budget
        self.assertAlmostEqual(cost @ optimal, budget)
        self.assertAlmostEqual(np.sum(sigma**2/optimal), target)
        rng = np.random.default_rng(2319)
        for _ in range(100):
            allocation = budget*rng.dirichlet(np.ones(3))/cost
            self.assertGreaterEqual(np.sum(sigma**2/allocation), target-1e-10)

    def test_tv_drift_bias_inequality_for_random_channels(self):
        rng = np.random.default_rng(12191)
        for _ in range(30):
            a = rng.dirichlet(np.ones(4),size=3).T
            drifted = rng.dirichlet(np.ones(4),size=3).T
            v = rng.normal(size=4)
            tau = .5*np.max(np.sum(np.abs(a-drifted),axis=0))
            max_bias = np.max(np.abs(v @ (a-drifted)))
            self.assertLessEqual(max_bias, tau*np.ptp(v)+1e-12)


if __name__ == '__main__':
    unittest.main()
