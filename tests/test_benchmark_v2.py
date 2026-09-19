import copy
import json
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments/v2'))
from benchmark import POPULATIONS, controls, digest, generate, request, utility
from analyze import action_index, analyze, response_index


class BenchmarkV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.outcomes,cls.truth=generate(calibration_per_class=8,field_size=12,
            outcome_audits=32,domains=['cloud'])
        cls.records=[r for r in controls(cls.rows) if r['system']=='optimal']

    def test_frozen_generation_and_independent_splits(self):
        again=generate(calibration_per_class=8,field_size=12,outcome_audits=32,domains=['cloud'])
        self.assertEqual(digest(self.rows),digest(again[0]))
        self.assertEqual(len(self.rows),32+3*12)
        self.assertEqual(len({r['task_id'] for r in self.rows}),len(self.rows))
        cal={json.dumps(r['private_features']) for r in self.rows if r['split']=='calibration'}
        field={json.dumps(r['private_features']) for r in self.rows if r['split']=='field'}
        self.assertFalse(cal & field)

    def test_no_constructed_universal_winner(self):
        chosen={r['semantic_choice'][r['optimal_choices'][0]] for r in self.rows}
        self.assertGreaterEqual(len(chosen),3)
        self.assertTrue(all(0<=v<=1 for r in self.rows for v in r['option_utilities'].values()))

    def test_schema_and_position_remapping(self):
        r=self.rows[0]
        body=request(r,'test-model')
        self.assertEqual(body['text']['format']['schema']['properties']['choice_id']['enum'],['A','B','C','D'])
        self.assertEqual(set(r['semantic_choice']),set('ABCD'))
        self.assertFalse('private_intent' in json.dumps(body))

    def test_threshold_penalty_is_scored(self):
        self.assertLess(utility(np.array([[.34,.5,.5,.5]]),0)[0],
                        utility(np.array([[.35,.5,.5,.5]]),0)[0]-.2)

    def test_missing_and_duplicate_responses_rejected(self):
        ids={r['task_id'] for r in self.rows}
        with self.assertRaises(ValueError): response_index(self.records[:-1],ids)
        with self.assertRaises(ValueError): response_index(self.records+[self.records[0]],ids)

    def test_failures_remain_observed(self):
        t=self.rows[0]
        self.assertEqual(action_index(t,{'error':'refused'}),4)
        self.assertEqual(action_index(t,{'choice_id':'BAD'}),4)
        self.assertEqual(action_index(t,{'error':'timeout'},True),5*t['regime']+4)

    def test_cohort_separation_bounds_and_failure_denominator(self):
        results=analyze(self.rows,self.records,self.outcomes,self.truth,bootstrap_replicates=4)
        self.assertEqual(len(results),6)
        self.assertEqual({r['cohort'] for r in results},set(POPULATIONS))
        for r in results:
            self.assertEqual(r['calibration_n'],32)
            self.assertEqual(r['field_n'],12)
            self.assertEqual(r['optimal_choice_rate'],1.)
            self.assertGreaterEqual(r['upper'],r['lower'])
            self.assertLess(r['max_solver_constraint_violation'],1e-7)
            self.assertEqual(sum(r['field_counts']),12)
        failed=copy.deepcopy(self.records)
        field_id=next(r['task_id'] for r in self.rows if r['split']=='field')
        for r in failed:
            if r['task_id']==field_id: r['error']='timeout'
        reports=analyze(self.rows,failed,self.outcomes,self.truth,bootstrap_replicates=4)
        self.assertEqual(sum(r['failure_rate']>0 for r in reports),2)

    def test_field_private_intent_cannot_change_inference(self):
        altered=copy.deepcopy(self.rows)
        for r in altered:
            if r['split']=='field': r['private_intent']=(r['private_intent']+1)%4
        original=analyze(self.rows,self.records,self.outcomes,self.truth,bootstrap_replicates=4)
        changed=analyze(altered,self.records,self.outcomes,self.truth,bootstrap_replicates=4)
        self.assertEqual(original,changed)

    def test_known_target_has_both_decision_signs(self):
        cohorts=self.truth['cloud']['cohorts']
        self.assertGreater(cohorts['positive']['target_contrast'],0.)
        self.assertLess(cohorts['negative']['target_contrast'],0.)


if __name__=='__main__': unittest.main()
