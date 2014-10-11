from experiment import Experiment


def compute_something(a, b, x):
    import time
    print('taking a nap...')
    time.sleep(2)
    return a + b * x


def compute_alternatively(a, b, x):
    print('hard working, effective computation')
    return a + b * x


experiment = Experiment('silly example', compute_something,
                        compute_alternatively)

result = experiment.run(1, 2, 3)
print(experiment.report())
