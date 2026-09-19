import itertools
from pathlib import Path
import sys
import unittest
import numpy as np
from scipy.stats import binom
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from delegation_blind_spot.certificates import minimax_decision,worst_hidden_width,linear_certificate


class CertificateTests(unittest.TestCase):
    def test_minimax_equalizes_endpoint_regret(self):
        r=minimax_decision(-.3,.5)
        self.assertAlmostEqual(r.choose_variant_one_probability,.625)
        self.assertAlmostEqual(r.worst_case_regret,.1875)
        for t in np.linspace(0,1,101):
            self.assertGreaterEqual(max(.3*t,.5*(1-t))+1e-12,r.worst_case_regret)

    def test_exact_identification_and_complete_pooling_widths(self):
        self.assertAlmostEqual(worst_hidden_width(np.eye(3),[-.5,.2,.9]),0.)
        self.assertAlmostEqual(worst_hidden_width(np.ones((1,3)),[-.5,.2,.9]),1.4)

    def test_exhaustive_binomial_coverage_for_fixed_and_drifted_channels(self):
        A=np.array([[.9,.2],[.1,.8]]); d=np.array([-.2,.5]); n=40
        for drift in [0.,.1]:
            certificate=linear_certificate(A,d,n,alpha=.05,tv_drift=drift)
            for p in np.linspace(0,1,7):
                for offsets in itertools.product([-drift,drift],repeat=2):
                    aprime=A.copy(); aprime[0]+=offsets; aprime[1]-=offsets
                    if np.any(aprime<0) or np.any(aprime>1): continue
                    q=aprime@np.array([p,1-p]); target=d@np.array([p,1-p])
                    coverage=0.
                    for k in range(n+1):
                        lo,hi=certificate.interval([k,n-k])
                        if lo-1e-10<=target<=hi+1e-10: coverage+=binom.pmf(k,n,q[0])
                    self.assertGreaterEqual(coverage,.95-1e-10)

    def test_drift_cannot_improve_optimal_certificate_radius(self):
        A=np.array([[.7,.3],[.3,.7]]); d=[-.3,.5]
        radii=[linear_certificate(A,d,100,tv_drift=t).radius for t in [0,.05,.2,1]]
        self.assertTrue(np.all(np.diff(radii)>=-1e-9))

    def test_nearly_pooled_full_rank_is_not_exact_nonidentification(self):
        A=np.array([[.5+1e-8,.5-1e-8],[.5-1e-8,.5+1e-8]])
        self.assertLess(worst_hidden_width(A,[-.3,.5]),1e-7)
        # Identification can coexist with a practically uninformative finite-n certificate.
        self.assertGreater(linear_certificate(A,[-.3,.5],100).radius,.39)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): minimax_decision(1,-1)
        with self.assertRaises(ValueError): worst_hidden_width([[.2,.1]],[0,1])
        with self.assertRaises(ValueError): linear_certificate(np.eye(2),[0,1],0)
        with self.assertRaises(ValueError): linear_certificate(np.eye(2),[0,1],5).interval([2,2])


if __name__=='__main__': unittest.main()
