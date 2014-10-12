import unittest
from experiment import Experiment


class MyExperiment(Experiment):
    published = None

    def publish(self, event, payload):
        """Append experiment info to published list"""
        if self.published is None:
            self.published = []

        self.published.append((event, payload))

    def is_new_enabled(self, args, kwargs):
        return True


def raise_error(x):
    raise ValueError('test')


class TestExperiment(unittest.TestCase):

    def test_returns_control_result(self):
        experiment = MyExperiment('test', control=lambda x: x * 3,
                                  new=lambda x: x * 3 -1)
        result = experiment.run(1)
        self.assertEqual(result, 3)

    def test_swallow_exceptions_from_candidate_code(self):
        """New code shouldn't disrupt user experience"""


        experiment = MyExperiment('test', control=lambda x: x * 3,
                                  new=raise_error)

        experiment.run(1)

    def test_cant_swallow_exceptions_from_control_code(self):
        """We shouldn't interfere how control code is run"""

        experiment = MyExperiment('test', control=raise_error,
                                  new=lambda x: x)

        self.assertRaises(ValueError, experiment.run, (1,))

    def test_if_results_are_published(self):
        experiment = MyExperiment('test', control=lambda x: x * 3,
                                  new=lambda x: 3 * x)

        result = experiment.run(1)
        result = experiment.run(2)
        result = experiment.run(3)

        self.assertEqual(len(experiment.published), 3)

    def test_if_same_results_are_match(self):
        experiment = MyExperiment('test', control=lambda x: x * 3,
                                  new=lambda x: 3 * x)

        result = experiment.run(3)

        self.assertEqual(experiment.published[0][0], 'match')

    def test_if_different_results_are_mismatch(self):
        experiment = MyExperiment('test', control=lambda x: x * 3,
                                  new=lambda x: 3 * x + 1)

        result = experiment.run(3)

        self.assertEqual(experiment.published[0][0], 'mismatch')

    def test_if_equal_using_custom_compare(self):
        experiment = MyExperiment('test', control=lambda x: 'a' + x,
                                  new=lambda x: 'A' + x,
                                  custom_compare=lambda x, y: x.value.lower() == y.value.lower())

        result = experiment.run('test')
        self.assertEqual(experiment.published[0][0], 'match')

    def test_custom_cleanup_for_experiment_data(self):
        experiment = MyExperiment('test', control=lambda x: x,
                                  new=lambda x: x,
                                  custom_clean=lambda result: result['test'])

        result = experiment.run({'test': True, 'other_data': 42})
        self.assertEqual(experiment.published[0][1]['control']['value'], True)

    def test_if_all_key_in_recorded_payload(self):
        payload_keys = {"name", "timestamp", "new", "control"}

        experiment = MyExperiment('test', control=lambda x: x,
                                  new=lambda x: x)

        result = experiment.run(1)
        self.assertEqual(set(experiment.published[0][1].keys()), payload_keys)

    def test_logs_exceptions_from_code(self):
        """New code shouldn't disrupt user experience"""

        experiment = MyExperiment('test', control=raise_error,
                                  new=raise_error)
        try:
            experiment.run(1)
        except ValueError:
            self.assertEquals(len(experiment.published), 1)
            self.assertIsNotNone(experiment.published[0][1]['new']['problem'])
            self.assertIsNotNone(experiment.published[0][1]['control']['problem'])


if __name__ == '__main__':
    unittest.main()
