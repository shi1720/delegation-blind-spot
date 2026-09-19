from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from delegation_blind_spot.identification import contrast_bounds, probability_intervals, channel_intervals


class IdentificationTests(unittest.TestCase):
    def test_identity_recovers_known_contrast(self):
        A = np.eye(3); p = np.array([.2,.3,.5]); d = np.array([-1.,.2,.8])
        r = contrast_bounds(A,A,p,p,d)
        self.assertAlmostEqual(r.lower, d@p)
        self.assertAlmostEqual(r.upper, d@p)
        self.assertEqual(r.decision,'variant_1')

    def test_pooling_returns_opposing_worlds_with_same_logs(self):
        A = np.array([[1.,1.],[0.,0.]])
        q = np.array([1.,0.]); d = np.array([-1.,1.])
        r = contrast_bounds(A,A,q,q,d)
        self.assertAlmostEqual(r.lower,-1.)
        self.assertAlmostEqual(r.upper,1.)
        np.testing.assert_allclose(A@r.lower_population,A@r.upper_population)
        self.assertEqual(r.decision,'unresolved')

    def test_rank_deficiency_need_not_hide_every_contrast(self):
        A = np.array([[1.,1.,0.],[0.,0.,1.]])
        q = np.array([.4,.6]); d = np.array([-.2,-.2,.8])
        r=contrast_bounds(A,A,q,q,d)
        self.assertAlmostEqual(r.lower,.4)
        self.assertAlmostEqual(r.upper,.4)

    def test_more_uncertainty_cannot_narrow_interval(self):
        A = np.array([[.9,.2],[.1,.8]]); q=np.array([.62,.38]); d=np.array([-1.,1.])
        exact = contrast_bounds(A,A,q,q,d)
        relaxed=contrast_bounds(np.maximum(0,A-.1),np.minimum(1,A+.1),q,q,d)
        self.assertLessEqual(relaxed.lower,exact.lower+1e-9)
        self.assertGreaterEqual(relaxed.upper,exact.upper-1e-9)

    def test_zero_mass_column_has_valid_witness(self):
        A=np.eye(2); q=np.array([1.,0.])
        r=contrast_bounds(A,A,q,q,np.array([.2,-.4]))
        self.assertAlmostEqual(r.lower,.2)
        self.assertLess(r.max_constraint_residual,1e-9)

    def test_inconsistent_channel_and_logs_rejected(self):
        A=np.array([[1.,1.],[0.,0.]])
        with self.assertRaises(ValueError):
            contrast_bounds(A,A,[.2,.8],[.2,.8],[1.,-1.])

    def test_malformed_probabilities_rejected(self):
        for bad in [np.array([[1.2,.1],[0.,.9]]), np.ones((2,2)), np.full((2,2),np.nan)]:
            with self.assertRaises(ValueError):
                contrast_bounds(bad,bad,[.5,.5],[.5,.5],[1.,-1.])

    def test_full_uncertainty_is_simplex_range(self):
        r=contrast_bounds(np.zeros((3,4)),np.ones((3,4)),[.2,.3,.5],[.2,.3,.5],[-.4,.6,.1,-.2])
        self.assertAlmostEqual(r.lower,-.4)
        self.assertAlmostEqual(r.upper,.6)

    def test_recover_unknown_channel_from_joint_witness(self):
        lo=np.array([[.4,.2],[.1,.3]]); hi=np.array([[.9,.7],[.6,.8]])
        q=np.array([.6,.4]); d=np.array([-.3,.7])
        r=contrast_bounds(lo,hi,q,q,d)
        for p,J in [(r.lower_population,r.lower_joint),(r.upper_population,r.upper_joint)]:
            np.testing.assert_allclose(J.sum(axis=0),p,atol=1e-9)
            np.testing.assert_allclose(J.sum(axis=1),q,atol=1e-9)
            for k in range(len(p)):
                if p[k]>1e-9:
                    column=J[:,k]/p[k]
                    self.assertTrue(np.all(column >= lo[:,k]-1e-9))
                    self.assertTrue(np.all(column <= hi[:,k]+1e-9))

    def test_empty_calibration_is_uninformative(self):
        lo,hi=channel_intervals(np.zeros((3,2),dtype=int))
        np.testing.assert_equal(lo,np.zeros((3,2)))
        np.testing.assert_equal(hi,np.ones((3,2)))

    def test_binomial_interval_contains_endpoint_when_count_extreme(self):
        lo,hi=probability_intervals([0,100])
        self.assertEqual(lo[0],0.)
        self.assertEqual(hi[1],1.)
        self.assertLess(hi[0],.1)
        self.assertGreater(lo[1],.9)


if __name__=='__main__':
    unittest.main()
