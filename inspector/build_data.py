#!/usr/bin/env python3
"""Build an offline viewer dataset from recorded analysis, never from API calls."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'inspector/data.js'
ATTRIBUTES = {
    'cloud': ['Processing capacity', 'Affordability', 'Portability', 'Technical support'],
    'travel': ['Schedule fit', 'Affordability', 'Change flexibility', 'Service support'],
    'workflow': ['Automation coverage', 'Affordability', 'Customizability', 'Implementation support'],
}
COHORT = {'positive': 'A', 'negative': 'B', 'near': 'C'}


def build():
    rows, sources = [], []
    for model in ['mini', 'nano']:
        primary_path = ROOT / f'results/model-study-{model}/analysis.json'
        receipt_path = ROOT / f'results/receipt-study-{model}/comparison.json'
        primary = json.loads(primary_path.read_text())
        receipt = json.loads(receipt_path.read_text())
        for p in [primary_path, receipt_path]:
            sources.append({'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
        groups = [(primary['reports'], {'action_only':'primary_action','context_and_action':'primary_context'}, primary_path),
                  (receipt['action_reports'], {'action_only':'matched_action'}, receipt_path),
                  (receipt['receipt_reports'], {'receipt_attribute':'receipt'}, receipt_path)]
        for records, schemas, source in groups:
            for r in records:
                if r['log_schema'] not in schemas:
                    continue
                d = r['known_synthetic_class_contrasts']
                for key, endpoint in [('lower_witness_population','lower'),('upper_witness_population','upper')]:
                    p = r[key]
                    assert len(p) == len(d) == 4
                    assert abs(sum(p)-1) < 1e-7 and min(p) >= -1e-7
                    assert abs(sum(x*y for x,y in zip(p,d))-r[endpoint]) < 1e-7
                schema = schemas[r['log_schema']]
                rows.append({
                    'id': ':'.join([model,r['domain'],COHORT[r['cohort']],schema]),
                    'model':model,'model_snapshot':primary['system'],'domain':r['domain'],
                    'cohort':COHORT[r['cohort']],'schema':schema,
                    'class_attributes':ATTRIBUTES[r['domain']],
                    'class_contrasts':d,'lower':r['lower'],'upper':r['upper'],'decision':r['decision'],
                    'lower_witness':[max(0.,x) for x in r['lower_witness_population']],
                    'upper_witness':[max(0.,x) for x in r['upper_witness_population']],
                    'calibration_n':r['calibration_n'],'field_n':r['field_n'],
                    'calibration_by_class':[sum(column) for column in zip(*r['channel_counts'])],
                    'field_failures':round(r['failure_rate']*r['field_n']),
                    'solver_violation':r['max_solver_constraint_violation'],
                    'source':str(source.relative_to(ROOT)),
                    'evidence_scope':'synthetic_profiles_and_outcomes_with_recorded_model_responses',
                    'followup':schema in ['receipt','matched_action'],
                })
    rows.sort(key=lambda r:r['id'])
    assert len(rows)==72 and len({r['id'] for r in rows})==72
    data={'version':'0.1.0','scope':'Offline inspector of precomputed results. No human participants.',
          'evaluation_truth_included':False,'rows':rows,'sources':sources}
    payload='window.INSPECTOR_DATA = '+json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+';\n'
    OUT.write_text(payload)
    print(f'Wrote {len(rows)} precomputed conditions; evaluation-only populations and targets omitted.')

if __name__ == '__main__':
    build()
