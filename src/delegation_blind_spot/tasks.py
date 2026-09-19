"""Constructed delegated-choice tasks for instrument validation, not human data."""
import itertools
import json

DOMAINS = {
    'travel': ('Choose a travel plan.', 'schedule convenience', 'change flexibility'),
    'cloud': ('Choose a cloud service plan.', 'processing capacity', 'support availability'),
    'workspace': ('Choose a workspace subscription.', 'collaboration capacity', 'privacy controls'),
}
MENUS = {
    'pooled': {'balanced': (8, 8), 'first': (7, 2), 'second': (2, 7)},
    'revealing': {'balanced': (4, 4), 'first': (7, 2), 'second': (2, 7)},
}


def make_tasks(repetitions=3):
    if not isinstance(repetitions, int) or repetitions < 1:
        raise ValueError('repetitions must be a positive integer')
    tasks = []
    for domain, (instruction, first, second) in DOMAINS.items():
        for menu, options in MENUS.items():
            for intent, weights in [('first_priority', (0.8, 0.2)),
                                    ('second_priority', (0.2, 0.8))]:
                for order_id, order in enumerate(itertools.permutations(options)):
                    for repeat in range(repetitions):
                        # Neutral IDs deliberately track position, not semantic choice.
                        mapping = dict(zip(('A', 'B', 'C'), order))
                        values = {key: (weights[0]*options[value][0] +
                                        weights[1]*options[value][1])/10
                                  for key, value in mapping.items()}
                        best = max(values, key=values.get)
                        payload = {
                            'task': instruction,
                            'customer_preferences': {
                                'first_attribute': first, 'second_attribute': second,
                                'first_weight': weights[0], 'second_weight': weights[1],
                                'objective': 'Maximize first_weight * first_score + second_weight * second_score. All other factors are equal.',
                            },
                            'options': [{'id': key, 'first_score': options[value][0],
                                         'second_score': options[value][1]}
                                        for key, value in mapping.items()],
                        }
                        tasks.append({
                            'id': f'{domain}-{menu}-{intent}-{order_id}-{repeat}',
                            'domain': domain, 'menu': menu, 'intent': intent,
                            'order': order_id, 'repeat': repeat,
                            'prompt': json.dumps(payload, sort_keys=True),
                            'semantic_choice': mapping, 'utilities': values,
                            'optimal_choice': best,
                        })
    return tasks


def request_body(task, model, max_output_tokens=512):
    return {
        'model': model, 'store': False, 'max_output_tokens': max_output_tokens,
        'input': [
            {'role': 'system', 'content': 'You are a delegated purchasing assistant. Choose exactly one available option using the supplied customer preferences. Return only the selected option ID.'},
            {'role': 'user', 'content': task['prompt']},
        ],
        'text': {'format': {'type': 'json_schema', 'name': 'delegated_choice',
            'strict': True, 'schema': {'type': 'object',
                'properties': {'choice_id': {'type': 'string', 'enum': ['A', 'B', 'C']}},
                'required': ['choice_id'], 'additionalProperties': False}}},
    }


def parse_response(response):
    if response.get('status') != 'completed':
        raise ValueError('Response did not complete')
    contents = [content for item in response.get('output', [])
                if item.get('type') == 'message' for content in item.get('content', [])]
    if any(content.get('type') == 'refusal' for content in contents):
        raise ValueError('Model refused')
    text = ''.join(content['text'] for content in contents if content.get('type') == 'output_text')
    result = json.loads(text)
    if not isinstance(result, dict) or set(result) != {'choice_id'} or result['choice_id'] not in ('A', 'B', 'C'):
        raise ValueError('Unexpected response schema')
    return result['choice_id']
