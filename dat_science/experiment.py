import datetime
import functools
import random
import time


def timed(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        return result, end - start
    return inner


class Result(object):

    def __init__(self, experiment, value=None, duration=None, problem=None):
        self.experiment = experiment
        self.value = value
        self.duration = duration
        self.problem = self.serialize_problem(problem)

    def is_alright(self):
        return self.problem is None

    @property
    def payload(self):
        return {
            "duration": self.duration,
            "value": self.experiment.clean(self.value),
            "problem": self.problem,
        }

    def serialize_problem(self, problem):
        return problem

    def __str__(self):
        return "Result {value}, in {duration} s, problems: {problem}".format(
            value=self.value,
            duration=self.duration,
            problem=self.problem
        )

    def __eq__(self, other):
        return self.experiment.compare(self, other)


def compare(this, that):
    return this.value == that.value and this.problem == that.problem


def cleanup(result_value):
    return result_value


class Experiment(object):

    """Wrapper for running experiments"""

    def __init__(self, name, control, new,
                 custom_compare=None, custom_clean=None):
        self.name = name
        self.control = control
        self.new = new
        self.control_result = None
        self.new_result = None
        self.compare = custom_compare or compare
        self.clean = custom_clean or cleanup

    def run(self, *args, **kwargs):
        self.control_result = self.observe(self.control, args, kwargs)

        if self.is_new_enabled(args, kwargs):
            self.new_result = self.observe(self.new, args, kwargs)

            timestamp = datetime.datetime.now().isoformat()
            payload = {
              "name": self.name,
              "timestamp": timestamp,
              "new": self.new_result.payload,
              "control": self.control_result.payload,
            }

            kind = self.evaluate()

            # publish results only if new way is also run
            self.publish(kind, payload)

        if self.control_result.is_alright():
            return self.control_result.value
        else:
            self.panic(self.control_result.problem)

    def panic(self, problem):
        exception, _ = problem
        raise exception

    def observe(self, function, args, kwargs):
        try:
            value, duration = timed(function)(*args, **kwargs)
            return Result(self, value=value, duration=duration)
        except Exception as e:
            import traceback
            problem = e, traceback.format_exc()
            return Result(self, problem=problem)

    def is_new_enabled(self, args, kwargs):
        return random.random() > 0.5

    def publish(self, kind, payload):
        print(kind, payload)

    def evaluate(self):
        if self.control_result == self.new_result:
            return "match"
        else:
            return "mismatch"

    def report(self):
        report_lines = ["-" * 60, "Experiment: {}".format(self.name), "-" * 60]
        report_lines.append("Control: {}".format(self.control_result))
        report_lines.append("New: {}".format(self.new_result))
        return "\n".join(report_lines)

