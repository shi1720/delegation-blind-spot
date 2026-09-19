import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments/v2'))
from benchmark import generate
from prepare_receipts import receipt_request,receipt_task,selected_subset
from analyze_receipts import receipt_operational_scope


class ReceiptExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,_,_=generate(calibration_per_class=8,field_size=12,outcome_audits=8,domains=['cloud'])

    def test_fixed_stratified_selection_does_not_depend_on_outcomes(self):
        chosen=selected_subset(self.rows,4,6)
        self.assertEqual(len(chosen),4*4+3*6)
        altered=copy.deepcopy(self.rows)
        for row in altered:
            row['option_utilities']={'A':-999,'B':999,'C':0,'D':0}
            row['optimal_choices']=['B']
            if row['split']=='field': row['private_intent']=999
        again=selected_subset(altered,4,6)
        self.assertEqual([r['task_id'] for r in chosen],[r['task_id'] for r in again])
        self.assertEqual({r['task_id'] for r in chosen if r['split']=='calibration' and r['private_intent']==0},
                         {f'cloud-calibration-{i:06d}' for i in range(4)})

    def test_receipt_only_reports_supplied_preference(self):
        for source in self.rows:
            row=receipt_task(source)
            self.assertEqual(row['optimal_choices'],[chr(65+source['private_intent'])])
            request=receipt_request(row,'test-model')
            self.assertEqual(request['reasoning']['effort'],'none')
            sent=json.dumps(request)
            for forbidden in ['private_intent','option_utilities','class_contrasts','target_contrast','private_features','product_type']:
                self.assertNotIn(forbidden,sent)
            self.assertNotIn('options',json.loads(row['prompt']))

    def test_oversize_subset_fails(self):
        with self.assertRaises(ValueError): selected_subset(self.rows,9,6)

    def test_receipt_analysis_cannot_report_product_regret(self):
        reports=[{'optimal_choice_rate':.97,'mean_synthetic_utility':0.,'mean_synthetic_regret':0.,
                  'log_schema':'action_only','failure_rate':.03}]
        row=receipt_operational_scope(reports)[0]
        self.assertEqual(row['receipt_attribute_accuracy'],.97)
        self.assertEqual(row['log_schema'],'receipt_attribute')
        for forbidden in ['optimal_choice_rate','mean_synthetic_utility','mean_synthetic_regret']:
            self.assertNotIn(forbidden,row)


if __name__=='__main__': unittest.main()
