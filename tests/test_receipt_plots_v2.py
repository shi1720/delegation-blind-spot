import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments/v2'))
from plot_receipts import comparison_summary,paired_reports,receipt_figure


def fixture():
    actions=[];receipts=[]
    for domain in ['travel','cloud','workflow']:
        for cohort in ['positive','negative','near']:
            target={'positive':.03,'negative':-.02,'near':.005}[cohort]
            base={'domain':domain,'cohort':cohort,'calibration_n':160,'field_n':80,
                  'evaluation_only':{'true_contrast':target,'certified_wrong_decision':False},
                  'failure_rate':0.}
            actions.append(dict(copy.deepcopy(base),log_schema='action_only',lower=-.04,upper=.05,decision='unresolved'))
            receipts.append(dict(copy.deepcopy(base),log_schema='receipt_attribute',lower=target-.005,upper=target+.005,
                decision='capacity' if target>.005 else 'flexibility' if target<-.005 else 'unresolved',receipt_attribute_accuracy=1.))
    return {'action_reports':actions,'receipt_reports':receipts}


class ReceiptPlotTests(unittest.TestCase):
    def test_equal_budget_is_checked(self):
        data=fixture();data['receipt_reports'][0]['field_n']=81
        with self.assertRaises(ValueError):paired_reports(data)

    def test_no_product_utility_allowed_for_receipt(self):
        data=fixture();data['receipt_reports'][0]['mean_synthetic_regret']=0.
        with self.assertRaises(ValueError):paired_reports(data)

    def test_summary_uses_unique_domain_cohort_conditions(self):
        data=fixture()
        contextual=[dict(r,log_schema='context_and_receipt_attribute') for r in data['receipt_reports']]
        data['receipt_reports']+=contextual
        summary=comparison_summary(data)
        self.assertEqual(summary['field_receipt_count'],720)
        self.assertEqual(summary['selected_domain_cohort_conditions'],9)
        self.assertEqual(summary['receipt_attribute_accuracy'],1.)
        self.assertEqual(summary['original_action']['decisive_conditions'],0)
        self.assertEqual(summary['explicit_receipt']['decisive_conditions'],6)

    def test_receipt_figure_smoke(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)
            receipt_figure({'Synthetic fixture A':fixture(),'Synthetic fixture B':fixture()},output)
            for ext in ['pdf','png']:
                self.assertGreater((output/f'receipt-comparison.{ext}').stat().st_size,1000)


if __name__=='__main__':unittest.main()
