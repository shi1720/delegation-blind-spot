import importlib.util
from pathlib import Path
import unittest
import numpy as np

path=Path(__file__).resolve().parents[1]/'experiments/v3/precision_sweep.py'
spec=importlib.util.spec_from_file_location('precision_sweep',path)
sweep=importlib.util.module_from_spec(spec); spec.loader.exec_module(sweep)


class PrecisionSweepTests(unittest.TestCase):
    def test_spectrum_and_analytic_width(self):
        d=np.array([.06,.02,-.04,-.02]); p=np.array([.65,.1,.15,.1])
        for eta in [0,.01,.03,.1,.3,1]:
            A=sweep.channel(eta)
            np.testing.assert_allclose(A.sum(axis=0),1)
            np.testing.assert_allclose(np.linalg.eigvalsh(A),[eta,eta,eta,1],atol=1e-12)
            result=sweep.structural(A,p,d,eta)
            self.assertAlmostEqual(result['width'],.1 if eta==0 else 0,places=7)
            self.assertLessEqual(result['lower'],d@p+1e-9)
            self.assertGreaterEqual(result['upper'],d@p-1e-9)

    def test_methods_retain_witnesses_and_expected_keys(self):
        r=sweep.one_replicate(sweep.channel(1),np.array([.65,.1,.15,.1]),
            np.array([.06,.02,-.04,-.02]),160,320,np.random.default_rng(821))
        self.assertEqual(set(r),{'field_only','calibration_only','joint'})
        for fit in r.values():
            self.assertTrue(fit['feasible'])
            self.assertLessEqual(fit['max_constraint_residual'],1e-7)
            self.assertGreaterEqual(fit['width'],-1e-9)

    def test_failed_intervals_stay_in_unconditional_denominator(self):
        records=[{'feasible':True,'covered':True,'resolved':True,'wrong_resolution':False,
                  'width':.04,'max_constraint_residual':0},
                 {'feasible':False,'covered':False,'resolved':False,'wrong_resolution':False,
                  'width':None,'max_constraint_residual':None}]
        s=sweep.summarize(records)
        self.assertEqual(s['replicates'],2); self.assertEqual(s['infeasible_count'],1)
        self.assertEqual(s['covered_rate'],.5); self.assertEqual(s['resolved_rate'],.5)
        self.assertEqual(s['width_feasible_n'],1); self.assertEqual(s['width_median'],.04)
        self.assertGreater(s['wrong_resolution_mc_ci_upper'],0)

    def test_incompatible_sample_is_retained_as_failed_interval(self):
        class ExtremeCounts:
            def multinomial(self,n,probabilities):
                return np.array([n,0,0,0])
        # This possible but extremely unlikely sample excludes q=(1/4,...)
        # from its field box. It must remain an explicit failed repetition.
        result=sweep.one_replicate(sweep.channel(0),np.ones(4)/4,
            np.array([.06,.02,-.04,-.02]),10,10,ExtremeCounts())
        self.assertFalse(result['field_only']['feasible'])
        self.assertFalse(result['field_only']['covered'])
        self.assertFalse(result['field_only']['resolved'])
        self.assertIsNone(result['field_only']['width'])
        self.assertTrue(result['field_only']['error'])

    def test_reproducible_independent_draws(self):
        args=(sweep.channel(.3),np.ones(4)/4,np.array([.06,.02,-.04,-.02]),40,80)
        a=sweep.one_replicate(*args,np.random.default_rng(121))
        b=sweep.one_replicate(*args,np.random.default_rng(121))
        self.assertEqual(a,b)


if __name__=='__main__': unittest.main()
