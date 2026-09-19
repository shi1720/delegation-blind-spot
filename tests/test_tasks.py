import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from delegation_blind_spot.tasks import make_tasks, parse_response, request_body


class TaskValidation(unittest.TestCase):
    def test_semantic_winner_is_invariant_to_order(self):
        tasks = make_tasks(1)
        self.assertEqual(len(tasks), 72)
        self.assertEqual(len({t['id'] for t in tasks}), len(tasks))
        for task in tasks:
            expected = 'balanced' if task['menu'] == 'pooled' else task['intent'].split('_')[0]
            self.assertEqual(task['semantic_choice'][task['optimal_choice']], expected)
            self.assertEqual(len(set(task['semantic_choice'].values())), 3)

    def test_balanced_position_controls(self):
        positions = [t['optimal_choice'] for t in make_tasks(1)
                     if t['domain'] == 'travel' and t['menu'] == 'pooled' and t['intent'] == 'first_priority']
        self.assertEqual([positions.count(k) for k in 'ABC'], [2,2,2])

    def test_response_parsing_does_not_count_incomplete_or_refused_as_choice(self):
        valid = {'status': 'completed', 'output': [{'type': 'message', 'content': [
            {'type': 'output_text', 'text': json.dumps({'choice_id': 'B'})}]}]}
        self.assertEqual(parse_response(valid), 'B')
        for bad in [{'status': 'incomplete', 'output': valid['output']},
                    {'status': 'completed', 'output': []},
                    {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'refusal'}]}]}]:
            with self.assertRaises(ValueError):
                parse_response(bad)

    def test_request_does_not_leak_evaluation_labels(self):
        task = make_tasks(1)[0]
        body = request_body(task, 'declared-model')
        self.assertNotIn('optimal_choice', json.dumps(body))
        self.assertNotIn('semantic_choice', json.dumps(body))
        self.assertFalse(body['store'])
        self.assertEqual(body['model'], 'declared-model')


if __name__ == '__main__':
    unittest.main()
