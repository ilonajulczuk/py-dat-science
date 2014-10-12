import time
import random
import functools


def timed(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        return result, end - start
    return inner


class Result(object):

    def __init__(self, value=None, execution_time=None, problem=None):
        self.value = value
        self.execution_time = execution_time
        self.problem = problem

    def is_alright(self):
        return self.problem is None

    def __str__(self):
        return "Result {value}, in {execution_time} s, problems: {problem}".format(
            value=self.value,
            execution_time=self.execution_time,
            problem=self.problem
        )


class Experiment(object):

    """Wrapper for running experiments"""

    def __init__(self, name, control, new):
        self.name = name
        self.control = control
        self.new = new
        self.control_result = None
        self.new_result = None

    def run(self, *args, **kwargs):
        self.control_result = self.observe(self.control, args, kwargs)

        if self.is_new_enabled(args, kwargs):
            self.new_result = self.observe(self.new, args, kwargs)

            # publish results only if new way is also run
            self.publish()

        if self.control_result.is_alright():
            return self.control_result.value
        else:
            self.panic(self.control_result.problem)

    def panic(self, problem):
        exception, _ = problem
        raise exception

    def observe(self, function, args, kwargs):
        try:
            value, execution_time = timed(function)(*args, **kwargs)
            return Result(value=value, execution_time=execution_time)
        except Exception as e:
            import traceback
            problem = e, traceback.format_exc()
            return Result(problem=problem)

    def is_new_enabled(self, args, kwargs):
        return random.random() > 0.5

    def publish(self):
        print(self.report())

    def report(self):
        report_lines = ["-" * 60, "Experiment: {}".format(self.name), "-" * 60]
        report_lines.append("Control: {}".format(self.control_result))
        report_lines.append("New: {}".format(self.new_result))
        return "\n".join(report_lines)
