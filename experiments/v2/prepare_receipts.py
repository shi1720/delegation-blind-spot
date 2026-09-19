#!/usr/bin/env python3
"""Freeze an exploratory explicit-preference measurement extension.

Selections use only predeclared task strata and lexicographic IDs. The model
reports already supplied synthetic weights; it does not supply human feedback.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import platform
from benchmark import TYPES, digest
from analyze import load_jsonl


def selected_subset(rows,calibration_per_class=40,field_per_cohort=80):
    if min(calibration_per_class,field_per_cohort)<1:
        raise ValueError('Positive subset sizes are required')
    groups=defaultdict(list)
    for row in rows:
        if row['split']=='calibration': key=(row['domain'],'calibration',row['private_intent'])
        elif row['split']=='field': key=(row['domain'],'field',row['cohort'])
        else: raise ValueError('Unknown source split')
        groups[key].append(row)
    chosen=[]
    for key,group in sorted(groups.items()):
        n=calibration_per_class if key[1]=='calibration' else field_per_cohort
        if len(group)<n: raise ValueError('Source stratum is smaller than the predeclared subset')
        chosen.extend(sorted(group,key=lambda r:r['task_id'])[:n])
    # Retain the source's frozen randomized execution order, not outcome order.
    chosen_ids={r['task_id'] for r in chosen}
    return [r for r in rows if r['task_id'] in chosen_ids]


def receipt_task(source):
    supplied=json.loads(source['prompt'])
    weights=supplied['customer_preferences']['weights']
    if len(weights)!=4 or len(set(weights))<2:
        raise ValueError('Expected the source benchmark four-attribute preference task')
    maximum=max(weights)
    if sum(w==maximum for w in weights)!=1: raise ValueError('Ambiguous highest supplied preference')
    expected=chr(65+weights.index(maximum))
    payload={'domain':source['domain'],'customer_supplied_preferences':[
        {'attribute_id':chr(65+i),'attribute_name':name,'weight':weights[i]}
        for i,name in enumerate(supplied['attributes'])],
        'question':'Which attribute has the largest customer-supplied weight? Report its attribute_id. This is a preference receipt, not a recommendation of any offer.'}
    result={key:source[key] for key in ['task_id','domain','split','regime','private_intent']}
    if 'cohort' in source: result['cohort']=source['cohort']
    result.update({'policy':'explicit_preference_receipt','measurement_kind':'explicit_preference_receipt',
        'prompt':json.dumps(payload,sort_keys=True),
        # Existing LP code indexes these four category names. Here they are
        # category aliases only, not chosen products or utilities.
        'semantic_choice':dict(zip('ABCD',TYPES)),
        'receipt_attribute_mapping':dict(zip('ABCD',range(4))),
        'optimal_choices':[expected],
        'option_utilities':dict.fromkeys('ABCD',0.),
        'utility_scope':'Zero placeholders required by the shared analysis adapter. No product-choice utility is measured or reported for receipts.',
        'source_task_sha256':digest(source)})
    return result


def receipt_request(row,model):
    return {'model':model,'store':False,'max_output_tokens':256,
        'reasoning':{'effort':'none'},
        'input':[{'role':'system','content':'Return an accurate receipt of the customer preferences supplied in the user message. Report the ID of the attribute with the highest supplied weight. Do not choose a product or infer preferences not supplied.'},
                 {'role':'user','content':row['prompt']}],
        'text':{'format':{'type':'json_schema','name':'explicit_preference_receipt','strict':True,
            'schema':{'type':'object','properties':{'choice_id':{'type':'string','enum':['A','B','C','D']}},
                'required':['choice_id'],'additionalProperties':False}}}}


def write_json(path,data): path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def prepare(source,output,calibration_per_class=40,field_per_cohort=80):
    source,output=Path(source),Path(output)
    manifest=json.loads((source/'manifest.json').read_text())
    original=load_jsonl(source/'tasks.jsonl')
    if digest(original)!=manifest['tasks_sha256']: raise ValueError('Source tasks do not match frozen manifest')
    selected=selected_subset(original,calibration_per_class,field_per_cohort)
    rows=[receipt_task(row) for row in selected]
    outcomes=json.loads((source/'outcomes.json').read_text())
    truth=json.loads((source/'evaluation-truth.json').read_text())
    if digest(outcomes)!=manifest['outcomes_sha256'] or digest(truth)!=manifest['evaluation_truth_sha256']:
        raise ValueError('Source outcomes do not match frozen manifest')
    output.mkdir(parents=True,exist_ok=False)
    for filename,records in [('tasks.jsonl',rows),('source-action-tasks.jsonl',selected),
            ('requests.jsonl',[{'task_id':r['task_id'],'request':receipt_request(r,manifest['model_requested'])} for r in rows])]:
        (output/filename).write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in records))
    write_json(output/'outcomes.json',outcomes)
    write_json(output/'evaluation-truth.json',truth)
    write_json(output/'manifest.json',{'benchmark':'delegation-explicit-receipt-extension',
        'design':'Exploratory follow-up prompted by unresolved primary benchmark intervals; frozen before receipt API calls.',
        'scope':'Reports of already supplied synthetic preference weights. Zero human participants. No privacy or customer-validation claim.',
        'mode':'prepared_only','model_requested':manifest['model_requested'],'task_count':len(rows),
        'distinct_receipt_prompts':len({r['prompt'] for r in rows}),
        'prompt_diversity_scope':'Repeated extraction from four supplied weight profiles in three domain framings, not 1200 distinct customer decisions.',
        'calibration_per_class':calibration_per_class,'field_per_cohort':field_per_cohort,
        'selection_rule':'First lexicographic task IDs within domain/class calibration strata and domain/cohort field strata; preserve original execution order.',
        'source_directory':str(source),'source_tasks_sha256':digest(original),'source_action_subset_sha256':digest(selected),
        'selected_task_ids_sha256':digest([r['task_id'] for r in rows]),
        'tasks_sha256':digest(rows),'outcomes_sha256':digest(outcomes),'evaluation_truth_sha256':digest(truth),
        'outcome_scope':'Primary outcome contrasts are exactly known in the original independent finite synthetic bank.',
        'comparison':'Same selected task IDs and calibration/field budgets from existing original action records. No original API call is rerun.',
        'uncertainty_budget':{'channel':.02,'field':.02,'outcome':.01},
        'python':platform.python_version(),'source_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(Path(__file__).parent.glob('*.py'))}})
    return len(rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--calibration-per-class',type=int,default=40)
    p.add_argument('--field-per-cohort',type=int,default=80)
    a=p.parse_args()
    count=prepare(a.source,a.output,a.calibration_per_class,a.field_per_cohort)
    print(f'Frozen {count} explicit-preference receipt requests. No model was called and no human data was collected.')


if __name__=='__main__': main()
