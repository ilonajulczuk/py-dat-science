# dat-science for python

Github [dat-science ruby library](https://github.com/github/dat-science).

`some_file.py`:

```
def compute_something(a, b, x):
    import time
    print('taking a nap...')
    time.sleep(2)
    return a + b * x


def compute_alternatively(a, b, x):
    print('hard working, effective computation')
    return a + b * x
```

`usage.py`:

```
from experiment import Experiment

experiment = Experiment('silly example', compute_something,
                        compute_alternatively)

result = experiment.run(1, 2, 3)
print(experiment.report())
```
