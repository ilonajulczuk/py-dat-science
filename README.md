# dat-science for python

Small Python for refactoring critical chunks of your code.
Helps trying out new solutions fast in production environment using science.

Refactoring can be risky, code may turn out to be buggy or give different
results than the previous one or just be slower than previous version.

We want
[to move fast and break nothing](http://zachholman.com/talk/move-fast-break-nothing/), right?

This small utility library can help you do just that... with science!
In experiment we run both control code (old one) and new one. User gets
the results from the control code, so nothing changes. Under the cover
running times, values and possible problems from both code paths are
recorded and published. This usefull data can be send to your mongodb, statsd,
redis, keen.io... you get the idea. Try out new things fast, observe them in
production not breaking anything, collect data and make an informed decision.

It's insipired by Github [dat-science ruby library](https://github.com/github/dat-science),
but implemented in pure python, so it can be used in python codebase.

# Installation

1. clone this repository
2. Run setup.py
```
$ python setup.py install
```
3. Check installation
```
import dat_science
```

# How to use it?

Usually the first you should do is to import Experiment class, initialized
with name of experiment and two callables (object with `__call__`, function or lambda):
 - control code
 - new code

## Simple example

```
from dat_science.experiment import Experiment

experiment = Experiment('try out dat-science', control=lambda x: x,
                        new=lambda x: x.upper())

experiment.run('hello!')
print experiment.report()

```

## What can it does exactly?

First, we create an experiment with two code paths, 
it would cause to big overhead if new code was run every time,
so we check `is_new_enabled` and if it's true, new code is run.

You can customize it by inheriting from Experiment class.
Code is `observed` - exceptions are catched and results compared
 and information about experiment gets published.
There can be two kind of events - `match` or `mismatch`.



## How to extend it in your own code?

You should overload `publish` method
```
from dat_science.experiment import Experiment

class MyExperiment(Experiment):
    def publish(self, event, payload):
        # ... publish to your analytics backend

experiment = MyExperiment('my own', do_something, do_it_new_way) 

```

It's very simple. To learn more you can take a peek into examples.py or tests.py.

