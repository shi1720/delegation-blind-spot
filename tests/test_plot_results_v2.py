import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments/v2'))
from plot_results import aggregate_performance, execution_summary, forest_figure, competence_figure


class PublicationPlotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.directory=Path(self.tmp.name)

    def tearDown(self): self.tmp.cleanup()

    def fixture(self):
        tasks=[{'task_id':str(i),'split':'field','semantic_choice':{'A':'essential'}} for i in range(4)]
        records=[]
        for i in range(4):
            records.append({'event':'attempt','task_id':str(i)})
            result={'event':'result','task_id':str(i),'elapsed_seconds':1.}
            if i<2:
                result.update({'choice_id':'A','model_returned':'test-model','usage':{
                    'input_tokens':100,'input_tokens_details':{'cached_tokens':20},'output_tokens':10,'total_tokens':110}})
            else: result['error']={'type':'TimeoutError' if i==2 else 'ConnectionResetError'}
            records.append(result)
        (self.directory/'tasks.jsonl').write_text(''.join(json.dumps(t)+'\n' for t in tasks))
        (self.directory/'responses.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
        (self.directory/'manifest.json').write_text(json.dumps({'task_count':4,'model_requested':'test-model'}))
        (self.directory/'analysis.json').write_text('{}')
        return records

    def test_usage_failures_and_cost_not_silently_dropped(self):
        self.fixture()
        pricing={'test-model':{'input_per_million':.75,'cached_input_per_million':.075,'output_per_million':4.5,'source':'fixture'}}
        report=execution_summary(self.directory,pricing)
        self.assertEqual(report['final_results'],4)
        self.assertEqual(report['valid_choices'],2)
        self.assertEqual(report['failures'],2)
        self.assertEqual(report['timeout_failures'],1)
        self.assertEqual(report['connection_reset_failures'],1)
        self.assertEqual(report['requests_without_reported_usage'],2)
        self.assertAlmostEqual(report['cost']['reported_usage_estimate_usd'],.000213)

    def test_incomplete_or_duplicate_run_rejected(self):
        records=self.fixture()
        path=self.directory/'responses.jsonl'
        path.write_text(''.join(json.dumps(r)+'\n' for r in records[:-1]))
        with self.assertRaises(ValueError): execution_summary(self.directory)
        path.write_text(''.join(json.dumps(r)+'\n' for r in records+[records[-1]]))
        with self.assertRaises(ValueError): execution_summary(self.directory)

    def test_no_double_counting_field_rows_across_schemas(self):
        reports=[]
        for cohort,n,rate in [('positive',10,.5),('negative',30,1.)]:
            row={'domain':'cloud','cohort':cohort,'field_n':n,'log_schema':'action_only',
                 'optimal_choice_rate':rate,'mean_synthetic_regret':.1,'mean_synthetic_utility':.7,'failure_rate':.1}
            reports.extend([row,dict(row,log_schema='context_and_action')])
        result=aggregate_performance({'reports':reports})
        self.assertEqual(result['all']['field_n'],40)
        self.assertAlmostEqual(result['all']['optimal_choice_rate'],.875)

    def test_publication_figure_smoke_with_explicit_fixture(self):
        reports=[]
        for domain in ['travel','cloud','workflow']:
            for cohort in ['positive','negative','near']:
                for schema in ['action_only','context_and_action']:
                    reports.append({'domain':domain,'cohort':cohort,'log_schema':schema,'field_n':10,
                        'lower':-.04,'upper':.08,'evaluation_only':{'true_contrast':.02},
                        'optimal_choice_rate':.9,'mean_synthetic_regret':.01,'mean_synthetic_utility':.7,'failure_rate':.1})
        analyses={'Synthetic fixture A':{'reports':reports},'Synthetic fixture B':{'reports':copy.deepcopy(reports)}}
        forest_figure(analyses,self.directory)
        competence_figure(analyses,self.directory)
        for name in ['decision-intervals','task-performance']:
            for extension in ['pdf','png']:
                self.assertGreater((self.directory/f'{name}.{extension}').stat().st_size,1000)


if __name__=='__main__': unittest.main()
