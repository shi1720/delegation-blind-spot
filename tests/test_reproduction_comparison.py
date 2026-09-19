"""Protect cross-platform reproduction checks from hiding substantive changes."""
import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[1]/'scripts/reproduce_v3_results.py'
spec=importlib.util.spec_from_file_location('reproduction',path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
compare=module.compare_parser


class ReproductionComparisonTests(unittest.TestCase):
    def test_exact_mode_rejects_even_last_digit_differences(self):
        with self.assertRaisesRegex(ValueError,'numerical result'):
            compare({'width':0.02284660696519887},{'width':0.022846606965198867})

    def test_explicit_tolerance_reports_every_float_difference(self):
        delta=compare({'row':[0.02284660696519887,7,'positive',False]},
                      {'row':[0.022846606965198867,7,'positive',False]},1e-12)
        self.assertEqual(len(delta),1)
        self.assertGreater(delta[0],0)
        self.assertLess(delta[0],1e-16)

    def test_tolerance_never_relaxes_counts_decisions_or_types(self):
        for a,e in [(8,7),('negative','positive'),(True,False),(7.,7),(True,1)]:
            with self.subTest(actual=a,expected=e):
                with self.assertRaises(ValueError):compare({'result':a},{'result':e},1e-12)

    def test_schema_and_numerical_changes_fail(self):
        for a,e in [({'a':1},{'b':1}),([1],[1,2]),({'x':.2},{'x':.1})]:
            with self.subTest(actual=a,expected=e):
                with self.assertRaises(ValueError):compare(a,e,1e-12)

    def test_nonfinite_numbers_and_invalid_tolerances_fail(self):
        for value in [float('nan'),float('inf'),-float('inf')]:
            with self.assertRaises(ValueError):compare(value,value,1e-12)
        for tol in [-1.,float('inf'),float('nan')]:
            with self.assertRaises(ValueError):compare(1.,1.,tol)

    def test_identical_nested_record_has_no_differences(self):
        record={'counts':[1,2,3],'fields':{'low':-.04,'high':.06,'decision':'unresolved','wrong':False,'extra':None}}
        self.assertEqual(compare(record,record),[])


if __name__=='__main__':unittest.main()
