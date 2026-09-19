"""Synthetic delegated-choice benchmark. No record is a human participant.

Data generation, rather than model success, defines the task distribution.
All optional analyst access to private intent and utility is explicitly marked.
"""
import hashlib
import json
import numpy as np

DOMAINS = {
    'travel': ['schedule fit', 'affordability', 'change flexibility', 'service support'],
    'cloud': ['processing capacity', 'affordability', 'portability', 'technical support'],
    'workflow': ['automation coverage', 'affordability', 'customizability', 'implementation support'],
}
WEIGHTS = np.array([[.55,.20,.15,.10], [.15,.55,.20,.10],
                    [.15,.15,.55,.15], [.15,.15,.15,.55]])
TYPES = ['essential', 'performance', 'flexible', 'assisted']
REGIMES = ['ordinary', 'capacity_constrained', 'service_rich']
BASE = np.array([[.45,.87,.42,.35], [.86,.40,.50,.45],
                 [.57,.56,.86,.43], [.55,.50,.53,.87]])
SYSTEMS = {
    'direct': 'You are a delegated purchasing assistant. Select the available option with the highest stated customer utility. Return its option ID. Do not substitute your own preferences.',
    'concise': 'Make a practical recommendation for this customer. Use the stated utility rule and all supplied preferences. Return one option ID.',
}
POPULATIONS = {'positive':[.65,.10,.15,.10], 'negative':[.15,.10,.65,.10],
               'near':[.42,.18,.27,.13]}


def utility(features, intent):
    """Known simulated utility in [0,1], including a noncompensatory penalty."""
    f = np.asarray(features, dtype=float)
    scores = f @ WEIGHTS[intent]
    # All profiles have an explicit minimum for their most important attribute.
    return np.clip(scores - .30 * (f[..., intent] < .35), 0., 1.)


def menu(rng, regime):
    features = np.clip(BASE + rng.normal(0., .16, BASE.shape), .02, .98)
    if regime == 1:
        features[:, 0] = np.clip(features[:, 0] - .16, .02, .98)
    elif regime == 2:
        features[:, 3] = np.clip(features[:, 3] + .17, .02, .98)
    return np.round(features, 2)


def task(rng, domain, intent, split, index, policy='direct'):
    regime = int(rng.integers(len(REGIMES)))
    features = menu(rng, regime)
    order = rng.permutation(4)
    mapping = {chr(65+i): int(order[i]) for i in range(4)}
    scores = utility(features, intent)
    payload = {
        'domain': domain, 'market_context': REGIMES[regime],
        'attributes': DOMAINS[domain],
        'customer_preferences': {'weights': WEIGHTS[intent].tolist(),
            'minimum_attribute_index_zero_based': intent, 'minimum_score': .35},
        'utility_rule': 'Compute the weighted sum of four scores. Subtract 0.30 if the minimum attribute is below 0.35. Clip the result to [0,1]. Choose a utility maximizer. All other factors are equal.',
        'options': [{'id': key, 'product_type': TYPES[value], 'scores': features[value].tolist()}
                    for key, value in mapping.items()],
    }
    row = {'task_id': f'{domain}-{split}-{index:06d}', 'domain': domain,
           'split': split, 'regime': regime, 'policy': policy,
           'prompt': json.dumps(payload, sort_keys=True),
           'semantic_choice': {k: TYPES[v] for k,v in mapping.items()},
           'option_utilities': {k: float(scores[v]) for k,v in mapping.items()},
           'optimal_choices': [k for k,v in mapping.items() if np.isclose(scores[v], scores.max())],
           'private_intent': intent,
           'private_features': features.tolist()}
    return row


def request(row, model, max_output_tokens=256):
    return {'model': model, 'store': False, 'max_output_tokens': max_output_tokens,
        'input': [{'role': 'system', 'content': SYSTEMS[row['policy']]},
                  {'role': 'user', 'content': row['prompt']}],
        'text': {'format': {'type': 'json_schema', 'name': 'delegated_choice_v2',
            'strict': True, 'schema': {'type': 'object', 'properties': {
                'choice_id': {'type': 'string', 'enum': ['A','B','C','D']}},
                'required': ['choice_id'], 'additionalProperties': False}}}}


