asp-wrapper
===========


This repository provides a solution for a common scenario in which you have an answer set program in place that you wish
to run from within your Python code together with additional facts.
Such a program could, e.g., specify a fixed set of rules that you would like to employ for reasoning about different
scenarios that should be specified from within a Python application.
To that end, the package `aspwrapper` specifies an abstract base class,
[`BaseSolver`](src/main/python/aspwrapper/base_solver.py#L41),
for wrappers that encapsulate access to answer set solvers.
At the current time, there exists only one implementation of this base class for
[DLV](http://www.dlvsystem.com/dlv/),
yet similar wrappers for other solvers are straightforward to implement.


Installation
------------

This package can be installed via pip:
```
pip install git+https://github.com/riley-momo/asp-wrapper-new
```


How To Use It
-------------

Suppose that you would like to use the following very simple answer set program that specifies logical inference over
superheroes and villains, and which is stored in the local file `heroes.asp`:

```
% all superheros and villains are persons
person(P) :- superhero(P) .
person(P) :- villain(P)   .

% superheroes fight villains
superhero(S) :- fights(S, _) .
villain(V)   :- fights(_, V) .
```

Let's assume further that you would like to run this answer set program together with the fact `fights(batman,joker)`.
In this case, you could use the following code:  

```python
import aspwrapper

# create an instance representing the DLV solver
solver = aspwrapper.DlvSolver("/path/to/dlv/binary")

# a set of facts consisting of the single literal fights(batman, joker)
facts = [aspwrapper.Literal("fights", ["batman", "joker"])]

# this set of facts has one according answer set
answer_sets = solver.run("heroes.asp", facts)
for a in answer_sets:
    print(a)
```

The output of the code above is the following:

```
>>> for a in answer_sets:
...     print(a)
AnswerSet(
	facts      = { fights(batman,joker) },
	inferences = { villain(joker), person(joker), superhero(batman), person(batman) }
)
```

If you would like to try this by yourself, then have a look at the [`examples`](examples) folder, which contains the
code for this very example.
