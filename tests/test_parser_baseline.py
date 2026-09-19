import copy
import json
from pathlib import Path
import sys
import unittest
import numpy as np
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/v3'))
from parser_baseline import WEIGHTS,analyze,extract_supplied_class,infer_from_counts


def prompt(k):
    return json.dumps({'customer_supplied_preferences':[{'attribute_id':chr(65+i),'weight':float(w)}
        for i,w in enumerate(WEIGHTS[k])]})


class ParserBaselineTests(unittest.TestCase):
    def test_identity_on_the_declared_public_profile_taxonomy(self):
        for k in range(4):self.assertEqual(extract_supplied_class(prompt(k)),k)

    def test_rejects_ambiguous_or_unknown_profiles(self):
        for weights in [[.25]*4,[.5,.2,.2,.1]]:
            with self.assertRaises(ValueError):
                extract_supplied_class({'customer_supplied_preferences':[{'attribute_id':chr(65+i),'weight':w} for i,w in enumerate(weights)]})

    def test_inference_does_not_use_private_intent_or_future_optimal_label(self):
        rows=[{'task_id':str(i),'split':'field','domain':'cloud','cohort':'mixed',
               'prompt':prompt(i%4),'private_intent':999,'optimal_choices':['D']} for i in range(20)]
        outcomes={'cloud':{'known_class_contrasts':[.1,.02,-.1,0.]}}
        a=analyze(rows,outcomes)
        altered=copy.deepcopy(rows)
        for row in altered: row.pop('private_intent');row['optimal_choices']=['A']
        self.assertEqual(a,analyze(altered,outcomes))
        self.assertEqual(a[0]['class_counts'],[5,5,5,5])

    def test_constant_contrast_is_known_without_sampling_error(self):
        r=infer_from_counts([3,4,5,6],[.1]*4)
        for key in ['known_identity_channel_with_multinomial_CP','direct_bounded_contrast_Hoeffding']:
            self.assertAlmostEqual(r[key]['lower'],.1)
            self.assertAlmostEqual(r[key]['upper'],.1)

    def test_direct_mean_bound_exhaustive_binomial_check(self):
        n=12;prob=.4;d=[-.05,.05,0.,0.];target=-.05+.1*prob
        coverage=0.
        for successes in range(n+1):
            r=infer_from_counts([n-successes,successes,0,0],d)['direct_bounded_contrast_Hoeffding']
            if r['lower']<=target<=r['upper']:coverage+=binom.pmf(successes,n,prob)
        self.assertGreaterEqual(coverage,.96-1e-12)

    def test_methods_report_separate_error_budgets(self):
        r=infer_from_counts([60,10,5,5],[.05,.002,-.037,.003])
        self.assertEqual(r['known_identity_channel_with_multinomial_CP']['alpha'],.04)
        self.assertEqual(r['direct_bounded_contrast_Hoeffding']['alpha'],.04)
        self.assertNotIn('intersection',r)


if __name__=='__main__':unittest.main()