def outcome_bank(seed, size=4096):
    """Independent finite target population of future product menus.

    Contrast = utility under capacity investment minus utility under flexibility
    investment. Both improvements impose an identical affordability tradeoff.
    This is a known synthetic outcome, never an observed human outcome.
    """
    rng = np.random.default_rng(seed)
    bank = []
    for _ in range(size):
        f = menu(rng, int(rng.integers(3)))
        capacity, flexibility = f.copy(), f.copy()
        capacity[:, 0] = np.minimum(1., capacity[:, 0] + .16)
        flexibility[:, 2] = np.minimum(1., flexibility[:, 2] + .16)
        capacity[:, 1] = np.maximum(0., capacity[:, 1] - .05)
        flexibility[:, 1] = np.maximum(0., flexibility[:, 1] - .05)
        bank.append([float(utility(capacity,k).max()-utility(flexibility,k).max()) for k in range(4)])
    return np.array(bank)


def generate(seed=73912, calibration_per_class=40, field_size=160,
             outcome_audits=256, policy='direct', domains=None, populations=None):
    if min(calibration_per_class, field_size, outcome_audits) < 1:
        raise ValueError('Split sizes must be positive')
    if policy not in SYSTEMS:
        raise ValueError('Unknown policy')
    domains = list(DOMAINS) if domains is None else list(domains)
    if not domains or len(set(domains)) != len(domains) or any(d not in DOMAINS for d in domains):
        raise ValueError('Invalid domains')
    populations=list(POPULATIONS) if populations is None else list(populations)
    if not populations or len(set(populations))!=len(populations) or any(p not in POPULATIONS for p in populations):
        raise ValueError('Invalid populations')
    # Independent child streams: calibration, field, target bank, outcome sample.
    children = np.random.SeedSequence(seed).spawn(4 * len(domains))
    rows, outcomes, truths = [], {}, {}
    for di, domain in enumerate(domains):
        cal_rng, field_rng, bank_rng, outcome_rng = [np.random.default_rng(s)
            for s in children[4*di:4*di+4]]
        for k in range(4):
            for i in range(calibration_per_class):
                rows.append(task(cal_rng,domain,k,'calibration',k*calibration_per_class+i,policy))
        for cohort in populations:
            p=np.asarray(POPULATIONS[cohort])
            for i in range(field_size):
                k=int(field_rng.choice(4,p=p))
                row=task(field_rng,domain,k,'field',i,policy)
                row['task_id']=f'{domain}-field-{cohort}-{i:06d}'
                row['cohort']=cohort
                rows.append(row)
        bank = outcome_bank(int(bank_rng.integers(2**31)))
        sample = bank[outcome_rng.integers(len(bank),size=outcome_audits)]
        outcomes[domain] = {'contrast_samples': sample.tolist(),
            'known_class_contrasts':bank.mean(axis=0).tolist(),
            'scope': 'Synthetic product utilities sampled with replacement from an independent fixed target bank.'}
        truths[domain] = {'class_contrasts': bank.mean(axis=0).tolist(),
            'bank_size':len(bank),'cohorts':{cohort:{'population':POPULATIONS[cohort],
                'target_contrast':float(bank.mean(axis=0)@POPULATIONS[cohort])} for cohort in populations}}
    # Interleave intent, split and domain before API execution. This ordering seed
    # is independent of generation, and never controls the provider's randomness.
    np.random.default_rng(seed+901).shuffle(rows)
    return rows, outcomes, truths


def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def controls(rows, seed=191):
    rng = np.random.default_rng(seed)
    records = []
    for row in rows:
        choices = list(row['semantic_choice'])
        default = next(k for k,v in row['semantic_choice'].items() if v == 'essential')
        for name, choice in [('optimal',row['optimal_choices'][0]),
                             ('uniform_random',str(rng.choice(choices))),
                             ('always_essential',default)]:
            records.append({'task_id':row['task_id'], 'system':name,
                'choice_id':choice, 'source':'algorithmic_control'})
    return records
